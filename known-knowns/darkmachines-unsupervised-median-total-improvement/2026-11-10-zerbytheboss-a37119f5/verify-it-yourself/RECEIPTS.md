# Verification Receipts — Dark Machines BS-POT (`darkmachines-unsupervised-median-total-improvement`)

Command executed from package root:

```sh
sh verify-it-yourself/run_checks.sh
```

Output:

```text
Negative control rejected perturbed CSV cell.
Verified all 136 signal-channel rows and live Channel 2a retraining (max float32 diff = 0.0000).
BSPOT_MaxSec     : cha300 TI = 6.0000 (> 1.10), cha400 TI = 7.0000 (> 1.00), Median_TI = 5.3759.
BSPOT_Union_OR   : cha300 TI = 3.0000 (> 1.10), cha400 TI = 5.0000 (> 1.00), Median_TI = 5.0000, Min_TI = 0.8000 (>= 0.80).
BSPOT_FloorGuard : cha300 TI = 1.8000 (> 1.10), cha400 TI = 2.2136 (> 1.00), Median_TI = 3.1000, Min_TI = 0.9000 (>= 0.90).
PASS
```
