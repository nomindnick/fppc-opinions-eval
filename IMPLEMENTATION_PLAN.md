# Implementation Plan

This document provides step-by-step instructions for building the FPPC Opinions Search Evaluation Suite. Work is divided into sprints, each designed to be completable in a single Claude Code session.

**Before starting any sprint:**
1. Read `SPEC.md` for the full specification
2. Read `RELEVANCE_RUBRIC.md` for the relevance grading rubric
3. Read `SPRINT_LOG.md` for context from previous sprints (skip for Sprint 0)
4. Follow the **Git Workflow** section below

---

## Git Workflow (Every Sprint)

Every sprint follows this git workflow. Do this **every time**, not just for code sprints.

### At the Start of the Sprint

1. Make sure you're on `main` and up to date:
   ```
   git checkout main && git pull
   ```
2. Create a feature branch:
   ```
   git checkout -b sprint-<N>/<short-description>
   ```
   Examples: `sprint-0/project-scaffolding`, `sprint-1/coi-taxonomy`, `sprint-4/relevance-coi-batch1`

### During the Sprint

- Commit incrementally as you complete meaningful chunks of work.
- Use descriptive commit messages.

### At the End of the Sprint

1. **Update the sprint log** — Write a summary of what was completed to `SPRINT_LOG.md` (see Sprint Log section below).
2. **Commit all remaining changes** including the sprint log update.
3. **Push the branch and create a PR:**
   ```
   git push -u origin <branch-name>
   gh pr create --title "Sprint N: <description>" --body "<summary of work>"
   ```
4. **Run the `/code-review` slash command** on the PR.
5. **Fix any issues** identified by the code review. Commit the fixes to the same branch.
6. **Merge the PR:**
   ```
   gh pr merge --merge
   ```
7. **Return to main:**
   ```
   git checkout main && git pull
   ```

---

## Sprint Log

Maintain a tracking document at `SPRINT_LOG.md` in the project root. Update it at the end of every sprint **before** creating the PR.

### Format

```markdown
# Sprint Log

## Sprint 0: Project Scaffolding
**Date:** YYYY-MM-DD
**Branch:** sprint-0/project-scaffolding
**Status:** Complete

### Completed
- [Bulleted list of what was accomplished]

### Artifacts Created/Modified
- [List of files created or modified]

### Notes for Future Sprints
- [Any context, decisions, surprises, or issues that might affect later sprints]
- [E.g., "The taxonomy for lobbying was thin — only found 3 distinct issues, may need to revisit"]
- [E.g., "Opinion 89-142 has an empty question field despite being classified as CoI — watch for similar data issues"]

---

## Sprint 1: CoI Taxonomy
...
```

### What to Record

- **Completed:** What was actually done (may differ from plan — that's fine)
- **Artifacts:** Files created or modified, so the next sprint knows where things stand
- **Notes:** This is the most important section. Capture:
  - Deviations from the plan and why
  - Data quality issues encountered
  - Decisions made that weren't covered by the plan
  - Counts and statistics (e.g., "Generated 73 queries: 28 CoI, 13 campaign finance, ...")
  - Anything that will help the next sprint pick up context quickly

---

## Sprint 0: Project Scaffolding

**Agent strategy:** Single agent, no subagents needed.

**Goal:** Create the project structure, search engine interface, and scoring harness.

### Tasks

1. **Create directory structure:**
   ```
   eval/
   src/
   tests/
   ```

2. **Create `src/interface.py`:**
   - Define the `SearchEngine` ABC as specified in SPEC.md
   - Keep it minimal — just the interface contract

3. **Create `src/scorer.py`:**
   - Implement the scoring harness that:
     - Loads the eval dataset from `eval/dataset.json`
     - Imports a search engine module and instantiates it
     - Runs each query through the search engine
     - Computes all metrics defined in SPEC.md (MRR, nDCG@5, nDCG@10, P@5, P@10, R@10, R@20)
     - Prints a formatted scorecard (overall, by query type, by topic)
     - Optionally writes detailed JSON results to a file
   - CLI interface: `python src/scorer.py --search-module <module_path> --dataset eval/dataset.json [--output results.json]`

4. **Create `tests/test_scorer.py`:**
   - Unit tests for the metric computation functions using small hand-crafted examples
   - Verify nDCG, MRR, precision, recall calculations are correct

5. **Create `eval/dataset.json`:**
   - Initialize with the schema from SPEC.md, empty `taxonomy` and `queries` arrays
   - This file will be populated in later sprints

6. **Create `SPRINT_LOG.md`:**
   - Initialize with the header and Sprint 0 entry (follow the format in the Sprint Log section above)

7. **Follow the Git Workflow** to branch, commit, PR, code review, fix, and merge.

### Definition of Done
- `python src/scorer.py --help` works
- `pytest tests/test_scorer.py` passes
- `eval/dataset.json` exists and is valid JSON matching the schema
- `SPRINT_LOG.md` exists with Sprint 0 entry
- PR created, code reviewed, issues fixed, merged to main

---

## Sprint 1: Conflicts of Interest Taxonomy

**Agent strategy:** Agent team (1 lead + 3 researcher agents).

**Goal:** Identify the distinct legal issues and fact patterns within the "conflicts of interest" topic area (~6,800 opinions, 48% of corpus).

### Team Setup

Create a team with 4 agents:

- **Lead agent:** Coordinates research, synthesizes findings, writes the taxonomy
- **Researcher 1 — Statute-based exploration:** Search opinions by the most-cited Government Code sections for conflicts of interest:
  - Section 87100 (prohibition on participation): ~4,750 opinions
  - Section 87103 (financial interest definition): ~3,550 opinions
  - Section 87103(a)-(e) (specific interest types): varying counts
  - Section 1090 (self-dealing prohibition): ~2,120 opinions
  - Section 87200 (designated employees): ~890 opinions
  - For each statute, read 10-15 representative opinions and identify what distinct issues arise
- **Researcher 2 — Decade sampling:** Sample 10-15 opinions per decade from the conflicts_of_interest topic to capture how issues have evolved. Focus on identifying issues NOT found by Researcher 1.
- **Researcher 3 — Citation chain exploration:** Start from well-known modern opinions (2015-2025) that cite many prior opinions. Follow citation chains to find clusters of opinions on the same issue. Report the clusters found.

### How Researchers Should Work

Each researcher searches the opinion JSON files in `data/extracted/` using Grep and Read tools:

- **Grep** on `classification.topic_primary` to filter to conflicts_of_interest opinions
- **Grep** on `citations.government_code` to find opinions citing specific statutes
- **Read** individual opinion files to understand the question and conclusion
- Focus on the `sections.question`, `sections.conclusion`, `embedding.qa_text`, and `embedding.summary` fields — these are the most efficient way to understand an opinion without reading the full text

Each researcher should report back to the lead agent with:
- A list of distinct issues they identified
- For each issue: a short description and 2-3 example opinion IDs
- Any issues that seem ambiguous or overlapping

### Lead Agent Tasks

1. Collect findings from all three researchers
2. Synthesize into a deduplicated taxonomy of issues
3. Target: **8-15 distinct issues** within conflicts of interest
4. For each issue, record:
   - `id`: a slug (e.g., `real_property_proximity`)
   - `name`: human-readable name
   - `description`: 2-3 sentence description of the legal issue
   - `key_statutes`: which Government Code sections are most relevant
   - `example_opinion_ids`: 3-5 representative opinion IDs
5. Write the taxonomy to `eval/taxonomy.json` under the `conflicts_of_interest` key

### Expected Issues (not exhaustive — discover more)

These are likely categories based on the data. Researchers should confirm, refine, split, or merge as the data warrants:

- Real property proximity (500-foot rule, Regulation 18702.2)
- Financial interest in a business entity
- Source of income conflicts
- Family member / personal relationships creating conflicts
- Section 1090 self-dealing in contracts
- Post-employment restrictions (revolving door)
- Disqualification vs. disclosure obligations
- Remote/minimal interest exceptions
- Common law vs. Political Reform Act conflicts

### Definition of Done
- `eval/taxonomy.json` contains 8-15 issues under `conflicts_of_interest`, each with description and example opinion IDs
- Issues are distinct (minimal overlap) and collectively cover the major patterns found in the data
- Sprint log updated, PR created, code reviewed, fixes applied, merged to main

---

## Sprint 2: Remaining Topics Taxonomy

**Agent strategy:** Parallel subagents (one per topic area).

**Goal:** Build the taxonomy for campaign finance, gifts/honoraria, lobbying, and other topics.

### Subagent Assignments

Spawn 4 subagents in parallel, each responsible for one topic:

1. **Campaign finance subagent** (~2,400 opinions)
   - Grep for `topic_primary: campaign_finance`
   - Read 30-40 opinions sampled across decades
   - Identify 5-10 distinct issues
   - Key statutes to explore: Sections 82015, 82030, 82041, 83114, 84200-series, 85200-series

2. **Gifts/honoraria subagent** (~760 opinions)
   - Grep for `topic_primary: gifts_honoraria`
   - Read 20-30 opinions
   - Identify 3-6 distinct issues
   - Key statutes: Sections 86201-86204, 89501-89503

3. **Lobbying subagent** (~180 opinions)
   - Grep for `topic_primary: lobbying`
   - Read 15-20 opinions
   - Identify 2-4 distinct issues
   - Key statutes: Sections 86100-86300

4. **Other topics subagent** (~1,060 opinions)
   - Grep for `topic_primary: other` and opinions with no primary topic
   - Read 20-30 opinions
   - Identify what categories exist — may include: mass mailing, statement of economic interests (Form 700), ballot measure issues, enforcement/penalties, etc.
   - Identify 3-6 distinct issues

### Each Subagent Should Return

For each issue identified:
- `id`, `name`, `description`, `key_statutes`, `example_opinion_ids`

### Main Agent Tasks

1. Collect outputs from all 4 subagents
2. Review for consistency and quality
3. Merge into `eval/taxonomy.json` alongside the conflicts_of_interest taxonomy from Sprint 1
4. Commit

### Definition of Done
- `eval/taxonomy.json` contains all topics with their issues
- Total issues across all topics: ~25-40
- Each issue has description and example opinion IDs
- Sprint log updated, PR created, code reviewed, fixes applied, merged to main

---

## Sprint 3: Query Generation

**Agent strategy:** Parallel subagents (one per topic area).

**Goal:** Generate 60-80 test queries covering all topics, issues, and query types.

### Setup

Read `eval/taxonomy.json` to understand the issue taxonomy. Read `RELEVANCE_RUBRIC.md` to understand what the queries will be used for.

### Subagent Assignments

Spawn one subagent per topic area. Each subagent:

1. Reads the taxonomy for its topic
2. For each issue in the taxonomy:
   - Reads 3-5 of the example opinions to understand the issue concretely
   - Generates **2-3 queries** across the three query types:
     - 1 keyword query
     - 1 natural language question
     - 1 fact pattern (for issues with enough complexity)
   - Not every issue needs all 3 types — use judgment. Simple issues might only need 2 queries. Rich issues might warrant 4.
3. Returns the queries in the dataset schema format (see SPEC.md)

### Query Quality Guidelines

- **Keyword queries** should reflect what a California attorney would actually type — include statute numbers, legal terms of art, and concise phrases. E.g., `"Section 87100 disqualification business entity financial interest"`
- **Natural language queries** should be phrased as genuine questions an attorney would ask a colleague. E.g., `"Does a planning commissioner need to recuse from a vote if their landlord is the project applicant?"`
- **Fact pattern queries** should describe a realistic scenario in 2-5 sentences with specific (but fictional) details. Include the type of official, the type of decision, the nature of the financial interest, and any complicating factors.
- **Ground the queries in real opinions** — after reading the example opinions for an issue, write queries that those opinions would plausibly answer. Don't invent queries about issues that don't exist in the corpus.
- **Vary difficulty** — include some queries that should be easy to answer (directly match common language in opinions) and some that are harder (use different terminology, describe facts from the requester's perspective rather than the legal framework).

### Main Agent Tasks

1. Collect queries from all subagents
2. Review for:
   - **Coverage:** Every taxonomy issue has at least 1 query
   - **Type balance:** Roughly equal distribution across keyword / NL / fact pattern
   - **No duplicates:** No two queries are asking essentially the same thing
   - **Total count:** 60-80 queries total
3. Assign sequential IDs (q001, q002, ...)
4. Write to `eval/dataset.json` (populate the `queries` array with empty `relevance_judgments`)
5. Commit

### Target Distribution

| Topic | Target Queries |
|-------|---------------|
| Conflicts of interest | 25-30 |
| Campaign finance | 10-15 |
| Gifts/honoraria | 5-8 |
| Lobbying | 3-5 |
| Other / cross-topic | 5-10 |

### Definition of Done
- `eval/dataset.json` contains 60-80 queries
- Every taxonomy issue has at least 1 query
- Mix of query types within each topic
- `relevance_judgments` arrays are empty (populated in later sprints)
- Sprint log updated, PR created, code reviewed, fixes applied, merged to main

---

## Sprint 4: Relevance Judgments — Conflicts of Interest, Batch 1

**Agent strategy:** Agent team (1 lead + 3-4 researcher agents).

**Goal:** Complete relevance judgments for the first ~12 conflicts-of-interest queries.

### Setup

1. Read `eval/dataset.json` and select the first ~12 CoI queries (those not yet judged)
2. Read `RELEVANCE_RUBRIC.md` — all team members must understand the scoring rubric
3. Read `eval/taxonomy.json` for context on what issues exist

### Team Workflow

For **each query**, the lead assigns the query to the team and the team works as follows:

#### Step 1: Candidate Search (all researchers, parallel)

Each researcher searches for potentially relevant opinions using a different strategy:

- **Researcher A — Keyword search:** Grep for key terms from the query across `sections.question`, `sections.conclusion`, `embedding.qa_text`, and `content.full_text` fields. Try multiple search terms — don't rely on a single grep. Search for statute numbers, legal concepts, and factual keywords.
- **Researcher B — Statute/topic filter:** Based on the query's topic and issue, grep for opinions with matching `classification.topic_primary` and relevant `citations.government_code` entries. Read the most promising candidates.
- **Researcher C — Citation chain:** Start from the taxonomy's example opinions for this issue. Read those opinions, note which other opinions they cite (`citations.prior_opinions`) and which cite them (`citations.cited_by`). Read the cited/citing opinions.
- **Researcher D (optional):** If the team has 4 researchers, assign exploratory search — look at adjacent issues, broader keyword searches, different decades.

Each researcher reports back to the lead with:
- A list of candidate opinion IDs
- For each candidate: their recommended score (0, 1, or 2) and a brief rationale
- Any additional candidates they found via citation chains

#### Step 2: Compile and Deduplicate (lead)

The lead:
1. Merges all candidate lists, deduplicating by opinion ID
2. For opinions where researchers disagree on scores, reads the opinion to make a final judgment
3. Ensures the calibration checklist from the rubric is met:
   - At least 10 opinions judged (score >= 1)
   - At least 2-3 opinions scored as 2
   - Rationale written for every judgment
4. Records final judgments in the dataset

#### Step 3: Move to Next Query

Repeat Steps 1-2 for each query in the batch.

### Lead Tasks at End of Sprint

1. Write all relevance judgments to `eval/dataset.json`
2. Verify data integrity (valid JSON, opinion IDs exist in the corpus)
3. Commit

### Definition of Done
- ~12 CoI queries have complete relevance judgments
- Each query has 10-20 judged opinions with scores and rationales
- Sprint log updated, PR created, code reviewed, fixes applied, merged to main

---

## Sprint 5: Relevance Judgments — Conflicts of Interest, Batch 2

**Agent strategy:** Agent team (same approach as Sprint 4).

**Goal:** Complete relevance judgments for the remaining ~13-18 conflicts-of-interest queries.

### Process

Identical to Sprint 4. Pick up where Sprint 4 left off — judge all remaining CoI queries that don't yet have relevance judgments.

### Definition of Done
- All CoI queries have complete relevance judgments
- Each query has 10-20 judged opinions with scores and rationales
- Sprint log updated, PR created, code reviewed, fixes applied, merged to main

---

## Sprint 6: Relevance Judgments — Campaign Finance & Gifts

**Agent strategy:** Agent team (same approach as Sprint 4).

**Goal:** Complete relevance judgments for all campaign finance and gifts/honoraria queries (~15-23 queries).

### Notes

- Campaign finance opinions often cite different statutes than CoI opinions, so researchers should adjust their search strategies accordingly
- Gifts/honoraria is a smaller topic — opinions may be fewer and more concentrated
- The team workflow (Steps 1-3) is the same as Sprint 4

### Definition of Done
- All campaign finance and gifts/honoraria queries have complete relevance judgments
- Each query has 10-20 judged opinions with scores and rationales
- Sprint log updated, PR created, code reviewed, fixes applied, merged to main

---

## Sprint 7: Relevance Judgments — Lobbying, Other, Cross-Topic

**Agent strategy:** Agent team (same approach as Sprint 4).

**Goal:** Complete relevance judgments for all remaining queries (~10-15 queries).

### Notes

- Lobbying has a small corpus (~180 opinions) — researchers may need to cast a wider net
- "Other" and cross-topic queries may span multiple topic areas — researchers should search across the full corpus, not just one topic
- For cross-topic queries, one researcher should specifically look for opinions that bridge multiple topic areas

### Definition of Done
- All remaining queries have complete relevance judgments
- Each query has 10-20 judged opinions with scores and rationales
- Sprint log updated, PR created, code reviewed, fixes applied, merged to main

---

## Sprint 8: Compilation, Validation & Smoke Test

**Agent strategy:** Single agent with subagents for spot-check validation.

**Goal:** Finalize the eval dataset, validate quality, and verify the scoring harness works end-to-end.

### Tasks

#### 1. Dataset Validation (main agent)

Run validation checks on `eval/dataset.json`:

- **Schema validation:** All required fields present, types correct
- **Referential integrity:** Every `opinion_id` in relevance judgments corresponds to an actual file in `data/extracted/`
- **Coverage:** Every taxonomy issue has at least 1 query. Every query has at least 10 relevance judgments.
- **Score distribution:** No query has zero score-2 opinions. Overall distribution isn't wildly skewed.
- **ID uniqueness:** All query IDs are unique. No duplicate opinion IDs within a single query's judgments.
- **Completeness:** Taxonomy is populated for all topics. Total query count is 60-80.

Write a validation script (`src/validate_dataset.py`) that checks all of the above and reports any issues.

#### 2. Spot-Check Validation (subagents)

Spawn 3-4 subagents, each assigned ~5 randomly-selected queries. Each subagent:

1. Reads the query and its relevance judgments
2. Reads 3-4 of the judged opinions (mix of score-2 and score-1)
3. Independently assesses whether the scores seem correct per the rubric
4. Reports any disagreements or concerns

The main agent reviews the spot-check results and fixes any issues found.

#### 3. Scoring Harness Smoke Test (main agent)

Create a trivial baseline search engine to verify the harness works:

```python
# src/baselines/random_baseline.py
class RandomBaseline(SearchEngine):
    """Returns random opinion IDs. Should score poorly."""
    def search(self, query, top_k=20):
        # Return random opinion IDs from the corpus
        ...
```

Run: `python src/scorer.py --search-module src.baselines.random_baseline --dataset eval/dataset.json`

Verify:
- The harness runs without errors
- The scorecard output is formatted correctly
- The random baseline scores poorly (as expected — this confirms the eval isn't trivially easy)

#### 4. Finalize

- Fix any issues found during validation
- Tag the merge commit as `v1.0` after merging:
  ```
  git checkout main && git pull && git tag v1.0 && git push --tags
  ```

### Definition of Done
- Validation script passes with no errors
- Spot-checks confirm judgment quality
- Scoring harness runs end-to-end and produces a scorecard
- Random baseline scores poorly
- Sprint log updated, PR created, code reviewed, fixes applied, merged to main
- `v1.0` tag pushed

---

## Sprint Summary

| Sprint | Goal | Agent Strategy | Estimated Queries |
|--------|------|---------------|-------------------|
| 0 | Project scaffolding | Single agent | — |
| 1 | CoI taxonomy | Agent team (4 agents) | — |
| 2 | Other topics taxonomy | Parallel subagents (4) | — |
| 3 | Query generation | Parallel subagents | 60-80 generated |
| 4 | Relevance: CoI batch 1 | Agent team | ~12 judged |
| 5 | Relevance: CoI batch 2 | Agent team | ~13-18 judged |
| 6 | Relevance: Campaign + Gifts | Agent team | ~15-23 judged |
| 7 | Relevance: Lobbying + Other | Agent team | ~10-15 judged |
| 8 | Validation & smoke test | Single agent + subagents | — |

**Total: 9 sprints, yielding 60-80 fully-judged queries.**

---

## Appendix: Key Search Patterns for Agents

When searching the opinion JSON files, these patterns are most useful:

### Finding opinions by topic
```
Grep for "topic_primary": "conflicts_of_interest" across data/extracted/**/*.json
```

### Finding opinions citing a specific statute
```
Grep for "87100" in the citations.government_code arrays across data/extracted/**/*.json
```

### Finding opinions citing a specific prior opinion
```
Grep for the opinion ID (e.g., "A-24-003") across data/extracted/**/*.json
```

### Reading an opinion's key content efficiently
Focus on these fields (in order of usefulness):
1. `embedding.qa_text` — Best single-field summary of what the opinion is about
2. `sections.question` + `sections.conclusion` — The core Q&A
3. `embedding.summary` — Brief summary if available
4. `sections.facts` + `sections.analysis` — Full detail when needed
5. `content.full_text` — Last resort; often noisy especially for older opinions
