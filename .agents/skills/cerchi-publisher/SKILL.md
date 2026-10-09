---
name: cerchi-publisher
description: Prepare a new Cerchi d'inchiostro author guide from final editorial text and a cover in this repository. Use for a new guide draft and its local validation or preview; do not use to revise published guides.
---

# Cerchi d'inchiostro Publisher

Ask for the definitive body text (paste or UTF-8 `.txt`/`.md`) and the cover. Ask only for missing essentials such as the author, source notes or intended triad. Keep the supplied manuscript available as a separate source file for comparison; do not rewrite or summarize it.

Read the repository `AGENTS.md` and `docs/cerchi-guide-standard.md`. Compare `.github/templates/cerchi-guide-template.html` with the most recent coherent published guide. Treat `AGENTS.md` as authoritative where they differ. The template contains placeholders and incomplete JSON-LD, so never publish it unchanged.

1. Check Git status and the latest published guide number, then propose the next number, a unique slug and the cover name `cerchi-guida-NN-nome-autore-temi-principali-1600x900.webp`. Confirm any editorial choice that cannot be inferred from the final text.
2. Prepare only a new `cerchi/guide/<slug>/index.html` and its 1600×900 WebP cover. If the supplied image needs conversion, use an already available local tool or request a suitable cover; never alter a published asset. Preserve every supplied paragraph in order while adding HTML markup. Keep hero compact; place the editorial opening after cover and `.guide-toc`. Match index labels to section H2 and IDs. Finish with Fonti, Prosegui la lettura, Chiusura editoriale. Link only to existing, relevant pages.
3. Fill self-canonical metadata, Open Graph, Twitter, Article and BreadcrumbList. Include FAQPage only for visible FAQ. Use the existing header, footer, stylesheet and script. Keep drafts outside the public tree until approved for a real guide.
4. Validate the candidate with `python3 tools/validate-cerchi-guide.py PATH/cerchi/guide/<slug>/index.html --cover PATH/cover.webp --source PATH/manoscritto.txt`. The source file contains the definitive guide body, separated into paragraphs; simple Markdown headings, lists and inline emphasis are supported. The validator checks source blocks in order. Review the rendered wording against the source as well; this mechanical check cannot judge editorial equivalence.
5. Preview locally from the directory containing `cerchi/` and `assets/`: `python3 -m http.server 8000 --bind 127.0.0.1`, then open `http://127.0.0.1:8000/cerchi/guide/<slug>/`. For a temporary candidate, assemble its page and cover in a temporary site root with the repository assets available there; never add temporary material to the sitemap.

For an actual publication proposal, show the page, cover, hub card and sitemap entry together in the diff. Run the existing public-site checks and `git diff --check`. Do not publish, push, create a PR, update Triadi or change protected pages without the user's separate authorization.
