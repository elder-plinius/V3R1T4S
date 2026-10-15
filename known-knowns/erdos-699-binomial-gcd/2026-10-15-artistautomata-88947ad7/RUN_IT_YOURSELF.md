# Run it yourself (from this folder, fresh shell)

Quick check of the certificate (Python 3 standard library, about 1 minute):

    sh verify-it-yourself/run_checks.sh          # last line: PASS

It checks the definition for n <= 200 by exact gcd, that object/seg699_chunk_summaries.txt covers [0, 10^9] with
candidates=0 and overflow=0 in every chunk, and recomputes every chunk's case count with its own sieve.

Rebuild the object (the full scan, about 4.5 h on 4 cores; gcc):

    cd how-we-built-it && mkdir -p code chunks && gcc -O2 -o code/seg699 seg699.c
    for K in 0 1 2 3; do sh run_chunks.sh $K 4 & done; wait
    ./code/seg699 1000000000 1000000000 0 > chunks/s_1000000000_1000000000.txt
    python3 coverage.py                          # last line: COVERAGE_COMPLETE_4_TO_1e9
    for f in $(ls chunks/s_*.txt | sort -t_ -k2 -n); do grep DONE $f; done | diff - ../object/seg699_chunk_summaries.txt

Expected: no diff output. Any single chunk: ./code/seg699 A B 0 reproduces its line in about a minute.
Cross-checks: fast699.c (gcc -O2 ... -lm; ./fast699 A B 0 gives nontrivial_i equal to seg699's cases),
sample_windows.py, third699.py and compare.py (expect paths ./code/seg699 and ./code/fast699).
