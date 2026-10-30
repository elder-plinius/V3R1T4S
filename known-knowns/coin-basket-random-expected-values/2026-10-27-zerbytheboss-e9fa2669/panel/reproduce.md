# Reproduce Skeptic Report — `coin-basket-random-expected-values`

context: subagent (fresh invocation)
target_id: coin-basket-random-expected-values
review_utc: 2026-10-28T00:46:00Z

## Reproduction Audit

1. **Independent Verification from First Principles**:
   The game is defined by $k$ exchangeable baskets and coins $1, \dots, n$. On each turn one basket is selected uniformly at random ($1/k$ probability), and the player chooses a remaining coin $c \in R$ to place into that basket. The final payoff is $\max(s_1, \dots, s_k)$.
   Under the backward induction recurrence:
   $$W(R, s) = \sum_{b=1}^k \max_{c \in R} W(R \setminus \{c\}, s + c \cdot e_b)$$
   with $W(\emptyset, s) = \max_{1 \le i \le k} s_i$, all values are strictly exact integers. The published sequence values are given by $a(n) = \frac{1}{k} W(\{1..n\}, 0) = \max_{c \in \{1..n\}} W(\{1..n\} \setminus \{c\}, c \cdot e_1)$.

2. **Published Sequence Calibration**:
   Both Solver 1 (Rust) and Solver 2 (C++) were executed against the official OEIS b-files:
   - OEIS A391791 ($k=2$): Exactly reproduced all 22 published terms ($n=1..22$):
     1, 5, 20, 65, 190, 530, 1407, 3585, 8942, 21819, 52204, 123190, 287044, 661329, 1509949, 3420580, 7688444, 17173896, 38143782, 84262365, 185278522, 405700861. Zero discrepancies.
   - OEIS A391792 ($k=3$): Exactly reproduced all 18 published terms ($n=1..18$):
     1, 7, 40, 192, 837, 3423, 13478, 51396, 190809, 693595, 2477822, 8740848, 30419671, 104752091, 357748926, 1211285880, 4074000387, 13615817865. Zero discrepancies.

3. **New Sequence Terms ($K=3$ for each sequence)**:
   The two independent compiled solvers agree on every single new term:
   - $A391791(23) = 884741548$
   - $A391791(24) = 1922512940$
   - $A391791(25) = 4164198462$
   - $A391792(19) = 45245088184$
   - $A391792(20) = 149627079790$
   - $A391792(21) = 492482601295$

4. **Partial Win p2 (Jehn's Conjecture Audit)**:
   For every $n \in [10..25]$, both independent engines evaluated all initial moves $c \in \{1..n\}$ and proved that the optimal first move is strictly unique and identical to $\lfloor (n+3)/2 \rfloor$:
   $n=10: \{6\}$, $n=11: \{7\}$, $n=12: \{7\}$, $n=13: \{8\}$, $n=14: \{8\}$, $n=15: \{9\}$, $n=16: \{9\}$, $n=17: \{10\}$, $n=18: \{10\}$, $n=19: \{11\}$, $n=20: \{11\}$, $n=21: \{12\}$, $n=22: \{12\}$, $n=23: \{13\}$, $n=24: \{13\}$, $n=25: \{14\}$.
   Zero floating point was used in either solver.

pass: true
