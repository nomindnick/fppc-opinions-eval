# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

An evaluation suite for search engines built to retrieve FPPC (Fair Political Practices Commission) advisory opinions. The corpus is ~14,100 opinions (1975–2025) covering California's Political Reform Act. The suite provides ground-truth queries with graded relevance judgments and a scoring harness to objectively measure search quality.

**Current status:** v1.0 complete. 65 queries with 877 graded relevance judgments across 5 topics and 37 issues. Scoring harness, dataset validator, and random baseline all operational. See `SPRINT_LOG.md` for detailed progress.

## Commands

```bash
# Run all tests
pytest tests/ -v

# Run a single test
pytest tests/test_scorer.py::TestComputeMRR::test_score2_at_rank1 -v

# Run the scoring harness against a search engine
python src/scorer.py --search-module <dotted.module.path> --dataset eval/dataset.json

# With JSON output
python src/scorer.py --search-module <dotted.module.path> --dataset eval/dataset.json --output results.json

# Validate the dataset
python src/validate_dataset.py --dataset eval/dataset.json --data-dir data/extracted
```

No external dependencies — stdlib only. Python 3.12+.

## Architecture

Three artifacts, one interface:

1. **`src/interface.py`** — `SearchEngine` ABC with a single method: `search(query, top_k=20) -> list[str]` returning opinion IDs ordered by relevance. Any search backend implements this.

2. **`src/scorer.py`** — Scoring harness that loads the eval dataset, runs queries through a search engine, and computes IR metrics. Pure functions for each metric (MRR, nDCG@5/10, P@5/10, R@10/20). CLI entry point that dynamically imports a search engine module.

3. **`eval/dataset.json`** — Evaluation dataset containing the taxonomy and test queries with relevance judgments. Schema defined in `SPEC.md`.

Supporting artifact: **`eval/taxonomy.json`** — Issue taxonomy (5 topics, 37 issues) used during dataset construction.

## Metric Semantics (important for correctness)

- **MRR** counts only score=2 (highly relevant), not score=1
- **nDCG** IDCG is computed from ALL judged documents, not just returned ones — this penalizes engines that miss relevant docs
- **Precision@k** divides by k even if engine returns fewer than k results
- **Recall@k** counts score≥1 as relevant (both 1 and 2)
- Unjudged opinion IDs are treated as score=0
- Results are deduped before metric computation

## Opinion Data

Opinions live in `data/extracted/{year}/{id}.json` (gitignored). When reading opinions, prefer these fields in order:

1. `embedding.qa_text` — best single-field summary (~97% coverage)
2. `sections.question` + `sections.conclusion` — core Q&A (66% coverage)
3. `embedding.summary` — brief summary (variable coverage)
4. `content.full_text` — last resort, often noisy for older opinions

Useful search fields: `classification.topic_primary`, `citations.government_code`, `citations.prior_opinions`, `citations.cited_by`.

## Relevance Scoring

0–2 scale. Relevance is about **legal substance**, not fact-pattern matching. See `RELEVANCE_RUBRIC.md` for the full rubric. Per query: minimum 10 judged opinions, at least 2–3 scored as 2, rationale required for every judgment.

## Git Workflow

Branch naming: `sprint-N/<short-description>` (e.g., `sprint-3/query-generation`). Each sprint ends with: update `SPRINT_LOG.md`, push branch, create PR, run `/code-review:code-review`, fix issues, merge to main.

## Key Documents

- **`SPEC.md`** — Full specification (metrics, schema, interface, query types)
- **`IMPLEMENTATION_PLAN.md`** — Sprint-by-sprint build plan with agent strategies
- **`RELEVANCE_RUBRIC.md`** — Grading standards with examples and edge cases
- **`SPRINT_LOG.md`** — Progress tracking, decisions, and notes from each sprint
