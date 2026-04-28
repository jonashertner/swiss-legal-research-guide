"""Sitemap and robots.txt emitters."""

from __future__ import annotations

from datetime import date
from pathlib import Path


def emit_sitemap(
    base_url: str,
    base_path: str,
    urls: list[str],
    out_path: Path,
) -> None:
    """Write a basic sitemap.xml."""
    today = date.today().isoformat()
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for url in urls:
        full = f"{base_url.rstrip('/')}{base_path.rstrip('/')}/{url.lstrip('/')}".replace("//", "/")
        full = full.replace("https:/", "https://").replace("http:/", "http://")
        lines += [
            "  <url>",
            f"    <loc>{full}</loc>",
            f"    <lastmod>{today}</lastmod>",
            "  </url>",
        ]
    lines.append("</urlset>")
    out_path.write_text("\n".join(lines), encoding="utf-8")


def emit_robots(base_url: str, base_path: str, out_path: Path) -> None:
    """Permissive robots.txt with explicit AI crawler allowance."""
    sitemap = f"{base_url.rstrip('/')}{base_path.rstrip('/')}/sitemap.xml".replace("//", "/")
    sitemap = sitemap.replace("https:/", "https://").replace("http:/", "http://")
    body = "\n".join([
        "# This guide is intentionally machine-readable.",
        "# All crawlers — including AI training and research bots — are welcome.",
        "",
        "User-agent: *",
        "Allow: /",
        "",
        "User-agent: GPTBot",
        "Allow: /",
        "",
        "User-agent: ClaudeBot",
        "Allow: /",
        "",
        "User-agent: Claude-Web",
        "Allow: /",
        "",
        "User-agent: PerplexityBot",
        "Allow: /",
        "",
        "User-agent: Google-Extended",
        "Allow: /",
        "",
        "User-agent: CCBot",
        "Allow: /",
        "",
        f"Sitemap: {sitemap}",
        "",
    ])
    out_path.write_text(body, encoding="utf-8")
