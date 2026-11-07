# Run It Yourself — `dreval-exvivo-beataml2-pdx-transfer` (`p3`)

## 1. Standalone Package Verification (< 3 Seconds, Python 3.8+ Standard Library Only)

From the root of this package directory (`2026-11-07-mizopl-d1d47e16`), run:

```sh
sh verify-it-yourself/run_checks.sh
```

This executes `verify-it-yourself/verify.py` using only the Python standard library and verifies:
1. Every entry in `SHA256SUMS` (`53` files, every file `< 910 KB`).
2. Exact digit-for-digit agreement between `object/certificate.json` (`sha256: d1d47e161a4d025e732817e75adbcc7a06bf258e1695c2d5800ed781e74e2025`) and `object/stage3_p3_gap_decomposition.json` (`sha256: d29f8337f60ef6a9d372a3b744892547c66f35071ce20016a297fe6f6d013542`).
3. All 10-split sample means, sample standard deviations (`ddof=1`), `RMSE == sqrt(MSE)` identities, and `p3` single-factor / cumulative gain equations.
4. All 30 keyed per-split prediction CSVs (`object/beataml2_split_{0..9}_{schur,base}.csv` and `object/pdx_bruna_split_{0..9}.csv`), confirming that **no ground-truth `y` (`response`) column is copied into `object/`**, verifying row-by-row `(split, cell_line_name, drug_name, pubchem_id)` alignment and key SHA-256 digests, and recomputing every column's L1 sum, L2 sum, mean, cross-column dot products, and the three unlabeled `p3` correction terms (`delta_assay`, `delta_platform`, `delta_overlap`) directly from the CSVs.

## 2. Re-Scoring Against Official Upstream `drevalpy` Response Files

To join the keyed per-split CSVs in `object/` directly against the official `drevalpy` response files on Zenodo (`https://zenodo.org/records/14974099`):
1. Download `BeatAML2.zip` (`BeatAML2/BeatAML2.csv` `sha256: 259d409e33d87be1c63139fd2c38f82d2d94be23442010bc2b5fd71cd5de73d9`), `PDX_Bruna.zip` (`PDX_Bruna/PDX_Bruna.csv` `sha256: 63ef6dc157bc6bf0dc7a08a18ca86ff84509b8d2ef5e1f4a3c42a3cfbf368ee4`), and `CTRPv2.zip` (`CTRPv2/CTRPv2.csv` `sha256: 3069f5df0ffefeb2adeeb2ae4be2e0e43ff588154e3be2d414cfbd1224a7dc41`, `splits.zip` `sha256: 28dfdd7dca4ea5d2ca7da1ea0f53bb2eb149bd150bfabbf47cd9f1f145fd5839`) into `$DREVAL_DATA_DIR`.
2. Run:

```sh
DREVAL_DATA_DIR=/path/to/data python3 how-we-built-it/stage3_exvivo_and_cross_study_eval.py
```

This fits the within-drug Fixed-Effect (`FE`) concentration-window regression (`LN_IC50_curvecurator ~ log_min_uM + log_max_uM`) strictly on each `CTRPv2` training split, applies the three unlabeled `p3` adjustments `(i)`, `(ii)`, `(iii)` each on its own and cumulatively to the frozen `SchurBilinearExVivoDRP` predictions, and reproduces every number in `object/certificate.json` and `object/stage3_p3_gap_decomposition.json` to 5 decimal places.
