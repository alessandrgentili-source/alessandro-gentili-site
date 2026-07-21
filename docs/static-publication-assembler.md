# Static publication assembler

This repository uses a restricted GitHub Actions workflow to assemble large, pre-validated static publication bundles on `publish/**` branches.

The workflow:

- runs only when staged publication files change on a `publish/**` branch;
- requires exactly one SHA-256 manifest;
- verifies bundle integrity before extraction;
- rejects absolute paths, traversal paths, duplicate members, links and special files;
- accepts only guide pages, Cerchi index/triadi pages, Cerchi image assets and `sitemap.xml`;
- enforces conservative limits on archive size and member count;
- commits only to the same publication branch;
- never publishes directly to `main`.

Public changes still reach `main` exclusively through a reviewed pull request.
