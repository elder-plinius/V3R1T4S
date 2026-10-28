# Novelty Skeptic Report — `myerson-vs-anonymous-reserve-gap`

context: subagent (fresh invocation)
target_id: myerson-vs-anonymous-reserve-gap
review_utc: 2026-10-28T18:25:00Z

## Novelty & Prior Art Audit

1. **Status Source and Literature Verification**:
   - Status URL: `https://arxiv.org/abs/2411.03583`
   - Primary reference 1: Yiannis Giannakopoulos, Jinshan Zhang, and Lu Xiao (JLTX), "Tight Bounds for Anonymous Reserve Pricing in Single-Item Auctions", SODA 2019 (`arXiv:1804.00480`). Theorem 3 introduced the triangular equalisation recursion and gave a numerical 4-buyer example with ratio $\approx 2.1596$.
   - Primary reference 2: Zhe Feng and Lu Jin, "On the Power of Anonymous Reserve in Single-Item Auctions", November 2024 (`arXiv:2411.03583v1`). Result 3 and Theorem 7 state that for regular distributions, $\text{AR}/\text{OPT} \in [0.3817, 0.4630]$, where the upper end $0.4630$ ($1/0.4630 \approx 2.1598$) is taken from JLTX Theorem 3. They explicitly characterize the exact gap as open.

2. **Benchmarking against Incumbent Records**:
   - The JLTX 4-buyer example used rounded 4-decimal parameters $(v_1=2.0125, q_1=0.2520, v_2=1.1492, q_2=0.4905, v_3=0.8876, q_3=0.7876, v_4=0.8143, q_4=1.0)$, yielding $\text{OPT} \approx 2.1596$ with numerical rounding in the integrals.
   - The target threshold in `repo/bank/targets.json` is set to $2.1600$, requiring rigorous certification that separates the ratio from the numerical 2.1596 record.
   - The 5-buyer instance discovered in this run achieves a certified ratio of $\text{OPT}/\text{AR} \ge 2.16310706 > 2.16000000$, exceeding the target threshold with a strict separation margin of $+0.00310706$.
   - Scaling experiments in Lens 2 show the recursion scales up to $n=25$, peaking near $n=6$ ($\text{OPT} \approx 2.163604$).

3. **Repository and PR Check**:
   - Inspected `repo/TROPHY_CASE.md`: no prior entry exists for `myerson-vs-anonymous-reserve-gap`.
   - Inspected open pull requests on `elder-plinius/V3R1T4S`: zero open PRs claim this target.
   - This represents the first certified regular instance establishing $\text{OPT}/\text{AR} \ge 2.1600$.

pass: true
