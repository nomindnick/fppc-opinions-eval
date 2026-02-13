"""
Validates eval/dataset.json against the FPPC Opinions Search Evaluation spec.

Checks schema, referential integrity, coverage, score distribution,
uniqueness, and completeness. Exits 0 on pass, 1 on failure.

Usage:
    python src/validate_dataset.py --dataset eval/dataset.json [--data-dir data/extracted]
"""

import argparse
import json
import os
import sys


VALID_QUERY_TYPES = {"keyword", "natural_language", "fact_pattern"}
VALID_SCORES = {0, 1, 2}
EXPECTED_TOPICS = {
    "conflicts_of_interest",
    "campaign_finance",
    "gifts_honoraria",
    "lobbying",
    "other",
}
MIN_JUDGMENTS_PER_QUERY = 10
MIN_QUERIES = 60
MAX_QUERIES = 80


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def collect_opinion_ids(data_dir: str) -> set[str]:
    """Walk data_dir/{year}/*.json and return the set of opinion IDs (filename minus .json)."""
    ids = set()
    for year_dir in os.listdir(data_dir):
        year_path = os.path.join(data_dir, year_dir)
        if not os.path.isdir(year_path):
            continue
        for fname in os.listdir(year_path):
            if fname.endswith(".json"):
                ids.add(fname[:-5])
    return ids


# ---------------------------------------------------------------------------
# Validation functions — each returns a list of error strings
# ---------------------------------------------------------------------------

def validate_schema(dataset: dict) -> list[str]:
    """Check required fields present with correct types, valid score and query type values."""
    errors = []

    # Top-level fields
    for field in ("version", "taxonomy", "queries"):
        if field not in dataset:
            errors.append(f"Missing top-level field: '{field}'")

    if "version" in dataset and not isinstance(dataset["version"], str):
        errors.append(f"'version' must be a string, got {type(dataset['version']).__name__}")

    if "taxonomy" in dataset and not isinstance(dataset["taxonomy"], dict):
        errors.append(f"'taxonomy' must be a dict, got {type(dataset['taxonomy']).__name__}")

    if "queries" in dataset and not isinstance(dataset["queries"], list):
        errors.append(f"'queries' must be a list, got {type(dataset['queries']).__name__}")

    # Taxonomy structure
    taxonomy = dataset.get("taxonomy", {})
    for topic_id, topic in taxonomy.items():
        if not isinstance(topic, dict):
            errors.append(f"Taxonomy topic '{topic_id}' must be a dict")
            continue
        for field in ("name", "issues"):
            if field not in topic:
                errors.append(f"Taxonomy topic '{topic_id}' missing field: '{field}'")
        issues = topic.get("issues", [])
        if not isinstance(issues, list):
            errors.append(f"Taxonomy topic '{topic_id}' issues must be a list")
            continue
        for issue in issues:
            for field in ("id", "name", "description"):
                if field not in issue:
                    errors.append(f"Taxonomy issue in '{topic_id}' missing field: '{field}'")

    # Query structure
    for query in dataset.get("queries", []):
        if not isinstance(query, dict):
            errors.append("Query must be a dict")
            continue
        qid = query.get("id", "?")
        for field in ("id", "text", "type", "topic", "issue", "relevance_judgments"):
            if field not in query:
                errors.append(f"Query '{qid}' missing field: '{field}'")

        qtype = query.get("type")
        if qtype is not None and qtype not in VALID_QUERY_TYPES:
            errors.append(f"Query '{qid}' has invalid type: '{qtype}'")

        judgments = query.get("relevance_judgments", [])
        if not isinstance(judgments, list):
            errors.append(f"Query '{qid}' relevance_judgments must be a list")
            continue
        for j in judgments:
            if not isinstance(j, dict):
                errors.append(f"Query '{qid}' has non-dict judgment")
                continue
            for field in ("opinion_id", "score", "rationale"):
                if field not in j:
                    errors.append(f"Query '{qid}' judgment missing field: '{field}'")
            score = j.get("score")
            if score is not None and score not in VALID_SCORES:
                errors.append(f"Query '{qid}' has invalid score: {score}")

    return errors


def validate_referential_integrity(dataset: dict, data_dir: str) -> list[str]:
    """Check that every opinion_id in judgments and example_opinion_ids exists on disk."""
    errors = []

    if not os.path.isdir(data_dir):
        return errors  # caller handles the warning

    corpus_ids = collect_opinion_ids(data_dir)

    # Check judgment opinion IDs
    for query in dataset.get("queries", []):
        qid = query.get("id", "?")
        for j in query.get("relevance_judgments", []):
            oid = j.get("opinion_id")
            if oid and oid not in corpus_ids:
                errors.append(f"Query '{qid}' judgment references missing opinion: '{oid}'")

    # Check taxonomy example_opinion_ids
    for topic_id, topic in dataset.get("taxonomy", {}).items():
        for issue in topic.get("issues", []):
            for oid in issue.get("example_opinion_ids", []):
                if oid not in corpus_ids:
                    errors.append(
                        f"Taxonomy '{topic_id}/{issue.get('id', '?')}' "
                        f"example_opinion_id missing: '{oid}'"
                    )

    return errors


def validate_coverage(dataset: dict) -> list[str]:
    """Check issue coverage and minimum judgment counts."""
    errors = []

    queries = dataset.get("queries", [])
    num_queries = len(queries)
    if num_queries < MIN_QUERIES or num_queries > MAX_QUERIES:
        errors.append(f"Expected {MIN_QUERIES}-{MAX_QUERIES} queries, got {num_queries}")

    # Every taxonomy issue must have at least 1 query
    taxonomy = dataset.get("taxonomy", {})
    issue_ids = set()
    for topic in taxonomy.values():
        for issue in topic.get("issues", []):
            issue_ids.add(issue["id"])

    query_issues = {q.get("issue") for q in queries}
    uncovered = issue_ids - query_issues
    if uncovered:
        errors.append(f"Taxonomy issues with no queries: {sorted(uncovered)}")

    # Every query must have >= MIN_JUDGMENTS_PER_QUERY judgments
    for query in queries:
        qid = query.get("id", "?")
        num_j = len(query.get("relevance_judgments", []))
        if num_j < MIN_JUDGMENTS_PER_QUERY:
            errors.append(f"Query '{qid}' has {num_j} judgments (minimum {MIN_JUDGMENTS_PER_QUERY})")

    return errors


def validate_score_distribution(dataset: dict) -> tuple[list[str], list[str]]:
    """Check score distribution. Returns (errors, warnings)."""
    errors = []
    warnings = []

    total_judgments = 0
    total_score2 = 0

    for query in dataset.get("queries", []):
        qid = query.get("id", "?")
        judgments = query.get("relevance_judgments", [])
        scores = [j.get("score", 0) for j in judgments]
        num_score2 = sum(1 for s in scores if s == 2)
        total_judgments += len(scores)
        total_score2 += num_score2

        if num_score2 == 0:
            errors.append(f"Query '{qid}' has zero score-2 opinions")
        elif num_score2 < 3:
            warnings.append(f"Query '{qid}' has only {num_score2} score-2 opinions (recommend >= 3)")

    if total_judgments > 0:
        proportion = total_score2 / total_judgments
        if proportion < 0.20:
            warnings.append(
                f"Overall score-2 proportion is {proportion:.1%} (< 20%)"
            )
        elif proportion > 0.60:
            warnings.append(
                f"Overall score-2 proportion is {proportion:.1%} (> 60%)"
            )

    return errors, warnings


def validate_uniqueness(dataset: dict) -> list[str]:
    """Check for duplicate query IDs and duplicate opinion IDs within queries."""
    errors = []

    query_ids = []
    for query in dataset.get("queries", []):
        qid = query.get("id", "?")
        query_ids.append(qid)

        opinion_ids = []
        for j in query.get("relevance_judgments", []):
            opinion_ids.append(j.get("opinion_id"))
        dupes = [oid for oid in opinion_ids if opinion_ids.count(oid) > 1]
        if dupes:
            errors.append(f"Query '{qid}' has duplicate opinion IDs: {sorted(set(dupes))}")

    dupe_qids = [qid for qid in query_ids if query_ids.count(qid) > 1]
    if dupe_qids:
        errors.append(f"Duplicate query IDs: {sorted(set(dupe_qids))}")

    return errors


def validate_completeness(dataset: dict) -> list[str]:
    """Check that all expected topics are present and queries reference valid taxonomy entries."""
    errors = []

    taxonomy = dataset.get("taxonomy", {})
    present_topics = set(taxonomy.keys())

    missing_topics = EXPECTED_TOPICS - present_topics
    if missing_topics:
        errors.append(f"Missing expected topics: {sorted(missing_topics)}")

    for topic_id, topic in taxonomy.items():
        issues = topic.get("issues", [])
        if len(issues) == 0:
            errors.append(f"Topic '{topic_id}' has no issues")

    # Build valid topic -> issue mapping
    valid_issues = {}
    for topic_id, topic in taxonomy.items():
        valid_issues[topic_id] = {issue["id"] for issue in topic.get("issues", [])}

    for query in dataset.get("queries", []):
        qid = query.get("id", "?")
        qtopic = query.get("topic")
        qissue = query.get("issue")

        if qtopic and qtopic not in taxonomy:
            errors.append(f"Query '{qid}' references nonexistent topic: '{qtopic}'")
        elif qtopic and qissue and qissue not in valid_issues.get(qtopic, set()):
            errors.append(
                f"Query '{qid}' references nonexistent issue '{qissue}' in topic '{qtopic}'"
            )

    return errors


def validate_all(dataset: dict, data_dir: str | None = None) -> tuple[list[str], list[str]]:
    """Run all validations. Returns (errors, warnings)."""
    errors = []
    warnings = []

    errors.extend(validate_schema(dataset))
    errors.extend(validate_coverage(dataset))
    errors.extend(validate_uniqueness(dataset))
    errors.extend(validate_completeness(dataset))

    dist_errors, dist_warnings = validate_score_distribution(dataset)
    errors.extend(dist_errors)
    warnings.extend(dist_warnings)

    if data_dir:
        if os.path.isdir(data_dir):
            errors.extend(validate_referential_integrity(dataset, data_dir))
        else:
            warnings.append(f"Data directory not found: '{data_dir}' — skipping referential integrity check")

    return errors, warnings


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Validate FPPC Opinions Search Evaluation Dataset"
    )
    parser.add_argument(
        "--dataset",
        required=True,
        help="Path to eval dataset JSON file",
    )
    parser.add_argument(
        "--data-dir",
        default=None,
        help="Path to extracted opinion data (e.g., data/extracted)",
    )
    args = parser.parse_args()

    with open(args.dataset) as f:
        dataset = json.load(f)

    errors, warnings = validate_all(dataset, args.data_dir)

    if warnings:
        print(f"\n{len(warnings)} warning(s):")
        for w in warnings:
            print(f"  WARNING: {w}")

    if errors:
        print(f"\n{len(errors)} error(s):")
        for e in errors:
            print(f"  ERROR: {e}")
        print(f"\nValidation FAILED ({len(errors)} errors, {len(warnings)} warnings)")
        sys.exit(1)
    else:
        print(f"\nValidation PASSED (0 errors, {len(warnings)} warnings)")
        sys.exit(0)


if __name__ == "__main__":
    main()
