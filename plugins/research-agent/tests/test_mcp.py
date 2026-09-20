"""Check the real installed console entry point and MCP wire protocol."""

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class ProtocolTests(unittest.IsolatedAsyncioTestCase):
    async def test_installed_command_from_unrelated_directory(self):
        command = shutil.which("research-agent-mcp")
        self.assertIsNotNone(command, "The package's console entry point is not installed")
        with tempfile.TemporaryDirectory(prefix="research agent test ") as temporary:
            parameters = StdioServerParameters(command=command, cwd=temporary)
            async with stdio_client(parameters) as (read, write):
                async with ClientSession(read, write, read_timeout_seconds=20) as session:
                    await session.initialize()
                    result = await session.list_tools()
                    self.assertEqual({tool.name for tool in result.tools},
                        {"search_openalex", "search_crossref", "fetch_public_page"})
                    result = await session.call_tool("fetch_public_page", {"url": "file:///etc/passwd"})
                    self.assertTrue(result.is_error)
                    self.assertTrue(result.content)
                    self.assertEqual(len((await session.list_tools()).tools), 3)

    async def test_manifest_launch_from_clean_copy_with_spaces(self):
        source = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory(prefix="research agent install ") as temporary:
            installed = Path(temporary) / "plugin with spaces"
            shutil.copytree(source, installed, ignore=shutil.ignore_patterns(
                ".venv", "__pycache__", "*.egg-info", "dist", "build", ".git"))
            config = json.loads((installed / ".mcp.json").read_text())["mcpServers"]["research-source"]
            command = shutil.which(config["command"])
            self.assertIsNotNone(command, "uv must be on PATH for plugin installation")
            parameters = StdioServerParameters(command=command, args=config["args"],
                cwd=str(installed / config["cwd"]))
            async with stdio_client(parameters) as (read, write):
                async with ClientSession(read, write, read_timeout_seconds=120) as session:
                    await session.initialize()
                    self.assertEqual({tool.name for tool in (await session.list_tools()).tools},
                        {"search_openalex", "search_crossref", "fetch_public_page"})


if __name__ == "__main__":
    unittest.main()
