# Run It Yourself (`RUN_IT_YOURSELF.md`)

## 1. Quick Verification of the Packaged Certificate & Per-Antibody Predictions (`< 1 second`)

From the root of this package (`2026-10-26-mizopl-e1d0aaa2/`), run:
```bash
sh verify-it-yourself/run_checks.sh
```
This requires only Python 3.8+ standard library (`csv`, `hashlib`, `json`, `math`, `os`, `sys`), verifies the SHA-256 commitments of `object/certificate.json` (`d59325d4892db661c638af2d7d2bdf6e35a6c06f95e869d2bc361470def74ecb`), `object/predictions_tm_polyreactivity.csv` (`63cf82e9994c98a2dd2a69b47ff154b5ea9344fbfca0c4535ab11626ad0d7a9e`), and all 94 upstream `Graylab/FLAb` data files at commit `e05e3f0135783ffb7de412df6a1467e7a0031911`, confirms that `object/predictions_tm_polyreactivity.csv` (`4,499` rows across `76` dataset evaluations) embeds zero third-party sequence data, recomputes the unweighted, sample-size-weighted (`N>=10`, `SqrtN-wt`, `N-wt`), full-category (`data/` + `score/`), and `score/`-subset means and margins for the single claimed method `CLSS_Reg8_AllBP_IMGT_Z`, verifies `p1` (all 4 Thermostability universes), `p2` ($\ge 80\%$ sign consistency), `p3` (length & germline confound control), and the $B = 1,000$ permutation null battery, and prints `PASS`.

## 2. Full Re-Computation from the `Graylab/FLAb` Benchmark Repository (`~19.7 seconds`)

To re-run the entire zero-shot scoring pipeline across all `8,900` unique antibody Fv/VHH pairs, all 4 Thermostability universes (`15`, `20`, `21`, and `25` datasets), all Polyreactivity universes (`6` `score/`, `25` `data/`, `26` combined, and `20` unseen), the untouched categories (`pharmacokinetics` 9 datasets and `data/expression` 4 datasets), all `p3` partial and matched-stratum confound controls, and the $B = 1,000$ permutation null battery from scratch:

1. Clone `https://github.com/Graylab/FLAb` at commit `e05e3f0135783ffb7de412df6a1467e7a0031911` into `data/FLAb`:
   ```bash
   git clone https://github.com/Graylab/FLAb data/FLAb
   git -C data/FLAb checkout e05e3f0135783ffb7de412df6a1467e7a0031911
   ```
2. Run the standalone verification script (`requires numpy, scipy, pandas`):
   ```bash
   python3 how-we-built-it/verify_full_benchmark.py
   ```
   This finishes in `~19.7 seconds` on a single Apple M1 laptop CPU core (`16 GB` RAM) with zero GPU usage.
