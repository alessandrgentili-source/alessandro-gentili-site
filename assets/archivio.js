const controls = document.querySelector('.archive-controls');
const query = controls.querySelector('input');
const filters = [...controls.querySelectorAll('[data-filter]')];
const sectionSelect = controls.querySelector('select');
for (const button of filters) {
  sectionSelect.add(new Option(button.textContent, button.dataset.filter));
}
const statusLine = controls.querySelector('[role="status"]');
const emptyState = document.querySelector('.archive-empty');
const groups = [...document.querySelectorAll('.archive-group')];
const normalize = (text) => text.toLocaleLowerCase('it').normalize('NFD')
  .replace(/\p{M}/gu, '').replace(/[^\p{L}\p{N}]+/gu, ' ').trim();

const records = [...document.querySelectorAll('[data-archive-item]')].map(element => ({
  element,
  text: normalize([
    element.dataset.essayNumber ? 'Saggio ' + element.dataset.essayNumber : '',
    element.querySelector('h3').textContent,
    element.querySelector('.meta')?.textContent ?? '',
    element.closest('section').querySelector('h2').textContent,
  ].join(' ')),
}));
let category = 'all';

function updateArchive() {
  const words = normalize(query.value).split(' ');
  let total = 0;
  for (const { element, text } of records) {
    const matches = (category === 'all' || element.dataset.category === category)
      && words.every(word => text.includes(word));
    element.hidden = !matches;
    if (matches) total++;
  }
  for (const group of groups) {
    group.hidden = !group.querySelector('[data-archive-item]:not([hidden])');
  }
  for (const button of filters) {
    button.setAttribute('aria-pressed', String(button.dataset.filter === category));
  }
  sectionSelect.value = category;
  emptyState.hidden = total !== 0;
  statusLine.textContent = total === 1 ? '1 voce' : total + ' voci';
}

for (const button of filters) {
  button.addEventListener('click', () => {
    category = button.dataset.filter;
    updateArchive();
  });
}
sectionSelect.addEventListener('change', () => {
  category = sectionSelect.value;
  updateArchive();
});
query.addEventListener('input', updateArchive);
emptyState.querySelector('button').addEventListener('click', () => {
  category = 'all';
  query.value = '';
  updateArchive();
  query.focus();
});
window.addEventListener('pageshow', updateArchive);
updateArchive();
controls.hidden = false;
