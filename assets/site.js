// Suchen — Lesen — Analysieren · client behaviours
// (1) Glossary hover/focus-card; (2) anchor link copy; (3) TOC scroll-spy.
// No framework, no innerHTML — every node is built via createElement / textContent.

(function () {
  "use strict";

  function el(tag, className, text) {
    var node = document.createElement(tag);
    if (className) node.className = className;
    if (text != null) node.textContent = text;
    return node;
  }

  /* ─────── Glossary hover-card ─────── */
  document.querySelectorAll("span.glossary").forEach(function (host) {
    var term = host.getAttribute("data-term") || host.textContent.trim();
    var full = host.getAttribute("data-full") || "";
    var def = host.getAttribute("data-definition") || "";
    var srcUrl = host.getAttribute("data-source-url");
    var srcLabel = host.getAttribute("data-source-label") || srcUrl;

    if (!def && !full) return; // unknown term — leave dotted underline only

    var card = el("span", "glossary-card");
    card.setAttribute("role", "tooltip");
    card.appendChild(el("span", "term", term));
    if (full) card.appendChild(el("span", "full", full));
    if (def) card.appendChild(el("span", null, def));
    if (srcUrl) {
      var srcWrap = el("span", "src");
      var link = document.createElement("a");
      link.href = srcUrl;
      link.target = "_blank";
      link.rel = "noopener";
      link.textContent = (srcLabel || srcUrl) + " →";
      srcWrap.appendChild(link);
      card.appendChild(srcWrap);
    }
    host.appendChild(card);

    host.setAttribute("tabindex", "0");

    var open = function () { host.setAttribute("data-open", "true"); };
    var close = function () { host.removeAttribute("data-open"); };
    host.addEventListener("mouseenter", open);
    host.addEventListener("mouseleave", close);
    host.addEventListener("focus", open);
    host.addEventListener("blur", close);
    host.addEventListener("click", function (e) {
      if (e.target && e.target.tagName === "A") return;
      host.toggleAttribute("data-open");
    });
  });

  /* ─────── Anchor link → copy URL on click ─────── */
  document.querySelectorAll("h2 a.anchor, h3 a.anchor").forEach(function (a) {
    a.addEventListener("click", function (ev) {
      ev.preventDefault();
      var href = a.getAttribute("href");
      var url = location.origin + location.pathname + href;
      history.replaceState(null, "", href);
      if (navigator.clipboard) {
        navigator.clipboard.writeText(url).then(function () {
          var orig = a.textContent;
          a.textContent = "✓";
          setTimeout(function () { a.textContent = orig; }, 900);
        });
      }
    });
  });

  /* ─────── TOC scroll-spy ─────── */
  var tocLinks = Array.prototype.slice.call(document.querySelectorAll(".toc a[data-spy]"));
  if (tocLinks.length && "IntersectionObserver" in window) {
    var bySlug = {};
    tocLinks.forEach(function (a) { bySlug[a.getAttribute("data-spy")] = a; });
    var sections = Array.prototype.slice.call(
      document.querySelectorAll("main.reading h2[id]")
    );
    if (sections.length) {
      var active = null;
      var setActive = function (slug) {
        if (active === slug) return;
        if (active && bySlug[active]) bySlug[active].classList.remove("active");
        if (slug && bySlug[slug]) bySlug[slug].classList.add("active");
        active = slug;
      };
      var io = new IntersectionObserver(function (entries) {
        var visible = entries
          .filter(function (e) { return e.isIntersecting; })
          .sort(function (a, b) { return a.boundingClientRect.top - b.boundingClientRect.top; });
        if (visible.length) setActive(visible[0].target.id);
      }, { rootMargin: "-80px 0px -65% 0px", threshold: 0 });
      sections.forEach(function (s) { io.observe(s); });
      if (sections[0]) setActive(sections[0].id);
    }
  }
})();
