# Spherical code: rows of Cohn's table in dimension 7 (24 improved rows labelled "needs more optimization")

## What

In dimension 7, 24 distinct rows (N = 177, 178, 204, 212, 215, 308 to 310, 312 to 318, 322, 323, 325, 362, 364 to 368) that the saved index rows label 'needs more optimization' each have a saved object whose 50-digit maximum normalised inner product is lower than the saved /plain cosine by at least 3.19e-9 (largest 1.377e-4 at N=308), which meets partial win p2 and no wider claim.

The 24 objects are the files under `object/`, one per row, listed with their sha256 in `INDEX.csv` (one row each). The package identifier uses the first 8 hex digits of the sha256 of `INDEX.csv` (f2033d824c6279b1bd4cefe5294d96c80a62ebd9154077a27427be09ad684b79), because the package has 24 objects and no single main file.

## Check it yourself

From this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Requirements**: `python3` 3.8 or later, standard library only (the panel's own checks used mpmath at 50 digits and agree).
- **Rough laptop time**: under thirty seconds.
- **Expected last line**: `ALL CHECKS PASS`

## Compared to

| Source | Cell | Value | URL | UTC fetch time |
|---|---|---|---|---|
| Henry Cohn, spherical-codes.org `/plain` | d=7, the 24 rows | `/plain` cosines (12 decimals): N=177: 0.570051592256; N=178: 0.570228301539; N=204: 0.601295919469; N=212: 0.611962614152; N=215: 0.614265846451; N=308: 0.660836744901; N=309: 0.660912967551; N=310: 0.660953811794; N=312: 0.661595420972; N=313: 0.661974195320; N=314: 0.662290658947; N=315: 0.662675365192; N=316: 0.663332152344; N=317: 0.663597580717; N=318: 0.663816385482; N=322: 0.665029616003; N=323: 0.665046095133; N=325: 0.665504583307; N=362: 0.668965357603; N=364: 0.670170636995; N=365: 0.670487284551; N=366: 0.670943830170; N=367: 0.671529770134; N=368: 0.671589583556 | https://spherical-codes.org/plain | 2026-10-18T17:50:10Z |
| Henry Cohn, spherical-codes.org HTML index | same 24 rows | every row reads "Henry Cohn, 2026, needs more optimization." and has no proven-optimal mark | https://spherical-codes.org/ | 2026-10-18T17:50:11Z |
| V3R1T4S `TROPHY_CASE.md` | spherical codes | no entry mentions spherical codes | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | 2026-10-18T17:50:14Z |
| V3R1T4S pull requests (pages 1 to 5) | dimension 7 | no open or merged pull request names any of these rows | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=all&per_page=100 | 2026-10-18T17:50:14Z to 17:50:22Z |
| Vahteristo, arXiv:2610.19988 | d=7 | none of the 24 rows cites it (a row it improved would); no value for them in the abstract | https://export.arxiv.org/api/query?id_list=2610.19988 | 2026-10-18T17:50:28Z to 17:50:31Z |

The panel's novelty skeptic fetched each source independently (report: `panel/novelty.md`). Snapshot metadata, HTTP status and page sha256: `the-record-we-beat/README.md`. Our values (maximum normalised inner product, 20 digits): (7,177) 0.57005146649038168026, (7,178) 0.57022827037247204148, (7,204) 0.60129577690939465485, (7,212) 0.61195558470432380924, (7,215) 0.61426501492671052856, (7,308) 0.66069903248246405657, (7,309) 0.66086366017695630200, (7,310) 0.66093543926639098299, (7,312) 0.66158195187028534665, (7,313) 0.66194582298233295488, (7,314) 0.66228055884701518731, (7,315) 0.66253967224944071829, (7,316) 0.66332295342813728145, (7,317) 0.66359291769009461765, (7,318) 0.66381384252360427781, (7,322) 0.66502756653880460223, (7,323) 0.66502782069173565965, (7,325) 0.66549951613480608035, (7,362) 0.66896535441309224291, (7,364) 0.67016801924131928539, (7,365) 0.67046703514181086524, (7,366) 0.67092606041178163551, (7,367) 0.67152789617238754178, (7,368) 0.67158806395847414257.

## Not claimed

- **Not a record claim.** All 24 rows are labelled "needs more optimization" by the table itself, meaning the posted codes are known to be unconverged. Improving an unconverged row is the partial win p2 of the target (at least 20 such rows in one dimension), never a claim of a best-known value.
- Only dimension 7 and only these 24 rows (N = 177, 178, 204, 212, 215, 308 to 310, 312 to 318, 322, 323, 325, 362, 364 to 368). Nothing is claimed for other N in dimension 7 or for other dimensions.
- The objects are not proven optimal and are not claimed to be converged; some gains are tiny (the smallest is 3.19e-9 at N = 362).
- The panel did not fetch the Zenodo data set behind arXiv:2610.19988 (https://doi.org/10.5281/zenodo.23270586); an unposted better code could exist there. The table postdates that paper and none of these rows cites it.
- Nothing was uploaded to the table (its /upload-code route); that needs the contributor's explicit permission and is a separate step.
- Not peer reviewed. It was checked by a three-skeptic panel (`panel/`) and by the standalone checker shipped here.

## Filing history

New filing. No earlier pull request carries this object. The contributor's earlier closed filings on this target (V3R1T4S pull requests 70 to 77) are different rows.

## Credits

- **Henry Cohn**, *Table of spherical codes* (https://spherical-codes.org/): the table, its /plain file and the posted coordinate files this claim is compared against.
- **Henry Cohn**: every one of the 24 live rows is credited "Henry Cohn, 2026, needs more optimization."
- **Ilmari Vahteristo**, *New spherical codes by tuning an annealing solver*, arXiv:2610.19988 (https://arxiv.org/abs/2610.19988; code https://github.com/ilmari99/Spherical-code-solver): the live table cites it for many rows; it is the closest published work.
- **mpmath** (https://mpmath.org/) and **NumPy** (https://numpy.org/): used by the panel's independent checks; the shipped checker needs only the Python standard library.
- Search tool: the solver `sc_opt.c` in `how-we-built-it/` was written by the contributor's AI search agent (Gemini, "Argon") for the contributor `calgulbenkian`; it is a Riemannian L-BFGS with a log-sum-exp objective and basin hopping, a standard technique with no third-party code in it.
- Contributor credit: `calgulbenkian`.
