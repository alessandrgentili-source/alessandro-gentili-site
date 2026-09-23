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


const bilingualPairs = {
  "/": { it: "/", en: "/en/" },
  "/cerchi/": { it: "/cerchi/", en: "/en/cerchi/" },
  "/cerchi/triadi/": { it: "/cerchi/triadi/", en: "/en/cerchi/triads/" },
  "/temi/": { it: "/temi/", en: "/en/themes/" },
  "/cerchi/guide/alessandro-manzoni-lingua-storia-responsabilita/": { it: "/cerchi/guide/alessandro-manzoni-lingua-storia-responsabilita/", en: "/en/cerchi/guides/alessandro-manzoni-language-history-responsibility/" },
  "/cerchi/guide/carlo-collodi-formazione-prova-mondo/": { it: "/cerchi/guide/carlo-collodi-formazione-prova-mondo/", en: "/en/cerchi/guides/carlo-collodi-pinocchio-education-desire-judgment/" },
  "/cerchi/guide/pier-paolo-pasolini-mutazione-antropologica-omologazione/": { it: "/cerchi/guide/pier-paolo-pasolini-mutazione-antropologica-omologazione/", en: "/en/cerchi/guides/pier-paolo-pasolini-anthropological-mutation-consumer-culture/" },
  "/cerchi/guide/platone-vita-opere-pensiero/": { it: "/cerchi/guide/platone-vita-opere-pensiero/", en: "/en/cerchi/guides/plato-ideas-truth-power/" },
  "/cerchi/guide/dante-vita-opere-commedia-esilio/": { it: "/cerchi/guide/dante-vita-opere-commedia-esilio/", en: "/en/cerchi/guides/dante-exile-language-divine-comedy/" },
  "/cerchi/guide/machiavelli-vita-opere-pensiero-politico/": { it: "/cerchi/guide/machiavelli-vita-opere-pensiero-politico/", en: "/en/cerchi/guides/machiavelli-power-state-effectual-truth/" },
  "/cerchi/guide/marx-vita-opere-pensiero/": { it: "/cerchi/guide/marx-vita-opere-pensiero/", en: "/en/cerchi/guides/karl-marx-capital-labor-alienation/" },
  "/cerchi/guide/nietzsche-vita-opere-pensiero/": { it: "/cerchi/guide/nietzsche-vita-opere-pensiero/", en: "/en/cerchi/guides/friedrich-nietzsche-nihilism-values-death-of-god/" },
  "/cerchi/guide/leopardi-desiderio-infinito-modernita/": { it: "/cerchi/guide/leopardi-desiderio-infinito-modernita/", en: "/en/cerchi/guides/giacomo-leopardi-desire-infinity-modernity/" },
  "/cerchi/guide/seneca-dominio-tempo-morte/": { it: "/cerchi/guide/seneca-dominio-tempo-morte/", en: "/en/cerchi/guides/seneca-time-self-mastery-death/" },
  "/cerchi/guide/aristotele-forma-fine-realta/": { it: "/cerchi/guide/aristotele-forma-fine-realta/", en: "/en/cerchi/guides/aristotle-form-purpose-actuality/" },
  "/cerchi/guide/weber-razionalizzazione-potere-disincanto/": { it: "/cerchi/guide/weber-razionalizzazione-potere-disincanto/", en: "/en/cerchi/guides/max-weber-rationalization-power-disenchantment/" },
  "/en/": { it: "/", en: "/en/" },
  "/en/cerchi/": { it: "/cerchi/", en: "/en/cerchi/" },
  "/en/cerchi/triads/": { it: "/cerchi/triadi/", en: "/en/cerchi/triads/" },
  "/en/themes/": { it: "/temi/", en: "/en/themes/" },
  "/en/cerchi/guides/alessandro-manzoni-language-history-responsibility/": { it: "/cerchi/guide/alessandro-manzoni-lingua-storia-responsabilita/", en: "/en/cerchi/guides/alessandro-manzoni-language-history-responsibility/" },
  "/en/cerchi/guides/carlo-collodi-pinocchio-education-desire-judgment/": { it: "/cerchi/guide/carlo-collodi-formazione-prova-mondo/", en: "/en/cerchi/guides/carlo-collodi-pinocchio-education-desire-judgment/" },
  "/en/cerchi/guides/pier-paolo-pasolini-anthropological-mutation-consumer-culture/": { it: "/cerchi/guide/pier-paolo-pasolini-mutazione-antropologica-omologazione/", en: "/en/cerchi/guides/pier-paolo-pasolini-anthropological-mutation-consumer-culture/" },
  "/en/cerchi/guides/plato-ideas-truth-power/": { it: "/cerchi/guide/platone-vita-opere-pensiero/", en: "/en/cerchi/guides/plato-ideas-truth-power/" },
  "/en/cerchi/guides/dante-exile-language-divine-comedy/": { it: "/cerchi/guide/dante-vita-opere-commedia-esilio/", en: "/en/cerchi/guides/dante-exile-language-divine-comedy/" },
  "/en/cerchi/guides/machiavelli-power-state-effectual-truth/": { it: "/cerchi/guide/machiavelli-vita-opere-pensiero-politico/", en: "/en/cerchi/guides/machiavelli-power-state-effectual-truth/" },
  "/en/cerchi/guides/karl-marx-capital-labor-alienation/": { it: "/cerchi/guide/marx-vita-opere-pensiero/", en: "/en/cerchi/guides/karl-marx-capital-labor-alienation/" },
  "/en/cerchi/guides/friedrich-nietzsche-nihilism-values-death-of-god/": { it: "/cerchi/guide/nietzsche-vita-opere-pensiero/", en: "/en/cerchi/guides/friedrich-nietzsche-nihilism-values-death-of-god/" },
  "/en/cerchi/guides/giacomo-leopardi-desire-infinity-modernity/": { it: "/cerchi/guide/leopardi-desiderio-infinito-modernita/", en: "/en/cerchi/guides/giacomo-leopardi-desire-infinity-modernity/" },
  "/en/cerchi/guides/seneca-time-self-mastery-death/": { it: "/cerchi/guide/seneca-dominio-tempo-morte/", en: "/en/cerchi/guides/seneca-time-self-mastery-death/" },
  "/en/cerchi/guides/aristotle-form-purpose-actuality/": { it: "/cerchi/guide/aristotele-forma-fine-realta/", en: "/en/cerchi/guides/aristotle-form-purpose-actuality/" },
  "/en/cerchi/guides/max-weber-rationalization-power-disenchantment/": { it: "/cerchi/guide/weber-razionalizzazione-potere-disincanto/", en: "/en/cerchi/guides/max-weber-rationalization-power-disenchantment/" },
  "/en.html": { it: "/", en: "/en/positioning/" },
  "/metodo-ai.html": { it: "/", en: "/en/method/" },
  "/strumenti.html": { it: "/", en: "/en/system/" }
};

const normalizeLanguagePath = (pathname) => pathname.replace(/\/index\.html$/, "/") || "/";
const currentLanguagePath = normalizeLanguagePath(window.location.pathname);
const isEnglishPath = currentLanguagePath.startsWith("/en/");
const explicitLanguagePair = bilingualPairs[currentLanguagePath];
const languageTargets = explicitLanguagePair || (isEnglishPath
  ? { it: "/", en: currentLanguagePath }
  : { it: currentLanguagePath, en: "/en/" });

document.querySelectorAll('.primary-nav a, .footer-nav a').forEach((link) => {
  const raw = link.getAttribute('href');
  if (!raw || /^(?:https?:|mailto:|tel:|#)/.test(raw)) return;
  const path = normalizeLanguagePath(new URL(raw, window.location.href).pathname);
  const migration = {
    "/en.html": "/en/positioning/",
    "/metodo-ai.html": "/en/method/",
    "/strumenti.html": "/en/system/"
  }[path];
  if (migration) link.setAttribute('href', migration);
});

const primaryNavList = document.querySelector('.primary-nav-list');
if (primaryNavList && !primaryNavList.querySelector('[data-language-switcher]')) {
  const item = document.createElement('li');
  item.className = 'primary-nav-item language-switcher';
  item.dataset.languageSwitcher = '';
  item.setAttribute('aria-label', 'Language');
  item.innerHTML = `<a class="language-switcher-link${document.documentElement.lang.startsWith('it') ? ' active' : ''}" href="${languageTargets.it}" lang="it" hreflang="it">IT</a><span aria-hidden="true">|</span><a class="language-switcher-link${document.documentElement.lang.startsWith('en') ? ' active' : ''}" href="${languageTargets.en}" lang="en" hreflang="en">EN</a>`;
  if (!explicitLanguagePair && !isEnglishPath) {
    item.querySelector('a[lang="en"]')?.setAttribute('title', 'English home — this page does not have an English edition yet');
  }
  primaryNavList.appendChild(item);
}
