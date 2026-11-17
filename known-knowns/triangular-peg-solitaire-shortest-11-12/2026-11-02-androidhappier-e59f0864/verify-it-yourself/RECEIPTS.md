# Revised package check, 2026-11-07

Ran `sh verify-it-yourself/run_checks.sh` on Windows with Git Bash, Python 3.12 and a C compiler:

```text
== 1. object hash matches INDEX.csv
object sha256 e59f0864e5e9fc3034f2ee6815a92a2fa05775d4b1e2f6f3515082553a6ef6f4 ok
== 2. standalone checker (explicit start vacancy a2): 22 moves, 64 jumps, one peg at j11, no mergeable moves
ok   check_peg T11: check_peg: n=11 vacancy=a2 moves=22 jumps=64 pegs_left=1 finish=j11 merges=0 VALID
== 3. second simulator (Python, vacancy inferred from the first jump)
ok   pegcheck T11: n=11 start_vacancy=a2 pegs_left=1 finish=j11 jumps=64 moves=22 VALID
== 4. third simulator (C, cube coordinates)
ok   pegsim2 T11: n=11 jumps=64 moves=22 pegs_left=1 VALID
== 5. Bell calibration skipped: published move lists are not included
summary: Triangle(11) a2 -> j11 in 22 moves, so A127500(11) <= 22 (published upper bound 28)
PASS
```

# Receipts

The following is historical output from the original package on 2026-11-02. Its calibration fixtures have since been removed and step 5 is skipped by the revised script; this is not a receipt for the revised script.

# Receipts: real output of sh verify-it-yourself/run_checks.sh (2026-11-02, run from this folder)

```
== 1. object hash matches INDEX.csv
object sha256 e59f0864e5e9fc3034f2ee6815a92a2fa05775d4b1e2f6f3515082553a6ef6f4 ok
== 2. standalone checker (explicit start vacancy a2): 22 moves, 64 jumps, one peg at j11, no mergeable moves
ok   check_peg T11: check_peg: n=11 vacancy=a2 moves=22 jumps=64 pegs_left=1 finish=j11 merges=0 VALID
== 3. second simulator (Python, vacancy inferred from the first jump)
ok   pegcheck T11: n=11 start_vacancy=a2 pegs_left=1 finish=j11 jumps=64 moves=22 VALID
== 4. third simulator (C, cube coordinates)
ok   pegsim2 T11: n=11 jumps=64 moves=22 pegs_left=1 VALID
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
summary: Triangle(11) a2 -> j11 in 22 moves, so A127500(11) <= 22 (published upper bound 28)
PASS
```

## Rebuild check (RUN_IT_YOURSELF.md section 2), 2026-11-02 while packaging

`BEAM_V=2 ./beam3 11 200000 2 45` (gcc -O2 -march=native) took 150 s on one core. Its stdout ended with
"SOLVED n=11 moves=22" and "start a2"; its last line is byte-identical to object/T11_22moves.txt (`cmp` silent), and
its stderr is identical to how-we-built-it/beam_T11_B200000_W2_V2.log.
