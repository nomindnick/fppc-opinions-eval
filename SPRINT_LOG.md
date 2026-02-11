# Sprint Log

## Sprint 0: Project Scaffolding
**Date:** 2026-02-11
**Branch:** sprint-0/project-scaffolding
**Status:** Complete

### Completed
- Created project directory structure (`src/`, `tests/`, `eval/`)
- Implemented `src/interface.py` with the `SearchEngine` ABC (verbatim from SPEC.md)
- Implemented `src/scorer.py` scoring harness with all 7 IR metrics (MRR, nDCG@5, nDCG@10, P@5, P@10, R@10, R@20)
- Implemented CLI interface for scorer (`--search-module`, `--dataset`, `--output`)
- Created `tests/test_scorer.py` with 28 unit tests covering all metric functions and edge cases
- Initialized `eval/dataset.json` with empty schema matching SPEC.md
- Created `SPRINT_LOG.md`

### Artifacts Created/Modified
- `src/__init__.py` — empty package init
- `src/interface.py` — SearchEngine ABC
- `src/scorer.py` — scoring harness (~250 lines)
- `tests/__init__.py` — empty package init
- `tests/test_scorer.py` — 28 unit tests
- `eval/dataset.json` — empty eval dataset
- `SPRINT_LOG.md` — this file

### Notes for Future Sprints
- Scorer uses only stdlib imports (json, math, argparse, importlib, sys, os, datetime, inspect) — no external dependencies needed
- Unjudged opinion IDs in results are treated as score 0
- nDCG ideal ranking uses all judged documents, not just returned ones
- MRR only counts score=2 (highly relevant), not score=1
- Precision divides by k even if engine returns fewer results
- `load_dataset` skips queries with empty `relevance_judgments` with a warning — this means the empty dataset will produce "No queries" output until judgments are added
- `load_engine` scans a module for the first SearchEngine subclass and instantiates it

## Sprint 1: Conflicts of Interest Taxonomy
**Date:** 2026-02-11
**Branch:** sprint-1/coi-taxonomy
**Status:** Complete

### Completed
- Identified 12 distinct legal issues within the conflicts of interest topic
- Created `eval/taxonomy.json` with full taxonomy structure
- Each issue includes: `id`, `name`, `description`, `key_statutes`, `example_opinion_ids`
- All 59 example opinion IDs verified to exist in `data/extracted/` and be classified as `conflicts_of_interest`
- No duplicate example opinions across issues

### Taxonomy Issues (12)
| # | ID | Name | Key Statutes | Examples |
|---|-----|------|-------------|----------|
| 1 | `business_entity_interest` | Business Entity Interest | 87103(a) | 5 |
| 2 | `real_property_proximity` | Real Property Proximity | 87103(b), Reg 18702.2 | 5 |
| 3 | `source_of_income` | Source of Income | 87103(c) | 5 |
| 4 | `gift_source_disqualification` | Gift Source Disqualification | 87103(d) | 5 |
| 5 | `personal_financial_effect` | Personal Financial Effect | 87103(e) | 5 |
| 6 | `section_1090_self_dealing` | Section 1090 Self-Dealing | 1090, 1091, 1097 | 5 |
| 7 | `post_employment` | Post-Employment Restrictions | 87400-87407 | 5 |
| 8 | `public_generally_exception` | Public Generally Exception | Reg 18703 | 5 |
| 9 | `legally_required_participation` | Legally Required Participation | Reg 18707 | 5 |
| 10 | `remote_minimal_interest` | Remote and Noninterest Exceptions | 1091, 1091.5 | 5 |
| 11 | `spousal_community_property` | Spousal and Community Property | 87103 | 5 |
| 12 | `common_law_conflicts` | Common Law Conflict of Interest | Common law | 4 |

### Artifacts Created/Modified
- `eval/taxonomy.json` — taxonomy with 12 issues, 59 example opinions
- `SPRINT_LOG.md` — updated with Sprint 1 entry

### Notes for Future Sprints
- Opinion counts per statute group: 87103(c) source of income is largest (1,780), followed by 1090 self-dealing (2,086), 87103(a) business entity (1,452), Reg 18703 public generally (1,749)
- Common law conflicts is the thinnest category (~21 opinions) — consider merging if query generation yields too few results
- Spousal/community property is a cross-cutting concern (357 opinions mention spouse) — many also fit into other statute categories
- Many opinions address multiple issues simultaneously (e.g., both 87103(a) and 1090)
- Example opinion IDs are intentionally spread across decades (1970s-2020s) for diversity
- Classification method is `heuristic:citation_based` — some edge cases may be misclassified
