# Every tree on at most 20 vertices is super edge-magic

**Status: CONFIRMED_PARTIAL.** Confirmed by a fresh-context three-skeptic panel (REPRODUCE, NOVELTY, CRITERION)
and the honesty gate; see panel/gate.md.

Target: `super-edge-magic-trees-beyond-17`, partial win p1. Credit: GitHub [thefullnacho](https://github.com/thefullnacho).

## What

The files cert_n18.txt, cert_n19.txt and cert_n20.txt (sha256 in object/certificates.sha256; archive sha256 390d1698ff6e9563ed2e41a645cff865a05ab6b5427ece910e5bdda6ed82cc8b, DOI 10.5281/zenodo.23918679) give, for every one of the 123867, 317955 and 823065 unlabeled trees on 18, 19 and 20 vertices (A000055(n), matched one-to-one by canonical form against an independent regeneration and against nauty gentreeg), a bijection to {1..n} whose n-1 edge sums are consecutive integers, so, with Lee and Shan's verification for at most 17 vertices as cited in DS6 (28th ed., Section 5.2), this is a certificate (as in (a)) that every tree on at most 20 vertices is super edge-magic (partial win p1).

## Check it yourself

From this folder, after putting the three certificate files in `certificates/` (download and unpack the archive
named in `object/CERTIFICATES.md`, published on Zenodo as DOI 10.5281/zenodo.23918679
<https://zenodo.org/records/23918679>; or let the script fetch it itself):

    sh verify-it-yourself/run_checks.sh

Expected last line: `PASS`. Needs only python3 (standard library). About 5 minutes on one core (282 s measured), most of it
regenerating every tree on up to 20 vertices; peak memory about 0.7 GB (663 MB measured). The archive is 29618152 bytes
(sha256 390d1698ff6e9563ed2e41a645cff865a05ab6b5427ece910e5bdda6ed82cc8b) and unpacks to about 192 MB of text.

## Compared to

| table | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| J. A. Gallian, A Dynamic Survey of Graph Labeling, Electron. J. Combin. DS6, 28th ed. (Oct 30, 2025), Section 5.2, p. 168 | all trees on at most n vertices are super edge-magic (computer verification) | 17 (S. M. Lee and Q. X. Shan, 2002) | https://www.combinatorics.org/ojs/index.php/eljc/article/download/DS6/pdf/ | 2026-11-03T12:27:24Z |

This package: 20. Snapshot with headers and sha256 in `the-record-we-beat/RECORD.md`.

## Not claimed

- Nothing about 21 or more vertices, and no proof of the Enomoto-Llado-Nakamigawa-Ringel conjecture.
- Orders up to 17 are not re-certified here; they rest on Lee and Shan's verification as cited in DS6.
- No tree was found that is not super edge-magic.
- The tree list was produced with networkx, not nauty gentreeg; the package checkers establish coverage by an
  independent regeneration and by distinct canonical forms equal in number to A000055(n). An optional cross-check
  against real gentreeg output is in `panel/criterion-work/` (see RUN_IT_YOURSELF.md, step 4).

## Credits

- Y. Enomoto, A. S. Llado, T. Nakamigawa and G. Ringel, Super edge-magic graphs, SUT J. Math. 34 (1998): the
  conjecture and the caterpillar construction used for the last three trees. https://doi.org/10.55937/sut/991985322
- S. M. Lee and Q. X. Shan, All trees with at most 17 vertices are super edge-magic, 16th MCCCC Conference,
  Carbondale, Southern Illinois University, Nov. 2002: the record extended here.
- R. M. Figueroa-Centeno, R. Ichishima and F. A. Muntaner-Batle: the consecutive-edge-sum characterisation.
- Y. Fukuchi and A. Oshima: trees with diameter at least n-5 are super edge-magic.
- J. A. Gallian, A Dynamic Survey of Graph Labeling (DS6): https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS6
- OEIS A000055, number of trees with n unlabeled nodes: https://oeis.org/A000055
- networkx (tree enumeration in the search): https://networkx.org
- V3R1T4S kit and bank entry: https://github.com/elder-plinius/V3R1T4S
