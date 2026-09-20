# CU-URC-2027 agents

Private team distribution of locally executed Codex plugins. The canonical
source is `https://github.com/CU-URC-2027/agents`.

Start with [HOW-TO.md](HOW-TO.md) for teammate installation, maintenance, and
development instructions.

Skills and all supporting references, templates, scripts, and assets belong
under each plugin's `skills/` directory. Teammates install a versioned local
copy managed by Codex; they do not manually copy or maintain these files.

## First installation

1. Install Codex and [uv](https://docs.astral.sh/uv/getting-started/installation/).
   Verify `codex --version` and `uv --version` in a terminal, then restart Codex.
2. Authenticate Git with a GitHub account that can read the private repository.
   If the organization requires SSO, authorize that account/credential for it.
3. Add the team marketplace and install the plugin:

   ```text
   codex plugin marketplace add https://github.com/CU-URC-2027/agents.git
   codex plugin add research-agent@cu-urc-2027
   ```

   `cu-urc-2027` is the team catalog identifier, separate from GitHub visibility.
4. Open a new Codex task and run the example in
   [the Research Agent guide](plugins/research-agent/README.md).

The first tool invocation downloads Python and locked dependencies if needed.
All subsequent launches reuse the local environment. uv and Codex must be
installed once; cloning the source and creating a virtual environment manually
are unnecessary for teammate installation.

## Updating

Maintainers test changes, increment the plugin version for a release, and push
the release to GitHub. Teammates refresh the marketplace and reinstall:

```text
codex plugin marketplace upgrade cu-urc-2027
codex plugin add research-agent@cu-urc-2027
```

Start a new task afterward. Updates are explicit, not silently promised on
every agent invocation. Teams can select a tested tag/commit with `--ref` when
adding the marketplace for reproducible rollouts.

## Repository layout

```text
.agents/plugins/marketplace.json  Team plugin catalog
.github/workflows/test.yml       Windows/macOS/Linux checks
plugins/research-agent/
  .codex-plugin/plugin.json      Codex plugin identity
  .mcp.json                     Portable local launch configuration
  pyproject.toml, uv.lock        Python package and locked dependencies
  skills/research-synthesis/    Skill, references, and metadata
  mcp_server/                  Local source tools
  tests/                       Offline and MCP protocol tests
```

Add future agents as sibling directories under `plugins/`, with an entry in
the marketplace. Avoid machine-specific paths and committed environments.

## Troubleshooting

- `uv` not found: install uv on the host that runs Codex and restart the app.
- Repository not found: check the URL, account membership, and organization SSO.
  GitHub uses the same response for inaccessible private repositories.
- First tool startup times out: run `uv sync --locked` in the installed plugin
  folder once to expose any download/proxy error, then retry in a new task.
- Old behavior: refresh the marketplace, reinstall the version, and open a new task.
- Citation quality: inspect the source; metadata discovery is not verification.

No open-source license has been selected. Keep distribution within the team
until the repository owners choose licensing terms.
