# Skeptic 3 — Criterion & Zero-Leakage Audit (`tdc-dti-dg-bindingdb-patent-pcc`)

context: fresh review session

## 1. Verification Against Target Criteria (`a`)–(`f`) & Reviewers' Guidelines

1. **Criterion (a) — Official Benchmark Split (`train_val` 2013–2018 vs. `test` 2019–2021):**
   - Verified against official `tdc.benchmark_group.dti_dg_group` (`BindingDB_Patent`, `data/dti_dg_group.zip` `sha256: 4708233b8536d856a9ee6522623e4d44bbf7d2efc1c8496e69f6cd2c6482457a`): `train_val.csv` (`183,430` rows, years `2013–2018`) and `test.csv` (`49,028` rows, years `2019–2021`).
   - All `40` CSV part files in `object/` are keyed by `(row_index, Drug_ID, Target_ID, y_pred)` matching `group.get('BindingDB_Patent')['test']` row-for-row (`0..49,027`). `object/test_labels_and_strata.csv` and `object/skeptic_audit_certificate_fullwin.json` have been removed, and `.DS_Store` / `__MACOSX` entries have been removed from `object/manifest_sha256.json`.
2. **Criterion (b) — Official 5-Seed Evaluation (`seeds 1..5`):**
   - Claimed primary `Track A` (`trackA_strict_train`) is trained independently on each official seed's `train_s` split (`group.get_train_valid_split(benchmark='bindingdb_patent', split_type='default', seed=s)` for $s \in \{1, 2, 3, 4, 5\}$) and achieves `0.580 ± 0.003` (`0.57942 ± 0.00299`; seeds `0.57856, 0.58064, 0.58094, 0.58287, 0.57410`).
3. **Criterion (c) — Out-of-Time Generalization Breakdown (`Seen-Target` vs `Unseen-Target` vs `Unseen-Ligand` and Per-Year `2019 / 2020 / 2021`):**
   - Reported in `object/certificate.json`, `object/certificate_phase1_cpu_p1_p2.json`, and `the-record-we-beat/record.md`:
     - Per-year (`2019 / 2020 / 2021`): `Track A` achieves `0.55625 / 0.74675 / 0.86212` vs. reproduced 5-seed `ERM` `0.49720 / 0.64163 / 0.07611`.
     - By entity novelty: `Seen-Target` (`n=45,031`): `0.59719 ± 0.00307` (vs `ERM = 0.52590`); `Unseen-Target` (`n=3,997`): `0.20577 ± 0.00543` (vs `ERM = 0.12204`); `Unseen-Ligand` (`n=30,959`): `0.50163 ± 0.00417` (vs `ERM = 0.48444`).
4. **Criterion (d) — Zero Test-Year Selection Leakage & Pre-Test `train_val` Validation (`step02`–`step07`):**
   - Every architectural component and hyperparameter of the claimed primary `Track A` (`p1`) was developed and fixed on two internal temporal splits carved strictly out of `train_val` (`2013–2018`) in `how-we-built-it/step02_inner_temporal_anatomy.py` through `how-we-built-it/step07_test_full_modular_stack_splits.py` (`2026-10-29 04:12:50`–`05:20:09`) **prior to the first test-set evaluation in `step08_run_5seeds_and_verify.py` (`2026-10-29 05:24:41`)**:
     - **Inner Temporal Split A (`2013–2016 -> 2017–2018`, $n=58,283$):** `0.45340` (`step02` Target Mean) $\to$ `0.50615` (`step02` Target+Drug Residual) $\to$ `0.57503` (`step05` Per-Target TKRR) $\to$ `0.57548` (`step05b` Schur-Coupled Homology TKRR) $\to$ `0.60856` (`step06` 4-Level Universal Kriging TKRR) $\to$ **`0.62386` (`step07` Full 4-Level CPU-Only Stacker)**.
     - **Inner Temporal Split B (`2013–2017 -> 2018`, $n=24,499$):** `0.45172` (`step02` Target Mean) $\to$ `0.50157` (`step02` Target+Drug Residual) $\to$ `0.55863` (`step05` Per-Target TKRR) $\to$ `0.56207` (`step05b` Schur-Coupled Homology TKRR) $\to$ `0.58805` (`step06` 4-Level Universal Kriging TKRR) $\to$ **`0.60613` (`step07` Full 4-Level CPU-Only Stacker)**.
   - Because Phase 2 (`step10`–`step16`, `06:44`–`09:26`) was executed after `step08` and involved 5 additional test-set runs (`step11`, `step12`, `step14`, `step15`, `step16`), the formal claim is narrowed strictly to **Partial Win `p1` (`Track A = 0.580 ± 0.003` [`0.57942 ± 0.00299`])**, while Phase-2 `Track F1` (`beta_Ex = 0.72`, `0.59996 ± 0.00266`) and diagnostic breakdowns (`p2`, `p3`) are reported as unclaimed exploratory ablations.
5. **Criteria (e) & (f) — Pretraining Disclosure & Margin (`>= +0.010`):**
   - `Track A` uses **zero external pretraining (`0` PLM, `0` external bioactivity data)** and beats Rank #2 `OrangeBalls-ProtBertMorgan` (`0.538 ± 0.008`) by **`+0.04142 >= +0.010`** (`100.00%` 10,000-resample bootstrap win rate).

pass: true
