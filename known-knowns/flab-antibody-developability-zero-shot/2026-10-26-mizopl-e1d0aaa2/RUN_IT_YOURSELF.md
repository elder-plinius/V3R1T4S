# Run It Yourself (`RUN_IT_YOURSELF.md`)

## 1. Quick Verification of the Packaged Certificate & Per-Antibody Predictions (`~1.5 seconds`)

From the root of this package (`2026-10-26-mizopl-e1d0aaa2/`), run:
```bash
sh verify-it-yourself/run_checks.sh
```
This requires only Python 3.8+ standard library (`csv`, `hashlib`, `json`, `math`, `os`, `sys`), verifies the SHA-256 commitments of `object/certificate.json` (`b6be3abe5d0dcff18fcf18d8e7a16f64164d434290274613f79b76f80f598eb6`), `object/predictions_tm_polyreactivity.csv` (`63cf82e9994c98a2dd2a69b47ff154b5ea9344fbfca0c4535ab11626ad0d7a9e`), `object/predictions_binding_part1..8.csv` (`8e748b57...` through `f41772d0...`, `104,737` rows), and all `190` upstream `Graylab/FLAb` data files at commit `e05e3f0135783ffb7de412df6a1467e7a0031911`, confirms that all `109,236` prediction rows across `172` dataset evaluations (`76` in `predictions_tm_polyreactivity.csv` + `96` in `predictions_binding_part1..8.csv`: `16` `score/binding` + `80` `data/binding`) embed zero third-party sequence data, recomputes the unweighted, sample-size-weighted (`N>=10`, `SqrtN-wt`, `N-wt`), full-category (`data/` + `score/`), and `score/`-subset means across all 6 `score/` categories (`tm`, `polyreactivity`, `binding`, `aggregation`, `expression`, `immunogenicity`) and all `data/` universes (including all `80` `data/binding` CSVs, the `12`/`15` `score/`-covered `data/binding` subsets, the `68`/`65` excluded `data/binding` subsets, and the `score/tm` plus `data/thermostability` 25-dataset union) for the single frozen method `CLSS_Reg8_AllBP_IMGT_Z`, verifies the claimed Partial Wins `p2` ($\ge 80\%$ sign consistency) and `p3` (length & germline confound control; Full Win, Binding, and `p1` are not claimed), verifies the $B = 1,000$ permutation null battery, and prints `PASS`.

## 2. Full Re-Computation from the `Graylab/FLAb` Benchmark Repository (`~46.0 seconds`)

To re-run the entire zero-shot scoring pipeline across all `54,131` unique antibody Fv/VHH pairs (`190` upstream FLAb CSV files), all `score/binding` (`16` datasets, `6,959` rows) and `data/binding` (`80` CSVs, `97,778` rows) universes, all 4 Thermostability universes (`15` `score/tm`, `20` standard `data/thermostability`, `21` full `data/thermostability`, and the `25`-dataset `score/tm` plus `data/thermostability` union), all Polyreactivity universes (`6` `score/`, `25` `data/`, `26` combined, and `20` unseen), the untouched categories (`pharmacokinetics` 9 datasets and `data/expression` 4 datasets), all `p3` partial and matched-stratum confound controls, and the $B = 1,000$ permutation null battery from scratch:

1. Clone `https://github.com/Graylab/FLAb` at commit `e05e3f0135783ffb7de412df6a1467e7a0031911` into `data/FLAb`:
   ```bash
   git clone https://github.com/Graylab/FLAb data/FLAb
   git -C data/FLAb checkout e05e3f0135783ffb7de412df6a1467e7a0031911
   ```
2. Run the standalone verification script (`requires numpy, scipy, pandas`):
   ```bash
   python3 how-we-built-it/verify_full_benchmark.py
   ```
   This finishes in `~46.0 seconds` on a single Apple M1 laptop CPU core (`16 GB` RAM) with zero GPU usage.
