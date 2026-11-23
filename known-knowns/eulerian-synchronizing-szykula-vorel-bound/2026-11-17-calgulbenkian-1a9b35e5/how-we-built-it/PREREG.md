# Pre-Registration: `eulerian-synchronizing-szykula-vorel-bound`

frozen_utc: 2026-11-17T05:53:59Z
target_id: eulerian-synchronizing-szykula-vorel-bound
null_test: not needed because exact finite mathematical counterexample verified by exhaustive 2^n subset BFS

## Verbatim Gates

1. Explicit complete DFA `A = (Q, Sigma, delta)` with `3 <= n = |Q| <= 30` states that is strongly connected, Eulerian (every state has exact incoming edge count `|Sigma|`), and synchronizing.
2. Exact subset-BFS reset threshold `rt(A) > floor((n^2 - 3) / 2)`, confirmed independently by two standalone verifiers (Python stdlib `frozenset` forward/backward BFS + Hierholzer check and C99 `uint32_t` bitmask BFS + Floyd-Warshall check), both calibrated on Szykula-Vorel `A_1 (n=5 -> 11)`, `A_2 (n=9 -> 39)`, `A_3 (n=13 -> 83)`, and non-Eulerian Cerny `C_5 (rt=16, Eulerian=false)`.
