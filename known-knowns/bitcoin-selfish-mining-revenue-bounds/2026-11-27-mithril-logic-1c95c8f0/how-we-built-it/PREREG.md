# PREREG (frozen before any result of this run)
date -u at freeze: Fri Nov 27 01:50:49 UTC 2026 (ISO: 2026-11-27T01:50:49Z; format-only restatement added 2026-11-26 ~10:20 PM ET after a box restore reset all file mtimes in this run to 21:46 ET) (written before any solver code of this run existed or ran).
Criterion (verbatim, bank bitcoin-selfish-mining-revenue-bounds): copied in target.md.
Claim scope planned: alpha=9/20 only.
Statistic/checker: exact-rational dual certificate on the over-paying MDP with h=T compensation given by the CORRECTED (28) (E[a0|return]=h+alpha(h-a)/(1-2alpha)), and also (same h vector) on N_rho^T as printed; label-invariant bias h(a,h,f)=H(a,h); checker computes the exact max over every (state, allowed action) of r + sum P h - h in Fractions/integers; CERT_OK iff that max < 0 for the compensation variant checked.
Thresholds: success iff CERT_OK under the corrected variant at rational rho <= 0.70099 (bank bar). Report the lowest rho certified.
Calibration gate (own builder): under-paying root at T=95 must match SSZ 0.56808 (alpha .425) and 0.66891 (alpha .45) within one last digit; over-paying optimal gain at alpha .45, rho .66 must be positive.
Negative controls: (a) certificate built the same way at rho below the float root must give CERT_FAIL; (b) an exact policy-gain lower certificate in the corrected over-paying MDP at rho just below the root must show gain > 0 (so no certificate exists there at that T); (c) an exact under-paying policy lower certificate showing true max REV > some L (no rho <= L can ever be certified).
null_test: not needed because the claim is an explicit certificate checked by a deterministic exact checker, not a search or statistical score.
Baseline (3c): not an empirical benchmark; calibration above plays that role.
