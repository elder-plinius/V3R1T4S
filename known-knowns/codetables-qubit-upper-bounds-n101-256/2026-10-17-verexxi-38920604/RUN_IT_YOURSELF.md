# Run it yourself

From this folder, in a fresh shell (Python 3.8 or newer, standard library only):

    sh verify-it-yourself/run_checks.sh

Expected output: one VERIFIED line and one "check2 PASS" line per certificate, then PASS
(verify-it-yourself/RECEIPTS.md holds the real run).

What is checked: each certificate lists integer multipliers for the rows of the stabilizer-code LP (A_0 = 1,
sum A_i = 2^(n-k), A_j = B_j below the distance, A_j <= B_j from the distance on, Rains shadow S_j >= 0, with
B and S given by the quaternary MacWilliams transform). The combined row has every coefficient <= 0 and a
positive right-hand side, so the LP is infeasible (Farkas' lemma) and no [[135,1,d]] code exists for the d named
in each certificate file.

Rebuild (needs python-flint 0.9.0 in a virtual environment; minutes per LP):

    python3 -m venv venv && venv/bin/pip install python-flint==0.9.0
    venv/bin/python -c "import sys; sys.path.insert(0,'how-we-built-it'); import qlp, json; r = qlp.solve_phase1(135, 1, 45, True, prec=1536, window=8, max_iter=60000); print(r['status']); json.dump(r.get('cert'), open('rebuilt.json','w'))"

Expected: `infeasible`; check rebuilt.json with verify-it-yourself/check_cert.py (it need not be byte-identical).
Propagation check: how-we-built-it/parse_table.py and propagate.py on the complete table page
https://www.codetables.de/QECC/Tables_color.php?q=4&n0=1&n1=256&k0=0&k1=256 (fetch it yourself).
