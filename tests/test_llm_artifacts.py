"""Tests for the LLM-artifact emitters."""

from pathlib import Path

from lib.llm_artifacts import (
    ChapterArtifact,
    SectionArtifact,
    SiteContext,
    chapter_description,
    emit_llms_full_txt,
    emit_llms_txt,
    emit_section_md_mirrors,
)


def make_site(tmp_path: Path) -> SiteContext:
    return SiteContext(
        base_url="https://example.ch",
        base_path="/guide/",
        title="Test Guide",
        subtitle="A test subtitle.",
        description="One-line description.",
        version="April 2026",
    )


def make_chapter() -> ChapterArtifact:
    sections = [
        SectionArtifact(
            slug="suchen",
            title="Suchen von Erlassen",
            description="Wo Erlasse publiziert sind.",
            body_md="## Suchen von Erlassen\n\nText here.",
        ),
        SectionArtifact(
            slug="aufbau",
            title="Aufbau von Erlassen",
            description="Typischer Aufbau.",
            body_md="## Aufbau von Erlassen\n\nMore text.",
        ),
    ]
    return ChapterArtifact(
        slug="erlasse",
        chapter="II",
        title="Erlasse",
        short_title="Erlasse",
        description="Chapter intro.",
        body_md="## Suchen von Erlassen\n\nText here.\n\n## Aufbau von Erlassen\n\nMore text.",
        sections=sections,
    )


def test_section_md_mirrors_have_canonical_link(tmp_path: Path):
    site = make_site(tmp_path)
    chapter = make_chapter()
    out_dir = tmp_path / "out"
    out_dir.mkdir()
    written = emit_section_md_mirrors(site, chapter, out_dir)
    assert len(written) == 2
    suchen = (out_dir / "suchen.md").read_text(encoding="utf-8")
    assert "Canonical HTML: https://example.ch/guide/de/erlasse/#suchen" in suchen
    assert "# II.suchen — Suchen von Erlassen" in suchen
    assert "Test Guide (April 2026)" in suchen


def test_llms_txt_lists_chapters_and_sections(tmp_path: Path):
    site = make_site(tmp_path)
    chapter = make_chapter()
    out = tmp_path / "llms.txt"
    emit_llms_txt(site, [chapter], out)
    content = out.read_text(encoding="utf-8")
    assert "# Test Guide" in content
    assert "> One-line description." in content
    assert "[II. Erlasse](https://example.ch/guide/de/erlasse/)" in content
    assert "(https://example.ch/guide/de/erlasse/suchen.md)" in content
    assert "https://example.ch/guide/llms-full.txt" in content


def test_llms_full_txt_contains_chapter_bodies(tmp_path: Path):
    site = make_site(tmp_path)
    chapter = make_chapter()
    out = tmp_path / "full.txt"
    emit_llms_full_txt(site, [chapter], out)
    content = out.read_text(encoding="utf-8")
    assert "# Test Guide" in content
    assert "## II. Erlasse" in content
    assert "Suchen von Erlassen" in content
    assert "Aufbau von Erlassen" in content
    assert "April 2026" in content


def test_chapter_description_pulls_first_sentence():
    body = "## Heading\n\nDies ist der Einleitungssatz. Weiterer Text."
    assert chapter_description(body, "fallback") == "Dies ist der Einleitungssatz."


def test_chapter_description_falls_back_when_empty():
    assert chapter_description("", "Fallback title") == "Fallback title"
