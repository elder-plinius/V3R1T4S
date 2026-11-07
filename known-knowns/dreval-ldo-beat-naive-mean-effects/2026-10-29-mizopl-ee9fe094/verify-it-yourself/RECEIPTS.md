# Verification Receipts (`2026-10-29-mizopl-ee9fe094`)

## 1. Zero-Dependency Standalone Verification (`< 3 seconds`)

Command:
```bash
sh verify-it-yourself/run_checks.sh
```

Output:
```text
[INFO] Verified SHA-256 integrity of certificate.json (ee9fe094c784f640...) and all 46 files in object/
[PASS] Target dreval-ldo-beat-naive-mean-effects metrics and p3 / Tanimoto decompositions verified to < 1e-4 from object/*.csv
PASS
```

## 2. Cryptographic Commitments Verified by `verify.py`

- `object/certificate.json`: `ee9fe094c784f640d989ca22d0271533ff1b05e0a9d07c0fcbad975125170fa7`
- `object/preregistration_lock.json`: `5c9295e157e58376a63e0ef358edbfc950bcff6f30499c494ffc01a47cd6c33a`
- `object/stage2_ctrpv2_inner_results.json`: `280d82f7ba77125c4e101c59b69abf6f5191cb2988209304a2829b549fb564f5`
- `object/stage3_exvivo_cross_study_results.json`: `18d5a2fe711d78bdf00d87ac1d4cdda763fccfa617088f1452a9305594bec1c0`
- `object/stage3_p3_gap_decomposition.json`: `0cd24df7d16e1791d54a5c6ef4574d388ed232763bd8f5f7b34b98a16f2410fc`
- `object/stage4_formalities_and_tanimoto_nulls.json`: `1a3fddf801b6a7da49de5767f7dafdfeca1646dc5f9b9fbefe835a11cc46726f`
