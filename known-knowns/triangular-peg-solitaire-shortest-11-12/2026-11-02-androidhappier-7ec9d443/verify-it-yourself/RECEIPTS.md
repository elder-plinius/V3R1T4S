# Receipts (real output, 2026-11-02T18:24:46Z)

## sh verify-it-yourself/run_checks.sh (Python 3.13.5, cc (Debian 14.2.0-19) 14.2.0)
```
== 1. object: solution hash vs INDEX.csv, and object/BOUND.txt recomputed from the solution
object/T12_25moves.txt sha256 7ec9d443efe7b234fb31c6d427820f067f3815e99dea8750a547bc1b53a6c78b (INDEX.csv: match)
object/BOUND.txt matches the values recomputed from the solution
bound a(12) <= 25, published 29: strictly better
ok
== 2. standalone checker (explicit start vacancy a3): 25 moves, 76 jumps, one peg at j12, no mergeable moves
ok   check_peg T12: check_peg: n=12 vacancy=a3 moves=25 jumps=76 pegs_left=1 finish=j12 merges=0 VALID
== 3. second simulator (Python, vacancy inferred from the first jump)
ok   pegcheck T12: n=12 start_vacancy=a3 pegs_left=1 finish=j12 jumps=76 moves=25 VALID
== 4. third simulator (C, cube coordinates)
ok   pegsim2 T12: n=12 jumps=76 moves=25 pegs_left=1 VALID
== 5. calibration on G. I. Bell's published solutions (expect VALID with his move counts) and two corrupted T11 orders (expect ILLEGAL)
ok   check_peg bell_T9_16: check_peg: n=9 vacancy=a2 moves=16 jumps=43 pegs_left=1 finish=i9 merges=0 VALID
ok   pegcheck bell_T9_16: n=9 start_vacancy=a2 pegs_left=1 finish=i9 jumps=43 moves=16 VALID
ok   pegsim2 bell_T9_16: n=9 jumps=43 moves=16 pegs_left=1 VALID
ok   check_peg bell_T10_18: check_peg: n=10 vacancy=a3 moves=18 jumps=53 pegs_left=1 finish=c6 merges=0 VALID
ok   pegcheck bell_T10_18: n=10 start_vacancy=a3 pegs_left=1 finish=c6 jumps=53 moves=18 VALID
ok   pegsim2 bell_T10_18: n=10 jumps=53 moves=18 pegs_left=1 VALID
ok   check_peg bell_T11_28: check_peg: n=11 vacancy=a4 moves=28 jumps=64 pegs_left=1 finish=a1 merges=0 VALID
ok   pegcheck bell_T11_28: n=11 start_vacancy=a4 pegs_left=1 finish=a1 jumps=64 moves=28 VALID
ok   pegsim2 bell_T11_28: n=11 jumps=64 moves=28 pegs_left=1 VALID
ok   check_peg bell_T12_29: check_peg: n=12 vacancy=e11 moves=29 jumps=76 pegs_left=1 finish=a3 merges=0 VALID
ok   pegcheck bell_T12_29: n=12 start_vacancy=e11 pegs_left=1 finish=a3 jumps=76 moves=29 VALID
ok   pegsim2 bell_T12_29: n=12 jumps=76 moves=29 pegs_left=1 VALID
ok   check_peg neg_T11_swapped: check_peg: n=11 vacancy=a4 ILLEGAL (move 25: illegal jump b2-d4)
ok   pegcheck neg_T11_swapped: ILLEGAL illegal jump b2-d4
ok   pegsim2 neg_T11_swapped: ILLEGAL jump 26
ok   check_peg neg_T11_order: check_peg: n=11 vacancy=a4 ILLEGAL (move 1: illegal jump a8-a6)
ok   pegcheck neg_T11_order: ILLEGAL illegal jump a6-a4
ok   pegsim2 neg_T11_order: ILLEGAL jump 2
summary: Triangle(12) a3 -> j12 in 25 moves, so A127500(12) <= 25 (published upper bound 29)
PASS
```

## Rebuild of the object (RUN_IT_YOURSELF.md step 3, 2026-11-02T18:24:59Z, gcc 14.2.0, one core)
```
$ gcc -O2 -march=native -o beam3 how-we-built-it/beam3.c
$ time (BEAM_V=2 ./beam3 12 200000 3 45 > found.txt 2> found.log)
real	3m52.141s
$ tail -1 found.txt | cmp - object/T12_25moves.txt && echo identical
identical
$ cmp found.log how-we-built-it/logs/T12_B200000_W3_V2.log && cmp found.txt how-we-built-it/logs/T12_B200000_W3_V2.txt && echo identical
identical
```
