# Swiss Legal Research Guide — Site Design Spec

**Working title:** *Suchen — Lesen — Analysieren: Erlasse und Gerichtsentscheide. Juristisches Handwerk mit und ohne KI.*
**Authors of the text:** Kaspar Ehrenzeller, Daniel Brugger (HSG)
**Site implementer:** Jonas Hertner
**Source:** PDF (39 pp., A4), version April 2026
**Spec date:** 2026-04-28
**Status:** Draft, pending author approval

---

## 1. Goal

Publish the Ehrenzeller/Brugger guide to Swiss legal research as a *living* web document at a dedicated URL. The site must (a) match the source text's intellectual seriousness with corresponding typographic and layout excellence in a Swiss-minimalist register, (b) be navigable as a long-form linear read *and* as a deep-linkable reference, *and* (c) be first-class machine-readable so that LLMs can use it as guidance when supporting Swiss legal research.

This spec describes v1 — the launch of the document as it exists today (April 2026), with infrastructure ready for ongoing author revisions and (eventually) French and Italian translations.

## 2. Decisions captured during brainstorming

| Topic | Decision |
| --- | --- |
| Hosting | GitHub Pages, fresh dedicated repository |
| Scope | Single document, forever — the site *is* the guide |
| Languages | DE at launch; URL/i18n primitives ready for FR / IT |
| Authoring | Pure GitHub workflow — Markdown source, "Edit on GitHub" links, PR previews |
| Tech stack | Hand-crafted static, ~250-line Python build (mistune + Jinja2 + PyYAML + pygments) — no JS framework |
| LLM access | Semantic HTML + `/llms.txt` + per-section `.md` mirrors + `/llms-full.txt` |
| Audience | Linear readers, reference seekers, cross-border outsiders, and developers/LLM-instructors — all served, no priority |
| Typography | Source Serif 4 (body) + JetBrains Mono (labels, navigation, footnotes); single accent in the deep forest green from the PDF cover |
| Layout | Three-column reading: persistent left TOC ▏ centered serif body ▏ right-margin Tufte sidenotes; collapses gracefully on narrow viewports |
| Interactive elements | Hover-card glossary, click-to-deep-link section anchors, hover-to-reveal `¶` anchors |
| Search | None at launch — `⌘F` covers a chapter-per-page document |
| Analytics | None at launch |
| Dark mode | None in v1 — single warm-paper theme |
| License | CC BY 4.0 for content, MIT for code (separate `LICENSE` files) |

## 3. Information architecture

Five HTML pages, one per chapter. Subsections live as anchors. For every section anchor the build also emits a standalone Markdown mirror, giving LLMs and bookmarkers section-level addressability without splitting the HTML reading flow.

| URL | Source | Chapter |
| --- | --- | --- |
| `/` | redirect → `/de/` | — |
| `/de/` | `00-einleitung.md` | I. Einleitung |
| `/de/erlasse/` | `10-erlasse.md` | II. Erlasse |
| `/de/gerichtsentscheide/` | `20-gerichtsentscheide.md` | III. Gerichtsentscheide |
| `/de/ki-konzepte/` | `30-ki-konzepte.md` | IV. KI-Konzepte |
| `/de/opencaselaw-connector/` | `40-opencaselaw-connector.md` | V. Anhang: OpenCaseLaw-Connector |

Section anchors are kebab-case slugs of headings (e.g., `#suchen-von-erlassen`, `#fallbeispiel-hundeeuthanasie`). Per-section Markdown mirrors live at the same path with `.md` suffix (`/de/erlasse/suchen.md`).

`/de/` is first-class and live; `/fr/` and `/it/` are reserved. The language switcher in the masthead shows DE active and FR / IT visibly disabled until those translations exist.

## 4. Content model

```
content/
  de/
    00-einleitung.md
    10-erlasse.md
    20-gerichtsentscheide.md
    30-ki-konzepte.md
    40-opencaselaw-connector.md
    glossary.yml
    references.yml
  meta.yml
assets/
  fonts/        # self-hosted Source Serif 4 + JetBrains Mono subsets
  pdf/          # downloadable PDF version of the current text
  og/           # social/OG share image
```

**Frontmatter per chapter file:**

```yaml
---
chapter: II
slug: erlasse
title: Suchen, Lesen und Analysieren von Erlassen
short_title: Erlasse
order: 20
---
```

**`meta.yml`** holds: site title, version (e.g., `April 2026`), authors, contact, license, repository URL.

**Three Markdown conventions added on top of CommonMark:**

1. **Footnotes** — standard `[^1]` syntax (mistune footnote plugin).
2. **Glossary terms** — `[[BGE]]` resolves against `glossary.yml` to a `<span class="glossary">` with hover-card containing definition + authoritative-source link. Authors tag once; the build does the rest.
3. **Cross-references** — `{{erlass:SR 173.110}}` and `{{bge:2C_166/2009}}` resolve to live links via patterns in `references.yml`. Base-URL changes are one edit.

Raw Markdown remains readable; rendered HTML gets the affordances. Authors learn three small idioms.

## 5. Build pipeline

**Tech:** Python 3.12+, `mistune`, `Jinja2`, `PyYAML`, `pygments`. Locked via `pyproject.toml`. Single command: `python build.py`. Watch mode for authoring: `python build.py --serve` (livereload on `content/` change).

**Steps (executed in order):**

1. **Discover** — glob `content/de/*.md`, load `meta.yml`, `glossary.yml`, `references.yml`. Build a page registry.
2. **Parse** — split frontmatter from body; run custom inline transforms (`[[…]]` → glossary span; `{{…}}` → resolved link); convert Markdown → HTML via mistune with footnotes plugin.
3. **Anchor** — walk the HTML tree, slugify every `h2`/`h3`, attach stable `id` and a hover-revealed `¶` self-link.
4. **Render** — pass through Jinja: chapter HTML, TOC built from headings, prev/next links, "Edit on GitHub" link, glossary script tag, sidenote markup.
5. **LLM artifacts** — `.md` per section, `/llms.txt`, `/llms-full.txt` (formats below).
6. **Sitemap & robots** — `sitemap.xml` from page registry; `robots.txt` allows all major AI crawlers explicitly (`GPTBot`, `ClaudeBot`, `PerplexityBot`, `Google-Extended`).
7. **Copy** — `assets/` (fonts, downloadable PDF, OG image) → `dist/`.

Output → `dist/`. CI deploys `dist/` to GitHub Pages.

## 6. Visual identity

**Type system (chosen during brainstorm — Direction C, "Mono Eyebrow"):**

- **Body:** Source Serif 4 (variable, optical sizing on), 17.5 px / 1.62 line-height, ~60ch measure. Italic for emphasis and *Frage*-headings.
- **Display (chapter titles, section headings):** Source Serif 4 at 38 px (chapter) / 22 px (section), 600 weight, slight negative tracking.
- **Labels, eyebrows, navigation, sidenote text, footnote markers:** JetBrains Mono.
- **Section markers:** mono `§ 1`, `§ 2` echoing the legal-paragraph idiom.

**Color:**

- Paper: `#FAFAF7` (warm off-white)
- Ink: `#1A1A1A` (near-black)
- Rule / borders: `#D8D6CF`, `#E8E6DF` for soft variants
- Muted text (sidenotes, metadata): `#6B6B6B`
- Accent: deep forest green from the PDF cover, `#08612D`. Used for: chapter eyebrows, footnote markers, glossary dotted underlines, section markers, the masthead version pill, footer column accents. Single accent — the only color besides the neutrals.

**Layout (three-column reading on ≥ 1280 px):**

- **Left column (240 px):** persistent chapter TOC. Mono. Scroll-spy highlights the active section with a thin green leader line. A divider separates the active chapter's sections from the document-level TOC.
- **Center column (fluid, ~60ch):** reading body.
- **Right column (~280 px):** Tufte-style sidenote column. Footnotes auto-promoted, vertically aligned to their reference in the body. Each sidenote starts with a green mono-set numeric marker.

**Responsive behaviour:**

- ≥ 1280 px → full three-column.
- 900–1279 px → two-column. Sidenotes collapse to inline expandable footnotes; left TOC stays. Body widens to ~64ch.
- < 900 px → single column. TOC becomes a slide-in drawer summoned by a small mono "§" button. Sidenotes become tap-to-expand inline popovers.

**Homepage variation:** chapter I opens with a *frontispiece* — oversized title and subtitle, authors, version, and the deep-green PDF-cover color used as a single thick rule above the title. Then chapter I prose begins. The homepage is not a separate landing page; it *is* the document, opening at page one.

**Interactive elements (all v1, no JS framework):**

- **Glossary hover-card** — dotted-underlined term opens a dark popover with abbreviation, full-name definition, and authoritative-source link. Touch: tap to open, tap again to close. Driven by `glossary.yml`.
- **Section anchor `¶`** — appears on hover next to every section heading; click copies a deep-link to the clipboard.
- **Footnote sidenote sync** — hovering a footnote reference in the body subtly highlights the corresponding sidenote.
- **"Edit on GitHub" link** — bottom of every chapter, deep-links to the source `.md` file on the appropriate branch.

Total client-side JavaScript budget: < 5 KB minified, no framework, no third-party scripts. Authored as a single ES module in `assets/site.js`.

## 7. LLM artifacts

The site teaches AI-assisted legal research; its own LLM-readability is therefore a feature, not an afterthought.

**`/llms.txt`** — root-level plain text, follows the [`llms.txt` convention](https://llmstxt.org/). Short index linking to each chapter and (with `.md` paths) each section, with one-line descriptions. Generated from chapter frontmatter and the first paragraph of each section.

**`/llms-full.txt`** — entire guide concatenated as one Markdown document, chapters in order, no frontmatter clutter, version line at top, last-updated date. Generated from the same source on every build, so it cannot drift.

**`/de/<chapter>/<section>.md`** — for each H2 in each chapter, a small Markdown file containing just that section's body, prefixed with a one-line header pointing back to the canonical HTML URL.

**`/sitemap.xml`** — every HTML URL.

**`/robots.txt`** — explicit allow for `GPTBot`, `ClaudeBot`, `PerplexityBot`, `Google-Extended`, plus standard search crawlers. Points to sitemap.

**Surfacing:** the masthead carries a "For AI / devs" link to a small `/for-ai/` page that documents the LLM endpoints, the `.md`-mirror convention, and the connector setup (chapter V). The footer has a dedicated "FOR AI / AGENTS" column listing the four artifacts as direct links.

## 8. Repository, hosting, deploy

**Repository:** fresh, dedicated, public. Working name `swiss-legal-research-guide` (final name an open question — see § 13). Owner: open question (Jonas, the authors, or a new shared org).

**Repository layout:**

```
content/                      # authored Markdown + YAML
assets/                       # fonts, PDF, OG image
templates/                    # Jinja2: base, chapter, partials
styles/main.css               # one stylesheet, hand-tuned
build.py                      # ~250 lines, single entrypoint
lib/parser.py                 # mistune + custom inline rules
lib/llm_artifacts.py          # llms.txt, llms-full.txt, .md mirrors
lib/sitemap.py
tests/                        # pytest: parser, llm artifacts, build smoke
.github/workflows/
  build-deploy.yml
  pr-preview.yml
pyproject.toml
AUTHORING.md                  # one-page guide for the authors
README.md
LICENSE                       # CC BY 4.0 (content) — see § 11
LICENSE-CODE                  # MIT (build code)
```

**Branching:** `main` is production. Authors edit on feature branches and open PRs. Each PR gets a preview deploy. Merge to `main` rebuilds and replaces production. No staging branch.

**GitHub Actions — two workflows:**

1. **`build-deploy.yml`** — on push to `main`: install Python via `uv`, run `pytest`, run `python build.py`, upload `dist/` via `actions/deploy-pages`.
2. **`pr-preview.yml`** — on PR open/sync: same build, deploy to a preview path (e.g., `<owner>.github.io/<repo>/pr-<n>/`). Comment back on the PR with the preview URL. Tear down on PR close.

Both ~30 lines of YAML. No third-party CI vendors.

**Domain strategy:**

- **Phase 0 (immediately on launch):** `<owner>.github.io/<repo>/` — works the moment the workflow runs.
- **Phase 1 (when domain is chosen):** custom domain via `CNAME` file in repo root. Apex with `www.` redirecting to apex. HTTPS via GitHub Pages' auto-provisioned cert. Domain selection is an open question — see § 13.

## 9. Authoring workflow

Ehrenzeller and Brugger edit Markdown directly on GitHub — either via the web editor (zero-install) or via local clone. Every chapter page links to its source `.md` on the current branch ("Edit on GitHub"). PRs trigger preview deploys so authors see changes before merging.

`AUTHORING.md` (top of repo) is a one-page guide with: the three Markdown conventions, where the glossary lives, how to add a new term, how the version field is updated, and how to roll a release tag.

## 10. Testing

- **Unit tests** — parser custom-rule resolution (glossary, cross-refs), LLM-artifact generation. Pure Python, no I/O.
- **Snapshot tests** — one rendered chapter, asserts the HTML output matches a checked-in golden file. Catches accidental template breakage. Easy to refresh when intentional design changes happen.
- **Smoke test** — `python build.py` exits 0, produces `llms.txt`, `llms-full.txt`, and ≥ 1 section `.md` mirror. Runs in CI.

`pytest` invoked in `build-deploy.yml` before the build runs.

## 11. License

- **Content** (the prose, the glossary, the chapter Markdown): **CC BY 4.0**. Footer links to the canonical license; `LICENSE` in repo root contains the canonical text. Attribution must include both authors' names and a link to the canonical site.
- **Code** (build script, templates, CSS, JS module): **MIT**, in `LICENSE-CODE`. Decoupling permits forking the build infrastructure without inheriting CC BY obligations on the code.
- *Confirm with authors before launch.*

## 12. Out of scope (v1)

- French / Italian translations (URL structure ready; content not produced)
- Client-side full-text search (deferred — `⌘F` covers chapter-per-page)
- Comments / discussions
- Newsletter / email signup
- Cookie banner (no tracking, no banner needed)
- Dark-mode toggle (single warm-paper theme; `prefers-color-scheme: dark` deferred to v1.1)
- Auto-generated PDF from the Markdown source (we ship the original PDF in `assets/pdf/` for v1)
- Analytics
- Author photos / author bios pages

## 13. Open questions to resolve before launch

1. **Domain name** — which `.ch` domain (or other TLD) the authors register. Candidates discussed: `suchen-lesen-analysieren.ch`, `legalresearch.ch`, `juristisches-handwerk.ch`, others. Owner: Jonas + authors.
2. **Repository name and owner** — final repo name (working title `swiss-legal-research-guide`); owner: Jonas, an author, or a new shared GitHub org.
3. **Author contact** — keep the two `@unisg.ch` addresses from the PDF, or set up a shared `kontakt@<domain>` mailbox?
4. **Glossary scope at launch** — recommended ~30 terms (those appearing in this document). Confirm with authors.
5. **PDF download** — v1 ships the existing manually-prepared PDF. v1.1 question: auto-generate via WeasyPrint from the Markdown source so the PDF stays in lockstep with the site.

## 14. Implementation phases

**Phase 1 — MVP launch (the work this spec defines):**

1. Initialise repo, scaffold directory layout.
2. Build pipeline (parser, templates, LLM-artifact emitter, sitemap).
3. Typography + layout CSS + JS module.
4. Convert PDF chapters I–V to Markdown, attach frontmatter, populate glossary and references.
5. Wire GitHub Actions (build-deploy + pr-preview).
6. Deploy on `<owner>.github.io/<repo>/`.
7. Author review + revisions via PR cycle.
8. Custom domain CNAME once registered.

**Phase 1.1 — post-launch (deferred, not blocking):**

- `prefers-color-scheme: dark` variant
- Auto-generated PDF
- French translation infrastructure activation (when authors are ready)
- Optional Plausible analytics if the authors want readership data

## 15. Success criteria

- All 5 chapters render at the URLs in § 3, faithfully reproducing the PDF's content and citation apparatus.
- `/llms.txt`, `/llms-full.txt`, and per-section `.md` mirrors exist and match the source.
- A reader on a 4G connection sees the homepage in < 1 s (no JS framework, no fonts blocking).
- The authors can edit a chapter on GitHub, open a PR, see the preview deploy, and merge — without involving Jonas.
- Lighthouse: Performance ≥ 95, Accessibility ≥ 95, Best Practices ≥ 95, SEO ≥ 95.
- A Claude or other LLM, given the URL of the site, can fetch `/llms.txt`, follow it to the relevant section, fetch the `.md` mirror, and answer a Swiss-legal-research question grounded in the guide.
- The site, in the authors' judgement, looks like *theirs* — typographically distinctive, intellectually serious, "Swiss" in the disciplined-design sense rather than the cliché sense.
