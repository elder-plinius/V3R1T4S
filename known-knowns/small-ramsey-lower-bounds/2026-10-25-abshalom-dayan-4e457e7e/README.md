# A 3-colouring of K_271 proving R(3,3,15) >= 272 (small-ramsey-lower-bounds, partial win p1)

## What
The 3-colouring of K_271 in object/R_3_3_15.txt has no colour-1 triangle, no colour-2 triangle and no colour-3 K_15 (checked exhaustively), so R(3,3,15) >= 272, which exceeds the R(3,3,15) >= 269 of DS1 (revision of April 24, 2026, Table XIb) and every bound I found in newer arXiv papers or implied by DS1's Section 6.2 constructions; it is a corollary of the same object's 266-vertex R(3,3,14) colouring via the folklore colour-3 join.

Path note: the panel files and how-we-built-it/PREREG.md refer to the run's folders. There, claim/ is this package's folder, CLAIM.md is README.md, table_record.md is the-record-we-beat/README.md, verify_join.py is verify-it-yourself/verify_join.py, RUN/checker/mcheck.py is how-we-built-it/code/mcheck.py, and repo/bank/targets.json is bank/targets.json in this repository. Work files and folders named there (literature_record.md, the author's search record; work/; panel/.work/; RUN/checker/checker_tests.out; runs/2026-10-25-1101/attempts/evaluator-first/, the run's own checker in weekend run 7; the run's REPORT.md) are not shipped. Weekend runs 5 and 7 and "the scout" are steps of the same weekend runs; the panel ran on the full run folder, and everything needed to check the claim is in this package.

Corrections to the panel text:
- panel/novelty.md gives 261 for the DS1 6.2.g bound 4R(3,14) - 3 (the value in DS1's text, from R(3,14) >= 66); with DS1's current R(3,14) >= 67 it is 265, as panel/gate.md says. Both are below 272.

## Check it yourself
```sh
sh verify-it-yourself/run_checks.sh
```
Expected last three lines: `proves R(3,3,15) >= 272`, `PASS`, `PASS`. Python 3 standard library only; about 5 seconds on a laptop.

## Compared to
| source | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| DS1, Radziszowski, Small Ramsey Numbers (revision of April 24, 2026), Table XIb | R(3,3,15) | 269 (reference ExT) | https://www.combinatorics.org/ojs/index.php/eljc/article/download/DS1/pdf | 2026-10-25T06:19:34Z, 07:44:20Z and 11:04:12Z |

272 > 269. Fetch records, hashes and the extracted table are in the-record-we-beat/; the panel's own searches for anything newer are in panel/novelty.md and panel/criterion.md.

## Not claimed
- Only a lower bound: nothing about upper bounds or the exact value of R(3,3,15).
- One cell only. Other cells built in the same runs are separate claims with their own panels.
- Not a new method: the construction is the folklore colour-3 join of the R(3,3,14) >= 267 colouring of the same weekend (a separate claim, known-knowns/small-ramsey-lower-bounds/2026-10-25-abshalom-dayan-d46e9b16; itself the splitting method of Exoo and Tatarevic applied to a published circulant) with a 5-vertex block (see Credits). With DS1's own R(3,3,14) value the join gives only 247, and no DS1 general construction reaches 272 (the highest is 4R(3,14) - 3 = 265). It is a claim of its own only because DS1 lists R(3,3,15) as a separate cell and partial win p1 is per cell.
- "Nothing at 272 or above was published" rests on the searches listed in panel/novelty.md and panel/criterion.md (DS1, arXiv, the authors' repositories, this repository).
- Exoo's construction folder http://cs.indstate.edu/ge/RAMSEY/ExTa/ was not read (HTTP 403 to an earlier fetch in the same weekend runs; not retried).

## Credits
- Geoffrey Exoo and Milos Tatarevic, "New Lower Bounds for 28 Classical Ramsey Numbers", Electron. J. Combin. 22(3) (2015) #P3.11, https://www.combinatorics.org/ojs/index.php/eljc/article/view/v22i3p11 , arXiv:1504.02403 (https://arxiv.org/abs/1504.02403): the splitting method behind the R(3,3,14) colouring used for vertices 0..265, and the current DS1 entry R(3,3,15) >= 269.
- Eugene Kuznetsov, "Computational lower limits on small Ramsey numbers", arXiv:1505.07186v5 (2016), https://arxiv.org/abs/1505.07186v5 , Table 2: the (5,14) circulant on Z_266 whose two colour classes the R(3,3,14) colouring starts from.
- Stanislaw Radziszowski, "Small Ramsey Numbers", Electron. J. Combin. Dynamic Survey DS1 (revision of April 24, 2026), https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS1 : the table compared against, and section 6.2's general constructions.
- PySAT (python-sat 1.9.dev17), https://github.com/pysathq/pysat , with Armin Biere's CaDiCaL solver, https://github.com/arminbiere/cadical : the SAT searches in the run's checkers (how-we-built-it/code/) and the panel's checks.
- The colour-3 join with a block is a folklore construction for multicolour Ramsey lower bounds; it is not the author's.
- Found and packaged by Abshalom Dayan with the V3R1T4S kit (https://github.com/elder-plinius/V3R1T4S).
