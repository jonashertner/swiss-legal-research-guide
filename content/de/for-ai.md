---
slug: for-ai
title: For AI / agents
short_title: For AI
description: "Endpoints and conventions for LLM and agent consumers of this guide."
---

This guide is intentionally machine-readable. The same content humans read at `/de/…` is exposed in raw Markdown and in summarised index form for use by language models, agents, and offline consumers.

## Endpoints

| URL | Type | Purpose |
| :--- | :--- | :--- |
| `/llms.txt` | text/plain | Index of every chapter and section with one-line descriptions and links. Follows the [`llms.txt` convention](https://llmstxt.org/). |
| `/llms-full.txt` | text/plain | The entire guide concatenated as one Markdown document — chapter dividers, no chrome. Designed for one-shot context-window inclusion. |
| `/de/<chapter>/<section>.md` | text/markdown | Raw Markdown for a single section (e.g. `/de/erlasse/suchen-von-erlassen.md`). Same content the chapter HTML page is rendered from, scoped to the named section. |
| `/sitemap.xml` | XML | Standard sitemap. |
| `/robots.txt` | text/plain | Permissive — explicitly allows `GPTBot`, `ClaudeBot`, `Claude-Web`, `PerplexityBot`, `Google-Extended`, `CCBot`, plus standard crawlers. |

## Conventions

- **Slugs** — section anchors are lowercase, German diaereses ASCII-folded (`ä→ae`, `ö→oe`, `ü→ue`, `ß→ss`), non-alphanumerics collapsed to hyphens. Stable across releases unless a section is renamed.
- **Section addressability** — every H2 in every chapter has a stable anchor and a corresponding `.md` mirror at the same path.
- **Footnotes** — preserved as standard Markdown footnote syntax (`[^N]`) in `.md` mirrors and `llms-full.txt`.
- **Cross-references** — the human-rendered HTML resolves `{{erlass:SR …}}` and `{{bge:…}}` to live URLs. The raw Markdown preserves the original tokens so a downstream agent can re-resolve against its own URL conventions if needed.

## How to fetch the whole guide

```
curl https://jonashertner.github.io/swiss-legal-research-guide/llms-full.txt
```

That single response contains the full text of every chapter, in Markdown, with chapter dividers. Suitable for direct ingestion into a model's context.

## How to fetch a single section

```
curl https://jonashertner.github.io/swiss-legal-research-guide/de/erlasse/suchen-von-erlassen.md
```

Each section's `.md` mirror begins with an HTML comment pointing back to its canonical HTML location.

## How to use this guide *and* the OpenCaseLaw database from Claude

Chapter [V — Connector](../de/opencaselaw-connector/) walks through adding OpenCaseLaw to Claude as an MCP connector. With both the connector and this guide accessible, an agent can read the guide for methodology and call OpenCaseLaw for primary sources.

## Licence

Content is published under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Attribution: *Kaspar Ehrenzeller, Daniel Brugger — Suchen — Lesen — Analysieren: Erlasse und Gerichtsentscheide*. The build code is published separately under MIT.
