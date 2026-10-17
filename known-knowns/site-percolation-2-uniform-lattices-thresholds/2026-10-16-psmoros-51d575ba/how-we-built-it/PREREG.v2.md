# PREREG.v2 (written 2026-10-16T06:50:19Z, AFTER results existed; PREREG.md, frozen 03:03:58Z, is unchanged)

Why a v2: the kit step-5 lenses (attempts/contrarian here; runs/2026-10-16-0607/attempts/contrarian and
.../statistician) showed that the PREREG rule-4 sigma of the transfer-matrix (method B) extrapolation under-covers the
true error at these widths: on the square-site calibration the |E1-E2| part under-covers by up to 2.87x, and on #23 site
E1 moved by 3.26e-7 between W_max = 11 and 14, 4.7x the sigma quoted at W_max = 11.

What changes (only the method-B error bar, only upwards):
- sigma_B,v2 = max( sigma_B (PREREG rule 4), drift_3, 2.87 * sigma_B ), where drift_3 = max over k = 1, 2, 3 of
  |E1(W_max) - E1(W_max - k)| (E1 computed on each trailing three-size window) and 2.87 is the worst ratio of true error
  to rule-4 sigma measured on square site (Jacobsen 2015 Table 2, n_max up to 21), kagome bond and elongated triangular
  bond at comparable widths (runs/2026-10-16-0607/attempts/statistician/report.md). Script: checker/sigma_v2.py.
- The method-B central value stays E1 (PREREG rule 4). When rule 4 falls back (non-monotone sequence), the value is the
  last p(W) and the sigma is the rule-4 fallback spread, as before.
- Rule 5 then uses sigma_B,v2 in place of sigma_B. Every other rule (1-10, calibration gate, thresholds 2e-6, 3 sigma,
  1e-6, 5e-8) is unchanged. Method A (Monte Carlo, rule 3) is unchanged.

Effect (from checker/sigma_v2.py at 06:49Z): #23 site sigma_B 7.245e-8 -> 3.255e-7; #22 bond 7.293e-9 -> 2.093e-8.
Both remain inside their bars (2e-6 site, 5e-8 for p2). No result passes under v2 that failed under v1; v2 can only make
a pass harder.

In runs/2026-10-16-0607 this v2 applies to the p2 claim on row #22 bond; the line below concerns runs/2026-10-16-0245.
Committed before the final Monte Carlo analysis (production runs end 08:25Z): the full-win claim of this run folder is
row #23 (TSSS) site, whatever the final rule-3 numbers for #21, #22 or #23 turn out to be.
