# INTERNATIONALIZATION ROLLOUT — v6 / TRIAD 05

Date: 2026-09-24
Branch: `internationalization-v6-triad-05`
Baseline: `1c4c0fa97288762dce0ca4c34ff0f7240aa37712`

## Scope

Localize the fifth Italian Cerchi d'inchiostro triad as the sixth complete English cluster:

**Averroes — Georg Simmel — Adam Smith**
**Threshold:** Interpretation, money, exchange.

## Editorial source rule

The English pages are derived from the existing Italian guides and preserve:
- the central human problem of each author;
- core conceptual distinctions and explicit cautions;
- the contemporary wound;
- primary-source and critical orientation.

They are editorial localizations rather than literal translations.

## English canonical URLs

- /en/cerchi/guides/averroes-reason-interpretation-law/
- /en/cerchi/guides/georg-simmel-money-metropolis-individuality/
- /en/cerchi/guides/adam-smith-exchange-sympathy-wealth/

## Shared relation

The Italian triad asks what holds a civilization together when:
- meaning must be interpreted;
- value becomes comparable;
- trust makes exchange among strangers possible.

English editorial question:

> What lets strangers share a world when meaning must be interpreted, value made comparable and exchange sustained by trust?

## Technical integration

Required:
- reciprocal hreflang on the three Italian guides;
- explicit language-switcher pairs;
- sitemap and llms.txt update;
- English gateway / Cerchi / Triads / Themes expansion;
- i18n checker expansion from 22 to 25 canonical English pages and from 19 to 22 reciprocal IT/EN pairs;
- CI, Archive regression, GitHub Pages deployment and artifact QA.

## Out of scope

- no seventh English triad;
- no essay localization;
- no Archive language filter;
- no Italian URL migration or body rewrite.
