"""PDF generation via WeasyPrint.

Renders a single concatenated print document — cover, colophon, TOC, all
chapters with running headers and footnotes-at-page-bottom — using
print-specific CSS (@page rules, CSS counters, target-counter for TOC
page numbers).

WeasyPrint is an optional dependency. The build script calls
`render_pdf(...)` only after checking `weasyprint_available()`.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from bs4 import BeautifulSoup, NavigableString, Tag


def weasyprint_available() -> bool:
    try:
        import weasyprint  # noqa: F401
        return True
    except Exception:
        return False


def convert_footnotes_for_print(html: str) -> str:
    """Convert mistune's footnote layout into inline `.fn-content` spans.

    Web layout: <sup class="footnote-ref"><a href="#fn-N">N</a></sup> in
    body, plus a <section class="footnotes"><ol><li id="fn-N">...</li></ol></section>
    at chapter end.

    Print layout: each <sup class="footnote-ref"> is replaced in place by an
    inline <span class="fn"><span class="fn-content">…</span></span> containing
    the body of the matching footnote (without its backref). The chapter-end
    footnote section is removed, since CSS `float: footnote` will lay them
    out at the bottom of each page automatically.

    Also strips the post-processed sidenote `<aside class="sn">` clones —
    those are a web-only presentation. Footnote rendering on print uses
    the canonical mechanism, not the cloned sidenotes.
    """
    soup = BeautifulSoup(html, "html.parser")

    # Drop the web-only sidenote clones
    for aside in soup.find_all("aside", class_="sn"):
        aside.decompose()

    fn_section = soup.find("section", class_="footnotes")
    if fn_section is None:
        return str(soup)

    # Build a map: id → list of inline-only nodes (paragraphs unwrapped, backrefs stripped).
    items: dict[str, list] = {}
    for li in fn_section.find_all("li"):
        fn_id = li.get("id", "")
        # Drop backref anchors (mistune emits a class="footnote" but also class="footnote-backref")
        for back in li.find_all("a"):
            classes = back.get("class") or []
            if any("footnote" in c for c in classes):
                back.decompose()
        # Unwrap any block-level descendants (p, div) so the resulting nodes are inline-safe.
        # If the <li> contains a single <p>, replace it with that <p>'s children.
        flattened: list = []
        for child in list(li.children):
            if isinstance(child, Tag) and child.name in ("p", "div"):
                for grandchild in list(child.children):
                    flattened.append(grandchild)
                # Insert a space if there are multiple paragraphs to keep them readable inline
                if li.find_all(["p", "div"]).index(child) < len(li.find_all(["p", "div"])) - 1:
                    flattened.append(NavigableString(" "))
            else:
                flattened.append(child)
        items[fn_id] = flattened

    for sup in soup.find_all("sup", class_="footnote-ref"):
        a = sup.find("a")
        if not a:
            continue
        href = a.get("href", "")
        if not href.startswith("#"):
            continue
        fn_id = href[1:]
        contents = items.get(fn_id)
        if contents is None:
            continue
        # `.fn` is the float-footnote element; `.fn-content` is just for styling hooks.
        wrap = soup.new_tag("span", attrs={"class": "fn"})
        for c in contents:
            wrap.append(_clone_node(c, soup))
        sup.replace_with(wrap)

    fn_section.decompose()
    return str(soup)


def _clone_node(node, soup: BeautifulSoup):
    """Deep-clone a BS4 node into a fresh structure attached to `soup`."""
    if isinstance(node, Tag):
        new = soup.new_tag(node.name, attrs=dict(node.attrs))
        for child in node.children:
            new.append(_clone_node(child, soup))
        return new
    return BeautifulSoup(str(node), "html.parser")


def strip_section_numbers_and_anchors(html: str) -> str:
    """For print, drop the `¶` anchor links and tighten the `§ N` markers."""
    soup = BeautifulSoup(html, "html.parser")
    for a in soup.find_all("a", class_="anchor"):
        a.decompose()
    return str(soup)


def render_pdf(
    print_html: str,
    base_dir: Path,
    out_path: Path,
    extra_stylesheets: list[Path] | None = None,
) -> None:
    """Render the print document HTML to a PDF at out_path.

    `base_dir` is used as the WeasyPrint base URL so relative paths to fonts
    and stylesheets resolve.
    """
    from weasyprint import CSS, HTML

    base_url = base_dir.as_uri() + "/"
    css_files = [CSS(filename=str(p)) for p in (extra_stylesheets or [])]
    HTML(string=print_html, base_url=base_url).write_pdf(
        target=str(out_path),
        stylesheets=css_files,
        optimize_images=True,
        presentational_hints=False,
    )


def annotate_tables_for_print(html: str) -> str:
    """Add `single-col` class to tables with one column for distinct print styling."""
    soup = BeautifulSoup(html, "html.parser")
    for table in soup.find_all("table"):
        first_row = table.find("tr")
        if first_row is None:
            continue
        cells = first_row.find_all(["th", "td"])
        if len(cells) == 1:
            classes = table.get("class") or []
            classes.append("single-col")
            table["class"] = classes
    return str(soup)


def post_process_for_print(chapter_html: str) -> str:
    """Apply transformations needed for the print layout."""
    html = convert_footnotes_for_print(chapter_html)
    html = strip_section_numbers_and_anchors(html)
    html = annotate_tables_for_print(html)
    return html
