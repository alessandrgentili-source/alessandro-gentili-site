const mobileNavQuery = window.matchMedia('(max-width: 760px)');
const dropdownNavItems = document.querySelectorAll('.primary-nav-item--dropdown');

const closePrimaryNavDropdowns = (exceptItem) => {
  dropdownNavItems.forEach((item) => {
    if (item === exceptItem) {
      return;
    }
    item.classList.remove('is-open');
    item.querySelector('.primary-nav-link')?.setAttribute('aria-expanded', 'false');
  });
};

dropdownNavItems.forEach((item) => {
  const trigger = item.querySelector('.primary-nav-link');
  if (!trigger) {
    return;
  }

  trigger.setAttribute('aria-expanded', 'false');
  trigger.addEventListener('click', (event) => {
    if (!mobileNavQuery.matches) {
      return;
    }

    event.preventDefault();
    const isOpen = item.classList.toggle('is-open');
    trigger.setAttribute('aria-expanded', String(isOpen));
    closePrimaryNavDropdowns(item);
  });
});

document.addEventListener('click', (event) => {
  if (!mobileNavQuery.matches || event.target.closest('.primary-nav')) {
    return;
  }

  closePrimaryNavDropdowns();
});

document.addEventListener('keydown', (event) => {
  if (event.key !== 'Escape') {
    return;
  }

  closePrimaryNavDropdowns();
});

mobileNavQuery.addEventListener('change', () => {
  closePrimaryNavDropdowns();
});
document.querySelectorAll('[data-filter]').forEach((button) => {
  button.addEventListener('click', () => {
    const filter = button.dataset.filter;
    document.querySelectorAll('[data-filter]').forEach((b) => b.setAttribute('aria-pressed', 'false'));
    button.setAttribute('aria-pressed', 'true');
    document.querySelectorAll('[data-archive-item]').forEach((item) => {
      item.hidden = filter !== 'all' && item.dataset.category !== filter;
    });
  });
});

document.querySelectorAll('[data-newsletter-form]').forEach((form) => {
  form.addEventListener('submit', (event) => {
    event.preventDefault();
    const name = form.querySelector('[name="name"]')?.value.trim() || '';
    const email = form.querySelector('[name="email"]')?.value.trim() || '';
    const feedback = form.querySelector('.feedback');
    const validEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    if (!name || !validEmail) {
      if (feedback) {
        feedback.textContent = 'Inserisci nome e indirizzo email valido.';
        feedback.dataset.state = 'error';
      }
      return;
    }
    const subject = encodeURIComponent('Iscrizione alla Lettera periodica');
    const body = encodeURIComponent(`Ciao Alessandro,\n\nvorrei iscrivermi alla Lettera periodica.\n\nNome: ${name}\nEmail: ${email}\n`);
    window.location.href = `mailto:lettera@alessandro-gentili.it?subject=${subject}&body=${body}`;
    if (feedback) {
      feedback.textContent = 'Si aprirà il tuo client email per confermare l’iscrizione.';
      feedback.dataset.state = 'ok';
    }
  });
});

const cookieConsentKey = 'ag_cookie_statistics';
const googleAnalyticsId = 'G-NCN48MN7VJ';
let googleAnalyticsLoaded = false;

const getCookieStatisticsPreference = () => {
  try {
    return window.localStorage.getItem(cookieConsentKey);
  } catch (error) {
    return null;
  }
};

const setCookieStatisticsPreference = (value) => {
  try {
    window.localStorage.setItem(cookieConsentKey, value);
  } catch (error) {
    // If storage is unavailable, keep the choice for the current page only.
  }
};

const loadGoogleAnalytics = () => {
  if (googleAnalyticsLoaded || document.querySelector(`script[src="https://www.googletagmanager.com/gtag/js?id=${googleAnalyticsId}"]`)) {
    googleAnalyticsLoaded = true;
    return;
  }

  const analyticsScript = document.createElement('script');
  analyticsScript.async = true;
  analyticsScript.src = `https://www.googletagmanager.com/gtag/js?id=${googleAnalyticsId}`;
  document.head.appendChild(analyticsScript);

  window.dataLayer = window.dataLayer || [];
  window.gtag = function gtag(){window.dataLayer.push(arguments);};
  window.gtag('js', new Date());
  window.gtag('config', googleAnalyticsId);
  googleAnalyticsLoaded = true;
};

const closeCookieBanner = () => {
  document.querySelector('[data-cookie-banner]')?.remove();
};

const showCookieBanner = () => {
  closeCookieBanner();

  const banner = document.createElement('section');
  banner.className = 'cookie-banner';
  banner.dataset.cookieBanner = '';
  banner.setAttribute('aria-label', 'Preferenze cookie');
  banner.innerHTML = `
    <div class="cookie-banner-copy">
      <p>Usiamo cookie tecnici necessari e, solo con il tuo consenso, strumenti statistici per capire come viene letto il sito e migliorare i contenuti.</p>
      <a href="/privacy.html">Privacy</a>
    </div>
    <div class="cookie-banner-actions">
      <button type="button" class="btn-secondary" data-cookie-reject>Rifiuta</button>
      <button type="button" class="btn" data-cookie-accept>Accetta statistiche</button>
    </div>
  `;

  banner.querySelector('[data-cookie-accept]')?.addEventListener('click', () => {
    setCookieStatisticsPreference('accepted');
    loadGoogleAnalytics();
    closeCookieBanner();
  });

  banner.querySelector('[data-cookie-reject]')?.addEventListener('click', () => {
    setCookieStatisticsPreference('rejected');
    closeCookieBanner();
  });

  document.body.appendChild(banner);
};

window.openCookiePreferences = showCookieBanner;

const cookieStatisticsPreference = getCookieStatisticsPreference();
if (cookieStatisticsPreference === 'accepted') {
  loadGoogleAnalytics();
} else if (cookieStatisticsPreference !== 'rejected') {
  showCookieBanner();
}

const getArchiveEssayNumber = (item) => {
  const explicitNumber = Number(item.dataset.essayNumber);
  if (Number.isFinite(explicitNumber)) {
    return explicitNumber;
  }

  const match = item.querySelector('h3')?.textContent.trim().match(/^(\d+)\s+—/);
  return match ? Number(match[1]) : null;
};

const sortNumberedArchiveEssays = (archiveList) => {
  const numberedEssays = Array.from(archiveList.querySelectorAll('[data-archive-item][data-category="saggi"]'))
    .map((item, index) => ({ item, index, number: getArchiveEssayNumber(item) }))
    .filter(({ number }) => Number.isFinite(number));

  if (numberedEssays.length < 2) {
    return;
  }

  const insertionPoint = numberedEssays[numberedEssays.length - 1].item.nextSibling;
  const sortedEssays = document.createDocumentFragment();
  numberedEssays
    .sort((a, b) => b.number - a.number || a.index - b.index)
    .forEach(({ item }) => sortedEssays.appendChild(item));

  archiveList.insertBefore(sortedEssays, insertionPoint);
};

// Keep Saggio 15 visible across the homepage, essays index and general archive.
(() => {
  const essayUrl = '/saggi/saggio-15-il-mondo-senza-apprendisti.html';
  const coverUrl = '/assets/img/saggi/site/saggio-15-il-mondo-senza-apprendisti_site_960x540.webp';
  const coverAlt = 'Cover del saggio Il mondo senza apprendisti: su fondo antracite, una sequenza di disegni tecnici conduce a un prototipo industriale, evocando il rapporto tra intelligenza artificiale, lavoro, apprendistato e formazione della competenza.';

  const latestGrid = document.querySelector('.latest-essays .essay-grid');
  if (latestGrid && !latestGrid.querySelector('[data-saggio-15]')) {
    latestGrid.insertAdjacentHTML('afterbegin', `
      <article class="essay-card" data-saggio-15>
        <figure class="essay-cover"><img src="${coverUrl}" width="1600" height="900" loading="lazy" alt="${coverAlt}" /></figure>
        <div class="essay-card-body"><p class="essay-number">Saggio 15 · <span class="essay-release-label">SAGGIO INTEGRALE</span></p><h3><a href="${essayUrl}">Il mondo senza apprendisti</a></h3><p class="essay-subtitle">Intelligenza artificiale, lavoro e scomparsa del tempo necessario a diventare capaci.</p><p class="meta">20 luglio 2026 · Macro · Saggio integrale nell’archivio locale</p></div>
        <div class="actions"><a class="btn-secondary" href="${essayUrl}">Leggi il saggio</a></div>
      </article>`);
    while (latestGrid.children.length > 3) {
      latestGrid.lastElementChild.remove();
    }
  }

  const essaysGrid = document.querySelector('#archivio-saggi .essay-grid');
  if (essaysGrid && !essaysGrid.querySelector('[data-saggio-15]')) {
    essaysGrid.insertAdjacentHTML('afterbegin', `
      <article class="essay-card" data-saggio-15>
        <figure class="essay-cover"><img src="${coverUrl}" width="1600" height="900" loading="lazy" alt="${coverAlt}" /></figure>
        <div class="essay-card-body"><div class="essay-card-meta"><span>SAGGIO 15</span><span class="essay-kind-pill">MACRO</span></div><h3><a href="${essayUrl}">Il mondo senza apprendisti</a></h3><p class="essay-subtitle">Intelligenza artificiale, lavoro e scomparsa del tempo necessario a diventare capaci.</p><p>Un saggio su AI, lavoro e apprendistato: perché migliori output possono nascondere la perdita del tempo necessario a formare gli esperti futuri.</p><p class="meta">20 luglio 2026 · Tema: AI, lavoro e formazione della competenza</p><div class="essay-status"><span>Testo integrale</span><span>English note</span></div></div>
        <div class="actions"><a class="btn-secondary" href="${essayUrl}">Leggi il saggio</a></div>
      </article>`);
  }

  const corpusTitle = document.querySelector('#corpus-title');
  if (corpusTitle) {
    corpusTitle.textContent = 'Percorso 0–15.';
  }
  const corpusList = document.querySelector('.essay-index-list');
  if (corpusList && !corpusList.querySelector('[data-saggio-15]')) {
    corpusList.insertAdjacentHTML('beforeend', `<article class="item" data-saggio-15><div><h3>15 — Il mondo senza apprendisti</h3><p class="meta">20 luglio 2026 · Testo integrale</p></div><div class="actions"><a class="btn-secondary" href="${essayUrl}">Leggi il saggio</a></div></article>`);
  }

  const generalArchive = document.querySelector('.archive-list');
  if (generalArchive && document.querySelector('[data-filter]') && !generalArchive.querySelector('[data-saggio-15]')) {
    const saggio14 = Array.from(generalArchive.querySelectorAll('[data-archive-item]')).find((item) => item.querySelector('h3')?.textContent.trim().startsWith('14 —'));
    const entry = `<article class="item" data-archive-item data-category="saggi" data-saggio-15 data-essay-number="15"><div><h3>15 — Il mondo senza apprendisti</h3><p class="meta">20 luglio 2026 · Saggio integrale · Archivio locale</p><p>Un saggio su intelligenza artificiale, lavoro e apprendistato: come preservare il processo che forma gli esperti futuri.</p></div><div class="actions"><a class="btn-secondary" href="${essayUrl}">Leggi il saggio</a></div></article>`;
    if (saggio14) {
      saggio14.insertAdjacentHTML('beforebegin', entry);
    } else {
      generalArchive.insertAdjacentHTML('afterbegin', entry);
    }
    sortNumberedArchiveEssays(generalArchive);
  }
})();

// Keep Saggio 16 visible across the homepage, essays index and general archive.
(() => {
  const essayUrl = '/saggi/saggio-16-la-pace-senza-forma.html';
  const coverUrl = '/assets/img/saggi/site/saggio-16-la-pace-senza-forma-960x540.webp';
  const coverAlt = 'Cover del saggio La pace senza forma: su fondo nero materico, due strutture verticali diseguali tendono senza riuscire a comporre una forma comune, immagine della distanza tra riarmo europeo e sovranità politica.';

  const latestGrid = document.querySelector('.latest-essays .essay-grid');
  if (latestGrid && !latestGrid.querySelector('[data-saggio-16]')) {
    latestGrid.insertAdjacentHTML('afterbegin', `
      <article class="essay-card" data-saggio-16>
        <figure class="essay-cover"><img src="${coverUrl}" width="960" height="540" loading="lazy" alt="${coverAlt}" /></figure>
        <div class="essay-card-body"><p class="essay-number">Saggio 16 · <span class="essay-release-label">SAGGIO INTEGRALE</span></p><h3><a href="${essayUrl}">La pace senza forma</a></h3><p class="essay-subtitle">L’Europa si arma, ma non ha ancora deciso quale ordine vuole difendere.</p><p class="meta">4 agosto 2026 · Macro · Saggio integrale nell’archivio locale</p></div>
        <div class="actions"><a class="btn-secondary" href="${essayUrl}">Leggi il saggio</a></div>
      </article>`);
    while (latestGrid.children.length > 3) {
      latestGrid.lastElementChild.remove();
    }
  }

  const essaysGrid = document.querySelector('#archivio-saggi .essay-grid');
  if (essaysGrid && !essaysGrid.querySelector('[data-saggio-16]')) {
    essaysGrid.insertAdjacentHTML('afterbegin', `
      <article class="essay-card" data-saggio-16>
        <figure class="essay-cover"><img src="${coverUrl}" width="960" height="540" loading="lazy" alt="${coverAlt}" /></figure>
        <div class="essay-card-body"><div class="essay-card-meta"><span>SAGGIO 16</span><span class="essay-kind-pill">MACRO</span></div><h3><a href="${essayUrl}">La pace senza forma</a></h3><p class="essay-subtitle">L’Europa si arma, ma non ha ancora deciso quale ordine vuole difendere.</p><p>Un saggio su riarmo europeo, NATO e sovranità: perché capacità militari senza autorità politica non bastano a dare forma alla pace.</p><p class="meta">4 agosto 2026 · Tema: Europa, difesa e sovranità strategica</p><div class="essay-status"><span>Testo integrale</span><span>English note</span></div></div>
        <div class="actions"><a class="btn-secondary" href="${essayUrl}">Leggi il saggio</a></div>
      </article>`);
  }

  const corpusTitle = document.querySelector('#corpus-title');
  if (corpusTitle) {
    corpusTitle.textContent = 'Percorso 0–16.';
  }
  const corpusList = document.querySelector('.essay-index-list');
  if (corpusList && !corpusList.querySelector('[data-saggio-16]')) {
    corpusList.insertAdjacentHTML('beforeend', `<article class="item" data-saggio-16><div><h3>16 — La pace senza forma</h3><p class="meta">4 agosto 2026 · Testo integrale</p></div><div class="actions"><a class="btn-secondary" href="${essayUrl}">Leggi il saggio</a></div></article>`);
  }

  const generalArchive = document.querySelector('.archive-list');
  if (generalArchive && document.querySelector('[data-filter]') && !generalArchive.querySelector('[data-saggio-16]')) {
    const saggio15 = Array.from(generalArchive.querySelectorAll('[data-archive-item]')).find((item) => item.querySelector('h3')?.textContent.trim().startsWith('15 —'));
    const entry = `<article class="item" data-archive-item data-category="saggi" data-saggio-16 data-essay-number="16"><div><h3>16 — La pace senza forma</h3><p class="meta">4 agosto 2026 · Saggio integrale · Archivio locale</p><p>Un saggio sulla costruzione di una sovranità strategica europea capace di legare forza, legittimità e pace.</p></div><div class="actions"><a class="btn-secondary" href="${essayUrl}">Leggi il saggio</a></div></article>`;
    if (saggio15) {
      saggio15.insertAdjacentHTML('beforebegin', entry);
    } else {
      generalArchive.insertAdjacentHTML('afterbegin', entry);
    }
    sortNumberedArchiveEssays(generalArchive);
  }
})();
