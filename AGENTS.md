# AGENTS.md — alessandro-gentili-site

## Repository identity

This repository powers `alessandro-gentili.it`, the proprietary and canonical website of Alessandro Gentili’s editorial, cultural and professional work.

The website is the canonical source. Medium is a secondary distribution channel.

Every change must preserve:

* editorial elegance;
* site stability;
* SEO/GEO clarity;
* maintainability;
* internal linking coherence;
* public/private separation;
* consistency across similar pages.

Prefer reusable standards over isolated fixes. If a discrepancy appears across similar pages, first identify the intended standard, then apply it consistently.

## Operating method

Before structural changes:

1. perform a read-only audit;
2. diagnose the issue;
3. propose the patch;
4. wait for approval when the change is risky or broad;
5. apply a conservative modification;
6. run relevant tests;
7. provide a final report.

Do not edit files unless the task has a clear:

* objective;
* scope;
* list of files to modify;
* list of files not to modify;
* SEO/editorial constraints;
* testing plan.

## Protected files and protected elements

Do not modify unless explicitly requested:

* slugs;
* filenames;
* canonical URLs;
* `sitemap.xml`;
* `robots.txt`;
* meta title;
* meta description;
* H1;
* JSON-LD;
* global CSS;
* Home page;
* main editorial text.

Do not create links to:

* future pages;
* nonexistent URLs;
* private pages;
* test pages;
* unpublished prototypes;
* `delos-reference.html`.

Do not publicly promote `IN|SUPERFICIE` as a brand or project name.

Do not use `Delos` as a public operating name.

## Home page rules

The Home page must remain sober, proprietary and site-oriented.

Rules:

* do not add Medium CTAs to the Home page;
* do not turn the Home page into a full archive;
* keep a maximum of 9 visible Cerchi d’inchiostro guide cards;
* treat the Home page as an editorial selection, not an update feed;
* link primarily to proprietary content: essays, Cerchi d’inchiostro, author page, archive and mature tools only.

## Essay index pages

In `saggi.html`:

* primary CTA: `Leggi il saggio`;
* secondary CTA: `Medium ↗`, only when a Medium version exists;
* Medium CTA must remain secondary and visually coherent;
* do not use mixed labels such as `Leggi su Medium` on some cards and `Medium ↗` on others;
* do not introduce inconsistent dark/light button variants;
* do not modify the Home page when standardizing essay CTAs.

In `archivio.html`:

* for essays also published on Medium, use the same standard:

  * `Leggi il saggio`;
  * `Medium ↗`.
* do not add Medium CTAs or canonicals to Medium-only content or non-duplicate content.


## Saggi page card taxonomy

For `saggi.html`, preserve the editorial card taxonomy.

Top meta row:

* Left side: `SAGGIO X`.
* Right side: one separated kind pill only: `MICRO`, `MACRO`, or `SOGLIA`.
* Never inline the kind as `SAGGIO X · MICRO`.
* Never concatenate the kind as `SAGGIO XMICRO`.

Kind mapping:

* Saggio 13: `MICRO`
* Saggio 12: `MICRO`
* Saggio 11: `MACRO`
* Saggio 10: `MACRO`
* Saggio 9: `MICRO`
* Saggio 8: `MICRO`
* Saggio 7: `MICRO`
* Saggio 6: `MACRO`
* Saggio 5: `MACRO`
* Saggio 4: `MACRO`
* Saggio 3: `MACRO`
* Saggio 2: `MACRO`
* Saggio 1: `MACRO`
* Saggio 0: `SOGLIA`

Date/theme line:

* Use only date and theme.
* Preferred pattern: `date · Tema: short theme`.
* Do not add publication state labels in this line.

Bottom pills:

* Allowed values only:

  * `Testo integrale`
  * `English note`
  * `Saggio-cerniera`
* Do not use bottom pills such as:

  * `Pubblicato`
  * `saggio pubblicato`
  * `Medium`
  * `Archivio locale`
  * `Collegato al Saggio 0`
  * `Saggio integrale`
* Replace `Saggio integrale` with `Testo integrale`.

Actions:

* Use buttons for actions:

  * `Leggi il saggio`
  * `Medium ↗` only when a real Medium URL exists.
* Do not duplicate Medium as a pill.

Editorial meaning:

* `MICRO` identifies essays focused on territory, community, civic thresholds, care, return, and concrete forms of common life.
* `MACRO` identifies essays focused on power, apparatuses, technology, crisis, governance, systems, and broad historical forms.
* `SOGLIA` identifies the introductory/editorial threshold essay.

Before editing `saggi.html`, inspect existing card patterns and apply the taxonomy consistently.
After editing `saggi.html`, verify there are no occurrences of:

* `SAGGIO 13MICRO`
* `SAGGIO 13 · MICRO`
* `Pubblicato` as a bottom pill
* `Medium` as a bottom pill
* `Archivio locale` as a bottom pill

Final report must confirm:

* files modified;
* whether only `AGENTS.md` was changed;
* no protected SEO files were touched.

## Single essay page structure

Each single essay page must preserve:

* editorial hero;
* hero side panel;
* `Coordinate editoriali`;
* `Pubblicazione` block;
* cover;
* main essay body;
* standard sidebar;
* final previous/next navigation.

Do not rewrite the main essay text unless explicitly requested.

## `Coordinate editoriali` standard

In essay pages, the `Coordinate editoriali` block must be uniform.

Use this standard wording:

Title/label:

`Saggio in archivio proprietario`

Description:

`Questa pagina raccoglie la versione integrale del saggio, con metadati editoriali, collegamenti interni e accesso alla versione Medium.`

Do not create text variants across essays unless explicitly requested.

Purpose:
`Coordinate editoriali` identifies the page as the proprietary archive version. It is not a creative teaser, not a CTA area and not a substitute for the sidebar.

## `Pubblicazione` block standard

In the hero side panel:

* label: `Pubblicazione`;
* badge: `SAGGIO X · PUBBLICATO`;
* text: `Pubblicato anche su Medium.`;
* CTA text: `Leggi su Medium ↗`;
* CTA class: `btn-secondary`;
* external attributes: `target="_blank" rel="noopener noreferrer"`.

Medium should appear only once on a single essay page, unless an explicit exception is approved.

## Standard essay sidebar

The essay sidebar has a fixed order:

1. `Continua il percorso`
2. `Aggiornamenti`
3. `Archivio`

### `Continua il percorso`

Rules:

* use maximum 2–3 genuinely relevant links;
* links may point to essays, Cerchi d’inchiostro guides or Metodo/AI only if semantically useful;
* do not use long lists;
* do not use identical serial links on every page;
* do not turn the sidebar into a catalogue.

### `Aggiornamenti`

Use this standard text:

`Per ricevere nuovi saggi e aggiornamenti editoriali, puoi seguire la lettera periodica.`

CTA:

* href: `../contatti.html#lettera-periodica`
* text: `Lettera periodica`
* class: `btn-secondary`

### `Archivio`

Use these CTAs:

* `Tutti i saggi` → `../saggi.html`
* `Archivio generale` → `../archivio.html`

## Final essay navigation

Use only one final navigation card:

* previous essay, if it exists;
* next essay, if it exists.

Avoid duplication with sidebar links or body links.
Do not invent incoherent previous/next relations.
Keep the essay chain readable.

## Medium and canonical rules

Fundamental rule:

* site pages must use self-referencing canonical URLs;
* Medium articles should canonicalize to the site URL only when the Medium text is duplicate or near-duplicate of the proprietary site page.

Never set the website canonical URL toward Medium.

Never set a custom canonical on Medium-only articles, autonomous international articles, lateral notes, poems, events, book material, tools or content not equivalent to a proprietary site page.

## Cerchi d’inchiostro guide rules

Cerchi d’inchiostro guides must remain coherent across:

* hero;
* cover;
* index/table of contents;
* editorial opening;
* proprietary sections;
* CTAs toward the Cerchi hub;
* navigation toward already published guides;
* JSON-LD where present;
* BreadcrumbList where present.

Do not create links to future unpublished guides.
Do not increase visible Home guide cards beyond 9.
Do not use `Delos` as the public operating name.

## SEO/GEO rules

Goal:
Improve clarity, indexability, internal linking and semantic comprehension without forcing.

Rules:

* do not change slugs to force indexing;
* do not modify canonicals without evidence;
* do not resubmit sitemap unnecessarily;
* do not add artificial links;
* do not duplicate CTAs or functional blocks;
* prefer editorially relevant internal links;
* keep sitemap limited to public canonical URLs;
* verify public pages do not have `noindex`;
* do not make private/test/reference pages public.

## Google Search Console workflow

When work affects public SEO/indexing, follow this sequence:

1. real patch;
2. deploy;
3. live check;
4. URL inspection;
5. live URL test;
6. request indexing only for a few strategic URLs;
7. avoid massive requests;
8. wait 24–48 hours before broad revalidation;
9. monitor without compulsive resubmission.

Typical priority URLs:

* Home;
* `saggi.html`;
* `archivio.html`;
* `cerchi/`;
* new essays;
* new guides;
* key non-indexed pages.

## Required final report for every task

Every final Codex response must include:

1. files modified;
2. protected files not modified;
3. summary by file/group;
4. confirmation that SEO constraints were respected;
5. confirmation that main editorial texts were not rewritten;
6. local links checked;
7. JSON-LD validated if present;
8. tests/checks executed;
9. commit created;
10. PR created, or confirmation that no PR was opened.

## Minimum testing

Run when relevant:

* HTML parsing;
* local link checks;
* JSON-LD validation;
* Medium link verification when involved;
* verification that `sitemap.xml` and `robots.txt` were not modified;
* verification that canonical/meta/H1 stayed unchanged when protected;
* `git diff --check`;
* `git status --short` after commit.

## Operating style

Be conservative.
Be concise.
Do not “improve” what was not requested.
Do not expand the scope.
Do not perform unnecessary aesthetic refactoring.
Do not create new variants.
When a structure has been standardized, preserve it.
