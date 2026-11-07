context: subagent

# Criterion skeptic: route (ii), L = 501/1000 (re-judged after the interval run finished and after the edit of PROOF.md Step 1)

Logs read at 2026-10-31T22:50Z; PROOF.md Step 1 re-read at 2026-10-31T22:57Z (PROOF.md sha256 a1de390a...). This replaces my two earlier verdicts. I read only claim/. My own runs are in panel/scratch_criterion/. Nothing in claim/ was changed. No tool block, no HTTP request, no outward step.

## Bottom line

My condition is met, by my own count. Route (ii) passes on the evidence in claim/. One limit stays: I can only say that no explicit value of Biro's c appears in claim/; whether one exists elsewhere is for the novelty check, see clause 5. The sentence in PROOF.md Step 1 that I flagged as too wide has been rewritten and is now correct, see clause 3.

## The condition: coverage of logs/check2_*.log, counted by my own parser

| File | Rows | Row lines | Sum of row_fails | Largest fails, unresolved on any row line | Ending |
|---|---|---|---|---|---|
| logs/check2_full.log | 0-397 | 398 | 0 | 0, 0 | no `finished:` line; stopped by process id |
| logs/check2_full_398_400.log | 398-399 | 2 | 0 | 0, 0 | `finished:` 0, 0 |
| logs/check2_full_400_450.log | 400-449 | 50 | 0 | 0, 0 | `finished:` 0, 0 |
| logs/check2_full_450_500.log | 450-499 | 50 | 0 | 0, 0 | `finished:` 0, 0 |
| logs/check2_full_500_800.log | 500-799 | 300 | 0 | 0, 0 | `finished:` 0, 0 |
| logs/check2_full_800_1200.log | 800-1199 | 400 | 0 | 0, 0 | `finished:` 0, 0 |
| logs/check2_full_1200_1600.log | 1200-1599 | 400 | 0 | 0, 0 | `finished:` 0, 0 |

- Union: rows 0 to 1599, each exactly once, nothing missing, no overlap, nothing out of range, contiguous inside each file. Every row line has 2514 cells, so 4,022,400 cells. Zero witness failures, zero unresolved. No FAIL line in any of these logs or in logs/check2_full*.out. Smallest row_worst_lb is 1.00000049e-06, at or above the threshold 1e-6. (That bound is the stopping threshold, not the true minimum.)
- logs/check2_full.log has no `finished:` line and logs/check2_full.out no summary, so for rows 0-397 my count rests on the row lines alone. This is acceptable: code/check2.c writes a row line only after the whole row is done. logs/check2_chain.log shows the worker was stopped after row 397 was done; rows 398-399 ran separately.
- REPRODUCE.md section 3's table and totals agree with my count. The sha256 of code/check2.c matches the value it states (eaf6f33d...). The sha256 of V_b.npy matches the value it states (b1712e64...).
- The logs carry no table hash. To tie them to this table, I compiled claim/code/check2.c with the documented flags and reran 13 rows against claim/V_b.npy: 11, 397, 398, 399, 449, 450, 603, 799, 800, 925, 1199, 1232, 1599. All 13 match the log lines exactly, including box counts, and they touch all seven logs. I did not rerun all rows.

## Clause by clause

### 1. About C_42 as table/42a.html defines it: MET

Same definition: limsup R_n, with R_n the minimum over z_1..z_n with max|z_i| = 1 of max_{k<=n}|sum z_i^k|. The claim holds for every n, which is stronger than the limsup statement needs.

### 2. Lower bound with L strictly above the best explicit bound listed: MET on the snapshot

The page lists explicit 1/2 and an inexplicit ">1/2". 501/1000 > 1/2. Hashes of table/42a.html and table/pulls_open.json still match table/record.txt (fetched 2026-10-31T22:02:55Z and 22:02:56Z). No open pull request in that list gives a C_42 lower bound. I did not refetch, so this is the state at that fetch, not at any later moment.

### 3. Proof complete: MET (an agent's line-by-line read; nothing here is refereed)

My earlier rederivation of every step stands, and the rest of PROOF.md is unchanged in substance. The new text:

- Step 1, as edited (line 93), re-checked clause by clause. By file size, line 93 is the only line of PROOF.md that differs from the version I read before. Correct:
  - rho_l <= 1 from |M_l| <= A_l.
  - The map y -> y - h mu(y) is nondecreasing on (0,1] for h <= 1.
  - y_l in (rho_+, 1] for l <= J0. The step from y_{J0} > rho_+ to all earlier l needs the sequence to stay positive on the way. The text says "decreasing while positive", and I confirmed it with an exact-integer run of the (LATE) recurrence: every lower iterate is positive and strictly decreasing up to J0, and the last exceeds rho_+ by exact squaring.
  - The induction is now limited to l <= min(n, J0). Base rho_1 = y_1 = 1. In the step, rho_l >= y_l > rho_+ gives r_l != 0; l < n gives |rho_l - w_l| <= T, so e >= 0; (F1) then gives the first inequality, and monotonicity on (0,1] with h_l <= 1 gives the second.
  - n > J0 follows from (1.2): n <= J0 would give rho_n > rho_+ > T.
  - B exists with B <= n, and B > A >= J0, because rho_l > rho_+ for l <= J0.
  - No other line relies on the old wider range: y_l appears only in (LATE) and in this step.
- One point the text leaves to the reader, not a gap: "Monotonicity gives rho_{l0} >= rho_+ - mu(rho_+)/A > rho_-" applies (F1) and e >= 0 at l = A, and A may exceed J0, so the induction sentence does not cover it literally. (F1) is stated for every l with r_l != 0; here rho_A > rho_+ > 0 and A < B <= n, so it applies. The strict inequality uses 2b' > 0 from (GAP) (mu(rho_+)/J0 is about 7.2e-10 against 2b = 0.007).
- Step 3, "if K is empty, S_K = 0 and the next inequality is trivial": correct, since the right side is nonnegative. S_K >= S - 8 - 1/l0 still holds in that case.
- Section 7, values: each agrees with logs/late_gap.txt and logs/check2_full.out (L_tau, L_phi, C0, eps1, m, eta', mu_max, both (GAP) margins, 0.00984336). "Since eta' > 0" supplies the sign used to pass from Step 3 to (X).

### 4. All numerical steps interval-certified: MET, with one stated assumption

- (HJB): code/check2.c, outward-rounded interval branch and bound on the 4-dimensional box, all cells (count above). It uses no corner or chord reduction from CERT.md; only Lemma R, a written proof step, takes circle to disc. I read Gfun and the mean value bound against HYPOTHESES.md and found no soundness bug.
- (INIT), (TERM), Lipschitz bounds: Arb in code/late_gap.py and intervals in code/check2.c (logs/late_gap.txt, logs/check2_full.out). They agree. m >= 0.0146231 in Arb and m_cert >= 0.0146262 in check2, against the needed 0.00984336. All 7 logs/check2_full*.out files report identical values. I reran code/late_gap.py: identical to the log apart from timings.
- (LATE), (GAP), J0 >= 2 Zb + 2: Arb, and exact integers for (LATE).
- code/check_hjb.py: floats with a padding argument, as CERT.md says. It is a full-coverage cross-check, and I do not count it as interval certification.

The assumption, now stated in CERT.md Rounding: Apple libm within 4 ulps, round to nearest, no flush to zero. These are not proved. CERT.md's account matches the code. My judgement is that they do not undo the clause:

- The proof needs G >= 0 and the program certifies G >= 1e-6, so a libm error would have to be about nine orders of magnitude larger than assumed to matter.
- I sampled 500,000 points against Arb on the ranges used: worst error 0.84 ulp for sin and cos, 0.51 ulp for exp. That is evidence, not proof.
- The selftest's long double comparison adds little on this Mac, where long double equals double.

Discrimination, saved and mine: logs/check2_test_perturbed.out fails on the touched cells; logs/check2_test_depthlimit.out reports unresolved; the threshold bracket around cell (800,1947) behaves correctly (passes at 0.000519, witness failure at 0.00054). My runs: a node change of 1e-5 fails; certified minima lie within 2.1e-10 of sampled minima and never above them.

Remaining note, not blocking: "written without access to check_hjb.py" in CERT.md cannot be checked from claim/, and route (ii) does not require two independent checkers.

### 5. Biro's constant clause, literally: NOT TRIGGERED on the evidence in claim/; L NOT compared with c

The clause requires L above c "once that value has been published or established under p1". The page says the value is not computed, and neither claim/ nor table/pulls_open.json gives one. So there is no number to compare with, and the clause adds no requirement on what I can see.

Two limits on this, stated plainly:

- This does not show 501/1000 > c. Biro's theorem gives some c > 1/2, and c could be above 0.501.
- I cannot see the literature beyond the snapshot, or any p1 result elsewhere in the run. If such a value exists at or above 501/1000, this clause fails. That check belongs to the novelty side or the main session.

### 6. Merely an evaluation of Biro's constant: NO

The proof is self-contained and re-proves what it credits to Biro. T is a chosen value, verified through a value-function table with fixed beta and gamma; no formula for c is evaluated. PROOF.md's statement that it avoids his Lemma 8 and (38)-(47) is unchecked against the paper, which is not in claim/, but the logic does not depend on it.

## Null models

- The certificate is not vacuous: a 1e-5 change at one node breaks it.
- The result does not prove too much: 0.501 is far below the listed upper bounds, and T enters through mu > 0, which vanishes at T = 1/2 at rho = 1/sqrt2.
- It is not a restatement of 1/2: at T = 1/2 mu vanishes at rho = 1/sqrt2 and there is no crossing cost to compare; here (GAP) needs a certified positive margin m.

## Non-blocking items

- code/negctl.py and logs/negative_controls.txt now agree: four lines, and REPRODUCE.md section 4 says the row control was removed. code/negctl.py changed after that output was produced; only the unfinished control was removed.

confirmed_scope: For every positive integer n and all complex z_1,...,z_n with max|z_i| = 1, max_{1<=k<=n}|z_1^k+...+z_n^k| > 501/1000, so Turan's pure power sum constant C_42, as defined at https://teorth.github.io/optimizationproblems/constants/42a.html, satisfies C_42 >= 501/1000, strictly above the explicit lower bound 1/2 listed there when fetched at 2026-10-31T22:02:55Z; this rests on an unrefereed written proof whose finite hypotheses on a binary64 table were machine-checked (Arb for LATE, GAP, TERM and INIT, and outward-rounded binary64 intervals on all 4,022,400 table cells for HJB, taking Apple libm as accurate to 4 ulps, which is assumed and not proved), and 501/1000 has not been compared with Biro's constant c from Indag. Math. 11 (2000) 343-358, whose explicit value appears neither on that page nor in the open pull requests fetched at 2026-10-31T22:02:56Z.
pass: true
