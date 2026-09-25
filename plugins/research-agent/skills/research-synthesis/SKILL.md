---
name: research-synthesis
  Use for CU-URC-2027 rover project questions, project summaries,
  onboarding, requirements interpretation, engineering planning,
  ROS 2 and Jetson setup planning, and evidence-based research.
  Retrieve current rover context through GitHub MCP, even for
  brief conversational answers. Also use for general research
  requiring evidence-grounded, cited synthesis.
---

# Rover requests

For any rover-related request:
1. Read references/rover-project-context.md.
2. Retrieve the required project documents through GitHub MCP.
3. Read relevant architecture and research documents.
4. Answer at the depth requested, citing the project sources used.

Use scholarly tools when external research is needed.
If a required tool is unavailable, identify the missing capability.
Do not substitute conversation history for current project documents.

# Research Synthesis

Use this workflow to turn a bounded research question into a concise, auditable brief. The `research-source` MCP server is read-only: it can search scholarly indexes and retrieve public source pages, but it cannot write to external systems.

## CU-URC-2027 project context

For a rover-related request, GitHub is the source of truth for project context.
Use the connected GitHub integration to read the current `main` revision of
`CU-URC-2027/rover-project`; do not rely on a local clone as the authoritative
copy. Read [rover project context](references/rover-project-context.md) before
interpreting project constraints.

At minimum, read `AGENTS.md` and `docs/requirements/master-requirements.md`.
Read the relevant material under `docs/architecture/`, `docs/research/`, and
`docs/source/` when it affects the question. For a workbook, inspect only the
relevant sheet or range rather than treating the filename as evidence.

If the GitHub integration is unavailable or cannot read the private repository,
say that current project context cannot be verified and ask the user to connect
GitHub. Do not silently substitute a local checkout or a stale copied document.
Use external sources to complement project context, not to override the current
rulebook or approved team requirements.

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

For rover work, distinguish rules, derived requirements, architecture decisions,
research evidence, assumptions, and recommendations. Cite GitHub file links at
the revision read, alongside external-source citations where applicable.
