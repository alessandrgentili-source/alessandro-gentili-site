/* Gabriel Tarde EN26: progressive enhancement of three semantic reading tables.
   No network access. With JavaScript disabled, all source rows remain visible. */
(() => {
  "use strict";
  const main = document.querySelector(".atlas-tarde-v3 .atlas-main");
  if (!main) return;

  const normalize = value => String(value)
    .normalize("NFD").replace(/[\u0300-\u036f]/g, "")
    .toLowerCase().replace(/\s+/g, " ").trim();

  const readers = [];
  for (const id of ["life", "works", "glossary"]) {
    const panel = main.querySelector('[data-tarde-controls="' + id + '"]');
    const table = main.querySelector("#tarde-" + id + "-table");
    if (!panel || !table || !table.tBodies.length) continue;

    const tbody = table.tBodies[0];
    const original = Array.from(tbody.rows);
    const search = panel.querySelector('input[type="search"]');
    const sort = panel.querySelector("select");
    const reset = panel.querySelector("button");
    const status = panel.querySelector('[role="status"]');
    const header = table.querySelector("thead th:nth-child(" + (id === "works" ? "2" : "1") + ")");
    if (!search || !reset || !status) continue;

    const unit = id === "life" ? "dates" : id === "works" ? "works" : "terms";
    const model = { original, tbody, search, sort, reset, panel, status, header, unit, printing: false };

    function update() {
      if (model.printing) return;
      const words = normalize(search.value).split(" ").filter(Boolean);
      const rows = [...original];
      if (sort && sort.value !== "source") {
        rows.sort((a, b) => {
          const yearA = Number(a.dataset.year || 0);
          const yearB = Number(b.dataset.year || 0);
          const delta = yearA - yearB;
          return (sort.value === "asc" ? delta : -delta) ||
                 (Number(a.dataset.originalIndex) - Number(b.dataset.originalIndex));
        });
      }
      tbody.append(...rows);
      let shown = 0;
      for (const row of original) {
        const searchable = normalize(row.textContent);
        const match = words.every(word => searchable.includes(word));
        row.hidden = !match;
        if (match) shown++;
      }
      status.textContent = shown + " of " + original.length + " " + unit;
      if (sort && header) {
        header.setAttribute("aria-sort",
          sort.value === "source" ? "none" :
          sort.value === "asc" ? "ascending" : "descending");
      }
    }

    function showAllForPrint() {
      if (model.printing) return;
      model.printing = true;
      tbody.append(...original);
      original.forEach(row => { row.hidden = false; });
    }
    function restoreAfterPrint() {
      model.printing = false;
      update();
    }

    search.addEventListener("input", update);
    if (sort) sort.addEventListener("change", update);
    reset.addEventListener("click", () => {
      search.value = "";
      if (sort) sort.value = "source";
      update();
      search.focus();
    });
    panel.hidden = false;
    update();
    readers.push({ showAllForPrint, restoreAfterPrint });
  }

  if (!readers.length) return;
  let inPrint = false;
  const beforePrint = () => {
    if (inPrint) return;
    inPrint = true;
    readers.forEach(reader => reader.showAllForPrint());
  };
  const afterPrint = () => {
    if (!inPrint) return;
    inPrint = false;
    readers.forEach(reader => reader.restoreAfterPrint());
  };
  window.addEventListener("beforeprint", beforePrint);
  window.addEventListener("afterprint", afterPrint);
  if (typeof window.matchMedia === "function") {
    const media = window.matchMedia("print");
    if (typeof media.addEventListener === "function") {
      media.addEventListener("change", event => {
        if (event.matches) beforePrint();
        else afterPrint();
      });
    }
  }
})();
