# Verification Receipts: `bivariate-bicycle-exact-distance-360-756` (`p1`)

## SHA-256 Digest of Claimed Witness
```text
2894986d2179d2db637805691c36033eae41721b9d29267c58d044d85da0f878  object/bb504_logical_wt28.txt
```

## Control & Calibration Checks (`attempts/isd-stern-logical-hunter/result/isd_run_80k.log`)
- `[[288, 12, 18]]` (`l=12, m=12, A=x^3+y^2+y^7, B=y^3+x+x^2`): `rank(H_X) = rank(H_Z) = 138`, `k = 12`, `min_logical_wt = 18` (`11,978` hits).
- `[[360, 12, <= 24]]` (`l=30, m=6, A=x^9+y+y^2, B=y^3+x^25+x^26`): `rank(H_X) = rank(H_Z) = 174`, `k = 12`, `min_logical_wt = 24` (`47,152` hits).

## Exact Output of `sh verify-it-yourself/run_checks.sh`
```text
{"k": 12, "l": 42, "left_weight": 12, "m": 6, "n": 504, "rank_HX": 246, "rank_HZ": 246, "rank_HZ_aug": 247, "right_weight": 16, "weight": 28}
PASS
```
