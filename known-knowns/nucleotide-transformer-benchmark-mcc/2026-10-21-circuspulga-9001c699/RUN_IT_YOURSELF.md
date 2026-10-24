# Run it yourself (fresh shell, from this folder)
sh verify-it-yourself/run_checks.sh
Expected: ten task lines (see verify-it-yourself/RECEIPTS.md) and last line PASS.
Rebuild the object from the source: download benchmark.csv (URL in the-record-we-beat/record.md; check sha256 a93c1e72...0ca6), then
  pip install -r how-we-built-it/requirements.txt && python how-we-built-it/fold_audit_v2.py benchmark.csv FOLD_AUDIT.json
and keep the 10 histone tasks (same pairs, diffs, p-values as object/fold_audit_histone.json).
