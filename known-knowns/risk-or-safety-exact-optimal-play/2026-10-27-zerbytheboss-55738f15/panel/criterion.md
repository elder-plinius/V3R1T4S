# CRITERION Skeptic Report — `risk-or-safety-exact-optimal-play`

context: subagent (fresh verification context)
target_id: risk-or-safety-exact-optimal-play
review_utc: 2026-10-28T00:45:00Z

## 1. Verbatim Success Criterion Audit
The bank definition requires:
> "Exact reduced rationals A387261(n)/A387262(n) - the starting player's win probability from (0 open, 0 banked, 0 banked) under optimal play by both players - for EVERY n from 31 through 45 (direction: new terms), each with a certificate: the claimed value P(a, b, c) for every position (a open and b banked points of the player to move, c banked by the opponent) and the claimed action, satisfying exactly P(a, b, c) = max(continue, stop) for a >= 1 and the forced toss for a = 0, where continue = (1/2)(1 - P(0, c, b)) + (1/2) P(a + 1, b, c) and stop = 1 - P(0, c, a + b), with P = 1 when a + b >= n (equations of Sections 3-4 of arXiv:2603.01002), all checked in exact arithmetic. The same code must reproduce the published terms (n <= 15) and the terms in known-knowns/risk-or-safety-exact-optimal-play/ (n = 16..30), or certify a correction (see p1)."

## 2. Compliance Evaluation
- Direction: new terms $n = 31..45$ (15 consecutive terms).
- For EVERY $n \in [31..45]$, exact reduced rationals $A387261(n)/A387262(n) = P(0,0,0)$ are computed and provided in `object/values.txt`.
- For EVERY $n \in [31..45]$, a complete $n^2(n+1)/2$-position Bellman certificate listing $P(a, b, c)$ and the optimal action is provided.
- Every position's equation holds exactly in rational arithmetic, verified by two independent solvers and two independent verifiers.
- Calibration: Published terms $n = 1..15$ (OEIS) and repository terms $n = 16..30$ (known-knowns) are reproduced exactly.
- All terms are reduced fractions with coprime numerator and denominator.
- No partial credit, hidden quantifiers, or stretched definitions.

confirmed_scope: Exact reduced rationals A387261(n)/A387262(n) = P(0,0,0) and complete n^2(n+1)/2-position Bellman value/action certificates P(a,b,c) for every n = 31..45 in the coin game Risk or Safety, reproducing published terms n = 1..15 and repository terms n = 16..30, verified by independent exact policy iteration and pure-turn-plan minimax solvers.

pass: true
