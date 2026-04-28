#!/usr/bin/env python3
"""Build the Swiss legal research guide site.

Reads Markdown chapters from content/de/, applies custom inline rules
(glossary, cross-references), renders to HTML through Jinja2 templates,
and emits LLM artifacts (llms.txt, llms-full.txt, per-section .md mirrors)
plus sitemap.xml and robots.txt.

Usage:
    python build.py [--base-path /repo/]
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path
from typing import Any

import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape

from lib.llm_artifacts import (
    ChapterArtifact,
    SectionArtifact,
    SiteContext,
    chapter_description,
    emit_llms_full_txt,
    emit_llms_txt,
    emit_section_md_mirrors,
)
from lib.parser import (
    first_sentence,
    make_renderer,
    render_chapter,
    slugify_de,
    split_frontmatter,
)
from lib.sitemap import emit_robots, emit_sitemap


ROOT = Path(__file__).parent
CONTENT = ROOT / "content"
TEMPLATES = ROOT / "templates"
STYLES = ROOT / "styles"
ASSETS = ROOT / "assets"
DIST = ROOT / "dist"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--base-path",
        default=None,
        help="URL path prefix (e.g. /repo/ for GitHub Pages project sites). "
             "Overrides site.base_path in meta.yml.",
    )
    p.add_argument(
        "--base-url",
        default=None,
        help="Full base URL (e.g. https://example.ch). Overrides site.base_url.",
    )
    p.add_argument("--out", default=str(DIST), help="Output directory (default: dist/)")
    return p.parse_args()


def load_meta() -> dict[str, Any]:
    return yaml.safe_load((CONTENT / "meta.yml").read_text(encoding="utf-8"))


def load_glossary() -> dict[str, dict[str, Any]]:
    raw = yaml.safe_load((CONTENT / "de" / "glossary.yml").read_text(encoding="utf-8")) or {}
    out: dict[str, dict[str, Any]] = {}
    for key, value in raw.items():
        out[key] = value
        out[str(key).upper()] = value
    return out


def load_references() -> dict[str, str]:
    return yaml.safe_load((CONTENT / "de" / "references.yml").read_text(encoding="utf-8")) or {}


def discover_chapters() -> list[Path]:
    return sorted((CONTENT / "de").glob("[0-9][0-9]-*.md"))


def main() -> int:
    args = parse_args()
    out = Path(args.out)
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True, exist_ok=True)

    meta = load_meta()
    glossary = load_glossary()
    references = load_references()

    base_url = args.base_url or meta["site"].get("base_url", "")
    base_path = args.base_path or meta["site"].get("base_path", "/")
    if not base_path.endswith("/"):
        base_path += "/"

    site = SiteContext(
        base_url=base_url,
        base_path=base_path,
        title=meta["site"]["title"],
        subtitle=meta["site"]["subtitle"],
        description=meta["site"]["description"],
        version=meta["version"],
    )

    md = make_renderer(references)

    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES)),
        autoescape=select_autoescape(enabled_extensions=("html",), default_for_string=False),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    env.globals["site"] = {
        "title": site.title,
        "subtitle": site.subtitle,
        "description": site.description,
        "version": site.version,
        "base_url": site.base_url,
        "base_path": site.base_path,
        "authors": meta["authors"],
        "license": meta["license"],
        "repository": meta["repository"],
    }
    env.globals["meta"] = meta
    env.globals["nav_chapters"] = []  # filled below

    # Render chapters
    chapter_files = discover_chapters()
    rendered: list[dict[str, Any]] = []
    artifacts: list[ChapterArtifact] = []

    for path in chapter_files:
        text = path.read_text(encoding="utf-8")
        fm, body = split_frontmatter(text)
        if not fm:
            print(f"WARN: {path.name} has no frontmatter; skipping.", file=sys.stderr)
            continue
        result = render_chapter(body, md, glossary)
        rendered.append({
            "path": path,
            "fm": fm,
            "body_md": body,
            "result": result,
        })

    # Build nav from chapters in order
    env.globals["nav_chapters"] = [
        {
            "slug": r["fm"]["slug"],
            "short_title": r["fm"].get("short_title", r["fm"]["title"]),
            "chapter": r["fm"].get("chapter", ""),
            "url": _chapter_url(site.base_path, r["fm"]["slug"]),
        }
        for r in rendered
    ]

    # Per-chapter HTML render
    chapter_template = env.get_template("chapter.html.j2")
    index_template = env.get_template("index.html.j2") if (TEMPLATES / "index.html.j2").exists() else chapter_template

    for r in rendered:
        fm = r["fm"]
        slug = fm["slug"]
        is_index = fm.get("is_index", False) or fm.get("order", 999) == 0 or slug == "einleitung"
        body_html = r["result"].html
        headings = r["result"].headings
        ctx = {
            "frontmatter": fm,
            "body_html": body_html,
            "headings": [h.__dict__ for h in headings],
            "chapter_slug": slug,
            "is_index": is_index,
            "edit_url": _edit_url(meta["repository"], r["path"]),
            "prev_chapter": _neighbor(rendered, r, -1, site.base_path),
            "next_chapter": _neighbor(rendered, r, +1, site.base_path),
        }
        if is_index:
            html = index_template.render(**ctx)
            (out / "index.html").write_text(_redirect_html(site.base_path), encoding="utf-8")
            de_dir = out / "de"
            de_dir.mkdir(parents=True, exist_ok=True)
            (de_dir / "index.html").write_text(html, encoding="utf-8")
        else:
            html = chapter_template.render(**ctx)
            chapter_dir = out / "de" / slug
            chapter_dir.mkdir(parents=True, exist_ok=True)
            (chapter_dir / "index.html").write_text(html, encoding="utf-8")

        # Per-section .md mirrors
        chapter_md_dir = out / "de" / (slug if not is_index else "")
        chapter_md_dir.mkdir(parents=True, exist_ok=True)
        sections: list[SectionArtifact] = []
        for h in headings:
            if h.level != 2:
                continue
            section_md = r["result"].section_md.get(h.slug, "")
            sections.append(SectionArtifact(
                slug=h.slug,
                title=h.text,
                description=first_sentence(_strip_heading_line(section_md)) or h.text,
                body_md=section_md,
            ))
        ch_artifact = ChapterArtifact(
            slug="" if is_index else slug,
            chapter=fm.get("chapter", ""),
            title=fm["title"],
            short_title=fm.get("short_title", fm["title"]),
            description=fm.get("description") or chapter_description(r["body_md"], fm["title"]),
            body_md=r["body_md"],
            sections=sections,
        )
        emit_section_md_mirrors(site, ch_artifact, chapter_md_dir)
        artifacts.append(ch_artifact)

    # Render the For-AI utility page if present
    for_ai_md = CONTENT / "de" / "for-ai.md"
    if for_ai_md.exists():
        text = for_ai_md.read_text(encoding="utf-8")
        fm, body = split_frontmatter(text)
        result = render_chapter(body, md, glossary)
        ai_template = env.get_template("for-ai.html.j2") if (TEMPLATES / "for-ai.html.j2").exists() else chapter_template
        html = ai_template.render(
            frontmatter=fm,
            body_html=result.html,
            headings=[h.__dict__ for h in result.headings],
            chapter_slug="for-ai",
            is_index=False,
            edit_url=_edit_url(meta["repository"], for_ai_md),
            prev_chapter=None,
            next_chapter=None,
        )
        ai_dir = out / "for-ai"
        ai_dir.mkdir(parents=True, exist_ok=True)
        (ai_dir / "index.html").write_text(html, encoding="utf-8")

    # Copy styles
    out_assets = out / "assets"
    out_assets.mkdir(parents=True, exist_ok=True)
    if STYLES.exists():
        (out_assets / "main.css").write_text(
            (STYLES / "main.css").read_text(encoding="utf-8"), encoding="utf-8"
        )
    if (ASSETS / "site.js").exists():
        (out_assets / "site.js").write_text(
            (ASSETS / "site.js").read_text(encoding="utf-8"), encoding="utf-8"
        )
    # Copy any other static assets recursively (fonts/, pdf/, og/)
    for sub in ("fonts", "pdf", "og"):
        src = ASSETS / sub
        if src.exists():
            shutil.copytree(src, out_assets / sub, dirs_exist_ok=True)

    # LLM artifacts
    emit_llms_txt(site, artifacts, out / "llms.txt")
    emit_llms_full_txt(site, artifacts, out / "llms-full.txt")

    # Sitemap + robots
    urls: list[str] = ["de/"]
    for a in artifacts:
        if a.slug:
            urls.append(f"de/{a.slug}/")
    if for_ai_md.exists():
        urls.append("for-ai/")
    emit_sitemap(site.base_url, site.base_path, urls, out / "sitemap.xml")
    emit_robots(site.base_url, site.base_path, out / "robots.txt")

    # CNAME passthrough if present
    cname = ROOT / "CNAME"
    if cname.exists():
        (out / "CNAME").write_text(cname.read_text(encoding="utf-8"), encoding="utf-8")

    # .nojekyll for GH Pages (no jekyll processing)
    (out / ".nojekyll").write_text("", encoding="utf-8")

    print(f"Built {len(artifacts)} chapters → {out}")
    print(f"  HTML pages: {sum(1 for _ in out.rglob('index.html'))}")
    print(f"  .md mirrors: {sum(1 for _ in out.rglob('*.md'))}")
    print(f"  llms.txt: {(out / 'llms.txt').exists()}")
    print(f"  llms-full.txt: {(out / 'llms-full.txt').exists()}")
    return 0


def _chapter_url(base_path: str, slug: str) -> str:
    if slug == "einleitung":
        return f"{base_path}de/"
    return f"{base_path}de/{slug}/"


def _neighbor(rendered: list[dict[str, Any]], current: dict[str, Any], offset: int, base_path: str) -> dict[str, Any] | None:
    idx = rendered.index(current) + offset
    if idx < 0 or idx >= len(rendered):
        return None
    n = rendered[idx]
    return {
        "title": n["fm"]["title"],
        "short_title": n["fm"].get("short_title", n["fm"]["title"]),
        "chapter": n["fm"].get("chapter", ""),
        "url": _chapter_url(base_path, n["fm"]["slug"]),
    }


def _edit_url(repo: dict[str, Any], path: Path) -> str:
    base = repo.get("url", "").rstrip("/")
    branch = repo.get("edit_branch", "main")
    rel = path.relative_to(ROOT).as_posix()
    if not base:
        return ""
    return f"{base}/edit/{branch}/{rel}"


def _redirect_html(base_path: str) -> str:
    target = f"{base_path}de/"
    return (
        "<!DOCTYPE html>\n"
        '<html lang="de">\n'
        "<head>\n"
        '  <meta charset="UTF-8">\n'
        f'  <meta http-equiv="refresh" content="0; url={target}">\n'
        f'  <link rel="canonical" href="{target}">\n'
        "  <title>Redirecting…</title>\n"
        "</head>\n"
        f'<body><p>→ <a href="{target}">{target}</a></p></body>\n'
        "</html>\n"
    )


def _strip_heading_line(md_text: str) -> str:
    """Drop the leading '## …' line from a section's Markdown."""
    lines = md_text.splitlines()
    if lines and lines[0].startswith("## "):
        lines = lines[1:]
    return "\n".join(lines)


if __name__ == "__main__":
    sys.exit(main())
