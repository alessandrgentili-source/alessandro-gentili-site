# Core corpus: legacy decisions

The 17 entries originally listed by `tools/site-hardening-legacy.json` were
reviewed individually. Their editorial generations are intentional; their
missing shared script was a real navigation defect. At 390 px the shared CSS
hides every submenu until JavaScript adds `is-open`, but these pages did not load
that script. Restore only the existing script, retaining each guide's content,
section order, hero, TOC, metadata, schemas and historical closing composition.

| Guide | Existing family | Decision |
| --- | --- | --- |
| 08 Aristotle | Extended guide with footer | Restore shared navigation script |
| 09 Weber | Extended guide with footer | Restore shared navigation script |
| 10 Freud | Extended guide with footer | Restore shared navigation script |
| 11 Gramsci | Extended guide with footer | Restore shared navigation script |
| 12 Hobbes | Extended guide with footer | Restore shared navigation script |
| 13 Averroes | Extended guide with footer | Restore shared navigation script |
| 14 Simmel | Extended guide with footer | Restore shared navigation script |
| 15 Smith | Guide with in-body closing navigation, no footer | Restore script; allow historical footer omission |
| 16 Cicero | Guide with in-body closing navigation, no footer | Restore script; allow historical footer omission |
| 17 Tocqueville | Guide with in-body closing navigation, no footer | Restore script; allow historical footer omission |
| 18 Condorcet | Guide with in-body closing navigation, no footer | Restore script; allow historical footer omission |
| 19 Polybius | Guide with in-body closing navigation, no footer | Restore script; allow historical footer omission |
| 20 Mosca | Guide with in-body closing navigation, no footer | Restore script; allow historical footer omission |
| 21 Pareto | Guide with in-body closing navigation, no footer | Restore script; allow historical footer omission |
| 22 Manzoni | Guide with in-body closing navigation, no footer | Restore script; allow historical footer omission |
| 23 Collodi | Guide with in-body closing navigation, no footer | Restore script; allow historical footer omission |
| 24 Pasolini | Guide with in-body closing navigation, no footer | Restore script; allow historical footer omission |

All 17 retain their historical editorial structure; all 17 receive the same
functional patch. Ten footer omissions remain admitted exceptions, not an open
request to rebuild these guides. Their primary navigation and in-body links to
the hub and published guides preserve discovery. All have Article,
BreadcrumbList and FAQPage data, a cover and a working TOC.

The existing exact-match allowlist remains in use: unexpected omissions and
stale exceptions fail `python3 tools/check-public-site.py`. New pages receive no
exception implicitly. A missing script is no longer admitted on any guide.
Do not copy historical exceptions into the new-guide template.
