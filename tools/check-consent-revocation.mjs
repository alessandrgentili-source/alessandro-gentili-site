import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import vm from 'node:vm';

const source = await readFile(new URL('../assets/script.js', import.meta.url), 'utf8');
const consent = source.slice(source.indexOf('const cookieConsentKey'), source.indexOf('const bilingualPairs'));
const key = 'ag_cookie_statistics';
const disabled = 'ga-disable-G-NCN48MN7VJ';

function session(initial = null, storageBlocked = false) {
  let preference = initial;
  const buttons = {};
  const listeners = {};
  const scripts = [];
  const expiredCookies = [];
  const window = {
    location: { hostname: 'alessandro-gentili.it' },
    addEventListener: (name, callback) => { listeners[name] = callback; },
    localStorage: {
      getItem: () => { if (storageBlocked) throw Error('blocked'); return preference; },
      setItem: (_, value) => { if (storageBlocked) throw Error('blocked'); preference = value; },
    },
  };
  const document = {
    documentElement: { lang: 'it' },
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
  return { window, scripts, expiredCookies, listeners, click, preference: () => preference };
}

for (const initial of [null, 'rejected']) {
  const s = session(initial);
  assert.equal(s.scripts.length, 0, 'No Google request before consent');
  assert.equal(s.window[disabled], true);
}
for (const blocked of [false, true]) {
  const s = session(null, blocked);
  s.click('accept');
  assert.equal(s.scripts.length, 1);
  assert.equal(s.window[disabled], false);
  // Revoke while the external script could still be loading.
  s.click('reject');
  assert.equal(s.window[disabled], true);
  assert.equal(s.window.dataLayer.at(-1)[2].analytics_storage, 'denied');
  assert(s.expiredCookies.some(value => value.startsWith('_ga=;')));
  assert(s.expiredCookies.some(value => value.startsWith('_ga_NCN48MN7VJ=;')));
  if (!blocked) assert.equal(s.preference(), 'rejected');
  s.click('accept');
  assert.equal(s.window[disabled], false);
  assert.equal(s.scripts.length, 1, 'Reacceptance must not inject another tag');
  assert.equal(s.window.dataLayer.filter(args => args[0] === 'config').length, 1);
  s.listeners.storage({ key, newValue: 'rejected' });
  assert.equal(s.window[disabled], true, 'Cross-tab revocation');
}
const returning = session('accepted');
assert.equal(returning.scripts.length, 1);
returning.click('reject');
assert.equal(returning.window[disabled], true);
console.log('Consent checks passed: initial denial, accept/revoke/reaccept, delayed tag, blocked storage, cross-tab revocation. No network requests made.');
