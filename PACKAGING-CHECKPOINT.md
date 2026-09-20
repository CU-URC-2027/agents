# Packaging checkpoint

Initial package for the private repository `CU-URC-2027/agents`.

## Passed locally

- Codex plugin manifest validation using the Plugin Creator validator.
- Seven offline and MCP integration tests on Windows with Python 3.14.6.
- The manifest's exact uv launch command from a fresh copy in a path containing
  spaces; uv created the environment and installed all locked dependencies.
- Live arXiv retrieval through the newly packaged MCP process.
- Python wheel and source-distribution builds.
- Registration of the local `cu-urc-2027` marketplace in Codex.

The existing `research-agent-local` plugin remains the installed working
prototype. Registering the new catalog does not replace that installation.

## Passed on GitHub

The initial code commit `632917b90a75ab881c6df0d88e641f73ab944497` passed
[the three-platform workflow](https://github.com/CU-URC-2027/agents/actions/runs/35480121199).
Windows, macOS, and Ubuntu runners each installed locked dependencies, passed
all seven tests, and built the Python distributions using Python 3.12.
This verifies the local server package on each OS; it does not verify every
Codex desktop installation or a machine with no Python installation.

## Pending

- A teammate's first installation through the private GitHub marketplace.
- No-Python first installation: uv's attempted managed Python 3.12 download
  on this Windows host encountered a missing-target/minor-version-link error.
  The successful clean-copy test used the already installed Python 3.14.6.
  uv supports automatic Python downloads, but that scenario is not verified
  here. If needed, install Python 3.12 separately, then rerun the smoke check.

## GitHub destination

Authentication was verified as `liamolczak`, with read/write access to the
private repository. The repository was confirmed empty before the initial
upload. This checkout uses that account explicitly for GitHub access and uses
its GitHub noreply address for commit attribution; other repositories' Git
settings are unchanged. Subsequent changes should use a feature branch and
preserve repository history.

## Scope of this release

Packaging changes preserve the existing research method and source tool logic.
The known search-identification limitation remains: a matching title alone
does not establish that a search result is the original paper. See the plugin
README for the current retrieval and security limitations.

The marketplace/ZIP is the complete agent distribution, including skills and
references. The optional Python wheel contains the executable source tools
only; installing that wheel by itself does not install the Codex skill.
