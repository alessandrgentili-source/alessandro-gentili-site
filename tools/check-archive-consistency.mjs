import { access, readFile, readdir } from 'node:fs/promises';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = fileURLToPath(new URL('../', import.meta.url));
const baseUrl = 'https://alessandro-gentili.it/';

const assert = (condition, message) => {
  if (!condition) {
    throw new Error(message);
  }
};

const readText = (path) => readFile(join(root, path), 'utf8');

const publicUrlForFile = (path) => {
  if (path.endsWith('/index.html')) {
    return baseUrl + path.slice(0, -'index.html'.length);
  }
  return baseUrl + path;
};

const collectHtml = async (dir) => {
  const output = [];
  const walk = async (relative) => {
    const entries = await readdir(join(root, relative), { withFileTypes: true });
    for (const entry of entries) {
      const path = `${relative}/${entry.name}`;
      if (entry.isDirectory()) {
        await walk(path);
      } else if (entry.isFile() && entry.name.endsWith('.html')) {
        output.push(path);
      }
    }
  };
  await walk(dir);
  return output.sort();
};

const archive = await readText('archivio.html');
const sitemap = await readText('sitemap.xml');
const script = await readText('assets/script.js');

const sitemapUrls = new Set(
  [...sitemap.matchAll(/<loc>(https:\/\/alessandro-gentili\.it\/[^<]*)<\/loc>/g)]
    .map((match) => match[1])
);

const archiveHrefs = [...archive.matchAll(/href="([^"]+)"/g)].map((match) => match[1]);
const archiveLocalHrefs = archiveHrefs
  .filter((href) => !/^(?:https?:|mailto:|tel:|#)/.test(href))
  .map((href) => href.split('#')[0].split('?')[0]);

const saggiPages = (await collectHtml('saggi'))
  .filter((path) => /saggio-\d+/.test(path) || path.includes('il-giorno-in-cui-un-paese-torna/'));
const portfolioProjects = (await collectHtml('portfolio'))
  .filter((path) => /portfolio\/[^/]+\/index\.html$/.test(path));

for (const page of [...saggiPages, ...portfolioProjects]) {
  const url = publicUrlForFile(page);
  const relativeUrl = url.slice(baseUrl.length);
  assert(sitemapUrls.has(url), `Public content missing from sitemap: ${url}`);
  assert(
    archiveHrefs.some((href) => href === relativeUrl),
    `Public content missing from archive: ${relativeUrl}`
  );
}

const essayNumbers = [...archive.matchAll(/data-essay-number="(\d+)"/g)]
  .map((match) => Number(match[1]));
const expectedEssayNumbers = Array.from({ length: 17 }, (_, index) => 16 - index);
assert(
  essayNumbers.join(',') === expectedEssayNumbers.join(','),
  `Archive essay sequence must be static and ordered 16→0. Found: ${essayNumbers.join(',')}`
);

assert(
  archive.includes('href="saggi/il-giorno-in-cui-un-paese-torna/"'),
  'Micro-saggio is missing from archive'
);
assert(
  archive.includes('href="portfolio/le-figure-di-pinocchio/"'),
  'Pinocchio portfolio is missing from archive'
);
assert(
  archive.includes('href="portfolio/un-paese-dentro-la-storia/"'),
  'Un paese dentro la storia is missing from archive'
);
assert(
  !archive.includes('g-69264b3869ac81918a0d3ff4a1754d98'),
  'Archive still contains the obsolete Scaffale Strategico GPT URL'
);

assert(
  !script.includes('saggio-15-il-mondo-senza-apprendisti') &&
  !script.includes('saggio-16-la-pace-senza-forma'),
  'script.js still contains obsolete dynamic publication injections for Saggio 15/16'
);

const filters = new Set(
  [...archive.matchAll(/data-filter="([^"]+)"/g)].map((match) => match[1])
);
const categories = new Set(
  [...archive.matchAll(/data-archive-item[^>]*data-category="([^"]+)"/g)]
    .map((match) => match[1])
);
for (const category of categories) {
  assert(filters.has(category), `Archive category has no filter button: ${category}`);
}
for (const filter of filters) {
  if (filter !== 'all') {
    assert(categories.has(filter), `Archive filter has no items: ${filter}`);
  }
}

for (const href of new Set(archiveLocalHrefs)) {
  if (!href) continue;
  const filesystemPath = href.endsWith('/') ? `${href}index.html` : href;
  try {
    await access(join(root, filesystemPath));
  } catch {
    throw new Error(`Broken local archive link: ${href}`);
  }
}

console.log(
  `Archive consistency checks passed: ${saggiPages.length} essay pages, ${portfolioProjects.length} portfolio projects, ${categories.size} categories.`
);
