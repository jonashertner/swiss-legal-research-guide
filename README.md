# Suchen — Lesen — Analysieren

A practical guide to searching, reading, and analysing Swiss statutes (*Erlasse*) and court decisions (*Gerichtsentscheide*) — with and without AI.

By **Kaspar Ehrenzeller** and **Daniel Brugger** (Universität St. Gallen), version April 2026.

This repository is the source for the live document at <https://jonashertner.github.io/swiss-legal-research-guide/>.

## What this is

A static website rendered from Markdown source files into HTML, plus machine-readable artifacts (`/llms.txt`, `/llms-full.txt`, per-section `.md` mirrors) so language models and agents can use the guide as guidance when supporting Swiss legal research.

The site has no JavaScript framework, no analytics, and no tracking. It is hand-typeset for long-form reading, with Tufte-style sidenotes on wide screens, glossary hover-cards on Swiss terms of art, and a single deep-green accent borrowed from the original PDF cover.

Content is licensed **CC BY 4.0**; the build code is licensed **MIT** (see `LICENSE` and `LICENSE-CODE`).

## How to edit a chapter

1. Open the relevant `content/de/<n>-<slug>.md` file.
2. Edit the Markdown.
3. Commit and push, or open a pull request — the GitHub Action rebuilds and deploys automatically.

For a detailed walkthrough see [`AUTHORING.md`](./AUTHORING.md).

## How to build locally

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest                       # run the test suite
python build.py              # build → dist/
python -m http.server -d dist 8080  # serve locally at http://localhost:8080
```

The build expects Python 3.12 or later. Dependencies are pinned in `pyproject.toml` (`mistune`, `Jinja2`, `PyYAML`, `Pygments`, `beautifulsoup4`).

## Repository layout

```
content/
  de/                  authored Markdown chapters + glossary + references
  meta.yml             site metadata (version, authors, repo URL)
templates/             Jinja2 templates (base, chapter, index, partials)
styles/main.css        single hand-written stylesheet
assets/site.js         small enhancement layer (glossary card, scroll-spy)
build.py               build entrypoint (~250 lines)
lib/                   parser, llm-artifact emitter, sitemap helper
tests/                 pytest unit + smoke + snapshot tests
.github/workflows/     build-deploy + PR preview
```

## LLM-readability

The site is intentionally machine-readable. See [`/for-ai/`](https://jonashertner.github.io/swiss-legal-research-guide/for-ai/) for the full list of endpoints and conventions.

## Feedback

Comments, corrections, and contributions are welcome — open an issue or a pull request, or write to [kaspar.ehrenzeller@unisg.ch](mailto:kaspar.ehrenzeller@unisg.ch) / [daniel.brugger@unisg.ch](mailto:daniel.brugger@unisg.ch).
