# Research Agent

A Codex skill and three read-only tools, executed on the teammate's computer.
The complete skill folder (instructions, references, and metadata) is versioned
with the server. Install through the repository marketplace; no separate Python
package registry is required.

## Runtime

Codex starts `uv run --locked --no-dev research-agent-mcp` in the installed plugin
directory. Install [uv](https://docs.astral.sh/uv/getting-started/installation/)
once and make sure Codex can find `uv` on PATH. uv uses a compatible Python
installation (3.11 through 3.14), downloads one when needed, and creates the
dependency environment automatically on first use.
The first launch needs network access and may take longer than later launches.
Restart Codex after installing uv so the app receives the updated PATH.

No hard-coded username, home directory, virtual-environment path, Bash, or
PowerShell launcher is required. The target platforms are Windows, macOS, and
Linux; iOS/iPadOS are not supported local Python hosts for this package.
Codex performs the reasoning using its configured model; a local MCP process
does not imply a locally running model or offline research.

## Tools

- `search_openalex`: scholarly metadata discovery.
- `search_crossref`: DOI and bibliographic metadata discovery.
- `fetch_public_page`: text extraction from public HTML pages.

Search results can include duplicate or unrelated records. Confirm title,
authors, publication year, and the original source before citing a result.
HTML retrieval does not read PDFs or bypass publisher restrictions. DNS and
redirect checks reject private destinations, but the fetcher is not a complete
network isolation boundary (for example, it does not pin DNS resolution).

## Validate a checkout

From this plugin directory, on any supported desktop OS:

```text
uv sync --locked
uv run --locked python -m unittest discover -s tests -v
uv build
```

Tests verify parsing, source metadata, URL rejection, and the actual MCP
handshake through the installed console command from an unrelated directory.
Tests do not require live research services.

For a launch check with readable output, run `uv run --locked python
scripts/smoke_test.py`. Add `--live` to retrieve the known arXiv paper through
the packaged MCP server (this makes a public network request).

## Try the skill

```text
Use $research-synthesis to read https://arxiv.org/abs/1706.03762.
Explain what the paper introduced and which translation tasks it evaluated.
Cite the source and distinguish abstract-supported claims from anything
requiring the full paper.
```

## Dependency updates

Change the tested MCP version in `pyproject.toml`, regenerate `uv.lock`, and run
the tests on all three operating systems before merging. Keep runtime updates
separate from changes to the research method so regressions are easy to isolate.
