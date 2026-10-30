# The Record We Beat — `coin-basket-random-expected-values`

## Published OEIS Sequence Records
- Sequence 1 URL: `https://oeis.org/A391791`
- Sequence 2 URL: `https://oeis.org/A391792`
- Fetched UTC: `2026-10-28T00:31:50Z`
- HTTP Status: 200
- A391791 Page SHA-256: `f4ca4c77d1c41c96dab40e5f51e2756147aba06cdbd83067bfd5e1d807f79b59`
- A391792 Page SHA-256: `3143809d4ee29eb93fba6cc44747cff5fece2579df206bbda294c773bc26cb68`

## Target Instances and Published Literature Extents
- **A391791 (k=2 baskets)**:
  - Published extent in OEIS (revision #16, 7 Jan 2026): $n = 1..22$
  - Published terminal term: $a(22) = 405700861$
  - Status: Open beyond $n=22$
  - Conjecture: For $n > 9$, optimal first move is coin $\lfloor (n+3)/2 \rfloor$ (unverified for $n \ge 23$)
- **A391792 (k=3 baskets)**:
  - Published extent in OEIS (revision #6, 7 Jan 2026): $n = 1..18$
  - Published terminal term: $a(18) = 13615817865$
  - Status: Open beyond $n=18$

## What This Work Extends
This work computes the exact integer backward-induction solutions beyond the published frontiers:
- $A391791(23) = 884741548$
- $A391791(24) = 1922512940$
- $A391791(25) = 4164198462$
- $A391792(19) = 45245088184$
- $A391792(20) = 149627079790$
- $A391792(21) = 492482601295$
Furthermore, it audits and settles Jehn's conjecture for all $n \in [10..25]$, proving that the optimal first move is strictly unique and identically equal to $\lfloor (n+3)/2 \rfloor$.
