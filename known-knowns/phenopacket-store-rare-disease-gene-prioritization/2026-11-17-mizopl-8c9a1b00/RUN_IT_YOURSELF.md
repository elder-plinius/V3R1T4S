# Run It Yourself

## 1. Live Upstream-Joined Verification Across `P2-Raw` (`127`), `P2-Holdout` (`988`), and `Pos-40` (`40`)

From this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

When `~/.cache/phenopacket_p2` is already populated with the pinned `< 2026-06-09` upstream archives (SHA-256 verified before use), `run_checks.sh` executes 100% offline in ~20 seconds and ends with:

```text
PASS
```

(On a fresh machine without `~/.cache/phenopacket_p2`, `verify.py` invokes `how-we-built-it/compile_precorpus_kg.py` to fetch the official pinned archives and verify their SHA-256 digests.)

## 2. Adversarial Negative Control (`--corrupt`)

```sh
sh verify-it-yourself/run_checks.sh --corrupt
```
