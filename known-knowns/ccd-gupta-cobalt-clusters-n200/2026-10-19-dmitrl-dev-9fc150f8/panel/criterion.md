# CRITERION panel report: claim for partial win p1 of `ccd-gupta-cobalt-clusters-n200`

context: subagent (fresh-context delegation)
role: CRITERION (kit/RUN.md step 6), one of three skeptics. Input: the claim folder only (archive `claim_p1.zip`, sha256 `b700d809cbe05fb1feeb02bea1fd5b8ef9c266231b33fcefe60de5f63279c285`), plus read-only checks of the public sources the claim names.
No outward action was taken (no comments, issues, PRs, pushes or messages).

## Verdict

The claim asks for **partial win p1** only. It does not assert the full success criterion, and it does not meet it, because no structure below a record is offered.
Read clause by clause, p1 is met. I recomputed every number the claim relies on with my own code (energy, gradient and Hessian written separately from `verify/check_p1.py`), using a polish about 10^8 times tighter in gradient norm than the author's, and checked the borderline cases in 30-digit mpmath. Every flag and every number in `object/ccd_cobalt_audit.csv` agrees with my results.
There is one interpretive caveat, about the calibration clause that p1 inherits through "the calibrated potential". It is documented below. It does not change any p1 output.

## p1, read literally, clause by clause

p1 (verbatim; I checked it character-for-character against the bank file at commit `04fdfba4…` and on `main`; both match `CLAIM.md`): "Audit: recompute all 199 table point files plus the ten Co.zip files with the calibrated potential and publish a merged table, listing every N where the posted energy is not reproduced within 1e-5 eV or a posted structure polishes lower by more than 1e-4 eV."

| Clause | Finding | Status |
|---|---|---|
| "all 199 table point files" | `data/points.tgz` has 199 files, N = 2..200. Each file has exactly N lines of 3 numbers (minimum pair distance over all files 0.879 r0). The page table parses independently to 199 unique (N, PG, energy) cells with no duplicates. I fetched 11 individual `points/N` files linked from the table (the 8 flagged N plus 102, 155, 13). All 11 are byte-identical to the `points.tgz` members, with Last-Modified 2005-10-16. | ✓ (the other 188 individual files were not fetched, so their equivalence is provisional) |
| "plus the ten Co.zip files" | `data/Co.zip` has Co84, 95, 101, 113, 121, 122, 196, 197, 198, 200 and `Co/Energy.txt` with 10 values. The page text says "107", but the archive holds 197; the claim follows the files, as the bank's Traps section prescribes. | ✓ |
| "with the calibrated potential" | Cleri-Rosato Co: A 0.0950, xi 1.4880, p 11.604, q 2.286. All ten Co.zip files reproduce Energy.txt as posted within 4.781e-7 eV (worst N = 196). After polishing, 198 of 199 table energies match the posted value within 6e-8 eV (the rounding of the posted digits). The exception is N = 102, which sits 1.110e-6 eV below its posted value. See the caveat for the literal 1e-6 table clause. | ✓ in substance (caveat C1) |
| "publish a merged table" | `object/ccd_cobalt_audit.csv` has one row per N = 2..200 and columns table posted / as-is / polished, Co.zip posted / as-is, `E_best`, `best_source`. Its `point_group` and `E_table_posted` strings equal the page in all 199 rows, and its `E_coZip_posted` strings equal Energy.txt. | ✓ |
| "listing every N where the posted energy is not reproduced within 1e-5 eV" | As posted: exactly N = 163, 175, 179, 183, 185, 188, 189, 190. Their deviations (as-is minus posted) are +1.435e-5, +2.938e-5, +2.418e-5, +2.118e-5, +2.194e-5, +1.473e-5, +2.534e-5, +2.067e-5 eV. The largest of the other 191 is 8.901e-6 (N = 155, 1.1e-6 below the threshold). After polishing: none (max 1.110e-6). Co.zip: none. | ✓ complete and correct |
| "or a posted structure polishes lower by more than 1e-4 eV" | Table structures against their own posted energy: none (minimum polished minus posted is -1.110e-6, at N = 102). Co.zip structures against Energy.txt: none (minimum -4.533e-7). | ✓ (Co.zip half checked by me; see C2) |

The author's checker, run exactly as in `REPRODUCE.md` (`python3 verify/check_p1.py object/ccd_cobalt_audit.csv data`), returned code 0 with last line `PASS` in 20.5 s. Its summary lines match all of the above.

## Independent recomputation (reviewer-side scripts, not part of claim/)

- Data authenticity: I made one GET per URL to the three CCD files at 2026-10-19T05:01:39Z–05:01:44Z. All returned HTTP 200 with sizes 40715 / 276791 / 25979 bytes. Their Last-Modified headers match `TABLE_RECORD.md`, and their sha256 equals the pins in `verify/check_p1.py` and the files in `data/`.
- Energy: float64 with compensated summation. Gradient and Hessian are analytic, and both were checked against finite differences on N = 13, 38 and 75 at perturbed geometries (gradient error ≤ 4.6e-8, Hessian error ≤ 2.0e-7, on entries up to 1.3e2).
- Polish: L-BFGS-B followed by Newton steps with the zero modes projected out. The final gradient norm is ≤ 8.79e-13 for table structures and ≤ 9.50e-13 for Co.zip structures, compared with the < 1e-4 gate in the author's checker.
- 30-digit mpmath re-evaluation of 26 structures (the 8 flagged; N = 2, 13, 55, 100, 102, 147, 155, 200; and all 10 Co.zip). It agrees with float64 within 9.79e-14 eV as posted and 1.10e-13 eV polished. The 30-digit gradient norm at the polished points is ≤ 9.54e-13, below the full criterion's 1e-10.
- Hessian of all 209 polished structures: no eigenvalue below -1e-6 (the minimum is -3.9e-13). Each has exactly 6 near-zero modes, except N = 2, which has 5 as a linear dimer should. The smallest non-zero |lambda| is 0.2803. No saddle point could therefore hide a downhill polish. The author's looser polish (|g| < 1e-4) is accurate to about |g|^2/(2·0.28), roughly 2e-8 eV.
- CSV against my values: `E_table_as_is` differs by at most 4.94e-10, `E_table_polished` by 4.99e-8, `E_coZip_as_is` by 3.79e-10 and `E_best` by 4.98e-8. All three yes/no flag columns and `best_source` agree in all 199 rows.

## Hidden quantifiers and stretched definitions examined

- C1, calibration clause (inherited through "the calibrated potential"). The full criterion requires the checker to "reproduce the posted energies of ten randomly chosen table point files to 1e-6 eV". Read literally on the coordinates as posted, the exact potential fails this clause: only 84 of 199 table files are within 1e-6 eV as posted, so a random ten passes with probability 1.295e-4. With a polish first, 198 of 199 are within 1e-6, so a random ten passes with probability 0.9497; only a draw that contains N = 102 fails. I made one literal draw, N = [16, 21, 89, 92, 93, 106, 108, 109, 115, 185]. As posted, 7 of those 10 miss 1e-6. After polishing, all ten pass.
  The as-posted shortfall is a property of the CCD point files, not of the potential:
  - As-posted gradient norms are 1.80e-2 to 2.20e-2 for the flagged N, with a median of 6.54e-3 for the rest.
  - The as-is minus posted deviation has a median of +1.28e-6 eV.
  - The rounding null and the parameter null below rule out the alternative explanations.
  The bank's checker recipe itself specifies polishing the posted structures. I therefore read "calibrated" as polish-then-compare, and under that reading the potential is calibrated. `CLAIM.md` does not report the 1e-6 table calibration explicitly (it reports 1e-5 after polishing). The figure can be derived from its own CSV: 198 of 199 rows have |`E_table_polished` − `E_table_posted`| ≤ 6e-8.
- C2, "no posted structure polishes lower" (claim sentence). `verify/check_p1.py` asserts this only for table structures; it never compares the polished Co.zip energies with Energy.txt. I checked that half and it holds (the largest lowering is 4.5e-7 eV). The CSV has no `E_coZip_polished` column, but `E_best` minus `E_coZip_posted` (≤ 5.0e-7 for the ten Co.zip rows) carries the same information.
- C3, the meaning of "polishes lower". The claim reads it as lower than that structure's own posted energy. Under the cross reading, a Co.zip structure lower than the table energy for the same N, all ten Co.zip N qualify, by 0.0041 eV (N = 197) up to 0.2479 eV (N = 196). The merged table lists exactly these ten as `best_source = Co.zip`, so the listing requirement is met under either reading.
- C4, table point files versus the tgz. This was checked by sampling (see above) and found identical for all 8 flagged N.
- C5, the polish routine. p1 does not define one. The full criterion's routine (extended precision, |g| < 1e-10) gives the same flags as the author's float64 L-BFGS polish. My float64 Newton polish meets |g| < 1e-10 in a 30-digit evaluation on the 26 structures checked.
- Non-subsumed. The target page on `main` is identical to the pinned commit ("open as of 2026-10-15"). `TROPHY_CASE.md` on `main` does not mention cobalt or `ccd-gupta`. At the pinned commit, the only repository paths containing 'cobalt' or 'ccd-gupta' are two known-unknowns entries: this target and a separate Murrell-Mottram target. I found no prior p1 win. p1 is an enumerated partial win in the bank, and the audit yields new information: 8 under-relaxed point files, plus N = 102 posted 1.11e-6 eV high.

## Null models

- Rounding null. I rewrote the exact polished minima in the CCD point-file format (6 significant digits, 6 decimals). The energy rose by at most 8.498e-8 eV (N = 198), and by 6.1e-8 to 7.9e-8 for the 8 flagged N; no N rose by more than 1e-6. Coordinate rounding therefore explains neither the 8 flags (≥ 1.4e-5) nor the 1e-6-level shortfalls. Those come from under-relaxed coordinates: polishing moves atoms by at most 1.85e-3 r0 for the flagged N and 9.95e-4 r0 for the rest. Because 357 tokens (e.g. in N = 102) carry full 6-decimal precision, this null is an upper bound.
- Parameter null. These perturbations were applied to the as-is table energies; the counts are how many of 199 files stay within 1e-5 eV:

  | Perturbation | Files within 1e-5 eV |
  |---|---|
  | A × (1+1e-6) | 11 |
  | xi × (1+1e-6) | 2 |
  | A × (1+1e-5) | 1 |
  | xi × (1+1e-5) | 0 |
  | p × (1+1e-5) | 0 |
  | q × (1+1e-5) | 5 |
  | p = 11.60 | 0 |
  | q = 2.29 | 0 |

  The unperturbed set gives 191, and 199 after polishing. The 1e-5 test is therefore highly discriminating, and the posted data pin the parameter set to about 1e-6 relative.
- Saddle null. Covered by the Hessian check: all 209 polished posted structures are local minima.

## Caveats (none changes a p1 output)

1. The literal as-posted reading of the 1e-6 table calibration clause cannot be met by the exact potential (C1). This is a bank wording issue that maintainers may want to fix: state "after polishing", and note N = 102.
2. The claim's checker does not assert the Co.zip polish half of its own sentence, and its tolerance on polished energies is 2e-6 (C2). I verified both independently.

## Network log (one GET per URL, default urllib User-Agent, no retries, nothing blocked)

- 3 CCD files: `cobalt.html`, `points.tgz`, `Co.zip`.
- 11 CCD `points/N` files: N = 163, 175, 179, 183, 185, 188, 189, 190, 102, 155, 13.
- GitHub: the API tree at commit `04fdfba48c6e277fe083b6811f1a5deb3c52b74e` (1 request), the target `.md` at that commit (1), `TROPHY_CASE.md` on `main` (1), and the target `.md` on `main` (1).

## Resource use

The author checker took 17.2 s user time on the first run and 20.5 s wall time on the second. My 209-structure audit took 35.4 s user time, and the 26-structure mpmath run took 34.5 s. I ran one heavy process at a time with at most 2 BLAS threads. Peak memory of the background scripts was not measured; the largest array is a 600 × 600 Hessian.

confirmed_scope: With the Gupta potential A = 0.0950 eV, xi = 1.4880 eV, p = 11.604, q = 2.286 (r in units of r0), which reproduces all ten Co.zip energies within 4.8e-7 eV as posted and 198 of 199 table energies within 6e-8 eV after polishing (N = 102 lies 1.1e-6 eV below its posted value), object/ccd_cobalt_audit.csv correctly recomputes all 199 CCD cobalt table point files in data/points.tgz (sha256-identical to the live CCD download of 2026-10-19) and all ten Co.zip files, and the only N whose posted table energy is not reproduced within 1e-5 eV are N = 163, 175, 179, 183, 185, 188, 189 and 190 for the coordinates as posted (all within 1e-5 eV after polishing), while no posted table or Co.zip structure polishes lower than its own posted energy by more than 1e-4 eV.
pass: true
