// Suchen — Lesen — Analysieren · client behaviours
// (1) Glossary hover/focus-card with viewport-aware positioning;
// (2) Anchor link copy on click;
// (3) TOC scroll-spy;
// (4) Mobile drawer toggles (nav, TOC) with scrim + ESC + focus return.
// No framework; no innerHTML. ~5 KB minified.

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

    if (!def && !full) return;

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

    var open = function () {
      host.setAttribute("data-open", "true");
      // Reset overrides before measuring.
      card.style.left = "";
      card.style.right = "";
      card.style.top = "";
      card.style.bottom = "";
      card.style.transform = "";
      // Wait one frame so layout settles, then push back into viewport if needed.
      requestAnimationFrame(function () {
        var r = card.getBoundingClientRect();
        var pad = 8;
        var vw = window.innerWidth;
        var vh = window.innerHeight;
        if (r.right > vw - pad) {
          card.style.left = "auto";
          card.style.right = "0";
        }
        if (r.left < pad) {
          card.style.left = "0";
          card.style.right = "auto";
        }
        if (r.bottom > vh - pad) {
          // Flip above the term.
          card.style.top = "auto";
          card.style.bottom = "calc(100% + 6px)";
        }
      });
    };
    var close = function () { host.removeAttribute("data-open"); };
    host.addEventListener("mouseenter", open);
    host.addEventListener("mouseleave", close);
    host.addEventListener("focus", open);
    host.addEventListener("blur", close);
    host.addEventListener("click", function (e) {
      if (e.target && e.target.tagName === "A") return;
      if (host.hasAttribute("data-open")) close();
      else open();
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

  /* ─────── Mobile drawers (nav + TOC) ─────── */
  var body = document.body;
  var scrim = document.querySelector(".drawer-scrim");
  if (scrim) scrim.removeAttribute("hidden");

  var navToggle = document.querySelector(".nav-toggle");
  var tocToggle = document.querySelector(".toc-toggle");
  var nav = document.getElementById("primary-nav");
  var toc = document.getElementById("chapter-toc");

  function openDrawer(which) {
    closeDrawers(); // close the other one first
    body.classList.add(which + "-open");
    var btn = which === "nav" ? navToggle : tocToggle;
    if (btn) btn.setAttribute("aria-expanded", "true");
    var panel = which === "nav" ? nav : toc;
    if (panel) {
      var firstFocusable = panel.querySelector("a, button");
      if (firstFocusable) firstFocusable.focus({ preventScroll: true });
    }
  }
  function closeDrawers() {
    body.classList.remove("nav-open", "toc-open");
    if (navToggle) navToggle.setAttribute("aria-expanded", "false");
    if (tocToggle) tocToggle.setAttribute("aria-expanded", "false");
  }
  function isAnyOpen() {
    return body.classList.contains("nav-open") || body.classList.contains("toc-open");
  }

  if (navToggle && nav) {
    navToggle.addEventListener("click", function () {
      if (body.classList.contains("nav-open")) closeDrawers();
      else openDrawer("nav");
    });
  }
  if (tocToggle && toc) {
    tocToggle.addEventListener("click", function () {
      if (body.classList.contains("toc-open")) closeDrawers();
      else openDrawer("toc");
    });
  }

  if (scrim) scrim.addEventListener("click", closeDrawers);

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && isAnyOpen()) {
      closeDrawers();
      if (body.classList.contains("toc-open") && tocToggle) tocToggle.focus();
      if (body.classList.contains("nav-open") && navToggle) navToggle.focus();
    }
  });

  // Close TOC drawer when a link inside it is clicked (smooth UX)
  if (toc) {
    toc.addEventListener("click", function (e) {
      var a = e.target.closest("a");
      if (a && body.classList.contains("toc-open")) closeDrawers();
    });
  }

  // If viewport grows beyond the breakpoint, ensure drawers don't stay "open" in state
  var mq = window.matchMedia("(max-width: 900px)");
  function syncWithMq() {
    if (!mq.matches) closeDrawers();
  }
  if (mq.addEventListener) mq.addEventListener("change", syncWithMq);
  else if (mq.addListener) mq.addListener(syncWithMq);
})();
