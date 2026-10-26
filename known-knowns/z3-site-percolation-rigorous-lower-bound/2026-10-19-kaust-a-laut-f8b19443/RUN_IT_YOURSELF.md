# Run it yourself (from this folder, fresh shell)

Fast exact checks (Python 3.8+, standard library; about half a minute):

    sh verify-it-yourself/run_checks.sh          # last line: PASS

Rebuild the enumerator and reproduce the small tables (Go; about a minute on 6 cores):

    GO=1 sh verify-it-yourself/run_checks.sh     # last line: PASS (go: N = 3..14 and 16 reproduced byte for byte)

Full reproduction of the certificate table (Go; about 2.6 hours on 6 cores, a few MB of memory):

    FULL=1 sh verify-it-yourself/run_checks.sh
    # last line: PASS (full: N = 3..14, 16, 18 and 20 reproduced byte for byte; K_20(263376/10^6) < 1 on the regenerated table)

WORKERS=k sets the number of worker goroutines (default 6). The tables do not depend on it: they are integer sums.

By hand, from a copy of object/ (its layout matches the paths in object/PROOF.md, object/REPRODUCE.md and
object/result/bound.json):

    cd code/par && go build -o par.exe . && cd ../..
    ./code/par/par.exe 16 6 > p16.txt && cmp p16.txt outputs/p16.txt          # about 30 s
    ./code/par/par.exe 20 6 > p20.txt && cmp p20.txt outputs/p20.txt          # about 2.5 hours
    python3 code/verify_cert.py p20.txt 263376

Expected from verify_cert.py:

    N = 20, sum of c_f = 14334995983614
    f_max = 23: K_N is increasing on [0, 21/44] = [0, 0.477273]; (j+1)/10^6 inside: True
    K_N(263376/10^6) = 0.999971526024  ->  PASS: p_c >= 263376/10^6
    K_N(263377/10^6) = 1.000041779030  ->  fails (p* is maximal on the grid)
    sanity 1/5 (proven bound; must pass): K = 0.005547
    sanity 0.3116 (numerical p_c; must fail): K = 21.417580

The output format of par.exe is "TOTAL N a_N" (the number of N-step neighbour-avoiding walks) and
"EXT N f:c_f ..." (c_f = the sum, over walks whose forced-closed set has f sites, of the number of valid
extensions). Its arguments are N and the number of workers. code/kcheck.py object/outputs/p20.txt reruns the exact
threshold search (object/outputs/k20.txt).

How the object was built: object/PROOF.md is the argument (definitions, Lemmas 0-4, the theorem).
object/code/par/main.go enumerates the sign-flip orbit representatives of all N-step neighbour-avoiding walks,
maintaining the forced-closed set incrementally, and weights each representative by its orbit size 2^|axes used|
(PROOF.md Lemma 4). The 216 canonical 3-step prefixes are split among the workers.
