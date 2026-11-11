# Every tree on at most 25 vertices is super edge-magic

Target: `super-edge-magic-trees-beyond-17`, success criterion (a) in full. Supersedes the partial-win packages of pull
requests #917 (closed; at most 20 vertices) and #945 (at most 22): the same certificate files for 18 to 22, plus 23,
24 and 25. Credit: GitHub [thefullnacho](https://github.com/thefullnacho).

## What

For every n from 18 to 25, the hash-verified certificate file in claim/object gives exactly A000055(n) pairwise non-isomorphic trees on n vertices (hence every unlabeled tree of that order), each with a bijection onto {1..n} whose n-1 edge sums are consecutive integers (a super edge-magic labeling), as confirmed by an exact canonical-key count, by leaf-extension regeneration from order n-1, and by the claim's own regenerating checker for n up to 24; combined with the Lee and Shan verification up to 17 cited in DS6 (29th ed., Nov 6, 2026), every tree on at most 25 vertices is super edge-magic, meeting criterion (a) in full.

## Check it yourself

From this folder, with the eight certificate files in `certificates/` (or let the script fetch them; names, sizes,
hashes and URLs in `object/CERTIFICATES.md`):

    sh verify-it-yourself/run_checks.sh

Expected last line: `PASS`. Needs python3 (standard library), xz and curl. The full run downloads about 4.9 GB and takes
about 3 hours on one core, with a peak of about 12 GB of memory at n = 25; `ORDERS="18 19 20 21 22"` checks a subset
in minutes on a laptop. Two checkers with different code and different methods read every line of every order: one
regenerates every tree by the Wright-Richmond-Odlyzko-McKay algorithm and matches each one to exactly one certificate
line; the other counts distinct AHU canonical codes against A000055.

## Compared to

| table | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| J. A. Gallian, A Dynamic Survey of Graph Labeling, Electron. J. Combin. DS6, 29th ed. (Nov 6, 2026), Section 5.2, p. 174 | all trees on at most n vertices are super edge-magic (computer verification) | 17 (S. M. Lee and Q. X. Shan, 2002) | https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS6 | 2026-11-10T17:24:20Z |

This package: 25. Pending in this repo: 22 (pull request #945, same contributor). Snapshot in `the-record-we-beat/RECORD.md`.

## Not claimed

- Nothing about 26 or more vertices, and no proof of the Enomoto-Llado-Nakamigawa-Ringel conjecture.
- Orders up to 17 are not re-certified here; they rest on Lee and Shan's 2002 verification (a conference talk) as
  cited in DS6.
- No tree was found that is not super edge-magic. Trees the time-capped search left over (301, 1,012 and 23,458 at
  n = 23, 24, 25) were all labelled by a longer search; they are listed in `how-we-built-it/leftovers/` as data, since
  they are the trees this search found hardest. None is a caterpillar; most are lobsters.
- The search enumerated trees with nauty gentreeg (networkx for 18 to 20); neither checker uses either.
  `indep_check.py` was written on the contributor's side (independent code, not independent authorship); the panel's
  REPRODUCE and CRITERION skeptics each wrote their own checker (`panel/`).

## Credits

- Y. Enomoto, A. S. Llado, T. Nakamigawa and G. Ringel, Super edge-magic graphs, SUT J. Math. 34 (1998): the
  conjecture and the caterpillar construction. https://doi.org/10.55937/sut/991985322
- S. M. Lee and Q. X. Shan, All trees with at most 17 vertices are super edge-magic, 16th MCCCC Conference,
  Carbondale, Southern Illinois University, Nov. 2002: the record extended here.
- R. M. Figueroa-Centeno, R. Ichishima and F. A. Muntaner-Batle: the consecutive-edge-sum characterisation.
- Y. Fukuchi and A. Oshima: trees with diameter at least n-5 are super edge-magic.
- J. A. Gallian, A Dynamic Survey of Graph Labeling (DS6): https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS6
- R. A. Wright, B. Richmond, A. Odlyzko and B. D. McKay, Constant time generation of free trees, SIAM J. Comput. 15
  (1986): the regeneration in `indep_check.py`.
- B. D. McKay and A. Piperno, nauty 2.8.9 (gentreeg), used by the search: https://pallini.di.uniroma1.it
- OEIS A000055, number of trees with n unlabeled nodes: https://oeis.org/A000055
- V3R1T4S kit and bank entry: https://github.com/elder-plinius/V3R1T4S
