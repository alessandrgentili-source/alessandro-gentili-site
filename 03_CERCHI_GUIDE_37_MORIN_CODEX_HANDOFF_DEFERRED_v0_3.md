# CERCHI D’INCHIOSTRO — GUIDE 37 EDGAR MORIN — DEFERRED CODEX HANDOFF

**Status: EDITORIAL CANDIDATE v0.3 — AWAITING AUTHOR APPROVAL. READ ONLY. DO NOT PUBLISH.**

**Date:** 17 November 2026  
**Scope:** English guide 37 only. Italian guide 37 and all other guides, shared styles, covers, hubs and sitemap remain outside the authorised scope.  
**Repository:** `alessandrgentili-source/alessandro-gentili-site`.

## 1. Packet manifest

This ZIP contains exactly three `.md` files:

1. `01_CERCHI_GUIDE_37_EDGAR_MORIN_INTERNATIONAL_v0_3_APPROVAL_REQUIRED.md` — complete English editorial candidate. **Never paraphrase, shorten, reorder or complete it from memory during HTML conversion.**
2. `02_CERCHI_GUIDE_37_MORIN_INTERNATIONAL_DESIGN_v0_3_APPROVAL_REQUIRED.md` — visual specification; distinct from the text and incapable of authorising editorial changes.
3. `03_CERCHI_GUIDE_37_MORIN_CODEX_HANDOFF_DEFERRED_v0_3.md` — deferred instructions, safeguards and approval gates.

The Italian source (not included here) is `CERCHI_GUIDA_37_EDGAR_MORIN_FINALE_CANDIDATA_v1_0.md` and has **not** been modified.

## 2. Permission boundary — DO NOT EXECUTE

**At upload time CodeX may only:** inspect these three documents, identify missing prerequisites, compare the existing read-only repository structure and report a bounded preflight. Do not create a branch, add assets, alter files, generate HTML, open a PR, deploy, edit SEO or update the sitemap. Do not infer author approval from the existence of this ZIP.

Wait for a **new, explicit publishing command from Alessandro Gentili**, given only after the checks below. An instruction to inspect, load or retain the packet is not that command.

## 3. Editorial consolidation of external audits

The user supplied independent reports attributed to Claude, Gemini, DeepSeek and Qwen. Claude’s critique was more demanding on Modules II and III; the others broadly considered the structure satisfactory. Agreement between models has not been taken as proof.

**Evidence-backed corrections accepted in v0.3:**

- CECMAS formed in **January 1960**, not 1959. Contemporary journal editorial: *Communications* 1 (1961), pp. 1–2, accessible at `https://www.persee.fr/doc/comm_0588-8018_1961_num_1_1_2211`.
- UNESCO *Pour une réforme de la pensée*: **do not change the date to 1996** based on the audit speculation. UNESCO’s page for this exact title is dated **24 May 2019**: `https://courier.unesco.org/fr/articles/pour-une-reforme-de-la-pensee`; the English bibliography now specifies the date as that of the *online edition*, without making an unverified claim about the first historical appearance of the text.
- Morin’s Plozévet case: named source Bernard Paillard, “Plozévet et l’affaire Morin” (2022), `https://bcd.bzh/becedia/fr/plozevet-et-l-affaire-morin`. Historical synthesis: André Burguière, *Bretons de Plozévet* (Flammarion, 1975), documented in `https://www.persee.fr/doc/rhmc_0048-8003_1977_num_24_2_980_t1_0310_0000_1`.
- 2024 manuscript title standardised to *La Méthode de La Méthode: Le manuscrit perdu*, consistent with the Fondation Edgar Morin bibliography, `https://fondationedgarmorin.org/loeuvre/`.

**Selective editorial changes:** Module II now tests explanatory limits against Plozévet and differentiates correction of a *description* from correction of an *action*; the Essay 0 digression is removed from the module but the essay remains named later. Module III is anchored in Morin’s already-documented political self-criticism, then develops programme/strategy and a labelled hypothetical policy case. The four conceptual terms are kept in prose; the text no longer presents them as a fixed four-stage policy cycle. Dialogics versus logic, the transdisciplinary wager, two awkward phrases and the closing have been tightened. These are substantive changes: **author approval remains outstanding**.

**Not automatically adopted:** adding a 2002 Morin political controversy (outside the authorised scope and not a necessary correction), adding unsupported claims about the effect of Morin’s political commitments, and cosmetic rewrites suggested without substantial justification.

## 4. Pending editorial gates and STOP

- **GATE EN-1 — Human approval:** author must explicitly approve the complete v0.3 English Markdown. This has not yet happened.
- **GATE IT-2 — Factual parity:** the Italian `1959` CECMAS claim conflicts with the now-verified `1960` date. Do **not** silently edit the Italian approved source or revert EN to the wrong date. Obtain permission for a separate, narrowly scoped Italian editorial correction or explicit editorial reconciliation before publication.
- **GATE SOURCE-3 — Accuracy:** the four external reports did not all verify the primary editions or every secondary work. Treat the bibliography as partially checked; do not represent it as a page-level philological audit. If a material error appears during implementation, STOP and return to the source Markdown.
- **GATE TRIAD-4 — Publication trigger:** per the Project’s 13 November 2026 rules, do not publish this guide as part of Triad 13 unless all three guides (37 Morin, 38 Carson, 39 Keynes) are prepared and explicitly approved in IT/EN, with their three-file packages and the three approved 1600×900 covers in JPG/WebP, and the Medium EN draft with the Italian editorial note prepared; obtain a separate explicit human publishing instruction.
- **GATE COVER-5:** verify Morin’s actual approved WebP asset on `main` before any PR. This packet contains no cover and does not invent a path.

**STOP if any gate is unmet.** No branch or PR may substitute for missing approval.

## 5. Current repository observations — verify again before publishing

Read-only checks on `main` during packet preparation found **no** URLs for Morin, Carson, or Keynes in `sitemap.xml`. This observation does **not** establish that pages or unpublished assets are absent. The current English guide architecture uses `/en/cerchi/guides/` (plural), not `/en/cerchi/guide/`. Use the current `main`, not these historical observations, for technical truth.

Read three mature, recent EN pages before future implementation, including:

- `en/cerchi/guides/enrico-mattei-energy-public-enterprise-autonomy/index.html`
- `en/cerchi/guides/aristide-merloni-enterprise-fate-of-places/index.html`
- `en/cerchi/guides/adriano-olivetti-community-power/index.html`

All three use International Atlas conventions; they are benchmarks, not rigid templates. Do not redesign shared styles, the home page, macro-covers, or older guide generations.

## 6. Future implementation — ONLY AFTER fresh explicit authorisation

1. Fetch updated `main`, inventory the exact existing Italian/English URLs and assets, validate prerequisites, and determine the strictly necessary EN scope. **Do not assume the IT standard three-file scope applies to EN.** Explicitly agree on the affected EN page, hub, sitemap, reciprocal language links and any other necessary surfaces before writing.
2. Confirm the canonical English slug against the current architecture. No invented `hreflang`, cover path, cross-guide URL or future Triad 13 URL.
3. Create a branch from latest `main` according to procedure v2.1, strictly scoped to approved files. Source editorial Markdown remains a separate approved source; no source draft should enter the public publication PR.
4. Convert the **approved exact Markdown** into the current International Atlas template, retaining all sections, 31 contents entries, three modules, 18 glossary items and 12 FAQ Q/A pairs in their exact words and order. Use only visuals specified by the approved design; no generated fake stills or decorative cards.
5. Run existing CI and additional preflight: one H1; header/footer, canonical, `Article`, `BreadcrumbList`, `FAQPage` with exact visible Q/A parity; links, anchors, cover, shared `/assets/script.js`; semantic IT/EN navigation even without JavaScript; keyboard, 320px/mobile, responsive tables, reduced motion; no horizontal overflow. Count text sections and compare to the approved source, not to a page fragment.
6. Open a PR only after passing checks and approved scope. **STOP BEFORE MERGE.** Human review, `Squash and merge`, live checking, sitemap checking and Search Console follow separately. CI green never equals human approval, deployment, or indexing.

## 7. One instruction for CodeX at the current moment

> Read this ZIP as a **candidate awaiting approval**. Perform only a READ-ONLY inventory of prerequisites and possible technical blockers. Do not edit the repository, create branches, generate HTML or publish. Report the missing author approvals, Italian CECMAS reconciliation, assets, triad prerequisites and proposed EN scope. Stop.

## 8. Closing state

`EN v0.3 CANDIDATE` → `AWAITING AUTHOR APPROVAL` → `IT FACTUAL RECONCILIATION` → `TRIAD/COVER/MEDIUM TRIGGER` → `NEW PUBLISHING MANDATE` → `CODEX IMPLEMENTATION` → `PR REVIEW` → `LIVE VERIFICATION`.

**This packet is prepared for controlled handoff, not approved for publishing.**
