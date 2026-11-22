# PREREG_B3: blind second method (open-boundary strips), written BEFORE any open-strip high-precision value

Family: OPEN rows (free boundary, rows are paths of m sites, free along the length).  Not looked at before: I have run only
the dense small-m validation (m <= 9) and the n x n board counts for this family; no open-strip eigenvalue beyond that.
Disclosure: the periodic family (B, B2) and the method-A value were seen.  The recipe below copies the structure of B2 (one-step differences + Wynn)
because the periodic data suggested it; the open family may behave differently (surface term, different corrections), and I do not know how.

- Data: L_m = ln alpha(m), alpha(m) = largest eigenvalue of the exact open-row transfer matrix A_m, m = 3, 4, ..., M, >= 45 digits
  (same exact u128 fixed-point power iteration as hp mode, 25 iterations after 6 exact refinements).  M = 29 if it completes in <= 26 GB, else 28.
- Sequence: r_m = L_m - L_{m-1}, m = 5, 6, ..., mmax (start width m0 = 4).
- Extrapolation: Wynn epsilon algorithm at 70 digits on r_5..r_mmax; E3(mmax) = last entry of the highest even-index column.  Nothing else selected.
- Ladder: mmax = 21, 22, ..., M.  Headline D_B3 = number of leading decimals common to E3 for the last four consecutive mmax.
- Afterwards (not feeding back): decimals shared with method A (chi = 48) and with the rigorous enclosure check.
- Outcome reported as it falls; if D_B3 < 20, no blind second method reaches 20 decimals.
