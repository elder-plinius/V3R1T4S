context: subagent (fresh Claude Code Agent-tool context, general-purpose)

# REPRODUCE skeptic: #23 site threshold claim

I worked only inside a private copy of the claim folder. I wrote my own checkers in claim/my_check/ (tm.py, tm_kag.py, extrap.py, mc_analyze.py, mymc.c, lattice23.py) before I opened any of the author's code. After that I ran the author's REPRODUCE.md steps 0 to 4. I did not run test_stream.py or test_nzwrap2.py (both optional). In a later repair round:
- I recomputed the #23 site roots n = 9..16 with the claim's streamed program (item 9);
- I ran a step-5-style fresh-seed Monte Carlo with the claimant's evaluator at 96 x 24 (item 10).

## Definitions I checked against (quoted from rules/PREREG.md)

- Method A: "p_c(n), the root of Lambda_open(p) = Lambda_closed(p) on the n x infinity cylinder of circumference n a1 (a1 = (1,0), along the rows)". I derived the two sectors from the torus criterion P(2D) = P(0D) in the long-torus limit:
  - sector A: connectivity states in which any cluster closing a cycle around the circumference kills the configuration.
  - sector B: one marked cluster that must reach every layer.
  - p_c(n) is the root of Lambda_A = Lambda_B.
- Extrapolation: "ansatz p_c(n) = p_c + sum_{k=1..K} A_k n^(-e_k) ... e_k = 2(k+1) if the local exponent from the three largest n is within 0.5 of an even integer >= 4 ... K = 1..4, each solved exactly on the K+1+j largest available n, j = 0, 1, 2, using only n >= 4. p_TM = median of the family; sigma_TM = max |estimate - p_TM|".
- Method B: "R_0D(n) = P(n < n1), R_2D(n) = P(n >= n2), canonical curves by binomial convolution. p_L = root of R_2D(p) - R_0D(p) = 0 from the pooled histograms; sigma_L = jackknife over ... blocks. FSS fit (primary): weighted least squares p_L = p_MC + A L2^(-4) over the sizes with L2 >= 16; sigma_MC from the fit covariance, multiplied by sqrt(chi2/dof) when chi2/dof > 1. Stability: the same fit restricted to L2 >= 24 must agree with the primary within one sigma_MC."
- Decision rules (a), (b) and (c) are as worded in rules/PREREG.md.

## What I checked

1. **Manifest.** I hashed every file listed in MANIFEST.sha256 with my own script.
   - Result: 2013 files listed, 0 bad, 0 missing.
   - The only unlisted file is MANIFEST.sha256 itself.

2. **The lattice is #23** (my_check/lattice23.py).
   - I built rows S S S T geometrically: unit squares, unit triangles, and a 1/2 shift across the T row.
   - I found each vertex's faces from the angular gaps between its unit-length edges:
     - lines 0 and 3 are (3,3,3,4,4);
     - lines 1 and 2 are (4,4,4,4);
     - fractions are 1/2 and 1/2; z = 5 and 4; zbar = 9/2.
   - This matches row 23 as recorded in table/table_record.md: (1/2)(3^3,4^2) + (1/2)(4^4), z 5,4, zbar 4.5.
   - Lines 1 and 2 are mirror images, and so are lines 0 and 3, so there are 2 orbits.
   - The other row lattice with the same two vertex types is SST, which has fractions 2/3 and 1/3; that is #22.
   - The adjacency my transfer matrix uses matches this geometry.
   - The author's evaluator-first/code/test_lattices.py also passes: `ok #23: fractions {... 1/2, ... 1/2}, zbar 9/2, 2 orbits` and `TESTS: PASS (0 failures)`.
   - The author's rows() construction is the same geometry as mine.

3. **Transfer-matrix roots, independent code** (my_check/tm.py, Python, sparse eigenvalues).
   - Square site, n = 2..6: matches Jacobsen's table (exact-polynomial/out/jacobsen_table2_square_site.txt) to 1e-15. Example, n = 6: 0.592507356205642.
   - Triangular site: 1/2 at every n.
   - Kagome site (my_check/tm_kag.py), 2 to 5 cells: 0.652703644666139 = 1 - 2 sin(pi/18) at every width. This confirms that my sector definition is the right one.
   - #23 site, n = 2..9: every root equals exact-polynomial/out/r23_site_series.txt to within 1e-15. Examples:
     - n = 8: 0.571708088280108 (file: 0.57170808828010811);
     - n = 9: 0.571729202384443 (file: 0.57172920238444325).
   - State counts also match: 3, 7, 19, 51, 141, 393, 1107, 3139.
   - My Python n = 10 run passed 2 GB of memory and I stopped it. Instead, the author's C program reproduced n = 10 (see item 7).

4. **Extrapolation, independent implementation** (my_check/extrap.py, 40-digit mpmath).
   - The quoted rule can be read two ways:
     - windows: an exact solve on K+1 consecutive n, dropping the j largest;
     - least squares on the K+1+j largest n.
   - For #23 site with n_max = 16:
     - local exponent 4.0793, so the even family 4, 6, 8, 10 applies;
     - windows reading: p_TM = 0.571764539546341, sigma = 1.042e-7 (12 estimates);
     - union of both readings (24 estimates): the same p_TM and sigma.
   - This is the claimed 0.57176453954634 +- 1.04e-7 exactly. The author's extrapolate.py documents the union choice and prints the same values.
   - With n_max = 15, my union gives 0.5717645628 +- 1.075e-7, the interim value recorded in rules/PREREG.v2.md.
   - My rule also reproduces:
     - #23 bond: 0.45844602208062 +- 3.75e-8;
     - (3^3,4^2) site: 0.55021219057408 +- 8.01e-8;
     - (3^3,4^2) bond: 0.41964035938487 +- 1.47e-8.
   - Calibration of the rule on Jacobsen's square-site sequence (true value 0.59274605079210), truncated at n_max = 10..21: the error is 0.3% to 1.8% of sigma_TM at every n_max. At n_max = 16 the error is 6.6e-10 against a sigma of 5.2e-8. So the rule's sigma is conservative.
   - Local exponents of the #23 site series rise smoothly from 3.94 (n = 10) to 4.08 (n = 16); there are no jumps in n = 11..16.

5. **Monte Carlo from the saved histograms** (my_check/mc_analyze.py).
   - For every block the counts sum to its stated sample count.
   - Every p_L, sigma_L and blocks count in result/threshold_23_site.json is reproduced to the printed digits, for all 8 #23 site sizes.
   - #23 site fits:
     - primary: p_MC 0.571766679 +- 1.393e-6, A -0.049896, chi2 3.515 on 4 dof;
     - L2 >= 24: 0.571767860 +- 1.741e-6. The difference is 1.18e-6, below 1.393e-6, so STABLE.
   - Check torus 2048 x 512: 0.571764522 +- 2.273e-5.
   - #23 bond: 0.458445217 +- 1.553e-6.
   - Kagome: 0.652704208 +- 9.886e-7, which is +0.57 sigma from exact.
   - Square: 0.592745302 +- 9.87e-7, which is -0.76 sigma.
   - (3^3,4^2) site: 0.550212455 +- 1.889e-6, chi2 8.45 on 3 dof (sigma inflated by sqrt(chi2/dof)).
   - Triangular, p_L - 1/2: +1.83, +0.12 and +1.40 sigma.

6. **Independent Monte Carlo evaluator** (my_check/mymc.c).
   - It is my own Newman-Ziff code: union-find with lifted displacements, n1 and n2 as defined above, my own xoshiro256** seeding, and my own #23 adjacency.
   - Run: 64 x 16 torus, 10 blocks x 400,000 samples, seeds 900000-900009.
   - Result: p_L = 0.571764198 +- 8.94e-6. The saved value is 0.571766140 +- 1.74e-6, a 0.21 sigma difference. The saved histograms are consistent with an independent evaluator on the correct lattice.

7. **The author's REPRODUCE.md steps, run on the claim copy.** The compiler was `python -m ziglang cc -O2`.
   - Step 0: manifest OK.
   - Step 1: PASS (item 2).
   - regress.py: worst diff 5.0e-16, `REGRESSION: PASS`. This includes kagome site and (3,12^2) site, exact for n = 1..4.
   - run_series "#23" site 1 8 and bond 1 6: every pc equals the saved file byte for byte.
   - Extra runs:
     - site n = 9..10 and bond n = 7..10, starting the series fresh;
     - n = 10 site is identical;
     - the others differ from the file only in the last 1-2 ulps (at most 4e-16), because run_series.py picks its root bracket from the previous lines of the output file;
     - repeated runs with the same start are identical, so this is path dependence, not non-determinism.
   - extrapolate.py:
     - `p_TM 0.57176453954634  sigma_TM 1.04e-7  (24 estimates)`;
     - bond: `p_TM 0.45844602208062  sigma_TM 3.75e-8`.
   - calib_rule.py:
     - square: |err|/sigma 0.00-0.02 for n_max = 10..21;
     - (3^3,4^2) bond at n_max = 12: +5.2e-10 (0.04 sigma).
   - Step 4 printed exactly the expected lines:
     - `primary L2>=16 p_MC 0.571766679 +- 0.000001393`, STABLE, (a) AGREE, (b) WITHIN;
     - check torus `p_L 0.571764522 +- 0.000022729`;
     - bond `p_MC 0.458445217 +- 0.000001553`;
     - kagome +0.57 sigma, square -0.76 sigma;
     - `D +4.216e-07 +- 6.472e-07 (+0.65 sigma) -> PASS`;
     - `TRIANGULAR ESTIMATOR TEST: PASS`;
     - (3^3,4^2) (a) AGREE.

8. **Numbers in CLAIM.md and result/threshold_23_site.json**, recomputed:
   - Rule (a): |p_TM - p_MC| = 2.13945e-6 against 3 combined sigma = 4.19063e-6, which is 1.5316 combined sigma. CLAIM.md says 1.53.
   - Rule (b): |p_TM - 0.5720| = 2.3546e-4 against 6.0e-4, which is 1.18 sigma.
   - Rule (c), transfer matrix, bond: |TM - 0.45844622| = 1.98e-7, below 1e-6, with sigma 3.75e-8 (at most 1e-7).
   - Rule (c), Monte Carlo, bond: 1.003e-6 = 0.65 sigma, with sigma at most 2e-6.
   - Kagome sigmas from exact: 0.5696; square: -0.7587.
   - Check torus: |p_L - p_MC| = 2.16e-6 against 6.8e-5.
   - Rounding in the claim sentence is correct: 0.57176454 +- 0.00000010 and 0.5717667 +- 0.0000014.
   - The bank's uncertainty bound (2e-6) and the prereg bounds (sigma_TM at most 2e-7, sigma_MC at most 2e-6) are all met.

## Repair round: transfer-matrix roots n = 9..16 recomputed, and a second fresh-seed Monte Carlo

9. **#23 site roots with the claim's streamed program, n = 9..16** (requested by the panel's main session).
   - Setup:
     - built per REPRODUCE.md step 2;
     - the new output file my_check/r23_site_11_16.txt was seeded with my step-3 recomputation of n = 1..8 (r23_site_check.txt, byte-identical to the saved file), so that run_series.py picks its brackets exactly as in the original series;
     - command: `python exact-polynomial/code/run_series.py "#23" site 9 16 my_check/r23_site_11_16.txt tmcrit_stream.exe`;
     - launched with PowerShell Start-Process at BelowNormal priority; the tmcrit_stream.exe child processes inherited BelowNormal;
     - one process at a time, about 0.56 GB of memory at n = 16;
     - scratch in exact-polynomial/scratch, peaking at about 9.3 GB. The program emptied it itself and I removed the empty folder.
   - Wall clock 00:42:49 to 02:28:36. Compute times per root: n = 11: 21.6 s, n = 12: 57.1 s, n = 13: 201.5 s, n = 14: 504.2 s, n = 15: 1707.9 s, n = 16: 3839.0 s.
   - Result: **every root n = 9..16 is bit-identical** to the line of the same n in exact-polynomial/out/r23_site_series.txt. Identical means the same pc, the same root bracket and the same state counts; fields 1-14 of every line n = 1..16 compare byte-identical (`cmp`). For example:
     - n = 16: pc 0.57176107923512143, 5196627 states in each sector;
     - n = 15: pc 0.57176004479806108.
   - Extrapolating the recomputed file:
     - author's extrapolate.py: `p_TM 0.57176453954634  sigma_TM 1.04e-7  (24 estimates)`;
     - my extrap.py: 0.571764539546341 +- 1.042e-7.
   - So the claimed value now rests entirely on roots that the panel recomputed.

10. **Fresh-seed Monte Carlo at a second fit size, with the claimant's evaluator.**
   - Command: `python timeline-aligner/code/mc_worker.py "#23" site 1 4 24 8 81000 my_check/fresh_mc24 nzwrap2.exe`, at BelowNormal priority.
   - Run: 96 x 24 torus, seed 81024, 8 blocks of 488,000 samples (3,904,000 in total). Each block took 294-323 s; the whole run took about 47 min.
   - Analysis: timeline-aligner/code/analyze_mc.py and my mc_analyze.py both give **p_L = 0.571759490 +- 4.330e-6**.
   - The saved 96 x 24 value is 0.571763300 +- 2.528e-6. The difference is 3.81e-6, which is **0.76 combined sigma** (combined sigma 5.01e-6). With only 8 blocks the jackknife sigma is itself uncertain. Using the per-block spread of the saved data instead (about 6.9e-6 for 8 blocks), the difference is about 0.5 sigma.
   - Together with my own evaluator at 64 x 16 (item 6: 0.21 sigma), the Monte Carlo is reproduced with fresh seeds at two fit sizes.

## Mismatches and concerns

- **No numerical mismatch found.** One near-miss: from the rounded fit outputs I got the common offset D = 4.2045e-7. The author's file gives 4.216e-7, and it uses the unrounded kagome offset (+5.633e-7 instead of +5.634e-7). The author's command on the saved files prints 4.216e-7 exactly, so this is a rounding effect, not an error.
- **Resolved in the repair round: transfer-matrix roots for n = 11..16 were not recomputed in the first pass.** They are now recomputed with the claim's streamed program and are bit-identical (item 9). Remaining limit: my independent Python transfer matrix covers n <= 9 only. Above that, the check is the claim's own program rerun, not an independent algorithm.
- **sigma_TM is a convergence spread, not a statistical one-sigma.** Its reliability rests on calibration:
  - on the square-site sequence it is 50 to 300 times larger than the true error;
  - on the (3^3,4^2) bond sequence it is 25 times larger at n_max = 12;
  - but at very small n_max the rule fails: (3^3,4^2) bond at n_max = 6 is off by 9.7 sigma. The #23 site series is far beyond that regime.
  - The Monte Carlo can only test the claimed value at the 1.4e-6 level, not at 1e-7.
- **The Monte Carlo fit goes up to 512 x 128.** The 2048 x 512 torus has only 4000 samples (sigma 2.3e-5), so it is a weak check. The bank's "L >= 2048" wording is an example ("for example"), not a requirement.
  - The report-only free-exponent fit for #23 is unconstrained: w = 0.52 +- 1.37.
  - The amplitude A changes from -0.05 (primary fit) to -1.25 (L2 >= 24 fit), although the stability rule passes.
- **All three triangular offsets are positive.** The pre-registered common-offset test passes at 0.65 sigma. The Monte Carlo sits 1.5 combined sigma above the transfer matrix for #23, which is consistent with a small positive estimator bias of the same kind but does not fail any rule.
- **Not checked by me (outside the reproduce role, and no network):** the live Wikipedia fetch (table/table_record.md) and the literature search for criterion (d) (table/literature_record.md). I took both as recorded.
- **Housekeeping in my copy:**
  - The author's step 3 commands wrote r23_site_check.txt, r23_bond_check.txt and build outputs inside my claim copy.
  - One awk redirect of mine wrote two small scratch files outside the claim copy (a temporary folder).
  - My stopped n = 10 Python run briefly used about 2.2 GB of memory.
  - The repair-round runs left only my_check/r23_site_11_16.txt (with its .stderr file), my_check/fresh_mc24/, and the run_11_16 and fresh24 stdout/stderr files. The transfer-matrix scratch folder is removed.

pass: true
