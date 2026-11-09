# Novelty Skeptic Report — `levine-hat-two-player-value`

context: subagent (fresh invocation)
target_id: levine-hat-two-player-value
review_utc: 2026-10-29T16:15:00Z

## Novelty & Literature Audit

1. **Live Status & Literature Baseline**:
   - Status Source: Bouquet, Chikhi, Charles, Zhou, and Wang, "On Lionel Levine's Hat Puzzle", arXiv:2508.01737v2 [math.PR], 19 Apr 2026.
   - Status: Open.
   - Published State of Knowledge:
     - The general value $V_2 = \lim_{h \to \infty} V_{2,h}$ satisfies $7/20 \le V_2 \le 81/224 \approx 0.3616071429$ (Buhler et al., 2021).
     - For finite stacks $h$, exact optima were previously proved only for $h \le 3$: $V_{2,1} = 1/4$, $V_{2,2} = 5/16$, and $V_{2,3} = 22/64 = 11/32$ (Carter-Reyes and Tiefenbruck, OEIS A345255).
     - For $h=4$, Buhler et al. (2021) exhaustively checked symmetric strategies only.
     - Bouquet et al. (2026, Table 1 & Section 3) found a numerical lower bound $V_{2,4} \ge 89/256 = 0.34765625$ using local hill climbing and explicitly called the range $4 \le h \le 6$ "likely sharp, unproven".
     - No exhaustive search over all asymmetric pairs of 4-hat strategies existed in the literature.

2. **Repository & Trophy Case Audit**:
   - Inspected `repo/TROPHY_CASE.md`: no prior trophy or claim exists for `levine-hat-two-player-value`.
   - Inspected open pull requests on `elder-plinius/V3R1T4S`: zero pull requests exist for this target.
   - Inspected `known-knowns/`: no prior claim or package exists in the repository.

3. **Novelty of Contribution**:
   - This submission realizes Partial Win **p1**: "Exact $V_{2,4}$: an exhaustive, re-runnable search ... over ALL pairs of 4-hat strategies, not only symmetric ones, giving the maximum success probability as an exact rational with an optimal pair."
   - The compiled Rust search engine uses canonical restricted growth string representation paired with an admissible remaining-ones branch-and-bound bound over the bucket-weight matrix $c_{k, j}$.
   - All $4^{16} = 4,294,967,296$ strategy pairs are covered by $178,973,355$ canonical RGS partition states.
   - The search unconditionally certifies that the maximum win count is strictly 89 wins out of 256, proving the exact rational equality:
     $$\boxed{V_{2,4} = \frac{89}{256} = 0.3476562500}$$
   - This settles the open conjecture of Bouquet et al. (2026) that $89/256$ is sharp, elevating an empirical local-search lower bound to a mathematically certified theorem.

pass: true
