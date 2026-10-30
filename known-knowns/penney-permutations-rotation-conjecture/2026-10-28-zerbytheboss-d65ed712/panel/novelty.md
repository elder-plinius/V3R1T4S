# Novelty Skeptic Report — `penney-permutations-rotation-conjecture`

context: subagent (fresh invocation)
target_id: penney-permutations-rotation-conjecture
review_utc: 2026-10-28T18:50:00Z

## Novelty & Prior Art Audit

1. **Status Source and Literature Verification**:
   - Status URL: `https://arxiv.org/abs/2404.06585` (Sergi Elizalde and Yixin Lin, "Penney’s Game for Permutations", DMTCS 28:1 (2026)).
   - In Section 6, the authors state Conjecture 6.1: for any $k \ge 3$ and any pattern $\sigma \in S_k$, Bob's cyclic rotation choice $\tau = (\sigma_2, \dots, \sigma_k, \sigma_1)$ beats Alice's pattern with $\Pr(\sigma \prec \tau) < 1/2$.
   - In the paper, the conjecture was rigorously proven only for $k = 3$ (Section 4). For $k = 4$, the authors presented only numerical approximations by truncating the series at $n = 11$, leaving the remainder uncertified.
   - Prior to this work, no rigorous proof or finite horizon certificate establishing $\Pr(\sigma \prec \tau) < 1/2$ for all $\sigma \in S_4$ existed in the literature.

2. **Benchmarking against Incumbent Records**:
   - Incumbent knowledge: analytical proof for $S_3$; heuristic truncated series for $S_4$.
   - This submission provides exact big-integer certificates $(A(H) + R(H))/H! < 1/2$ at $H \le 36$ for every one of the 24 permutations of $S_4$, establishing Partial Win `p1`.

3. **Repository and PR Check**:
   - Inspected `repo/TROPHY_CASE.md`: no prior entry exists for `penney-permutations-rotation-conjecture`.
   - Inspected open pull requests on `elder-plinius/V3R1T4S`: zero competing claims for this target.
   - This represents the first certified mathematical resolution of claim `p1`.

pass: true
