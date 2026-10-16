# Run it yourself

From this folder, in a fresh shell (Python 3.8 or newer, standard library only):

    sh verify-it-yourself/run_checks.sh

Expected output (verify-it-yourself/RECEIPTS.md holds the real run):

    VERIFIED [[150,1,50]] shadow=True: value=1362 digits, max column coefficient <= 0, 49+2+48 multipliers
    check2 PASS [[150,1,50]] value>0: True max column: <=0
    VERIFIED [[150,1,51]] shadow=True: value=1485 digits, max column coefficient <= 0, 50+3+49 multipliers
    check2 PASS [[150,1,51]] value>0: True max column: <=0
    PASS

What is checked: each certificate lists integer multipliers for the rows of the stabilizer-code LP (A_0 = 1,
sum A_i = 2^(n-k), A_j = B_j below the distance, A_j <= B_j from the distance on, Rains shadow S_j >= 0, with
B and S given by the quaternary MacWilliams transform). The combined row has every coefficient <= 0 and a
positive right-hand side, so the LP is infeasible (Farkas' lemma) and no [[150,1,d]] code exists for d = 50
(object/cert_150_1_50_sh.json) or d = 51 (object/cert_150_1_51_sh.json).

Rebuild the certificates (needs python-flint 0.9.0 in a virtual environment; minutes per LP):

    python3 -m venv venv && venv/bin/pip install python-flint==0.9.0
    venv/bin/python -c "import sys; sys.path.insert(0,'how-we-built-it'); import qlp, json; r = qlp.solve_phase1(150, 1, 50, True, prec=1536, window=8, max_iter=60000); json.dump(r['cert'], open('cert_150_1_50_sh.json','w')); print(r['status'])"

Expected: `infeasible`. The rebuilt certificate need not be byte-identical (any valid Farkas certificate proves
the same statement); check it with verify-it-yourself/check_cert.py. The same call with 51 in place of 50 rebuilds the d = 51 certificate (both were found with window=8).
Propagation check: how-we-built-it/parse_table.py and propagate.py on the complete table page
https://www.codetables.de/QECC/Tables_color.php?q=4&n0=1&n1=256&k0=0&k1=256 (fetch it yourself) give closure 51
at (150,1).
