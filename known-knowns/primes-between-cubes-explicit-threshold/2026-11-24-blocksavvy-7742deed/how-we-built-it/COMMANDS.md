# Reproduce
Requirements: python3 with python-flint (tested 0.9.0, arb) and mpmath (tested 1.3.0).
  pip install python-flint mpmath        # in a fresh venv
  cd code && PY=python3 ./run_all.sh     # about 1 second
Expected (out/): main_prec128.txt and main_prec256.txt end with PASS (Phi(X0) = 0.934253344488...); main_29.734_expect_FAIL.txt
ends with FAIL; standalone_main.txt PASS and standalone_29.734_expect_FAIL.txt FAIL; scan_out.txt first line
"c=51.34 dens=thm11 Y_cert(prec128)=29.735 Y_cert(prec256)=29.735 agree=True"; null_tests_out.txt ALL_CONTROLS_BEHAVE;
journal_zfr_54.004_prec256.txt PASS at 29.907 and journal_zfr_54.004_29.906_expect_FAIL.txt FAIL;
standalone_journal_zfr_54.004.txt PASS; replay_ch_out.txt reproduces Cully-Hugill's 32.891867 and MTY's 32.753; mutation_out.txt MUTATIONS_AS_EXPECTED; the
script prints RUN_ALL_DONE.
Checking the inputs: the exact statements I1-I7 quoted in PROOF.md §1 are in data/ (I1: arxiv_2107.14468.pdf Thm 2,
Table 2, eq. (4) and §4; I3: yang_thesis_2025.pdf Theorem 1.3 (p. ~3 of Ch. 1); I4: arxiv_2311.05136.pdf Theorem 1.1;
I2 is quoted in arxiv_2311.05136.pdf Theorem 2.2; the record: ch_thesis.pdf Theorem 4.3 and its proof in Ch. 4).
