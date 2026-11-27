# Run It Yourself — `eterna100-v2-vienna2-algorithmic-solve` (`2026-11-08-mizopl-3aa1af0b`)

## 1. Fast Standalone Verification (`< 1s`, Standard Python + ViennaRNA)

From the package root, run:

```sh
sh verify-it-yourself/run_checks.sh
```

This runs `verify-it-yourself/verify.py`, which checks:
1. All `SHA256SUMS` digests across `object/`.
2. `object/manifest_sha256.json` (`sha256: a378b52c903b42aaa2aaf7c55a8759575515760f66cef8689e38e55ecfb19e75`) and `object/certificate.json` (`sha256: 3aa1af0b4cff8661193a5ab8fc3b074a42182b666d4a6af04104bcabc9c77879`).
3. `object/ckpt_best.json` (`sha256: 03594be6116df6a7e796fc45191e8aade08b12a215c15c394deb2d636af39b2f`), verifying all `100` Eterna100-V2 de novo designs under live `RNA.fold` (`95/100` exact MFE `d_bp = 0` including `#79 Shapes and Energy` and `#71 Variation of a crop circle`; `96/100` exact MFE ground state `de_mfe = 0.00 kcal/mol` including `#68 Taraxacum officinale`).
4. `object/p3_undesignability_certificates.json` (`sha256: e08fb41d6b11a3d01841866bba9cd33ca25d43924039267e3673e8001207f240`), verifying all `5` Turner 2004 thermodynamic barrier certificates (`#68, #86, #90, #99, #100`) and all `3` general mathematical laws (`Law #1`, `Law #2`, `Law #3`).

To run the negative control (adversarial corruption rejection):

```sh
python3 verify-it-yourself/verify.py --corrupt
```

## 2. Clean-Room Cold-Start De Novo Solver Reproduction (`~4.5s` on Laptop CPU)

To re-run our frozen de novo solver (`how-we-built-it/cegis_rna_solver.py`, `sha256: 52f5b2e60fe717e9c18768bd31776d33eafa1ee62da6b830cd622eb95249cb75`) from a clean-room cold start without reading `ckpt_best.json`:

```sh
python3 how-we-built-it/cegis_rna_solver.py --puzzles 79,71,68 --max-seconds 25 --ckpt clean_cold_verify.json
```

To re-run the exhaustive Turner 2004 `p3` thermodynamic barrier verifier (`~7.7s` under `ViennaRNA 2.6.4`):

```sh
python3 how-we-built-it/verify_p3_undesignability_certificates.py
```
