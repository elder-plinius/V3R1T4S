# Three-Qubit GHZ Nonlocality Robustness Below `0.49140` (`18 x 24 x 72` Exact Certificate)

## What

The 18x24x72 integer full-correlation Bell functional in object/bell_ghz3_18x24x72.json with planar projective qubit settings has exact local bound L = 130692616 (confirmed by two independent orbit-enumeration programs that agree) and Q_GHZ = 265961302.90703046706895787151..., so the white-noise-mixed three-qubit GHZ state is nonlocal for every v > 0.4913971114274656713239022, which beats the 0.49143 Table III value by more than 1e-5 and meets the stated full criterion for N = 3.

## Check it yourself

From this package folder:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected final output line: `PASS` (runs in ~22 seconds on 2 laptop threads, `< 135 MB` RAM; requires `python3` with `mpmath` and a C++17 compiler).

## Compared to

| Source | Cell | Value | URL | UTC fetch time |
|---|---|---|---|---|
| Designolle, Vértesi, Pokutta, `arXiv:2310.20677v3` (5 Oct 2026, Table III) | `N = 3` certified (`m = 22`) | `0.49143` (`0.49142745...`) | https://arxiv.org/abs/2310.20677 | 2026-11-15T16:06:29Z |
| Vértesi and Pál, `arXiv:1108.1998` | `N = 3` (`5 x 5 x 5`) | `0.496057` | https://arxiv.org/abs/1108.1998 | 2026-11-15T15:11:51Z |

Snapshot details and SHA-256 digests: `the-record-we-beat/README.md`.

## Not claimed

- Certifies an upper bound $v_c \le 0.4913971114274656713239022$ for $N = 3$ using $(18, 24, 72)$ XY-plane projective settings; does not break the planar lower bound $v_{XY} \ge 0.49129$ (`arXiv:2310.20677v3` Sec. IX.2) or claim improvements for $N \in \{4, \dots, 10\}$.

## Credits

- **Sébastien Designolle, Tamás Vértesi, and Sebastian Pokutta** (*Phys. Rev. A* 109, 022205, 2024; <https://arxiv.org/abs/2310.20677>; <https://github.com/ZIB-IOL/BellPolytopes.jl>): established the previous certified `0.49143` record and antiperiodic polygon symmetry methods.
- **Tamás Vértesi and Károly F. Pál** (<https://arxiv.org/abs/1108.1998>): earlier `0.496057` three-qubit GHZ visibility upper bound.
- **mpmath** (<https://mpmath.org/>): 55-digit outward-rounded interval arithmetic (`mpmath.iv`).
