# Positive Resolution of Kurz's Section 6 Research Problem: 240 Order-5 Planes in `PG(6, 2)` Disjoint from the Fixed Plane (`binary-q-fano-plane-s2-2-3-7`, `p2`)

## What

The file object/p2_240_planes_order5.txt gives an explicit order-5 matrix pi in GL(7,2) (acting on row vectors) and 240 distinct rank-3 planes of PG(6,2) that are pi-invariant as a set, disjoint from the 3-dimensional pi-fixed space F, pairwise meeting in at most a point, and covering each of the 120 points outside F exactly 14 times, which answers in the affirmative the Section 6 research problem of arXiv 2112.11766v3 with its evidently intended count of 14 (not the paper's misprinted 15), and says nothing about a 381-plane q-Fano plane or any code of 334 or more planes.

## Check it yourself

From this package folder (requires only Python 3 standard library and a C99 compiler `cc`):

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last output line: `PASS` (verifies `ord(pi) = 5` in `GL(7, 2)`, `dim(F) = 3` (`7` projective points), `240` distinct rank-`3` binary RREF planes disjoint from `F` and `pi`-invariant in `48` orbits of size `5`, at most `1` plane per line across all `2,667` lines of `PG(6, 2)` (`1,680` covered once), and exact coverage `14` on all `120` points outside `F`, in both Python 3 and C99, while rejecting `5` corrupted negative controls).

## Compared to

- **Survey & open problem**: Sascha Kurz, *Constructions and bounds for subspace codes*, Section 6 Research Problem (https://arxiv.org/abs/2112.11766, `arXiv:2112.11766v3`, Dec 20, 2025)
- **Fetched**: `2026-11-17T10:21:42Z` (`HTTP 200`, SHA-256 `24723303e32759e552581a62d1225c82e1632f1df345be55454c90db8b129dd6`)
- **Prior status**: Open existence vs non-existence question for `240` order-`5`-invariant planes disjoint from `F` in `PG(6, 2)`

## Not claimed

- Existence or non-existence of the full `381`-plane binary q-analog of the Fano plane `S_2[2, 3, 7]` is not claimed (exact MILP over all `261` compatible residual planes shows this `240`-plane configuration extends to at most `277` planes, consistent with Braun-Kiermaier-Nakic's theorem that no `381`-plane `S_2[2, 3, 7]` admits an order-`5` automorphism).
- Partial Win `p1` (`A_2(7, 4; 3) >= 334`) and Partial Win `p3` (`45`-plane `F_2^6` relaxation) are not claimed.

## Credits

- **Sascha Kurz**, *Constructions and bounds for subspace codes* (https://arxiv.org/abs/2112.11766), for formulating the Section 6 Research Problem and surveying the `S_2[2, 3, 7]` subspace-coding landscape.
- **Daniel Heinlein, Michael Kiermaier, Sascha Kurz, and Alfred Wassermann**, *A subspace code of size 333 in the setting of a binary q-analog of the Fano plane* (https://arxiv.org/abs/1708.06224), for the `333`-plane construction and canonical subgroup generators (`G_{5,1}`).
- **Michael Braun, Michael Kiermaier, and Anamari Nakic** (https://arxiv.org/abs/1501.07790) and **Michael Kiermaier, Sascha Kurz, and Alfred Wassermann** (https://arxiv.org/abs/1605.03853), for automorphism group bounds on `S_2[2, 3, 7]`.
