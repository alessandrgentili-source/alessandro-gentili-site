const mobileNavQuery = window.matchMedia('(max-width: 760px)');
const dropdownNavItems = document.querySelectorAll('.primary-nav-item--dropdown');
document.documentElement.classList.add('nav-enhanced');

const setPrimaryNavState = (item, open) => {
  item.classList.toggle('is-open', open);
  item.querySelector('.primary-nav-link')?.setAttribute('aria-expanded', String(open));
};
const closePrimaryNavDropdowns = (exceptItem) => {
  dropdownNavItems.forEach(item => { if (item !== exceptItem) setPrimaryNavState(item, false); });
};
dropdownNavItems.forEach((item, index) => {
  const trigger = item.querySelector('.primary-nav-link');
  const submenu = item.querySelector('.primary-nav-dropdown');
  if (!trigger || !submenu) return;
  submenu.id ||= `primary-submenu-${index}`;
  trigger.setAttribute('aria-controls', submenu.id);
  // This is a disclosure containing ordinary navigation links, not an ARIA menu widget.
  trigger.removeAttribute('aria-haspopup');
  setPrimaryNavState(item, false);
  const open = () => { closePrimaryNavDropdowns(item); setPrimaryNavState(item, true); };
  item.addEventListener('mouseenter', () => { if (!mobileNavQuery.matches) open(); });
  item.addEventListener('mouseleave', () => {
    if (!mobileNavQuery.matches && !item.contains(document.activeElement)) setPrimaryNavState(item, false);
  });
  item.addEventListener('focusin', () => { if (!mobileNavQuery.matches) open(); });
  item.addEventListener('focusout', (event) => {
    if (!item.contains(event.relatedTarget)) setPrimaryNavState(item, false);
  });
  trigger.addEventListener('click', (event) => {
    if (!mobileNavQuery.matches) return;
    event.preventDefault();
    const wasOpen = item.classList.contains('is-open');
    closePrimaryNavDropdowns();
    setPrimaryNavState(item, !wasOpen);
  });
  trigger.addEventListener('keydown', (event) => {
    if (event.key !== 'ArrowDown' && event.key !== ' ') return;
    event.preventDefault();
    open();
    submenu.querySelector('a')?.focus();
  });
});
document.addEventListener('click', (event) => {
  if (!event.target.closest('.primary-nav')) closePrimaryNavDropdowns();
});
document.addEventListener('keydown', (event) => {
  if (event.key !== 'Escape') return;
  const item = document.activeElement?.closest('.primary-nav-item--dropdown');
  // Focus first: focusin may open the dropdown, which is then closed below.
  if (item?.classList.contains('is-open')) item.querySelector('.primary-nav-link')?.focus();
  closePrimaryNavDropdowns();
});
mobileNavQuery.addEventListener('change', () => closePrimaryNavDropdowns());

const mainContent = document.querySelector('main');
if (mainContent) {
  mainContent.id ||= 'main-content';
  mainContent.setAttribute('tabindex', '-1');
  const skip = document.createElement('a');
  skip.className = 'skip-link';
  skip.href = `#${mainContent.id}`;
  skip.textContent = document.documentElement.lang.startsWith('en') ? 'Skip to content' : 'Salta al contenuto';
  skip.addEventListener('click', () => mainContent.focus({ preventScroll: true }));
  document.body.prepend(skip);
}
const siteHeader = document.querySelector('.site-header');
if (siteHeader) {
  const measureHeader = () => document.documentElement.style.setProperty('--site-header-height', `${Math.ceil(siteHeader.getBoundingClientRect().height)}px`);
  measureHeader();
  if ('ResizeObserver' in window) new ResizeObserver(measureHeader).observe(siteHeader);
  else window.addEventListener('resize', measureHeader);
}
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
// Disable collection until this page has an explicit statistics opt-in.
window[`ga-disable-${googleAnalyticsId}`] = true;

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
  window[`ga-disable-${googleAnalyticsId}`] = false;
  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function gtag(){window.dataLayer.push(arguments);};
  window.gtag('consent', 'update', { analytics_storage: 'granted' });
  if (googleAnalyticsLoaded) return;

  window.gtag('js', new Date());
  window.gtag('config', googleAnalyticsId);
  const analyticsScript = document.createElement('script');
  analyticsScript.async = true;
  analyticsScript.src = `https://www.googletagmanager.com/gtag/js?id=${googleAnalyticsId}`;
  document.head.appendChild(analyticsScript);
  googleAnalyticsLoaded = true;
};

const disableGoogleAnalytics = () => {
  // The opt-out flag also blocks a tag that finishes loading after revocation.
  // Already transmitted requests cannot be recalled; removing the script is not an opt-out.
  window[`ga-disable-${googleAnalyticsId}`] = true;
  window.gtag?.('consent', 'update', { analytics_storage: 'denied' });
  const domains = ['', window.location.hostname, 'alessandro-gentili.it'];
  for (const name of ['_ga', `_ga_${googleAnalyticsId.slice(2)}`]) {
    for (const domain of new Set(domains)) {
      document.cookie = `${name}=; Max-Age=0; path=/; SameSite=Lax${domain ? `; domain=${domain}` : ''}`;
    }
  }
};

// Apply revocation in other open pages without waiting for navigation.
window.addEventListener('storage', (event) => {
  if ((event.key === cookieConsentKey && event.newValue !== 'accepted') || event.key === null) {
    disableGoogleAnalytics();
  }
});

const closeCookieBanner = () => {
  document.querySelector('[data-cookie-banner]')?.remove();
};

const showCookieBanner = () => {
  closeCookieBanner();

  const isEnglishPage = document.documentElement.lang.toLowerCase().startsWith('en');
  const copy = isEnglishPage
    ? {
        ariaLabel: 'Cookie preferences',
        message: 'We use necessary technical cookies and, only with your consent, statistical tools to understand how the site is read and improve its content.',
        reject: 'Reject',
        accept: 'Accept statistics',
      }
    : {
        ariaLabel: 'Preferenze cookie',
        message: 'Usiamo cookie tecnici necessari e, solo con il tuo consenso, strumenti statistici per capire come viene letto il sito e migliorare i contenuti.',
        reject: 'Rifiuta',
        accept: 'Accetta statistiche',
      };

  const banner = document.createElement('section');
  banner.className = 'cookie-banner';
  banner.dataset.cookieBanner = '';
  banner.setAttribute('aria-label', copy.ariaLabel);
  banner.innerHTML = `
    <div class="cookie-banner-copy">
      <p>${copy.message}</p>
      <a href="/privacy.html">Privacy</a>
    </div>
    <div class="cookie-banner-actions">
      <button type="button" class="btn-secondary" data-cookie-reject>${copy.reject}</button>
      <button type="button" class="btn" data-cookie-accept>${copy.accept}</button>
    </div>
  `;

  banner.querySelector('[data-cookie-accept]')?.addEventListener('click', () => {
    setCookieStatisticsPreference('accepted');
    loadGoogleAnalytics();
    closeCookieBanner();
  });

  banner.querySelector('[data-cookie-reject]')?.addEventListener('click', () => {
    setCookieStatisticsPreference('rejected');
    disableGoogleAnalytics();
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
  "/cerchi/guide/freud-inconscio-desiderio-civilta/": { it: "/cerchi/guide/freud-inconscio-desiderio-civilta/", en: "/en/cerchi/guides/sigmund-freud-unconscious-desire-civilization/" },
  "/cerchi/guide/gramsci-egemonia-cultura-senso-comune/": { it: "/cerchi/guide/gramsci-egemonia-cultura-senso-comune/", en: "/en/cerchi/guides/antonio-gramsci-hegemony-culture-common-sense/" },
  "/cerchi/guide/hobbes-paura-sovranita-ordine-politico/": { it: "/cerchi/guide/hobbes-paura-sovranita-ordine-politico/", en: "/en/cerchi/guides/thomas-hobbes-fear-sovereignty-political-order/" },
  "/cerchi/guide/averroe-ragione-interpretazione-legge/": { it: "/cerchi/guide/averroe-ragione-interpretazione-legge/", en: "/en/cerchi/guides/averroes-reason-interpretation-law/" },
  "/cerchi/guide/simmel-denaro-metropoli-individualita/": { it: "/cerchi/guide/simmel-denaro-metropoli-individualita/", en: "/en/cerchi/guides/georg-simmel-money-metropolis-individuality/" },
  "/cerchi/guide/adam-smith-scambio-simpatia-ricchezza/": { it: "/cerchi/guide/adam-smith-scambio-simpatia-ricchezza/", en: "/en/cerchi/guides/adam-smith-exchange-sympathy-wealth/" },
  "/cerchi/guide/cicerone-repubblica-legge-parola-civile/": { it: "/cerchi/guide/cicerone-repubblica-legge-parola-civile/", en: "/en/cerchi/guides/cicero-republic-law-civic-speech/" },
  "/cerchi/guide/alexis-de-tocqueville-democrazia-opinione-liberta/": { it: "/cerchi/guide/alexis-de-tocqueville-democrazia-opinione-liberta/", en: "/en/cerchi/guides/alexis-de-tocqueville-democracy-opinion-liberty/" },
  "/cerchi/guide/nicolas-de-condorcet-istruzione-progresso-decisione/": { it: "/cerchi/guide/nicolas-de-condorcet-istruzione-progresso-decisione/", en: "/en/cerchi/guides/nicolas-de-condorcet-education-progress-decision/" },
  "/cerchi/guide/polibio-costituzione-potenza-decadenza/": { it: "/cerchi/guide/polibio-costituzione-potenza-decadenza/", en: "/en/cerchi/guides/polybius-constitution-power-decline/" },
  "/cerchi/guide/gaetano-mosca-classe-politica-organizzazione-governo-reale/": { it: "/cerchi/guide/gaetano-mosca-classe-politica-organizzazione-governo-reale/", en: "/en/cerchi/guides/gaetano-mosca-political-class-organization-real-government/" },
  "/cerchi/guide/vilfredo-pareto-elite-residui-circolazione/": { it: "/cerchi/guide/vilfredo-pareto-elite-residui-circolazione/", en: "/en/cerchi/guides/vilfredo-pareto-elites-residues-circulation/" },
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
  "/en/cerchi/guides/sigmund-freud-unconscious-desire-civilization/": { it: "/cerchi/guide/freud-inconscio-desiderio-civilta/", en: "/en/cerchi/guides/sigmund-freud-unconscious-desire-civilization/" },
  "/en/cerchi/guides/antonio-gramsci-hegemony-culture-common-sense/": { it: "/cerchi/guide/gramsci-egemonia-cultura-senso-comune/", en: "/en/cerchi/guides/antonio-gramsci-hegemony-culture-common-sense/" },
  "/en/cerchi/guides/thomas-hobbes-fear-sovereignty-political-order/": { it: "/cerchi/guide/hobbes-paura-sovranita-ordine-politico/", en: "/en/cerchi/guides/thomas-hobbes-fear-sovereignty-political-order/" },
  "/en/cerchi/guides/averroes-reason-interpretation-law/": { it: "/cerchi/guide/averroe-ragione-interpretazione-legge/", en: "/en/cerchi/guides/averroes-reason-interpretation-law/" },
  "/en/cerchi/guides/georg-simmel-money-metropolis-individuality/": { it: "/cerchi/guide/simmel-denaro-metropoli-individualita/", en: "/en/cerchi/guides/georg-simmel-money-metropolis-individuality/" },
  "/en/cerchi/guides/adam-smith-exchange-sympathy-wealth/": { it: "/cerchi/guide/adam-smith-scambio-simpatia-ricchezza/", en: "/en/cerchi/guides/adam-smith-exchange-sympathy-wealth/" },
  "/en/cerchi/guides/cicero-republic-law-civic-speech/": { it: "/cerchi/guide/cicerone-repubblica-legge-parola-civile/", en: "/en/cerchi/guides/cicero-republic-law-civic-speech/" },
  "/en/cerchi/guides/alexis-de-tocqueville-democracy-opinion-liberty/": { it: "/cerchi/guide/alexis-de-tocqueville-democrazia-opinione-liberta/", en: "/en/cerchi/guides/alexis-de-tocqueville-democracy-opinion-liberty/" },
  "/en/cerchi/guides/nicolas-de-condorcet-education-progress-decision/": { it: "/cerchi/guide/nicolas-de-condorcet-istruzione-progresso-decisione/", en: "/en/cerchi/guides/nicolas-de-condorcet-education-progress-decision/" },
  "/en/cerchi/guides/polybius-constitution-power-decline/": { it: "/cerchi/guide/polibio-costituzione-potenza-decadenza/", en: "/en/cerchi/guides/polybius-constitution-power-decline/" },
  "/en/cerchi/guides/gaetano-mosca-political-class-organization-real-government/": { it: "/cerchi/guide/gaetano-mosca-classe-politica-organizzazione-governo-reale/", en: "/en/cerchi/guides/gaetano-mosca-political-class-organization-real-government/" },
  "/en/cerchi/guides/vilfredo-pareto-elites-residues-circulation/": { it: "/cerchi/guide/vilfredo-pareto-elite-residui-circolazione/", en: "/en/cerchi/guides/vilfredo-pareto-elites-residues-circulation/" },
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
