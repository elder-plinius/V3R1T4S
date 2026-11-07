# Panel Gate: `tdc-dti-dg-bindingdb-patent-pcc`

- `target_id`: `tdc-dti-dg-bindingdb-patent-pcc`
- `submission_id`: `2026-10-29-mizopl-d0d5d2a2`
- `status`: `CONFIRMED_PARTIAL`
- `partial_win`: `p1`
- `reproduce_pass`: `true`
- `novelty_pass`: `true`
- `criterion_pass`: `true`
- `confirmed_scope`: Partial Win p1 on TDC DTI Domain-Generalization (BindingDB patent-year split: 2013-2018 train_val -> 2019-2021 test, N = 49,028 across official seeds 1..5): 100% CPU-only 4-Level Matryoshka Functional ANOVA + Universal Kriging Tanimoto Kernel Ridge Regression (TKRR) + Homology-Gated Stacker (Track A, zero PLM, zero GPU, zero external data, with all architectural and hyperparameter choices fixed on train_val inner temporal validation splits 2013-2016 -> 2017-2018 and 2013-2017 -> 2018 prior to the first test-set evaluation in step08) achieves official group.evaluate_many test Pearson r = 0.580 ± 0.003 (exact 5-seed mean 0.57942 ± 0.00299; seeds 0.57856, 0.58064, 0.58094, 0.58287, 0.57410), surpassing Rank #2 OrangeBalls-ProtBertMorgan (0.538 ± 0.008) by +0.04142 (>= +0.010 margin, 100.00% 10,000-resample bootstrap win rate) and reproduced 5-seed ERM (0.51310 ± 0.00270) by +0.06632.

## Panel Summary

1. **Reproduce (`panel/reproduce.md` — `pass: true`):** `sh verify-it-yourself/run_checks.sh` executes `verify-it-yourself/verify.py`, verifying `object/manifest_sha256.json` (`sha256: 97ed1afd16d55de3a4768f78143660ee77d63e1f3fb3eb5c737c65522795e386`), `object/certificate.json` (`sha256: 027ee0b610df47dca9bb52746493f7b2cf264724f42b32c5ae2a295f2b797b82`), `object/certificate_phase1_cpu_p1_p2.json` (`sha256: 74a7be4004be2b3f500c9690b4e502bfd5fadc05bf069a5b6909f6cd57aa673c`), and all `40` keyed prediction CSV part files (`object/seed_{1..5}_{track}_part{1,2}.csv`, keyed by `row_index,Drug_ID,Target_ID,y_pred` across all `49,028` official test rows), and rejects any corrupted object (`--corrupt` or byte/digit tampering).
2. **Novelty (`panel/novelty.md` — `pass: true`):** The CPU-only 4-Level Matryoshka Functional ANOVA + Universal Kriging TKRR + Catalytic Pocket-Core (`S_pocket`) Homology-Gated Stacker (`Track A`) is distinct from the DomainBed neural baselines (`ERM`, `IRM`, `GroupDRO`, `MMD`, `CORAL`, `MTL`, `AndMASK`), `OrangeBalls-ProtBertMorgan` (`0.538 ± 0.008`), and `Otter-Knowledge-Ensemble` (`0.588 ± 0.002`).
3. **Criterion (`panel/criterion.md` — `pass: true`):** All architectural levels, kernel weights, and hyperparameters of the claimed primary `Track A` (`p1`) were selected on `train_val` (2013–2018) inner temporal validation splits (`step02`–`step07`: Split A `2013–2016 -> 2017–2018` `0.45340 -> 0.62386`; Split B `2013–2017 -> 2018` `0.45172 -> 0.60613`) before the first test-set evaluation in `step08`. Post-`step08` Phase-2 runs (`step11`–`step16`, including `Track F1` at `0.59996 ± 0.00266`) and diagnostic stratum breakdowns (`p2`, `p3`) are disclosed as unclaimed exploratory ablations.
