# REPRODUCE

context: saved logs results/2026-10-23-a395265-a20/verify_run.txt and results/2026-10-24-a395265-a21/verify_run.txt, re-read while assembling this package, plus a fresh difference count of both witnesses by verify-it-yourself/check.py

The fresh checker confirms the witnesses in object/rulers.json:

- 0, 1, 2, 3, 8, 11, 14, 16, 20, 24, 29, 31, 36, 40, 43, 46, 50, 54, 55, 56. Twenty marks, diameter 56, maximum multiplicity 5.
- 0, 1, 2, 3, 8, 12, 17, 19, 23, 27, 30, 35, 37, 40, 43, 49, 52, 56, 60, 61, 62. Twenty-one marks, diameter 62, maximum multiplicity 5.

Saved exhaustive record:

- results/2026-10-23-a395265-a20/verify_run.txt recomputes a(3) through a(20) with the right-to-left program, prints NONE for n = 20 at diameters 50 through 55 (the diameter-55 line is `n=20 D=55: NONE (2795585430 nodes)`), then `a(20) = 56`, `a(1..19) match OEIS`, and `PASS: A395265 a(20) = 56`.
- results/2026-10-24-a395265-a21/verify_run.txt checks the 21-mark witness and then runs the right-to-left program on diameters 57 through 61, every slice NONE, and ends with `PASS: A395265 a(21) = 62`.

The fresh checker does not repeat those NONE searches.

pass: true
