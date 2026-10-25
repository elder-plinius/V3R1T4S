# REPRODUCE

context: saved logs results/2026-10-20-a390087-a8/verify_run.txt, results/2026-10-20-a390087-a8/vf_L16.txt, results/2026-10-20-a390087-a8/vf_L18plus.txt, results/2026-10-21-a390087-a9/verify_run.txt, results/2026-10-21-a390087-a9/vf2_L18.txt, and results/2026-10-21-a390087-a9/vf2_L20plus.txt, re-read while assembling this package, plus a fresh subset enumeration of both witnesses by verify-it-yourself/check.py

Witnesses in object/terms.json:

- length 16, largest absolute value 77, sum 0, no nonempty proper subset sums to 0. This is the a(8) = 39 witness.
- length 18, largest absolute value 95, sum 0, no nonempty proper subset sums to 0. This is the a(9) = 48 witness.

The fresh checker repeats that subset enumeration.

Saved exhaustive record, re-read and counted, not re-run for this package:

- verify_run.txt for a(8) ends with PASS. It includes NONE for length 16 at every odd magnitude from 31 through 75, and FOUND at 77. It also reproduces published a(5) = 16, a(6) = 23, and a(7) = 30.
- vf_L16.txt is 23 lines, all NONE, magnitudes 31 through 75, length 16.
- vf_L18plus.txt is 132 lines, all NONE, lengths 18, 20, ..., 38, each from magnitude 2*length-1 through 77. A trailing timing line is not a result row.
- verify_run.txt for a(9) ends with PASS. It includes NONE for length 18 at magnitudes 35 through 93, and FOUND at 95.
- vf2_L18.txt has 30 NONE lines for length 18 at magnitudes 35 through 93, and one FOUND line at magnitude 95.
- vf2_L20plus.txt has 225 lines, all NONE, lengths 20, 22, ..., 48, each from magnitude 2*length-1 through 95.

Together with the published a(7) = 30 (so A390085 is already 7 at k = 30) and monotonicity in k, this is A390085(31)..(38) = 7, (39)..(47) = 8, and (48) = 9.

pass: true
