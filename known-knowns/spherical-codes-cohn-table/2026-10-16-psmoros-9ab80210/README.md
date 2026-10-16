# spherical-codes-cohn-table: a 526-point code in R^6 below the table's (6,526) cosine

## What

The 526 vectors in R^6 of object/d6_N526.txt (sha256 9ab8021055cf16bc37eafb5ff62c65ce9a9660c1c907fca8e202f9def2d5b83a, 26 significant digits per coordinate) have, after normalisation in mpmath at 50 digits over all 138,075 pairs, maximum inner product c* = 0.78643061854457972538529914, which is 2.0578e-4 below the cosine 0.786636400242 of the unstarred, unlabelled (6,526) row of spherical-codes.org /plain and HTML index as fetched 2026-10-16T03:59Z, and arXiv metadata searches at 2026-10-16T04:10Z found no (6,526) result newer than the row's own source arXiv:2610.19988.

## Check it yourself

From this folder, with only Python 3 (standard library):

    sh verify-it-yourself/run_checks.sh

Expected last line: `PASS` (about 3 seconds on a laptop; it checks every one of the 138,075 pairs in exact decimal
arithmetic at 70 digits, and the object's sha256). Real output: verify-it-yourself/RECEIPTS.md.

## Compared to

| table | cell | listed cosine | ours | gain | URL | fetched (UTC) |
|---|---|---|---|---|---|---|
| Henry Cohn, Table of spherical codes | (d, N) = (6, 526), no star, no "needs more optimization", held by Vahteristo (arXiv:2610.19988) | 0.786636400242 | 0.786430618544579725385299 | 2.0578e-4 | https://spherical-codes.org/plain | 2026-10-16T05:12:04Z |

Also below every other public value the panel found for (6,526): Vahteristo's Zenodo archive
(10.5281/zenodo.23270586: combined 0.7866364002418642, per-instance 0.7866409885238883, global 0.7880757234615681)
and the earlier table value 0.788513093183 (A. Jay et al., 2026-09-23). Smaller is better: the table lists the cosine
of the minimal angle. Minimal angle of this code: 38.14681274152183 degrees.

## Not claimed

- Only the row (6, 526). The same code with one point deleted also lies below the (6,525) row; that row and the other
  rows this run improved are not part of this package (each would be its own claim and panel).
- No optimality, no exact (algebraic) value, no statement about other dimensions or sizes.
- Nothing was uploaded to spherical-codes.org; the maintainer has not reviewed this code.
- Not covered by the novelty check: the SSRN full text of Jay et al. (host blocked a plain client), arXiv full
  texts (titles and abstracts were searched), and uploads still pending at the table.

## Credits

- Henry Cohn, Table of spherical codes, https://spherical-codes.org/ (data set https://hdl.handle.net/1721.1/153543):
  the table compared against, and the posted (6,527) code ("needs more optimization") that was the starting point.
- Ilmari Vahteristo, "New spherical codes by tuning an annealing solver", arXiv:2610.19988,
  https://arxiv.org/abs/2610.19988; codes on Zenodo https://doi.org/10.5281/zenodo.23270586: the code that holds the
  (6,526) row, and the LogSumExp-annealing idea used in the polish.
- A. Jay, M. Poberznik, M. Brut, A. Hemeryck, L.-H. Hoang, M. Gunde, N. Salles, G. Cruchon and M. Roux,
  "Equidistribution of points on the hypersphere including symmetries" (SSRN 6427919): earlier holders of the row.
- Methods: monotonic basin hopping (R. H. Leary 2000; A. Grosso, M. Locatelli, F. Schoen 2007); the penalty-threshold
  polish follows soft-sphere jamming (Lubachevsky-Stillinger).
- Submission credit: psmoros. Built and reviewed with the V3R1T4S protocol, https://github.com/elder-plinius/V3R1T4S;
  panel: REPRODUCE (fable), NOVELTY and CRITERION (opus) subagents, each seeing only the claim.
