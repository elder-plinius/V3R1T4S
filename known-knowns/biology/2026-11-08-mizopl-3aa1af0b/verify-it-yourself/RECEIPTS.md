# Verification Receipts — `eterna100-v2-vienna2-algorithmic-solve` (`2026-11-08-mizopl-3aa1af0b`)

## 1. Clean Verification Command & Output

Command executed from package root:

```sh
sh verify-it-yourself/run_checks.sh
```

Exact output (`exit 0`):

```text
========================================================================
V3R1T4S Verification — eterna100-v2-vienna2-algorithmic-solve (Full Win)
========================================================================
[OK] SHA256SUMS verified across all 4 files in object/.
[OK] object/manifest_sha256.json commitments and 100-puzzle structural vectors verified.
[OK] Full Win & p1/p2 verified (live ViennaRNA 2.8.0): 95/100 exact MFE (d_bp=0, vs DesiRNA 92/100) and 96/100 MFE ground state (de_mfe=0.00 kcal/mol), including #79 Shapes and Energy (d_bp=0, E=-18.80), #71 Variation of a crop circle (d_bp=0, E=-6.50), and #68 Taraxacum officinale (de_mfe=0.00, E=-100.60).
[OK] p3 Thermodynamic Barrier Certificates & 3 Mathematical Laws verified across all 5 Sample Solution = None targets (#68, #86, #90, #99, #100).
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

## 3. Verified Object & Code Digest Summary

- `object/certificate.json`: `3aa1af0b4cff8661193a5ab8fc3b074a42182b666d4a6af04104bcabc9c77879`
- `object/manifest_sha256.json`: `a378b52c903b42aaa2aaf7c55a8759575515760f66cef8689e38e55ecfb19e75`
- `object/ckpt_best.json`: `03594be6116df6a7e796fc45191e8aade08b12a215c15c394deb2d636af39b2f`
- `object/p3_undesignability_certificates.json`: `e08fb41d6b11a3d01841866bba9cd33ca25d43924039267e3673e8001207f240`
- `how-we-built-it/cegis_rna_solver.py`: `52f5b2e60fe717e9c18768bd31776d33eafa1ee62da6b830cd622eb95249cb75`
- `how-we-built-it/verify_p3_undesignability_certificates.py`: `c4670dfee1223a03880ae97a7494f9a003b4ac5e5cccfa177ca4b6f5636fc1e5`
- `how-we-built-it/eterna100_v2_targets_only.tsv`: `c3e79eef8eef7db8a40d5c3e92c71114703e36a847593997dbe3edc025c7978a`
- Upstream `data/results.tsv` (`2,271,309` bytes, fetched `2026-11-08T15:32:28Z`): `2861ceb5a0280e5565c40016f169697fb324db7f7c56505c1489a8b78afcea6c`
- Upstream `data/eterna100_puzzles.tsv` (`96,092` bytes, fetched `2026-11-08T15:32:28Z`): `71147b94c1762a3c8fe93f59e87b53b6292b1c3b9367ce22d5a9c7c6b4736ef6`
