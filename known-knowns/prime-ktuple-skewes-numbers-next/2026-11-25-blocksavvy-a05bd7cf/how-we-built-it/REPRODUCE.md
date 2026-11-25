# Reproduce (fresh shell; needs cc, python3 with numpy, python-flint >= 0.6, mpmath, sympy)
All commands from this claim/ folder. Times measured on an 8-core box under load.

## 1. Fast check of the crossing (~2 s)
    python3 code/verify_claim.py result            # last line PASS
    python3 code/tamper_controls.py                # 400 tampered claims all rejected; last line RESULT: PASS (~10 min)

## 2. Full exhaustive recount, sieve B (odd-only Eratosthenes) + mpmath monotone bound (~9 min wall on 6 threads, 1e12)
    mkdir -p work && cc -O3 -o work/sexyB code/sexyB.c -lpthread -lm
    work/sexyB count 349024813056 6 work/B.bin            # 5325696 sub-blocks of 65536; total_pairs=1416032531
    SEXYB=work/sexyB python3 code/postB.py work/B.bin 100663296 349100000000   # expects FIRST VIOLATION q=349018493647 pi6(q)=1416008996

## 3. Full exhaustive recount, sieve A (6k+-1 bitsets, presieve 5..17) + Arb chord bound (~2.5 min wall, 1e12)
    cc -O3 -o work/sexyA code/sexyA.c -lpthread -lm
    python3 code/ltable.py 27738 work/L.bin 4             # Arb lower bounds of C*Li2 at block boundaries
    work/sexyA 27738 work/L.bin work/A.bin 6 100000000 1000000000 10000000000 100000000000 > work/A.txt
    python3 code/post.py work/A.bin work/L.bin work/A.txt 1e8   # expects flagged_blocks=1 [27737]: every block 8..27736 has positive chord margin (smallest 143.296, block 27736)
    python3 code/exact_block.py 349012230144 349024813056 1415985401   # FIRST CROSSING p=349018493647

## 4. Small range (n <= 100663296, where chord/monotone bounds are not used) and calibration
    python3 code/small2.py 100663296     # [0,2] -> 1369391 (known), [0,4] -> 5206837 (known), [0,6] -> None; ~3 min

## 5. Constant
    python3 code/constant.py             # C2 ball, radius < 6e-48

Expected outputs are in outputs/.
