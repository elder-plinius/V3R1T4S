# Spherical code: one improved row of Cohn's table, d=29, N=60

## What

For the single row (d=29, N=60) the saved object has maximum normalised inner product 0.032282689322, which is lower than the saved live /plain cosine 0.032282791684 by 1.02362e-7, at least 1e-10, on an index row with no ast mark and no 'needs more optimization' text and outside the kissing-number range, as fetched 2026-10-18T17:39Z.

## Check it yourself

From this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Requirements**: `python3` 3.8 or later, standard library only (the panel's own checks used mpmath at 50 digits and agree).
- **Rough laptop time**: under ten seconds.
- **Expected last line**: `ALL CHECKS PASS`

## Compared to

| Source | Cell | Value | URL | UTC fetch time |
|---|---|---|---|---|
| Henry Cohn, spherical-codes.org `/plain` | d=29, N=60 | 0.032282791684 (row credited to Ilmari Vahteristo (arXiv:2610.19988)) | https://spherical-codes.org/plain | 2026-10-18T17:50:10Z |
| Henry Cohn, spherical-codes.org HTML index | d=29, N=60 | same cosine; no proven-optimal mark; no "needs more optimization" text | https://spherical-codes.org/ | 2026-10-18T17:50:11Z |
| Posted coordinate file | d=29, N=60 | its recomputed cosine matches `/plain` to 12 decimals | https://spherical-codes.org/data/29/60 | 2026-10-18T17:51:07Z to 17:51:10Z |
| V3R1T4S `TROPHY_CASE.md` | spherical codes | no entry mentions spherical codes | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | 2026-10-18T17:50:14Z |
| V3R1T4S pull requests (pages 1 to 5) | this row | no open or merged pull request names this row | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=all&per_page=100 | 2026-10-18T17:50:14Z to 17:50:22Z |
| Vahteristo, arXiv:2610.19988 | this row | no value for this row in the abstract; the live row already postdates the paper | https://export.arxiv.org/api/query?id_list=2610.19988 | 2026-10-18T17:50:28Z to 17:50:31Z |

The panel's novelty skeptic fetched each source independently (report: `panel/novelty.md`). Snapshot metadata, HTTP status and page sha256: `the-record-we-beat/README.md`. Our values (maximum normalised inner product, 20 digits): (29,60) 0.032282689322403249986.

## Not claimed

- One row only: (d=29, N=60). Nothing is claimed for neighbouring N or dimensions, and no claim of optimality or of a best possible value.
- The comparison is with the table's 12-decimal cosine on `/plain` as fetched at the times above, and with the posted code. The table is maintained and may move.
- The panel did not fetch the Zenodo data set behind arXiv:2610.19988 (https://doi.org/10.5281/zenodo.23270586); an unposted better code could exist there. The live row postdates that paper.
- The row is outside the kissing-number range, so it does not belong to the kissing-number target.
- Nothing was uploaded to the table (its /upload-code route); that needs the contributor's explicit permission and is a separate step.
- Not peer reviewed. It was checked by a three-skeptic panel (`panel/`) and by the standalone checker shipped here.

## Filing history

New filing. No earlier pull request carries this object. The contributor's earlier closed filings on this target (V3R1T4S pull requests 70 to 77) are different rows.

## Credits

- **Henry Cohn**, *Table of spherical codes* (https://spherical-codes.org/): the table, its /plain file and the posted coordinate files this claim is compared against.
- **Ilmari Vahteristo**: the live row for d=29, N=60 is credited to them, and our object improves on that posted code.
- **Ilmari Vahteristo**, *New spherical codes by tuning an annealing solver*, arXiv:2610.19988 (https://arxiv.org/abs/2610.19988; code https://github.com/ilmari99/Spherical-code-solver): the live table cites it for many rows; it is the closest published work.
- **mpmath** (https://mpmath.org/) and **NumPy** (https://numpy.org/): used by the panel's independent checks; the shipped checker needs only the Python standard library.
- Search tool: the solver `sc_opt.c` in `how-we-built-it/` was written by the contributor's AI search agent (Gemini, "Argon") for the contributor `calgulbenkian`; it is a Riemannian L-BFGS with a log-sum-exp objective and basin hopping, a standard technique with no third-party code in it.
- Contributor credit: `calgulbenkian`.
