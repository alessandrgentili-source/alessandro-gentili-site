import { readFile, access } from 'node:fs/promises';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = fileURLToPath(new URL('../', import.meta.url));
const base = 'https://alessandro-gentili.it';

const assert = (condition, message) => {
  if (!condition) throw new Error(message);
};
const read = (path) => readFile(join(root, path), 'utf8');

const pages = [
  { path: 'en/index.html', url: `${base}/en/`, it: `${base}/`, type: 'WebSite' },
  { path: 'en/cerchi/index.html', url: `${base}/en/cerchi/`, it: `${base}/cerchi/`, type: 'CollectionPage' },
  { path: 'en/cerchi/triads/index.html', url: `${base}/en/cerchi/triads/`, it: `${base}/cerchi/triadi/`, type: 'CollectionPage' },
  { path: 'en/themes/index.html', url: `${base}/en/themes/`, it: `${base}/temi/`, type: 'CollectionPage' },
  { path: 'en/positioning/index.html', url: `${base}/en/positioning/`, type: 'ProfilePage' },
  { path: 'en/method/index.html', url: `${base}/en/method/`, type: 'WebPage' },
  { path: 'en/system/index.html', url: `${base}/en/system/`, type: 'WebPage' },
  { path: 'en/cerchi/guides/alessandro-manzoni-language-history-responsibility/index.html', url: `${base}/en/cerchi/guides/alessandro-manzoni-language-history-responsibility/`, it: `${base}/cerchi/guide/alessandro-manzoni-lingua-storia-responsabilita/`, type: 'Article', breadcrumb: true },
  { path: 'en/cerchi/guides/carlo-collodi-pinocchio-education-desire-judgment/index.html', url: `${base}/en/cerchi/guides/carlo-collodi-pinocchio-education-desire-judgment/`, it: `${base}/cerchi/guide/carlo-collodi-formazione-prova-mondo/`, type: 'Article', breadcrumb: true },
  { path: 'en/cerchi/guides/pier-paolo-pasolini-anthropological-mutation-consumer-culture/index.html', url: `${base}/en/cerchi/guides/pier-paolo-pasolini-anthropological-mutation-consumer-culture/`, it: `${base}/cerchi/guide/pier-paolo-pasolini-mutazione-antropologica-omologazione/`, type: 'Article', breadcrumb: true },
  { path: 'en/cerchi/guides/plato-ideas-truth-power/index.html', url: `${base}/en/cerchi/guides/plato-ideas-truth-power/`, it: `${base}/cerchi/guide/platone-vita-opere-pensiero/`, type: 'Article', breadcrumb: true },
  { path: 'en/cerchi/guides/dante-exile-language-divine-comedy/index.html', url: `${base}/en/cerchi/guides/dante-exile-language-divine-comedy/`, it: `${base}/cerchi/guide/dante-vita-opere-commedia-esilio/`, type: 'Article', breadcrumb: true },
  { path: 'en/cerchi/guides/machiavelli-power-state-effectual-truth/index.html', url: `${base}/en/cerchi/guides/machiavelli-power-state-effectual-truth/`, it: `${base}/cerchi/guide/machiavelli-vita-opere-pensiero-politico/`, type: 'Article', breadcrumb: true },
  { path: 'en/cerchi/guides/karl-marx-capital-labor-alienation/index.html', url: `${base}/en/cerchi/guides/karl-marx-capital-labor-alienation/`, it: `${base}/cerchi/guide/marx-vita-opere-pensiero/`, type: 'Article', breadcrumb: true },
  { path: 'en/cerchi/guides/friedrich-nietzsche-nihilism-values-death-of-god/index.html', url: `${base}/en/cerchi/guides/friedrich-nietzsche-nihilism-values-death-of-god/`, it: `${base}/cerchi/guide/nietzsche-vita-opere-pensiero/`, type: 'Article', breadcrumb: true },
  { path: 'en/cerchi/guides/giacomo-leopardi-desire-infinity-modernity/index.html', url: `${base}/en/cerchi/guides/giacomo-leopardi-desire-infinity-modernity/`, it: `${base}/cerchi/guide/leopardi-desiderio-infinito-modernita/`, type: 'Article', breadcrumb: true }
];

const italianPairs = [
  { path: 'index.html', it: `${base}/`, en: `${base}/en/` },
  { path: 'cerchi/index.html', it: `${base}/cerchi/`, en: `${base}/en/cerchi/` },
  { path: 'cerchi/triadi/index.html', it: `${base}/cerchi/triadi/`, en: `${base}/en/cerchi/triads/` },
  { path: 'temi/index.html', it: `${base}/temi/`, en: `${base}/en/themes/` },
  { path: 'cerchi/guide/alessandro-manzoni-lingua-storia-responsabilita/index.html', it: `${base}/cerchi/guide/alessandro-manzoni-lingua-storia-responsabilita/`, en: `${base}/en/cerchi/guides/alessandro-manzoni-language-history-responsibility/` },
  { path: 'cerchi/guide/carlo-collodi-formazione-prova-mondo/index.html', it: `${base}/cerchi/guide/carlo-collodi-formazione-prova-mondo/`, en: `${base}/en/cerchi/guides/carlo-collodi-pinocchio-education-desire-judgment/` },
  { path: 'cerchi/guide/pier-paolo-pasolini-mutazione-antropologica-omologazione/index.html', it: `${base}/cerchi/guide/pier-paolo-pasolini-mutazione-antropologica-omologazione/`, en: `${base}/en/cerchi/guides/pier-paolo-pasolini-anthropological-mutation-consumer-culture/` },
  { path: 'cerchi/guide/platone-vita-opere-pensiero/index.html', it: `${base}/cerchi/guide/platone-vita-opere-pensiero/`, en: `${base}/en/cerchi/guides/plato-ideas-truth-power/` },
  { path: 'cerchi/guide/dante-vita-opere-commedia-esilio/index.html', it: `${base}/cerchi/guide/dante-vita-opere-commedia-esilio/`, en: `${base}/en/cerchi/guides/dante-exile-language-divine-comedy/` },
  { path: 'cerchi/guide/machiavelli-vita-opere-pensiero-politico/index.html', it: `${base}/cerchi/guide/machiavelli-vita-opere-pensiero-politico/`, en: `${base}/en/cerchi/guides/machiavelli-power-state-effectual-truth/` },
  { path: 'cerchi/guide/marx-vita-opere-pensiero/index.html', it: `${base}/cerchi/guide/marx-vita-opere-pensiero/`, en: `${base}/en/cerchi/guides/karl-marx-capital-labor-alienation/` },
  { path: 'cerchi/guide/nietzsche-vita-opere-pensiero/index.html', it: `${base}/cerchi/guide/nietzsche-vita-opere-pensiero/`, en: `${base}/en/cerchi/guides/friedrich-nietzsche-nihilism-values-death-of-god/` },
  { path: 'cerchi/guide/leopardi-desiderio-infinito-modernita/index.html', it: `${base}/cerchi/guide/leopardi-desiderio-infinito-modernita/`, en: `${base}/en/cerchi/guides/giacomo-leopardi-desire-infinity-modernity/` }
];

const extractJsonLd = (html, path) => {
  const blocks = [...html.matchAll(/<script\s+type="application\/ld\+json">([\s\S]*?)<\/script>/g)]
    .map((match) => match[1].trim());
  assert(blocks.length > 0, `${path}: missing JSON-LD`);
  return blocks.map((block, index) => {
    try {
      return JSON.parse(block);
    } catch (error) {
      throw new Error(`${path}: invalid JSON-LD block ${index + 1}: ${error.message}`);
    }
  });
};

for (const page of pages) {
  await access(join(root, page.path));
  const html = await read(page.path);
  assert(/<html\s+lang="en"/.test(html), `${page.path}: html lang must be en`);
  assert(html.includes(`<link rel="canonical" href="${page.url}" />`), `${page.path}: wrong or missing self canonical`);
  assert(!/<meta\s+name="robots"\s+content="[^"]*noindex/i.test(html), `${page.path}: canonical English page must be indexable`);
  assert(html.includes('<meta name="description"'), `${page.path}: missing meta description`);
  assert(html.includes('<meta property="og:title"'), `${page.path}: missing Open Graph title`);
  assert(html.includes('<meta property="og:url"'), `${page.path}: missing Open Graph URL`);
  assert(html.includes('<meta name="twitter:card"'), `${page.path}: missing Twitter card`);

  if (page.it) {
    assert(html.includes(`hreflang="it" href="${page.it}"`), `${page.path}: missing Italian hreflang`);
    assert(html.includes(`hreflang="en" href="${page.url}"`), `${page.path}: missing English hreflang`);
    assert(html.includes(`hreflang="x-default" href="${page.it}"`), `${page.path}: x-default must point to Italian canonical`);
  }

  const jsonLd = extractJsonLd(html, page.path);
  assert(jsonLd.some((node) => node['@type'] === page.type), `${page.path}: expected JSON-LD type ${page.type}`);
  assert(jsonLd.some((node) => node.inLanguage === 'en'), `${page.path}: at least one JSON-LD node must declare inLanguage=en`);
  if (page.breadcrumb) {
    assert(jsonLd.some((node) => node['@type'] === 'BreadcrumbList'), `${page.path}: missing BreadcrumbList`);
  }
}

for (const pair of italianPairs) {
  const html = await read(pair.path);
  assert(/<html\s+lang="it"/.test(html), `${pair.path}: Italian pair must keep lang=it`);
  assert(html.includes(`<link rel="canonical" href="${pair.it}" />`), `${pair.path}: Italian canonical changed unexpectedly`);
  assert(html.includes(`hreflang="it" href="${pair.it}"`), `${pair.path}: missing self Italian hreflang`);
  assert(html.includes(`hreflang="en" href="${pair.en}"`), `${pair.path}: missing reciprocal English hreflang`);
  assert(html.includes(`hreflang="x-default" href="${pair.it}"`), `${pair.path}: missing x-default`);
}

const legacy = [
  { path: 'en.html', canonical: `${base}/en/positioning/` },
  { path: 'metodo-ai.html', canonical: `${base}/en/method/` },
  { path: 'strumenti.html', canonical: `${base}/en/system/` }
];
for (const page of legacy) {
  const html = await read(page.path);
  assert(html.includes(`<link rel="canonical" href="${page.canonical}" />`), `${page.path}: legacy canonical is wrong`);
  assert(/<meta\s+name="robots"\s+content="noindex, follow"\s*\/>/i.test(html), `${page.path}: legacy page must be noindex, follow`);
}

const sitemap = await read('sitemap.xml');
const locs = [...sitemap.matchAll(/<loc>([^<]+)<\/loc>/g)].map((match) => match[1]);
assert(new Set(locs).size === locs.length, 'sitemap.xml: duplicate URLs found');
for (const page of pages) {
  assert(locs.includes(page.url), `sitemap.xml: missing canonical English URL ${page.url}`);
}
for (const oldUrl of [`${base}/en.html`, `${base}/metodo-ai.html`, `${base}/strumenti.html`]) {
  assert(!locs.includes(oldUrl), `sitemap.xml: legacy non-canonical URL must be removed: ${oldUrl}`);
}

const script = await read('assets/script.js');
assert(script.includes('const bilingualPairs ='), 'assets/script.js: bilingual pair map missing');
assert(script.includes('data-language-switcher'), 'assets/script.js: language switcher missing');
assert(!script.includes('navigator.language'), 'assets/script.js: browser-language detection is forbidden');
assert(!script.includes('navigator.languages'), 'assets/script.js: browser-language detection is forbidden');

const style = await read('assets/style.css');
assert(style.includes('.language-switcher{'), 'assets/style.css: language switcher styles missing');

const robots = await read('robots.txt');
assert(/User-agent:\s*\*/.test(robots) && /Allow:\s*\//.test(robots), 'robots.txt: crawlability changed unexpectedly');
assert(robots.includes('Sitemap: https://alessandro-gentili.it/sitemap.xml'), 'robots.txt: sitemap declaration missing');

await access(join(root, 'tools/check-archive-consistency.mjs'));
await access(join(root, 'tools/check-saggio-16-publication.mjs'));

console.log(`Internationalization checks passed: ${pages.length} canonical English pages, ${italianPairs.length} reciprocal IT/EN pairs, legacy compatibility verified.`);
