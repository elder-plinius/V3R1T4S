# How we found it (contributor text, unverified)

The target asks for the next terms of OEIS A387261/A387262: the exact win probability of the starting player in the coin
push-your-luck race "Risk or Safety" (R. Jehn, arXiv:2603.01002), published only for n = 1..15, each term to come with a
certificate that proves optimality in exact arithmetic.

The brief: the game is a finite two-player zero-sum stochastic game whose positions split into strongly connected
components by the pair of banked totals; inside a component only two unknowns are cyclic (the two players' values with
no open points), so the whole game can be solved exactly, one 2x2 rational linear solve per policy step. Rewriting
positions in points-needed coordinates (points the mover still needs, points the opponent needs) makes one table serve
every n at once: the value for goal n is the entry at (n, n).

What was done: a checker was written from the definition and tested on one correct and five corrupted certificates
before any solver ran; the success rule was frozen (PREREG.md). Two lenses then wrote independent exact solvers:
one a component-wise exact policy iteration (a safeguarded Newton root-finder on the two-cycle of each component; the
exact bisection safeguard never fired), the other an exact minimax over pure turn-plans with a closed-form fixed point
per component. Both reproduced the 15 published terms exactly and agreed on all 30 values; a third computation in
floating point agreed to 1e-15; the certificates of every n embed consistently into every larger n (640,088 position
comparisons); the toss counts derived from the exact actions equal all 400 published terms of A394776 and the 361 cells
of the paper's Table 1; only the bank's reading of the rules (and provably equivalent variants) reproduces the published
numbers, which rules out a definition mismatch. No exact tie between stopping and continuing exists anywhere up to
n = 60, so every optimal action is unique.

What failed or was dead: no published value or action needed correction (partial win p1 is empty); the "closed form for
the denominators" idea gave only the observation that every prime factor of A387262(n) divides some 2^k + 2^l - 1
(the component determinants) and no shortcut.

Compute: the exact solve for all n <= 30 takes about 1.3 s single-threaded; verification about 10 s. The run also
certified n = 31..40 and computed values to n = 60 (not part of this package); a compact certificate format
(how-we-built-it/code/ros_compact_check.py) is the tool for pushing further.
