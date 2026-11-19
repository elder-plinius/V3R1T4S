== 1. object files present
== 2. full verification (pure-stdlib checker: rows, metrics, margin, bootstrap, calibration)
recomputed CLASS_LOK pr_auc 0.634333770922 roc_auc 0.880208333333
recomputed CLASS_SLK pr_auc 0.377856659137 roc_auc 0.838073691015
recomputed mean pr_auc 0.506095215029
match CLASS_LOK pr_auc 0.634333770922
match CLASS_LOK roc_auc 0.880208333333
match CLASS_SLK pr_auc 0.377856659137
match CLASS_SLK roc_auc 0.838073691015
match mean pr_auc 0.506095215029
margin ok: 0.634333770922 >= 0.275319148936
stdlib 10,000-resample bootstrap: fraction above bar 1.000000 (degenerate 0)
calibration ok: constant-1 gives 0.18181818181818182 / 0.09848484848484848 (the listed null-model values)
VERIFY_LOKSLK: PASS
== 3. corruption self-test (the checker must reject a reordered object)
corrupted object -> VERIFY_LOKSLK: FAIL
corruption correctly rejected
== 4. online cross-check of the official input pins (informational; skipped when offline)
table_v1.parquet: sha256 653d2b6f3013c7c6... (pinned 653d2b6f3013c7c6...) match=True
bench_pkis2-lok-slk-c-1.json: sha256 b7a58de2d71d5266... (pinned b7a58de2d71d5266...) match=True
PASS
