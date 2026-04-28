"""Build artifacts that make the guide first-class machine-readable."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .parser import first_sentence


@dataclass
class SiteContext:
    base_url: str  # full URL with scheme, e.g. https://example.ch
    base_path: str  # path prefix, e.g. /repo/ for project pages, / for custom domain
    title: str
    subtitle: str
    description: str
    version: str


@dataclass
class ChapterArtifact:
    slug: str
    chapter: str
    title: str
    short_title: str
    description: str
    body_md: str
    sections: list["SectionArtifact"]


@dataclass
class SectionArtifact:
    slug: str
    title: str
    description: str
    body_md: str


def emit_section_md_mirrors(
    site: SiteContext,
    chapter: ChapterArtifact,
    out_dir: Path,
) -> list[Path]:
    """Write per-section .md mirror files into out_dir."""
    written: list[Path] = []
    for section in chapter.sections:
        path = out_dir / f"{section.slug}.md"
        canonical = (
            f"{site.base_url.rstrip('/')}{site.base_path}de/{chapter.slug}/#{section.slug}"
        )
        content = (
            f"<!-- Canonical HTML: {canonical} -->\n"
            f"# {chapter.chapter}.{section.slug} — {section.title}\n\n"
            f"_From: {chapter.title} — {site.title} ({site.version})_\n\n"
            f"{section.body_md.lstrip('# ').lstrip()}\n"
        )
        path.write_text(content, encoding="utf-8")
        written.append(path)
    return written


def emit_llms_txt(
    site: SiteContext,
    chapters: list[ChapterArtifact],
    out_path: Path,
) -> None:
    """Write the /llms.txt index file (https://llmstxt.org convention)."""
    base = f"{site.base_url.rstrip('/')}{site.base_path}"
    lines = [
        f"# {site.title}",
        "",
        f"> {site.description}",
        "",
        f"_Authors:_ Kaspar Ehrenzeller, Daniel Brugger (HSG). _Version:_ {site.version}.",
        "",
        "## Chapters",
        "",
    ]
    for ch in chapters:
        ch_url = f"{base}de/{ch.slug}/" if ch.slug else f"{base}de/"
        lines.append(f"- [{ch.chapter}. {ch.short_title}]({ch_url}): {ch.description}")
        for section in ch.sections:
            sect_md = f"{base}de/{ch.slug}/{section.slug}.md" if ch.slug else f"{base}de/{section.slug}.md"
            lines.append(f"  - [{section.title}]({sect_md}): {section.description}")
    lines += [
        "",
        "## Conventions",
        "",
        "- Append `.md` to any section slug to fetch the raw Markdown for that section.",
        f"- Full guide as a single Markdown file: {base}llms-full.txt",
        "- Each chapter URL also accepts `.md`-suffixed section paths under it.",
        "",
        "## Source",
        "",
        f"- Repository: see footer of any HTML page.",
        f"- License: CC BY 4.0 (content), MIT (code).",
        "",
    ]
    out_path.write_text("\n".join(lines), encoding="utf-8")


def emit_llms_full_txt(
    site: SiteContext,
    chapters: list[ChapterArtifact],
    out_path: Path,
) -> None:
    """Write /llms-full.txt — the entire guide as one Markdown document."""
    parts = [
        f"# {site.title}",
        "",
        f"_{site.subtitle}_",
        "",
        f"Authors: Kaspar Ehrenzeller, Daniel Brugger (HSG).",
        f"Version: {site.version}.",
        "",
        "License: CC BY 4.0 — attribution required.",
        "",
        "---",
        "",
    ]
    for ch in chapters:
        parts.append(f"## {ch.chapter}. {ch.title}")
        parts.append("")
        parts.append(ch.body_md.strip())
        parts.append("")
        parts.append("---")
        parts.append("")
    out_path.write_text("\n".join(parts), encoding="utf-8")


def chapter_description(body_md: str, fallback: str = "") -> str:
    """Pull a one-line description from the start of a chapter body."""
    for paragraph in body_md.split("\n\n"):
        if paragraph.strip().startswith("#"):
            continue
        sent = first_sentence(paragraph)
        if sent:
            return sent
    return fallback
