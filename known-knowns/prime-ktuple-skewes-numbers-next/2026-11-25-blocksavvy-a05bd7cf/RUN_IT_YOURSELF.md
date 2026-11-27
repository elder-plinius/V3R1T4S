# Run it yourself (fresh shell, from this package folder)

## 1. Standalone check (python3 standard library, ~25 s)
    sh verify-it-yourself/run_checks.sh          # last line PASS (see verify-it-yourself/RECEIPTS.md)

## 2. Full exhaustive recount (C compiler; python3 with numpy, mpmath, python-flint >= 0.6, sympy)
    mkdir -p work && cc -O3 -o work/sexyB how-we-built-it/code/sexyB.c -lpthread -lm
    work/sexyB count 349024813056 4 work/B.bin                     # total_pairs=1416032531
    SEXYB=work/sexyB python3 how-we-built-it/code/postB.py work/B.bin 100663296 349100000000
        # FIRST VIOLATION q=349018493647 pi6(q)=1416008996 C*Li2(q)=1416008995.52083626635901
    cc -O3 -o work/sexyA how-we-built-it/code/sexyA.c -lpthread -lm
    python3 how-we-built-it/code/ltable.py 27738 work/L.bin 4
    work/sexyA 27738 work/L.bin work/A.bin 4 100000000 1000000000 10000000000 100000000000 > work/A.txt
    python3 how-we-built-it/code/post.py work/A.bin work/L.bin work/A.txt 1e8     # flagged_blocks=1 [27737]
    python3 how-we-built-it/code/exact_block.py 349012230144 349024813056 1415985401   # FIRST CROSSING p=349018493647
    python3 how-we-built-it/code/small2.py 100663296      # exact range; twins 1369391, cousins 5206837 reproduced
    python3 how-we-built-it/code/exact_block_conv.py 349012230144 349024813056 1415985401   # exclusive-count variant 349018493981

Expected outputs: how-we-built-it/outputs/. Sieve A and sieve B are separately written (6k+-1 bitsets with a chord bound in Arb;
odd-only Eratosthenes with a monotone bound in mpmath) and agree on all 79473 blocks to 1.0e12 (outputs/compare_A_B_1e12.txt).

## Rebuilding the object
object/sexy_skewes.json and object/block_counts_0_to_27737.txt are the outputs of steps 2 (sieve A block counts, identical to sieve B).
