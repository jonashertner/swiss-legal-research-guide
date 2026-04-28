"""Unit tests for custom Markdown inline rules and helpers."""

from lib.parser import (
    first_sentence,
    make_renderer,
    slugify_de,
    split_frontmatter,
)


def test_slugify_de_handles_diaereses():
    assert slugify_de("Übergangsrecht") == "uebergangsrecht"
    assert slugify_de("Geständnis") == "gestaendnis"
    assert slugify_de("Schöne Grüsse") == "schoene-gruesse"


def test_slugify_de_strips_punctuation():
    assert slugify_de("Was sind Erlasse?") == "was-sind-erlasse"
    assert slugify_de("Art. 27 BGG (Auszug)") == "art-27-bgg-auszug"


def test_slugify_de_strips_leading_trailing_hyphens():
    assert slugify_de("  Hallo  ") == "hallo"
    assert slugify_de("---test---") == "test"


def test_split_frontmatter_extracts_yaml():
    text = "---\ntitle: Test\nslug: foo\n---\n\nBody content here."
    fm, body = split_frontmatter(text)
    assert fm == {"title": "Test", "slug": "foo"}
    assert body == "Body content here."


def test_split_frontmatter_returns_empty_when_absent():
    text = "Just a body, no frontmatter."
    fm, body = split_frontmatter(text)
    assert fm == {}
    assert body == text


def test_glossary_rule_renders_span():
    md = make_renderer({})
    out = md("Der [[BGE]] ist amtlich.")
    assert 'class="glossary"' in out
    assert 'data-term="BGE"' in out
    assert ">BGE</span>" in out


def test_xref_rule_resolves_known_kind():
    md = make_renderer({"erlass": "https://example.ch/sr/{value_encoded}"})
    out = md("Vgl. {{erlass:SR 173.110}}.")
    assert 'href="https://example.ch/sr/SR%20173.110"' in out
    assert "SR 173.110</a>" in out


def test_xref_rule_supports_label():
    md = make_renderer({"bge": "https://example.ch/{value_encoded}"})
    out = md("Vgl. {{bge:2C_166/2009|Hundeeuthanasie}}.")
    assert ">Hundeeuthanasie</a>" in out


def test_xref_rule_unresolved_kind_is_marked():
    md = make_renderer({})
    out = md("Vgl. {{unknown:foo}}.")
    assert "xref-unresolved" in out


def test_first_sentence_extracts_initial_period():
    text = "Erlasse sind generell-abstrakte Rechtsnormen. Sie sind publiziert."
    assert first_sentence(text) == "Erlasse sind generell-abstrakte Rechtsnormen."


def test_first_sentence_strips_footnote_markers():
    text = "Erlasse[^1] sind allgemein.[^2] Beispiel."
    assert first_sentence(text).startswith("Erlasse sind allgemein.")


def test_first_sentence_strips_glossary_and_xref_markers():
    text = "Der [[BGE]] ist publiziert. Vgl. {{erlass:SR 101}}."
    out = first_sentence(text)
    assert "Der BGE ist publiziert." == out
