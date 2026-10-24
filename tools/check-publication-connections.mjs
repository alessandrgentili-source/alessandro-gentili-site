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

  // A selected Home is not a chronological feed: only its *first* essay slot
  // is required to be the newest numbered essay; remaining slots are editorial.
  const featuredSection = s.home.match(/<section[^>]*class="[^"]*\blatest-essays\b[^"]*"[\s\S]*?<\/section>/)?.[0] ?? '';
  const featuredCards = [...featuredSection.matchAll(/<article class="essay-card" data-saggio-(\d+)[\s\S]*?<\/article>/g)];
  const allFeaturedCards = [...featuredSection.matchAll(/<article class="essay-card"[\s\S]*?<\/article>/g)];
  require(featuredSection.length > 0, 'Home: missing latest-essays section');
  require(allFeaturedCards.length === 3, 'Home: preserve the three selected essay cards');
  require(featuredCards.length > 0 && Number(featuredCards[0][1]) === d.latest.number,
    'Home: first featured card must show latest numbered essay ' + d.latest.number);
  require(featuredCards.length > 0 && featuredCards[0][0].includes('href="' + latestLink + '"'),
    'Home: latest essay card must link to ' + latestLink);
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

  require(s.enHome.includes(d.enGuideSlugs.length + ' English author guides and ' + enIds.length + ' triad reading paths'),
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
    ['stale guide count', staleGuideCount],
    ['stale triad CTA', staleTriadCount]
  ]) {
    if (check(mutated, data).length === 0) throw Error('Regression escaped publication gate: ' + label);
  }
  console.log('Mutation tests PASS (home, guide count, triad count)');
}
console.log('Publication dependencies PASS: latest essay ' + latest.number +
  ', ' + itGuideSlugs.length + ' IT guides, ' + enGuideSlugs.length +
  ' EN guides, IT/EN triads checked.');
