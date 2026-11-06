# Optional full check: the panel's own independent C checker (about about 25 minutes on 28 threads)

What it adds. The quick check (../run_checks.sh) reads the shipped vector pair (v, y) and trusts that y is the transfer matrix applied
to v. This check recomputes y itself. It lifts v to every proper 5-colouring of the cycle C_14 and applies the FULL transfer matrix of the
definition (all 268435460 states, no quotient and no equitable-partition assumption): for each of the 81433 orbit representatives it
enumerates every compatible colouring exhaustively and sums v in exact integer arithmetic. Then it compares its own y with the shipped y
entry by entry, and computes the Collatz-Wielandt ratios and the bound with exact rational arithmetic.

Credit. mycw.c and analyse.py were written by the panel's reproduce skeptic (a Claude Code subagent, started fresh, given only the claim
folder, from the definition and before reading the author's code). They are copied here unchanged from the panel's working folder. The
expected output below is that skeptic's own run, quoted from panel/reproduce.md.

Needs: a C compiler for a 64-bit machine with unsigned __int128 and POSIX threads (gcc or clang), python3 for the last step.
Time: about 25 minutes on 28 threads (panel run). More threads shorten it; the result does not depend on the thread count (exact integer arithmetic).
Memory: not recorded by the panel. The program keeps a dense table of the lifted vector, so allow a few gigabytes (estimate, not measured).
The compile flags below are the ones we used to build it on a Mac and to run it on a width-8 certificate; the panel did not record its own flags.

Commands, from the package folder:

```sh
cd verify-it-yourself/full-check
python3 ../reassemble.py ../../object/PARTS.txt 5cert.bin
cc -O3 -pthread -o mycw mycw.c
./mycw 5 14 5cert.bin out.txt 28
python3 -I analyse.py out.txt 14 3.250407145038276
```

Arguments of mycw: the number of colours, the cycle length, the certificate file, the output file, the number of threads.
Arguments of analyse.py: the output file, the cycle length, the published bound to compare with.

Expected: the panel skeptic's own run, quoted verbatim from panel/reproduce.md (its file names differ from the commands above):

```
Command: ./mycw 5 14 q5_14.bin out_q5_14.txt 28   (concatenated certificate; 28 threads; wall time about 25 minutes)
Program log (progress lines removed):
    q=5 m=14 proper RGS count N=2238328
    orbits found by own enumeration: 81433 ; orbits in certificate: 81433
    orbits where own S != certificate y: 0

Command: python -I analyse.py out_q5_14.txt 14 3.250407145038276
Output (also in rep_ws/skeptic/output.txt):
    orbits: 81433 ids contiguous: True
    all v > 0: True  min v bits: 223  max v bits: 224
    argmax orbit 80146 argmin orbit 74525
    C_hi = max (Cv)_i/v_i exactly = 70527689875082357677159322222225331322003283177851297924316568940791733691 / 4799926535208162933632183472881474187716556614045961155232665021516
    C_hi (decimal 40 digits): 14693493.6103191247992568599424794513959236209793
    C_lo = min ratio (decimal 40): 14693493.6103191247992568599424794513959236209793
    C_hi - C_lo (float): 1.6431131415882124e-60  relative: 1.1182589962364477e-67
    W <= C_hi^(1/m) <= (outward rounded UP, 40 decimals): 3.2504052058785496850598045891913500783901
       (rounded down, 40 decimals): 3.2504052058785496850598045891913500783900
    outward rounded UP at 20 decimals: 3.25040520587854968506
    published bound: 3.250407145038276  improvement (published - rounded-up claim) = 1.93915972631494e-06  >= 1e-9 : True
    exact check, margin as Fraction >= 1e-9: True
```

Pass means: the line "orbits where own S != certificate y: 0", "all v > 0: True", and the final line "exact check, margin as Fraction >= 1e-9: True".
The upward 20-decimal rounding printed by analyse.py is the value this package states: 3.25040520587854968506.
