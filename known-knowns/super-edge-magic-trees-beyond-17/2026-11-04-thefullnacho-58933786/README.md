# Every tree on at most 22 vertices is super edge-magic

**Status: CONFIRMED_PARTIAL.** Confirmed by a fresh-context three-skeptic panel (REPRODUCE, NOVELTY, CRITERION)
and the honesty gate; see panel/gate.md.

Target: `super-edge-magic-trees-beyond-17`, partial win p2. Extends the p1 package of pull request #917 (at most 20
vertices). Credit: GitHub [thefullnacho](https://github.com/thefullnacho).

## What

For every n in 18..22, the files object/cert_n18.txt .. object/cert_n22.txt.xz (one per order, cert_nN for order N) list exactly A000055(n) pairwise non-isomorphic trees on n vertices (hence every unlabeled tree on n vertices), each with a bijection onto {1..n} whose n-1 edge sums are consecutive integers, so every tree on 18 to 22 vertices is super edge-magic, and together with Lee and Shan's cited verification up to 17 vertices every tree on at most 22 vertices is super edge-magic (partial win p2).

## Check it yourself

From this folder, with the five certificate files in `certificates/` (or let the script fetch them; names, hashes
and URLs in `object/CERTIFICATES.md`):

    sh verify-it-yourself/run_checks.sh

Expected last line: `PASS`. Needs python3 (standard library), xz and curl. About 7 minutes on two cores, under 1 GB
per process. Two checkers with different code and different methods each read every line of every order: one
regenerates all trees by the Wright-Richmond-Odlyzko-McKay algorithm and matches them one-to-one by canonical form,
the other counts distinct AHU canonical codes against A000055.

## Compared to

| table | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| J. A. Gallian, A Dynamic Survey of Graph Labeling, Electron. J. Combin. DS6, 28th ed. (Oct 30, 2025), Section 5.2, p. 168 | all trees on at most n vertices are super edge-magic (computer verification) | 17 (S. M. Lee and Q. X. Shan, 2002) | https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS6 | 2026-11-04T03:00:01Z |

This package: 22. Pending in this repo: 20 (pull request #917, same contributor). Snapshot in `the-record-we-beat/RECORD.md`.

## Not claimed

- Nothing about 23 or more vertices, and no proof of the Enomoto-Llado-Nakamigawa-Ringel conjecture.
- Orders up to 17 are not re-certified here; they rest on Lee and Shan's 2002 verification (a conference talk) as
  cited in DS6.
- No tree was found that is not super edge-magic.
- The search enumerated trees with nauty gentreeg; neither checker uses gentreeg. `indep_check.py` was written on
  the contributor's side (independent code, not independent authorship); the panel's REPRODUCE and CRITERION
  skeptics each wrote their own checker and reached the same counts (`panel/`).
- The search for a higher published bound covered DS6 and the sources listed in `panel/novelty.md`; it is not
  exhaustive.

## Credits

- Y. Enomoto, A. S. Llado, T. Nakamigawa and G. Ringel, Super edge-magic graphs, SUT J. Math. 34 (1998): the
  conjecture and the caterpillar construction. https://doi.org/10.55937/sut/991985322
- S. M. Lee and Q. X. Shan, All trees with at most 17 vertices are super edge-magic, 16th MCCCC Conference,
  Carbondale, Southern Illinois University, Nov. 2002: the record extended here.
- R. M. Figueroa-Centeno, R. Ichishima and F. A. Muntaner-Batle: the consecutive-edge-sum characterisation.
- J. A. Gallian, A Dynamic Survey of Graph Labeling (DS6): https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS6
- R. A. Wright, B. Richmond, A. Odlyzko and B. D. McKay, Constant time generation of free trees, SIAM J. Comput. 15
  (1986): the regeneration in `indep_check.py`.
- B. D. McKay and A. Piperno, nauty 2.8.9 (gentreeg), used by the search: https://pallini.di.uniroma1.it
- OEIS A000055, number of trees with n unlabeled nodes: https://oeis.org/A000055
- V3R1T4S kit and bank entry: https://github.com/elder-plinius/V3R1T4S
