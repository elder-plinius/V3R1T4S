# How we found it (contributor text, unverified)

Found by Kaust-a-laut with Claude Code (Anthropic) running claude-opus-5-5, in a V3R1T4S run on 2026-10-18.

Brief. The same session had just proved a new lower bound for square-lattice site percolation (0.5567) with a
van den Berg-Ermakov growth-process coupling and exact posteriors. Looking for where that machinery had the best odds,
a literature check found that the best rigorous upper bound on p_c^site(Z^3) was still Campanino and Russo's
non-explicit p_c < 1/2 from 1985 (listed as 0.5000 in a 2026 table), while p_c is about 0.3116 numerically.

What failed. Small blocks with "largest component" as the designated set (2x2x2, 2x3x3, elongated 2x2x4) gave bounds
above 1/2. A rule taking every site connected to the entry was worse: the children succeed often but inherit a small
designated set. A face-count requirement added nothing. Depth-1 posteriors were judged not worth it: the worst entry
(a single corner site) is realised by real histories, so the depth-0 adversary is close to tight here.

What worked. Exhaustive 3x3x3 blocks (2^27 states) passed the gate below 1/2 (float probe ~0.4725 at q = 1/2). A
minimum size of 6 for the designated component and a face-weight tie-break moved the iteration's fixed point to
~0.4426. Since each proven bound can serve as the comparison level q for the next link, a chain of exact
certificates descends to 0.4427. The certificate engine uses outward-rounded interval sums over all states and an
exact integer up-set test; a separately written float engine agreed to 6e-12 on every used entry, and the panel's
reproducer wrote its own exhaustive checker, which matched.

A contrarian pass then removed the dependence on Campanino-Russo: starting the chain at q = 0.68, justified by
Wierman's 1995 square-lattice bound 0.679492 and Z^2 inside Z^3, also reaches 0.4427 (not panelled).
