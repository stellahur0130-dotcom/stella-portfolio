# Stella Hur — Portfolio

A plain HTML/CSS/JS site. No build step, no framework, no dependencies to
install — every page works by just opening the `.html` file, and the whole
thing deploys to Netlify by connecting this repo directly.

## Deploying

**Netlify (recommended):**
1. Push this repo to GitHub.
2. In Netlify: **Add new site → Import an existing project → GitHub** → pick this repo.
3. Build settings: leave **Build command** blank and set **Publish directory** to `/` (the repo root). There's nothing to build.
4. Deploy. Done — every push to your main branch auto-redeploys.

A `netlify.toml` is already included with these settings pre-filled, so Netlify
should detect them automatically.

**GitHub Pages** works too, if you'd rather use that: Settings → Pages → Deploy
from branch → root.

---

## Folder structure

```
index.html          Work (homepage)
about.html
resume.html
more.html            "More About Me :)"
css/style.css         all styling
js/main.js             nav routing, category filtering
assets/
  images/              every photo on the site
  Stella_Hur_Resume.pdf   the downloadable resume file
pages.py, build_site.py   optional — regenerates the HTML from Python
                          (see "Editing text" below; not required to deploy)
```

Each `.html` file is a complete, standalone page — you can open any one of
them directly in a browser with no server needed.

---

## 1. Editing images (any card, any size)

Every image card is a **padded white frame around a plain `<img>` tag** — no
cropping, no fixed shape. The frame just wraps whatever image you give it.
**To replace an image: put your new file at the same path with the same
filename, keeping the same file extension.** That's it — no code changes.

Where the files live:

| What | Path |
|---|---|
| Your profile photo | `assets/images/portrait.jpg` |
| Work → "All" grid (6 cards) | `assets/images/work/overview/<category-slug>.jpg` |
| Work → category detail images | `assets/images/work/<category-folder>/<project>.jpg` |
| About page image | `assets/images/about/about-image.jpg` |
| More About Me cards | `assets/images/more/card-1.jpg` through `card-7.jpg` |

**Any dimensions work.** A card sizes itself to whatever image you drop in —
tall photo, wide photo, square, doesn't matter. If you want to swap a
landscape placeholder for a portrait photo, just do it; the card will get
taller automatically, nothing gets cropped, and the layout reflows around it.

If you want to add a *brand new* image slot that doesn't exist yet, that
requires a small code change — see "Editing text" below, since new slots are
defined in `pages.py`.

### Sizing notes
- Every frame has a small (8px) padding so the image never touches the
  rounded corner — this is what prevents corners from clipping content.
- There's a generous `max-height` safety cap on most frames (e.g. 560px for
  project images) purely so one extremely tall photo can't blow out the whole
  page layout. Photos wider than they are tall will basically never hit this
  cap. If you ever do hit it and want a taller display, search `max-height`
  in `css/style.css` and adjust the relevant rule.

---

## 2. Editing videos

Every video on the site is currently a **placeholder Vimeo embed** (the same
video, id `1222911482`, repeated everywhere). Vimeo's own player already
handles click-to-play and fullscreen (there's a fullscreen button built into
its controls) — there's no custom video code to worry about.

**To swap in your real videos:** open `pages.py`, find this line near the top:

```python
VIMEO_URL = "https://player.vimeo.com/video/1222911482"
```

If you want the *same* real video everywhere, just change this one line and
regenerate (see below). If you want *different* videos per project, you'll
add a `vimeo_id` (or similar) field per project in the `CATEGORIES` list and
adjust `vimeo_embed_html()` to use it — ask me and I can wire this up for you
if/when you're ready with real clips.

**Uploading your own videos to Vimeo:** create a free Vimeo account, upload
your clip, and use the numeric ID from its player URL
(`vimeo.com/1234567` → the ID is `1234567`) in place of the placeholder one.

---

## 3. Editing text

There are two ways to do this, depending on your comfort level:

### Option A — edit the HTML directly (no tools needed)
Every page's text is plain, readable HTML. Open `index.html`, `about.html`,
`resume.html`, or `more.html` in any text editor, find the sentence you want
to change, edit it, save. This works for one-off tweaks to any single page.

### Option B — edit `pages.py` and regenerate (better for repeated content)
Text that repeats across the site (the hero tagline, nav labels) or is
organized as structured data (Work categories/projects, Resume experience
entries, Skills, Languages) lives in `pages.py` as plain Python
lists/dictionaries — this is usually easier to edit accurately than hunting
through generated HTML, especially for the Work page's 6 categories.

To regenerate after editing `pages.py`:
```bash
python3 pages.py
```
This rewrites `index.html`, `about.html`, `resume.html`, and `more.html` from
the data in `pages.py`. Requires Python 3 (no other dependencies).

**You do not need to do this to deploy** — the committed `.html` files are
already fully built and ready. Only run this if you've edited `pages.py` and
want those changes reflected in the HTML.

The one thing shared across *every* page (your name, the tagline, primary
nav) lives in `build_site.py`, in the `hero()` and `NAV_ITEMS` — edit there if
you want to change those, then run `python3 pages.py` again.

---

## 4. Resume PDF

The **Download Resume PDF** button on the Resume page points to:

```
assets/Stella_Hur_Resume.pdf
```

**⚠️ The file currently there is an old resume draft from early in this
project — it does not match the "Resume" page content on the site.** Replace
it with your current resume, keeping the exact same filename, and the
download button will just work with no other changes needed.

---

## 5. Mobile responsiveness

Every page has been checked at both desktop and mobile (390px) widths:
- The hero collapses to a single stacked column below 760px.
- The Work grid and video grids drop to one column on narrow screens.
- The Resume experience rows and Skills grid stack vertically.
- The More About Me two-column layout (images | text) becomes one column.

If you add new sections and they don't look right on mobile, the relevant
breakpoints in `css/style.css` are `@media (max-width: ...)` rules — search
for the component's class name (e.g. `.work-overview`) and you'll find its
mobile override nearby.

---

## Fonts

Two free Google Fonts, no license needed for either:
- **Montserrat** — your name, the tagline, and the primary nav (Work / About
  / Resume / More About Me).
- **Poppins** — everything else (project titles, body copy, secondary nav,
  buttons).

Both are loaded via `@import` at the top of `css/style.css`. If you want to
change either, that's the line to edit — plus the `--font-display` /
`--font-body` variables just below it in the `:root` block.

---

## Colors & other design tokens

Every color, spacing value, and corner radius on the site is a CSS variable
defined once at the top of `css/style.css`, inside `:root`. Changing, say,
`--accent` there updates the accent blue everywhere it's used (currently the
active Work pill and a few link/text-color spots) — no need to hunt through
the rest of the file.

---

## Questions / next steps

Things that are still placeholder and worth filling in when you're ready:
- Real photos in every image slot listed above.
- A real resume PDF.
- Real video(s) on Vimeo, swapped in via `VIMEO_URL`.
- The five "More About Me" text modules (Colombia, hobbies, currently
  watching, favorite AI videos, design references) — currently bracketed
  placeholder copy in `pages.py`.
