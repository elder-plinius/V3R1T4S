# A 3-colouring of K_182 proving R(3,5,6) >= 183 (small-ramsey-lower-bounds, partial win p1)

## What
The circulant 3-colouring of K_182 in object/R_3_5_6.txt (sha256 436b74cecb10c8263ed5c3413d66993ce1f9d34993718f7b5bb4b31890896826) has, by exhaustive enumeration, no K_3 in colour 1, no K_5 in colour 2 and no K_6 in colour 3, so R(3,5,6) >= 183, which is strictly above the bound 181 in DS1 revision #18 (April 24, 2026) Table XIb and above every R(3,5,6) lower bound in the arXiv titles and abstracts I searched on 2026-10-25 (none of them gives one).

Path note: the panel files and how-we-built-it/PREREG.md refer to the run's folders. There, claim/ is this package's folder, CLAIM.md is README.md, table_record.md is the-record-we-beat/README.md, verify_circ.py is verify-it-yourself/verify_circ.py, RUN/checker/mcheck.py is how-we-built-it/code/mcheck.py, and repo/bank/targets.json is bank/targets.json in this repository. Work files and folders named there (literature_record.md, the author's search record; work/; panel/.work/; RUN/checker/checker_tests.out; runs/2026-10-25-1101/attempts/evaluator-first/, the run's own checker in weekend run 7) are not shipped. Weekend runs 4, 5 and 7 and "the scout" are steps of the same weekend runs; the panel ran on the full run folder, and everything needed to check the claim is in this package.

Corrections to the panel text:
- panel/gate.md, panel/novelty.md and panel/criterion.md give 169 (6.2.g with R(5,5) >= 43) as the best bound from DS1's general constructions; the third form of 6.2.g gives 4R(3,3,5) - 3 = 4*45 - 3 = 177 (see Compared to). 183 is above both.

## Check it yourself
```sh
sh verify-it-yourself/run_checks.sh
```
Expected last three lines: `proves R(3,5,6) >= 183`, `PASS`, `PASS`. Python 3 standard library only; under a second on a laptop.

## Compared to
| source | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| DS1, Radziszowski, Small Ramsey Numbers (revision of April 24, 2026), Table XIb | R(3,5,6) | 181 (reference Ex17) | https://www.combinatorics.org/ojs/index.php/eljc/article/download/DS1/pdf | 2026-10-25T06:19:34Z, 07:44:20Z and 11:04:12Z |

183 > 181. Fetch records, hashes and the extracted table are in the-record-we-beat/; the panel's own searches for anything newer are in panel/novelty.md and panel/criterion.md.

The best bound from DS1's general constructions is lower: the third form of construction 6.2.g gives R(3,5,6) >= 4R(3,3,5) - 3 = 177 (the form DS1 uses for its R(3,5,7) >= 241 entry; Xu, Xie, Exoo and Radziszowski, Electron. J. Combin. 11 (2004) #R35, https://www.combinatorics.org/ojs/index.php/eljc/article/view/v11i1r35).

## Not claimed
- Only a lower bound: nothing about upper bounds or the exact value of R(3,5,6).
- One cell only. Other cells built in the same runs are separate claims with their own panels.
- Not a new method: the construction is the splitting method of Exoo and Tatarevic applied to a published two-colour circulant (see Credits).
- "Nothing at 183 or above was published" rests on the searches listed in panel/novelty.md and panel/criterion.md (DS1, arXiv, the authors' repositories, this repository).
- DS1's 181 is Exoo's personal communication [Ex17], so an unpublished better construction by Exoo cannot be ruled out. His construction folder http://cs.indstate.edu/ge/RAMSEY/ExTa/ returned HTTP 403 to the run and was not retried, so it was not read. The arXiv searches covered titles and abstracts only; a paper that gives this cell only in its full text would not have been found.

## Credits
- Geoffrey Exoo and Milos Tatarevic, "New Lower Bounds for 28 Classical Ramsey Numbers", Electron. J. Combin. 22(3) (2015) #P3.11, https://www.combinatorics.org/ojs/index.php/eljc/article/view/v22i3p11 , arXiv:1504.02403 (https://arxiv.org/abs/1504.02403): the splitting method used here (split one colour graph of a two-colour colouring into two colour graphs with smaller forbidden cliques).
- Eugene Kuznetsov, "Computational lower limits on small Ramsey numbers", arXiv:1505.07186v5 (2016), https://arxiv.org/abs/1505.07186v5 , Table 2: the (6,9) circulant on Z_182 whose two colour classes this object starts from.
- Geoffrey Exoo: the current DS1 entry R(3,5,6) >= 181 (DS1 reference [Ex17]); his Ramsey pages: http://cs.indstate.edu/ge/RAMSEY
- Stanislaw Radziszowski, "Small Ramsey Numbers", Electron. J. Combin. Dynamic Survey DS1 (revision of April 24, 2026), https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS1 : the table compared against.
- PySAT (python-sat 1.9.dev17), https://github.com/pysathq/pysat , with Armin Biere's CaDiCaL solver, https://github.com/arminbiere/cadical : the SAT solving that built the object and the run's second checker.
- Found and packaged by Abshalom Dayan with the V3R1T4S kit (https://github.com/elder-plinius/V3R1T4S).
