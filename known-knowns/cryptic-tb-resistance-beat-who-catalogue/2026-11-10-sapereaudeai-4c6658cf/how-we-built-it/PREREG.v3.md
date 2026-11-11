# PREREG.v3 (secondary p2 drugs: reduced control count; written before any secondary drug is run)

written_at: Tue Nov 10 11:53:07 UTC 2026 (date -u). PREREG.md and PREREG.v2.md are unchanged.

Seen before this file: the primary p2 result for ETH (attempts/leakage-knn/p2_knn_ETH_output.txt). The secondary p2
runs for the other 12 drugs ("the same for the other 12 drugs", PREREG.md) use 50 random isolate-level splits
(seeds 1..50) and 10 alternative cluster-aware splits (alt salts 1..10) per drug instead of 400 and 100, to fit the
time budget. They remain secondary, are reported, and are never used for a claim or to choose a drug.
