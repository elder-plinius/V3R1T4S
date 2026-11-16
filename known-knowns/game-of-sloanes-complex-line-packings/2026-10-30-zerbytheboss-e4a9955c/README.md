# Complex Line Packings Record Upgrade

## What

Explicit complex line packing of 47 unit vectors in C^5 with coherence mu = 0.5365483510672764450529014297211004070950 computed in mpmath at 40 digits after normalization, strictly lowering the Game of Sloanes live leaderboard record 0.53660699 by 5.86389e-5 >= 1e-8, alongside record packings for (6,40), (6,41), and (4,11).

## Check It Yourself

Execute the standalone verification suite from the package root:

```bash
sh verify-it-yourself/run_checks.sh
```

This normalizes the 47 vectors in $\mathbb{C}^5$ from `object/5x47_v3r1t4s.txt` in 40-digit `mpmath` and evaluates all $\binom{47}{2} = 1,081$ pairwise Hermitian inner products, verifying that the coherence strictly improves the leaderboard record by $5.86389 \times 10^{-5} \ge 10^{-8}$ and remains above the theoretical lower bound.

## Compared To

- **Leaderboard Record**: The Game of Sloanes leaderboard record for $(d=5, n=47)$ was `0.53660699` (submitted by `oai`).
- **This Submission**: Achieves coherence `0.5365483510...`, lowering the record by $5.86389 \times 10^{-5}$ (over 5,800 times the required $10^{-8}$ threshold).
- **Additional Records**: Also includes new record configurations for $(6,40)$, $(6,41)$, and $(4,11)$ in `how-we-built-it/`.

## Not Claimed

- No claim is made that these packings meet the absolute theoretical lower bounds (which are unachievable for these $(d, n)$ parameters).
- No claim is made of global optimality.

## Credits

- V3R1T4S project contributors.
- Maintainers of the Game of Sloanes project (gnikylime).
