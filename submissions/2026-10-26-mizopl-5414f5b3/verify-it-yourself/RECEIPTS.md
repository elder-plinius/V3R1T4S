# Verification Receipts (`2026-10-26-mizopl-5414f5b3`)

## 1. Zero-Dependency Standalone Verification (`< 1s`)

Command:
```bash
sh verify-it-yourself/run_checks.sh
```

Output:
```text
[INFO] Loaded object/certificate.json (SHA-256: 5414f5b34d21ca17...)
[PASS] Track A (Mendelian Full Win, N=3,380, 19 chroms): ZS_7_cadd_free = 0.789624 (+0.077439), CI_6_multimodal = 0.807396 (+0.095211)
[PASS] Track A Transfer (Complex Traits p1, N=11,400, 22 chroms): ZS_7_cadd_free = 0.281541 (+0.031641), ZS_8_standalone = 0.284569 (+0.034669)
[PASS] Track B (p1 Alignment-Free Zero-Shot vs phyloP-241m=0.695964): AF_Closed_4 = 0.754022, AF_4P = 0.793262, AF_HumanOnly = 0.749720
[PASS] Track C (p2/p3 + MAF Audit): M1_135cols = 0.898454, M2_165cols = 0.904124, Borzoi Block-Scaled (7,731 cols) = 0.885711, CADD_noPopFreq_105cols = 0.740276 (delta -0.137446)
PASS
```

## 2. Full Raw-Parquet Benchmark Reproduction & Audit (`how-we-built-it/verify_full_benchmark.py`)

Command (against the released Hugging Face `songlab/TraitGym` parquet tables):
```bash
python3 how-we-built-it/verify_full_benchmark.py
```

Verified SHA-256 hashes of official input parquets:
- `mendelian_traits_matched_9/test.parquet`: `144db4bf965e3c2b8936cd675448bade96369b6546cfdadb5c7b2bca17389607`
- `complex_traits_matched_9/test.parquet`: `068940684e1e6f735a25a1a4418fb65390628023a96188af7f1a15dd17de7036`
- `object/certificate.json`: `5414f5b34d21ca175a70e8586db2d3374bcfe4e87323042d9b6d8256853ca2dd`
