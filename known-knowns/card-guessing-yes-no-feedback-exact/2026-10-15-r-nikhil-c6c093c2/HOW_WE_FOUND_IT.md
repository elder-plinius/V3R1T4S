# How we found it (contributor text, unverified)

The target asks for the first exact values of P+_{2,n}, the optimal expected number of correct guesses with yes/no
feedback for a deck with two copies of each of n labels, for n = 11..16, with Bellman certificates. Luo's 2026 paper
(arXiv:2609.25062, Appendix A) gives the sufficient state (per label: remaining undetermined copies r_i and
forbidden-position count f_i), the inclusion-exclusion count C(r,f) of consistent arrangements, and the backward
recursion for V+. We implemented that recursion from the paper in C++ with exact integers: the value times the count,
W = C V+, is an integer, so no fractions are needed until the end; counts are computed with GMP because intermediate
inclusion-exclusion terms exceed 128 bits even though the results fit. Labels are exchangeable, and the forbidden
positions of exhausted labels matter only through their total, which keeps the n = 16 table at 18.6 million states.
The solver enumerates the reachable states layer by layer (by the number of remaining guesses), evaluates them
backwards, and streams the table out as gzip text, so a verifier needs only two layers in memory.

Before trusting it we checked it against things that do not depend on the recursion: a brute force over all
arrangements of tiny decks (posterior sets as bitmasks, every label guessable at every step), Luo's closed form for
two labels, the Diaconis-Graham formula for one copy per label, the published four-decimal values for n = 2..10, and
the 1981 Diaconis-Graham / Gatto values 4.26, 5.47 and 6.63 for the (3,3), (4,4) and (5,5) decks (the Monthly paper's
Table 1 prints 6.65 for the last one; the 1981 source and our exact value give 6.63). A second solver, written
independently by a different language model on the same machine before this run, had obtained the same fifteen
values; agreement of two separately written implementations was a pre-registered requirement. An independent
streaming checker (Python, standard library) then verified every state of every certificate, and mutation tests
confirmed that it rejects corrupted values, missing states and wrong claims. The published four-decimal entry for n = 7
(3.0323) turned out to be the truncation rather than the rounding of the exact value; every other entry rounds
correctly.

What failed or was left: the greedy and linear-strategy columns of the Monthly paper's Table 2 could not be reproduced
exactly because their tie-breaking rule is unstated (the optimal column matches exactly); the persistence conjecture
of Diaconis and Graham (1981) held on every reachable state for n <= 16, so no counterexample was found; n = 17 was
computed as an extension outside this claim.


Packaging note (contributor text, unverified): in the panel copies in panel/, the file-name notation that wrote the
certificate index as the letter n inside angle brackets (as in cert/n{n}.txt.gz with angle brackets) was replaced by
the same letter inside curly braces (4 places in criterion.md, 6 in reproduce.md) because the kit's placeholder scan
rejects angle-bracket tokens; nothing else in the panel files was changed, and the originals in the run folder are
untouched.
