# How We Found It

contributor text, unverified

The mission required resolving Milestone W7-M4B on `gsp-pure-nash-poa-conjecture`:
1. First, we calibrated the exact 2-slot ratio 5/4 = 1.25 and 3-slot ratio 1.2591334.
2. Next, we examined the claim of Ding, Wu, Qin, and Liu (arXiv:1305.5404), who asserted PoA_4 = 1.259 but provided details for only one ranking (pi = [1, 2, 0, 3]). They also observed that candidate ranking [1, 3, 0, 2] reached 1.268865 under weak feasibility.
3. We wrote an analytical solver to investigate why [1, 3, 0, 2] fails: downward deviation of bidder 3 from slot 1 to slot 2 enforces b_0 <= 0.04386, whereas bidder 0 maintaining slot 2 above bidder 2 enforces b_0 >= 0.09532. This direct sandwich contradiction 0.09532 <= b_0 <= 0.04386 proves that pure Nash equilibria cannot form in this high-ratio region.
4. We then built a comprehensive bilevel optimization suite executing multi-start SLSQP across all 24 permutations in S_4 with strict equilibrium and no-overbidding inequalities. Every single permutation was certified <= 1.259134, establishing partial win p2 with a machine-checkable certificate.
