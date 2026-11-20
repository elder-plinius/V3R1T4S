# Path map for frozen PREREG.v2.md

how-we-built-it/PREREG.v2.md is frozen and is not edited by this note. It cites the run's internal paths (attempts/..., far-import/code/..., null-and-leak-auditor/code/..., claim/), not paths relative to this package.

Each cited path is mapped below. Where the cited file can be identified in this package, sha256sum of that package file was compared with the sha256 written in PREREG.v2.md. A full-digest match is written identical (sha256 plus the first 12 hex digits). A cited file absent from this package is marked not included in this package. No file outside this package was hashed.

| cited path | package-relative path | comparison |
|---|---|---|
| king_bounds.py | not included in this package | not included in this package |
| far-import/code/simplex20.py | not included in this package | not included in this package |
| far-import/code/gf4slice.py | how-we-built-it/gf4slice.py | identical (sha256 d37c340ed102) |
| PREREG.md | how-we-built-it/PREREG.md | present in this package; PREREG.v2.md cites the name and writes no sha256, so it is not marked identical or differs. sha256sum 0c7a1a55d014385c50091aa9ca2ec811a09244b5f4ecabec9fb58722718825f3 |
| null-and-leak-auditor/code/nullgreedy.c | how-we-built-it/nullgreedy.c | identical (sha256 18f054099837). The controls line cites the prefix sha256 18f05409, which matches the start of this digest |
| gf4slice.py | how-we-built-it/gf4slice.py | identical (sha256 d37c340ed102) |
| gcmc (prose: gcmc warm start) | how-we-built-it/gcmc.c | same package file as attempts/evaluator-first/code/gcmc.c; identical (sha256 7d0e5e2415c1) |
| claim/ | not included in this package | not included in this package |
| attempts/table-auditor/code/king_bounds.py | not included in this package | not included in this package |
| attempts/far-import/code/mseq.py | not included in this package | not included in this package |
| attempts/far-import/code/simplex20.py | not included in this package | not included in this package |
| attempts/far-import/code/gf4slice.py | how-we-built-it/gf4slice.py | identical (sha256 d37c340ed102) |
| attempts/evaluator-first/code/gcmc.c | how-we-built-it/gcmc.c | identical (sha256 7d0e5e2415c1) |
| attempts/null-and-leak-auditor/code/nullgreedy.c | how-we-built-it/nullgreedy.c | identical (sha256 18f054099837) |
