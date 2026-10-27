# PREREG v2 (run 2026-10-26-1727): written 2026-10-26T17:34:23Z (date -u). No null, control or early-hours value has been computed yet.

## Why a v2
PREREG.md L1.3's known-negative test failed for the float64 code as specified there: at YER, template nn00888600,
data index j = 1667405 (2024-12-09T23:09:30.25, unaligned; REPRODUCE's "23:09:29" point) the float32 code gives 0.7050,
the float64 code 0.1939, the direct Pearson CC 0.1886 (attempts/detector-f64/checker_out.txt, scan_chunk_out.txt).
Cause: the normalisation uses whole-day running sums (cumsum of x and x^2); after the mainshock, YER's c2 is 6.5e13
against a window sum of 1.65e-2, so s2 - s1^2/L cancels catastrophically (den 0.1244 against an exact 0.1279). Per
L1.3 the v1 float64 code is not used.

## Change (everything else in PREREG.md stands)
L1.1 becomes: float64 numerator as in v1, AND the per-window normalisation sqrt(sum (x - mean)^2) over each 120-sample
window computed directly in float64 (blocked sliding windows), replacing the running-sum formula. The gap rule and the
1e-3 x median(den) floor are unchanged. L1.3's tests are rerun unchanged, plus the known-negative point at j = 1667405,
and must all pass (|f64 - direct| <= 1e-5) before the null runs. L2 uses the same exact normalisation (its circular
windows: direct per-window sums over the circularly padded series).
