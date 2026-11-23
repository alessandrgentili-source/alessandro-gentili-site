import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import vm from 'node:vm';

const source = await readFile(new URL('../assets/script.js', import.meta.url), 'utf8');
const consent = source.slice(source.indexOf('const cookieConsentKey'), source.indexOf('const bilingualPairs'));
const key = 'ag_cookie_statistics';
const disabled = 'ga-disable-G-NCN48MN7VJ';

function session(initial = null, storageBlocked = false, pathname = '/contatti.html') {
  let preference = initial;
  const buttons = {};
  const listeners = {};
  const scripts = [];
  const expiredCookies = [];
  const window = {
    location: { hostname: 'alessandro-gentili.it', origin: 'https://alessandro-gentili.it', pathname },
    addEventListener: (name, callback) => { listeners[name] = callback; },
    localStorage: {
      getItem: () => { if (storageBlocked) throw Error('blocked'); return preference; },
      setItem: (_, value) => { if (storageBlocked) throw Error('blocked'); preference = value; },
    },
  };
  const document = {
    documentElement: { lang: 'it' },
    addEventListener: (name, callback) => { listeners[name] = callback; },
    querySelector: () => null,
    head: { appendChild: script => scripts.push(script) },
    body: { appendChild() {} },
    set cookie(value) { expiredCookies.push(value); },
    createElement: tag => tag === 'script' ? {} : {
      dataset: {}, setAttribute() {},
      querySelector: selector => ({ addEventListener: (_, callback) => { buttons[selector] = callback; } }),
    },
  };
  vm.runInNewContext(consent, { window, document });
  const click = choice => { window.openCookiePreferences(); buttons[`[data-cookie-${choice}]`](); };
  const activateLink = (href, defaultPrevented = false) => listeners.click?.({
    defaultPrevented,
    target: { closest: () => href ? { getAttribute: () => href } : null },
  });
  const events = () => JSON.parse(JSON.stringify(
    (window.dataLayer ?? []).filter(args => args[0] === 'event').map(args => Array.from(args)),
  ));
  return { window, scripts, expiredCookies, listeners, click, activateLink, events, preference: () => preference };
}

const emailLink = 'mailto:contatti@alessandro-gentili.it?subject=private';
const brevoLink = 'https://12110d84.sibforms.com/serve/test?EMAIL=reader%40example.com';
const expectedEvent = (name, path) => ['event', name, {
  send_to: 'G-NCN48MN7VJ', page_location: `https://alessandro-gentili.it${path}`, page_referrer: '',
}];

for (const initial of [null, 'rejected']) {
  const s = session(initial);
  assert.equal(s.scripts.length, 0, 'No Google request before consent');
  assert.equal(s.window[disabled], true);
  s.activateLink(emailLink);
  s.activateLink(brevoLink);
  assert.deepEqual(s.events(), []);
}
for (const blocked of [false, true]) {
  const s = session(null, blocked);
  s.click('accept');
  assert.equal(s.scripts.length, 1);
  assert.equal(s.window[disabled], false);
  s.activateLink(emailLink);
  s.activateLink(brevoLink);
  assert.deepEqual(s.events(), [
    expectedEvent('contact_email_click', '/contatti.html'),
    expectedEvent('newsletter_brevo_click', '/contatti.html'),
  ]);
  // Revoke while the external script could still be loading.
  s.click('reject');
  assert.equal(s.window[disabled], true);
  assert.equal(s.window.dataLayer.at(-1)[2].analytics_storage, 'denied');
  assert(s.expiredCookies.some(value => value.startsWith('_ga=;')));
  assert(s.expiredCookies.some(value => value.startsWith('_ga_NCN48MN7VJ=;')));
  s.activateLink(emailLink);
  s.activateLink(brevoLink);
  assert.equal(s.events().length, 2);
  if (!blocked) assert.equal(s.preference(), 'rejected');
  s.click('accept');
  assert.equal(s.window[disabled], false);
  assert.equal(s.scripts.length, 1, 'Reacceptance must not inject another tag');
  assert.equal(s.window.dataLayer.filter(args => args[0] === 'config').length, 1);
  s.activateLink(brevoLink);
  assert.equal(s.events().length, 3);
  s.listeners.storage({ key, newValue: 'rejected' });
  assert.equal(s.window[disabled], true, 'Cross-tab revocation');
  s.activateLink(emailLink);
  assert.equal(s.events().length, 3);
}
const returning = session('accepted');
assert.equal(returning.scripts.length, 1);
for (const unrelated of [
  null, '/en/contact/', 'mailto:lettera@alessandro-gentili.it',
  'mailto:contatti@alessandro-gentili.it.example.com', 'https://12110d84.sibforms.com.example.com/serve/test',
]) {
  returning.activateLink(unrelated);
}
returning.activateLink(emailLink, true);
assert.deepEqual(returning.events(), []);
returning.click('reject');
assert.equal(returning.window[disabled], true);

for (const path of ['/en/contact/', '/en/contact/index.html']) {
  const english = session('accepted', false, path);
  english.activateLink(emailLink);
  assert.deepEqual(english.events(), [expectedEvent('contact_email_click', '/en/contact/')]);
}
const home = session('accepted', false, '/');
home.activateLink(emailLink);
assert.deepEqual(home.events(), []);
console.log('Consent and contact event checks passed. No network requests made.');
