# How the objects were built (exact commands; Python 3.9+, standard library only, single thread)

All code here is the run's own code, copied as it ran (two path constants in the contrarian copies were replaced by "."
for publication, marked in the files).

1. Exact solver (extender lens), points-needed coordinates, component-wise exact policy iteration (safeguarded Newton on
   the two-cycle of each component, exact 2x2 solves, exact bisection fallback that was never needed). One run computes
   every n <= N and writes one certificate per n:

       python3 -I code/solver_extender.py 30 CERTDIR 1 30 CERTDIR/values.txt --b-dir PUBLISHED_TERMS_DIR

   (1.29 s for the exact solve at N = 30, 0.65 s to write the 30 certificates.) object/n16.json ... n30.json and
   verify-it-yourself/calibration/n1.json ... n15.json are those files (n27..n30 gzipped for the size limit).
   Rerunning the command reproduces every certificate byte for byte.

2. Independent solver (contrarian lens), a different algorithm: exact minimax over pure turn-plans, closed-form fixed
   point per component, no policy iteration:

       python3 -I code/solver_contrarian_needs_minimax.py        # writes the needs table and values for N = 30 (5 s)

   Its 30 values are identical to the extender's (how-we-built-it/code/cross_compare.py was used for the comparison).

3. Checks run during the build (all saved in the run folder; summarised in HOW_WE_FOUND_IT.md):
   - code/ros_cert_check.py (the run's checker, written from the definition before any solver ran) on all 60 certificates
     of both lenses: ALL_PASS, oeis_match=yes for n = 1..15;
   - code/consistency.py: P_n(a,b,c) = P_m(a, b+m-n, c+m-n) across all 435 pairs n < m <= 30 (640,088 comparisons, 0 mismatches);
   - code/float_vi.py: double-precision Gauss-Seidel value iteration agrees with the exact values to 1.1e-15;
   - code/audit_table1_contrarian.py: toss counts derived from the exact actions equal all 400 published terms of A394776
     and the 361 cells of the paper's Table 1; code/variants_contrarian.py: only the bank's rule reading (and its
     provably equivalent variants) reproduces the published terms;
   - code/ros_compact_check.py: checker for the compact (points-needed) certificate format used for the extension beyond n = 30.

PREREG.md (frozen 2026-10-15 03:25:44 UTC, before any solver output was scored) and PREREG.v2.md (09:11:24 UTC, for the
extension beyond n = 30) are copied here unchanged.
