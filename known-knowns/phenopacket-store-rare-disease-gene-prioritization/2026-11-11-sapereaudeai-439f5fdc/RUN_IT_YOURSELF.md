# Run it yourself (from this folder, fresh shell)

## 1. Check the claimed p1 numbers (seconds, standard library)
    sh verify-it-yourself/run_checks.sh
Expected output: the lines in verify-it-yourself/RECEIPTS.md, ending with `PASS`.

## 2. Recompute the frozen p1 statistics with numpy (seconds)
how-we-built-it/code/p1_eval.py needs the full per-case table (object/h2h_percase_all_cases.tsv.gz, gunzipped) and
the earlier run's per-case table with the same n_terms column (its sha256 is in how-we-built-it/PREREG.md; it is
regenerable with run 1's code). Expected output: how-we-built-it/logs/p1_eval.out.

## 3. Rebuild the per-case rows from public sources (hours)
1. Download phenopacket-store 0.1.27 all_phenopackets.zip (sha256 d0c70005...205a) and HPO release v2026-06-06
   (hp.obo, phenotype.hpoa, genes_to_disease.txt); hashes in how-we-built-it/inputs/frozen_inputs_and_code_sha256.txt.
2. Clean the HPOA: `python -I how-we-built-it/code/run3_full_eval/clean_hpoa.py all_phenopackets.zip
   v2026-06-06.phenotype.hpoa cleaned.hpoa census.json` (expected sha256 5e1a2fcf...aa14).
3. Run the frozen method: how-we-built-it/code/run3_full_eval/frozen_method.py (see its docstring and README.md there;
   about 1.5 min, up to about 1 GB).
4. Run LIRICAL 2.4.1 `benchmark --phenotype-only --parallelism 4` with the cleaned file as phenotype.hpoa, in chunks of
   100 cases (run_lirical_chunks.sh; about 13,400 JVM-seconds for all 10,189 cases, -Xmx1g).
5. Score both with how-we-built-it/code/run3_full_eval/h2h_score.py; the result must equal
   object/h2h_percase_all_cases.tsv.gz (gunzipped).
6. Select n_terms <= 3 and run step 2.
Large intermediate files are listed with sizes and sha256 in how-we-built-it/inputs/LARGE_FILES_not_included.txt.

Note on the candidate space (found by the REPRODUCE skeptic): the HGNC protein-coding file used holds 19,276 approved
genes; rdlib.load_hgnc keeps those approved on or before 2026-06-09 (the corpus release date), which drops RNF229 and
TLN2-AS2 and gives the 19,274 candidates used for both tools. With all 19,276 genes, cases whose causal gene scores 0
get 2 more ties (RR changes below 1e-8).
