#!/usr/bin/env python3
"""Static site generator for Stella Hur's portfolio — v3 foundation.
Hero (name + portrait + tagline) and primary pill nav are shared
across every page. Secondary filter nav is Work-page-only and is
injected by the caller.

Run pages.py (not this file directly) from the repo root to
regenerate the site: python3 pages.py
"""
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

NAV_ITEMS = [
    ("Work", "index.html"),
    ("About", "about.html"),
    ("Resume", "resume.html"),
    ("More About Me :)", "more.html"),
]


def primary_nav(active_href, root_prefix=""):
    links = []
    for label, href in NAV_ITEMS:
        cls = "active" if href == active_href else ""
        links.append(f'<a class="{cls}" href="{root_prefix}{href}">{label}</a>')
    return f'<nav class="nav-primary">\n      {"".join(links)}\n    </nav>'


def hero(root_prefix=""):
    return f'''<header class="hero">
      <h1 class="hero-name">Jeongwoo<br>Stella<br>Hur</h1>
      <div class="hero-portrait-wrap">
        <div class="hero-portrait">
          <img src="{root_prefix}assets/images/portrait.jpg" alt="Portrait of Stella Hur">
        </div>
      </div>
      <div class="hero-tagline">
        <p>Technical products. Creative marketing.<br>Everything in between.</p>
      </div>
    </header>'''


def footer(root_prefix=""):
    return f'''<footer class="site-footer">
      <span>&copy; 2026 Stella Hur</span>
      <span><a href="mailto:stellahur0130@gmail.com">stellahur0130@gmail.com</a> &nbsp;&middot;&nbsp; <a href="https://linkedin.com/in/jeongwoo-stella-hur" target="_blank" rel="noopener">LinkedIn</a></span>
    </footer>'''


def page(title, active_href, body, root_prefix="", secondary_nav_html=""):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — Stella Hur</title>
<meta name="description" content="Stella Hur — B2B Marketing Specialist.">
<link rel="icon" type="image/svg+xml" href="{root_prefix}assets/favicon/favicon.svg">
<link rel="icon" type="image/png" sizes="32x32" href="{root_prefix}assets/favicon/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="{root_prefix}assets/favicon/favicon-16x16.png">
<link rel="apple-touch-icon" href="{root_prefix}assets/favicon/apple-touch-icon.png">
<link rel="stylesheet" href="{root_prefix}css/style.css">
<!--
  FONTS: Montserrat (name / tagline / primary nav) and Poppins
  (everything else — body copy, project titles, secondary nav,
  buttons). Both are free, loaded via Google Fonts in style.css —
  no license needed. See the top of style.css for the full note.
-->
</head>
<body>
  <div class="page">
    <div class="content-max">
      {hero(root_prefix)}
      {primary_nav(active_href, root_prefix)}
      <!--
        Everything below is the region the client-side router
        swaps in place (see js/main.js) so switching between Work /
        About / Resume / More About Me feels like an iOS tab switch
        instead of a full page reload — hero + primary nav never
        remount. Each file is still a complete, valid standalone
        page for direct loads, no-JS, and SEO.
      -->
      <div id="app-content" data-page="{active_href}">
        {secondary_nav_html}
        {body}
        {footer(root_prefix)}
      </div>
    </div>
  </div>

  <script src="{root_prefix}js/main.js"></script>
</body>
</html>'''


def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as f:
        f.write(content)
    print("wrote", path)
