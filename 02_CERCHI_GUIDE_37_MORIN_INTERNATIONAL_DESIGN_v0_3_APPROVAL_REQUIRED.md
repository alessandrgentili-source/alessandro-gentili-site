# Cerchi d’inchiostro — Guide 37 Edgar Morin
## International edition · Editorial design specification · Candidate v0.3 · Awaiting author approval

**Status:** Design specification for the reviewed English candidate v0.3. The editorial text still requires explicit author approval; this specification does not authorise HTML conversion, code changes, PR or publication.

**Source of truth after human approval:** `01_CERCHI_GUIDE_37_EDGAR_MORIN_INTERNATIONAL_v0_3_APPROVAL_REQUIRED.md`. The source Italian `CERCHI_GUIDA_37_EDGAR_MORIN_FINALE_CANDIDATA_v1_0.md` remains untouched. Its CECMAS date (1959) conflicts with the checked 1960 founding date: resolve as a separate IT editorial correction before claiming complete factual parity.

## 1. Design idea — The observer is inside the frame

A reader should experience Morin's argument as a series of changes in scale: a person before a camera; a filmed situation; an interpretation open to challenge; a whole intellectual project; and finally an action whose consequences change the world in which it began.

The page should remain a sustained essay. Its distinctive feature is the movement between **frame, relation and revision**. The visual system must make that movement intelligible, not merely repeat words such as *complexity* or decorate the page with circles.

**Visual principle:** A boundary makes a phenomenon visible; a second line reveals what the boundary has excluded; a return line shows the possibility of correction. Use editorial rules, aligned marginalia, dates and subtle ink marks. No technical network wallpaper, glowing nodes, animated fractals or schematic 'everything connects' illustration.

## 2. Observed International benchmark on current `main`

Read-only inspection of the published English guides:

- `en/cerchi/guides/enrico-mattei-energy-public-enterprise-autonomy/index.html`
- `en/cerchi/guides/aristide-merloni-enterprise-fate-of-places/index.html`
- `en/cerchi/guides/adriano-olivetti-community-power/index.html`

All three use the established **International Atlas** reading architecture: international masthead, guide hero, cover, contents/navigation rail, structured editorial sections, shared stylesheet and a guide-specific visual layer. They differ in the treatment of their subject matter; there is no need to copy one page's sections or visual devices into Morin.

At implementation time, read those paths again from the current `main`. The exact current template, components, scripts and CSS remain authoritative; this specification cannot override them.

## 3. Page architecture

**Hero:** the text title *Edgar Morin — Knowledge and Its Blind Spots* is the dominant H1. Set the Guide 37 and Triad 13 metadata discreetly. Keep the original approved cover unchanged; there is no separate English cover or new brand mark. Its position and alt text must respect the existing International Atlas hero and actual approved asset path. Do not infer an asset that is not on `main`.

**Reading rail:** use the International Atlas contents rail, with all 31 listed items in their exact order. The Introduction is a separate opening section and may receive its own heading/anchor outside the numbered list, following the existing accessible Atlas convention. Every entry must resolve to a real heading ID. Preserve the accessible skip link, visible focus styles, semantic `<nav>` and text-based navigation with JavaScript disabled. On narrow screens the contents may use the native responsive pattern already approved in the site's current CSS.

**Body:** maintain the complete source Markdown in reading order. The prose of the introduction, Plozévet, contemporary wound, critical argument and closing must flow as prose rather than be broken into sequences of cards or accordion panels.

**Rhythm:** alternate long-form reading width with occasional narrow marginal notes, sectional year markers, clearly typeset enumerations and three special treatments described below. The text must remain fully legible and meaningful at mobile width with no interaction. No accordion or graphical treatment may omit the new historically anchored passages in Modules II–III.

## 4. Three distinct interpretive treatments

### Module I — The camera inside reality

**Editorial form:** a restrained three-plane film-strip or field-note sequence, using the exact distinctions already present in the module:

1. The interviewees' lives outside the film.
2. The situation created by the camera.
3. The edited representation reviewed by the participants.

Treat these as three aligned layers on desktop, perhaps with fine rules and overlapping offsets that show the relationship among them. On mobile they become a linear progression. No photographs, extra claims or fabricated film stills are required. Crucially, the complete prose stays visible below or alongside the visual treatment, unchanged.

**Meaning:** the visual makes the difference between phenomenon, encounter and representation visible. It must not imply that scientific observation in every field operates in exactly the same way; the qualifying paragraph in the Markdown is essential.

### Module II — The price of an explanation

**Editorial form:** four questions presented as one annotated margin-led inquiry, not four promotional cards:

- What does it bring into view?
- What does it leave out?
- Which relationships does it consider?
- How might it be corrected?

Use a single vertical reading line with four numbered thresholds and substantial typography. The explanatory text belonging to each question is retained verbatim, as are the four exact question labels in the approved English Markdown. On desktop it can occupy a wider inset within the article; on mobile the line and descriptions stack in ordinary reading order.

**Meaning:** the reader sees a method of evaluating one explanation. Do not present it as Morin's formal protocol or as a scientific certification test. Retain the explicit distinction between Morin's theory and the original editorial reading by Cerchi d’inchiostro.

### Module III — When a decision changes the problem

**Editorial form:** the revised module now begins in Morin’s political and intellectual biography, moves to the conceptual distinction between a *programme* and a *strategy*, and only then offers a clearly labelled illustrative public-policy situation. Give these three movements typographic breathing room without separating the essay into decorative cards.

**Visual treatment:** two fine editorial trajectories, **programme** (fixed path through assumed conditions) and **strategy** (a path visibly revisable as circumstances change), may run as marginal guides next to the **existing prose**. The four analytical terms **intention / intervention / consequences / correction** remain in the text in this order; they must not become a generic process diagram or imply that correction is automatic. They can be given minimal in-line emphasis, without new labels, claims, or additional copy.

**Meaning:** action may change the situation in which it must operate. The revised layout should expose the tension between pre-set execution and revisable judgment, not promise that an actor can restore control or avoid every unintended consequence. The complete prose and its historical qualifications remain visible without JavaScript.

## 5. Other editorial devices

**The six volumes of *La Méthode*.** Keep the six numbered entries, French titles, publication years, conceptual descriptions and order. A restrained vertical chronology with years set in a consistent margin is appropriate; do not turn these into six detached card summaries. The 1983–84 preparatory manuscript discussion belongs in the following prose and must remain in context.

**Plozévet.** Give the section room to breathe, perhaps with a quiet typographic locator `Plozévet / Finistère / 1960s` only if treated as visual metadata and verified against the text. It is a historical case and an argument about representation; a tourist image or fictionalised map would distort its purpose.

**The constellation.** Keep its five categories in their present prose and order: antecedents; sciences and interlocutors; dialogues and reception; disagreements and corrections; the present. A small editorial index may help the reader move between them, but do not flatten documented influences, general comparisons and later reception into one uniform graphic network.

**Key concepts and glossary.** Keep all definitions complete. Distinguish the deep interpretive exposition of Key Concepts from the concise reference function of the Glossary. A definition-list treatment can aid scanning. No duplicated concepts or collapsed content.

**Limits and contradictions.** Present the sustained criticism as the necessary counterweight to the conceptual modules. Scholar names and precise objections are important; avoid both warning-colour boxes and a decorative 'pros and cons' scorecard.

**FAQ.** Maintain all twelve questions and answers in exact order. If disclosure is used, the current site's native accessible pattern must work without custom JavaScript, and no answer may disappear from machine-readable or no-interaction reading. A visible linear FAQ is preferable if the existing component would otherwise hide substantive text.

**Reading paths and Continue reading.** Preserve the five routes and six referenced published authors. Only add URLs after checking the exact relevant English or Italian published page. Do not create EN links to Carson, Keynes or the Triad 13 page until those destinations exist and have been verified live.

## 6. International language, links and metadata

- Use the full English editorial text; French book titles remain in the original language, retaining their accents and italics.
- `Cerchi d’inchiostro` remains the canonical project name; `Circles of Ink` remains the English entry designation, not a separate cover brand.
- Treat parenthetical English renderings of Alessandro Gentili's Italian essay titles as reading glosses, **not** as claims that English editions are already published.
- Create canonical, hreflang, breadcrumbs, `Article`, and `FAQPage` only after the final approved paths are checked on `main` and live. FAQPage must match all twelve visible English FAQ questions and answers exactly.
- Maintain existing International Atlas header, footer, `assets/script.js` and any required shared styles. Do not remove, bypass or weaken current CI.
- No redesign of the main site, shared atlas, or previously published Italian/English guides.

## 7. Accessibility and responsive acceptance

1. Complete text readable at 320–375 px and desktop without horizontal scrolling.
2. One H1, nested heading hierarchy, full TOC and resolved anchors, meaningful link labels.
3. Semantically ordered text before and after CSS enhancement; decorative lines marked appropriately and not exposed as empty controls.
4. High-contrast ink typography, keyboard access, visible focus and reduced-motion support wherever relevant.
5. Three conceptual treatments comprehensible without movement, hover or JavaScript.
6. Tables only when supported by actual comparable data; no table required merely to make the page appear varied.
7. No cards/graphics that replace paragraphs, omit qualifiers, rewrite headings or invent quotations.

## 8. STOP conditions and publication boundary

**Stop** before any HTML generation unless the v0.3 English text is expressly approved, the factual CECMAS divergence with IT is resolved, and the separate Triad 13 publication trigger is satisfied. Also stop if the HTML transformation paraphrases, omits or rearranges the approved English Markdown; if any of the twelve FAQ responses differs from `FAQPage`; if the source cover is missing; if a linked destination is unverified; if the proposed styling requires an unapproved redesign; or if the resulting page is illegible in mobile or keyboard navigation.

Current output is an **editorial/design candidate after consolidation of four external reports**. The reports do not substitute for author approval. The present three-file ZIP is a controlled review and deferred-handoff packet, not a publishing instruction. The external checks were not full page-level verification of every source. No publishing task begins without explicit fresh authorisation.
