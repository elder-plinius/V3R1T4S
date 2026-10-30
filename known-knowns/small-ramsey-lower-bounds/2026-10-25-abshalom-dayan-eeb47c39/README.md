# A 3-colouring of K_202 proving R(3,3,12) >= 203 (small-ramsey-lower-bounds, partial win p1)

## What
The circulant 3-colouring of K_202 in object/R_3_3_12.txt has no monochromatic K_3 in colours 1 and 2 and no K_12 in colour 3 (checked by all-triples brute force, a CaDiCaL UNSAT proof and the author's exhaustive B&B), so R(3,3,12) >= 203, strictly above DS1 (April 24, 2026) Table XIb's 194 and above every bound for this cell I found in arXiv papers newer than that revision.

Path note: the panel files and how-we-built-it/PREREG.md refer to the run's folders. There, claim/ is this package's folder, CLAIM.md is README.md, table_record.md is the-record-we-beat/README.md, verify_circ.py is verify-it-yourself/verify_circ.py, RUN/checker/mcheck.py is how-we-built-it/code/mcheck.py, and repo/bank/targets.json is bank/targets.json in this repository. Work files and folders named there (literature_record.md, the author's search record; work/; panel/.work/; RUN/checker/checker_tests.out; the run's REPORT.md and its "Needs you" section) are not shipped; everything REPORT.md says about this claim is in panel/gate.md. "Run 4" and "the scout" are earlier steps of the same weekend runs.

Corrections to the panel text:
- The What sentence (from panel/gate.md) says "a CaDiCaL UNSAT proof"; in fact CaDiCaL, called through pysat, returned UNSAT, and no DRAT/LRAT proof certificate was produced or checked. The brute force over all triples and the exhaustive branch and bound establish the claim without it.

## Check it yourself
```sh
sh verify-it-yourself/run_checks.sh
```
Expected last three lines: `proves R(3,3,12) >= 203`, `PASS`, `PASS` (the checker and the script each print PASS). Python 3 standard library only; under a second on a laptop.

## Compared to
| source | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| DS1, Radziszowski, Small Ramsey Numbers (revision of April 24, 2026), Table XIb | R(3,3,12) | 194 (reference ExT) | https://www.combinatorics.org/ojs/index.php/eljc/article/download/DS1/pdf | 2026-10-25T06:19:34Z and 07:44:20Z |

203 > 194. Fetch records, hashes and the extracted table are in the-record-we-beat/; the panel's own searches for anything newer are in panel/novelty.md and panel/criterion.md.

## Not claimed
- Only a lower bound: nothing about upper bounds or the exact value of R(3,3,12).
- One cell only. Other cells built in the same runs are separate claims with their own panels.
- Not a new method: the construction is the splitting method of Exoo and Tatarevic applied to a published two-colour circulant (see Credits).
- "Nothing at 203 or above was published" rests on the searches listed in panel/novelty.md and panel/criterion.md (DS1, arXiv, the authors' repositories, this repository).
- Exoo's construction folder http://cs.indstate.edu/ge/RAMSEY/ExTa/ returned HTTP 403 to the run and was not retried, so it was not read.

## Credits
- Geoffrey Exoo and Milos Tatarevic, "New Lower Bounds for 28 Classical Ramsey Numbers", Electron. J. Combin. 22(3) (2015) #P3.11, https://www.combinatorics.org/ojs/index.php/eljc/article/view/v22i3p11 (arXiv:1504.02403,
  https://arxiv.org/abs/1504.02403): the splitting method used here (split one colour graph of a two-colour colouring into two colour graphs with smaller forbidden cliques) and the current DS1 entry R(3,3,12) >= 194.
- Eugene Kuznetsov, "Computational lower limits on small Ramsey numbers", arXiv:1505.07186v5 (2016), https://arxiv.org/abs/1505.07186, Table 2: the (5,12) circulant on Z_202 whose two colour classes this object starts from.
- Stanislaw Radziszowski, "Small Ramsey Numbers", Electron. J. Combin. Dynamic Survey DS1 (revision of April 24, 2026), https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS1: the table compared against.
- Found and packaged by Abshalom Dayan with the V3R1T4S kit (https://github.com/elder-plinius/V3R1T4S).
