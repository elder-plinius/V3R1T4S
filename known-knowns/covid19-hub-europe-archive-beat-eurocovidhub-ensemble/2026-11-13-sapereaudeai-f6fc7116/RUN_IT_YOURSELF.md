# Run it yourself

## Quick check (standard library only, a few seconds)

From this package folder, in a fresh shell:

    sh verify-it-yourself/run_checks.sh

Expected last line: `PASS` (output as in verify-it-yourself/RECEIPTS.md). It checks the reproduction table against
the published per-model means, the 1% statements for both truth modes, the rows that are not exact, and the WIS
definition (identity, known positive, known negative).

## Full recomputation from the public inputs (numpy and pandas; about 80 MB download, a few minutes)

1. Fetch the inputs (one honest request per file, 2 s apart, sha256 logged; stops on 401/403/429/503):

       mkdir -p data
       python -I -B how-we-built-it/code/fetch_hub.py how-we-built-it/fetch_lists/fetch_list.tsv data fetch_log.tsv 2.0
       cp how-we-built-it/fetch_lists/file_map.tsv data/file_map.tsv

   Compare the sha256 values in fetch_log.tsv with how-we-built-it/outputs/fetch_log_all.tsv (fetched 2026-11-13
   from the archive's main branch, which the github.com tree pages showed at commit
   ef5eef8464a8ace38a6e93ca16026647bf09e1b5; scores.csv sha256
   c59afa8e3c9530e71d1c4c5445794bf6600b9ae3aaecec89db7e34def4aeb54c). To pin the commit, replace `/main/` by
   `/ef5eef8464a8ace38a6e93ca16026647bf09e1b5/` in the fetch list.

2. Scorer self-test:

       python -I -B how-we-built-it/code/wis_selftest.py

   expected last line `SELFTEST PASS`.

3. Recompute every published row under both truth modes:

       python -I -B how-we-built-it/code/p3_reproduce.py data out owidhosp
       python -I -B how-we-built-it/code/p3_reproduce.py data out primary

   expected first lines `... covered: 31256 | rows exact on all 4 (rounded): 31253 | missing files: 0` (owidhosp) and
   `... rows exact on all 4 (rounded): 30722 ...` (primary); out/per_model_owidhosp.csv and out/per_model_primary.csv
   rebuild object/p3_reproduction_table.csv (how-we-built-it/outputs/p3_log_*.txt hold the run's output).

4. Re-derive the row-selection rules and compare truth vintages:

       python -I -B how-we-built-it/code/rederive_exclusions.py data out/recomputed_rows_owidhosp.csv.gz out/rederive_owidhosp.txt
       python -I -B how-we-built-it/code/vintage_diff.py data out/vintage_diff.txt

   expected `kept AND published: 31256`, `kept but NOT published: 0`, `published but NOT kept: 0`, and for cases and
   deaths `ecdc vs final0927: ... differ 0`.

The truth modes: `primary` = the archive's data-truth/ECDC/truth_ECDC-Incident {Cases, Deaths, Hospitalizations}.csv
(the reading pre-registered in how-we-built-it/PREREG.md); `owidhosp` = the same for cases and deaths, with
hospitalisation truth from data-truth/OWID/truth_OWID-Incident Hospitalizations.csv only. `final0927` and
`final0927_owidhosp` swap in the weekly final vintage 2024-09-27 for cases and deaths (same results).
