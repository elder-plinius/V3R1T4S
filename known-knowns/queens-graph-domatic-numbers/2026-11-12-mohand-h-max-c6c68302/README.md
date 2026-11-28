# Queens graph Q_11: no domatic 20-partition (dom(Q_11) <= 19), by a chain of checked proofs

## What
dom(Q_11) <= 19, one below the upper bound 20 of Table 1 of Lauri's Corrigendum (upper bound only), certified for each of two CNF encodings written in separate contexts (formulas/enc1/Fbase.cnf and formulas/enc2/Fbase.cnf, which besides the partition and domination clauses contain, as premises not derived in any proof, two-way definitions of auxiliary variables and symmetry breaking on class labels) not by one proof but by a chain of 681 refutations per encoding, each with its own DRAT proof checked by drat-trim (a Windows build of the unmodified upstream source) and composed by a clause-inclusion argument checked by scripts, the generators of both encodings accepting the authors' own unpublished 19-partition and Lauri's published 18-partition as satisfiable cases.

## Terms used in the sentence above
- Q_11 is the graph whose vertices are the 121 squares of the 11 x 11 chessboard, two squares being adjacent when
  they share a row, a column or a diagonal. A set of squares is dominating when every square is in it or adjacent to
  one of its members. dom(Q_11), the domatic number, is the largest number of pairwise disjoint dominating sets into
  which the 121 squares can be split.
- 681 = 20 x 34 + 1. For each of the 20 class labels: a first lemma (L1), a second (L2), the third lemma cut into 31
  cases (piece-00 to piece-30) and a step that puts the cases together (glue); then one final step for the whole
  formula. The manifests in object/ list the 680 lemma checks, one per line. For the 20 glue steps per encoding the
  DRAT proof is the trivial one (two bytes: the empty clause follows by unit propagation).
- "Composed by a clause-inclusion argument": every formula of the chain contains only clauses of the base formula,
  lemmas proved earlier in the chain, and unit clauses negating the lemma it proves; so each refutation shows that
  the base formula implies that lemma (panel/reproduce.md, section 3).
- The two base formulas (Fbase.cnf) are not shipped as files: how-we-built-it/write_fbase.py rebuilds each in a few
  seconds and their sha256 are in object/certificate.txt. The paths in the sentence, in the panel files and in
  how-we-built-it/REPRODUCE-from-the-saved-files.md (claim/, formulas/, code/, chain/, checker/bin/, partitions/,
  manifests/, final/, attempts/, tmp-check/) are those of the authors' working folders, which are not shipped; in
  this package the programs are in how-we-built-it/ and the lists in how-we-built-it/lists/.

## Check it yourself
From this folder: `sh verify-it-yourself/run_checks.sh`. Expected last line: `PASS`. Time: under a minute on a laptop
(10 to 30 seconds; Python 3, standard library only). This quick check runs no solver and no proof checker: it
rebuilds the two base formulas and all 2 x 680 formulas of the chain from the generators and compares their hashes
with the certificate; it shows what was checked, not that the checks are right. Redoing the checks themselves takes
hours: see RUN_IT_YOURSELF.md.

## Compared to
| table | cell | value there | value here | source | fetched (UTC) |
|---|---|---|---|---|---|
| Table 1 of J. Lauri, Corrigendum, Discrete Math. Lett. 18 (2026) 34-35 | dom(Q_11), upper end of 18-20 | 20 | 19 | https://doi.org/10.47443/dml.2026.195 (the file fetched is the journal's PDF, https://www.dmlett.com/archive/v18/DML26_v18_pp34-35.pdf) | 2026-11-12T00:50:25Z |

## Not claimed
- Not one DRAT proof. No single solver run refuted the formula. The certificate is a chain of 681 refutations per
  encoding, each with its own DRAT proof checked by drat-trim, and a composition argument (which clauses each
  formula may contain) checked by scripts. A single proof file would be about 28 GB for the first encoding and more
  for the second, and could not be checked on our machine.
- Not the bare constraints alone. Each base formula also contains auxiliary variables with two-way definitions and
  symmetry breaking on the class labels; these are premises, not derived in any proof. An implied counting constraint
  (the sum over the 20 classes of min(size of the class, 7) is at most 121) is NOT a premise: it is derived inside
  the proof of the final step.
- The proofs themselves are not in this package (about 80 GB: 79.5 GB for the chain, 0.3 GB for the two final
  proofs; no public archive). A reader must rebuild them.
- One proof checker of record (drat-trim, built locally for Windows from the unmodified source). A second checker
  written from the definition (how-we-built-it/checker2/DratCheck.cs) accepted all 2 x 680 proofs of the chain
  (records in how-we-built-it/checker2/); its full pass ended after the panel had started, so the panel did not see
  it. Tried afterwards on the two proofs of the final step with a limit of 5,200 s of processor time per run, it
  gave no verdict (`s TIMEOUT` on all four runs, neither accepted nor rejected; records in the same folder): for
  these two proofs drat-trim is the only checker.
- Nothing about the lower bound or the exact value of dom(Q_11). The 19-partition used to cross-check the encodings
  on the satisfiable side is our own (draft pull request #954 of github.com/elder-plinius/V3R1T4S; the partition is
  in how-we-built-it/lists/dom-Q11-19-partition.txt), not a published one.
- An earlier, non-DRAT certificate of ours for the same bound (mentioned in pull request #954) is not part of this
  package.
- The exact brief given to the author of the second encoding was not archived inside the project folder; see
  how-we-built-it/REPRODUCE-from-the-saved-files.md, last section.

## Credits
- Juho Lauri, Improved bounds on the domatic numbers of queens graphs, Discrete Math. Lett. 16 (2025) 94-99,
  https://doi.org/10.47443/dml.2025.112, and its Corrigendum, Discrete Math. Lett. 18 (2026) 34-35,
  https://doi.org/10.47443/dml.2026.195 (definitions, Table 1, the published 18-partition used as a cross-check, and
  the first SAT attack on these numbers).
- Hedetniemi, Hedetniemi, Hedetniemi and Hedetniemi, On the domatic numbers of queens graphs, Congr. Numer. 235.
- drat-trim (N. Wetzler, M. Heule, W. Hunt), https://github.com/marijnheule/drat-trim ; CaDiCaL (A. Biere and
  co-authors) through python-sat (A. Ignatiev, A. Morgado, J. Marques-Silva), https://pysathq.github.io .
- The V3R1T4S kit (https://github.com/elder-plinius/V3R1T4S). Credit for this package: mohand-h-max.
