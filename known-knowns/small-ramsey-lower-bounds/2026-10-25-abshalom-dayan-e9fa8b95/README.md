# A 3-colouring of K_153 proving R(3,4,7) >= 154 (small-ramsey-lower-bounds, partial win p1)

## What
The circulant 3-colouring of K_153 in object/R_3_4_7.txt (sha256 e9fa8b95...6a40) has no colour-1 K3, no colour-2 K4 and no colour-3 K7, which I verified exhaustively by 3 independent methods, so R(3,4,7) >= 154, which is strictly above the R(3,4,7) >= 152 in DS1 revision #18 (April 24, 2026) Table XIb and above every bound for that cell in arXiv papers whose metadata (searched 2026-10-25) mentions Ramsey and that were submitted since April 2026.

Path note: the panel files and how-we-built-it/PREREG.md refer to the run's folders. There, claim/ is this package's folder, claim/object/ is object/, CLAIM.md is README.md, table_record.md is the-record-we-beat/README.md, verify_circ.py is verify-it-yourself/verify_circ.py, RUN/checker/mcheck.py is how-we-built-it/code/mcheck.py, and repo/bank/targets.json is bank/targets.json in this repository. Work files and folders named there (work/; panel/.work/; RUN/checker/checker_tests.out; runs/2026-10-25-1101/attempts/evaluator-first/, the run's own checker in weekend run 7) are not shipped. Weekend runs 4, 5 and 7 and "the scout" are steps of the same weekend runs; the panel ran on the full run folder, and everything needed to check the claim is in this package.

Corrections to the panel text:
- panel/gate.md says claim/ was fixed at 09:47Z; REPRODUCE ran earlier, 09:29:17Z to 09:30:28Z. The gate's diff -r (work/ excluded) found claim/ unchanged since the REPRODUCE copy.

## Check it yourself
```sh
sh verify-it-yourself/run_checks.sh
```
Expected last three lines: `proves R(3,4,7) >= 154`, `PASS`, `PASS`. Python 3 standard library only; under a second on a laptop.

## Compared to
| source | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| DS1, Radziszowski, Small Ramsey Numbers (revision of April 24, 2026), Table XIb | R(3,4,7) | 152 (reference ExT) | https://www.combinatorics.org/ojs/index.php/eljc/article/download/DS1/pdf | 2026-10-25T06:19:34Z, 07:44:20Z and 11:04:12Z |

154 > 152. Fetch records, hashes and the extracted table are in the-record-we-beat/; the panel's own searches for anything newer are in panel/novelty.md and panel/criterion.md.

## Not claimed
- Only a lower bound: nothing about upper bounds or the exact value of R(3,4,7).
- One cell only. Other cells built in the same runs are separate claims with their own panels.
- Not a new method: the construction is the splitting method of Exoo and Tatarevic applied to a published two-colour circulant (see Credits).
- "Nothing at 154 or above was published" rests on the searches listed in panel/novelty.md and panel/criterion.md (DS1, arXiv, the authors' repositories, this repository).
- Exoo's construction folder http://cs.indstate.edu/ge/RAMSEY/ExTa/ returned HTTP 403 to the run and was not retried, so it was not read. The arXiv searches covered metadata only; a paper that gives this cell only in its full text would not have been found.

## Credits
- Geoffrey Exoo and Milos Tatarevic, "New Lower Bounds for 28 Classical Ramsey Numbers", Electron. J. Combin. 22(3) (2015) #P3.11, https://www.combinatorics.org/ojs/index.php/eljc/article/view/v22i3p11 , arXiv:1504.02403 (https://arxiv.org/abs/1504.02403): the splitting method used here (split one colour graph of a two-colour colouring into two colour graphs with smaller forbidden cliques) and the current DS1 entry R(3,4,7) >= 152.
- Eugene Kuznetsov, "Computational lower limits on small Ramsey numbers", arXiv:1505.07186v5 (2016), https://arxiv.org/abs/1505.07186v5 , Table 2: the (7,7) circulant on Z_153 whose two colour classes this object starts from.
- Stanislaw Radziszowski, "Small Ramsey Numbers", Electron. J. Combin. Dynamic Survey DS1 (revision of April 24, 2026), https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS1 : the table compared against.
- PySAT (python-sat 1.9.dev17), https://github.com/pysathq/pysat , with Armin Biere's CaDiCaL solver, https://github.com/arminbiere/cadical : the SAT solving that built the object and the run's second checker.
- Found and packaged by Abshalom Dayan with the V3R1T4S kit (https://github.com/elder-plinius/V3R1T4S).
