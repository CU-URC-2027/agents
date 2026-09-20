# How to use and maintain CU-URC-2027 agents

This repository distributes Codex agents for the CU-URC-2027 team. Each agent
is installed locally on a teammate's computer, but its code, skills,
references, scripts, and release history are maintained here on GitHub.

## Use an agent

1. Install [Codex](https://openai.com/codex/) and
   [uv](https://docs.astral.sh/uv/getting-started/installation/). Restart Codex
   after installing uv so it can find `uv` on your PATH.
2. Make sure your GitHub account can read the private `CU-URC-2027/agents`
   repository. Complete organization SSO authorization if GitHub requests it.
   Connect GitHub in Codex as well if you will use rover-specific agents: the
   Research Agent reads current project context from the private
   `CU-URC-2027/rover-project` repository through that integration.
3. In a terminal, add the team's marketplace and install an agent:

   ```text
   codex plugin marketplace add https://github.com/CU-URC-2027/agents.git
   codex plugin add research-agent@cu-urc-2027
   ```

4. Start a **new Codex task** and invoke a skill by name. For example:

   ```text
   Use $research-synthesis to read https://arxiv.org/abs/1706.03762.
   Explain what the paper introduced and which translation tasks it evaluated.
   Cite the source and distinguish abstract-supported claims from anything
   requiring the full paper.
   ```

The first use may download Python and locked dependencies. Later launches reuse
the local environment.

## Update an installed agent

When a maintainer publishes changes, refresh the marketplace, reinstall the
agent, and begin a new task:

```text
codex plugin marketplace upgrade cu-urc-2027
codex plugin add research-agent@cu-urc-2027
```

## Develop an agent

Use a local clone of this GitHub repository as the only editable source of
truth. Do **not** edit the plugin files installed in Codex's cache: Codex can
replace them whenever the marketplace is refreshed or the plugin is reinstalled.

```text
git clone https://github.com/CU-URC-2027/agents.git
cd agents
git switch -c your-branch-name
```

For the Research Agent, work in `plugins/research-agent`. Before committing,
run:

```text
cd plugins/research-agent
uv sync --locked
uv run --locked python -m unittest discover -s tests -v
uv run --locked python scripts/smoke_test.py
uv build
```

Use `uv run --locked python scripts/smoke_test.py --live` only when you also
want to verify a public network retrieval. It is not required for ordinary
offline tests.

Then commit, push your feature branch, and open a pull request for team review:

```text
git add .
git commit -m "Describe the change"
git push -u origin your-branch-name
```

After the branch is reviewed and merged, teammates can use the update commands
above to install the released code.

## Add a future agent

1. Create a sibling directory under `plugins/`.
2. Include the plugin manifest, portable `.mcp.json` if the agent needs tools,
   and every `SKILL.md`, reference, template, script, or asset that it needs.
3. Add its entry to `.agents/plugins/marketplace.json`.
4. Test on Windows, macOS, and Linux through the GitHub Actions workflow.
5. Document one simple example prompt in that agent's README.

Keep paths relative and cross-platform. Never commit virtual environments,
credentials, access tokens, or a user-specific local path.

## Troubleshooting

- **`uv` is not found:** install uv, close and reopen Codex, then retry.
- **GitHub says the repository is unavailable:** confirm your team membership
  and SSO authorization; private repositories intentionally appear unavailable
  to accounts without access.
- **Changes do not appear in Codex:** refresh the marketplace, reinstall the
  plugin, and start a new task.
- **A source cannot be read:** confirm whether it is a public HTML page. The
  current Research Agent does not bypass logins or publisher restrictions, and
  it does not read PDFs directly from a web URL.

## Responsibility boundaries

The plugin executes source tools locally, while Codex provides the model used
for reasoning. Treat agent output as research assistance: verify sources,
distinguish rules from derived requirements and assumptions, and keep final
engineering decisions with the team.
