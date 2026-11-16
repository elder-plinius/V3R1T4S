# Global Optimality Certificate for the 4-to-1 Single-Qubit QRAC with Shared Randomness

## What

A re-runnable mpmath interval-arithmetic branch-and-bound certificate (43,476 dyadic leaves in canonical symmetry-reduced coordinates, which I re-checked numerically) shows that the maximum over four unit vectors in R^3 of 1/2 + (1/128) sum_x ||sum_i x_i v_i|| is at most 0.741481799559635, below 0.741482, which is criterion (a) for the 4-to-1 single-qubit QRAC with shared randomness; it says nothing about other n, and literature novelty was not assessed by me.

## Check it yourself

From this package folder:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected final output line: `PASS` (runs in ~52 seconds on 1 laptop core, `< 30 MB` RAM; requires `python3` with `mpmath`).

## Compared to

| Source | Cell | Value | URL | UTC fetch time |
|---|---|---|---|---|
| Tan and Jafar, `arXiv:2607.10414v3` (23 Oct 2026) | `(n, m) = (4, 1)` qubit QRAC | Exact optimality open; proven upper bound `0.75` | https://arxiv.org/abs/2607.10414 | 2026-11-15T16:06:29Z |
| Ambainis, Leung, Mančinska, Ozols, `arXiv:0810.2937` | `n = 4` SR QRAC (Table 2) | Constructive lower bound `1/2 + (1+sqrt(3))/(8*sqrt(2)) = 0.741481456572...` | https://arxiv.org/abs/0810.2937 | 2026-11-15T14:07:10Z |
| Mančinska and Storgaard, `arXiv:2106.00155` | `n = 4, m = 1` SR QRAC | Upper bound `0.75` | https://arxiv.org/abs/2106.00155 | 2026-11-15T14:07:10Z |

Snapshot details and SHA-256 digests: `the-record-we-beat/README.md`.

## Not claimed

- Certifies `n = 4` (`(4, 1)` single-qubit QRAC with shared randomness) within $3.43 \times 10^{-7} < 10^{-6}$ (`<= 0.741482`); does not settle $n \ge 5$ or symbolic uniqueness without interval arithmetic.

## Credits

- **Andris Ambainis, Debbie Leung, Laura Mančinska, and Maris Ozols** (<https://arxiv.org/abs/0810.2937>): Bloch-vector reduction, $p \le 1/2 + 1/(2\sqrt{n})$ bound, and the optimal $n = 4$ construction.
- **Shuo Tan and Syed A. Jafar** (<https://arxiv.org/abs/2607.10414>): status characterization of solved `(n, m)` QRACs through October 2026.
- **Laura Mančinska and Sigurd Storgaard** (<https://arxiv.org/abs/2106.00155>): general `m`-qubit shared-randomness upper bound.
- **mpmath** (<https://mpmath.org/>): outward-rounded interval arithmetic (`mpmath.iv`) used in `verify-it-yourself/verify_qrac4.py`.
