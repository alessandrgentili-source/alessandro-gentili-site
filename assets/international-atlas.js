/* Progressive enhancements: static links, articles and the comparison work without JS. */
(() => {
  'use strict';
  const main = document.querySelector('.international-atlas .atlas-main');
  if (!main) return;
  // The shared script adds its own focus-aware skip link. Retain the static
  // fallback only when that enhancement did not run (including no-JS mode).
  if (document.querySelectorAll('body > .skip-link').length > 1) {
    document.querySelector('[data-atlas-skip]')?.remove();
  }
  const form = main.querySelector('.atlas-search');
  if (form) {
    const input = form.querySelector('input');
    const status = form.querySelector('[role="status"]');
    const entries = [...document.querySelectorAll('[data-atlas-search]')];
    const groups = [...document.querySelectorAll('.atlas-group')];
    const empty = document.querySelector('.atlas-no-results');
    const directoryNav = document.querySelector('.atlas-directory-nav');
    const normalize = value => value.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().replace(/[^a-z0-9]+/g, ' ').trim();
    // Small, explicit editorial vocabulary; no remote service or invented AI ranking.
    const vocabulary = {
      education: ['education', 'formation', 'pedagogy', 'teaches', 'learn'],
      media: ['media', 'visibility', 'environment', 'images', 'language'],
      democracy: ['democracy', 'democratic', 'republic', 'collective decision'],
      freedom: ['freedom', 'liberty', 'self-mastery'],
      desire: ['desire', 'desiring', 'satisfaction', 'consumer'],
      power: ['power', 'government', 'sovereignty', 'authority', 'rule'],
      trust: ['trust', 'exchange', 'promises', 'credibility'],
      war: ['war', 'conflict', 'force']
    };
    const filter = () => {
      const tokens = normalize(input.value.trim()).split(/\s+/).filter(Boolean);
      let count = 0;
      let published = 0;
      for (const entry of entries) {
        const text = ` ${normalize(entry.dataset.atlasSearch)}`;
        // Start at a word boundary: "formation" must not accidentally match "information".
        const matches = tokens.every(token => (vocabulary[token] || [token]).some(term => text.includes(` ${normalize(term)}`)));
        entry.hidden = !matches;
        if (matches) { count++; if (entry.dataset.guideStatus === 'published') published++; }
      }
      groups.forEach(group => { group.hidden = ![...group.querySelectorAll('[data-atlas-search]')].some(entry => !entry.hidden); });
      directoryNav.hidden = tokens.length > 0;
      empty.hidden = count > 0;
      status.textContent = `${count} authors · ${published} published English guides${count > published ? ` · ${count - published} English guides forthcoming` : ''}`;
    };
    form.hidden = false;
    form.addEventListener('submit', event => event.preventDefault());
    form.addEventListener('input', filter);
    form.addEventListener('reset', () => { input.value = ''; filter(); input.focus(); });
    filter();
  }

  const contents = main.querySelector('.atlas-contents details');
  if (contents) {
    const mobile = window.matchMedia('(max-width: 760px)');
    contents.open = !mobile.matches;
    const links = [...contents.querySelectorAll('.guide-toc a[href^="#"]')];
    const sections = links.map(link => document.getElementById(link.hash.slice(1))).filter(Boolean);
    let queued = false;
    const update = () => {
      queued = false;
      let current = sections[0];
      const padding = parseFloat(getComputedStyle(document.documentElement).scrollPaddingTop) || 0;
      for (const section of sections) {
        const margin = parseFloat(getComputedStyle(section).scrollMarginTop) || 0;
        if (section.getBoundingClientRect().top <= padding + margin + 8) current = section;
      }
      links.forEach(link => {
        if (current && link.hash === `#${current.id}`) link.setAttribute('aria-current', 'location');
        else link.removeAttribute('aria-current');
      });
    };
    const schedule = () => {
      if (!queued) { queued = true; window.requestAnimationFrame(update); }
    };
    // Read the position actually reached, not the requested hash: scrolling can
    // stop early near the document end, or continue through an optional figure.
    window.addEventListener('scroll', schedule, { passive: true });
    ['resize', 'hashchange', 'pageshow', 'load'].forEach(event => window.addEventListener(event, schedule));
    mobile.addEventListener('change', () => {
      // Only reset at the layout boundary; preserve a reader's disclosure choice
      // during scrolling and ordinary resizes within the same layout.
      contents.open = !mobile.matches;
      schedule();
    });
    if ('ResizeObserver' in window) {
      const observer = new ResizeObserver(schedule);
      main.querySelectorAll('.atlas-guide-opening, .atlas-reading').forEach(element => observer.observe(element));
    }
    // Run after shared header measurement and native deep-link positioning.
    schedule();
  }
})();
