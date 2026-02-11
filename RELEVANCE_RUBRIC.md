# Relevance Judgment Rubric

This rubric guides the grading of opinions against test queries. Consistent application is critical — the entire eval suite's value depends on judgments being reliable and reproducible.

## Core Principle

Relevance is about the **legal question and analysis**, not about matching facts exactly. FPPC opinions rarely have identical facts. Two opinions can both be "highly relevant" to a query even if one involves a city council member and the other involves a school board trustee, as long as they address the same legal issue.

## Score Definitions

### Score 2 — Highly Relevant

The opinion addresses the **same core legal question or issue** as the query. An attorney researching this query would definitely want to read this opinion.

**Criteria (any one sufficient):**
- Analyzes the same legal standard or test applied to similar (not necessarily identical) facts
- Reaches a conclusion directly applicable to the query's scenario
- Provides the leading or most thorough analysis of the legal issue raised by the query

**Examples:**
- Query: "Must a city council member recuse from voting on a contract involving a property near their home?"
  - Opinion A-24-003 (Mills Act / real property proximity): **Score 2** — Directly analyzes recusal under Regulation 18702.2(a)(7) for officials with real property within 500 feet of a decision property
  - An opinion analyzing whether a planning commissioner must recuse from a zoning decision affecting property near their home: **Score 2** — Same legal issue (proximity-based recusal for real property) even though the governmental body and decision type differ

### Score 1 — Relevant

The opinion discusses **related legal concepts** that provide useful context, analogies, or background. An attorney would find it helpful as secondary reading but it doesn't directly answer the query.

**Criteria (any one sufficient):**
- Discusses the same statutory section but applies a different subsection or standard
- Addresses a related but distinct conflict-of-interest scenario (e.g., the query asks about real property proximity but the opinion addresses business entity interest)
- Provides important background on how the FPPC applies a relevant regulation, even if the specific issue differs
- Involves the same type of governmental decision but a different type of financial interest

**Examples:**
- Query: "Must a city council member recuse from voting on a contract involving a property near their home?"
  - An opinion about recusal where the official has a financial interest in a business entity that contracts with the city: **Score 1** — Same recusal framework (Section 87100) but different interest type (business vs. real property)
  - An opinion about Section 1090's prohibition on self-dealing in government contracts without a proximity issue: **Score 1** — Related statute often analyzed alongside the Act, but different legal standard

### Score 0 — Not Relevant

The opinion does **not meaningfully address** the query's legal question. An attorney researching this query would not benefit from reading it.

**Examples:**
- Query: "Must a city council member recuse from voting on a contract involving a property near their home?"
  - An opinion about campaign contribution limits for local candidates: **Score 0**
  - An opinion about lobbyist registration requirements: **Score 0**
  - An opinion about Form 700 filing deadlines (even though Form 700 relates to conflicts of interest): **Score 0** — procedural filing question, not a recusal analysis

## Edge Cases

### Same legal issue, opposite conclusion
If the opinion addresses the same legal issue but concludes the official does NOT need to recuse (e.g., because the financial effect is not material), it is still **Score 2**. The opinion is highly relevant precisely because it shows how the standard is applied, including cases where it doesn't trigger recusal.

### Superseded opinions
If an older opinion has been effectively superseded by a regulation change or later opinion, it is still judged on topical relevance. Score it based on whether it addresses the query's legal issue. A search engine that surfaces both old and new opinions on the same issue is doing its job — the attorney can assess currency themselves.

### Poor OCR quality
If an opinion is topically relevant but has poor text quality due to OCR issues, still score it based on its actual content (to the extent discernible). The eval measures relevance, not data quality.

### Procedural vs. substantive
Opinions that merely deny a request for advice without analysis (e.g., "we decline to issue an opinion because...") should generally be **Score 0** unless the denial itself discusses the substantive legal issue in a meaningful way.

### Opinions addressing multiple issues
Some opinions address several distinct legal questions. Score based on whether **any** of the issues addressed are relevant to the query. If one of three questions in the opinion matches the query's issue, it can still be Score 2.

### Very broad queries
For broad queries like "conflict of interest recusal," be selective. Not every conflict-of-interest opinion is relevant — only those that specifically discuss the recusal analysis (when and why an official must step aside). Opinions about disclosure requirements, filing deadlines, or other aspects of conflict-of-interest law that don't address recusal would be Score 0 or 1.

## Calibration Checklist

Before submitting judgments for a query, verify:

1. **At least 10 opinions judged** — If you can't find 10 opinions worth judging (score >= 1), the query may be too narrow; flag it for review.
2. **At least 2-3 opinions scored as 2** — If no opinions are highly relevant, the query may not correspond to a real issue in the corpus; flag it for review.
3. **Rationale written for every judgment** — Keep rationales brief (1-2 sentences) but specific enough that another reviewer could understand the reasoning.
4. **No score inflation** — A Score 1 opinion should genuinely help an attorney researching the query, not just mention a related keyword.
5. **Consider the query type** — A keyword query like `"Section 87103 real property 500 feet"` may have more precisely relevant opinions than a broad fact pattern. Adjust expectations, not standards.
