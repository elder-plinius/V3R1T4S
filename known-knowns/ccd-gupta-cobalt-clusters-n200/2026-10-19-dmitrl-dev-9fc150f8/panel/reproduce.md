# REPRODUCE: claim p1 of bank target ccd-gupta-cobalt-clusters-n200

context: subagent (fresh-context delegation)

Role (kit/RUN.md, step 6): "Before reading the author's code, write your own checker from the definition (quote it). Verify every property and the claimed value from the saved files; re-derive every proof step. For an exhaustive search, a sample is a spot check and cannot pass. Fail on any mismatch, missing object or non-determinism."

Input: the claim archive (sha256 `b700d809cbe05fb1feeb02bea1fd5b8ef9c266231b33fcefe60de5f63279c285`) containing CLAIM.md, REPRODUCE.md, TABLE_RECORD.md, data/cobalt.html, data/points.tgz, data/Co.zip, object/ccd_cobalt_audit.csv and verify/check_p1.py. File names below are relative to claim/.

Order of work: I wrote and ran my own checker, then compared its output with the CSV and checked every statement of the claim. Only after that did I open verify/check_p1.py and run it.

## 1. Definition used
CLAIM.md says (verbatim): "Under the Gupta potential with the Cleri-Rosato cobalt parameters (A = 0.0950 eV, xi = 1.4880 eV, p = 11.604, q = 2.286, distances in units of r0)".

CLAIM.md names the potential and its parameters but does not write out the formula. I used the standard Gupta / Cleri-Rosato second-moment form, with no cutoff (all pairs) and r_ij in units of r0:

    E = sum_i [ sum_{j!=i} A exp(-p (r_ij - 1)) - sqrt( sum_{j!=i} xi^2 exp(-2 q (r_ij - 1)) ) ]

After my checker was finished, I opened verify/check_p1.py and found the same formula in its docstring.

The data support this form independently:
- The dimer minimum computed analytically from the formula is r* = 0.879076516 and E* = -3.1506517881 eV. The page posts -3.15065179 for N = 2, and the posted dimer has r = 0.879075940.
- After polishing, 198 of 199 table energies match the posted values within 6e-8 eV.

## 2. Data integrity
- **Pinned hashes.** The sha256 of data/cobalt.html, data/points.tgz and data/Co.zip equal the pins in TABLE_RECORD.md (b1033b41…030ef, bd568d30…5f561, 28141c13…e9ca).
- **Live re-fetch.** I made one GET per URL with the default urllib User-Agent and no retries, at 2026-10-19T05:01:12Z–05:01:22Z, against https://www-wales.ch.cam.ac.uk/~wales/CCD/CoCCD/. All three returned HTTP 200 with the same byte counts (40715, 276791, 25979), the same Last-Modified headers as TABLE_RECORD.md, and sha256 values identical to the pins. The saved files are therefore the files currently served.
- **points.tgz.** It holds exactly 199 files, points/2 … points/200. Each has exactly N non-empty lines of 3 numbers.
- **Co.zip.** It holds 10 coordinate files, Co84, Co95, Co101, Co113, Co121, Co122, Co196, Co197, Co198 and Co200, each with exactly N lines. Co/Energy.txt lists the same 10 sizes.
- **cobalt.html.** It has 199 table entries, N = 2..200, each listed once. For every entry the link points/N, the label N and displayStruct(N) agree. I parsed the page from its HTML cell structure, independently of the author's regex.

## 3. My checker (reviewer-side scripts, not part of claim/: my_check_p1.py, compare_p1.py, sd_check.py)
- **Energy, gradient and Hessian.** All three are vectorised float64 and analytic. Against central finite differences on perturbed N = 13 and N = 38 clusters, the gradient agrees to within 6.95e-9 and 4.98e-8, and the Hessian to within 4.49e-9 and 7.32e-9.
- **Second energy code.** A separate pure-Python version uses math.fsum exact summation. It agrees with the vectorised code for all 209 structures to within 2.3e-13 eV.
- **Polishing.** Every one of the 209 structures was polished twice, each time from the posted coordinates:
  - (a) scipy L-BFGS-B followed by Newton refinement. The refinement uses the analytic Hessian and excludes the 6 zero modes.
  - (b) nonlinear CG followed by the same Newton refinement.
  - (c) An extra path-following check for 11 structures: the eight flagged files plus N = 102, 155 and 184. Each was run with fixed-step steepest descent (step 1/lambda_max, monotone decrease at every step) down to |g| < 1e-4, then Newton.
- **Hessian eigen-analysis** at every polished point.
- **Determinism.** I ran the checker twice in separate processes. The result JSONs are bitwise identical: sha256 b050b365ca71fe130689960acf4faad61ace5b03d54920b9d76d029998d1112a for both runs. Cost per run was about 77–82 s of CPU, with a measured peak RSS of 132.8 MB.

## 4. The one-sentence claim, statement by statement
| # | Statement | My recomputation | Verdict |
|---|---|---|---|
| S1 | all 199 table point files (N = 2..200) and all ten Co.zip files recomputed | 199 + 10 structures recomputed (as is, polished twice, Hessian) | confirmed |
| S2 | the ten Co.zip files reproduce Co/Energy.txt within 5e-7 eV | max abs(E_as_is - Energy.txt) = 4.781e-7 eV (N = 196). Per size: 84 2.44e-7, 95 1.81e-7, 101 4.53e-7, 113 4.48e-7, 121 4.54e-7, 122 1.02e-7, 196 4.78e-7, 197 1.01e-7, 198 1.39e-7, 200 3.18e-7 | confirmed |
| S3 | eight table files (N = 163, 175, 179, 183, 185, 188, 189, 190) are off their posted energy by more than 1e-5 eV as posted | The set of N with abs(E_as_is - E_posted) > 1e-5 is exactly {163, 175, 179, 183, 185, 188, 189, 190}. All eight are higher than posted, by +1.4348e-5, +2.9377e-5, +2.4183e-5, +2.1183e-5, +2.1939e-5, +1.4726e-5, +2.5337e-5 and +2.0669e-5 eV respectively. The largest unflagged deviation is 8.901e-6 (N = 155), so no value lies close to the threshold. | confirmed |
| S4 | every table file reproduces its posted energy within 1e-5 eV after polishing | max abs(E_polished - E_posted) = 1.110e-6 eV (N = 102), the same with both optimizers. 198 of 199 are within 6e-8 eV. | confirmed |
| S5 | no posted structure polishes lower than posted by more than 1e-4 eV | min(E_polished - E_posted) over the table files = -1.110e-6 eV (N = 102). Over the Co.zip files, E_polished - Energy.txt has a minimum of -4.53e-7 eV (N = 101). Both optimizers give these values. | confirmed (table and Co.zip structures) |
| S6 | object/ccd_cobalt_audit.csv is the merged table; the Co.zip energy is the best value at its ten sizes | All CSV fields match (section 5). Co.zip energy minus polished table energy, in eV: 84 -0.056787, 95 -0.092579, 101 -0.182155, 113 -0.009186, 121 -0.025749, 122 -0.021013, 196 -0.247929, 197 -0.004146, 198 -0.055962, 200 -0.147825 | confirmed |

The eight flagged files do not move far when polished. Their maximum atomic displacements are 4.3e-4 to 1.85e-3 r0, and each reaches a minimum within 5e-8 eV of its posted energy: polished minus posted is -4.71e-8, -2.95e-8, +2.94e-8, -3.53e-8, +2.56e-8, +2.79e-8, -2.43e-8 and +4.33e-8 eV, in the order of the S3 list.

## 5. Every row of object/ccd_cobalt_audit.csv
- **Shape.** 199 rows with N = 2..200 in order, each once, and 12 columns throughout.
- **Text fields.** point_group, E_table_posted, E_coZip_posted, the three yes/no flags and best_source match my recomputation exactly in all 199 rows. Rows without a Co.zip file have both Co.zip cells empty.
- **Numeric fields.** I rounded my values to the CSV's own number of decimals and compared the strings. They are equal in every row:

  | Column | Decimals | Rows equal | Max abs difference (eV) |
  |---|---|---|---|
  | E_table_as_is | 9 | 199/199 | 4.94e-10 |
  | E_table_polished | 7 | 199/199 | 4.99e-8 |
  | E_coZip_as_is | 9 | 10/10 | 3.79e-10 |
  | E_best | 7 | 199/199 | 4.98e-8 |

  For E_best I took the minimum of the polished table energy and the Co.zip as-is energy. The Co.zip polished and as-is energies differ by at most 2.35e-9 eV.
- **Row-level result.** 0 mismatches.

## 6. Polished energies: gradient norms reached and certification
- **L-BFGS-B alone** stops at |g|_2 up to 1.10e-5 eV/r0, because the line search runs into float noise.
- **After Newton refinement**, |g|_2 reaches:

  | Path | N >= 3 and Co.zip, max | Median | N = 2 |
  |---|---|---|---|
  | L-BFGS + Newton | 1.36e-13 eV/r0 | 7.7e-14 | 2.1e-11 |
  | CG + Newton | 1.42e-13 eV/r0 | 7.7e-14 | 8.6e-12 |

  The largest single gradient component is 1.16e-11 (the dimer).
- **Agreement between optimizers.** L-BFGS and CG polished energies agree to within 2.3e-13 eV for all 209 structures. For the 11 steepest-descent checks, abs(dE) ≤ 1.1e-13 eV and the largest atomic distance to the L-BFGS minimum is 3.4e-9 r0. Each of those paths decreased monotonically, in 2 to 1216 steps.
- **Hessian.** At every polished point with N ≥ 3, and at all 10 Co.zip structures, there are exactly 6 modes with |lambda| < 1e-6 (the largest of them is 3.9e-13) and no eigenvalue below -1e-6 (the most negative is -3.0e-13). The smallest non-zero |lambda| is 0.280 eV/r0^2. The dimer, being linear, has 5 near-zero modes and no negative eigenvalue. All polished points are therefore local minima in double precision.
- **Displacements.** The largest atomic displacement during polishing is 1.85e-3 r0 for the table files (N = 175) and 9.8e-6 r0 for the Co.zip files.

## 7. Author's checker, run afterwards as REPRODUCE.md says
From claim/, I ran `python3 verify/check_p1.py object/ccd_cobalt_audit.csv data` with Python 3.11.17, numpy 2.4.6, scipy 1.17.1 and single-threaded BLAS. I ran it twice. Both runs exited with code 0 and took 23 s and 44 s of wall time. The two outputs are byte-identical (sha256 4ffdfe0fb6a4472e38c49535a6aa287266ff395c06681a146199368fc0554e52):

    rows checked: 199; Co.zip rows: 10
    as posted, energy off by more than 1e-5 eV at N = 163, 175, 179, 183, 185, 188, 189, 190
    after polishing, every posted energy reproduced within 1e-5 eV: True
    posted structures that polish lower by more than 1e-4 eV: none
    rows whose best known energy is the Co.zip one: 84, 95, 101, 113, 121, 122, 196, 197, 198, 200
    PASS

## 8. Observations (they do not change the verdict)
1. **Functional form.** CLAIM.md does not state the formula explicitly (see section 1). The standard form I used reproduces the data.
2. **Calibration clause of the full target.** As-is, only 84 of 199 table files reproduce their posted energy within 1e-6 eV, because the coordinates are rounded and slightly off the minimum. After polishing, 198 of 199 do. The exception is N = 102: the page posts -388.0998555, while the as-is energy is -388.0998566096 and the polished energy is -388.0998566103, a difference of 1.11e-6 eV. This does not affect p1, whose threshold is 1e-5. It does matter for the target's clause "reproduce the posted energies of ten randomly chosen table point files to 1e-6 eV": that clause holds only for polished energies, and a random draw that includes N = 102 misses 1e-6 by about 1.1e-7 eV.
3. **verify/check_p1.py is looser than the CSV's precision.** It accepts polished and best energies within 2e-6 eV and stops polishing at |g| < 1e-4. It also does not test the Co.zip structures for "polishes lower by more than 1e-4 eV". My stricter checks (section 5, S5) cover all of this, so the looseness hides nothing here.
4. **E_best for the Co.zip rows.** The CSV takes the Co.zip as-is energy, while the author's checker uses the Co.zip polished energy. The two differ by at most 2.35e-9 eV, so the choice does not matter.
5. **Typo on the page.** cobalt.html lists the improved sizes as "84, 95, 101, 113, 121, 122, 196, 107, 198 and 200". "107" is a typo for 197: Co.zip contains Co197.txt. This is harmless.
6. **Reading of "not reproduced".** The p1 wording "listing every N where the posted energy is not reproduced within 1e-5 eV" can be read two ways, as-is or after polishing. The CSV carries flags for both, and both are correct: as-is, the eight files listed in S3; after polishing, none.
7. **Not checked here.** I did not check the verbatim bank text at commit 04fdfba against the V3R1T4S repository. It lies outside the claim folder, and I made no request for it.

## 9. Budget and actions
- **CPU.** My two full runs used about 82 s and 77 s of CPU. The steepest-descent check used 22.6 s. The author's checker ran for 23 s and 44 s of wall time. In total this is well under the 20-minute limit, with one heavy process at a time.
- **Memory.** Measured peak RSS was 132.8 MB for the second full run and 125.8 MB for the steepest-descent check. Peak memory was not measured for the first run or for the author's checker.
- **Network.** Three GETs, one per URL, with no retries.
- **Outward actions.** None.

## Verdict
Every row and field of object/ccd_cobalt_audit.csv matches my recomputation. All six statements of the one-sentence claim are confirmed on all 199 table files and all 10 Co.zip files, with no sampling. The polished energies are certified minima with gradient norms of about 1e-13 eV/r0. Both checkers are deterministic, and the author's checker prints PASS.

pass: true