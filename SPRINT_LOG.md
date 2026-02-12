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

## Sprint 2: Remaining Topics Taxonomy
**Date:** 2026-02-11
**Branch:** sprint-2/remaining-taxonomy
**Status:** Complete

### Completed
- Extended `eval/taxonomy.json` with 4 new topic categories: campaign_finance, gifts_honoraria, lobbying, other
- Identified 25 new issues across the 4 topics (37 total with existing 12 CoI issues)
- All 174 example opinion IDs verified to exist in `data/extracted/` and match their topic_primary
- No duplicate example opinions within any topic
- Used 4 parallel researcher subagents to sample 80+ opinions across the corpus

### Taxonomy Issues by Topic

**Campaign Finance (10 issues)**
| # | ID | Name | Key Statutes | Examples |
|---|-----|------|-------------|----------|
| 1 | `contribution_definition` | Contribution Definition and Political Purpose | 82015, 82007 | 5 |
| 2 | `campaign_fund_use` | Use of Campaign Funds | 85800-85802 | 5 |
| 3 | `mass_mailing` | Mass Mailing at Public Expense | 89001, 89002 | 4 |
| 4 | `pay_to_play_disqualification` | Section 84308 Pay-to-Play | 84308 | 3 |
| 5 | `campaign_reporting_disclosure` | Campaign Reporting and Disclosure | 84200-84216 | 5 |
| 6 | `contribution_limits_transfers` | Contribution Limits and Transfers | 85301-85304 | 4 |
| 7 | `independent_expenditures` | Independent Expenditures and Coordination | 82031, 85500 | 5 |
| 8 | `member_communications` | Member Communications Exception | 85312 | 4 |
| 9 | `behested_payments` | Behested Payment Reporting | 84224 | 5 |
| 10 | `committee_formation_management` | Committee Formation and Management | 82013, 85201 | 4 |

**Gifts and Honoraria (5 issues)**
| # | ID | Name | Key Statutes | Examples |
|---|-----|------|-------------|----------|
| 1 | `honoraria_ban_and_exceptions` | Honoraria Ban and Exceptions | 89501, 89502 | 5 |
| 2 | `gift_limits_and_applicability` | Gift Limits and Applicability | 89503 | 4 |
| 3 | `gift_definition_and_valuation` | Gift Definition and Valuation | 82028 | 4 |
| 4 | `travel_payment_exceptions` | Travel Payment Exceptions | 89506 | 4 |
| 5 | `campaign_fund_personal_use` | Campaign Fund Personal Use | 89510-89519 | 5 |

**Lobbying (4 issues)**
| # | ID | Name | Key Statutes | Examples |
|---|-----|------|-------------|----------|
| 1 | `lobbyist_registration_and_certification` | Lobbyist Registration and Certification | 86100-86107, 86300 | 5 |
| 2 | `lobbying_disclosure_and_reporting` | Lobbying Disclosure and Reporting | 86115-86117 | 5 |
| 3 | `lobbyist_gift_restrictions` | Lobbyist Gift Restrictions | 86201-86204 | 4 |
| 4 | `lobbyist_conduct_prohibitions` | Lobbyist Conduct Prohibitions | 86205 | 5 |

**Other (6 issues)**
| # | ID | Name | Key Statutes | Examples |
|---|-----|------|-------------|----------|
| 1 | `mass_mailing_restrictions` | Mass Mailing at Public Expense | 89001 | 5 |
| 2 | `permissible_campaign_fund_use` | Permissible Use of Campaign Funds | 85800-85802 | 5 |
| 3 | `sei_and_conflict_of_interest_codes` | SEI and Conflict of Interest Codes | 87200, 87300 | 5 |
| 4 | `jurisdiction_and_agency_coverage` | Jurisdiction and Agency Coverage | 82003, 82041 | 5 |
| 5 | `campaign_reporting_and_disclosure` | Campaign Reporting and Disclosure | 84200, 90001 | 5 |
| 6 | `lobbying_regulation` | Lobbying Registration and Restrictions | 86100, 86116 | 5 |

### Artifacts Created/Modified
- `eval/taxonomy.json` — expanded from 1 topic/12 issues to 5 topics/37 issues, 174 example opinions
- `SPRINT_LOG.md` — updated with Sprint 2 entry

### Notes for Future Sprints
- Campaign finance is the largest new topic (2,395 opinions, 10 issues) — issues like contribution_definition and campaign_fund_use overlap conceptually but are distinguished by statute focus
- The "other" topic contains opinions that touch campaign finance, lobbying, and SEI topics but were classified as "other" by the heuristic classifier — these are often procedural/jurisdictional questions rather than substantive ones
- Some campaign_finance issues (mass_mailing, behested_payments) have relatively few opinions (3-4 examples) — may need supplementation during query generation
- Lobbying is the smallest topic (180 opinions, 4 issues) — good coverage but thin corpus
- Gifts/honoraria has significant overlap between gift_definition_and_valuation and gift_limits_and_applicability — consider merging if query generation yields redundant results

## Sprint 3: Query Generation
**Date:** 2026-02-11
**Branch:** sprint-3/query-generation
**Status:** Complete

### Completed
- Generated 65 test queries covering all 5 topics and all 37 taxonomy issues
- Spawned 5 parallel subagents (one per topic) to read example opinions and generate grounded queries
- Compiled results from all subagents, reviewed for coverage/balance/duplicates, assigned sequential IDs
- Populated `eval/dataset.json` with full taxonomy (from `eval/taxonomy.json`) and all queries
- Each query includes: `id`, `text`, `type`, `topic`, `issue`, `notes`, empty `relevance_judgments`
- Validated: all IDs unique (q001-q065), all texts unique, all 37 taxonomy issues covered, valid JSON

### Query Distribution

| Topic | Queries | Target |
|-------|---------|--------|
| Conflicts of interest | 29 | 25-30 |
| Campaign finance | 14 | 10-15 |
| Gifts/honoraria | 7 | 5-8 |
| Lobbying | 5 | 3-5 |
| Other | 10 | 5-10 |
| **Total** | **65** | **60-80** |

| Query Type | Count | Percentage |
|-----------|-------|------------|
| keyword | 26 | 40.0% |
| natural_language | 22 | 33.8% |
| fact_pattern | 17 | 26.2% |

All three types roughly equal, per SPEC.md guidance.

### Per-Issue Coverage
- Every taxonomy issue has at least 1 query (minimum: 1, maximum: 3)
- Priority CoI issues (business_entity_interest, real_property_proximity, source_of_income, personal_financial_effect, section_1090_self_dealing) each have 3 queries
- Standard CoI issues have 2 queries each; light CoI issues have 1-2 queries
- Campaign finance: 1-2 queries per issue; gifts/honoraria: 1-2 per issue; lobbying: 1-2 per issue; other: 1-2 per issue

### Artifacts Created/Modified
- `eval/dataset.json` — populated with taxonomy and 65 queries (empty relevance judgments)
- `SPRINT_LOG.md` — updated with Sprint 3 entry

### Notes for Future Sprints
- All query counts are within or very close to target ranges
- Type balance is well-distributed: keyword (40%), natural_language (34%), fact_pattern (26%)
- Queries are ordered by topic (CoI → campaign → gifts → lobbying → other), then by issue (taxonomy order), then by type (keyword → NL → fact_pattern)
- All queries are grounded in specific example opinions — the `notes` field for each query records which opinions informed the query and difficulty level
- Dedicated topic subagents read 2-3 opinions per issue for grounding; the CoI subagent was most thorough (reading 40+ opinions for 12 issues)
- The `relevance_judgments` arrays are all empty — these will be populated in Sprints 4-7
- The `load_dataset` function in `src/scorer.py` will skip queries with empty relevance judgments, so the scorer won't produce meaningful output until judgments are added
- 28 existing scorer tests all pass

## Sprint 4: Relevance Judgments — CoI Batch 1 (q001-q012)
**Date:** 2026-02-12
**Branch:** sprint-4/relevance-coi-batch1
**Status:** Complete

### Completed
- Populated relevance judgments for 12 queries (q001-q012) covering 5 conflicts of interest issues
- Spawned 4 parallel researcher agents organized by issue group, each using multiple search strategies (statute grep, keyword search, citation chain following)
- All opinion IDs verified to exist in corpus; all judgments include rationales
- Dataset loads correctly via `src/scorer.py`; all 28 unit tests pass

### Judgment Summary

| Query | Issue | Type | Judged | Score 2 | Score 1 |
|-------|-------|------|--------|---------|---------|
| q001 | business_entity_interest | keyword | 22 | 12 | 10 |
| q002 | business_entity_interest | natural_language | 17 | 6 | 11 |
| q003 | business_entity_interest | fact_pattern | 17 | 7 | 10 |
| q004 | real_property_proximity | keyword | 25 | 15 | 10 |
| q005 | real_property_proximity | natural_language | 16 | 6 | 10 |
| q006 | real_property_proximity | fact_pattern | 18 | 8 | 10 |
| q007 | source_of_income | keyword | 25 | 10 | 15 |
| q008 | source_of_income | natural_language | 15 | 5 | 10 |
| q009 | source_of_income | fact_pattern | 13 | 4 | 9 |
| q010 | gift_source_disqualification | keyword | 10 | 3 | 7 |
| q011 | gift_source_disqualification | natural_language | 10 | 3 | 7 |
| q012 | personal_financial_effect | keyword | 11 | 4 | 7 |
| **Total** | | | **199** | **83** | **116** |

### Artifacts Created/Modified
- `eval/dataset.json` — populated relevance_judgments for q001-q012 (199 total judgments)
- `SPRINT_LOG.md` — updated with Sprint 4 entry

### Notes for Future Sprints
- Average 16.6 judgments per query, well above 10 minimum; average 6.9 score-2 per query, above 2-3 minimum
- Business entity interest (q001-q003) and real property proximity (q004-q006) have the richest judgment sets, reflecting large corpus coverage for those statutes
- Gift source disqualification (q010-q011) is the thinnest area with exactly 10 opinions each — 87103(d)/(e) opinions are less common in the corpus
- Source of income (q007-q009) has strong coverage; many opinions address employer vs. contract income identification
- Search strategies used: statute citation grep (87103(a)-(e)), keyword content search across qa_text, and citation chain following from taxonomy examples
- All 28 scorer unit tests continue to pass
