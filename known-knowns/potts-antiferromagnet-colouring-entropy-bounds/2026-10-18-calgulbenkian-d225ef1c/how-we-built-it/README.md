# How the object was built (contributor text, unverified)

The object was produced by Argon, an AI search agent (Gemini) working for the contributor calgulbenkian, on 2026-10-18. This folder holds
the search code and the pre-registration copied from Argon's read-only snapshot (taken 2026-10-18T17:35:35Z), nothing else from it.
No binaries, matrices or other certificates are copied. The package's own checkers do not use any of this code.

Files:
- potts_kink_cert.c: the program that wrote the certificate (matrix-free, site-by-site transfer on the S_q x D_m orbit quotient; a
  precision ladder of 35 double iterations, 50 native 128-bit iterations, then 65 to 90 exact 256-bit iterations, an exact 256-bit
  product y = C v, and a 512-bit cross-multiplied Collatz-Wielandt check). Its own description is section 2.1 of RESULTS_section2.md.
- potts_transfer.c: builds the explicit quotient matrix for small widths. It is not needed for the wide certificate; it is kept because the
  snapshot's RESULTS.md names it among the programs behind the small-width tables.
- PREREG.md: the pre-registration for the whole statistical-mechanics attack (it also covers a second target, the King's graph hard-core
  entropy, which has nothing to do with this package). Target 2 is this one. It declares null_test: not needed (exact algebra).
- RESULTS_section2.md: section 2 of the snapshot's results/RESULTS.md (the Potts target), copied unchanged.

Commands as the snapshot documents them. The usage lines are printed by the programs themselves:

```sh
cc -O2 -o potts_kink_cert potts_kink_cert.c -lm
./potts_kink_cert {q} {mode} {m} {n_iters_u256} {save_cert_path}        # mode 0 = cycle (cylinder), 1 = open strip
./potts_kink_cert 5 0 14 80 q5_cyl_14_cert.bin       # the shipped object's case, with the default 80 iterations
```

Where the commands are NOT recorded: the snapshot has no command log, no compile flags, no run times and no memory figures for the width
14 run, and it does not say which iteration count (within 65 to 90) produced the shipped file. The compile line above is ours. We
compiled the program that way and ran it for q = 4, m = 8 with 80 iterations: it wrote a certificate that the panel's independent
program (mycw.c, see ../verify-it-yourself/full-check/) accepts with y = C v exact (34 of 34 orbits), but the file is not byte-identical to the
shipped width-8 example, so the shipped bytes cannot be regenerated from the recorded information. Any valid certificate gives a valid
bound; the shipped one is checked on its own by the checkers in ../verify-it-yourself/.

Two cautions about the snapshot's text, both already recorded in the claim folder:
1. RESULTS_section2.md, Table A, row q = 4, open strip m = 3, lists 16.352349955308334315... That entry is wrong (a brute-force count and the
   snapshot's own certificate file for that case give 16.34846922834953...). The claim does not depend on it: it concerns an open strip of width 3,
   and this package uses only the cycle C_14.
2. Section 2.4 of RESULTS_section2.md cites the upper-bound inequality as "Theorem 2.2" of Lundow and Markstrom. That label is wrong: the
   inequality is equation (6) of their paper (Section 4). The text is copied unchanged.
