# Run it yourself (from this folder, fresh shell)
sh verify-it-yourself/run_checks.sh
# expected output: verify-it-yourself/RECEIPTS.md, last line PASS
# checker self-test: for t in pos_n8 neg_n8 stray_n8 space_n8; do python3 verify-it-yourself/check_union.py verify-it-yourself/selftest_inputs/$t.lines 8 2 | tail -1; done   # VALID INVALID INVALID INVALID
# rebuild the object byte for byte from source: see how-we-built-it/README.md
