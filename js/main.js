/* zoe-wang.com — small progressive enhancements. Everything works without JS. */
(function () {
  'use strict';
  var root = document.documentElement;
  var $ = function (sel, ctx) { return (ctx || document).querySelector(sel); };
  var $$ = function (sel, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); };

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
    var extras = $$('.news-item[data-extra]');
    var step = parseInt(newsBtn.getAttribute('data-step'), 10) || 5;
    var refresh = function () {
      var remaining = extras.filter(function (li) { return li.hidden; }).length;
      var allShown = remaining === 0;
      newsBtn.setAttribute('aria-expanded', allShown ? 'true' : 'false');
      newsBtn.textContent = allShown ? newsBtn.getAttribute('data-label-less')
        : newsBtn.getAttribute('data-label-more') + ' (' + remaining + ')';
    };
    newsBtn.addEventListener('click', function () {
      var hiddenOnes = extras.filter(function (li) { return li.hidden; });
      if (hiddenOnes.length) hiddenOnes.slice(0, step).forEach(function (li) { li.hidden = false; }); /* reveal the next few */
      else { extras.forEach(function (li) { li.hidden = true; }); var sec = document.getElementById('news'); if (sec) sec.scrollIntoView({ block: 'start' }); } /* collapse */
      refresh();
    });
    refresh();
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
    window.addEventListener('hashchange', function () {
      var el = location.hash.match(/^#pub-/) ? document.getElementById(location.hash.slice(1)) : null;
      if (el && el.hidden) { applyFilter('all', false); el.scrollIntoView(); }
    });
    if (target) target.scrollIntoView();
    else if (m) { var sec = document.getElementById('publications'); if (sec) sec.scrollIntoView({ behavior: 'instant', block: 'start' }); }
  }

  /* ---------- WeChat QR popup ---------- */
  var qr = $('.qr-dialog:not(.cat-dialog)');
  if (qr && typeof qr.showModal === 'function') {
    $$('[data-wechat]').forEach(function (a) {
      a.addEventListener('click', function (e) { e.preventDefault(); qr.showModal(); });
    });
    qr.addEventListener('click', function (e) { if (e.target === qr || e.target.closest('.qr-close')) qr.close(); });
  }

  /* ---------- Dumpling photo popup ---------- */
  var cat = $('.cat-dialog');
  if (cat && typeof cat.showModal === 'function') {
    var track = $('.cat-track', cat), slides = $$('img', track), count = $('.cat-count', cat);
    var prev = $('.cat-prev', cat), next = $('.cat-next', cat);
    var smooth = window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth';
    var current = function () { return track.clientWidth ? Math.round(track.scrollLeft / track.clientWidth) : 0; };
    var update = function () {
      var i = current();
      count.textContent = (i + 1) + ' / ' + slides.length;
      prev.disabled = i === 0;
      next.disabled = i === slides.length - 1;
    };
    var go = function (step) {
      track.scrollBy({ left: step * track.clientWidth, behavior: smooth });
      setTimeout(update, 400);
    };
    prev.addEventListener('click', function () { go(-1); });
    next.addEventListener('click', function () { go(1); });
    track.addEventListener('scroll', update, { passive: true });
    track.addEventListener('scrollend', update);
    cat.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowLeft') { e.preventDefault(); go(-1); }
      if (e.key === 'ArrowRight') { e.preventDefault(); go(1); }
    });
    $$('[data-cat]').forEach(function (a) {
      a.addEventListener('click', function (e) {
        e.preventDefault();
        cat.showModal();
        track.scrollLeft = 0;
        update();
      });
    });
    cat.addEventListener('click', function (e) { if (e.target === cat || e.target.closest('.qr-close')) cat.close(); });
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
