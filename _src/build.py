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
except FileNotFoundError:
    DIMS = {}
    print("warning: image_dims.json not found; design images fall back to 4:3 (run _src/update_dims.py)", file=sys.stderr)

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
SITE_URL = os.environ.get("SITE_URL", "https://www.zoe-wang.com").rstrip("/")
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
    a = a.rstrip("*† ").strip()   # equal-contribution / corresponding markers are kept in data but not shown
    return f'<span class="me">{E(a)}</span>' if a == D.ME else E(a)

BADGE_ICONS = {
    "award": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M8 21h8M12 17v4M7 4h10v5a5 5 0 0 1-10 0V4z"/><path d="M7 6H4a3 3 0 0 0 3 4M17 6h3a3 3 0 0 1-3 4"/></svg>',
    "oral": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m12 3 2.7 5.6 6.1.8-4.4 4.3 1.1 6.1L12 17l-5.5 2.8 1.1-6.1-4.4-4.3 6.1-.8z"/></svg>',
    "milestone": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 21V4M5 4h11l-2 4 2 4H5"/></svg>',
    "press": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 5h13v14H4zM17 8h3v9a2 2 0 0 1-2 2M7 9h7M7 13h7M7 16h4"/></svg>',
    "paper": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 3h7l4 4v14H7z"/><path d="M14 3v4h4M10 12h5M10 16h5"/></svg>',
}

def badge_kind(label):
    l = label.lower()
    if any(k in l for k in ("award", "best", "honorable", "spotlight", "prize", "recognition")): return "award"
    if any(k in l for k in ("oral", "talk", "keynote", "invited")): return "oral"
    if "milestone" in l: return "milestone"
    if "press" in l or "media" in l or "news" in l: return "press"
    return "paper"

def badge_class(label):
    k = badge_kind(label)
    cls = {"award": "badge badge-award", "oral": "badge badge-talk", "milestone": "badge badge-milestone", "press": "badge badge-press"}.get(k, "badge")
    if "preprint" in label.lower(): cls += " badge-outline"
    return cls

def badge_html(label):
    return f'<span class="{badge_class(label)}">{BADGE_ICONS[badge_kind(label)]}{E(label)}</span>'

def is_preprint(venue):
    v = venue.lower()
    return v.startswith("arxiv") or v.startswith("preprint")

def pub_html(p):
    authors = ", ".join(author_html(a) for a in p["authors"])
    links = "".join(
        f'<a href="{E(u)}" target="_blank" rel="noopener">{E(k)}{ICONS["ext"]}</a>' for k, u in p["links"].items()
    )
    primary = p["links"].get("arXiv") or p["links"].get("PDF") or (next(iter(p["links"].values())) if p["links"] else "")
    if not primary:
        raise SystemExit(f'error: publication "{p["id"]}" has no links; add at least a PDF or arXiv URL in _src/data.py')
    tags = " ".join(p["tags"]) if p["tags"] else ""
    hidden = "" if "selected" in p["tags"] else " hidden"
    vcls = "venue is-preprint" if is_preprint(p["venue"]) else "venue"
    flag = ""
    vf = p.get("venue_full", "")
    venue_full = f'<span class="visually-hidden"> ({E(vf)})</span>' if vf and vf.lower() != p["venue"].lower() else ""
    badges = "".join(badge_html(b) for b in p.get("badges", []))
    return f'''
      <li class="pub" id="pub-{E(p["id"])}" data-tags="{E(tags)}" data-year="{p["year"]}" data-area="{E(p["area"])}"{hidden}>
        <a class="pub-thumb" href="{E(primary)}" target="_blank" rel="noopener" tabindex="-1" aria-hidden="true">
          <img src="assets/img/pubs/{E(p["image"])}" alt="" loading="lazy" decoding="async">
        </a>
        <div class="pub-body">
          <div class="pub-meta"><span class="{vcls}">{E(p["venue"])}{venue_full}</span>{flag}{badges}</div>
          <h3 class="pub-title">{E(p["title"])}</h3>
          <p class="pub-authors">{authors}</p>
          <div class="pub-links">{links}</div>
        </div>
      </li>'''

def news_html(i, date, text, badges=(), visible=6):
    extra = ' data-extra hidden' if i >= visible else ''
    b = "".join(" " + badge_html(x) for x in badges)
    return f'''
      <li class="news-item"{extra}>
        <span class="news-date">{E(date)}</span>
        <span class="news-text">{text}{b}</span>
      </li>'''

def head(title, desc, path="", extra_meta="", base="", canonical=True):
    url = SITE_URL + "/" + path
    canon = f'\n  <link rel="canonical" href="{E(url)}">' if canonical else '\n  <meta name="robots" content="noindex">'
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{E(title)}</title>
  <meta name="description" content="{E(desc)}">
  <meta name="author" content="Ziyi Wang">
  <meta name="color-scheme" content="light">
  <meta name="theme-color" content="#ffffff">{canon}
  <meta property="og:type" content="website">
  <meta property="og:title" content="{E(title)}">
  <meta property="og:description" content="{E(desc)}">
  <meta property="og:url" content="{E(url)}">
  <meta property="og:image" content="{SITE_URL}/assets/img/og.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="Ziyi (Zoe) Wang">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:site" content="@ZoeWang0213">
  <link rel="icon" href="{base}assets/favicon.ico" sizes="any">
  <link rel="icon" href="{base}assets/img/favicon-32.png" type="image/png" sizes="32x32">
  <link rel="apple-touch-icon" href="{base}assets/img/apple-touch-icon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{base}css/style.css">
  <script>document.documentElement.classList.add('js');</script>
  <noscript><style>.pub[hidden]{{display:flex!important}}.news-item[hidden]{{display:grid!important}}.tabs,.more-row,[data-filter-status]{{display:none!important}}</style></noscript>{extra_meta}
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  <div id="top"></div>'''

JSONLD = '''
  <script type="application/ld+json">
  {"@context":"https://schema.org","@type":"Person","name":"Ziyi Wang","alternateName":["Zoe Wang","王子一"],
   "url":"https://www.zoe-wang.com/","image":"https://www.zoe-wang.com/assets/img/profile.jpg",
   "jobTitle":"Ph.D. student","affiliation":{"@type":"CollegeOrUniversity","name":"Texas A&M University"},
   "alumniOf":{"@type":"CollegeOrUniversity","name":"University of Maryland, College Park"},
   "email":"mailto:ziyiwang@tamu.edu",
   "sameAs":["https://scholar.google.com/citations?user=dYNpjEUAAAAJ","https://www.linkedin.com/in/ziyi-wang-488122292/","https://github.com/Zoewang0213","https://x.com/ZoeWang0213"]}
  </script>'''

def header(active, base=""):
    def item(href, label, key):
        cur = ' aria-current="page"' if key == active else ''
        return f'<a href="{base}{href}"{cur}>{label}</a>'
    home = base + "index.html" if active != "home" else "#top"
    if base and active != "home": home = base
    links = [
        item("index.html#about" if active != "home" else "#about", "About", "about"),
        item("index.html#news" if active != "home" else "#news", "News", "news"),
        item("index.html#publications" if active != "home" else "#publications", "Publications", "publications"),
        item("design.html", "Design", "design"),
    ]
    return f'''
  <header class="site-header">
    <div class="wrap">
      <a class="brand" href="{home}" aria-label="Ziyi Wang — home"><img class="brand-mark" src="{base}assets/img/favicon-32.png" alt="" width="26" height="26">Ziyi Wang</a>
      <nav class="nav" id="nav" aria-label="Primary">{"".join(links)}</nav>
      <div class="nav-actions">
        <button class="icon-btn menu-btn" type="button" aria-label="Menu" aria-expanded="false" aria-controls="nav">{ICONS["menu"]}</button>
      </div>
    </div>
  </header>'''

def footer(base=""):
    return f'''
  <footer class="footer">
    <div class="wrap">
      <p>Made with two cups of bubble tea and Ziyi’s 🎧 · Last updated {E(UPDATED)}</p>
      <p><a class="to-top" href="#top">Back to top {ICONS["up"]}</a></p>
    </div>
  </footer>
  <script src="{base}js/main.js" defer></script>
</body>
</html>
'''

# ----------------------------------------------------------------- index.html
def build_index():
    P = D.PROFILE
    L = P["links"]
    news = "".join(news_html(i, *item) for i, item in enumerate(D.NEWS))
    pubs = "".join(pub_html(p) for p in D.PUBS)
    n_first = sum(1 for p in D.PUBS if "first" in p["tags"])
    themes = ""
    for t in D.RESEARCH_THEMES:
        papers = " · ".join(f'<a href="#pub-{E(pid)}">{E(name)}</a>' for name, pid in t["papers"])
        themes += f'''
            <li><b>{E(t["title"])}</b> <span class="theme-desc">{E(t["desc"])}</span> <span class="theme-papers">{papers}</span></li>'''
    n_sel = sum(1 for p in D.PUBS if "selected" in p["tags"])

    bg = ""
    SPECIAL = badge_html("Special Recognition")
    service = ""
    if getattr(D, "SERVICE", None):
        rows = "".join(f'<li><span class="when">{E(k)}</span><span class="what">{v.replace("{SPECIAL}", SPECIAL)}</span></li>' for k, v in D.SERVICE)
        service = f'''
        <div class="personal service">
          <h3>Service &amp; honors</h3>
          <ul class="timeline personal-list">{rows}</ul>
        </div>'''
    personal = ""
    if getattr(D, "PERSONAL", None):
        items = "".join(f'<li><span class="when">{E(k)}</span><span class="what">{v}</span></li>' for k, v in D.PERSONAL)
        personal = f'''
        <div class="personal">
          <h3>Beyond research</h3>
          <ul class="timeline personal-list">{items}</ul>
        </div>'''
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
          <div class="bg-col"><h3>Research assistant</h3><ul class="timeline">{tl(getattr(D, "RESEARCH", []))}</ul></div>
          <div class="bg-col"><h3>Industry experience</h3><ul class="timeline">{tl(D.EXPERIENCE)}</ul></div>
        </div>{service}{personal}
      </div>
    </section>'''

    body = f'''{head("Ziyi (Zoe) Wang — HCI & Human-AI Interaction, Texas A&M", "Ziyi ‘Zoe’ Wang is a Ph.D. student in Computer Science & Engineering at Texas A&M University working on human-centered AI: designing, building and evaluating interactive systems that help people leverage, adapt and extend AI.", extra_meta=JSONLD)}
{header("home")}
  <main id="main" tabindex="-1">
    <section class="hero" id="about">
      <div class="wrap hero-grid">
        <figure class="hero-photo">
          <img src="assets/img/profile.jpg" alt="Ziyi Wang sitting on a lawn, flashing two peace signs" width="1350" height="1800" fetchpriority="high">
        </figure>
        <div>
          <h1>{E(P["name"])} <span class="name-cn" lang="zh-Hans">{E(P["name_cn"])}</span></h1>
          <p class="hero-sub">Hi! I’m Ziyi 👋 I’m a first-year Ph.D. student in <b>Computer Science at Texas A&amp;M University</b>, advised by {people_link("Prof. Meng Xia")}.</p>
          <div class="prose">
            <p>My research advances human-centered AI that helps people understand themselves and one another. I design, build, and evaluate interactive systems that foster reflection, empathy, and social connection, while safeguarding users against the socio-emotional risks of emerging technologies. My work spans NLP and HCI and has appeared at EMNLP, ACL, DIS, IEEE VIS, and AAAI.</p>
            <p>Previously, I was a Master’s student in HCI at the University of Maryland, working with {people_link("Dr. Zijian Ding")} and {people_link("Prof. Fumeng Yang")}. I also collaborated with {people_link("Prof. Yue Zhao")}, {people_link("Prof. Xiyang Hu")}, and {people_link("Prof. Xiang Yan")}.</p>
          </div>
          <div class="hero-links">
            <a class="btn" href="{E(L["scholar"])}" target="_blank" rel="noopener">{ICONS["scholar"]}Google Scholar</a>
            <a class="btn" href="mailto:{E(P["email"])}">{ICONS["mail"]}Email</a>
            <a class="btn" href="{E(L["linkedin"])}" target="_blank" rel="noopener">{ICONS["linkedin"]}LinkedIn</a>
            <a class="btn" href="{E(L["twitter"])}" target="_blank" rel="noopener">{ICONS["x"]}Twitter</a>
          </div>
        </div>
      </div>
    </section>

    <section class="section" id="news" aria-labelledby="news-h">
      <div class="wrap">
        <div class="section-head">
          <h2 id="news-h">News</h2>
        </div>
        <ul class="news-list">{news}
        </ul>
        <div class="more-row">
          <button class="btn btn-ghost" type="button" data-news-more data-step="5" aria-expanded="false" data-label-more="Show more" data-label-less="Show less">Show more</button>
        </div>
      </div>
    </section>

    <section class="section" id="publications" aria-labelledby="pubs-h">
      <div class="wrap">
        <div class="section-head">
          <h2 id="pubs-h">Publications</h2>
          <p class="aside">Full record on <a href="{E(L["scholar"])}" target="_blank" rel="noopener">Google Scholar ↗</a></p>
        </div>
        <div class="research">
          <p class="research-q">{E(D.RESEARCH_QUESTION)}</p>
          <ol class="themes">{themes}
          </ol>
        </div>
        <div class="pub-toolbar">
          <div class="tabs" role="group" aria-label="Filter publications">
            <button class="tab" type="button" data-filter="selected" aria-pressed="true">Selected</button>
            <button class="tab" type="button" data-filter="all" aria-pressed="false">All ({len(D.PUBS)})</button>
          </div>
          <p class="visually-hidden" aria-live="polite" data-filter-status></p>
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
            caps = s.get("captions") or []
            alt = caps[i - 1] if i - 1 < len(caps) and caps[i - 1] else f'{s["org"]} {s["title"].lower()} — work sample {i} of {s["count"]}'
            figs += f'''
          <figure style="--r:{ratio:.4f}"><a class="zoom" href="assets/img/design/{fn}" data-caption="{E(alt)}"><img src="assets/img/design/{fn}" alt="{E(alt)}" width="{w}" height="{h}" loading="lazy" decoding="async"></a></figure>'''
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
  <main id="main" tabindex="-1">
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
    <img alt="" src="data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==">
    <p class="lightbox-caption"></p>
  </dialog>
{footer()}'''

# ----------------------------------------------------------------- 404.html
def build_404():
    return f'''{head("Page not found — Ziyi Wang", "That page does not exist.", "404.html", base="/", canonical=False)}
{header("none", base="/")}
  <main id="main" tabindex="-1">
    <section class="nf"><div>
      <p class="eyebrow">404</p>
      <h1>Nothing here.</h1>
      <p>Remember to drink water — and head <a class="u-link" href="/">back home</a>.</p>
    </div></section>
  </main>
{footer(base="/")}'''

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name, fn in (("index.html", build_index), ("design.html", build_design), ("404.html", build_404)):
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
            f.write(fn())
        print("wrote", os.path.join(OUT, name))
