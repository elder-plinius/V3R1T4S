# PREREG_B2: post-hoc variant of Method B (written before any odd-width high-precision value or any all-width Wynn run)

Written after the prereg Method B (PREREG.md, even widths only, steps of 2) was run on widths 4..26 and its Wynn estimates up to
mmax = 24 were seen: they agree with each other only to about 12 decimals (window 18..24) because the sequence converges by a factor
of only ~14 per +2 in width.  Disclosure of what I looked at before writing this file (so B2 is NOT blind):
 - the prereg-B Wynn table for mmax = 12..24 and its four-term window agreements (7, 9, 10, 12 decimals);
 - the corrections eps_m = ln beta(m) - m*h computed with the CTM value of h (as a diagnostic only), for even widths 4..26 and, from the
   low-precision (1e-18) exact Collatz-Wielandt logs, for odd widths 5..27: odd/even successive corrections have ratio about -0.27
   (alternating sign), so even and odd widths lie on one alternating geometric family; this is why B2 uses every width.
The B2 recipe below is therefore a post-hoc choice, motivated by that diagnostic.  Its outcome is reported whatever it is.

B2 recipe (Method B data only; no CTM value enters):
- Data: L_m = ln beta(m) at >= 45 digits for every width m = 4, 5, 6, ..., M (periodic rows), M = 29 if the 26 GB run completes, else 28.
- Sequence: e_m = L_m - L_{m-1}, m = 5, 6, ..., mmax.
- Extrapolation: Wynn epsilon algorithm at 70 digits on e_5..e_mmax; E2(mmax) = last entry of the highest even-index column.
- Ladder: mmax = 21, 22, ..., M.  Headline D_B2 = leading decimals common to E2 for the last four consecutive mmax (three increases).
- Nothing else is selected.  Variants (start width 6, 7; even-only) are reported as context.
