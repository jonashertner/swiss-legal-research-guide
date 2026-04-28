# Authoring guide

Practical notes for editing the guide.

## The three Markdown idioms

In addition to standard CommonMark, three small extensions are recognised:

### 1. Footnotes

Standard Pandoc-style footnotes:

```markdown
This statement requires a citation.[^1]

[^1]: The citation goes here.
```

Footnotes auto-promote to right-margin sidenotes on wide screens; on narrow screens they collapse into a chapter-end "Anmerkungen" list.

### 2. Glossary terms — `[[TERM]]`

Wrap a Swiss term-of-art in double square brackets:

```markdown
Ein Erlass unterscheidet sich von der individuell-konkreten [[Verfügung]].
```

The build resolves `Verfügung` against `content/de/glossary.yml` and renders it as a dotted-underlined term with a dark hover-card containing the full name, definition, and authoritative-source link. Unknown terms render as plain dotted-underline (no card).

To add a new term, edit `content/de/glossary.yml`:

```yaml
NewTerm:
  full: "Long-form name"
  definition: "Plain-language explanation."
  source_url: "https://www.fedlex.admin.ch/..."
  source_label: "SR 173.110"
```

### 3. Cross-references — `{{kind:value}}`

Resolve to live links via patterns in `content/de/references.yml`:

```markdown
Vgl. Art. 27 BGG ({{erlass:SR 173.110}}).
Siehe {{bge:2C_166/2009|Hundeeuthanasie}}.
```

Defined kinds: `erlass`, `bge`, `bge_band`, `lexfind`, `url`. Add more by editing `references.yml`.

## File layout

```
content/
  de/
    00-einleitung.md         chapter I — order: 0, is_index: true → /de/
    10-erlasse.md            chapter II → /de/erlasse/
    20-gerichtsentscheide.md chapter III → /de/gerichtsentscheide/
    30-ki-konzepte.md        chapter IV → /de/ki-konzepte/
    40-opencaselaw-connector.md chapter V → /de/opencaselaw-connector/
    glossary.yml
    references.yml
  meta.yml                   version, authors, repo URL
```

## Frontmatter

Every chapter file starts with YAML frontmatter:

```yaml
---
chapter: II
slug: erlasse
title: Suchen, Lesen und Analysieren von Erlassen
short_title: Erlasse
order: 10
description: "One-line description used in /llms.txt."
---
```

## Section anchors

Every `## Heading` becomes a section with a stable anchor and a per-section `.md` mirror at `/de/<chapter-slug>/<section-slug>.md`. Don't change a section's heading text without thinking about external links.

Slugification: lowercase, German diaereses ASCII-folded (`ä→ae`, `ö→oe`, `ü→ue`, `ß→ss`), non-alphanumerics → single hyphen.

## Releasing a new version

1. Update `version` in `content/meta.yml` (e.g. `"April 2026"` → `"Mai 2026"`).
2. Update `last_updated`.
3. Tag the commit: `git tag v1.1 && git push --tags`.
4. The footer pulls the version from `meta.yml` automatically.

## Local preview

```
pip install -e ".[dev]"
python build.py
python -m http.server -d dist 8080
```

Open <http://localhost:8080>. Rebuild after every edit (no watch mode in v1).

## What changes still go through Jonas

For now, please cc Jonas on PRs that touch:

- `pyproject.toml` (dependencies)
- `templates/`, `styles/`, `assets/` (visual / structural changes)
- `lib/` and `build.py` (build pipeline)
- `.github/workflows/` (CI)

Content edits in `content/` can be merged directly.
