# Refutation of the Szykula-Vorel Conjecture on Eulerian Synchronizing Automata (`n = 7, k = 5, rt = 24 > 23`)

## What

The explicit 7-state, 5-letter complete Eulerian DFA in object/eulerian_n7_k5_rt24.json is strongly connected, has in-degree 5 at every state, is synchronizing with exact reset threshold 24 > 23 = floor((7^2-3)/2), which contradicts Szykula-Vorel Conjecture 19 as stated (any alphabet size, n >= 3), and no more than that single counterexample is claimed.

## Check it yourself

From this package folder (requires only Python 3 stdlib and a C99 compiler `cc`):

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last output line: `PASS` (calibrates both independent referees on Szykula-Vorel `A_1 -> 11`, `A_2 -> 39`, `A_3 -> 83`, and non-Eulerian Cerny `C_5 -> 16`, then verifies completeness, strong connectivity, exact Eulerian in-degree `5` at every state, synchronizability, and exact subset-BFS reset threshold `24 > 23`).

## Compared to

- **Conjecture paper**: Marek Szykula and Vojtech Vorel, *An Extremal Series of Eulerian Synchronizing Automata*, DLT 2016, LNCS 9840, pp. 380-392 (https://arxiv.org/abs/1604.02879, Conjecture 19)
- **Living list**: Mikhail V. Volkov, *Synchronizing Automata: A Living List of Open Problems*, Item A6 (https://arxiv.org/abs/2508.15655, `arXiv:2508.15655v4`, Jan 13, 2026)
- **Recent survey**: Marek Szykula, *Synchronizing Automata: Bounds and Extremal Constructions*, Section 2.8.2 & Corollary 20 (https://arxiv.org/abs/2608.24245, `arXiv:2608.24245v1`, Aug 26, 2026)
- **Fetched**: `2026-11-17T05:53:59Z` (`HTTP 200`, SHA-256 `f46913e8f581de23f4a243230032c45718ada646cdc5b90dfb3a5d5d0a11308e` and `f67e7307d4606e357e89faaababd615a3e3fcaf3007cdbb63813bec7b4b4258d`)
- **Prior bound**: `rt(A) <= floor((n^2 - 3)/2)` (`23` at `n = 7`), conjectured tight for all `n >= 3` and all alphabet sizes

## Not claimed

- No improvement to Jarkko Kari's quadratic upper bound `n^2 - 3n + 3` (or Szykula's `n^2 - n log_2 n + O(n)` upper bound) for Eulerian synchronizing automata is claimed.
- Binary (`|Sigma| = 2`) or `|Sigma| <= 4` counterexamples at `n = 7` are not claimed (Szykula & Vorel already proved exhaustively that `rt(A) <= 23` for `n <= 7` when `|Sigma| <= 4`).
- An infinite family or asymptotic constant above `1/2` is not claimed here.

## Credits

- **Marek Szykula and Vojtech Vorel**, *An Extremal Series of Eulerian Synchronizing Automata*, DLT 2016 (https://arxiv.org/abs/1604.02879), for formulating Conjecture 19, constructing the `(n^2 - 3)/2` odd-`n` extremal series `A_m`, and mapping the small-`(n, |Sigma|)` computational frontier.
- **Jarkko Kari**, *Synchronizing finite automata on Eulerian digraphs*, Theoretical Computer Science 295 (2003), pp. 223-232, for establishing the quadratic synchronization theorem on Eulerian automata.
- **Mikhail V. Volkov**, *Synchronizing Automata: A Living List of Open Problems* (https://arxiv.org/abs/2508.15655), for curating Item A6 and contextualizing the Eulerian Cerny problem.
- **Vladimir V. Gusev and Pavel V. Martyugin**, for foundational extremal constructions on Eulerian and binary Eulerian synchronizing automata cited in `arXiv:1604.02879`.
