---
name: research-synthesis
description: "Research a question and produce an evidence-grounded, cited brief using the local research-source MCP tools. Use when accuracy, traceability, and stated uncertainty matter; do not use for a quick uncited explanation."
---

# Research Synthesis

Use this workflow to turn a bounded research question into a concise, auditable brief. The `research-source` MCP server is read-only: it can search scholarly indexes and retrieve public source pages, but it cannot write to external systems.

## Scope the question

Before searching, state the research question, intended audience, boundaries (time period, geography, technology, or population), and what a useful answer will decide. If a missing boundary would materially change the conclusion, ask one focused question. Otherwise, state a reasonable assumption.

Break the question into a small set of factual subquestions. Search separately for definitions, outcomes, limitations, and counter-evidence rather than treating one result as a complete answer.

## Gather evidence

Use `search_openalex` and `search_crossref` for scholarly and bibliographic discovery. Use `fetch_public_page` to inspect a primary source, paper landing page, standards page, or official documentation discovered during research. Prefer original studies, standards bodies, public datasets, and official documentation over summaries.

Maintain a working evidence ledger with the claim, supporting source, source type, publication date, and caveat. Read [research standards](references/research-standards.md) when evaluating sources or resolving disagreement.

## Verify before writing

Do not turn a search snippet into a factual claim. Open the source when a claim is material, surprising, causal, numerical, or likely to be contested. Seek independent corroboration for material claims when sources are available. Distinguish:

- reported evidence from your synthesis;
- correlation from causation;
- absence of evidence from evidence of absence; and
- a source's conclusion from a general conclusion.

If sources disagree, represent the disagreement, explain the likely reason when supported, and avoid a false consensus. If support is thin, say so directly.

## Deliver the brief

Start with a direct answer calibrated to the available evidence. Then include the key findings, limitations or open questions, and a source list with title, publisher or venue, date when available, and URL. Attach a citation to each material claim. Do not cite a source that does not support the claim beside it.

For a decision-oriented request, add a short recommendation and label it as an inference when it goes beyond what the sources establish.
