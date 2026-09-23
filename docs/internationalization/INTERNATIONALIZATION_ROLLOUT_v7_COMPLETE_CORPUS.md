# INTERNATIONALIZATION ROLLOUT — v7 / COMPLETE CORPUS

Date: 2026-09-24
Branch: `internationalization-v7-complete-corpus`
Baseline: `a06dc6f633fdc24d1b204f78307c15cef602ee40`

## Goal

Complete the English Cerchi d'inchiostro author corpus and triad architecture.

Before this rollout:
- 18 / 24 author guides localized;
- 6 / 8 triads complete.

After this rollout:
- **24 / 24 author guides localized;**
- **8 / 8 triads represented in English;**
- no Italian URL migration;
- Italian source pages remain canonical for Italian.

## Triad 06 — Republic, opinion, decision

- Cicero — republic, law and civic speech
- Alexis de Tocqueville — democracy, opinion and liberty
- Nicolas de Condorcet — education, progress and collective decision

Shared editorial question:

> What makes political freedom durable — a common republic, citizens capable of acting together, and procedures that turn judgment into revisable collective decision?

## Triad 07 — Elite, mass, government

- Polybius — constitution, power and decline
- Gaetano Mosca — political class, organization and real government
- Vilfredo Pareto — elites, residues and circulation

Shared editorial question:

> How do political form, organization and the circulation of ruling groups shape government without reducing politics to conspiracy?

## English canonical URLs

- /en/cerchi/guides/cicero-republic-law-civic-speech/
- /en/cerchi/guides/alexis-de-tocqueville-democracy-opinion-liberty/
- /en/cerchi/guides/nicolas-de-condorcet-education-progress-decision/
- /en/cerchi/guides/polybius-constitution-power-decline/
- /en/cerchi/guides/gaetano-mosca-political-class-organization-real-government/
- /en/cerchi/guides/vilfredo-pareto-elites-residues-circulation/

## Editorial source rule

All six English guides are derived from their Italian source guides. They preserve:
- the central human or political problem;
- conceptual distinctions;
- explicit limitations and cautions;
- the contemporary wound;
- primary-source orientation.

No missing argument is silently filled with general knowledge.

## Technical completion

Required:
- six reciprocal IT/EN hreflang pairs;
- language switcher map completed for all 24 guides;
- sitemap and llms.txt completed;
- English gateway / Cerchi / Triads / Themes updated to full corpus;
- i18n checker expanded from 25 to 31 canonical English pages and from 22 to 28 reciprocal IT/EN pairs;
- CI source coverage expanded to all 24 Italian guides;
- Archive regression, Pages deployment and exact-artifact QA.

## Completion criterion

The internationalization task is closed only when:
1. PR gates pass;
2. changes are merged to main;
3. post-merge gates pass;
4. GitHub Pages deploy succeeds;
5. deployed artifact passes i18n, Archive and publication checks;
6. all local links/assets/anchors across canonical English pages pass structural QA.
