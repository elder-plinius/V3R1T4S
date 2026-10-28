# How we found it (contributor text, unverified)

The target asks for the next exact terms of OEIS A387261/A387262 beyond the established record: the exact win probability of the starting player in the coin push-your-luck race "Risk or Safety" (R. Jehn, arXiv:2603.01002), published for n = 1..15 in OEIS and n = 16..30 in this repository's known-knowns, each term requiring an independently checked Bellman optimality certificate in exact rational arithmetic.

The brief:
The game is a finite two-player zero-sum stochastic game whose positions split into strongly connected components indexed by points-needed coordinates (i, j). Banked points never decrease, so i + j is strictly decreasing upon banking. Inside each component only two unknowns are cyclic: the two players' 0-open continuation values x = Q(0, i, j) and y = Q(0, j, i). The entire game decomposes into an acyclic cascade of 2x2 rational linear systems.

What was done:
1. Checked live status at OEIS A387261 and verified that no exact terms for n >= 31 exist in the literature.
2. Two independent exact solvers were constructed from first principles:
   - Extender Lens: Component-wise exact policy iteration with safeguarded Newton-Raphson iteration on h(x) = x - F(G(x)) = 0.
   - Contrarian Lens: Pure-turn-plan exact minimax, solving each component's matrix game in closed form as x* = min_m max_k x_{km} with zero iteration.
3. Both independent solvers solved all 1,035 components for N = 45 in exact rational arithmetic (standard library fractions.Fraction, zero floating point). They agreed identically on all 45 exact rational values P(0, n, n).
4. Both solvers reproduced all 15 published terms of OEIS A387261/A387262 (n = 1..15), all 15 repository terms from known-knowns (n = 16..30), and all 400 terms of A394776 / Table 1.
5. Generated complete Bellman value and action certificates P(a, b, c) for every n = 31..45, comprising n^2(n+1)/2 positions per n (46,575 positions for n = 45).
6. Packaged the certificates in object/ using gzip compression and sharding for files > 1 MB to strictly obey package size constraints.
7. Verified all 45 certificates in two independent checkers: ros_cert_check.py (fractions.Fraction) and my_verify.py (exact integer cross-multiplication with coprimality checking).

What was dead:
No published value or action needed correction (partial win p1 was not triggered; all published values and strategy cells were verified optimal).
Floating-point approximations were rejected due to the risk of policy-flip roundoff errors on deep game trees.

Compute:
The exact solve for N = 45 took 12.64s for policy iteration and 62.96s for pure-turn-plan minimax on a single thread. The full verification suite takes ~20s.
