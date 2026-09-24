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
    var dark = t === 'dark' || (t !== 'light' && window.matchMedia('(prefers-color-scheme: dark)').matches);
    $$('meta[name="theme-color"]').forEach(function (m) {
      if (t === 'dark' || t === 'light') { m.setAttribute('content', dark ? '#000000' : '#ffffff'); m.removeAttribute('media'); }
    });
    $$('.theme-toggle').forEach(function (b) { b.setAttribute('aria-pressed', dark ? 'true' : 'false'); });
  }
  var savedTheme = null;
  try { savedTheme = localStorage.getItem(THEME_KEY); } catch (e) { /* storage blocked */ }
  if (savedTheme === 'dark' || savedTheme === 'light') applyTheme(savedTheme);
  else if (root.getAttribute('data-theme')) applyTheme(root.getAttribute('data-theme')); /* attribute set in markup */
  else applyTheme(null);
  var mq = window.matchMedia('(prefers-color-scheme: dark)');
  if (mq.addEventListener) mq.addEventListener('change', function () { if (!root.getAttribute('data-theme')) applyTheme(null); });
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
    var setMenu = function (open, refocus) {
      nav.classList.toggle('is-open', open);
      menuBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
      if (open) { var first = nav.querySelector('a'); if (first) first.focus(); }
      else if (refocus) menuBtn.focus();
    };
    menuBtn.addEventListener('click', function () { setMenu(!nav.classList.contains('is-open'), false); });
    nav.addEventListener('click', function (e) { if (e.target.tagName === 'A') setMenu(false, false); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && nav.classList.contains('is-open')) setMenu(false, true); });
    window.addEventListener('resize', function () { if (window.innerWidth > 720 && nav.classList.contains('is-open')) setMenu(false, false); });
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
  var status = $('[data-filter-status]');
  function applyFilter(f, fromUser) {
    var shown = 0;
    pubs.forEach(function (p) {
      var ok = f === 'all' || (p.getAttribute('data-tags') || '').split(' ').indexOf(f) !== -1;
      p.hidden = !ok; if (ok) shown++;
    });
    tabs.forEach(function (t) { t.setAttribute('aria-pressed', t.getAttribute('data-filter') === f ? 'true' : 'false'); });
    if (emptyNote) emptyNote.hidden = shown !== 0;
    if (status) status.textContent = 'Showing ' + shown + ' of ' + pubs.length + ' publications';
    if (fromUser) {
      try { history.replaceState(null, '', location.pathname + (f === 'all' ? '#publications' : '#publications-' + f)); } catch (e) { /* ignore */ }
    }
  }
  if (tabs.length) {
    tabs.forEach(function (t) { t.addEventListener('click', function () { applyFilter(t.getAttribute('data-filter'), true); }); });
    var m = location.hash.match(/^#publications-(\w+)$/);
    var initial = m ? m[1] : tabs[0].getAttribute('data-filter');
    if (!tabs.some(function (t) { return t.getAttribute('data-filter') === initial; })) initial = 'all';
    var target = location.hash.match(/^#pub-/) ? document.getElementById(location.hash.slice(1)) : null;
    if (target) initial = 'all';
    applyFilter(initial, false);
    if (target) target.scrollIntoView();
    else if (m) { var sec = document.getElementById('publications'); if (sec) sec.scrollIntoView({ behavior: 'instant', block: 'start' }); }
  }

  /* ---------- Lightbox for design gallery ---------- */
  var dlg = $('.lightbox');
  if (dlg && typeof dlg.showModal === 'function') {
    var dlgImg = $('img', dlg), dlgCap = $('.lightbox-caption', dlg);
    var blank = dlgImg.getAttribute('src');
    $$('.gallery a.zoom').forEach(function (a) {
      a.addEventListener('click', function (e) {
        if (e.metaKey || e.ctrlKey || e.shiftKey || e.button !== 0) return; /* let modifier-clicks open the file */
        e.preventDefault();
        var img = $('img', a);
        dlgImg.src = a.getAttribute('href');
        dlgImg.alt = img.alt;
        if (dlgCap) dlgCap.textContent = a.getAttribute('data-caption') || img.alt;
        dlg.showModal();
        document.body.style.overflow = 'hidden';
      });
    });
    dlg.addEventListener('click', function (e) { if (e.target === dlg || e.target.closest('.lightbox-close')) dlg.close(); });
    dlg.addEventListener('close', function () { dlgImg.src = blank; document.body.style.overflow = ''; });
  }

})();
