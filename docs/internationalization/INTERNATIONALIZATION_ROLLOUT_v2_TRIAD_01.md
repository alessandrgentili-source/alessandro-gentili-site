# INTERNATIONALIZATION ROLLOUT — v2 / TRIAD 01

Date: 2026-09-24
Branch: `internationalization-v2-triad-01`
Baseline: `7b3e1e5f839db37152cfab8ec72ead59a197cf1b`

## Scope

Complete the second English editorial cluster by localizing the first Italian triad:

**Plato — Dante — Machiavelli**
**Threshold:** Truth, language, power.

This is the second complete English triad after Manzoni–Collodi–Pasolini.

## Editorial source rule

The English pages are based on the existing Italian guides and preserve:
- each guide's conceptual thesis;
- its central biographical wound;
- the contemporary wound;
- the relation between author, works and present-day question;
- primary-source orientation and critical cautions.

They are not literal translations and do not copy the full Italian table of contents. They use the compact English guide architecture established in v1.

## English canonical URLs

- /en/cerchi/guides/plato-ideas-truth-power/
- /en/cerchi/guides/dante-exile-language-divine-comedy/
- /en/cerchi/guides/machiavelli-power-state-effectual-truth/

## Triad relation

The Italian triad defines the first threshold as:
- Plato — truth, ideas, power;
- Dante — exile, language, vision;
- Machiavelli — power, state, effectual truth.

The shared question is localized as:

> How can a city distinguish truth, give shared form to experience, and confront power as it actually works?

This preserves the Italian threshold rather than replacing it with a generic leadership or political-philosophy frame.

## Technical integration

Required:
- reciprocal hreflang on the three Italian guides;
- language-switcher pairs;
- sitemap entries;
- llms.txt graph update;
- English hub / triads / themes / gateway update;
- expansion of i18n consistency checks from 10 to 13 English canonical pages and from 7 to 10 reciprocal IT/EN pairs;
- CI + Archive regression + GitHub Pages deploy verification.

## Out of scope

- no new Italian URL;
- no Italian content rewrite;
- no third English triad in this task;
- no Archive language filter yet;
- no essay localization yet.
