# Static publication assembler

This repository uses a restricted GitHub Actions workflow to assemble large, pre-validated static publication bundles on `publish/**` branches.

The workflow:

- runs only when staged publication files change on a `publish/**` branch;
- requires exactly one SHA-256 manifest;
- verifies bundle integrity before extraction;
- rejects absolute paths, traversal paths, symbolic links and files outside the approved publication scope;
- commits only to the same publication branch;
- never publishes directly to `main`.

Public changes still reach `main` exclusively through a reviewed pull request.
