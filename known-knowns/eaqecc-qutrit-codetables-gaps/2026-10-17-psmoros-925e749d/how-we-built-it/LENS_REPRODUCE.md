# How the object was built (lens small-cases, run 2026-10-17-1119)

The builder code is in code/. RUN means the run folder, which holds data/qutrit_table.tsv (made from the table page by code/parse_table.py).

1. `python3 code/make_all.py`: [[n,1,n-1;n-1-T]] codes, at most 1 zero per logical word, with T = 2..4 classes.
2. `python3 code/make_lengthened.py`: the T = 4 family lengthened by |0> qutrits.
3. `python3 code/make_all2.py`: the upgrade to d = n-2, at most 2 zeros per logical word. It writes S_33_1_31_24.txt.

- The construction (contributor text, unverified): split the n positions into classes. The Z parts of the two logical vectors take, on each class, one projective point of PG(1,3). The radical R = R0 x 0 is a direct sum of small X-type pieces Y_t, each orthogonal to the all-ones vector on its class. The X parts are chosen so that every word outside R has at most 2 zeros.
- The lens verified the result with code/eacheck.py, exhaustively, and with a separate C checker.
- The run's PREREG (frozen before any attack) is PREREG.md. It says no null test is needed, because the claim is an explicit object checked by a deterministic exact checker.
