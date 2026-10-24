# Run it yourself (fresh shell, from this folder)

1. `sh verify-it-yourself/run_checks.sh`
   Expected output ends with:
       entry: OK at step 0
       symbolic closure for m >= M0: OK M0 = 0
       exact closure and non-palindromicity for 0 <= m <= 200 (+ special m []): OK
       CLAIM CHECK: PASS
       PASS
2. Optional, independent C simulation of the real orbit:
       gcc -O2 -o lo verify-it-yourself/longorbit.c && ./lo object/b13.tpl 100000
   Expected: RESULT base=13 steps=100000 final_len=30134 template_checks=100001 mismatches=0 palindromes=0

How to rebuild the object: see how-we-built-it/COMMANDS.md (exterior automaton -> exterior path -> seeded interior
search -> template extraction).
