# Exact Prime-Power Congruence `D(10) == 16 (mod 27)` for the Tenth Dedekind Number

## What

D(10) == 16 (mod 27) (hence == 7 mod 9), obtained by a truncated Burnside-Mobius sum over the 27 subgroups of order >= 9 of the Sylow 3-subgroup C3 wr C3 of S_9, agreed by two separately coded engines (C99 128-bit and Python CRT), which also give D(9) == 24 (mod 27) matching the exact value; not the full D(10), and not any other modulus.

## Check It Yourself

From this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last output line: `PASS` (runs two genuinely independent implementations — standalone C99 128-bit subgroup-poset Mobius + Bipartite Galois / Dedekind interval decomposition, and Pure Python 3 multi-prime finite-field CRT + Burnside Table-of-Marks + 4-slice Markov / Birkhoff Zeta transfer — verifying exact agreement on all `9` `S_9`-conjugacy classes, reproducing `D(0..7)`, `D(6..8) mod 9`, `D(9) == 24 (mod 27)`, and `arXiv:2611.13887v1`'s `D(10) == 1 (mod 3)`).

## Compared To

- **Table / primary status source:** OEIS sequence `A000372` (https://oeis.org/A000372, fetched `2026-11-18T07:50:22Z`, HTTP `200`, SHA-256 `8e3c908ad2471ff400bee43d8455b0c9ec3035ee3da407337255157bda33a8dc`).
- **Cell:** `D(10) mod 27` (`p^k = 3^3 = 27`, partial win `p1`: `D(10)` modulo a prime or prime power not determined by published congruences).
- **Existing published congruences:**
  - Koichi Yamamoto (1953): `D(2m) == 0 (mod 2)` (`D(10) == 0 (mod 2)`).
  - Bartlomiej Pawelski and Andrzej Szepietowski (`arXiv:2302.04615`, *J. Integer Seq.* 26, 2023): `D(9) == 6 (mod 210)` only; no new congruences for `D(10)`.
  - Bartlomiej Pawelski, Andrzej Szepietowski, and Blazej Szepietowski (`arXiv:2611.13887v1`, posted November 10, 2026, https://arxiv.org/abs/2611.13887, SHA-256 `c25cdade671f06642d12543a2b4cd7d15988a9a1ba51e2db3cbb9523c477ae23`): proves only squarefree prime congruences `D(10) == 106 (mod 210)` (`0 mod 2`, `1 mod 3`, `1 mod 5`, `1 mod 7`) via `|X| == |Fix(G, X)| (mod p)`, leaving `D(10) mod 9` (`3` open values) and `D(10) mod 27` (`9` open values: `1, 4, 7, 10, 13, 16, 19, 22, 25`) completely undetermined.
- **Our certified value:** `D(10) == 16 (mod 27)` (which immediately implies `D(10) == 7 (mod 9)` and matches `D(10) == 1 (mod 3)`), backed by the exact `P_81` Burnside sum `77588088181555989940 == 16 (mod 27)` in `object/d10_mod27_certificate.json` (SHA-256 `e0c8c761bd684d577f82d22d078f9f6269571d1756b2dfe797c723b037774ce8`).

## Not Claimed

- We do **not** claim the full exact integer `D(10) = A000372(10)` or `A003182(10)` (the full moonshot target).
- We do **not** bundle any congruence modulo other primes or prime powers; only the single prime-power cell `D(10) == 16 (mod 27)` (together with its immediate divisor reduction `mod 9 = 7` and `mod 3 = 1`) is claimed in this package.

## Credits

- **N. J. A. Sloane** and contributors to **OEIS A000372** (https://oeis.org/A000372) — sequence curation and references.
- **Koichi Yamamoto**, *Note on the order of free distributive lattices*, Sci. Rep. Kanazawa Univ. 2 (1953), 5–6 — parity of even-variable Dedekind numbers.
- **Doug H. Wiedemann**, *A computation of the eighth Dedekind number*, Order 8 (1991), 5–6 (https://doi.org/10.1007/BF00385808), and **R. Fidytek, A. W. Mostowski, R. Somla, and A. Szepietowski**, *Algorithms counting monotone Boolean functions*, Inform. Process. Lett. 79 (2001), 203–209 — `D(8)` and `B^k` decomposition identities.
- **Christian Jaekel**, *A computation of the ninth Dedekind number*, J. Comput. Algebra 6–7 (2023), 100006 (https://arxiv.org/abs/2304.00895), and **Lennart Van Hirtum, Patrick De Causmaecker, Jens Goemaere, Tobias Kenter, Heinrich Riebler, Michael Lass, and Christian Plessl**, *A computation of D(9) using FPGA Supercomputing* (https://arxiv.org/abs/2304.03039) — exact value `D(9) = 286386577668298411128469151667598498812366` used for `mod 27` calibration.
- **Andrzej Szepietowski**, *Fixes of permutations acting on monotone Boolean functions*, J. Integer Seq. 25 (2022), Art. 22.9.6 (https://arxiv.org/abs/2205.03868), **Bartlomiej Pawelski and Andrzej Szepietowski**, *Divisibility properties of Dedekind numbers*, J. Integer Seq. 26 (2023), Art. 23.7.7 (https://arxiv.org/abs/2302.04615), and **Bartlomiej Pawelski, Andrzej Szepietowski, and Blazej Szepietowski**, *Congruences for Dedekind numbers* (https://arxiv.org/abs/2611.13887, companion repository https://github.com/bpawelski/dedekind_congruences) — quotient-poset lemma `Fix(G, T^{P^n}) ~= T^{P^n / G}` and prime-modulus congruences `D(9) == 6 (mod 210)` and `D(10) == 106 (mod 210)`.
- **Alex Fihman, Lennart Van Hirtum, and Christian Plessl**, *Statistical Estimation of higher Dedekind Numbers* (https://arxiv.org/abs/2607.08446, July 2026) — 4-digit statistical estimate of `D(10)`.
- Contributor credit: `calgulbenkian`.
