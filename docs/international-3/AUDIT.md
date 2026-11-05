# International 3.0 — audit and design scope

Baseline: `e9df7f0f853e35c0cd70f60b3b4b5011efe1cae4` (latest remote main verified 2026-11-05). No open PRs at preflight. PR 280 is closed and is not a source for this work.

## Findings on main

- 33 Italian guides; 24 English guides; 11 English triad introductions. Only triads 01–08 have three English guide destinations.
- Triads 09–11 send the reader exclusively to Italian guides and expose an obsolete “coordinated release candidate” sentence.
- The Cerchi hub has 24 almost identical cover cards, ordered 08, 01–07. No author/concept lookup, no compact complete index, no routes crossing triads.
- All 24 guides share a sequence of full-width rounded panels. At 1265px, body lines span roughly 100 characters. The contents are disconnected from the current reading position. Sources and onward navigation are weakly differentiated.
- Themes has ten entries, but its two foundational paths lead into Italian. Eight other entries largely repeat triad destinations rather than exposing cross-triad connections.
- Main's four existing gates pass, including the gate that **requires** the last nine Italian guide links in English Triads. A passing legacy check does not establish English autonomy.
- Static language links and 28 reciprocal hreflang pairs already exist. The nine missing pairs must not be invented before approved English pages exist.
- sitemap.xml contains existing English pages. No new URL may be added for a Markdown candidate. llms.txt conflates rollout order and triad number and needs a clearer current inventory.
- Archive is an Italian catalogue with a working International entry. No structural change is needed there. The Italian home, body texts, covers and shared footer are protected.

## Reference analysis

Reference: https://rikiyat.github.io/blog/weight-space-programming/ (read and inspected visually 2026-11-05).
The transferable lesson is that a representation answers the question posed by the adjacent argument; detail can be inspected without obscuring the main reading path. Alternating scales and persistent evidence help a long text retain its shape. Cerchi uses questions, distinctions and editorial relations rather than imitating experimental dashboards or animation.

## Concrete proposal: an atlas of questions

1. Hub: an editorial opening; one featured triad; three cross-triad routes; a searchable, statically complete author directory grouped into eleven numbered relations.
2. Triads: existing questions and author lenses preserved, connected to approved cover images and individual guide destinations; a visible return to the complete index.
3. Guides: original narrative blocks retained byte for byte, a readable serif column, sticky desktop contents, mobile native disclosure, visible authorship and sources; an inserted relation plate reproduces the existing triad lenses and gives direct peer-guide access. It is labelled as an editorial comparison, never a claim of historical influence.
4. Themes: English routes across existing guides, with the rationale beside the links. Existing descriptions retained. Italian background is explicitly optional.
5. Home: a curated doorway into these routes, existing macro-cover preserved. No full guide archive on the home.
6. No runtime library, web font, external search service or generated bitmap. CSS is loaded only on the changed EN surfaces; all substantive content/relations are static HTML.

## Initial scope, superseded by the prototype request

`en/index.html`, `en/cerchi/index.html`, `en/cerchi/triads/index.html`, 24 existing `en/cerchi/guides/*/index.html`, `en/themes/index.html`, relevant inventory copy in `en/positioning/index.html`, new scoped CSS/JS, discovery documentation, tests, and publication-policy correction. New Markdown manuscripts live on a separate editorial branch.

Protected and unchanged: Italian design/body texts, all approved images, footer markup/styles, global CSS, current canonical/hreflang URLs, Italian home, archive, robots.txt. Sitemap and the missing language-map pairs remain gated until nine approved HTML editions exist. No main modification, merge or deployment.

## Acceptance and approval boundaries

The prototype is reviewable before publication. It must demonstrate narrower reading measure, direct peer-guide access, cross-triad exploration, keyboard navigation, mobile fit and full narrative availability without JS. Integrity tests compare original guide blocks and protected assets to baseline. Existing gates and new atlas-specific checks run after implementation.

**This branch is not a completed 33-guide release.** Triads 09–11 remain explicitly pending English manuscripts; they cannot be presented as completed or replaced by Italian-only routes. The final release must reject pending statuses and require 33 English guides, 11 complete triads, reciprocal language pairs, sitemap/discovery alignment and human-approved manuscripts.

At initial audit, the Project normative files were unavailable. They were subsequently supplied and read; see the scope update below.

## Scope update — first prototype

The subsequent user request narrows implementation to the English Cerchi hub and the existing Pasolini guide. All preparatory changes to other pages have been withdrawn. Nine manuscripts are explicitly deferred and have not been started. The seven original normative files supplied from Desktop were read; current conversation decisions take precedence. The audit above remains a historical diagnosis, not a release plan for this branch.
