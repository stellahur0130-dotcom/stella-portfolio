#!/usr/bin/env python3
"""Run this from inside the repo root: python3 pages.py
Regenerates index.html / about.html / resume.html / more.html
from the data below and from build_site.py."""
from build_site import page, write

# ============================================================
# WORK (home)
#
# Content model: CATEGORY -> [SUBSECTION, ...]. Clicking a
# category in the secondary nav never navigates anywhere — it
# just shows/hides subsections in this one continuous scroll.
#
# Each subsection has exactly one of:
#   img            — path under assets/images/, single photo
#   video          — path under assets/videos/, single clip
#   grid_videos     + grid_cols — a grid of N clips (e.g. 2x2)
#   grid_imgs       + grid_cols — same, for a grid of photos
#
# All frames auto-size to whatever file is actually there — no
# cropping, no fixed aspect ratio. Replace any file (same path,
# any dimensions) and the card just reflows. See README.md.
# ============================================================

CATEGORIES = [
    (1, "Technical Marketing", "technical-marketing", [
        dict(title="Technical Datasheet",
             desc="Product datasheets translating complex specs into clear, accessible technical documentation.",
             img="work/technical-marketing/technical-datasheet.jpg"),
        dict(title="Product Brochures & One-Pagers",
             desc="Concise brochures and one-pagers built to introduce products and highlight key differentiators at a glance.",
             img="work/technical-marketing/product-brochures.jpg"),
        dict(title="White Papers & Reports",
             desc="Long-form white papers and reports distilling technical and market research into digestible insights.",
             img="work/technical-marketing/white-papers.jpg"),
    ]),
    (2, "Product Launches & Campaigns", "product-launches-campaigns", [
        dict(title="Press Releases",
             desc="Press coverage secured with outlets including The Wall Street Journal and The New York Times, coordinated with photographers and the internal team.",
             img="work/product-launches/press-releases.jpg"),
        dict(title="New Product Introductions",
             desc="NPI communications and press releases supporting new product rollouts.",
             img="work/product-launches/new-product-introductions.jpg"),
        dict(title="Product Launch Productions",
             desc="Teaser videos and launch productions built to generate excitement ahead of product releases.",
             video=True),
    ]),
    (3, "Graphic Design", "graphic-design", [
        dict(title="Banner Ads",
             desc="Press, social, and email banner ads designed to capture attention and drive action.",
             img="work/graphic-design/banner-ads.jpg"),
        dict(title="Live Event Graphics",
             desc="Standalone marketing graphics for live events, trade shows, and expos.",
             img="work/graphic-design/live-event-graphics.jpg"),
        dict(title="Internal Magazine Covers",
             desc="Cover design and art direction for internal company magazines.",
             img="work/graphic-design/internal-magazine-covers.jpg"),
    ]),
    (4, "Video Production", "video-production", [
        dict(title="Field & Site Production",
             desc="On-location product and site video — manufacturing in India, field-testing, GoPro road testing, and testing in Jaisalmer.",
             grid_cols=2,
             grid_videos=4),
        dict(title="Edited Productions",
             desc="Post-production and editing work.",
             video=True),
        dict(title="3D Renders & Animation",
             desc="3D rendering and animation work supporting product storytelling.",
             grid_cols=2,
             grid_videos=2),
    ]),
    (5, "Events & Trade Shows", "events-tradeshows", [
        dict(title="Tradeshows & Live Events",
             desc="End-to-end trade show and event execution, spanning booth concepts and design, product displays, marketing materials, vendor coordination, logistics, and on-site support across domestic and international events.",
             img="work/events-tradeshows/tradeshows-live-events.jpg",
             list=["G-STAR 2021 — Busan, Korea", "Imagine Live Korea 2022 — Seoul, Korea",
                   "APEC 2023 — Orlando, Florida", "CES 2024 — Las Vegas, Nevada",
                   "APEC 2024 — Long Beach, California", "Electronica China 2024 — Shanghai, China",
                   "Elexcon 2024 — Shenzhen, China", "CES 2025 — Las Vegas, Nevada"]),
    ]),
    (6, "Web Design", "web-design", [
        dict(title="Conifer Website — V1",
             desc="[Draft] First website build for Conifer.",
             img="work/web-design/conifer-website-v1.jpg"),
        dict(title="Conifer Website — V2",
             desc="[Draft] Second website build/redesign for Conifer.",
             img="work/web-design/conifer-website-v2.jpg"),
        dict(title="Independent Web Projects",
             desc="Two additional independent web design projects.",
             img="work/web-design/independent-web-projects.jpg"),
    ]),
]

FILTERS = [(label, slug) for _, label, slug, _ in CATEGORIES]

secondary_nav = '<nav class="nav-secondary">\n      <button class="active" data-filter="all"><span>All</span></button>\n      ' + "\n      ".join(
    f'<button data-filter="{slug}"><span class="idx">{str(i+1).zfill(2)}</span><span>{label}</span></button>'
    for i, (label, slug) in enumerate(FILTERS)
) + '\n    </nav>'

disclaimer = ('<p class="disclaimer">* All information and content presented in this portfolio are '
              'publicly available and have been officially released by the respective companies.</p>')


# ---- Mode A: "All" overview — one card per category ----

def overview_card(num, label, slug):
    return f'''<button class="overview-card" data-goto="{slug}">
        <div class="overview-thumb">
          <img src="assets/images/work/overview/{slug}.jpg" alt="{label}" loading="lazy">
        </div>
        <div class="overview-title">{str(num).zfill(2)} {label}</div>
      </button>'''

overview_grid = '<div class="work-overview">\n      ' + "\n      ".join(
    overview_card(num, label, slug) for num, label, slug, _ in CATEGORIES
) + '\n    </div>'


# ---- Mode B: one rounded panel per category, stacked projects
#      (image -> title -> description [-> list]) ----

# Placeholder video for every video slot on the site — swap this
# one URL and every video card updates. Vimeo's own player handles
# click-to-play and fullscreen (via its built-in controls), so no
# custom JS/lightbox is needed for video at all.
VIMEO_URL = "https://player.vimeo.com/video/1222911482"

def vimeo_embed_html(title):
    return (f'<div class="video-embed">'
            f'<iframe src="{VIMEO_URL}" title="{title}" '
            f'frameborder="0" allow="autoplay; fullscreen; picture-in-picture" '
            f'allowfullscreen loading="lazy"></iframe>'
            f'</div>')

def project_media(sub):
    if sub.get("grid_videos"):
        cols = sub.get("grid_cols", 2)
        tiles = "".join(
            f'<div class="proj-media-grid-tile">{vimeo_embed_html(sub["title"])}</div>'
            for _ in range(sub["grid_videos"])
        )
        return f'<div class="proj-media-grid" style="grid-template-columns: repeat({cols}, 1fr);">{tiles}</div>'

    if sub.get("grid_imgs"):
        cols = sub.get("grid_cols", 2)
        tiles = "".join(
            f'<div class="proj-media-grid-tile"><img src="assets/images/{src}" alt="{sub["title"]}" loading="lazy"></div>'
            for src in sub["grid_imgs"]
        )
        return f'<div class="proj-media-grid" style="grid-template-columns: repeat({cols}, 1fr);">{tiles}</div>'

    if sub.get("video"):
        return f'<div class="proj-image">{vimeo_embed_html(sub["title"])}</div>'

    return f'<div class="proj-image"><img src="assets/images/{sub["img"]}" alt="{sub["title"]}" loading="lazy"></div>'

def project_block(sub):
    list_html = ""
    if sub.get("list"):
        items = "".join(f"<li>{item}</li>" for item in sub["list"])
        list_html = f'<ul class="list-plain">{items}</ul>'

    return f'''<div class="category-project">
        {project_media(sub)}
        <div class="proj-title">{sub["title"]}</div>
        <div class="proj-desc">{sub["desc"]}</div>
        {list_html}
      </div>'''

def category_panel(num, label, slug, subs):
    projects = "\n      ".join(project_block(s) for s in subs)
    return f'''<div class="category-panel is-hidden" data-category="{slug}">
      {projects}
    </div>'''

category_panels = "\n".join(
    category_panel(num, label, slug, subs) for num, label, slug, subs in CATEGORIES
)

work_body = f'''<div class="work-panel">
      {secondary_nav}
      {overview_grid}
{category_panels}
      {disclaimer}
    </div>'''

write("index.html", page("Work", "index.html", work_body, secondary_nav_html=""))


# ============================================================
# ABOUT — real content
# ============================================================

ABOUT_LEDE = 'I\'m a B2B marketer who likes to make technical products easier to understand — and harder to ignore!'

ABOUT_PARAGRAPHS = [
    "My background is in technical industries, from semiconductors to electric powertrains, where I've learned how to dig into complex technology, understand what makes them different, and turn that into marketing that's clear, engaging, and compelling.",
    "My work spans product launches, technical content, media campaigns, graphic design, video, websites, and trade shows. I especially enjoy the space between technical and creative: understanding how something works, figuring out what actually matters to the audience, and finding the best way to tell that story.",
    "I also love being hands-on. Whether that means building a new webpage, designing a brochure, filming in the field, or figuring out how to position a new product, I like taking ideas all the way from \u201cwe should do this\u201d to actually bringing them to life.",
]

# Recommendations shown as quote cards between the About text and photo.
RECOMMENDATIONS = [
    {
        "name": "Jae H Park",
        "role": "Marketing Executive",
        "linkedin": "https://www.linkedin.com/in/jaepark711/",
        "paragraphs": [
            "I cannot speak highly enough of Stella for her marketing communications skills, exceptional creativity, and work ethic. She consistently impresses with her imagination, dedication, and \u201ccan-do\u201d attitude.",
            "Stella has an amazing ability to create storyboards and visual concepts that truly connect with audiences. Whether she's designing graphics, managing projects big or small, or running marketing campaigns, she manages everything with ease and a great attitude. Her creative process is both strategic and flexible, making sure every project is executed perfectly.",
            "One of Stella's standout qualities is her ability to approach any challenge with confidence and determination. When faced with something new, she proactively seeks solutions and quickly learns how to do it, always delivering quality work on time. Her positive, can-do attitude makes her a pleasure to work with and contributes to the success of every team she's part of.",
            "Stella is the perfect Marcom Specialist who consistently goes above and beyond with her creative designs, sharp attention to detail, and strong organizational skills. She's a real asset to any team, and I highly recommend her to any company looking for a talented, resourceful, and creative marketing communications pro!",
        ],
    },
    {
        "name": "Hakan Cervell",
        "role": "President, Ericsson Saudi Arabia (formerly Ericsson Korea)",
        "linkedin": "https://www.linkedin.com/in/hakan-cervell-b1a6b1/",
        "paragraphs": [
            "Stella did an outstanding job in Marketing and Communications, and she really proved it is possible to contribute to a company in a great way also as an intern. With her impressive integrity, mindset and strong willingness to learn, she was able to contribute to a number of important company events, both internal and external. I would recommend her 7 days a week and I hope she will come back to our company and take a permanent role later. As an intern, she was really an asset to us.",
            "It is always great to see young talents seeing the opportunity and perform on a high level in new environments.",
        ],
    },
]


def quote_card_html(rec):
    paras = "\n              ".join(f"<p>{p}</p>" for p in rec["paragraphs"])
    return f'''<div class="quote-card">
            <blockquote class="quote-text">
              {paras}
            </blockquote>
            <div class="quote-attribution">
              <span class="quote-name"><a href="{rec['linkedin']}" target="_blank" rel="noopener">{rec['name']}</a></span>
              <span class="quote-role">{rec['role']}</span>
            </div>
          </div>'''


about_quotes_html = '''<div class="about-quotes">
          ''' + "\n          ".join(quote_card_html(r) for r in RECOMMENDATIONS) + '''
        </div>'''

about_body = '''<div class="content-panel">
      <div class="about-eyebrow">About</div>
      <p class="about-lede">''' + ABOUT_LEDE + '''</p>
      <div class="about-body">
        ''' + "\n        ".join(f"<p>{p}</p>" for p in ABOUT_PARAGRAPHS) + '''
        ''' + about_quotes_html + '''
        <div class="about-image"><img src="assets/images/about/about-image.jpg" alt="About Stella Hur" loading="lazy"></div>
      </div>
    </div>'''

write("about.html", page("About", "about.html", about_body))


# ============================================================
# RESUME — real content
# ============================================================

EXPERIENCE = [
    dict(date="Apr 2025 \u2013 Present",
         role="Marketing",
         company="Conifer",
         company_desc="Conifer is a fast-growing electric powertrain company developing next-generation motors and powertrain systems based in Sunnyvale, CA.",
         role_desc="As Conifer's first dedicated marketing hire, I've been building marketing from the ground up \u2014 from launching the company out of stealth to leading product campaigns, content, web, events, and customer outreach across the U.S. and India."),
    dict(date="Feb 2023 \u2013 Mar 2025",
         role="Marketing Communications Specialist",
         company="Halo Microelectronics International",
         company_desc="Halo Microelectronics is a semiconductor company developing analog and power management integrated circuits for mobile, IoT, automotive, and other applications.",
         role_desc="As part of a two-person global marketing team, I managed product launches, campaigns, websites, technical collateral, content, and trade shows across the U.S. and Asia, supporting teams and markets including South Korea, Japan, China, and Singapore."),
    dict(date="May 2022 \u2013 Aug 2022",
         role="Marketing and Communications Intern",
         company="Ericsson",
         company_desc="Ericsson is a global telecommunications company providing network infrastructure, software, and services.",
         role_desc="As a marketing intern at Ericsson Korea, I managed the daily internal newsletter for 300+ employees and supported B2B product showcases, press conferences, content, and internal and external communications."),
    dict(date="May 2021 \u2013 Jan 2022",
         role="Marketing and Sales Intern",
         company="data.ai (acquired by Sensor Tower), formerly App Annie",
         company_desc="data.ai was a mobile analytics and market intelligence platform helping companies understand app performance, markets, and consumer behavior.",
         role_desc="As the team's first marketing intern, I managed content optimization and localization for global campaigns and supported sales and customer success initiatives for the Korean market."),
]

EDUCATION = dict(
    date="Aug 2018 \u2013 Dec 2022, Class of 2022",
    role="University of California, Berkeley",
    company="B.A. Economics",
)

SKILLS = [
    ("CMS / Web", "WordPress, Webflow, Squarespace, GitHub"),
    ("CRM / Marketing", "Marketo, Salesforce, HubSpot, Zapier, Google Analytics, LinkedIn Campaign Manager"),
    ("Sales / Outreach", "Apollo, Lemlist, LinkedIn Sales Navigator"),
    ("Project Management", "Notion, Asana"),
    ("Adobe Creative", "Photoshop, Illustrator, InDesign, Lightroom, Premiere Pro, Premiere Rush"),
    ("AI", "ChatGPT, Claude, Higgsfield \u2014 I love new AI tools"),
    ("Social Media", "LinkedIn, Facebook, X (Twitter), YouTube"),
]

LANGUAGES = [("English", "Native"), ("Spanish", "Native"), ("Korean", "Native")]


def exp_row(item):
    return f'''<div class="resume-exp-row">
        <div class="exp-date">{item["date"]}</div>
        <div>
          <div class="exp-role">{item["role"]}</div>
          <div class="exp-company">{item["company"]}</div>
          {"<div class='exp-company-desc'>" + item["company_desc"] + "</div>" if item.get("company_desc") else ""}
          {"<div class='exp-role-desc'>" + item["role_desc"] + "</div>" if item.get("role_desc") else ""}
        </div>
      </div>'''

skills_html = "\n        ".join(
    f'<div class="skill-block"><div class="skill-cat">{cat}</div><div class="skill-items">{items}</div></div>'
    for cat, items in SKILLS
)

languages_html = "".join(
    f'<div class="lang-chip"><div class="lang-name">{lang}</div><div class="lang-level">{level}</div></div>'
    for lang, level in LANGUAGES
)

resume_body = '''<div class="content-panel resume-panel">
      <div class="resume-toolbar">
        <a class="resume-download" href="assets/Stella_Hur_Resume.pdf" download>&#8595;&nbsp; Download Resume PDF</a>
      </div>

      <div class="section-label">Experience</div>
      <div class="resume-exp-list">
        ''' + "\n        ".join(exp_row(e) for e in EXPERIENCE) + '''
      </div>

      <div class="section-label">Education</div>
      <div class="resume-exp-list">
        ''' + exp_row(EDUCATION) + '''
      </div>

      <div class="section-label">Skills</div>
      <div class="skills-grid">
        ''' + skills_html + '''
      </div>

      <div class="section-label">Languages</div>
      <div class="languages-row">
        ''' + languages_html + '''
      </div>
    </div>'''

write("resume.html", page("Resume", "resume.html", resume_body))


# ============================================================
# MORE ABOUT ME — two columns: varied photo/video card grid on
# the left, text modules on the right.
# ============================================================

# Each card: (path, is_video). Cards keep whatever aspect ratio
# their own file has — no forced ratio — so this list is just
# "which file goes in which slot," not a size declaration.
# Video cards ignore `path` entirely (they use the shared Vimeo
# placeholder — see VIMEO_URL above).
MORE_CARDS = [
    ("more/card-1.jpg", False),
    ("more/card-2.jpg", False),
    (None, True),
    ("more/card-4.jpg", False),
    (None, True),
    ("more/card-6.jpg", False),
    ("more/card-7.jpg", False),
]

MORE_TEXT_BLOCKS = [
    ("Growing Up in Colombia",
     "[Placeholder \u2014 a few sentences on growing up in Colombia, and how it shaped your relationship to language and culture. Native in English, Spanish, and Korean.]"),
    ("Off the Clock",
     "[Placeholder \u2014 what you actually do on weekends. Specific, not generic.]"),
    ("Currently Watching",
     "[Placeholder \u2014 a short, specific list of shows/movies.]"),
    ("Favorite AI Videos",
     "[Placeholder \u2014 2\u20134 specific AI-generated videos or channels you love, with a line on why.]"),
    ("Design References",
     "[Placeholder \u2014 a short list of sites/designers you keep going back to.]"),
]

def more_card(path, is_video):
    if is_video:
        return f'<div class="more-card">{vimeo_embed_html("More About Me video")}</div>'
    return f'<div class="more-card"><img src="assets/images/{path}" alt="" loading="lazy"></div>'

more_image_grid = '<div class="more-image-grid">\n        ' + "\n        ".join(
    more_card(path, is_video) for path, is_video in MORE_CARDS
) + '\n      </div>'

more_text = '<div class="more-text">\n        ' + "\n        ".join(
    f'<div class="more-text-block"><h4>{title}</h4><p>{body}</p></div>'
    for title, body in MORE_TEXT_BLOCKS
) + '\n      </div>'

more_body = '''<div class="content-panel more-panel">
      <div class="more-columns">
        ''' + more_image_grid + '''
        ''' + more_text + '''
      </div>
    </div>'''

write("more.html", page("More About Me", "more.html", more_body))

print("\\nDone: foundation pages built.")
