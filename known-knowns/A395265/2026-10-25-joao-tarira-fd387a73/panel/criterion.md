# CRITERION

context: comparison of the two saved verify_run.txt PASS logs and the witness difference counts to the A395265 definition, while assembling this package

a(n) = D means some n-mark 5-Golomb ruler has diameter D, and none has a smaller positive diameter. The witnesses give the first half for n = 20 and n = 21. The saved right-to-left searches give NONE for every smaller diameter that still has to be ruled out once a(19) = 50 and a(20) = 56 are known: 51 through 55, and 57 through 61. Diameters at or below the previous term are impossible because the function is strictly increasing on this initial segment (the published values, recomputed in the a(20) log, increase at every step).

Both search directions use the same two pruning rules. The a(20) log also recomputes a(3) through a(19) and matches the b-file. That is support for the rules, not an independent derivation of them.

confirmed_scope: A395265(20) = 56 and A395265(21) = 62, the minimum diameters of a 20-mark and a 21-mark 5-Golomb ruler, with explicit witnesses of those diameters and saved independent exhaustive searches reporting none of diameter 51 through 55 or 57 through 61, past the OEIS b-file ending at a(19) = 50.

pass: true
