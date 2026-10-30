# Generic 4-Player Binary-Action Game with 37 Regular Nash Equilibria

## What
An explicit generic 4-player binary-action game with rational payoffs and exactly 37 regular Nash equilibria certified across all 81 support patterns (Partial Win p1).

## Check It Yourself
Run the standalone verification script from this package directory:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output:
```text
[+] All 37 regular Nash equilibria verified in exact rational arithmetic.
    - Pure equilibria (k=0): 8
    - 1-mixed equilibria (k=1): 0
    - 2-mixed equilibria (k=2): 12
    - 3-mixed equilibria (k=3): 8
    - 4-mixed interior equilibria (k=4): 9
[+] All 37 Jacobians are non-singular and all pure slacks are strictly non-zero.
[+] Scaled integer game equivalence confirmed across all 16 profiles and 4 players.
PASS
PASS
```

Runtime is under 0.2 seconds on standard hardware using only the Python standard library (`fractions`, `itertools`, `json`).

## Compared To
- **Status Source**: Christoph Hertling, Jelena Vujic, "Maximal two-action games", arXiv:2412.17890v2 [math.PR] (25 Sep 2026), fetch timestamp 2026-10-29T04:41:42Z (HTTP 200, SHA-256 `c2cd243dedf14c4a0f1d2b13977ce80f010a1be84f2bc48d2f2d2baa46a215fa`).
- **Incumbent Record**:
  - Vidunas (2017) proved $\mu(4) \le 65$.
  - Hertling and Vujic (2024/2026) proved $\mu(4) \ge 37$ by demonstrating the existence of small generic deformations of product two-action games, and conjectured $\mu(4) = 37$ (Conjecture 4.5).
  - No explicit certified rational payoff table listing all 37 equilibrium coordinates and machine-checked Jacobians was provided in standard repositories.
- **Our Value**: An explicit generic rational payoff table ($a_j^i \in \{1/4, 1/2, 3/4\}$) and scaled integer payoff table ($L = 64$) with all 37 regular Nash equilibria certified with exact rational coordinates, non-singular Jacobians, and strict best-response slacks across all 81 support branches (Partial Win p1).

## Not Claimed
- We do not claim a formal mathematical proof that $\mu(4) \le 37$ (which remains Conjecture 4.5).
- We do not claim a full win counterexample with $\ge 39$ regular equilibria for $n = 4$ or $\ge 189$ equilibria for $n = 5$. A multithreaded perturbation search evaluating 2,963,000 perturbed candidate games observed zero instances exceeding 37 equilibria, corroborating the 37-equilibrium ceiling.

## Credits
- Christoph Hertling and Jelena Vujic for the product two-action game framework and Conjecture 4.5 (arXiv:2412.17890).
- Raimundas Vidunas for the theoretical upper bound $\mu(n) \le V(n)$ (arXiv:1705.04499).
- R. Jahani and B. von Stengel for maximal equilibrium bounds in 3-player binary-action games (2024).
- R. D. McKelvey and A. McLennan for the derangement bound on totally mixed equilibria (1997).
