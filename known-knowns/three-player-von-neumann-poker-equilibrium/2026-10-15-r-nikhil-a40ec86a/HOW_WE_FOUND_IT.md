# How we found it (contributor text, unverified)

The bank target asked whether the "conjectured Nash equilibrium" of three-player continuous von Neumann poker
(Krityakierne, Thanatipanonda and Zeilberger 2024, Section 4) really is an equilibrium at bet size 2, or for all bets.
The paper derives only the three indifference conditions at the cut points A, B, C.

A Codex-based agent run derived every action payoff exactly against the threshold opponents (integrating rectangles of
opponent hands from the terminal pot utilities with symbolic b), observed that each player's advantage of the
prescribed action, after subtracting the matching indifference equation and writing the ordered thresholds as sums
of positive gaps, has only nonnegative coefficients, and proved existence and uniqueness of the ordered root for
every b > 0 by a monotone-crossing argument. It froze the claim but could not start fresh reviewers.

A Claude-based run then re-derived the result independently from the rules. The proof becomes short: on [C,1) I's
bet-minus-check advantage is exactly b(3x^2 - 2Cx - 1), whose positive root is B by Eq. B; on (0,C] it is
3(A^2 - x^2) by Eq. A; a caller's call-minus-fold advantage is nondecreasing in the hand and vanishes on all of
[A,C] by Eq. C. It also confirmed the b=2 algebra and the paper's printed-digit errors, and found that a first
novelty review was blocked by one unreadable 1977 paper (Šimelis, "Equilibrium strategies in a three-person poker
game"). Springer's public first-pages preview showed that paper studies a different, sequential bet-or-fold game; a
fresh three-skeptic panel then passed the claim as partial win p1.

What failed or was ruled out on the way: the main criterion's printed-digit clause (the paper's 15th decimals are
off by about 4e-15); an observed-action (sequential) reading of the rules, under which the profile is not an
equilibrium but which is a different game; profitable deviations searched by exact finite-deck best responses (the
discretised profile's regret tends to 0) and Monte Carlo.
