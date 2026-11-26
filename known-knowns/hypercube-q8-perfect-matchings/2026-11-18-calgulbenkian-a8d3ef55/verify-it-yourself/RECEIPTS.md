# Verification Receipts

Command executed from package root:

```sh
sh verify-it-yourself/run_checks.sh
```

Real output:

```text
OK: Full-cube A005271(1..5) reproduced by both Engine 1 and Engine 2 (1, 2, 9, 272, 589185)
OK: Q_5 |Fix(P_5)| = 0 (Engine 1 == Engine 2), mod 5 = 0 == A005271(5) mod 5
OK: Q_6 |Fix(P_5)| = 836 (Engine 1 == Engine 2), mod 5 = 1 == A005271(6) mod 5
OK: Q_7 |Fix(P_5)| = 5741584 (Engine 1 == Engine 2), mod 5 = 4 == A005271(7) mod 5
OK: Q_8 |Fix(P_5)| = 743141892135168 (Engine 1 == Engine 2), mod 5 = 3
VERIFIED: A005271(8) == 3 (mod 5) via |Fix_{M(Q_8)}(P_5)| = 743141892135168
PASS
```
