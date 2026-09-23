#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build static HTML for zoe-wang.com from data.py.

Usage:  python3 build.py [output_dir]
"""
import html, os, sys, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import data as D
import json
try:
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "image_dims.json")) as _f:
        DIMS = {k: tuple(v) for k, v in json.load(_f).items()}
except Exception:
    DIMS = {}

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
SITE_URL = "https://www.zoe-wang.com"
UPDATED = datetime.date.today().strftime("%b %Y")
E = html.escape

# ----------------------------------------------------------------- icons
ICONS = {
    "sun": '<svg class="icon-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>',
    "moon": '<svg class="icon-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>',
    "menu": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>',
    "ext": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17 17 7M8 7h9v9"/></svg>',
    "scholar": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 3 1 9l11 6 9-4.9V17h2V9L12 3zm-6.5 9.7V17c0 1.7 2.9 3.5 6.5 3.5s6.5-1.8 6.5-3.5v-4.3L12 16.3l-6.5-3.6z"/></svg>',
    "mail": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg>',
    "linkedin": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M20.4 2H3.6A1.6 1.6 0 0 0 2 3.6v16.8A1.6 1.6 0 0 0 3.6 22h16.8a1.6 1.6 0 0 0 1.6-1.6V3.6A1.6 1.6 0 0 0 20.4 2zM8 19H5V9h3v10zM6.5 7.7a1.7 1.7 0 1 1 0-3.4 1.7 1.7 0 0 1 0 3.4zM19 19h-3v-4.9c0-1.2 0-2.7-1.6-2.7s-1.9 1.3-1.9 2.6V19h-3V9h2.9v1.4h.1a3.2 3.2 0 0 1 2.8-1.6c3 0 3.6 2 3.6 4.6V19z"/></svg>',
    "x": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.5 3h3.1l-6.8 7.8L21.8 21h-6.3l-4.9-6.4L5 21H1.9l7.3-8.3L1.5 3h6.4l4.4 5.9L17.5 3zm-1.1 16.2h1.7L6.9 4.7H5.1l11.3 14.5z"/></svg>',
    "github": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-3.2 19.5c.5.1.7-.2.7-.5v-1.8c-2.8.6-3.4-1.2-3.4-1.2-.4-1.2-1.1-1.5-1.1-1.5-.9-.6.1-.6.1-.6 1 .1 1.5 1 1.5 1 .9 1.6 2.4 1.1 3 .9.1-.7.4-1.1.6-1.4-2.2-.2-4.6-1.1-4.6-4.9 0-1.1.4-2 1-2.7-.1-.3-.4-1.3.1-2.7 0 0 .8-.3 2.8 1a9.5 9.5 0 0 1 5 0c1.9-1.3 2.8-1 2.8-1 .5 1.4.2 2.4.1 2.7.6.7 1 1.6 1 2.7 0 3.8-2.3 4.7-4.6 4.9.4.3.7.9.7 1.9v2.8c0 .3.2.6.7.5A10 10 0 0 0 12 2z"/></svg>',
    "up": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" width="14" height="14"><path d="M12 19V5M5 12l7-7 7 7"/></svg>',
    "close": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true" width="18" height="18"><path d="M6 6l12 12M18 6 6 18"/></svg>',
}

# ----------------------------------------------------------------- helpers
def people_link(name):
    url = D.PROFILE["people"].get(name)
    return f'<a href="{E(url)}">{E(name)}</a>' if url else E(name)

def author_html(a):
    sup = ""
    while a and a[-1] in "*†":
        sup = a[-1] + sup; a = a[:-1]
    a = a.strip()
    name = f'<span class="me">{E(a)}</span>' if a == D.ME else E(a)
    if sup: name += f'<sup>{E(sup)}</sup>'
    return name

def is_preprint(venue):
    v = venue.lower()
    return v.startswith("arxiv") or v.startswith("preprint")

def pub_html(p):
    authors = ", ".join(author_html(a) for a in p["authors"])
    links = "".join(
        f'<a href="{E(u)}" target="_blank" rel="noopener">{E(k)}{ICONS["ext"]}</a>' for k, u in p["links"].items()
    )
    primary = p["links"].get("arXiv") or p["links"].get("PDF") or next(iter(p["links"].values()))
    tags = " ".join(p["tags"]) if p["tags"] else ""
    vcls = "venue is-preprint" if is_preprint(p["venue"]) else "venue"
    flag = '<span class="flag">First author</span>' if "first" in p["tags"] else ""
    return f'''
      <li class="pub" id="pub-{E(p["id"])}" data-tags="{E(tags)}" data-year="{p["year"]}" data-area="{E(p["area"])}">
        <a class="pub-thumb" href="{E(primary)}" target="_blank" rel="noopener" tabindex="-1" aria-hidden="true">
          <img src="assets/img/pubs/{E(p["image"])}" alt="" loading="lazy" decoding="async">
        </a>
        <div class="pub-body">
          <h3 class="pub-title"><a href="{E(primary)}" target="_blank" rel="noopener">{E(p["title"])}</a></h3>
          <p class="pub-authors">{authors}</p>
          <div class="pub-meta"><span class="{vcls}" title="{E(p.get("venue_full", ""))}">{E(p["venue"])}</span>{flag}</div>
          <div class="pub-links">{links}</div>
          <details class="abstract">
            <summary>Abstract</summary>
            <p>{E(p["abstract"])}</p>
          </details>
        </div>
      </li>'''

def news_html(i, date, text, visible=6):
    extra = ' data-extra hidden' if i >= visible else ''
    return f'''
      <li class="news-item"{extra}>
        <span class="news-date">{E(date)}</span>
        <span class="news-text">{text}</span>
      </li>'''

def head(title, desc, path="", extra_meta=""):
    url = SITE_URL + "/" + path
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{E(title)}</title>
  <meta name="description" content="{E(desc)}">
  <meta name="author" content="Ziyi Wang">
  <meta name="theme-color" content="#ffffff">
  <link rel="canonical" href="{E(url)}">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{E(title)}">
  <meta property="og:description" content="{E(desc)}">
  <meta property="og:url" content="{E(url)}">
  <meta property="og:image" content="{SITE_URL}/assets/img/profile.jpg">
  <meta name="twitter:card" content="summary">
  <meta name="twitter:site" content="@ZoeWang0213">
  <link rel="icon" href="assets/favicon.ico" sizes="any">
  <link rel="icon" href="assets/img/favicon-32.png" type="image/png" sizes="32x32">
  <link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="css/style.css">
  <script>
    /* Apply saved theme before first paint to avoid a flash */
    try {{ var t = localStorage.getItem('zw-theme'); if (t === 'dark' || t === 'light') document.documentElement.setAttribute('data-theme', t); }} catch (e) {{}}
  </script>{extra_meta}
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>'''

def header(active):
    def item(href, label, key):
        cur = ' aria-current="page"' if key == active else ''
        return f'<a href="{href}"{cur}>{label}</a>'
    home = "index.html" if active != "home" else "#top"
    links = [
        item("index.html#about" if active != "home" else "#about", "About", "about"),
        item("index.html#news" if active != "home" else "#news", "News", "news"),
        item("index.html#publications" if active != "home" else "#publications", "Publications", "publications"),
        item("design.html", "Design", "design"),
    ]
    return f'''
  <header class="site-header" id="top">
    <div class="wrap">
      <a class="brand" href="{home}" aria-label="Ziyi Wang — home"><img class="brand-mark" src="assets/img/favicon-32.png" alt="" width="26" height="26">Ziyi Wang</a>
      <nav class="nav" id="nav" aria-label="Primary">{"".join(links)}</nav>
      <div class="nav-actions">
        <button class="icon-btn theme-toggle" type="button" aria-label="Toggle dark mode">{ICONS["sun"]}{ICONS["moon"]}</button>
        <button class="icon-btn menu-btn" type="button" aria-label="Menu" aria-expanded="false" aria-controls="nav">{ICONS["menu"]}</button>
      </div>
    </div>
  </header>'''

def footer():
    return f'''
  <footer class="footer">
    <div class="wrap">
      <p>Made with two cups of bubble tea and Ziyi’s 🎧 · Last updated {E(UPDATED)}</p>
      <p><a class="to-top" href="#top">Back to top {ICONS["up"]}</a></p>
    </div>
  </footer>
  <script src="js/main.js" defer></script>
</body>
</html>
'''

# ----------------------------------------------------------------- index.html
def build_index():
    P = D.PROFILE
    L = P["links"]
    news = "".join(news_html(i, d, t) for i, (d, t) in enumerate(D.NEWS))
    pubs = "".join(pub_html(p) for p in D.PUBS)
    n_first = sum(1 for p in D.PUBS if "first" in p["tags"])
    n_sel = sum(1 for p in D.PUBS if "selected" in p["tags"])

    bg = ""
    if getattr(D, "EDUCATION", None) or getattr(D, "EXPERIENCE", None):
        def tl(items):
            return "".join(
                f'<li><span class="when">{E(i["when"])}</span><span><span class="what">{E(i["what"])}</span><span class="where">{E(i["where"])}</span></span></li>'
                for i in items)
        bg = f'''
    <section class="section" id="background" aria-labelledby="background-h">
      <div class="wrap">
        <div class="section-head"><h2 id="background-h">Background</h2></div>
        <div class="bg-grid">
          <div class="bg-col"><h3>Education</h3><ul class="timeline">{tl(D.EDUCATION)}</ul></div>
          <div class="bg-col"><h3>Experience</h3><ul class="timeline">{tl(D.EXPERIENCE)}</ul></div>
        </div>
      </div>
    </section>'''

    body = f'''{head("Ziyi (Zoe) Wang — Ph.D. student in HCI & Human-AI Interaction, Texas A&M", "Ziyi ‘Zoe’ Wang is a Ph.D. student in Computer Science & Engineering at Texas A&M University working on human-centered AI: designing, building and evaluating interactive systems that help people leverage, adapt and extend AI.")}
{header("home")}
  <main id="main">
    <section class="hero" id="about">
      <div class="wrap hero-grid">
        <div>
          <h1>{E(P["name"])} <span class="name-cn" lang="zh-Hans">{E(P["name_cn"])}</span></h1>
          <p class="hero-sub">Hi! I’m Ziyi 👋 I’m a Ph.D. student in <b>Computer Science &amp; Engineering at Texas A&amp;M University</b>, advised by {people_link("Prof. Meng Xia")}.</p>
          <div class="prose">
            <p>My research uses human-centered methods to design, develop, and evaluate interactive systems that empower people to effectively leverage, adapt, and extend AI in their work and daily lives — to enhance their capabilities and augment their cognition.</p>
            <p>Previously, I was a Master’s student in HCI at the University of Maryland, working with {people_link("Dr. Zijian Ding")} and {people_link("Prof. Fumeng Yang")}. I also collaborated with {people_link("Prof. Yue Zhao")}, {people_link("Prof. Xiyang Hu")}, and {people_link("Prof. Xiang Yan")}. Before research, I worked as a designer on global brand design at NIO, HMI design at BMW, UX at Publicis Sapient and AI product management at bilibili — see my <a href="design.html">design work</a>.</p>
          </div>
          <div class="interests" aria-label="Research interests">
            <span class="chip">Human-Centered AI</span><span class="chip">Human–AI Interaction</span><span class="chip">Natural Language Processing</span><span class="chip">Design</span>
          </div>
          <div class="hero-links">
            <a class="btn btn-primary" href="{E(L["scholar"])}" target="_blank" rel="noopener">{ICONS["scholar"]}Google Scholar</a>
            <a class="btn" href="mailto:{E(P["email"])}">{ICONS["mail"]}Email</a>
            <a class="btn" href="{E(L["linkedin"])}" target="_blank" rel="noopener">{ICONS["linkedin"]}LinkedIn</a>
            <a class="btn" href="{E(L["twitter"])}" target="_blank" rel="noopener">{ICONS["x"]}Twitter</a>
            <a class="btn" href="{E(L["github"])}" target="_blank" rel="noopener">{ICONS["github"]}GitHub</a>
          </div>
        </div>
        <figure class="hero-photo">
          <img src="assets/img/profile.jpg" alt="Ziyi Wang sitting on a lawn, flashing two peace signs" width="1350" height="1800" fetchpriority="high">
        </figure>
      </div>
    </section>

    <section class="section" id="news" aria-labelledby="news-h">
      <div class="wrap">
        <div class="section-head">
          <h2 id="news-h">News</h2>
          <p class="aside">{len(D.NEWS)} updates since May 2025</p>
        </div>
        <ul class="news-list">{news}
        </ul>
        <div class="more-row">
          <button class="btn btn-ghost" type="button" data-news-more aria-expanded="false" data-label-more="Show all news" data-label-less="Show less">Show all news</button>
        </div>
      </div>
    </section>

    <section class="section" id="publications" aria-labelledby="pubs-h">
      <div class="wrap">
        <div class="section-head">
          <h2 id="pubs-h">Publications</h2>
          <p class="aside">Full record on <a href="{E(L["scholar"])}" target="_blank" rel="noopener">Google Scholar ↗</a></p>
        </div>
        <div class="pub-toolbar">
          <div class="tabs" role="tablist" aria-label="Filter publications">
            <button class="tab" role="tab" type="button" data-filter="selected" aria-selected="true">Selected</button>
            <button class="tab" role="tab" type="button" data-filter="first" aria-selected="false">First-author</button>
            <button class="tab" role="tab" type="button" data-filter="all" aria-selected="false">All ({len(D.PUBS)})</button>
          </div>
          <p class="legend"><sup>*</sup> Equal contribution &nbsp;·&nbsp; <sup>†</sup> Corresponding author</p>
        </div>
        <ul class="pub-list">{pubs}
        </ul>
        <p class="empty-note" hidden>Nothing here yet.</p>
      </div>
    </section>{bg}
  </main>
{footer()}'''
    return body

# ----------------------------------------------------------------- design.html
def build_design():
    secs = ""
    navs = "".join(f'<a class="chip" href="#{E(s["id"])}">{E(s["org"])}</a>' for s in D.DESIGN_SECTIONS)
    for s in D.DESIGN_SECTIONS:
        figs = ""
        for i in range(1, s["count"] + 1):
            fn = f'{s["id"]}-{i:02d}.jpg'
            w, h = DIMS.get(fn, (4, 3))
            ratio = w / h
            alt = f'{s["org"]} — {s["title"]} ({i}/{s["count"]})'
            figs += f'''
          <figure style="--r:{ratio:.4f}"><button type="button" data-full="assets/img/design/{fn}" aria-label="Enlarge: {E(alt)}"><img src="assets/img/design/{fn}" alt="{E(alt)}" width="{w}" height="{h}" loading="lazy" decoding="async"></button></figure>'''
        cols = ""
        secs += f'''
    <section class="work" id="{E(s["id"])}" aria-labelledby="{E(s["id"])}-h">
      <div class="wrap">
        <div class="work-head">
          <h2 id="{E(s["id"])}-h">{E(s["title"])}<span class="org">@ {E(s["org"])}</span></h2>
          <p>{E(s["blurb"])}</p>
        </div>
        <div class="gallery{cols}">{figs}
        </div>
      </div>
    </section>'''
    return f'''{head("Design — Ziyi (Zoe) Wang", "Selected design work by Ziyi Wang: global brand design at NIO, HMI design at BMW, UX design at Publicis Sapient, AI product management at bilibili, and side projects.", "design.html")}
{header("design")}
  <main id="main">
    <section class="page-hero">
      <div class="wrap">
        <p class="eyebrow">Design</p>
        <h1>Welcome to my design space :)</h1>
        <p class="hero-sub">Before my Ph.D. I worked as a designer and product manager. A few things I made along the way — brand systems, in-car interfaces, product flows and some play.</p>
        <nav class="work-nav" aria-label="Sections">{navs}</nav>
      </div>
    </section>{secs}
  </main>
  <dialog class="lightbox" aria-label="Enlarged image">
    <button class="lightbox-close" type="button" aria-label="Close">{ICONS["close"]}</button>
    <img alt="">
    <p class="lightbox-caption"></p>
  </dialog>
{footer()}'''

# ----------------------------------------------------------------- 404.html
def build_404():
    return f'''{head("Page not found — Ziyi Wang", "That page does not exist.", "404.html")}
{header("none")}
  <main id="main">
    <section class="nf"><div>
      <p class="eyebrow">404</p>
      <h1>Nothing here.</h1>
      <p>Remember to drink water — and head <a class="u-link" href="index.html">back home</a>.</p>
    </div></section>
  </main>
{footer()}'''

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name, fn in (("index.html", build_index), ("design.html", build_design), ("404.html", build_404)):
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
            f.write(fn())
        print("wrote", os.path.join(OUT, name))
