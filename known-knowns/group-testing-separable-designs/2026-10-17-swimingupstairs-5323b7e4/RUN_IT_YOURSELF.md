# Run it yourself (from this folder, fresh shell)
sh verify-it-yourself/run_checks.sh
# expected output: see verify-it-yourself/RECEIPTS.md, last line PASS
# checker self-test: for t in pos_n8 neg_n8 stray_n8 space_n8; do python3 verify-it-yourself/check_union.py verify-it-yourself/selftest_inputs/$t.lines 8 2 | tail -1; done   # VALID INVALID INVALID INVALID
# Rebuild (not bit-reproducible; wall-clock time limits): mkdir -p work/code work/out && cp how-we-built-it/mc2.c how-we-built-it/ladder.sh work/code/ && gcc -O2 -o work/code/mc2 work/code/mc2.c -lm && sh work/code/ladder.sh 15 70 600   # writes work/out/lad_15_<m>; see how-we-built-it/README.md for seeds and logs
