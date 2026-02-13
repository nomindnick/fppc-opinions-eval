"""Unit tests for the dataset validation module."""

import copy
import unittest

from src.validate_dataset import (
    validate_all,
    validate_completeness,
    validate_coverage,
    validate_schema,
    validate_score_distribution,
    validate_uniqueness,
)


def make_mini_dataset() -> dict:
    """Build a minimal valid dataset for testing."""
    return {
        "version": "1.0",
        "created_at": "2026-01-01T00:00:00Z",
        "description": "Test dataset",
        "taxonomy": {
            "conflicts_of_interest": {
                "name": "Conflicts of Interest",
                "description": "CoI topic",
                "issues": [
                    {
                        "id": "business_entity_interest",
                        "name": "Business Entity Interest",
                        "description": "Business entity CoI",
                        "key_statutes": ["87103(a)"],
                        "example_opinion_ids": [],
                    }
                ],
            },
            "campaign_finance": {
                "name": "Campaign Finance",
                "description": "CF topic",
                "issues": [
                    {
                        "id": "contribution_definition",
                        "name": "Contribution Definition",
                        "description": "Contribution def",
                        "key_statutes": ["82015"],
                        "example_opinion_ids": [],
                    }
                ],
            },
            "gifts_honoraria": {
                "name": "Gifts and Honoraria",
                "description": "Gifts topic",
                "issues": [
                    {
                        "id": "gift_limits_and_applicability",
                        "name": "Gift Limits",
                        "description": "Gift limits",
                        "key_statutes": ["89503"],
                        "example_opinion_ids": [],
                    }
                ],
            },
            "lobbying": {
                "name": "Lobbying",
                "description": "Lobbying topic",
                "issues": [
                    {
                        "id": "lobbyist_registration_and_certification",
                        "name": "Lobbyist Registration",
                        "description": "Lobbyist reg",
                        "key_statutes": ["86100"],
                        "example_opinion_ids": [],
                    }
                ],
            },
            "other": {
                "name": "Other",
                "description": "Other topic",
                "issues": [
                    {
                        "id": "sei_and_conflict_of_interest_codes",
                        "name": "SEI and CoI Codes",
                        "description": "SEI codes",
                        "key_statutes": ["87200"],
                        "example_opinion_ids": [],
                    }
                ],
            },
        },
        "queries": _make_queries(65),
    }


def _make_queries(n: int) -> list[dict]:
    """Generate n minimal valid queries spread across topics/issues."""
    topics_issues = [
        ("conflicts_of_interest", "business_entity_interest"),
        ("campaign_finance", "contribution_definition"),
        ("gifts_honoraria", "gift_limits_and_applicability"),
        ("lobbying", "lobbyist_registration_and_certification"),
        ("other", "sei_and_conflict_of_interest_codes"),
    ]
    types = ["keyword", "natural_language", "fact_pattern"]
    queries = []
    for i in range(n):
        topic, issue = topics_issues[i % len(topics_issues)]
        queries.append({
            "id": f"q{i+1:03d}",
            "text": f"Test query {i+1}",
            "type": types[i % len(types)],
            "topic": topic,
            "issue": issue,
            "notes": "",
            "relevance_judgments": [
                {"opinion_id": f"op-{i+1}-{j}", "score": 2 if j < 3 else 1, "rationale": "test"}
                for j in range(12)
            ],
        })
    return queries


class TestValidDataset(unittest.TestCase):
    """A valid dataset should produce no errors."""

    def test_valid_produces_no_errors(self):
        ds = make_mini_dataset()
        errors, warnings = validate_all(ds)
        self.assertEqual(errors, [], f"Unexpected errors: {errors}")


class TestSchemaValidation(unittest.TestCase):

    def test_missing_query_field(self):
        ds = make_mini_dataset()
        del ds["queries"][0]["type"]
        errors = validate_schema(ds)
        self.assertTrue(any("missing field: 'type'" in e for e in errors))

    def test_invalid_score_value(self):
        ds = make_mini_dataset()
        ds["queries"][0]["relevance_judgments"][0]["score"] = 3
        errors = validate_schema(ds)
        self.assertTrue(any("invalid score: 3" in e for e in errors))

    def test_invalid_query_type(self):
        ds = make_mini_dataset()
        ds["queries"][0]["type"] = "boolean"
        errors = validate_schema(ds)
        self.assertTrue(any("invalid type: 'boolean'" in e for e in errors))

    def test_missing_taxonomy_field(self):
        ds = make_mini_dataset()
        del ds["taxonomy"]["conflicts_of_interest"]["issues"][0]["name"]
        errors = validate_schema(ds)
        self.assertTrue(any("missing field: 'name'" in e for e in errors))

    def test_missing_judgment_field(self):
        ds = make_mini_dataset()
        del ds["queries"][0]["relevance_judgments"][0]["rationale"]
        errors = validate_schema(ds)
        self.assertTrue(any("missing field: 'rationale'" in e for e in errors))


class TestCoverageValidation(unittest.TestCase):

    def test_fewer_than_10_judgments(self):
        ds = make_mini_dataset()
        ds["queries"][0]["relevance_judgments"] = ds["queries"][0]["relevance_judgments"][:5]
        errors = validate_coverage(ds)
        self.assertTrue(any("has 5 judgments" in e for e in errors))

    def test_missing_issue_coverage(self):
        ds = make_mini_dataset()
        # Remove all queries for one issue
        ds["queries"] = [q for q in ds["queries"] if q["issue"] != "sei_and_conflict_of_interest_codes"]
        # Pad back to 60 queries
        while len(ds["queries"]) < 60:
            extra = copy.deepcopy(ds["queries"][0])
            extra["id"] = f"q{len(ds['queries'])+1:03d}"
            ds["queries"].append(extra)
        errors = validate_coverage(ds)
        self.assertTrue(any("sei_and_conflict_of_interest_codes" in e for e in errors))


class TestScoreDistribution(unittest.TestCase):

    def test_no_score2_is_error(self):
        ds = make_mini_dataset()
        for j in ds["queries"][0]["relevance_judgments"]:
            j["score"] = 1
        errors, _ = validate_score_distribution(ds)
        self.assertTrue(any("zero score-2" in e for e in errors))

    def test_low_score2_warning(self):
        ds = make_mini_dataset()
        for j in ds["queries"][0]["relevance_judgments"]:
            j["score"] = 1
        ds["queries"][0]["relevance_judgments"][0]["score"] = 2
        _, warnings = validate_score_distribution(ds)
        self.assertTrue(any("only 1 score-2" in w for w in warnings))


class TestUniquenessValidation(unittest.TestCase):

    def test_duplicate_query_ids(self):
        ds = make_mini_dataset()
        ds["queries"][1]["id"] = ds["queries"][0]["id"]
        errors = validate_uniqueness(ds)
        self.assertTrue(any("Duplicate query IDs" in e for e in errors))

    def test_duplicate_opinion_id_within_query(self):
        ds = make_mini_dataset()
        ds["queries"][0]["relevance_judgments"][1]["opinion_id"] = (
            ds["queries"][0]["relevance_judgments"][0]["opinion_id"]
        )
        errors = validate_uniqueness(ds)
        self.assertTrue(any("duplicate opinion IDs" in e for e in errors))


class TestCompletenessValidation(unittest.TestCase):

    def test_query_referencing_nonexistent_topic(self):
        ds = make_mini_dataset()
        ds["queries"][0]["topic"] = "nonexistent_topic"
        errors = validate_completeness(ds)
        self.assertTrue(any("nonexistent topic" in e for e in errors))

    def test_query_referencing_nonexistent_issue(self):
        ds = make_mini_dataset()
        ds["queries"][0]["issue"] = "nonexistent_issue"
        errors = validate_completeness(ds)
        self.assertTrue(any("nonexistent issue" in e for e in errors))

    def test_missing_expected_topic(self):
        ds = make_mini_dataset()
        del ds["taxonomy"]["lobbying"]
        # Also remove queries for that topic to avoid other errors
        ds["queries"] = [q for q in ds["queries"] if q["topic"] != "lobbying"]
        while len(ds["queries"]) < 60:
            extra = copy.deepcopy(ds["queries"][0])
            extra["id"] = f"q{len(ds['queries'])+1:03d}"
            ds["queries"].append(extra)
        errors = validate_completeness(ds)
        self.assertTrue(any("lobbying" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
