# report.md — lens interval-mishra

claim level: partial_win_claim

## Outcome (all numbers from command output; logs in result/logs/)
Mishra's cert_B_08344 (sha256 of the uncompressed file 33973342ab754dd5261b682d657e0b46b55f3377173a9238a2fa3948fefdb91f) was replayed on ALL leaves by `LebVerifyI`, whose leaf path is literally outward-rounded interval arithmetic (struct `Iv{lo,hi}`, every + - * / sqrt result widened by one ulp each way; constants from mpmath.iv at 70 digits rounded outward; sin/cos by interval Horner + explicit Lagrange remainder; points are exact doubles, membership = Iv upper bound of squared distance <= lower bound of rUse^2, order certificate = Iv cross product lo > 0, area = lower end of the Iv shoelace sum, acceptance lo >= upper bound of tau+1e-12 with tau = 8344/10000 enclosed). Undecided = fail. No floating-point error theorem is used.

Full-run log (result/logs/full_run.log, 5 threads, BelowNormal, PID 3720, started 2026-10-31T23:02:12Z, wall 149.14 min):
`RESULT VERIFIED  (interval mode)  a >= 0.8344 nodes 486,799,600 leaves 245,496,952 failing 0`
 - forest identity 2L - nseed = 486,799,600 OK; desync 0; a-priori leaves 1,208,576; hull leaves 244,288,376, ALL accepted at the first witness tier (N=256 + adaptive edge refinement); tiers N=1024/4096 never needed.
 - interval child-covers-parent check at every split (seed splits, pre-walk, DFS): 0 failures; all 524,288 top-end rho seeds Iv-certified to reach the enclosure of 2pi/5, bottom-end seeds to reach 0.
 - worst interval slack (lb.lo - TauThr, TauThr = 0.8344000000010002): 3.426674e-06 (tier-0 polygon, seed box in log). After re-evaluating the 11,009,232 leaves with slack < 2e-5 at the finest tier N=4096: 1.577153e-05.
 - `summarize` over the checkpoint (3,596 jobs) reproduces the verdict (result/logs/full_summarize.txt).
Previous rigorous-double run: worst slack 3.426651e-06 (same worst box up to sign symmetry). Agreement on a 10 % job sample (seed 5), 1,194,240 identical leaves logged by both programs: interval LB minus double LB min +2.002e-13, median +2.222e-13, max +4.441e-13 (never negative; the double run subtracts a 1e-13-scale running error allowance); both >= threshold on all of them; min slack identical to 7.439540e-06 (result/logs/cmp_new_vs_old.txt).
Unit tests of Iv: outputs/ivtest_check.txt: 20,000 random operands x (add, sub, mul, div, sqr, sqrt, sin10, cos10, sin7) + 13 constants checked against exact Fractions / mpmath.iv: 0 containment violations; Up/Dn bit-identical to Math.BitIncrement/BitDecrement on 2e6 doubles.
Controls (result/logs/controls_summary.txt): author's valid certB_test and accept_m_K_2048/4096 VERIFIED; bad_magic, trailing_byte, truncated_file, inflate 0/-1e-3, tmax 0.60/0.65 REJECTED at header; flip_first_bit, flip_mid_bit, truncated_block, tau 0.8301, tau 0.8348 VERIFICATION FAILED. 12/12 tampers rejected, 3/3 positives accepted.
Sensitivity on the real cert (job 3431 holding the worst leaf, header tau patched; result/logs/sensitivity_main_cert.txt): tau 0.83441 passes, tau 0.83442 fails on 194 leaves (verdict flips where the slack figures say it should).
Speed: 1% slice (43 jobs, 2,897,141 leaves) 3.07 min on 6 threads; optimisations that kept every check: winner-only certification of heuristic candidates, comparison-based Hull4 instead of Math.Min/Max, informational N=4096 re-evaluation limited to slack < 2e-5. Full run ~27.4k leaves/s.

## Scope (do not overclaim)
This is a replay of a published certificate: "this certificate verifies", not a new bound. Conditional on (i) the paper's analytic lemmas (Lemma 2.3, gauge/mirror, Lemma 4.4 f(d) monotone, Lemma 4.7/4.8 erosion and corner movement, Prop 4.9, Reuleaux n-gon = intersection of unit discs about its corners) which this program does not prove (lemma-proofs lens), and (ii) the trust base in result/INTERVAL_AUDIT.md (IEEE correct rounding of + - * / sqrt on the executing CPU, JIT executes the source as written, integer bit decoding exact). Self-observed limits: the Iv Up/Dn trick relies on (i) only; the unit test is statistical, not a proof; the heuristic selectors are re-certified but are also reasons a leaf could fail (none did).
The `--claim 8344/10000` header check shows the header double 0.8344 lies inside the enclosure of the decimal; the acceptance threshold uses the upper end, so area > 0.8344 + 1e-12 (conditional as above).

## Files
 - result/LebVerifyI/ (sources used), result/tools/ (generator, unit-test checker, comparison, tamper maker, control runner, patched reference program), result/logs/, result/SHA256SUMS.txt, result/INTERVAL_AUDIT.md (operation-by-operation audit), REPRODUCE.md (also copied to result/).
 - work/ (not packaged: certificate copy, checkpoints, leaf logs) — checkpoint work/full_ckpt.tsv is copied to result/logs/.

## Dead/negative lines tried inside this lens (for the record)
dead lines:
 - A first witness tier without edge refinement (256:1e9) is useless: only 335/3090 sampled leaves pass it and it doubles the cost.
 - Replacing Math.BitIncrement by a bit-twiddled Up/Dn did not speed the verifier measurably (kept, unit-tested); the real hotspots were Math.Min/Max inside Iv.mul and the N=4096 informational recheck (11% of leaves at 16x cost) — fixed, not a verdict-relevant change.
 - Using the previous run's inflate-based coverage argument (half*(inflate - 2.3e-16) >= 1.5e-16) is no longer needed: coverage is certified per split by Iv differences instead; a failing split would be reported as a COVER-FAIL (none).
 - Tampering only the header tau (0.8344034/0.8344035) does NOT fail by itself on the real cert because higher tiers add up to 1.6e-5; the verdict flips only between tau 0.83441 and 0.83442 (job 3431).
