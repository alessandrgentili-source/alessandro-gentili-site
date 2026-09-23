# INTERNATIONALIZATION ARCHITECTURE DECISION — v1

Date: 2026-09-23
Status: implemented in branch `internationalization-v1-english-pilot`

## Decision

Italian remains at the existing canonical paths. No `/it/` migration.

English uses a clean `/en/` subtree:
- `/en/`
- `/en/cerchi/`
- `/en/cerchi/triads/`
- `/en/themes/`
- `/en/positioning/`
- `/en/method/`
- `/en/system/`
- three complete English author-guide editions for Manzoni, Collodi and Pasolini.

Legacy English entry points `/en.html`, `/metodo-ai.html`, `/strumenti.html` remain reachable but become non-canonical compatibility pages pointing to the new `/en/` URLs. There is no browser-language redirect.

## Navigation

Language and professional architecture are separate:
- language selector: **IT | EN**
- professional area: **International → Positioning / Method / System**

The selector uses explicit links and falls back to the English gateway when the current Italian page has no English edition yet.

## hreflang

For actual IT/EN content pairs:
- self canonical on both pages;
- reciprocal `hreflang="it"` and `hreflang="en"`;
- `x-default` points to the established Italian canonical.

No fake hreflang pairing is created for pages without a true equivalent.

## Sitemap and crawlability

The sitemap contains canonical public English URLs only.
Legacy English root pages are removed from the sitemap after their canonical moves to `/en/`.
`robots.txt` remains permissive and unchanged.

## Structured data

English hubs use `CollectionPage` or `WebSite` with `inLanguage: "en"`.
English guides use `Article` plus `BreadcrumbList`, with English canonical URLs and `inLanguage: "en"`.

## Archive

The Archive is not converted in v1. Current static Archive invariants remain untouched.
Phase 2 may introduce explicit language metadata/filtering only after the bilingual corpus becomes large enough to justify it.

## Pilot rationale

The pilot is intentionally small but complete. The Manzoni–Collodi–Pasolini triad demonstrates:
1. paired IT/EN author pages;
2. a coherent English editorial relation rather than isolated translations;
3. internal linking from hub → triad → guides → themes;
4. different international query families (Manzoni/language/nation; Pinocchio/education/desire; Pasolini/consumer culture);
5. a reusable template for future guide localization.

## Editorial localization criteria

Preserve thesis, conceptual structure, sources, interpretation and authorial identity.
Adapt title, syntax, idiom, terminology and search language where necessary.
Do not Americanize European authors or turn guides into generic SEO explainers.

## Rollout after v1

Priority order:
1. complete the strongest remaining triads in English;
2. expand Themes only when at least two English source nodes support each theme;
3. selectively localize essays with international query potential;
4. only later internationalize civic-writing and portfolio material;
5. evolve Archive language filters when English volume makes them useful.

## Risks and mitigations

- Duplicate legacy English pages → canonical + noindex compatibility treatment.
- Partial English experience → English navigation links only to completed English pages.
- SEO dilution → no Italian URL changes; reciprocal hreflang only on true pairs.
- Translation flattening → editorial localization and full English guide editions.
- Maintenance drift → automated i18n consistency check in CI.

## Work estimate

v1 establishes the reusable infrastructure and pilot cluster.
A full 24-guide / 8-triad English rollout is a multi-phase editorial program, not a mechanical translation batch; with the templates and checks now in place, each subsequent triad can be localized independently without architectural changes.
