# FPPC Opinions Search Evaluation Suite — Specification

## Purpose

This evaluation suite measures the quality of search engines built to retrieve relevant FPPC (Fair Political Practices Commission) opinions. The corpus consists of ~14,100 advisory opinions spanning 1975-2025, covering conflict of interest, campaign finance, gifts/honoraria, lobbying, and related topics under California's Political Reform Act.

The goal is to build a search engine significantly better than the FPPC website's basic keyword search, capable of handling keyword queries, natural language questions, and multi-sentence fact pattern descriptions. This eval suite provides the ground truth and scoring harness to objectively measure and compare search approaches.

## Components

The eval suite consists of three artifacts:

1. **Eval dataset** (`eval/dataset.json`) — Test queries with graded relevance judgments
2. **Scoring harness** (`src/scorer.py`) — Computes IR metrics given search results
3. **Search engine interface** (`src/interface.py`) — ABC that any search backend implements

## Eval Dataset Schema

```json
{
  "version": "1.0",
  "created_at": "ISO-8601 timestamp",
  "description": "FPPC Opinions Search Evaluation Dataset",
  "taxonomy": {
    "<topic_id>": {
      "name": "Human-readable topic name",
      "description": "What this topic area covers",
      "issues": [
        {
          "id": "issue_slug",
          "name": "Human-readable issue name",
          "description": "What this specific legal issue is about",
          "key_statutes": ["87100", "87103"],
          "example_opinion_ids": ["A-24-003", "A-22-103"]
        }
      ]
    }
  },
  "queries": [
    {
      "id": "q001",
      "text": "The query string as a user would type it",
      "type": "keyword | natural_language | fact_pattern",
      "topic": "<topic_id>",
      "issue": "issue_slug",
      "notes": "Optional: what this query is specifically testing",
      "relevance_judgments": [
        {
          "opinion_id": "A-24-003",
          "score": 2,
          "rationale": "Brief explanation of why this score was assigned"
        }
      ]
    }
  ]
}
```

## Relevance Scale

See `RELEVANCE_RUBRIC.md` for the full rubric with examples.

| Score | Label | Definition |
|-------|-------|------------|
| **2** | Highly relevant | Addresses the same core legal question or issue. An attorney researching this topic would definitely want to read this opinion, regardless of whether the specific facts match exactly. |
| **1** | Relevant | Discusses related legal concepts that provide useful context, analogies, or background. An attorney might find it helpful as secondary reading. |
| **0** | Not relevant | Does not meaningfully address the query's legal question. |

### Expected Distribution

Per query, we expect approximately:
- **Score 2:** 3-8 opinions (addressing the same legal issue with varying facts)
- **Score 1:** 5-15 opinions (related concepts, adjacent issues)
- **Total judged:** 10-20 opinions per query (minimum 10)

## Query Types and Targets

### Query Types

| Type | Description | Example |
|------|-------------|---------|
| **keyword** | Terms an attorney would type into a search box | `"Section 1090 recusal real property 500 feet"` |
| **natural_language** | A question in plain English | `"Can a city council member vote on a zoning change for a property near their home?"` |
| **fact_pattern** | A multi-sentence scenario description | `"A planning commissioner owns a rental property two blocks from a proposed development. The development would add 200 residential units. The commissioner's property is currently valued at $800,000. The planning commission must vote on the project's EIR."` |

### Target Distribution

| Topic | % of Corpus | Target Queries |
|-------|-------------|----------------|
| Conflicts of interest | 48% | 25-30 |
| Campaign finance | 17% | 10-15 |
| Gifts/honoraria | 5% | 5-8 |
| Lobbying | 1% | 3-5 |
| Other / cross-topic | 8% | 5-10 |
| **Total** | | **60-80** |

Within each topic, aim for roughly equal distribution across the three query types.

## Metrics

The scoring harness computes the following metrics:

### Primary Metrics

- **MRR (Mean Reciprocal Rank):** Average of 1/rank of the first highly-relevant (score=2) result. Measures: "Is the best answer near the top?"
- **nDCG@10 (Normalized Discounted Cumulative Gain at 10):** Measures ranking quality of the top 10 results, accounting for graded relevance. The primary quality metric.

### Secondary Metrics

- **nDCG@5:** Same as nDCG@10 but for top 5 only.
- **Precision@5:** Fraction of top 5 results that are relevant (score >= 1).
- **Precision@10:** Fraction of top 10 results that are relevant (score >= 1).
- **Recall@10:** Fraction of all relevant opinions (score >= 1) that appear in top 10.
- **Recall@20:** Fraction of all relevant opinions (score >= 1) that appear in top 20.

### Reporting

Metrics are reported:
1. **Overall** — Aggregated across all queries
2. **By query type** — Broken out by keyword / natural_language / fact_pattern
3. **By topic** — Broken out by topic area

## Search Engine Interface

```python
from abc import ABC, abstractmethod

class SearchEngine(ABC):
    """Interface that any search backend must implement to be evaluated."""

    @abstractmethod
    def search(self, query: str, top_k: int = 20) -> list[str]:
        """
        Search for opinions relevant to the given query.

        Args:
            query: The search query string (keyword, natural language, or fact pattern).
            top_k: Maximum number of results to return.

        Returns:
            A list of opinion IDs (e.g., ["A-24-003", "89-142", "75003"]),
            ordered by relevance (most relevant first).
        """
        pass

    def name(self) -> str:
        """Human-readable name for this search engine (used in reports)."""
        return self.__class__.__name__
```

## Scoring Harness Usage

```bash
# Run evaluation against a search engine module
python src/scorer.py --search-module path.to.my_engine --dataset eval/dataset.json

# Output: scorecard printed to stdout + JSON results to file
python src/scorer.py --search-module path.to.my_engine --dataset eval/dataset.json --output results.json
```

## Project Structure

```
fppc-opinions-eval/
├── SPEC.md                      # This file
├── IMPLEMENTATION_PLAN.md       # Phased build plan
├── RELEVANCE_RUBRIC.md          # Detailed relevance grading rubric
├── SPRINT_LOG.md                # Tracking document updated after each sprint
├── data/                        # [gitignored] Raw opinion data
│   └── extracted/
│       └── {year}/*.json
├── eval/
│   ├── dataset.json             # The eval dataset (version controlled)
│   └── taxonomy.json            # Issue taxonomy (intermediate artifact)
├── src/
│   ├── interface.py             # SearchEngine ABC
│   └── scorer.py                # Scoring harness
└── tests/
    └── test_scorer.py           # Tests for the scoring harness
```

## Data Available Per Opinion

Each opinion JSON file contains these fields available for search and judgment:

| Field | Coverage | Description |
|-------|----------|-------------|
| `sections.question` | 66% (standard format) | The actual legal question posed |
| `sections.question_synthetic` | 31% (LLM-generated) | Synthetic question for non-standard opinions |
| `sections.conclusion` | 66% | The FPPC's conclusion |
| `sections.conclusion_synthetic` | 16% | Synthetic conclusion |
| `sections.facts` | 66% | Facts as presented by requester |
| `sections.analysis` | 66% | Legal analysis |
| `content.full_text` | 100% | Full extracted text |
| `embedding.qa_text` | ~97% | Combined question + conclusion text |
| `embedding.summary` | varies | Brief summary |
| `citations.government_code` | 79% | Government Code sections cited |
| `citations.prior_opinions` | 35% | Other FPPC opinions cited |
| `classification.topic_primary` | ~80% | Primary topic classification |
| `parsed.date` | varies | Date of the opinion |
| `extraction.quality_score` | 100% | OCR/extraction quality (0-1) |
