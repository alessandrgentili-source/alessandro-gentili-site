# Post-audit hardening — 2026-10-04

## Baseline and scope

Local main was fast-forwarded from `a77cf8c` to remote `f606e9b` after a clean-tree and ancestry check. Work is on `fix/site-hardening-post-audit-2026-10-04`.

Reconfirmed: missing footer/shared script in guides 25–27; ineffective in-page Analytics revocation; tablet map clipping; narrow Method arc; unbroken essay source URLs; anchors obscured by the sticky header; desktop disclosure ARIA/Escape mismatch.

Already corrected upstream: English Contact sitemap inclusion and dynamic numbered-essay inventory in archive checks. These were not changed.

No editorial body, published head metadata, canonical, hreflang, slug, sitemap, robots, image, prototype, or corpus count was edited. Home HTML is unchanged; its responsive map CSS is intentionally affected.

## Changes

- Guides 25–27 use the existing Seneca footer/shared script pattern. The guide template includes the shared stylesheet, header, footer and script.
- Analytics is disabled by default through Google's measurement-specific opt-out flag. Revocation sets the flag before denying analytics storage, expires this property's known root-path cookies, and propagates denial to other open tabs. Reacceptance reuses the initialized tag. Already transmitted requests cannot be recalled.
- Existing linear map layouts apply through 1050px, with legacy archive offsets neutralized. Desktop rules above that threshold remain unchanged.
- The Method arc stacks through 430px. Essay links can wrap without changing their text or destinations.
- Enhanced dropdowns use one shared open state for CSS and ARIA. Keyboard disclosure, Escape, outside click and focus departure are handled. A localized skip link focuses the main landmark. Sticky-header height drives anchor spacing; reduced-motion overrides include smooth scrolling. Maps retain a visible keyboard outline.

## Repeatable checks

```sh
node tools/check-archive-consistency.mjs
node tools/check-saggio-16-publication.mjs
node tools/check-i18n-consistency.mjs
node tools/check-consent-revocation.mjs
python3 tools/check-public-site.py
node --check assets/script.js
node --check assets/home-constellation.js
git diff --check
```

All passed locally. The Saggio 16 check opens a temporary loopback server.

Public-site checks parse 97 HTML documents, validate JSON-LD and 5,347 local references, verify common components, TOCs and sitemap coverage. In-memory mutations prove missing footer/script and broken fragments are detected. The i18n check inventories all 32 English pages and every Italian guide, with an explicit Italian-only decision for guides 25–27.

### Existing exceptions, not silent passes

`tools/site-hardening-legacy.json` records exactly 17 older Italian guides lacking a footer and/or the shared script. These files were outside the authorized guide repair. Checks reject new omissions and require removal of an exception when its debt is fixed. The missing-script pages do not receive script-based navigation improvements or the generated skip link in this patch. This is recorded debt, not a claim of complete site-wide accessibility.

## Browser QA

Local preview of the branch; no manual publication. Widths: 1440, 1280, 1024, 768, 430, 390, 375, 320px. Viewport height 900px, with focused navigation checks at 390×844.

15 surfaces, 120 rendered configurations: Home, Leggere il sistema, Method EN, Saggio 18, guides 25–27, Saggi, Archivio, Cerchi hub, English home, Plato EN, Portfolio, Autore, Contatti.

No global horizontal overflow or map nodes outside the viewport in the final matrix. At 768px the Home map's link boxes no longer overlap. At 1024px the full map's archive remains inside its container. At 390px Kahneman's target heading was approximately 206px from the viewport top, below the approximately 163px sticky header.

Verified desktop ArrowDown entry into the submenu, consistent expanded state, Escape closure with focus restored to the trigger, mobile open/close, and skip-link focus on `main-content`. Screenshots and the measured matrix were saved as local review artifacts under `/private/tmp/site-hardening-2026-10-04/` (not committed).

No new browser automation dependency was added. Responsive geometry and computed-style behavior are browser QA, not automated CI assertions. Reduced motion is covered by the global CSS override; OS-level preference emulation and actual 200% browser zoom were not certified. Consent regression tests execute the real consent code with a simulated DOM/storage and make no Google requests; they do not claim to recall prior network traffic or test Google's hosted implementation.

## Deferred by mandate

Prototype access controls, editorial IT/EN counts, `llms.txt`, English guide depth, International archive coverage, social links, image compression, asset cleanup and general CSS consolidation remain untouched. No merge, squash, branch deletion or manual deploy is part of this work.
