# RECEIPTS: real output of `sh verify-it-yourself/run_checks.sh` (run from the package folder)
run at 2026-11-11T19:24:40Z with Python 3.11 (standard library only)
```
ok    sha256 object/p1_subset_cases.tsv
ok    sha256 object/h2h_percase_all_cases.tsv.gz
ok    all-case table: 10189 rows, 10189 distinct cases
ok    subset n_terms <= 3 selected here = object/p1_subset_cases.tsv (2038 rows)
ok    every subset case has 1 to 3 terms
ok    all RR in [0, 1]
      MRR method 0.138444, LIRICAL 0.104737, ratio 1.321825
ok    MRRs and ratio equal the claimed 0.1384 / 0.1047 / 1.3218
ok    G1: MRR ratio >= 1.10
      stdlib paired bootstrap of the MRR difference: 95% [0.0250, 0.0425]
ok    G2: paired case-bootstrap 95% interval of the difference lies above 0
      null: real 0.033707, best of 400 controls 0.013722
ok    null values equal the claimed ones
ok    G3: real difference beats all 400 controls
ok    object/p1_summary.json records the same gate and n
PASS
exit code 0
```
