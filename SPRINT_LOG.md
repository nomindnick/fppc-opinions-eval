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
