/* zoe-wang.com — small progressive enhancements. Everything works without JS. */
(function () {
  'use strict';
  var root = document.documentElement;
  var $ = function (sel, ctx) { return (ctx || document).querySelector(sel); };
  var $$ = function (sel, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); };

  /* ---------- Theme toggle (persisted) ---------- */
  var THEME_KEY = 'zw-theme';
  function applyTheme(t) {
    if (t === 'light' || t === 'dark') root.setAttribute('data-theme', t);
    else root.removeAttribute('data-theme');
    var meta = $('meta[name="theme-color"]');
    if (meta) {
      var dark = t === 'dark' || (t !== 'light' && window.matchMedia('(prefers-color-scheme: dark)').matches);
      meta.setAttribute('content', dark ? '#0d0d0d' : '#ffffff');
    }
  }
  try { var saved = localStorage.getItem(THEME_KEY); if (saved === 'dark' || saved === 'light') applyTheme(saved); } catch (e) { /* storage blocked */ }
  $$('.theme-toggle').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var current = root.getAttribute('data-theme');
      var systemDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
      var isDark = current === 'dark' || (!current && systemDark);
      var next = isDark ? 'light' : 'dark';
      applyTheme(next);
      try { localStorage.setItem(THEME_KEY, next); } catch (e) { /* ignore */ }
    });
  });

  /* ---------- Header hairline on scroll ---------- */
  var header = $('.site-header');
  if (header) {
    var onScroll = function () { header.classList.toggle('is-scrolled', window.scrollY > 8); };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* ---------- Mobile menu ---------- */
  var menuBtn = $('.menu-btn');
  var nav = $('.nav');
  if (menuBtn && nav) {
    menuBtn.addEventListener('click', function () {
      var open = nav.classList.toggle('is-open');
      menuBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    nav.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') { nav.classList.remove('is-open'); menuBtn.setAttribute('aria-expanded', 'false'); }
    });
  }

  /* ---------- Scroll-spy for in-page nav ---------- */
  var spyLinks = $$('.nav a[href^="#"]');
  if (spyLinks.length && 'IntersectionObserver' in window) {
    var map = {};
    spyLinks.forEach(function (a) { var id = a.getAttribute('href').slice(1); var el = document.getElementById(id); if (el) map[id] = a; });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          spyLinks.forEach(function (a) { a.classList.remove('is-active'); });
          var a = map[en.target.id]; if (a) a.classList.add('is-active');
        }
      });
    }, { rootMargin: '-40% 0px -55% 0px', threshold: 0 });
    Object.keys(map).forEach(function (id) { io.observe(document.getElementById(id)); });
  }

  /* ---------- News: show more ---------- */
  var newsBtn = $('[data-news-more]');
  if (newsBtn) {
    var hidden = $$('.news-item[data-extra]');
    newsBtn.addEventListener('click', function () {
      var expanded = newsBtn.getAttribute('aria-expanded') === 'true';
      hidden.forEach(function (li) { li.hidden = expanded; });
      newsBtn.setAttribute('aria-expanded', expanded ? 'false' : 'true');
      newsBtn.textContent = expanded ? newsBtn.getAttribute('data-label-more') : newsBtn.getAttribute('data-label-less');
    });
  }

  /* ---------- Publications: filter tabs ---------- */
  var tabs = $$('.tab[data-filter]');
  var pubs = $$('.pub');
  var emptyNote = $('.empty-note');
  function applyFilter(f) {
    var shown = 0;
    pubs.forEach(function (p) {
      var ok = f === 'all' || (p.getAttribute('data-tags') || '').split(' ').indexOf(f) !== -1;
      p.hidden = !ok; if (ok) shown++;
    });
    tabs.forEach(function (t) { t.setAttribute('aria-selected', t.getAttribute('data-filter') === f ? 'true' : 'false'); });
    if (emptyNote) emptyNote.hidden = shown !== 0;
    try { history.replaceState(null, '', f === 'all' ? location.pathname + '#publications' : location.pathname + '#publications-' + f); } catch (e) { /* ignore */ }
  }
  if (tabs.length) {
    tabs.forEach(function (t) { t.addEventListener('click', function () { applyFilter(t.getAttribute('data-filter')); }); });
    var m = location.hash.match(/^#publications-(\w+)$/);
    var initial = m ? m[1] : (tabs[0].getAttribute('data-filter'));
    if (!tabs.some(function (t) { return t.getAttribute('data-filter') === initial; })) initial = 'all';
    applyFilter(initial);
  }

  /* ---------- Lightbox for design gallery ---------- */
  var dlg = $('.lightbox');
  if (dlg && typeof dlg.showModal === 'function') {
    var dlgImg = $('img', dlg), dlgCap = $('.lightbox-caption', dlg);
    $$('.gallery button').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var img = $('img', btn);
        dlgImg.src = btn.getAttribute('data-full') || img.src;
        dlgImg.alt = img.alt;
        if (dlgCap) dlgCap.textContent = img.alt;
        dlg.showModal();
      });
    });
    dlg.addEventListener('click', function (e) { if (e.target === dlg || e.target.classList.contains('lightbox-close')) dlg.close(); });
    dlg.addEventListener('close', function () { dlgImg.removeAttribute('src'); });
  }

  /* ---------- Back to top ---------- */
  $$('.to-top').forEach(function (a) {
    a.addEventListener('click', function (e) { e.preventDefault(); window.scrollTo({ top: 0, behavior: 'smooth' }); });
  });
})();
