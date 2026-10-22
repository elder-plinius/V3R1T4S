# PREREG_B: pre-registered recipe for method B (open-strip transfer matrices + Wynn epsilon)

Written 2026-10-18, BEFORE any run of the new memory-lean program and before any open-strip width above 28 exists.
Disclosure: widths 2..28 and the earlier m0=3 / m0=4 results were already seen (REPORT.md section 5: m0=4 blind gave 21 stable
decimals for mmax=25..28, m0=3 gave 22).  The recipe below is the m0=3 one, chosen because it was the better of the two; so the
choice itself is not blind, but widths 29..34 are new data on which the recipe is tested unchanged.  One recipe, reported
whatever it gives.

1. Data: lambda_m = dominant eigenvalue of the exact column transfer matrix of the OPEN king-graph strip (m rows, free
   boundary), m = 2..M, M = the largest width completed (target 34).  Widths 2..28 from the existing lam_open.txt (tm.c);
   widths 29..M from the new program (tmlean.c).  The new program must first reproduce lam_open.txt for m <= 28 to 40+ digits
   and A063443 n <= 12 exactly; if not, its data are discarded.
2. Sequence: r_m = lambda_m / lambda_{m-1}, for m = 3, 4, ..., mmax (start width m0 = 3), computed at 60 digits.
3. Extrapolation: Wynn epsilon algorithm on r_3..r_mmax.  Estimate E(mmax) = the LAST entry of the highest even-index column
   eps_{2k} of the epsilon table (k maximal for the number of terms).  No other column, no averaging, no selection.
4. Truncation parameter = mmax.  The estimates E(mmax) are reported for every mmax from 22 to M.
5. Stability rule: for the window of four successive truncation values mmax = M-3, M-2, M-1, M, D_B = the number of leading
   decimals (after "1.") common to all four E values.  Windows ending at M-1, M-2, ... are also reported for context, but the
   headline is the window ending at M.
6. Agreement with other methods is reported afterwards as leading common decimals; those numbers never feed back into B.
7. Iterations: power iteration count per width fixed at 100 (plus the check that 100 vs 160 differ < 1e-50 for two widths);
   eigenvalue from lambda^2 ~ |Tv|^2/|v|^2 (second-order accurate).
