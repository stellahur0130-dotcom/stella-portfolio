// ============================================================
// STELLA HUR — PORTFOLIO — shared behavior (v4 foundation)
//
// Two things live here:
// 1. Secondary nav (Work-page category filter), including an
//    "All" reset state — rebindable, since #app-content gets
//    replaced wholesale by the router below.
// 2. A tiny client-side router. Every page is still a complete,
//    valid standalone HTML file (works with JS off, direct loads,
//    SEO). When JS is available, clicking a primary-nav link
//    fetches the target page, swaps only #app-content with a
//    soft cross-fade, and updates history — so switching tabs
//    feels like an iOS tab bar instead of a full page reload.
//    The hero and primary nav never remount.
// ============================================================

/* ---- Secondary nav: work-category filtering ----
   Two content modes pre-rendered in the DOM:
   - .work-overview: the "All" 6-card grid (one card per category)
   - .category-panel (x6): one rounded panel per category, each
     with its 3 stacked single-image projects
   Selecting "All" shows the overview grid and hides every panel.
   Selecting a category hides the overview grid and shows only
   that one panel. Overview cards are themselves clickable and
   drive the same filter, so the grid doubles as category entry
   points. Deep-linkable via #category-slug. */
function initSecondaryNav(root) {
  const filterBtns = root.querySelectorAll('.nav-secondary button');
  const overview = root.querySelector('.work-overview');
  const panels = root.querySelectorAll('.category-panel');
  const overviewCards = root.querySelectorAll('.overview-card[data-goto]');
  if (!filterBtns.length) return;

  function applyFilter(filter, updateHash) {
    filterBtns.forEach(b => b.classList.toggle('active', b.dataset.filter === filter));

    if (overview) overview.classList.toggle('is-hidden', filter !== 'all');
    panels.forEach(panel => {
      panel.classList.toggle('is-hidden', panel.dataset.category !== filter);
    });

    if (updateHash) {
      const url = filter === 'all' ? window.location.pathname : `${window.location.pathname}#${filter}`;
      window.history.replaceState(null, '', url);
    }
  }

   function scrollToNav() {
    const nav = document.querySelector('.nav-primary');
    if (!nav) return;
    const y = nav.getBoundingClientRect().top + window.scrollY - 24;
    window.scrollTo({ top: y, behavior: 'instant' });
  }

  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      applyFilter(btn.dataset.filter, true);
      scrollToNav();
    });
  });

  overviewCards.forEach(card => {
    card.addEventListener('click', () => {
      applyFilter(card.dataset.goto, true);
      scrollToNav();
    });
  });

  // Respect an incoming #category-slug (e.g. from a shared link,
  // or a page swap that preserved the hash) on first bind.
  const initialHash = window.location.hash.replace('#', '');
  const matches = initialHash && root.querySelector(`.nav-secondary button[data-filter="${initialHash}"]`);
  if (matches) applyFilter(initialHash, false);
}

/* ---- Lightweight router ---- */
const APP_CONTENT_ID = 'app-content';
const FADE_MS = 180;

function getAppContent(doc) {
  return doc.getElementById(APP_CONTENT_ID);
}

function setPrimaryNavActive(href) {
  document.querySelectorAll('.nav-primary a').forEach(a => {
    a.classList.toggle('active', a.getAttribute('href') === href);
  });
}

async function swapTo(href, { push = true } = {}) {
  const current = document.getElementById(APP_CONTENT_ID);
  if (!current) { window.location.href = href; return; }

  try {
    const res = await fetch(href, { credentials: 'same-origin' });
    if (!res.ok) throw new Error('fetch failed');
    const html = await res.text();
    const doc = new DOMParser().parseFromString(html, 'text/html');
    const next = getAppContent(doc);
    if (!next) throw new Error('no #app-content in response');

    // Fade current content out
    current.style.opacity = '0';
    await new Promise(resolve => setTimeout(resolve, FADE_MS));

    // Swap
    current.innerHTML = next.innerHTML;
    current.dataset.page = next.dataset.page || '';
    document.title = doc.title;
    setPrimaryNavActive(href);
    initSecondaryNav(current);

    // Fade new content in
    requestAnimationFrame(() => { current.style.opacity = '1'; });

    if (push) {
      window.history.pushState({ href }, '', href);
    }
  } catch (err) {
    // Fetch/parse failed for any reason — fall back to a normal
    // navigation rather than leaving the tab in a broken state.
    window.location.href = href;
  }
}

function initRouter() {
  const content = document.getElementById(APP_CONTENT_ID);
  if (content) {
    content.style.transition = `opacity ${FADE_MS}ms ease`;
  }

  document.querySelectorAll('.nav-primary a').forEach(link => {
    link.addEventListener('click', (e) => {
      const href = link.getAttribute('href');
      // Only intercept same-page internal nav links (not new tabs,
      // modified clicks, or external/special-protocol links).
      if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
      if (!href || href.startsWith('http') || href.startsWith('mailto:')) return;
      if (href === window.location.pathname.split('/').pop()) { e.preventDefault(); return; }

      e.preventDefault();
      swapTo(href);
    });
  });

  window.addEventListener('popstate', () => {
    const path = window.location.pathname.split('/').pop() || 'index.html';
    swapTo(path, { push: false });
  });
}

document.addEventListener('DOMContentLoaded', () => {
  const content = document.getElementById(APP_CONTENT_ID);
  if (content) {
    initSecondaryNav(content);
  }
  initRouter();
});
