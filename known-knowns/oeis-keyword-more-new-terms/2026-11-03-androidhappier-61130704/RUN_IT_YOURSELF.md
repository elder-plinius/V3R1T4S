# Run it yourself (fresh shell, from this folder)

## 1. Quick check (about 30 seconds, Python 3 standard library; C step skipped without a compiler)
    sh verify-it-yourself/run_checks.sh            # last line: PASS

## 2. Both search programs (gcc, Go >= 1.20)
    gcc -O2 -o pA how-we-built-it/pA_c/medmed.c && ./pA 1 12
    (cd how-we-built-it/pB_go && go build -o ../../pB main.go) && ./pB 1 12
    python3 how-we-built-it/pC_py/brute.py 10
Expected (pA and pB): 1 1 / 2 0 / 3 3 / 4 6 / 5 30 / 6 96 / 7 461 / 8 2000 / 9 10727 / 10 57092 / 11 342348 / 12 2092816.
pC prints the first 10 lines.

## 3. Rebuild the object
    printf 'A361864(12) = %s\n' "$(./pA 12 12 | awk '{print $2}')" > VALUE.txt   # same bytes as object/VALUE.txt
