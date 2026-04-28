"""Markdown parsing with custom inline rules for the Swiss legal research guide."""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field
from typing import Any

import mistune
from bs4 import BeautifulSoup, NavigableString, Tag


_GLOSSARY_RE = re.compile(r"\[\[([A-Za-zÄÖÜäöüß0-9 \-/]+)\]\]")
_REF_RE = re.compile(r"\{\{([a-z]+):([^{}|]+?)(?:\|([^{}]+?))?\}\}")


def slugify_de(text: str) -> str:
    """Slugify with German-aware folding (ä→ae, ö→oe, ü→ue, ß→ss)."""
    text = text.strip().lower()
    text = (
        text.replace("ä", "ae")
        .replace("ö", "oe")
        .replace("ü", "ue")
        .replace("ß", "ss")
    )
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def _glossary_inline_rule(md):
    """Register [[term]] and [[term|label]] inline parser."""
    GLOSS_PATTERN = r"\[\[(?P<gloss>[^\[\]\|]+?)(?:\|(?P<gloss_label>[^\[\]]+?))?\]\]"

    def parse_glossary(inline, m, state):
        term = m.group("gloss").strip()
        label = (m.group("gloss_label") or "").strip()
        state.append_token({
            "type": "glossary_term",
            "attrs": {"term": term, "label": label or term},
        })
        return m.end()

    def render_glossary(renderer, term=None, label=None):
        display = label or term
        return (
            f'<span class="glossary" data-term="{mistune.escape(term)}">'
            f'{mistune.escape(display)}</span>'
        )

    md.inline.register("glossary", GLOSS_PATTERN, parse_glossary, before="link")
    if md.renderer:
        md.renderer.register("glossary_term", render_glossary)


def _ref_inline_rule(md, references: dict[str, str]):
    """Register {{kind:value}} or {{kind:value|label}} inline parser."""
    REF_PATTERN = r"\{\{(?P<xref_kind>[a-z]+):(?P<xref_val>[^{}|]+?)(?:\|(?P<xref_label>[^{}]+?))?\}\}"

    def parse_ref(inline, m, state):
        kind = m.group("xref_kind")
        val = m.group("xref_val").strip()
        label = (m.group("xref_label") or "").strip()
        state.append_token({
            "type": "xref",
            "attrs": {"kind": kind, "value": val, "label": label},
        })
        return m.end()

    def render_ref(renderer, kind=None, value=None, label=None):
        url = _resolve_ref(kind, value, references)
        text = label or value
        if url:
            return (
                f'<a class="xref xref-{mistune.escape(kind)}" '
                f'href="{mistune.escape(url)}" '
                f'target="_blank" rel="noopener noreferrer">{mistune.escape(text)}</a>'
            )
        return f'<span class="xref xref-unresolved">{mistune.escape(text)}</span>'

    md.inline.register("xref", REF_PATTERN, parse_ref, before="link")
    if md.renderer:
        md.renderer.register("xref", render_ref)


def _resolve_ref(kind: str, value: str, references: dict[str, str]) -> str | None:
    """Resolve a {{kind:value}} reference using patterns from references.yml."""
    pattern = references.get(kind)
    if not pattern:
        return None
    safe_value = value.strip()
    encoded = safe_value.replace(" ", "%20")
    return pattern.replace("{value}", safe_value).replace("{value_encoded}", encoded)


@dataclass
class ChapterDoc:
    slug: str
    chapter: str
    title: str
    short_title: str
    order: int
    body_md: str
    frontmatter: dict[str, Any] = field(default_factory=dict)


def split_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    """Split YAML frontmatter from a Markdown document."""
    import yaml

    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    fm = yaml.safe_load(parts[1]) or {}
    body = parts[2].lstrip("\n")
    return fm, body


def make_renderer(references: dict[str, str]):
    """Construct a configured mistune Markdown renderer."""
    md = mistune.create_markdown(
        renderer="html",
        plugins=["footnotes", "table", "strikethrough", "url"],
        escape=False,
    )
    _glossary_inline_rule(md)
    _ref_inline_rule(md, references)
    return md


@dataclass
class Heading:
    level: int
    slug: str
    text: str
    section_num: int | None  # for top-level "§ 1", "§ 2"


@dataclass
class RenderedChapter:
    html: str
    headings: list[Heading]
    raw_body_md: str
    section_md: dict[str, str]


def render_chapter(
    body_md: str,
    md: mistune.Markdown,
    glossary: dict[str, dict[str, Any]],
) -> RenderedChapter:
    """Render a chapter to HTML and return structural data."""
    section_md = _split_sections(body_md)
    raw_html = md(body_md)
    soup = BeautifulSoup(raw_html, "html.parser")

    headings: list[Heading] = []
    section_counter = 0
    for h in soup.find_all(["h2", "h3", "h4"]):
        text = h.get_text(strip=True)
        slug = slugify_de(text)
        h["id"] = slug
        if h.name == "h2":
            section_counter += 1
            section_marker = soup.new_tag("span", attrs={"class": "section-num"})
            section_marker.string = f"§ {section_counter}"
            h.insert(0, section_marker)
            headings.append(Heading(level=2, slug=slug, text=text, section_num=section_counter))
        else:
            headings.append(Heading(level=int(h.name[1]), slug=slug, text=text, section_num=None))
        anchor = soup.new_tag("a", attrs={"class": "anchor", "href": f"#{slug}", "aria-label": "Direktlink"})
        anchor.string = "¶"
        h.append(anchor)

    _enrich_glossary_titles(soup, glossary)
    _promote_footnotes_to_sidenotes(soup)

    return RenderedChapter(
        html=str(soup),
        headings=headings,
        raw_body_md=body_md,
        section_md=section_md,
    )


def _enrich_glossary_titles(soup: BeautifulSoup, glossary: dict[str, dict[str, Any]]) -> None:
    """Attach glossary metadata as data-* attrs for the JS hover-card."""
    for span in soup.find_all("span", class_="glossary"):
        term = span.get("data-term", "")
        entry = glossary.get(term) or glossary.get(term.upper())
        if not entry:
            continue
        span["data-full"] = entry.get("full", "")
        span["data-definition"] = entry.get("definition", "")
        if "source_url" in entry:
            span["data-source-url"] = entry["source_url"]
        if "source_label" in entry:
            span["data-source-label"] = entry["source_label"]


def _promote_footnotes_to_sidenotes(soup: BeautifulSoup) -> None:
    """Clone footnote content next to its in-body reference for Tufte-style sidenotes.

    The mistune footnotes plugin produces:
      <sup id="fnref-N"><a href="#fn-N">N</a></sup>           in the body
      <section class="footnotes"><ol><li id="fn-N">…</li></ol></section>  at the end

    We keep both — the bottom list remains as the canonical source — and add an
    <aside class="sn" data-fn="N">…</aside> as a sibling immediately after the
    block element that contains the reference.
    """
    footnote_section = soup.find("section", class_="footnotes")
    if not footnote_section:
        return
    items = {li.get("id", ""): li for li in footnote_section.find_all("li")}
    for sup in soup.find_all("sup", class_="footnote-ref"):
        a = sup.find("a")
        if not a:
            continue
        href = a.get("href", "")
        if not href.startswith("#"):
            continue
        fn_id = href[1:]
        li = items.get(fn_id)
        if not li:
            continue
        block = sup.find_parent(["p", "li", "blockquote", "div"])
        if not block:
            continue
        aside = soup.new_tag("aside", attrs={"class": "sn", "data-fn": fn_id})
        num_match = re.search(r"(\d+)$", fn_id)
        num = num_match.group(1) if num_match else fn_id
        num_span = soup.new_tag("span", attrs={"class": "sn-num"})
        num_span.string = f"[{num}]"
        aside.append(num_span)
        aside.append(NavigableString(" "))
        for child in li.contents:
            if isinstance(child, Tag) and child.name == "a" and "footnote-backref" in (child.get("class") or []):
                continue
            if isinstance(child, Tag):
                aside.append(_clone_for_sidenote(child))
            else:
                aside.append(NavigableString(str(child)))
        block.insert_after(aside)


def _clone_for_sidenote(tag: Tag) -> Tag:
    """Deep-clone a tag, stripping footnote backref links."""
    new_soup = BeautifulSoup(str(tag), "html.parser")
    for back in new_soup.find_all("a", class_="footnote-backref"):
        back.decompose()
    return new_soup.contents[0] if new_soup.contents else NavigableString("")


def _split_sections(body_md: str) -> dict[str, str]:
    """Split a chapter body into per-H2 Markdown chunks keyed by slug."""
    sections: dict[str, str] = {}
    lines = body_md.splitlines(keepends=False)
    current_slug: str | None = None
    current_buf: list[str] = []
    for line in lines:
        if line.startswith("## "):
            if current_slug is not None:
                sections[current_slug] = "\n".join(current_buf).strip()
            heading = line[3:].strip()
            current_slug = slugify_de(heading)
            current_buf = [line]
        else:
            if current_slug is not None:
                current_buf.append(line)
    if current_slug is not None:
        sections[current_slug] = "\n".join(current_buf).strip()
    return sections


def first_sentence(text: str, max_chars: int = 220) -> str:
    """Extract a one-line description from the start of a Markdown block."""
    cleaned = re.sub(r"\[\^\d+\]", "", text)
    # [[term|label]] → label; [[term]] → term
    cleaned = re.sub(r"\[\[([^\[\]\|]+)\|([^\[\]]+)\]\]", r"\2", cleaned)
    cleaned = re.sub(r"\[\[([^\]]+)\]\]", r"\1", cleaned)
    cleaned = re.sub(r"\{\{[a-z]+:([^{}|]+?)(?:\|([^{}]+?))?\}\}", lambda mm: mm.group(2) or mm.group(1), cleaned)
    cleaned = re.sub(r"^#+\s+.*$", "", cleaned, flags=re.MULTILINE)
    cleaned = re.sub(r"[*_`]", "", cleaned)
    cleaned = " ".join(cleaned.split())
    if not cleaned:
        return ""
    match = re.search(r"^(.{20,}?[\.!?])\s", cleaned)
    sentence = match.group(1) if match else cleaned[:max_chars].rstrip(" ,;")
    if len(sentence) > max_chars:
        sentence = sentence[: max_chars - 1].rstrip() + "…"
    return sentence
