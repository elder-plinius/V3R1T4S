Saved by the main session of run 2026-10-16-0731 from the CRITERION subagent's returned text (fresh Agent-tool context, model opus, finished about 08:17Z), text below as returned between its BEGIN and END markers.

# CRITERION skeptic: p2 claim, row #22 bond threshold (row word TSS)

context: fresh subagent (Agent tool), model opus, given only a copy of claim/

Time window: started 2026-10-16T07:51:28Z (date -u), last check 08:16:33Z.

What I read: everything in claim/; kit RULES.md and LESSONS.md; the bank entry `site-percolation-2-uniform-lattices-thresholds` (criterion, p2 text and pitfalls).

Sources opened through the shared helper (lens criterion-p2). These are one GET each with no retries; nothing was blocked and nothing was appended to the stop list:
- https://arxiv.org/pdf/1910.12376 (Scullard and Jacobsen 2020): 200, sha256 32c67e04472de0789db28366c231b2f6a1211911ca9fdb20ceced4e7279423d0, 347481 bytes, 2026-10-16T07:54:23Z
- https://arxiv.org/pdf/1507.03027 (Jacobsen 2015): 200, sha256 48004dc4bd22ae9d2f4cd3dfdb3685c5a6c25d1a4c707083a103f4044e0375d6, 574584 bytes, 2026-10-16T07:54:24Z

I also ran three WebSearch queries for a published bond value of this lattice and found none.

My scripts and outputs are in work/: robust.py, robust_out.txt, calib/, other/, tm_W8.txt, tm_W9.txt, tm_W10.log, tm_W10.time, pids.txt. The two PIDs I started, 67488 and 69962, have both finished.

injection_suspected: none.

## 1. Cell, table and lattice identity

**Hashes.** `shasum -a 256` gives status_source/wikipedia_percolation_threshold.html = 2f44ce4065839fa2baf1c1655cdcf5aa40e21fcdb7cdabf69287093e0fd27e95 and result/p2_value.json = 51d575bafaa6558f1f65bd6cd46f1fd2bc113e4717d93994d9bbbdeccec68c23. Both equal the values in CLAIM.md. NUMERICAL.

**The cell.** I parsed the raw HTML myself rather than using the claim's parser. The row sits under the heading "2-uniform lattices", before "Inhomogeneous 2-uniform lattice". Its text is: `22 ( 2 ⁄ 3 )(3 3 ,4 2 ) + ( 1 ⁄ 3 )(4 4 ) 5,4 4 2 ⁄ 3 0.5648(2) [ 74 ] 0.44528611(40) [ citation needed ]`.
- So the cell is a "citation needed" bond threshold in the same table as the 2-uniform site thresholds. KNOWN (saved copy).
- I did not re-fetch the live page. The saved fetch time comes from the claim and is not my own measurement.
- The claim's statement that the value came from "Gu and Ziff, to be published" cannot be checked from the saved page, which shows only [citation needed]. It does not affect the result.

**Lattice, derived by hand.** In the word T,S,S the gaps are T between rows 0 and 1, S between rows 1 and 2, and S between rows 2 and 0.
- Rows 0 and 1 each get 2 horizontal edges, 2 edges from the T gap and 1 from an S gap. That is degree 5, with three triangles and two squares: 3^3.4^2.
- Row 2 gets 2 horizontal edges and 1 vertical from each of its two S gaps. That is degree 4: 4^4.
- Fractions are therefore 2/3 and 1/3, and z-bar = (5+5+4)/3 = 14/3, matching "4 2⁄3". PROVED-HERE.
- The diagonal direction in a T strip does not matter: shifting the column labels of the upper rows gives an isomorphic graph on the cylinder. PROVED-HERE.
- TSSS would give 1/2 and 1/2 (row #23), so TSS is the only row word for #22. PROVED-HERE.
- `python3 -I code/check/q9_check.py lattice TSS` prints degrees {4: 48, 5: 96}, config {'3^3.4^2': '2/3', '4^4': '1/3'} and zbar 14/3. NUMERICAL.

## 2. "Independent determination": of what?

**What is determined.** The infinite-lattice bond percolation threshold of the TSS 2-uniform lattice, estimated by extrapolating the roots p(W) of Λ_open = Λ_closed on W × ∞ cylinders, W = 2 to 10. This is Jacobsen 2015 eq. (13) and Scullard and Jacobsen 2020 eq. (4); I opened both. KNOWN.

**Independent of what.** It is independent of the table's unsourced value. The two programs (code/tm/tm.cpp and code/eig/eig.c with mkgraph.py) are separate implementations with different designs: a slot/operation transfer matrix in C++ versus a graph-input Taylor-series power iteration in C. HEURISTIC (I read the headers, not a full audit).

**Limits of the independence.**
- Both programs use the same method and the same extrapolation pipeline (E1). They cross-check the finite-size roots, not the extrapolation.
- The extrapolation rests on the empirical scaling form that Scullard and Jacobsen 2020 also use ("There is currently little theoretical understanding of this scaling"). KNOWN.
- The value is therefore a numerical estimate with a convergence-based, non-rigorous error bar, the same epistemic status as published values from this method. HEURISTIC.

**My reproduction checks** (I rebuilt both programs in work/bin). NUMERICAL.
- TSS bond roots, my rerun minus data/tm/TSS_bond.tsv:

| W | difference |
|---|---|
| 5 | −2.16e-15 |
| 6 | −2.22e-15 |
| 7 | −2.72e-15 |
| 8 | +6.60e-16 |
| 9 | −2.30e-16 |
| 10 | −1.34e-15 |

- The W = 10 rerun took 383.49 s real time with a maximum RSS of 771850240 bytes.
- tm versus eig tables for TSS: the largest difference over W = 2 to 10 is 1.56e-15.
- Kagome roots from data/tm/kagome_bond.tsv versus Scullard and Jacobsen 2020 Table II, n = 1 to 6: the largest |difference| is 2.49e-15.
- Exact tests rerun: S bond at p = 0.5, W = 4 and 6, gives f = −1.39e-16 and 4.86e-16. T bond at 2 sin(π/18), W = 4 and 6, gives f = −6.38e-16 and 2.50e-16.

## 3. PREREG rule 4: main branch or fallback?

**Data.** Last four sizes W = 7 to 10. Differences are −9.583e-8, −3.878e-8 and −1.885e-8. Ratios of successive differences are 0.4047 and 0.4860. A pure W^-6 law gives 0.4126 and 0.4561; a pure W^-5 law gives 0.4687 and 0.5106. NUMERICAL.

**Reading.** The sequence is monotone, |differences| strictly decrease, and the ratios behave like a smooth power law. D_eff for the two three-point windows inside the last four sizes is 6.151 and then 5.439, which is also monotone. So the fallback condition ("not monotone or not smoothly converging over the last 4 sizes") is not met and the main branch applies. HEURISTIC (judgement of "smooth"); the arithmetic is PROVED-HERE.

**Why the branch matters.** The fallback would give sigma_B = p(8) − p(10) = 5.7628e-8. That exceeds 5e-8 and would fail rule 9, so the branch decides the outcome. I conclude it is not triggered on a literal reading. NUMERICAL.

**Earlier sizes.** The non-monotone step from W = 2 to 3 lies outside the last four sizes.

**Claim arithmetic reproduced** with `code/tm/extrap.py` and `code/check/sigma_v2.py`. NUMERICAL.
- E1 = 0.445287065459697 (D = 5.4386)
- E2 = 0.445287072207185
- E3 = 0.445287058166765
- sigma_B = 7.293e-09, rule4-main
- drift_3 = 1.722e-08
- 2.87·sigma_B = 2.093e-08, so sigma_v2 = 2.093e-08

## 4. PREREG.v2

**It only widens the error bar for this claim.** The code sets `sv2 = max(sb, d3, FACTOR * sb)`, which is always at least sigma_B. The central value stays E1 and the thresholds are unchanged. PROVED-HERE (code read).

**Caveat on its wording.** In general v2 does more than widen: in the fallback case it sets the central value to the last p(W), while frozen rule 4 says p_c(B) = E1. That clause does not apply here (main branch). PROVED-HERE.

**The 2.87 factor** comes from a statistician report outside the package that I could not inspect. The result does not depend on it: rule-4 sigma alone (7.3e-9) and my own worst-case alternative spread (3.39e-8, section 5) are both ≤ 5e-8. NUMERICAL.

## 5. Does the error bar come from observed convergence? Robustness tests

**Source of the bar.** Rule-4 sigma comes from a window shift (E2) and a second accelerator (E3). v2 adds the drift of E1 across windows. None of this is the last difference: that is 1.885e-8, similar in size but not where the bar comes from. So the bank pitfall is respected. PROVED-HERE (from the formulas).

**Alternatives** (work/robust.py and work/robust_out.txt), each as the TSS estimate at W_max = 10 minus E1. NUMERICAL.

| Alternative | minus E1 |
|---|---|
| n^-4, 2 points | −1.16e-8 |
| n^-6, 2 points | +2.99e-9 |
| n^-4, n^-6, 3 points | −1.45e-9 |
| n^-6, n^-7, 3 points | +8.8e-10 |
| E3 (n^-4, -6, -8, 4 points) | −7.29e-9 |
| n^-4, -5, -6, 4 points | −1.30e-8 |
| n^-6, -7, -8, 4 points | −2.73e-9 |
| n^-3, -4, -5, 4 points | −3.37e-8 |
| R5 (n^-4 to -10) | −1.18e-8 |
| n^-4, -5, -6, -7, 5 points | −2.23e-8 |
| n^-4 to -12, 6 points | −1.36e-8 |
| E1 on even W (6, 8, 10) | +4.64e-9 |
| E1 on odd W (5, 7, 9) | +5.62e-9 |
| BST ω=2, W = 5 to 10 | −3.39e-8 |
| BST ω=3, W = 5 to 10 | −1.57e-8 |
| BST ω=4, W = 5 to 10 | −8.80e-9 |
| BST ω=4, W = 7 to 10 | −5.55e-9 |
| BST ω=6, W = 7 to 10 | +3.93e-9 |
| Wynn, 4 points | +6.55e-9 |
| Wynn, 5 or 6 points | −6.10e-9 |

**Second orientation** (data/eigT/, circumference 3m, m = 1, 2, 3). E1 = 0.445287051218456 (D = 3.940), which is −1.42e-8 from E1. The n^-4 two-point fit gives −1.28e-8 and the n^-4, n^-6 three-point fit gives −1.32e-8. NUMERICAL.

**Largest deviation.** Over all 23 alternatives the largest |alternative − E1| is 3.39e-8. No reasonable alternative moves the value by more than 5e-8. NUMERICAL.

**Systematic lean.** Scullard and Jacobsen 2020 (Table III, opened) give exponents Δ = 4.00(2), 6.00(5) and 8.1(2) for the frieze lattice, which is TS. KNOWN. Estimators built on that class, and the second orientation, sit 0.7 to 1.6e-8 below E1.
- E1 has not converged: as W_max goes 8 → 9 → 10 its drifts are −2.92e-9 and then −6.75e-9. NUMERICAL.
- An Aitken extrapolation of the estimator drifts gives n^-4 two-point 0.445287057930, E3 0.445287050084, R5 0.445287051353 and the six-point fit 0.445287051356. These are −7.5e-9 to −1.54e-8 from E1. NUMERICAL.
- So E1 is probably about 1e-8 high. That is within 1 sigma_v2, but the rule-4 sigma alone would have under-covered by about 2x, so the v2 widening was needed. HEURISTIC.

**Calibration of the same pipeline on lattices with known values.** E1 error divided by rule-4 sigma_B. NUMERICAL.
- TS (elongated triangular) bond, W_max 7, 8, 9, 10: −0.17, −0.22, −0.06, +0.69. At W_max = 10 the error is +3.882e-9.
- Kagome bond, n_max 5 to 9 (data from Scullard and Jacobsen 2020 Table II): 0.01 to 0.09.
- Square site, n_max 8 to 14 (Jacobsen 2015 Table 2; reference 0.59274605079210): −1.44, −0.56, −0.78, −0.93, −0.95, −0.96, −0.97.
- sigma_v2 covers the true error in every one of these cases.

**Limits of the TS control.** TS converges with D_eff rising (2.16 to 4.53), whereas TSS has D_eff falling (6.32 to 5.44). TS's accuracy therefore does not transfer automatically; the alternative-fit and orientation checks above fill that gap. HEURISTIC.

## 6. "To at least 7 digits"

- Frozen rule 9 requires stated sigma ≤ 5e-8. The stated sigma is 2.093e-8 (v2) or 7.293e-9 (rule 4); both pass. NUMERICAL.
- Every one of the 23 alternative estimates truncates to 0.4452870. NUMERICAL.
- The rounded 7th digit is not secure: E1 rounds to 0.4452871, but estimates below 0.44528705 round to 0.4452870. The claim's line "To 7 digits: this value 0.4452871" is therefore borderline in its last rounded digit. The precision, in the sense of sigma ≤ 5e-8, is met. HEURISTIC.

## 7. Confirmation or discrepancy, and the claim's sentence

**Numbers.** delta = +9.5546e-07. delta / sigma_table = 2.389, delta / combined sigma = 2.385 (combined 4.0055e-07), and delta / sigma_v2 = 45.7. NUMERICAL (from my script). `q9_check.py claim` prints "VERDICT: MEETS NUMERIC RULES". NUMERICAL.

**Which p2 branch.**
- Literally, the result shows "a discrepancy larger than its stated error bar": 9.6e-7 against 4.0e-7.
- Under frozen rule 9 it is "confirms", since it is within 3 combined sigma.
- p2 is met under either branch. PROVED-HERE.

**Reading the discrepancy.** 2.4 table-sigma is not decisive evidence that the table is wrong. Scullard and Jacobsen 2020 Table I shows that older Monte Carlo bond values for Archimedean lattices sometimes had optimistic error bars; for example frieze 0.41964191(43) against 0.41964035886369(2). KNOWN.

**Neighbouring rows** computed by the same code (package data/eig/bond.tsv, rule 4) against the table. HEURISTIC: there is no systematic offset between code and table, so the #22 offset is specific to that row.
- #21 TTS: −1.69e-7 (0.33 combined sigma)
- #23 TSSS: fallback branch, −4.83e-7 (1.04 combined sigma)
- #20 TTTS: +5.6e-8 (sigma 1.9e-5)

**The claim's one sentence** asserts only "an independent determination to 7 digits" of the cell. It does not claim a record (consistent with bank pitfall 4) and does not claim a refutation. The body states both readings correctly. It is no wider than the evidence. PROVED-HERE (text read).

## 8. Bundling, subsumption, stretching, null models

- **One cell.** The calibrations are reproductions, not claims. The second orientation is labelled diagnostic. Nothing is bundled from the run's site claim on another row. PROVED-HERE (text read).
- **Subsumption.** Scullard and Jacobsen 2020 cover only Archimedean lattices. KNOWN. My three web searches found no published bond value for this lattice; that is not exhaustive, and novelty belongs to the NOVELTY skeptic. HEURISTIC.
- **Null models.** This is a numerical estimate, not a search, so the PREREG's null-test exemption is reasonable. The controls do their job as positive controls. HEURISTIC.
  - Exact lattices at every W test code correctness.
  - Kagome roots matching Table II to 2.5e-15 test correctness on a non-solvable lattice.
  - TS bond through the full pipeline at the same widths and in the same Δ class tests the extrapolation, with the limitation noted in section 5.
- **Rule 9 calibration wording.** Rule 9 asks for reproduction "to <= 5e-8"; TS gives |delta| = 3.88e-9, so this is met. If one also required the calibration's own sigma ≤ 5e-8 (as rule 7 does for the full win), rule-4 sigma 5.66e-9 passes but v2 sigma 1.770e-7 fails. The rule 9 text contains no such requirement. NUMERICAL.
- **Family behaviour.** The related TSSS sequence (same code) turns around near W = 7, so this family can show late crossovers. TSS shows no such sign: D_eff is falling, which fits a same-sign W^-4 term, and the second orientation agrees within 1.4e-8. HEURISTIC.

## 9. Decision

The claim meets p2 literally:
- an independent determination of the bond threshold of the correct lattice, in a "citation needed" cell of the same table;
- stated sigma 2.09e-8, which is ≤ 5e-8 under the main branch of rule 4, robust to every alternative I tried (largest move 3.39e-8);
- the outcome falls in an allowed p2 branch: a discrepancy larger than the table's stated error bar, and "confirms" under frozen rule 9;
- nothing bundled, no subsumption found.

Caveats: E1 probably sits about 1e-8 high, still within its bar. The fallback branch, if it applied, would fail rule 9, but it is not triggered.

confirmed_scope: For the bond threshold of row #22 of the 2-uniform table in Wikipedia's "Percolation threshold" article (lattice (2/3)(3^3,4^2) + (1/3)(4^4), built as the row tiling TSS), the claim's extrapolation of eigenvalue-form critical-polynomial roots on W x infinity cylinders (W = 2..10, reproduced here for W = 5..10) gives an independent estimate p_c = 0.445287065(21) whose one-sigma bar is a convergence-and-calibration estimate rather than a rigorous bound (23 alternative extrapolations all lie within 3.4e-8 of it), and this lies 9.6e-7 above the table's "citation needed" value 0.44528611(40), a discrepancy 2.4 times that value's stated error bar but within 3 combined sigma.

pass: true
