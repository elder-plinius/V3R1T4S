# A 3-colouring of K_182 proving R(3,3,11) >= 183 (small-ramsey-lower-bounds, partial win p1)

## What
The circulant 3-colouring of K_182 in object/R_3_3_11.txt (sha256 622b79c6...1270) has no triangle in colours 1 and 2 and no K_11 in colour 3, verified exhaustively by two independent methods, so R(3,3,11) >= 183, strictly above the bound 174 in DS1 revision #18 (April 24, 2026) Table XIb and above every R(3,3,11) lower bound in the arXiv papers my searches found.

Path note: the panel files and how-we-built-it/PREREG.md refer to the run's folders. There, claim/ is this package's folder, CLAIM.md is README.md, table_record.md is the-record-we-beat/README.md, verify_circ.py is verify-it-yourself/verify_circ.py, check_fast.py, alpha.c and RUN/checker/mcheck.py are in how-we-built-it/code/, and repo/bank/targets.json is bank/targets.json in this repository. Work files and folders named there (literature_record.md, the author's search record; work/; panel/.work/; RUN/checker/checker_tests.out; the run's REPORT.md and its "Needs you" section) are not shipped; everything REPORT.md says about this claim is in panel/gate.md. "Run 4" and "the scout" are earlier steps of the same weekend runs.

## Check it yourself
```sh
sh verify-it-yourself/run_checks.sh
```
Expected last three lines: `proves R(3,3,11) >= 183`, `PASS`, `PASS` (the checker and the script each print PASS). Python 3 standard library only; under a second on a laptop.

## Compared to
| source | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| DS1, Radziszowski, Small Ramsey Numbers (revision of April 24, 2026), Table XIb | R(3,3,11) | 174 (reference ExT) | https://www.combinatorics.org/ojs/index.php/eljc/article/download/DS1/pdf | 2026-10-25T06:19:34Z and 07:44:20Z |

183 > 174. Fetch records, hashes and the extracted table are in the-record-we-beat/; the panel's own searches for anything newer are in panel/novelty.md and panel/criterion.md.

## Not claimed
- Only a lower bound: nothing about upper bounds or the exact value of R(3,3,11).
- One cell only. Other cells built in the same runs are separate claims with their own panels.
- Not a new method: the construction is the splitting method of Exoo and Tatarevic applied to a published two-colour circulant (see Credits).
- "Nothing at 183 or above was published" rests on the searches listed in panel/novelty.md and panel/criterion.md (DS1, arXiv, the authors' repositories, this repository).
- Exoo's construction folder http://cs.indstate.edu/ge/RAMSEY/ExTa/ returned HTTP 403 to the run and was not retried, so it was not read.

## Credits
- Geoffrey Exoo and Milos Tatarevic, "New Lower Bounds for 28 Classical Ramsey Numbers", Electron. J. Combin. 22(3) (2015) #P3.11, https://www.combinatorics.org/ojs/index.php/eljc/article/view/v22i3p11 (arXiv:1504.02403,
  https://arxiv.org/abs/1504.02403): the splitting method used here (split one colour graph of a two-colour colouring into two colour graphs with smaller forbidden cliques) and the current DS1 entry R(3,3,11) >= 174.
- Eugene Kuznetsov, "Computational lower limits on small Ramsey numbers", arXiv:1505.07186v5 (2016), https://arxiv.org/abs/1505.07186, Table 2: the (5,11) circulant on Z_182 whose two colour classes this object starts from.
- Stanislaw Radziszowski, "Small Ramsey Numbers", Electron. J. Combin. Dynamic Survey DS1 (revision of April 24, 2026), https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS1: the table compared against.
- Found and packaged by Abshalom Dayan with the V3R1T4S kit (https://github.com/elder-plinius/V3R1T4S).
