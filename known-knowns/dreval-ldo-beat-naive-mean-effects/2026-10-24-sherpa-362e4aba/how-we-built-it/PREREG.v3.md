# Pre-registration v3 — pin the October 2025 data version

Written 2026-10-23T22:00:19Z. Supersedes only the data-version line of `PREREG.v2.md`
(sha256 `29260e18f26ade3be18a95037c5af5e2c3458410905f6f1f457430b3126d5d52`). Everything else in
`PREREG.md` and `PREREG.v2.md` stands. **No model output from this run had been scored.** The only
model run in flight is the reproduction of the *published* baselines, which v2 required first.

## Why

drevalpy 1.3.5 cannot run the published leader on the current data record: `MultiOmicsNeuralNetwork`
asks for 100 methylation principal components and record 23159774 ships a methylation view that
allows at most 80 (`ValueError: n_components=100 must be between 0 and min(n_samples, n_features)=80`).
The data's feature files drifted under the code. Patching the leader's settings would no longer be
re-running the published model, so instead the data version contemporaneous with the report is used.

## The pinned data

- Zenodo record **17343165** (created 2025-10-13, four days before the report's `last-modified` of
  2025-10-17), file `CTRPv2.zip`, md5 `e015a6753c820bdb4ffb3f972df1faac` (matches the record's
  published checksum; downloaded 2026-10-23T21:55:34Z, HTTP 200, 517,644,342 bytes). The previous
  record, 17176585 (2025-09-22), carries a byte-identical `CTRPv2.zip`, so the data was stable across
  the window in which the report could have been generated.
- `meta.zip` from the same record, md5 `39aa43dd152806ab58a35065bb268ba5`.
- **The response values are identical** to record 23159774: same 395,024 rows, 235,974 measured
  pairs, 545 drugs, 886 cell lines, and `LN_IC50_curvecurator` agrees on every shared pair to
  4.1e-14. Only feature files differ. The vault (drawn from drug identifiers) is unaffected.
- `CTRPv2.csv` sha256 recorded in `data/dataset-sha256-oct2025.txt`.

## Consequence for the claim

The confirmatory runs, the baseline re-runs and the null test all use drevalpy 1.3.5 on this data.
This is the closest available reconstruction of the environment that produced 0.0235.
