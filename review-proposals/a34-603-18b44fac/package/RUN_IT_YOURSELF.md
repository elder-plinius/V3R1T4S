# Deterministic reproduction from package root

No solver or network is required for verification because both the 602-word parent and 603-word target are included. From the package root, run:

```sh
python3 verify-it-yourself/validate.py
python3 verify-it-yourself/upstream_cwcheck.py object/A34_8_7_603.txt 34 8 7 --M 603 --sha256 18b44fac5d5ff1d4895fd9de1240669eb71543b3e15599f7f864e090aa1491ad
python3 verify-it-yourself/test_negative.py
sh verify-it-yourself/run_checks.sh
sha256sum -c SHA256SUMS
```

Expected end of `run_checks.sh`: `PASS`. The upstream file `upstream_cwcheck.py` has immutable Git blob SHA-1 `baf9430775d73e2221928693a0177488d620cd65`, from [original GitHub checker](https://github.com/elder-plinius/V3R1T4S/blob/7aca3835635e5323b48cdf3b5b59fcde502cab28/known-knowns/bigger-codes/verify-it-yourself/cwcheck.py). Verify file identity with `git hash-object verify-it-yourself/upstream_cwcheck.py`.

The pure Python verifier checks exact size, length, weight, uniqueness, all pair distances, four-subset collisions, the code SHA-256 and direct/inverse parent-to-result delta. The upstream checker is independent original code. Negative controls must be rejected.

Search reproduction, which is optional for validating the bound, uses `how-we-built-it/engine.cpp`, `scan.cpp`, `reproduce_search.sh`, and saved search logs. An identical trajectory is not guaranteed across C++ standard-library versions, whereas replaying the 38-remove/39-add certificate is deterministic.

## Optional exploratory search replay

From the package root, on Linux with g++ installed, use `bash how-we-built-it/reproduce_search.sh 50 150` (50 rounds, 150-second budget). The search writes under `how-we-built-it/replay_run/`, or another directory set using `OUTDIR=`. This may find a different witness or none on another standard-library implementation. This is not required to verify the exact included code.
