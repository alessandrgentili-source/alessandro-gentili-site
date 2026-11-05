// Regression checks for the shared progressive contents behaviour, without dependencies.
// A small DOM fixture exercises events and geometry; real browser QA remains required.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { runInNewContext } from 'node:vm';

const code = readFileSync(new URL('../assets/international-atlas.js', import.meta.url), 'utf8');
const events = new Map();
const frames = [];
let resizeLayout;
let changeBreakpoint;
const positions = [900, 1500, 2200];
const sections = ['opening', 'argument', 'sources'].map((id, i) => ({
  id, getBoundingClientRect: () => ({ top: positions[i] })
}));
const links = sections.map(section => ({
  hash: `#${section.id}`, attrs: {},
  setAttribute(key, value) { this.attrs[key] = value; },
  removeAttribute(key) { delete this.attrs[key]; }
}));
const contents = { open: true, querySelectorAll: () => links };
const mobile = { matches: false, addEventListener(type, fn) { changeBreakpoint = fn; } };
const main = {
  querySelector: selector => selector.includes('contents') ? contents : null,
  querySelectorAll: () => sections
};
const root = {};
const window = {
  matchMedia: () => mobile,
  requestAnimationFrame: callback => frames.push(callback),
  addEventListener: (type, fn) => events.set(type, fn),
  ResizeObserver: true
};
const document = {
  documentElement: root,
  querySelector: selector => selector.includes('atlas-main') ? main : null,
  querySelectorAll: () => [],
  getElementById: id => sections.find(section => section.id === id)
};
runInNewContext(code, {
  window, document,
  getComputedStyle: element => element === root ? { scrollPaddingTop: '86px' } : { scrollMarginTop: '24px' },
  ResizeObserver: class { constructor(fn) { resizeLayout = fn; } observe() {} }
});
const flush = () => { while (frames.length) frames.shift()(); };
const active = () => links.filter(link => link.attrs['aria-current'] === 'location').map(link => link.hash);
flush();
assert.equal(contents.open, true);
assert.deepEqual(active(), ['#opening']);
// Native deep link has landed exactly at scroll-padding + scroll-margin.
positions.splice(0, 3, -600, 110, 900);
events.get('hashchange')(); flush();
assert.deepEqual(active(), ['#argument']);
// Tall optional module: keep the preceding argument active until the next heading.
positions.splice(0, 3, -1200, -400, 600);
events.get('scroll')(); flush();
assert.deepEqual(active(), ['#argument']);
// Layout shifts without scrolling (font, cover or optional control).
positions[2] = 110;
resizeLayout(); flush();
assert.deepEqual(active(), ['#sources']);
positions[2] = 500;
events.get('resize')(); flush();
assert.deepEqual(active(), ['#argument']);
// Breakpoints restore the appropriate disclosure; ordinary resize keeps reader choice.
mobile.matches = true; changeBreakpoint(); flush();
assert.equal(contents.open, false);
contents.open = true;
events.get('resize')(); flush();
assert.equal(contents.open, true);
contents.open = false;
mobile.matches = false; changeBreakpoint(); flush();
assert.equal(contents.open, true);
positions.splice(0, 3, 900, 1500, 2200);
events.get('pageshow')(); flush();
assert.deepEqual(active(), ['#opening']);
// Non-atlas pages are inert even if the script is accidentally loaded.
runInNewContext(code, { document: { querySelector: () => null } });
console.log('Atlas PASS: deep links, scroll, optional module, layout shifts, resize, breakpoints, history restoration, scoped activation.');
