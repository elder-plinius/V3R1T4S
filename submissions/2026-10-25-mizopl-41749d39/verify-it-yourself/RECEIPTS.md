# Verification Receipts — `2026-10-25-mizopl-41749d39` (`iedb-mhci-bd2009-blind-auc`)

## Command Executed
```sh
sh verify-it-yourself/run_checks.sh
```

## Real Output (`0.45 s` Single-Thread on 16 GB M1 MacBook Air)
```text
======================================================================
IEDB MHC-I BD2009-to-BLIND BENCHMARK VERIFICATION SUMMARY
======================================================================
Zero-Contamination Firewall : PASS (BD2009 SHA-256 verified, 0 post-2009 rows)
87-Dataset Blind Mean AUC   : Variant A (Pure Seq) = 0.889379 (+0.006057 vs NetMHC)
                              Variant B (Seq+IRT)  = 0.889556 (+0.006234 vs NetMHC, +0.006508 vs NetMHCpan)
Dataset Wins (/ 87)         : 57/87 vs NetMHC (p=0.005014 < 0.01), 47/87 vs NetMHCpan, 74/87 vs SMM-PMBEC
Partial Win p1 (cv20 <=326) : Variant A = 0.850714 (+0.020676 >= 0.02 vs NetMHC)
                              Variant B = 0.850861 (+0.020823 >= 0.02 vs NetMHC, +0.021548 vs NetMHCpan) -> PASS
Partial Win p2 (Gap Shrink) : cv_rnd = 0.907408, blind = 0.889556, gap = 0.017852
                              Shrinkage vs NetMHCpan = +0.016701 (table) / +0.013848 (paper) >= 0.01 -> PASS
Partial Win p3 (Leakage)    : 42,038 post-2009 rows audited; f=0% (0.888874) -> f=10% (0.902231) -> f=100% (0.980744, +0.091869) -> PASS
PASS
```
