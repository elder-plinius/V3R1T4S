# Run It Yourself (`RUN_IT_YOURSELF.md`)

## 1. Quick Verification of the Packaged Certificate & Per-Antibody Predictions (`< 1 second`)

From the root of this package (`2026-10-26-mizopl-e1d0aaa2/`), run:
```bash
sh verify-it-yourself/run_checks.sh
```
This requires only Python 3.8+ standard library (`csv`, `hashlib`, `json`, `math`, `os`, `sys`), verifies the SHA-256 commitments of `object/certificate.json` and `object/predictions_tm_polyreactivity.csv`, audits all 723 antibody sequences across the 15 `tm` and 6 `polyreactivity` datasets, recomputes the unweighted and sample-size-weighted (`N>=10`, `SqrtN-wt`, `N-wt`) category means and margins, verifies `p1` (all 4 Thermostability universes), `p2` ($\ge 80\%$ sign consistency), `p3` (length & germline confound control), and both $B = 1,000$ permutation null batteries, and prints `PASS`.

## 2. Full Re-Computation from the `Graylab/FLAb` Benchmark Repository (`~14.7 seconds`)

To re-run the entire zero-shot scoring pipeline across all `5,961` unique antibody Fv/VHH pairs, all 4 Thermostability universes (`15`, `20`, `21`, and `25` datasets), all `p3` partial and matched-stratum confound controls, and both $B = 1,000$ permutation null batteries from scratch:

1. Clone `https://github.com/Graylab/FLAb` at commit `e05e3f0135783ffb7de412df6a1467e7a0031911` into `data/FLAb`:
   ```bash
   git clone https://github.com/Graylab/FLAb data/FLAb
   git -C data/FLAb checkout e05e3f0135783ffb7de412df6a1467e7a0031911
   ```
2. Run the standalone verification script (`requires numpy, scipy, pandas`):
   ```bash
   python3 how-we-built-it/verify_full_benchmark.py
   ```
   This finishes in `~14.7 seconds` on a single Apple M1 laptop CPU core (`16 GB` RAM) with zero GPU usage.
