/* Execute the shipped enhancement against small consultation fixtures. */
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';

const control = () => ({ value: '', hidden: true, handlers: {}, addEventListener(name, fn) { this.handlers[name] = fn; }, focus() { this.focused = true; } });
const makeRegion = (values, table = false) => {
  const input = control(), reset = control(), status = { textContent: '' };
  const controls = { hidden: true, querySelector(selector) { return selector === 'input' ? input : selector === '[data-consult-reset]' ? reset : status; } };
  const rows = values.map(cells => ({ hidden: false, textContent: cells.join(' '), cells: cells.map(textContent => ({ textContent })) }));
  const body = { rows: [...rows], append(row) { this.rows = this.rows.filter(x => x !== row); this.rows.push(row); } };
  const headers = table ? values[0].map((_, i) => ({
    children: [{ textContent: `Column ${i}` }], attrs: {},
    get firstChild() { return this.children[0]; },
    append(button) { this.children = [button]; this.button = button; },
    setAttribute(k, v) { this.attrs[k] = v; }, getAttribute(k) { return this.attrs[k]; }
  })) : [];
  const tableNode = { tBodies: [body], querySelectorAll() { return headers; } };
  return { input, reset, status, controls, rows, body, headers, dataset: { consult: table ? 'table' : 'glossary' },
    querySelector(selector) { return selector === '[data-consult-controls]' ? controls : tableNode; },
    querySelectorAll() { return rows; } };
};
const glossary = makeRegion([['Entropy', 'Average uncertainty'], ['Channel', 'Signal transmission']]);
const table = makeRegion([['Zeta', '2'], ['alpha', '10'], ['Álpha', '2']], true);
const events = {};
const document = {
  body: { classList: { contains: value => value === 'international-complete-guide' } },
  querySelectorAll: () => [glossary, table],
  createElement: () => ({ handlers: {}, append(child) { table.headers.find(h => h.children.includes(child)).children.shift(); }, addEventListener(name, fn) { this.handlers[name] = fn; } })
};
vm.runInNewContext(fs.readFileSync(new URL('../assets/international-complete-guides.js', import.meta.url), 'utf8'), {
  document, Intl, window: { addEventListener(name, fn) { (events[name] ||= []).push(fn); } }
});
const search = (region, value) => { region.input.value = value; region.input.handlers.input(); };
assert.equal(glossary.controls.hidden, false);
assert.equal(glossary.status.textContent, '2 of 2 entries');
search(glossary, 'entropy uncertainty');
assert.deepEqual(glossary.rows.map(r => r.hidden), [false, true]);
search(glossary, 'absent');
assert.equal(glossary.status.textContent, '0 of 2 entries');
glossary.reset.handlers.click();
assert.equal(glossary.input.focused, true);
assert.deepEqual(glossary.rows.map(r => r.hidden), [false, false]);
search(table, 'ALPHA 2');
assert.deepEqual(table.rows.map(r => r.hidden), [true, true, false]);
table.headers[0].button.handlers.click();
assert.deepEqual(table.body.rows.map(r => r.cells[0].textContent), ['alpha', 'Álpha', 'Zeta']);
assert.equal(table.headers[0].attrs['aria-sort'], 'ascending');
table.headers[0].button.handlers.click();
assert.deepEqual(table.body.rows.map(r => r.cells[0].textContent), ['Zeta', 'alpha', 'Álpha']);
table.headers[1].button.handlers.click();
assert.deepEqual(table.body.rows.map(r => r.cells[1].textContent), ['2', '2', '10']);
const orderBeforePrint = [...table.body.rows];
events.beforeprint.forEach(fn => fn());
assert.deepEqual(table.body.rows, table.rows);
events.afterprint.forEach(fn => fn());
assert.deepEqual(table.body.rows, orderBeforePrint);
table.reset.handlers.click();
assert.equal(table.input.value, '');
assert.equal(table.headers[0].attrs['aria-sort'], 'none');
assert.deepEqual(table.body.rows, table.rows);
assert.deepEqual(table.rows.map(r => r.hidden), [false, false, false]);
console.log('Complete guide interactions PASS: AND/accent search, counts, empty state, stable ascending/descending/numeric sort, reset/focus, print order/restore.');
