#!/usr/bin/env node
/* Deterministic Tarde EN26 progressive-enhancement interaction regression test.
   A lightweight DOM harness: not a substitute for real browser / assistive testing. */
"use strict";
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");
const assert = require("node:assert/strict");

class Control {
  constructor(value = "") { this.value = value; this.handlers = Object.create(null); this.focused = false; }
  addEventListener(name, fn) { this.handlers[name] = fn; }
  dispatch(name) { assert.equal(typeof this.handlers[name], "function"); this.handlers[name]({ type: name }); }
  focus() { this.focused = true; }
}
function fixture(id, values) {
  const rows = values.map(([year, label], i) => ({
    dataset: { year: String(year), originalIndex: String(i) },
    textContent: year + " " + label,
    hidden: false
  }));
  const tbody = { rows: [...rows], append(...newRows) { this.rows = [...newRows]; } };
  const search = new Control();
  const sort = id === "glossary" ? null : new Control("source");
  const reset = new Control();
  const status = { textContent: "" };
  const header = { attrs: {}, setAttribute(k, v) { this.attrs[k] = v; } };
  const panel = {
    hidden: true,
    querySelector(selector) {
      if (selector === 'input[type="search"]') return search;
      if (selector === "select") return sort;
      if (selector === "button") return reset;
      if (selector === '[role="status"]') return status;
      throw new Error(selector);
    }
  };
  const table = { tBodies: [tbody], querySelector: () => header };
  return { id, rows, tbody, search, sort, reset, status, header, panel, table };
}
const data = [
  fixture("life", [
    [1843, "Sarlat"], [1875, "Sarlat magistrate"], [1880, "Belief essay"],
    [1886, "Comparative criminology"], [1890, "Imitation"],
    [1894, "Paris statistics"], [1900, "College de France"], [1904, "Paris death"]
  ]),
  fixture("works", [
    [1880, "Belief desire"], [1886, "Criminality"], [1890, "Imitation"],
    [1895, "Social logic"], [1895, "Monadology"], [1898, "Social laws"],
    [1901, "Opinion crowd"], [1902, "Economic psychology"]
  ]),
  fixture("glossary", Array.from({ length: 20 }, (_, i) =>
    [i, i === 9 ? "Imitation social transmission" : "Concept " + i]))
];
const byId = Object.fromEntries(data.map(x => [x.id, x]));
const main = {
  querySelector(sel) {
    let m = sel.match(/^\[data-tarde-controls="([^"]+)"\]$/);
    if (m) return byId[m[1]]?.panel || null;
    m = sel.match(/^#tarde-([^-]+)-table$/);
    if (m) return byId[m[1]]?.table || null;
    return null;
  }
};
const windowHandlers = {};
let matchMediaChange = null;
const fakeWindow = {
  addEventListener(type, listener) { windowHandlers[type] = listener; },
  matchMedia() { return { addEventListener(type, listener) { if (type === "change") matchMediaChange = listener; } }; }
};
const document = {
  querySelector(sel) { return sel === ".atlas-tarde-v3 .atlas-main" ? main : null; }
};
const source = fs.readFileSync(
  path.resolve(__dirname, "../assets/international-tarde.js"), "utf8");
vm.runInNewContext(source, { document, window: fakeWindow, console });

for (const x of data) {
  assert.equal(x.panel.hidden, false, x.id + " controls progressively exposed");
  assert.equal(x.status.textContent, x.rows.length + " of " + x.rows.length + " " +
    (x.id === "life" ? "dates" : x.id === "works" ? "works" : "terms"));
  assert(x.rows.every(row => !row.hidden), x.id + " all rows must begin visible");
}
byId.life.search.value = "Sarlat";
byId.life.search.dispatch("input");
assert.equal(byId.life.rows.filter(row => !row.hidden).length, 2);
assert.equal(byId.life.status.textContent, "2 of 8 dates");

byId.life.sort.value = "desc";
byId.life.sort.dispatch("change");
assert.equal(byId.life.tbody.rows[0].dataset.year, "1904");
assert.equal(byId.life.header.attrs["aria-sort"], "descending");

byId.works.search.value = "psychology";
byId.works.search.dispatch("input");
assert.equal(byId.works.rows.filter(row => !row.hidden).length, 1);
assert.equal(byId.works.status.textContent, "1 of 8 works");

byId.glossary.search.value = "IMITATION";
byId.glossary.search.dispatch("input");
assert.equal(byId.glossary.rows.filter(row => !row.hidden).length, 1);
byId.glossary.search.value = "not-an-entry";
byId.glossary.search.dispatch("input");
assert.equal(byId.glossary.status.textContent, "0 of 20 terms");

assert.equal(typeof windowHandlers.beforeprint, "function");
assert.equal(typeof windowHandlers.afterprint, "function");
windowHandlers.beforeprint();
for (const x of data) {
  assert(x.rows.every(row => !row.hidden), x.id + " print must include all rows");
  assert.deepEqual(x.tbody.rows.map(row => row.dataset.originalIndex),
    x.rows.map(row => row.dataset.originalIndex), x.id + " print in source order");
}
windowHandlers.afterprint();
assert.equal(byId.life.rows.filter(row => !row.hidden).length, 2);
assert.equal(byId.life.tbody.rows[0].dataset.year, "1904");
assert.equal(byId.works.rows.filter(row => !row.hidden).length, 1);
assert.equal(byId.glossary.rows.filter(row => !row.hidden).length, 0);

byId.life.reset.dispatch("click");
assert.equal(byId.life.search.value, "");
assert.equal(byId.life.sort.value, "source");
assert(byId.life.rows.every(row => !row.hidden));
assert.equal(byId.life.tbody.rows[0].dataset.year, "1843");
assert.equal(byId.life.search.focused, true);

assert.equal(typeof matchMediaChange, "function");
matchMediaChange({ matches: true });
assert(data.every(x => x.rows.every(row => !row.hidden)));
matchMediaChange({ matches: false });
assert.equal(byId.glossary.rows.filter(row => !row.hidden).length, 0);
console.log("PASS Tarde EN26: search, chronological sorting, reset/focus, no-results feedback, print all rows and state restoration (DOM harness)");
