# Run It Yourself (`2026-10-29-mizopl-d0d5d2a2`)

## Option 1: Instant Zero-Dependency Verification (`< 3 seconds`)

Requires **only Python 3.8+ standard library** (`csv`, `hashlib`, `json`, `math`, `pathlib`, `sys`). Verifies all SHA-256 hashes of `object/certificate.json`, `object/certificate_phase1_cpu_p1_p2.json`, `object/manifest_sha256.json`, `object/test_labels_and_strata.csv`, and all 35 saved 5-seed prediction CSVs (`object/seed_{1..5}_*.csv`), and recomputes the exact 5-seed Pearson correlation (`PCC`) across all $N = 49,028$ official `BindingDB_Patent` test pairs (`2019–2021`), per-year domain-shift strata (`2019`, `2020`, `2021`, `p2`), and target/ligand generalization strata (`Seen-Target`, `Unseen-Target`, `Unseen-Ligand`, `p3`):

```bash
sh verify-it-yourself/run_checks.sh
```

## Option 2: Full End-to-End Reproduction via Official `PyTDC` (`DTI_DG_Group`)

To download `BindingDB_Patent` via `tdc.benchmark_group.dti_dg_group`, precompute the protein/ligand features and declared `facebook/esm2_t12_35M_UR50D` sequence embeddings, train all 5 official seeds (`1..5`) strictly on each seed's `train` split (`2013–2018`), and evaluate via `group.evaluate_many`:

```bash
pip install PyTDC numpy scipy pandas scikit-learn lightgbm xgboost rdkit numba torch transformers
python3 how-we-built-it/step01_download_manifest_and_eda.py
python3 how-we-built-it/step03_precompute_features.py
python3 how-we-built-it/extract_esm2_protein_embeddings.py
python3 how-we-built-it/step08_run_5seeds_and_verify.py
python3 how-we-built-it/step14_full_horizon_5seeds.py
python3 how-we-built-it/step16_bayes_mmse_asymmetric_gate_5seeds.py
python3 how-we-built-it/step17_zero_trust_skeptic_audit_fullwin.py
```
