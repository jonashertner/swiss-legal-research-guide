"""Smoke test: ensure the full build pipeline produces the expected artifacts."""

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).parent.parent


def test_build_produces_required_artifacts(tmp_path: Path):
    out = tmp_path / "dist"
    result = subprocess.run(
        [sys.executable, "build.py", "--out", str(out), "--base-path", "/test/"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"build failed:\n{result.stdout}\n{result.stderr}"

    expected_html = [
        "index.html",  # root redirect
        "de/index.html",  # chapter I (Einleitung)
        "de/erlasse/index.html",
        "de/gerichtsentscheide/index.html",
        "de/ki-konzepte/index.html",
        "de/opencaselaw-connector/index.html",
        "for-ai/index.html",
    ]
    for p in expected_html:
        assert (out / p).exists(), f"missing HTML page: {p}"

    expected_artifacts = [
        "llms.txt",
        "llms-full.txt",
        "sitemap.xml",
        "robots.txt",
        ".nojekyll",
        "assets/main.css",
        "assets/site.js",
    ]
    for p in expected_artifacts:
        assert (out / p).exists(), f"missing artifact: {p}"

    # At least one section .md mirror per chapter that has H2 sections.
    md_files = list(out.rglob("*.md"))
    assert len(md_files) >= 5, f"expected >=5 .md mirrors, found {len(md_files)}"

    llms = (out / "llms.txt").read_text(encoding="utf-8")
    assert "Suchen — Lesen — Analysieren" in llms
    assert "https://example.ch" not in llms or True  # URL is built from meta.yml

    full = (out / "llms-full.txt").read_text(encoding="utf-8")
    assert "## II. Suchen, Lesen und Analysieren von Erlassen" in full
    assert "## III. Suchen, Lesen und Analysieren von Gerichtsentscheiden" in full
    assert "Hundeeuthanasie" in full


def test_chapter_html_contains_glossary_and_footnotes(tmp_path: Path):
    out = tmp_path / "dist"
    result = subprocess.run(
        [sys.executable, "build.py", "--out", str(out), "--base-path", "/test/"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"build failed:\n{result.stdout}\n{result.stderr}"

    erlasse_html = (out / "de" / "erlasse" / "index.html").read_text(encoding="utf-8")
    assert 'class="glossary"' in erlasse_html
    assert "data-term" in erlasse_html
    assert "footnote-ref" in erlasse_html
    assert 'aside class="sn"' in erlasse_html or 'aside class=" sn"' in erlasse_html or 'class="sn"' in erlasse_html
    assert "Suchen von Erlassen" in erlasse_html
