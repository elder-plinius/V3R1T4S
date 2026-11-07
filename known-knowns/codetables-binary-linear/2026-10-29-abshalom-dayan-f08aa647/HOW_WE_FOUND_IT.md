# How we found it

contributor text, unverified

This is the fourth GF(9) table cell from one family, Construction X on nested one-point codes of the Hermitian curve y^3 + y = x^4 over GF(9), after our [31,18,10] (#644, with a Reed-Solomon tail), [29,19,8] (#792) and [32,19,10] (#806). Like the last two, it uses a general tail instead of a Reed-Solomon one. The textbook bound for this pair,
C(D,16P) = [27,14,11] inside C(D,19P) = [27,17,8], with a 4-column MDS tail, is min(11, 8 + 2) = 10, a tie with the
table. Instead of a fixed tail code, a small exact search picks the 4 tail columns so that every coset of C(D,16P)
gets enough tail weight to make up for its own minimum weight: every codeword outside the zero-tail subcode then has
weight at least 11.

An earlier run (2026-10-27) computed the exact coset weights and ran the tail search over 49 nested pairs and tail lengths against the live table (later runs searched more); it reported a hit for this pair but did not build it. The next run (2026-10-28) built
it and measured d = 11 with two exact programs, but claimed a different cell that night (one claim per run). This
run (2026-10-29) rebuilt it from the construction text, checked it again with both programs and an independent
rebuild, ran a closure audit over the live n = 28..36 range page (no table rule or earlier result gives d = 11 at
(31,17)), and sent it to a three-skeptic panel, one skeptic at a time.

What failed in the same family: Reed-Solomon tails for 411 of 413 Construction X candidates (nested pairs and tail lengths; the other two give our known [31,18,10]), every 5-column tail for [32,18,11] on the C(D,15P) and C(D,16P) subcodes (the C(D,17P) subcode is ruled out because it already has weight-10 words), and 29 high-distance nested pairs and tail lengths (searched exhaustively this run, with
no tail at all).
