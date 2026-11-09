# Levine's Two-Player Hat Puzzle — Exact Value V_{2,4} = 89/256

## What
Exact rational certification of V_{2,4} = 89/256 = 0.34765625 via exhaustive canonical search over all 4-hat strategies (Partial Win p1).

## Check it yourself
Run the standalone checker from this package directory:
```sh
sh verify-it-yourself/run_checks.sh
```
- Expected last line: `PASS`
- Rough laptop time: < 1 second (pure Python standard library)

## Compared to
- **Table / Source**: arXiv:2508.01737v2 [math.PR], Table 1 & Section 3
- **Cell**: $V_{2,4}$ (finite stack height $h=4$)
- **Published Value**: $\ge 89/256 = 0.34765625$ (empirical lower bound obtained via local hill climbing, called "likely sharp, unproven")
- **URL**: https://arxiv.org/abs/2508.01737
- **Fetch Time**: 2026-10-29T08:07:00Z (HTTP 200, SHA256: `78a1f96a58a69dd70d64216fb609a7d70c1cb00dc0fa21e92de2eaacc712e6dd`)

## Not claimed
- Full Win (A): Provable upper bound $V_2 \le U < 81/224$ via matrix hint game. The best provable upper bound in the literature remains $V_2 \le 81/224 \approx 0.361607$ (Buhler et al., 2021). The $16 \times 30$ affine matrix partition achieving $57/160 = 0.35625$ establishes only a lower bound $V(M_{16 \times 30}) \ge 57/160$.
- Full Win (B): Refutation of Bouquet et al. Conjecture 1 ($V_2 = 7/20 = 0.35$).
- Partial Win p2: Exact rational certification of $V_{2,5}$.

## Credits
- Lionel Levine (puzzle formulation)
- Joe Buhler, Richard Freiling, Ronald Graham, Colin Kariv, Jim Roche, Mark Tiefenbruck, Neil Van Alten, and Dmytro Yeroshkin, "On Levine's notorious hat puzzle", INTEGERS 21A (2021), arXiv:1407.4711
- Alice Carter-Reyes and Mark Tiefenbruck, OEIS A345255 / A345257 (finite stack solutions for $h \le 3$)
- Thomas Bouquet, Mustapha Chikhi, Augustin Charles, Yicheng Zhou, and Bryan Wang, "On Lionel Levine's Hat Puzzle", arXiv:2508.01737v2 (2026)
