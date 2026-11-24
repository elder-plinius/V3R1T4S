# PREREG (frozen Mon Nov 23 16:26:36 UTC 2026)
target: brun-constant-unconditional-upper-bound, partial win p1 (criterion verbatim in target.md).
Hypothesis basis: GRH as used by Dunn (RH + GRH for Dirichlet L-functions via zeta of Q(zeta_q); see scout.md). Any
result is stated "under GRH" and does not depend on the Lean proof being accepted.
Statistic: U' = the upper endpoint (sup) of a fully interval-evaluated (python-flint arb, outward rounding) bound on B
assembled exactly as in Dunn's Lemma 3.1 plus any changes listed under the lens that produced it.
Threshold: p1 claim only if U' <= 2.15939 (strictly below Dunn's 2.1594 with a margin of 1e-5 against rounding of his
quoted value), with every input cited by exact published statement.
Plan (lenses, in order):
 L1 reproduce (calibration, required first): independent Python reimplementation of Dunn's compute_B.jl formulas with
   his midpoints and an independent z-optimiser. Smoke test today: double/mpmath floats, non-rigorous, target |total -
   2.1594| <= 5e-4 (tolerance fixed now). Next session: the same in arb, must give sup <= 2.1594 + 1e-6 and >= 2.1593
   (i.e. it reproduces Dunn's 4-digit figure) before any improvement is scored. If it misses, the comparison is unresolved
   and the miss is the finding.
 L2 contrarian audit (today, short): check each numeric input in compute_B.jl against its stated source (pi_2 and li2
   constants, Dusart coefficients, c_3 = 12.6244, Schoenfeld, 1.840518, pi_2(4e18) = 3023463123235320) and recompute
   Dunn's V_list (V(z) at z = k*1e4) independently on a sample of z; any mismatch is reported.
 L3 improver (NOT started today; needs Matthew's go for the compute): (a) Selberg-weight error sum (sum |lambda_d|)^2
   replacing r(z)^2, with weights computed exactly for z <= 1e8 and an explicit bound beyond; (b) q-dependent GRH error;
   (c) finer intervals. A result from (c) alone (re-optimising Dunn's own parameters) is labelled "polish" in the report and
   claimed at most as PROMISING, since the NOVELTY skeptic may reject it as a local numerical polish.
Calibration / null: null_test: not needed because the result is a deterministic interval-arithmetic bound checked by
rerunning, not a search score or chance-level claim; calibration is the L1 reproduction of 2.1594, plus two precisions
(arb at 128 and 256 bits) agreeing to the reported digits.
Precision: arb 128-bit and 256-bit runs; reported U' = max of the two sups, rounded UP at the 6th decimal.
CPU budget (estimate, HEURISTIC): L1 arb replay ~0.5-1 CPU-h; exact V(z) to 1e8 in C ~1 min, independent V to 1e10
segmented ~1-2 CPU-h (8 cores ~15 min); L3 sweeps 2-6 CPU-h. All on the box; no cloud. Long jobs: nice, timeout, checkpoint.
Panel: three fresh contexts (via the parent session) before any CONFIRMED status; none can be started from this session.
