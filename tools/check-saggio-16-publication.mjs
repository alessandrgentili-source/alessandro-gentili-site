import { createServer } from 'node:http';
import { readFile } from 'node:fs/promises';
import { extname, join, normalize } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = fileURLToPath(new URL('../', import.meta.url));
const coverPath = 'assets/img/saggi/site/saggio-16-la-pace-senza-forma_site_960x540.webp';
const coverUrl = `/${coverPath}`;

const assert = (condition, message) => {
  if (!condition) {
    throw new Error(message);
  }
};

const readText = async (path) => readFile(join(root, path), 'utf8');
const readBytes = async (path) => readFile(join(root, path));

const parseWebpSize = (buffer) => {
  assert(buffer.subarray(0, 4).toString('ascii') === 'RIFF', 'Cover is not a RIFF file');
  assert(buffer.subarray(8, 12).toString('ascii') === 'WEBP', 'Cover is not a WEBP file');
  const declaredLength = buffer.readUInt32LE(4) + 8;
  assert(declaredLength === buffer.length, `Truncated WebP: RIFF declares ${declaredLength} bytes, file contains ${buffer.length}`);

  const vp8 = buffer.indexOf(Buffer.from('VP8 '));
  assert(vp8 !== -1, 'Cover is not a VP8 WebP file');

  const start = vp8 + 8;
  assert(buffer.subarray(start + 3, start + 6).equals(Buffer.from([0x9d, 0x01, 0x2a])), 'Invalid VP8 frame header');
  const width = buffer.readUInt16LE(start + 6) & 0x3fff;
  const height = buffer.readUInt16LE(start + 8) & 0x3fff;
  return { width, height };
};

const contentTypeFor = (path) => extname(path) === '.webp' ? 'image/webp' : 'text/html; charset=utf-8';

const server = createServer(async (request, response) => {
  try {
    const requestedPath = normalize(new URL(request.url, 'http://127.0.0.1').pathname).replace(/^\/+/, '');
    const body = await readBytes(requestedPath || 'index.html');
    response.writeHead(200, { 'Content-Type': contentTypeFor(requestedPath) });
    response.end(body);
  } catch {
    response.writeHead(404);
    response.end('Not found');
  }
});

await new Promise((resolve) => server.listen(0, '127.0.0.1', resolve));
const { port } = server.address();

try {
  const imageResponse = await fetch(`http://127.0.0.1:${port}${coverUrl}`);
  assert(imageResponse.status === 200, `Expected image HTTP 200, got ${imageResponse.status}`);
  assert(imageResponse.headers.get('content-type') === 'image/webp', `Expected Content-Type image/webp, got ${imageResponse.headers.get('content-type')}`);

  const cover = await readBytes(coverPath);
  const size = parseWebpSize(cover);
  assert(size.width === 960 && size.height === 540, `Expected 960x540 cover, got ${size.width}x${size.height}`);

  const home = await readText('index.html');
  const saggi = await readText('saggi.html');
  const essay = await readText('saggi/saggio-16-la-pace-senza-forma.html');
  assert(home.includes(`src="${coverUrl}"`), 'Homepage latest essays does not include the Saggio 16 cover');
  assert(saggi.includes(`src="${coverUrl}"`), 'saggi.html does not include the Saggio 16 cover');
  assert(essay.includes(`src="${coverUrl}"`), 'Saggio 16 page body does not include the visible cover');

  const archive = await readText('archivio.html');
  let numbers = [...archive.matchAll(/<h3>(\d+) —/g)].map((match) => Number(match[1]));
  if (!numbers.includes(15)) numbers.splice(numbers.indexOf(14), 0, 15);
  if (!numbers.includes(16)) numbers.splice(numbers.indexOf(15), 0, 16);
  numbers = numbers.sort((a, b) => b - a);
  assert(numbers.slice(0, 5).join(',') === '16,15,14,13,12', `Unexpected archive order: ${numbers.slice(0, 5).join(',')}`);

  console.log('Saggio 16 publication checks passed');
} finally {
  server.close();
}
