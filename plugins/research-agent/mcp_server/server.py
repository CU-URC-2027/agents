"""A small, read-only MCP server for scholarly and public-web research.

All tool responses are structured dictionaries so a client can preserve source
metadata in an evidence ledger. The server deliberately exposes no write tools.
"""

from __future__ import annotations

import ipaddress
import json
import re
import socket
from html import unescape
from html.parser import HTMLParser
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlparse
from urllib.request import HTTPRedirectHandler, Request, build_opener

from mcp.server import MCPServer


mcp = MCPServer("Research Source")

USER_AGENT = "research-agent/0.1 (local educational MCP server)"
MAX_PAGE_BYTES = 1_500_000
MAX_TEXT_CHARS = 20_000


class _TextExtractor(HTMLParser):
    """Extract readable text while omitting scripts, styles, and navigation markup."""

    def __init__(self) -> None:
        super().__init__()
        self._parts: list[str] = []
        self._ignored_depth = 0
        self.title = ""
        self._in_title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"script", "style", "noscript", "svg", "template"}:
            self._ignored_depth += 1
        if tag == "title":
            self._in_title = True

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "noscript", "svg", "template"} and self._ignored_depth:
            self._ignored_depth -= 1
        if tag == "title":
            self._in_title = False

    def handle_data(self, data: str) -> None:
        if self._ignored_depth:
            return
        normalized = " ".join(data.split())
        if normalized:
            self._parts.append(normalized)
            if self._in_title:
                self.title = f"{self.title} {normalized}".strip()

    def text(self) -> str:
        return " ".join(self._parts)


def _public_host(hostname: str) -> None:
    """Reject loopback and private destinations before an outbound request."""

    if not hostname or hostname.lower() == "localhost":
        raise ValueError("Only public HTTP(S) hosts may be fetched.")

    try:
        addresses = socket.getaddrinfo(hostname, None, type=socket.SOCK_STREAM)
    except socket.gaierror as exc:
        raise ValueError(f"Could not resolve host: {hostname}") from exc

    for address in addresses:
        ip = ipaddress.ip_address(address[4][0])
        if not ip.is_global:
            raise ValueError("Only public HTTP(S) hosts may be fetched.")


def _validate_url(url: str) -> str:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("URL must use http or https.")
    if parsed.username or parsed.password:
        raise ValueError("URLs with embedded credentials are not allowed.")
    _public_host(parsed.hostname or "")
    return url


class _SafeRedirects(HTTPRedirectHandler):
    def redirect_request(self, req: Request, fp: Any, code: int, msg: str, headers: Any, newurl: str) -> Request | None:
        _validate_url(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def _get_json(url: str) -> dict[str, Any]:
    request = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    try:
        with build_opener(_SafeRedirects()).open(request, timeout=20) as response:
            return json.loads(response.read(MAX_PAGE_BYTES).decode("utf-8"))
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Source request failed: {exc}") from exc


def _publication_year(item: dict[str, Any]) -> int | None:
    for key in ("publication_year", "published_year"):
        if item.get(key):
            return int(item[key])
    for key in ("published", "issued", "published-print", "published-online"):
        parts = item.get(key, {}).get("date-parts", [[]])
        if parts and parts[0]:
            return int(parts[0][0])
    return None


@mcp.tool()
def search_openalex(query: str, max_results: int = 5) -> dict[str, Any]:
    """Search OpenAlex for scholarly works. Returns titles, dates, and source URLs."""

    query = query.strip()
    if not query:
        raise ValueError("query cannot be empty")
    count = max(1, min(max_results, 20))
    payload = _get_json(
        "https://api.openalex.org/works?" + urlencode({"search": query, "per-page": count})
    )
    works = []
    for item in payload.get("results", []):
        location = item.get("primary_location") or {}
        source = location.get("source") or {}
        works.append(
            {
                "title": item.get("display_name"),
                "year": _publication_year(item),
                "doi": item.get("doi"),
                "landing_page": location.get("landing_page_url") or item.get("id"),
                "venue": source.get("display_name"),
                "cited_by_count": item.get("cited_by_count"),
                "abstract_available": bool(item.get("abstract_inverted_index")),
            }
        )
    return {"provider": "OpenAlex", "query": query, "works": works}


@mcp.tool()
def search_crossref(query: str, max_results: int = 5) -> dict[str, Any]:
    """Search Crossref for registered scholarly publications and DOI metadata."""

    query = query.strip()
    if not query:
        raise ValueError("query cannot be empty")
    count = max(1, min(max_results, 20))
    payload = _get_json(
        "https://api.crossref.org/works?" + urlencode({"query.bibliographic": query, "rows": count})
    )
    works = []
    for item in payload.get("message", {}).get("items", []):
        titles = item.get("title") or []
        works.append(
            {
                "title": titles[0] if titles else None,
                "year": _publication_year(item),
                "doi": item.get("DOI"),
                "landing_page": item.get("URL"),
                "venue": (item.get("container-title") or [None])[0],
                "publisher": item.get("publisher"),
                "type": item.get("type"),
            }
        )
    return {"provider": "Crossref", "query": query, "works": works}


@mcp.tool()
def fetch_public_page(url: str, max_chars: int = 12000) -> dict[str, Any]:
    """Fetch readable text from a public HTML page after blocking private-network targets."""

    _validate_url(url)
    limit = max(500, min(max_chars, MAX_TEXT_CHARS))
    request = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "text/html,application/xhtml+xml"})
    try:
        with build_opener(_SafeRedirects()).open(request, timeout=20) as response:
            content_type = response.headers.get_content_type()
            final_url = response.geturl()
            _validate_url(final_url)
            raw = response.read(MAX_PAGE_BYTES)
    except (HTTPError, URLError, TimeoutError) as exc:
        raise RuntimeError(f"Page request failed: {exc}") from exc

    if content_type not in {"text/html", "application/xhtml+xml"}:
        raise ValueError(f"Only HTML pages are supported; received {content_type}.")

    document = raw.decode("utf-8", errors="replace")
    parser = _TextExtractor()
    parser.feed(document)
    text = re.sub(r"\s+", " ", unescape(parser.text())).strip()
    return {
        "url": final_url,
        "title": parser.title or None,
        "text": text[:limit],
        "truncated": len(text) > limit,
    }


def main() -> None:
    """Run the local MCP server over standard input/output."""
    mcp.run()


if __name__ == "__main__":
    main()
