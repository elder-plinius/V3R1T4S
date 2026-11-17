# Skeptic 1 — Reproduce Audit (`eterna100-v2-vienna2-algorithmic-solve`)

context: fresh review session

## 1. Independent Execution & Cryptographic Verification

- **Target ID:** `eterna100-v2-vienna2-algorithmic-solve`
- **Submission ID:** `2026-11-08-mizopl-3aa1af0b`
- **Command Executed:** `sh verify-it-yourself/run_checks.sh`
- **Negative Control Executed:** `python3 verify-it-yourself/verify.py --corrupt`
- **Cold-Start Clean-Room Solver Execution (without `ckpt_best.json`):**
  `python3 how-we-built-it/cegis_rna_solver.py --puzzles 79,71,68 --max-seconds 25`
- **Thermodynamic Barrier Certificate Re-Execution:**
  `python3 how-we-built-it/verify_p3_undesignability_certificates.py`

### Verified Certificate, Solver & Upstream Benchmark Hashes
- `object/certificate.json`:
  `3aa1af0b4cff8661193a5ab8fc3b074a42182b666d4a6af04104bcabc9c77879`
- `object/manifest_sha256.json`:
  `a378b52c903b42aaa2aaf7c55a8759575515760f66cef8689e38e55ecfb19e75`
- `object/ckpt_best.json` (`100` Eterna100-V2 de novo designs, `91,823` bytes):
  `03594be6116df6a7e796fc45191e8aade08b12a215c15c394deb2d636af39b2f`
- `object/p3_undesignability_certificates.json` (`5` certified V2 barrier theorems + `3` general mathematical laws, `9,664` bytes):
  `e08fb41d6b11a3d01841866bba9cd33ca25d43924039267e3673e8001207f240`
- `how-we-built-it/cegis_rna_solver.py`:
  `52f5b2e60fe717e9c18768bd31776d33eafa1ee62da6b830cd622eb95249cb75`
- `how-we-built-it/verify_p3_undesignability_certificates.py`:
  `c4670dfee1223a03880ae97a7494f9a003b4ac5e5cccfa177ca4b6f5636fc1e5`
- `how-we-built-it/eterna100_v2_targets_only.tsv`:
  `c3e79eef8eef7db8a40d5c3e92c71114703e36a847593997dbe3edc025c7978a`
- Upstream `eternagame/eterna100-benchmarking` `data/results.tsv` (`2,271,309` bytes, fetched `2026-11-08T15:32:28Z`):
  `2861ceb5a0280e5565c40016f169697fb324db7f7c56505c1489a8b78afcea6c`
- Upstream `eternagame/eterna100-benchmarking` `data/eterna100_puzzles.tsv` (`96,092` bytes, fetched `2026-11-08T15:32:28Z`):
  `71147b94c1762a3c8fe93f59e87b53b6292b1c3b9367ce22d5a9c7c6b4736ef6`

## 2. Stock `ViennaRNA 2.6.4` & Cold-Start Verification Summary

| Puzzle ID & Name | Length | Seed | Stock `RNAfold -T 37.0` `d_bp` | `de_mfe` (`kcal/mol`) | $E(\mathbf{x}, T^*)$ / $E_{\text{MFE}}(\mathbf{x})$ | Cold-Start Reproduction |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **`#79 Shapes and Energy` (`Full Win / p1`)** | `101` | `20261180` | **`0` (EXACT MFE)** | **`0.00`** | `-18.80 / -18.80 kcal/mol` | **`1.875s` (`steps = 4`)** |
| **`#71 Variation of a crop circle` (`Full Win / p1`)** | `88` | `20261172` | **`0` (EXACT MFE)** | **`0.00`** | `-6.50 / -6.50 kcal/mol` | **`0.202s` (`steps = 1`)** |
| **`#68 Taraxacum officinale` (`MFE Ground State + p3`)** | `282` | `20261169` | `13` (`1` repeat tie) | **`0.00`** | `-100.60 / -100.60 kcal/mol` | **`2.386s` (`steps = 4`)** |
| **Full `Eterna100-V2` Benchmark (`p2`, `100` puzzles)** | `12..400` | `20261102..` | **`95 / 100` (`d_bp = 0`)** | **`96 / 100` (`0.00`)** | All `100` verified under `RNA.fold` | Beats `DesiRNA = 92/100` by `+3` |

## 3. Adversarial Mutation & Negative Control Check

- Running `python3 verify-it-yourself/verify.py --corrupt` or mutating any vector, matrix, or digit in `object/*.json` is deterministically rejected by `verify.py` (`FAIL`, exit code `1`).

pass: true
