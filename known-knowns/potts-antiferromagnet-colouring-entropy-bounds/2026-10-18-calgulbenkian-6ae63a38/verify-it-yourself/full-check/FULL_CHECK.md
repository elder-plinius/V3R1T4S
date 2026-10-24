# Optional full check: the panel's own independent C checker (about about 38 minutes on 27 threads)

What it adds. The quick check (../run_checks.sh) reads the shipped vector pair (v, y) and trusts that y is the transfer matrix applied
to v. This check recomputes y itself. It lifts v to every proper 4-colouring of the cycle C_18 and applies the FULL transfer matrix of the
definition (all 387420492 states, no quotient and no equitable-partition assumption): for each of the 451929 orbit representatives it
enumerates every compatible colouring exhaustively and sums v in exact integer arithmetic. Then it compares its own y with the shipped y
entry by entry, and computes the Collatz-Wielandt ratios and the bound with exact rational arithmetic.

Credit. mycw.c and analyse.py were written by the panel's reproduce skeptic (a Claude Code subagent, started fresh, given only the claim
folder, from the definition and before reading the author's code). They are copied here unchanged from the panel's working folder. The
expected output below is that skeptic's own run, quoted from panel/reproduce.md.

Needs: a C compiler for a 64-bit machine with unsigned __int128 and POSIX threads (gcc or clang), python3 for the last step.
Time: about 38 minutes on 27 threads (panel run). More threads shorten it; the result does not depend on the thread count (exact integer arithmetic).
Memory: not recorded by the panel. The program keeps a dense table of the lifted vector, so allow a few gigabytes (estimate, not measured).
The compile flags below are the ones we used to build it on a Mac and to run it on a width-8 certificate; the panel did not record its own flags.

Commands, from the package folder:

```sh
cd verify-it-yourself/full-check
python3 ../reassemble.py ../../object/PARTS.txt 4cert.bin
cc -O3 -pthread -o mycw mycw.c
./mycw 4 18 4cert.bin out.txt 27
python3 -I analyse.py out.txt 18 2.33606820555777
```

Arguments of mycw: the number of colours, the cycle length, the certificate file, the output file, the number of threads.
Arguments of analyse.py: the output file, the cycle length, the published bound to compare with.

Expected: the panel skeptic's own run, quoted verbatim from panel/reproduce.md (its file names differ from the commands above):

```
Command: ./mycw 4 18 q4_18.bin out_q4_18.txt 27   (concatenated certificate; 27 threads; wall time about 38 minutes)
Program log (progress lines removed):
    q=4 m=18 proper RGS count N=16142521
    orbits found by own enumeration: 451929 ; orbits in certificate: 451929
    orbits where own S != certificate y: 0

Command: python -I analyse.py out_q4_18.txt 18 2.33606820555777
Output (also in rep_ws/skeptic/output.txt):
    orbits: 451929 ids contiguous: True
    all v > 0: True  min v bits: 221  max v bits: 224
    argmax orbit 330432 argmin orbit 0
    C_hi = max (Cv)_i/v_i exactly = 10308110743659294181213305847653233613093647112644826588240099466940532396 / 2401410699841922024469331521067244028233344603985234653291323144461
    C_hi (decimal 40 digits): 4292523.0342056223587157719556590059728848958444
    C_lo = min ratio (decimal 40): 4292523.0342056223587157719556590059728848958444
    C_hi - C_lo (float): 2.6071006129789558e-45  relative: 6.073585609684277e-52
    W <= C_hi^(1/m) <= (outward rounded UP, 40 decimals): 2.3360602265554583581403491124455588569046
       (rounded down, 40 decimals): 2.3360602265554583581403491124455588569045
    outward rounded UP at 20 decimals: 2.33606022655545835815
    published bound: 2.33606820555777  improvement (published - rounded-up claim) = 7.97900231164186e-06  >= 1e-9 : True
    exact check, margin as Fraction >= 1e-9: True
```

Pass means: the line "orbits where own S != certificate y: 0", "all v > 0: True", and the final line "exact check, margin as Fraction >= 1e-9: True".
The upward 20-decimal rounding printed by analyse.py is the value this package states: 2.33606022655545835815.
