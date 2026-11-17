# PREREG (frozen before any order-23 search result exists)
Criterion: every tree on 23 vertices has a labeling passing checker/check_odd_graceful.py (labels distinct in [0,2n-3], edge differences exactly {1,3,..,2n-3}).
Coverage: checker/verify_count_distinct.py on the certificate: all lines trees on 23 vertices, AHU canonical codes pairwise distinct, count = A000055(23) = 14828074.
null_test: not needed because explicit labelings are judged by a deterministic checker (explicit labelings judged by a deterministic checker; same as PREREG.v4 of run 2026-11-02-1526).
Thresholds: PASS with 0 unlabeled. Any claim at most PROMISING (single-context, unpanelled). Not a bank win (bank stops at 22); a bonus extension.
Calibration: checker/test_checker.py must pass before trust.
