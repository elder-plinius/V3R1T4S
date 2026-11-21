Sat Nov 21 10:05:02 UTC 2026

# PREREG v5 — dreval-lco-ctrpv2-normalized-r2

Timestamp: 2026-11-21T10:05Z (line above), BEFORE the ensemble-v2 run's first result.
All win thresholds UNCHANGED from PREREG.v4.

## Change (attacker design, not thresholds)

The ensemble run att_v1ens (complete, 10 splits) scored mean normR2 0.2009 (SE 0.0140),
Pearson 0.4535, Spearman 0.4387 under the v1.3.1 ruler: beats the same-splits RF (0.1857) by
+0.0152 but MISSES the frozen R2 win bar (needs >= 0.2116 = 0.1857 + max(0.02, 2xSE)); p2's
Spearman margin is +0.0004 (a statistical tie -- not claimable per LESSONS 9).

Diagnosis: the package's default hpam_optimization_metric (RMSE on raw validation responses)
selects hyperparameter combos that do not align with the normalized metric (the tuner picked
the same combo on all 10 splits). One more improvement round is run BEFORE any claim:

- att_v1ens_v2: same model class, same splits, same data; hpam grid extended with a member
  weight w in {0.4, 0.5, 0.6} (alpha_b in {100,300,1000}, n_factors_b in {0,5});
  hpam_optimization_metric = "Pearson" on the VALIDATION partition only (a package-supported
  metric; selection never touches test folds -- the criterion's own hyperparameter rule).
- Decision rule (unchanged thresholds): if att_v1ens_v2's 10-split mean normR2 >= 0.2116
  (= 0.1857 + max(0.02, 2xSE of the 10 splits)) AND Pearson >= 0.4247 (and >= live leaderboard
  max), the R2-win claim proceeds to self-break + panel. If Spearman also >= 0.4383 and R2 >=
  0.175180, p2 is additionally claimed. Otherwise: NO win claim; the honest result is the
  same-splits RF-beating Pearson (+0.019-0.021) and the reproducibility findings, reported as
  such (reproduction-scale result).

null_test: not needed because (unchanged) explicit benchmark score vs live table value.
