# Verification Receipts (`immrep22-tcr-epitope-microauc`)

## Command

```sh
sh verify-it-yourself/run_checks.sh
```

## Exact Output

```text
=== [1/2] Verifying immrep22-tcr-epitope-microauc predictions, evaluate.py stats, and p1/p2/p3 audit ===
[Task 1] _Average MicroAUC: 0.882173 vs tcrexab 0.847347 (gain = +0.034826)
[Task 1] Epitope wins vs tcrexab: 15/17 | Wilcoxon p = 6.713867e-04 | Bootstrap win rate = 100.00%
[Task 1] Column-maximum wins across all 22 methods: 9/17
[p1]     SPRWYFYYL MicroAUC: 0.877874 vs column max 0.837823 (gain = +0.040050)
[p2]     _Average Rank:      2.859120 vs tcrexab 3.284289 (diff = -0.425169)
[p3]     Control overlap: 0/17 | Levenshtein>=2 MicroAUC: 0.868783 vs 0.831030 (+0.037753) | 400-perm Null max = 0.553360 (z = +22.38)
PASS: ALL IMMREP22 CLSS CHECKS SUCCEEDED
=== [2/2] Negative control: negated scores on SPRWYFYYL.txt (must fail) ===
Negative control rejected as expected.
ALL CHECKS PASS
```

- **Exit code**: `0`
- **Last line**: `ALL CHECKS PASS`
