# Run it yourself

From this folder, in a fresh shell, with a Python 3 that has python-flint 0.9.0 (`pip install python-flint==0.9.0`):

    PYTHON=python3 sh verify-it-yourself/run_checks.sh

(`PYTHON` may be any interpreter with python-flint; without it the script tries python3, python, `py -3` and a nearby
.venv, and says clearly if none can import flint.) Expected last lines (about 160 s on a 2026 desktop, one thread,
about 0.85 GB):

    RESULT: |lambda - mu| <= [4.5490e-843 +/- ...]  ->  D = 842 certified decimals; isolation/counting ok = True
    certified: |lambda_2 - mu| <= [4.54904e-843 +/- ...], D = 842; endpoints match object/C83_enclosure.txt; Nisoli centre agrees
    PASS

The vector is stored in four parts only to keep files under 1 MB; join them first for the commands below
(`cat object/v_N2800.part1.txt object/v_N2800.part2.txt object/v_N2800.part3.txt object/v_N2800.part4.txt > v_N2800.txt`;
sha256 cc6beb453558cfead1420c2d3cb5f4c54f83106c8417129e2bd09e08be17882a).

The same certificate at a second working precision (4300 bits, J = 12320, Q2 = 96; expected D = 842, radius about
4.4298e-843, about 3 min):

    python3 how-we-built-it/code/gkw_cert.py certify v_N2800.txt object/mu_N2800.txt 80 4300 12320 0.01 0.2 96 256 L2.json

Independent eigenvalue count of the 80 x 80 section by Gershgorin discs (expected `GERSHGORIN_COUNT PASS`, about 1 min):

    python3 how-we-built-it/code/gershgorin_count.py 80 3900 object/mu_N2800.txt 0.01 0.2

Exact centre checks against Nisoli's 175-digit centre and the OEIS A038517 b-file need those reference files, which are
not copied here (third-party data); `how-we-built-it/code/refs.py` and `compare.py` show how they were used, and
`how-we-built-it/logs/compare_L1.txt` / `compare_L2.txt` are their outputs. The Nisoli comparison alone is also done by
run_checks.sh, from the-record-we-beat/nisoli_centre_175.txt.

Rebuild the object (the approximate eigenvector and the proposed centre; midpoint arithmetic, proves nothing). The run
used a chain of warm starts: N = 2000 (an earlier run of the same route) -> N = 2400 (40 cycles, 3400 bits, about 3.6
min with 14 threads, 2.8 GB) -> N = 2800 (40 cycles, 3900 bits, about 5.7 min, 4.2 GB). The N = 2000 and N = 2400
vectors are not included; a cold start from e_0 should need roughly 190 cycles at about 4.8 decimals per cycle (an
estimate that was not run):

    python3 how-we-built-it/code/gkw_cert.py eigvec 2800 3900 190 v_rebuilt.txt - 14 mu_rebuilt.txt

then certify `v_rebuilt.txt` with `mu_rebuilt.txt` as above. The proof, with every constant traced to the code, is
object/PROOF.md. object/mu_N2800.txt is the centre: the Rayleigh quotient of the N = 2800 vector (1154 significant
digits), rounded to an exact binary number by the certifier; PROOF.md Remark 0 explains why its origin does not matter.
