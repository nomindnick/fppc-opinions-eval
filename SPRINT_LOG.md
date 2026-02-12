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

## Sprint 5: Relevance Judgments — CoI Batch 2 (q013-q029)
**Date:** 2026-02-12
**Branch:** sprint-5/relevance-coi-batch2
**Status:** Complete

### Completed
- Populated relevance judgments for 17 queries (q013-q029) covering 7 remaining conflicts of interest issues
- Spawned 4 parallel researcher agents organized by issue batch, each using keyword search, statute/topic filtering, and citation chain following
- All 194 judgment opinion IDs verified to exist in corpus; all judgments include rationales
- Dataset loads correctly via `src/scorer.py`; all 28 unit tests pass

### Judgment Summary

| Query | Issue | Type | Judged | Score 2 | Score 1 |
|-------|-------|------|--------|---------|---------|
| q013 | personal_financial_effect | natural_language | 12 | 4 | 8 |
| q014 | personal_financial_effect | fact_pattern | 12 | 5 | 7 |
| q015 | section_1090_self_dealing | keyword | 12 | 5 | 7 |
| q016 | section_1090_self_dealing | natural_language | 11 | 4 | 7 |
| q017 | section_1090_self_dealing | fact_pattern | 11 | 4 | 7 |
| q018 | post_employment | keyword | 12 | 6 | 6 |
| q019 | post_employment | natural_language | 11 | 4 | 7 |
| q020 | public_generally_exception | keyword | 12 | 5 | 7 |
| q021 | public_generally_exception | fact_pattern | 11 | 5 | 6 |
| q022 | legally_required_participation | keyword | 12 | 5 | 7 |
| q023 | legally_required_participation | natural_language | 11 | 4 | 7 |
| q024 | remote_minimal_interest | keyword | 12 | 5 | 7 |
| q025 | remote_minimal_interest | natural_language | 11 | 4 | 7 |
| q026 | spousal_community_property | keyword | 11 | 5 | 6 |
| q027 | spousal_community_property | natural_language | 11 | 4 | 7 |
| q028 | common_law_conflicts | keyword | 11 | 5 | 6 |
| q029 | common_law_conflicts | fact_pattern | 11 | 3 | 8 |
| **Total** | | | **194** | **77** | **117** |

### Issues Covered (7 new, completing all 12 CoI issues)
| # | Issue | Queries |
|---|-------|---------|
| 5 | personal_financial_effect | q013, q014 (+ q012 from Sprint 4) |
| 6 | section_1090_self_dealing | q015, q016, q017 |
| 7 | post_employment | q018, q019 |
| 8 | public_generally_exception | q020, q021 |
| 9 | legally_required_participation | q022, q023 |
| 10 | remote_minimal_interest | q024, q025 |
| 11 | spousal_community_property | q026, q027 |
| 12 | common_law_conflicts | q028, q029 |

### Artifacts Created/Modified
- `eval/dataset.json` — populated relevance_judgments for q013-q029 (194 new judgments; 393 total with Sprint 4)
- `SPRINT_LOG.md` — updated with Sprint 5 entry

### Notes for Future Sprints
- Average 11.4 judgments per query, above 10 minimum; average 4.5 score-2 per query, above 2-3 minimum
- All 29 CoI queries (q001-q029) now have judgments — conflicts of interest topic is fully judged
- Common law conflicts (q028-q029) is the thinnest area; fewer opinions explicitly use "common law conflict" terminology
- Post-employment (q018-q019) has rich coverage; Section 87400 opinions are well-indexed
- Section 1090 opinions (q015-q017) required cross-referencing both PRA and Government Code Section 1090 analysis
- Public generally exception (q020-q021) and legally required participation (q022-q023) had strong citation chains from foundational opinions (90-067, 98-224)
- Remote/noninterest exceptions (q024-q025) benefited from the -1090 suffixed opinion series (post-2014)
- Spousal/community property (q026-q027) drew heavily from 1970s-era opinions when the topic was frequently addressed
- Remaining work: Campaign finance (q030-q043), gifts/honoraria (q044-q050), lobbying (q051-q055), other (q056-q065)
- All 28 scorer unit tests continue to pass

## Sprint 6: Relevance Judgments — Campaign Finance & Gifts/Honoraria (q030-q050)
**Date:** 2026-02-12
**Branch:** sprint-6/relevance-cf-gifts
**Status:** Complete

### Completed
- Populated relevance judgments for 21 queries (q030-q050) covering 10 campaign finance issues and 5 gifts/honoraria issues
- Spawned 4 parallel researcher agents organized by issue batch:
  - Researcher A: Contributions, limits, IEs, member comms, committee formation (q030, q031, q038, q039, q040, q043)
  - Researcher B: Campaign fund use, mass mailing, pay-to-play (q032, q033, q034, q035, q036)
  - Researcher C: Campaign reporting, behested payments, campaign fund personal use (q037, q041, q042, q049, q050)
  - Researcher D: Honoraria, gift limits, gift definition, travel exceptions (q044, q045, q046, q047, q048)
- All 304 judgment opinion IDs verified to exist in corpus; all judgments include rationales
- Dataset loads correctly via `src/scorer.py`; all 28 unit tests pass

### Judgment Summary

| Query | Issue | Type | Judged | Score 2 | Score 1 |
|-------|-------|------|--------|---------|---------|
| q030 | contribution_definition | keyword | 14 | 6 | 7 |
| q031 | contribution_definition | fact_pattern | 13 | 4 | 7 |
| q032 | campaign_fund_use | keyword | 19 | 6 | 12 |
| q033 | campaign_fund_use | natural_language | 13 | 7 | 5 |
| q034 | mass_mailing | natural_language | 17 | 6 | 10 |
| q035 | pay_to_play_disqualification | keyword | 12 | 5 | 6 |
| q036 | pay_to_play_disqualification | fact_pattern | 12 | 6 | 5 |
| q037 | campaign_reporting_disclosure | natural_language | 16 | 4 | 10 |
| q038 | contribution_limits_transfers | keyword | 15 | 6 | 7 |
| q039 | independent_expenditures | natural_language | 13 | 4 | 7 |
| q040 | member_communications | fact_pattern | 15 | 6 | 7 |
| q041 | behested_payments | keyword | 15 | 4 | 9 |
| q042 | behested_payments | fact_pattern | 15 | 3 | 10 |
| q043 | committee_formation_management | natural_language | 15 | 6 | 7 |
| q044 | honoraria_ban_and_exceptions | keyword | 14 | 7 | 7 |
| q045 | honoraria_ban_and_exceptions | natural_language | 15 | 7 | 8 |
| q046 | gift_limits_and_applicability | keyword | 13 | 4 | 7 |
| q047 | gift_definition_and_valuation | fact_pattern | 16 | 5 | 9 |
| q048 | travel_payment_exceptions | natural_language | 18 | 7 | 9 |
| q049 | campaign_fund_personal_use | keyword | 12 | 3 | 7 |
| q050 | campaign_fund_personal_use | fact_pattern | 13 | 4 | 7 |
| **Total** | | | **305** | **110** | **163** |

### Issues Covered (15 new)

**Campaign Finance (10 issues)**
| # | Issue | Queries |
|---|-------|---------|
| 1 | contribution_definition | q030, q031 |
| 2 | campaign_fund_use | q032, q033 |
| 3 | mass_mailing | q034 |
| 4 | pay_to_play_disqualification | q035, q036 |
| 5 | campaign_reporting_disclosure | q037 |
| 6 | contribution_limits_transfers | q038 |
| 7 | independent_expenditures | q039 |
| 8 | member_communications | q040 |
| 9 | behested_payments | q041, q042 |
| 10 | committee_formation_management | q043 |

**Gifts and Honoraria (5 issues)**
| # | Issue | Queries |
|---|-------|---------|
| 1 | honoraria_ban_and_exceptions | q044, q045 |
| 2 | gift_limits_and_applicability | q046 |
| 3 | gift_definition_and_valuation | q047 |
| 4 | travel_payment_exceptions | q048 |
| 5 | campaign_fund_personal_use | q049, q050 |

### Artifacts Created/Modified
- `eval/dataset.json` — populated relevance_judgments for q030-q050 (305 new judgments; 698 total with Sprints 4-5)
- `SPRINT_LOG.md` — updated with Sprint 6 entry

### Notes for Future Sprints
- Average 14.5 judgments per query, well above 10 minimum; average 5.2 score-2 per query, above 2-3 minimum
- Campaign fund use (q032) has the richest judgment set at 19 opinions, reflecting the broad applicability of the 85800/85801 governmental purpose framework
- Travel payment exceptions (q048) also rich at 18 opinions — the Silicon Valley mayors' China trip cases created a cluster of closely related opinions
- Behested payments (q041-q042) coverage was thin as predicted but expanded successfully through "behest" keyword and 84224 statute searches
- Member communications (q040) benefited from the A-20-044 and 10-034 seed opinions which led to strong citation chains
- Campaign fund personal use (q049-q050) distinguished from regular campaign_fund_use by focusing on 89510-89519 statutes rather than 85800-85802
- Honoraria queries (q044-q045) had strong coverage — many opinions from 1990s-2000s when the bona fide business exception was frequently litigated
- 50 of 65 queries now have judgments (29 CoI + 14 CF + 7 G/H)
- Remaining work: Lobbying (q051-q055), other (q056-q065) — 15 queries remaining
- All 28 scorer unit tests continue to pass

## Sprint 7: Relevance Judgments — Lobbying & Other (q051-q065)
**Date:** 2026-02-12
**Branch:** sprint-7/relevance-lobbying-other
**Status:** Complete

### Completed
- Populated relevance judgments for 15 queries (q051-q065) covering 4 lobbying issues and 6 "other" issues
- Spawned 4 parallel researcher agents organized by query batch:
  - Researcher A: Lobbying registration & reporting (q051, q052)
  - Researcher B: Lobbying gifts & conduct (q053, q054, q055)
  - Researcher C: Mass mailing, campaign fund use, SEI/CoI codes (q056-q060)
  - Researcher D: Jurisdiction, campaign reporting, lobbying regulation (q061-q065)
- All 179 judgment opinion IDs verified to exist in corpus; all judgments include rationales
- Dataset loads correctly via `src/scorer.py`; all 28 unit tests pass
- All 65 queries now have relevance judgments — relevance judgment phase is complete

### Judgment Summary

| Query | Issue | Type | Judged | Score 2 | Score 1 |
|-------|-------|------|--------|---------|---------|
| q051 | lobbyist_registration_and_certification | keyword | 15 | 8 | 7 |
| q052 | lobbying_disclosure_and_reporting | fact_pattern | 14 | 5 | 9 |
| q053 | lobbyist_gift_restrictions | natural_language | 14 | 5 | 9 |
| q054 | lobbyist_conduct_prohibitions | keyword | 11 | 5 | 6 |
| q055 | lobbyist_conduct_prohibitions | fact_pattern | 10 | 4 | 6 |
| q056 | mass_mailing_restrictions | keyword | 13 | 6 | 7 |
| q057 | mass_mailing_restrictions | fact_pattern | 12 | 4 | 8 |
| q058 | permissible_campaign_fund_use | keyword | 12 | 5 | 7 |
| q059 | permissible_campaign_fund_use | natural_language | 12 | 5 | 7 |
| q060 | sei_and_conflict_of_interest_codes | natural_language | 11 | 6 | 5 |
| q061 | jurisdiction_and_agency_coverage | keyword | 12 | 6 | 6 |
| q062 | jurisdiction_and_agency_coverage | natural_language | 12 | 5 | 7 |
| q063 | campaign_reporting_and_disclosure | keyword | 11 | 4 | 7 |
| q064 | lobbying_regulation | natural_language | 10 | 4 | 6 |
| q065 | lobbying_regulation | fact_pattern | 10 | 3 | 7 |
| **Total** | | | **179** | **75** | **104** |

### Issues Covered (10 new, completing all 37 taxonomy issues)

**Lobbying (4 issues)**
| # | Issue | Queries |
|---|-------|---------|
| 1 | lobbyist_registration_and_certification | q051 |
| 2 | lobbying_disclosure_and_reporting | q052 |
| 3 | lobbyist_gift_restrictions | q053 |
| 4 | lobbyist_conduct_prohibitions | q054, q055 |

**Other (6 issues)**
| # | Issue | Queries |
|---|-------|---------|
| 1 | mass_mailing_restrictions | q056, q057 |
| 2 | permissible_campaign_fund_use | q058, q059 |
| 3 | sei_and_conflict_of_interest_codes | q060 |
| 4 | jurisdiction_and_agency_coverage | q061, q062 |
| 5 | campaign_reporting_and_disclosure | q063 |
| 6 | lobbying_regulation | q064, q065 |

### Artifacts Created/Modified
- `eval/dataset.json` — populated relevance_judgments for q051-q065 (179 new judgments; 877 total across all sprints)
- `SPRINT_LOG.md` — updated with Sprint 7 entry

### Notes for Future Sprints
- Average 11.9 judgments per query, above 10 minimum; average 5.0 score-2 per query, above 2-3 minimum
- Lobbyist registration (q051) was the richest lobbying query at 15 opinions — multiple ethics course opinions from the 1990s-2000s provided strong coverage despite the thin 86103 citation count (3 files)
- Lobbyist conduct (q054/q055) had significant overlap as predicted — both queries about Section 86205(f) contingency fee prohibition but from different angles (placement agent vs. school facility grants)
- Electronic filing/campaign reporting (q063) expanded successfully beyond the 4 files citing Section 84615 through broader "electronic filing" and "signature verification" keyword searches
- Jurisdiction/agency coverage (q061/q062) benefited from the rich Siegel test case law — many opinions from 1990s-2000s applying the four-factor test to various nonprofit entities
- Mass mailing (q056/q057) had the strongest corpus coverage — dozens of opinions from the late 1980s when Proposition 73 mass mailing amendments were heavily litigated
- Lobbying regulation (q064/q065) were the thinnest queries at 10 opinions each; q065 reached only 3 score-2, the minimum threshold
- All 65 queries now have relevance judgments — 877 total across 5 topics and 37 issues
- Cumulative stats: 877 judgments, 345 score-2 (39.3%), 500 score-1 (57.0%), average 13.5 judgments/query
- All 28 scorer unit tests continue to pass
- Next up: Sprint 8 (validation & smoke test)
