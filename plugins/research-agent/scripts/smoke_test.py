"""Test the packaged launch configuration; --live also retrieves a known paper."""

import argparse
import asyncio
import json
import shutil
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def check(live: bool) -> None:
    root = Path(__file__).resolve().parents[1]
    config = json.loads((root / ".mcp.json").read_text())["mcpServers"]["research-source"]
    executable = shutil.which(config["command"])
    if executable is None:
        raise RuntimeError("uv is not on PATH. Install uv and restart your terminal/Codex.")
    parameters = StdioServerParameters(command=executable, args=config["args"],
        cwd=str(root / config["cwd"]))
    async with stdio_client(parameters) as (read, write):
        async with ClientSession(read, write, read_timeout_seconds=120) as session:
            await session.initialize()
            names = sorted(tool.name for tool in (await session.list_tools()).tools)
            expected = ["fetch_public_page", "search_crossref", "search_openalex"]
            if names != expected:
                raise RuntimeError(f"Unexpected tool list: {names}")
            print("PASS: packaged MCP launch and all three tools")
            if live:
                result = await session.call_tool("fetch_public_page", {
                    "url": "https://arxiv.org/abs/1706.03762", "max_chars": 6000})
                if result.is_error:
                    raise RuntimeError(f"Live retrieval failed: {result.content}")
                text = " ".join(getattr(block, "text", "") for block in result.content)
                if "Attention Is All You Need" not in text or "Transformer" not in text:
                    raise RuntimeError("The source response did not contain the expected paper.")
                print("PASS: arXiv page retrieved through the packaged MCP server")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true", help="Make a public request to arXiv")
    asyncio.run(check(parser.parse_args().live))
