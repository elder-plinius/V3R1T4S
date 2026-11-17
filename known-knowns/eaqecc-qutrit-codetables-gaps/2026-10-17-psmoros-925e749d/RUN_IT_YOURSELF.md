# Run it yourself

From this package folder, in a fresh shell (python3, standard library only):

    sh verify-it-yourself/run_checks.sh

Expected output (verify-it-yourself/RECEIPTS.md holds the real one):

    n 33 s 56 c 24 k 1 dim_dual 10 d 31 (vectors of weight d outside the isotropic part: 17496)
    PASS

What it checks, from the definition:
- s = rank(S) over GF(3), and c = rank(S J S^T)/2 with <u,v> = u_X.v_Z - u_Z.v_X;
- k = n - s + c;
- d = the minimum symplectic weight over span(S)^perp minus span(S), by exhaustive enumeration of all 3^10 vectors;
- the result is compared with the cell (33,1,24) of the table, d_lower 25 < d <= d_upper 32.

## Rebuild the object (optional; needs numpy)

how-we-built-it/code/ holds the builder (class construction with at most 2 zeros per logical word). Set RUN to a folder that contains data/qutrit_table.tsv; how-we-built-it/code/parse_table.py makes that file from the saved table page. Then:

    python3 how-we-built-it/code/make_all.py
    python3 how-we-built-it/code/make_lengthened.py
    python3 how-we-built-it/code/make_all2.py

The commands write $RUN/attempts/small-cases/result/S_33_1_31_24.txt among other files (the result/ folder must exist first). how-we-built-it/LENS_REPRODUCE.md has the details.
