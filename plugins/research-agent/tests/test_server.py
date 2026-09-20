"""Deterministic checks; no public services or credentials required."""

import socket
import unittest
from unittest.mock import patch

from mcp_server import server


class SourceTests(unittest.TestCase):
    def test_extracts_visible_text(self):
        parser = server._TextExtractor()
        parser.feed("<title>Example</title><p>Visible</p><script>hidden()</script>")
        self.assertEqual(parser.title, "Example")
        self.assertEqual(parser.text(), "Example Visible")

    def test_rejects_unsafe_urls_without_dns(self):
        for url in ("file:///etc/passwd", "https://user:secret@example.com/", "http://localhost"):
            with self.subTest(url=url), self.assertRaises(ValueError):
                server._validate_url(url)

    @patch("mcp_server.server.socket.getaddrinfo")
    def test_rejects_private_and_loopback_addresses(self, resolve):
        for address in ("127.0.0.1", "10.0.0.1", "169.254.169.254", "::1"):
            resolve.return_value = [(socket.AF_INET, socket.SOCK_STREAM, 6, "", (address, 80))]
            with self.subTest(address=address), self.assertRaises(ValueError):
                server._validate_url("https://example.org")

    @patch("mcp_server.server._get_json")
    def test_openalex_metadata_and_result_limit(self, request):
        request.return_value = {"results": [{"display_name": "Paper", "publication_year": 2017,
            "doi": "https://doi.org/example", "primary_location": None}]}
        result = server.search_openalex(" Paper ", 100)
        self.assertEqual(result["query"], "Paper")
        self.assertEqual(result["works"][0]["year"], 2017)
        self.assertIn("per-page=20", request.call_args.args[0])

    @patch("mcp_server.server._get_json")
    def test_crossref_publication_year(self, request):
        request.return_value = {"message": {"items": [{"title": ["Paper"],
            "published": {"date-parts": [[2017, 6, 12]]}, "DOI": "example"}]}}
        self.assertEqual(server.search_crossref("Paper")["works"][0]["year"], 2017)


if __name__ == "__main__":
    unittest.main()
