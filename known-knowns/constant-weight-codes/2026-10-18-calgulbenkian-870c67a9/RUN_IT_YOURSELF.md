# Run it yourself: 2026-10-18-calgulbenkian-870c67a9

From this folder, in a fresh shell (python3 3.8 or later, standard library only):

```sh
sh verify-it-yourself/run_checks.sh
```

The last line should be `ALL CHECKS PASS`. The checker alone:

```sh
python3 -I verify-it-yourself/check_delsarte.py --selftest
python3 -I verify-it-yourself/check_delsarte.py object/cert_A29_6_12.json 29 6 12 228441
```

The checker builds the Eberlein eigenvalues of the Johnson scheme J(29,12), checks the orthogonality relations exactly, checks every dual value is nonnegative, checks sum_k y_k (-Q_k(x)) >= 1 for every Johnson distance x from 3 to 12, computes 1 + sum_k y_k m_k as a fraction, and requires its floor to equal 228441. The script prints `PASS: A(29,6,12) <= 228441` on success. The run script also tests the checker on cells with known answers and on the merged certificate for A(31,12,10) (197), and runs three negative controls that must all be rejected. The table-implied bound is reproduced as described in the-record-we-beat/README.md (needs a fresh copy of the live page).

## How to rebuild the object

The certificate is a list of nonnegative rational dual values y_k (key "y" in the object). The checker needs nothing else, so the certificate can be checked without rebuilding it. The LP-building code that produced it is not in the contributor's snapshot (see how-we-built-it/README.md), so there is no rebuild command; to find a certificate of your own, solve the Delsarte linear program of the Johnson scheme J(29,12) with exact rational arithmetic as described in how-we-built-it/README.md.
