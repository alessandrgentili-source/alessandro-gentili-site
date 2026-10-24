// Publication dependency gate. Read-only, dependency-free, and independent of the publisher.
import { readFile, readdir } from 'node:fs/promises';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = fileURLToPath(new URL('../', import.meta.url));
const read = (path) => readFile(join(root, path), 'utf8');
const listDirs = async (path) => (await readdir(join(root, path), { withFileTypes: true }))
  .filter((entry) => entry.isDirectory()).map((entry) => entry.name).sort();

const [home, essayIndex, itHub, itTriads, enHome, enHub, enTriads, enPositioning, essayFiles, itGuideSlugs, enGuideSlugs] = await Promise.all([
  read('index.html'), read('saggi.html'), read('cerchi/index.html'),
  read('cerchi/triadi/index.html'), read('en/index.html'),
  read('en/cerchi/index.html'), read('en/cerchi/triads/index.html'),
  read('en/positioning/index.html'), readdir(join(root, 'saggi')),
  listDirs('cerchi/guide'), listDirs('en/cerchi/guides')
]);

const essays = essayFiles
  .map((name) => ({ name, number: Number(name.match(/^saggio-(\d+)-.*\.html$/)?.[1]) }))
  .filter((item) => Number.isInteger(item.number) && item.number >= 0)
  .sort((a, b) => b.number - a.number);
if (essays.length === 0) throw Error('No numbered essay files found');
const latest = essays[0];
const previous = essays[1];
const previousPage = previous ? await read('saggi/' + previous.name) : '';
const latestPage = await read('saggi/' + latest.name);

const englishNumber = (number) => {
  const words = ['Zero', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven',
    'Eight', 'Nine', 'Ten', 'Eleven', 'Twelve', 'Thirteen', 'Fourteen',
    'Fifteen', 'Sixteen', 'Seventeen', 'Eighteen', 'Nineteen', 'Twenty'];
  return words[number] ?? String(number);
};

const state = {
  home, essayIndex, itHub, itTriads, enHome, enHub, enTriads,
  enPositioning, previousPage, latestPage
};
const data = { latest, previous, itGuideSlugs, enGuideSlugs };

function check(s, d) {
  const errors = [];
  const require = (ok, message) => { if (!ok) errors.push(message); };
  const latestLink = 'saggi/' + d.latest.name;

  // "Ultimi saggi" is strictly chronological: the three newest PUBLISHED works,
  // including micro-saggi. The rest of Home may remain an editorial selection.
  const indexedCards = [...s.essayIndex.matchAll(/<article class="essay-card"[^>]*>[\s\S]*?<\/article>/g)]
    .map((match) => match[0]);
  const months = ['gennaio', 'febbraio', 'marzo', 'aprile', 'maggio', 'giugno',
    'luglio', 'agosto', 'settembre', 'ottobre', 'novembre', 'dicembre'];
  const indexed = indexedCards.map((card) => {
    const href = card.match(/<h3><a href="(saggi\/[^"]+)"/)?.[1] ?? null;
    const meta = card.match(/<p class="meta">([^<]+)<\/p>/)?.[1] ?? '';
    const dateMatch = meta.match(/\b(\d{1,2})\s+([a-z]+)\s+(\d{4})\b/i);
    const month = dateMatch ? months.indexOf(dateMatch[2].toLowerCase()) : -1;
    const date = dateMatch && month >= 0
      ? Date.UTC(Number(dateMatch[3]), month, Number(dateMatch[1]))
      : null;
    return { href, date };
  });
  const featuredSection = s.home.match(/<section[^>]*class="[^"]*\blatest-essays\b[^"]*"[\s\S]*?<\/section>/)?.[0] ?? '';
  const featuredCards = [...featuredSection.matchAll(/<article class="essay-card"[^>]*>[\s\S]*?<\/article>/g)]
    .map((match) => match[0]);
  const featuredHrefs = featuredCards.map((card) =>
    card.match(/<h3><a href="(saggi\/[^"]+)"/)?.[1] ?? null);
  const expected = indexed.slice(0, 3);
  require(featuredSection.length > 0, 'Home: missing latest-essays section');
  require(indexed.length >= 3 && indexed.every((entry) => entry.href),
    'Saggi index: every published essay card must have a link to its proprietary page');
  require(expected.length === 3 && expected.every((entry) => entry.date !== null),
    'Saggi index: newest three essays need precise publication dates (day/month/year)');
  if (expected.length === 3 && expected.every((entry) => entry.date !== null)) {
    require(expected[0].date >= expected[1].date && expected[1].date >= expected[2].date,
      'Saggi index: newest three essays are not sorted by descending publication date');
    require(indexed.slice(3).every((entry) => entry.date === null || entry.date <= expected[2].date),
      'Saggi index: a newer dated essay appears below the first three cards');
  }
  require(featuredCards.length === 3, 'Home: "Ultimi saggi" must contain exactly three cards');
  require(featuredHrefs.length === 3 && featuredHrefs.every((href, i) => href === expected[i]?.href),
    'Home: "Ultimi saggi" must match the three most recently published works in Saggi index, including micro/macro, in chronological order. Expected: ' +
    expected.map((entry) => entry.href).join(', '));
  require(s.essayIndex.includes('href="' + latestLink + '"'),
    'Saggi index: missing latest numbered essay ' + latestLink);
  if (d.previous) {
    require(s.previousPage.includes('href="' + d.latest.name + '"'),
      'Previous numbered essay ' + d.previous.number + ': missing forward link to ' + d.latest.number);
    require(s.latestPage.includes('href="' + d.previous.name + '"'),
      'Latest numbered essay ' + d.latest.number + ': missing backward link to ' + d.previous.number);
  }

  // The guide index must expose every published IT/EN guide, independently.
  for (const slug of d.itGuideSlugs) {
    require(s.itHub.includes('href="guide/' + slug + '/"'),
      'Italian Cerchi hub: missing published guide ' + slug);
  }
  for (const slug of d.enGuideSlugs) {
    require(s.enHub.includes('href="/en/cerchi/guides/' + slug + '/"'),
      'English Cerchi hub: missing published English guide ' + slug);
  }

  // Triads are editorially completed groups, NOT floor(guideCount/3);
  // a guide may be published while a new triad is still being built.
  const itCount = [...s.itTriads.matchAll(/<p class="essay-number">[^<]*triade<\/p>/gi)].length;
  const enIds = [...s.enTriads.matchAll(/<section class="wrap triad-block" id="triad-(\d+)"/g)]
    .map((match) => match[1]);
  const enLinks = [...s.enTriads.matchAll(/<a href="#triad-(\d+)"/g)]
    .map((match) => match[1]);
  require(itCount > 0, 'Italian Triadi index: no published triad cards found');
  require(enIds.length > 0 && enIds.join('|') === enLinks.join('|'),
    'English Triads: index and reading paths must match in number and order');

  // Copy counts are a deliberate release responsibility, never client-side JS.
  require(s.itHub.includes('Le ' + d.itGuideSlugs.length + ' guide restano'),
    'Italian Cerchi hub: guide count in introductory copy must be ' + d.itGuideSlugs.length);
  require(s.itHub.includes(itCount + ' soglie di lettura'),
    'Italian Cerchi hub: triad kicker must be ' + itCount);
  require(s.itHub.includes('le ' + itCount + ' costellazioni'),
    'Italian Cerchi hub: triad paragraph must say ' + itCount);
  require(s.itHub.includes('Esplora le ' + itCount + ' triadi'),
    'Italian Cerchi hub: triad CTA must say ' + itCount);

  require(s.enHome.includes('data-corpus-count="en-guides">' + d.enGuideSlugs.length + '</span>') &&
    s.enHome.includes('data-corpus-count="en-triads">' + enIds.length + '</span>'),
    'English Home: guide/triad inventory counts do not match published files');
  require(s.enPositioning.includes('data-corpus-count="en-guides">' + d.enGuideSlugs.length + '</span>'),
    'English Positioning: English guide count does not match published files');
  require(s.enPositioning.includes('data-corpus-count="en-triads">' + enIds.length + '</span>'),
    'English Positioning: English triad count does not match reading paths');
  require(s.enTriads.includes(englishNumber(enIds.length) + ' triads'),
    'English Triads: spelled-out triad count is stale');
  return errors;
}

const errors = check(state, data);
if (errors.length) {
  throw Error('Publication dependencies FAIL:\n- ' + errors.join('\n- '));
}

// Mutation regression: the real published corpus must FAIL if connected surfaces drift.
if (process.argv.includes('--self-test')) {
  const omitNewest = {
    ...state,
    home: state.home.replace(/<article class="essay-card" data-saggio-\d+>[\s\S]*?<\/article>/, '')
  };
  const homeCards = [...state.home.matchAll(/<article class="essay-card"[^>]*>[\s\S]*?<\/article>/g)];
  const swapSecondThird = {
    ...state,
    home: state.home.replace(homeCards[1][0], '__SECOND_HOME_CARD__')
      .replace(homeCards[2][0], homeCards[1][0])
      .replace('__SECOND_HOME_CARD__', homeCards[2][0])
  };
  // Regression of the actual risk: a newly published micro-saggio must become
  // the first item if it is newer than the latest numbered essay.
  const indexedCards = [...state.essayIndex.matchAll(/<article class="essay-card"[^>]*>[\s\S]*?<\/article>/g)];
  const newerMicro = indexedCards[2][0].replace('4 settembre 2026', '15 ottobre 2026');
  const newerMicroIndex = {
    ...state,
    essayIndex: state.essayIndex.replace(indexedCards[0][0], newerMicro)
      .replace(indexedCards[2][0], indexedCards[0][0])
  };
  const staleGuideCount = {
    ...state,
    itHub: state.itHub.replace('Le ' + itGuideSlugs.length + ' guide restano', 'Le 0 guide restano')
  };
  const staleTriadCount = {
    ...state,
    itHub: state.itHub.replace('Esplora le ' +
      [...state.itTriads.matchAll(/<p class="essay-number">[^<]*triade<\/p>/gi)].length +
      ' triadi', 'Esplora le 0 triadi')
  };
  for (const [label, mutated] of [
    ['missing newest Home card', omitNewest],
    ['reordered chronological Home cards', swapSecondThird],
    ['newer micro-saggio omitted from first position', newerMicroIndex],
    ['stale guide count', staleGuideCount],
    ['stale triad CTA', staleTriadCount]
  ]) {
    if (check(mutated, data).length === 0) throw Error('Regression escaped publication gate: ' + label);
  }
  console.log('Mutation tests PASS (home, guide count, triad count)');
}
console.log('Publication dependencies PASS: chronological latest three essays (micro/macro), latest numbered essay ' + latest.number +
  ', ' + itGuideSlugs.length + ' IT guides, ' + enGuideSlugs.length +
  ' EN guides, IT/EN triads checked.');
