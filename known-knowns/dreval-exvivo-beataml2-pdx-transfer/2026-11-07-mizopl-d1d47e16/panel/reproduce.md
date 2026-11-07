# Skeptic 1: Reproducibility Review — `dreval-exvivo-beataml2-pdx-transfer` (`p3`)

context: independent verification review of verify-it-yourself/run_checks.sh and object/
target_id: dreval-exvivo-beataml2-pdx-transfer
package: 2026-11-07-mizopl-d1d47e16

## Checks Performed

1. **Clean Execution:** Executed `sh verify-it-yourself/run_checks.sh` from a clean copy of the package; the script verified all 50 entries in `SHA256SUMS`, validated `object/certificate.json` (`sha256: d1d47e161a4d025e732817e75adbcc7a06bf258e1695c2d5800ed781e74e2025`) against `object/stage3_p3_gap_decomposition.json` (`sha256: d29f8337f60ef6a9d372a3b744892547c66f35071ce20016a297fe6f6d013542`), verified all 30 per-split CSVs (`object/beataml2_split_{0..9}_{schur,base}.csv` and `object/pdx_bruna_split_{0..9}.csv`), and printed `PASS` (`exit 0`).
2. **No Copied Ground-Truth Labels in `object/`:** Verified that none of the 30 CSV files in `object/` contain the ground-truth `y` (`response` / `LN_IC50_curvecurator`) column, and that every row is keyed by `(split, cell_line_name, drug_name, pubchem_id)` with upstream SHA-256 citations for `BeatAML2.csv` (`259d409e33d87be1c63139fd2c38f82d2d94be23442010bc2b5fd71cd5de73d9`) and `PDX_Bruna.csv` (`63ef6dc157bc6bf0dc7a08a18ca86ff84509b8d2ef5e1f4a3c42a3cfbf368ee4`).
3. **Adversarial Corruption Rejection:** Perturbed single digits inside `object/certificate.json`, `object/stage3_p3_gap_decomposition.json`, `object/beataml2_split_0_schur.csv`, `object/beataml2_split_0_base.csv`, and `object/pdx_bruna_split_0.csv`; in every case `sh verify-it-yourself/run_checks.sh` exited with status `1` and printed `FAIL`.

pass: true
