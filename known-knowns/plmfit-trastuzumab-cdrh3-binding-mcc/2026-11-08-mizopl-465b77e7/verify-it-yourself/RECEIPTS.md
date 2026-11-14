# Verification Receipts — `plmfit-trastuzumab-cdrh3-binding-mcc` (`2026-11-08-mizopl-465b77e7`)

## 1. Clean Verification Command & Output

Command executed from package root:

```sh
sh verify-it-yourself/run_checks.sh
```

Exact output (`exit 0`):

```text
========================================================================
V3R1T4S Verification — plmfit-trastuzumab-cdrh3-binding-mcc (Full Win)
========================================================================
[OK] SHA256SUMS verified across all 14 files in object/.
[OK] object/manifest_sha256.json commitments and split counts [173, 1, 36386] verified.
[OK] Track B (CV-Learned Inductive Model, N=36,386 x 3 seeds): MCC = 0.421004 +- 0.001735 (95% CI [0.412067, 0.430182] > 0.3898), AUROC = 0.789510, AP = 0.624177, 2-body gain = +0.010601 MCC, Inductive-to-Oracle gap = 0.001752.
[OK] Track A (Parameter-Free Canonical Law, N=36,386 x 3 seeds): MCC = 0.408391 +- 0.000411 (95% CI [0.398892, 0.417982] > 0.3898), AUROC = 0.785602, AP = 0.622932, 2-body gain = +0.006512 MCC, Inductive-to-Oracle gap = 0.001402.
PASS
```

## 2. Negative Control (Adversarial Corruption Rejection)

Command executed:

```sh
python3 verify-it-yourself/verify.py --corrupt
```

Exact output (`exit 1`):

```text
[FAIL] Simulated corruption flag (--corrupt) triggered rejection.
FAIL
```

## 3. Verified Object Digest Summary

- `object/certificate.json`: `465b77e779fe37b92f9da4444bb53016a97449138ba4c28fb1d13a863e47908c`
- `object/manifest_sha256.json`: `96429fd22f9ecaedadc97e21506e19752e2f18e7a77216836ff535a347b27d6d`
- Official upstream dataset `data/herH3/herH3_data_full.csv` (`17,149,024` bytes): `5137572eec7ce2689283854fefacd8bcd7c5cb2547d57f5ffc7c53c9fed4070f`
- Official upstream scoreboard `README.md` (`14,780` bytes, fetched `2026-11-08T14:42:30Z`): `51b672d563c778ae40a435cad51424a5b8e0f82294211642d2bfff4983792f0b`
