# REPRODUCE Skeptic Report — `reversed-zeckendorf-game-p-positions-a389618`

context: subagent

## 1. Quoted Definition from `README.md` and `how-we-built-it/PREREG.md`

Verbatim from `README.md`:

> "Indexing the Fibonacci numbers by F_1 = 1, F_2 = 2, F_3 = 3, F_4 = 5, ..., the game for a positive integer n >= 2 starts at the unique Zeckendorf decomposition of n into non-consecutive Fibonacci parts. Two players alternate moves under normal play (last player able to move wins), choosing either: (i) Split: replace one F_{i+1} with F_i + F_{i-1} for i >= 2, or replace one F_2 with 2 F_1; or (ii) Combine: replace F_{i-2} + F_{i+1} with 2 F_i for i > 2, or replace F_1 + F_3 with 2 F_2. The game terminates when all pieces are in the first bin (n copies of F_1)."

And the Branch B success criterion from `README.md` and `how-we-built-it/PREREG.md`:

> "CONFIRMED: ... (B) the exact 1st/2nd-player outcomes of the Reversed Zeckendorf game for every integer n contiguously in 130..250 (yielding one table of outcomes, vertex counts, and edge counts for n = 130..250 that extends OEIS A389618, A389619, and A389617 through n = 250), computed by two independently written solvers using distinct representations that both reproduce every vertex count, edge count, and win/loss outcome in Table A1 of arXiv:2309.12748v2 for all 2 <= n <= 129 and agree on every n in 130..250."

---

## 2. Independent Checker Written Before Reading Author Code

Before reading any solver in `how-we-built-it/` or `verify-it-yourself/`, an independent C++ checker and a Python calibration checker were implemented directly from the quoted rules in `README.md`:

1. **Method 1 — Explicit Naive Per-$n$ BFS from the Zeckendorf Initial State ($2 \le n \le 65$)**:
   - Represents states as full 12-tuples $(c_1, c_2, \dots, c_{12})$ with $\sum_{i=1}^{12} c_i F_i = n$.
   - Generates only states reachable by explicit BFS from the greedy Zeckendorf decomposition of $n$ using the literal Split ($F_2 \to 2 F_1$, $F_{i+1} \to F_i + F_{i-1}$) and Combine ($F_1 + F_3 \to 2 F_2$, $F_{i-2} + F_{i+1} \to 2 F_i$) transitions.
   - Evaluates normal-play winning/losing status in reverse topological order of the quadratic value invariant $\Phi(c) = \sum_{i=1}^{12} c_i F_i^2$ (since every Split move decreases $\Phi$ by $2 F_i F_{i-1} > 0$ or $2 > 0$, and every Combine move replaces $F_a + F_b = 2 F_i$ with $a \ne b$, decreasing $\Phi$ by $2 F_{i-1}^2 > 0$).
   - **Result**: Matches `object/reversed_zeckendorf_n2_250.tsv` on every vertex count, edge count, and winner for all $2 \le n \le 65$.

2. **Method 2 — Exhaustive 44-Bit $W/\Psi$-Stratified Independent Checker ($2 \le n \le 250$)**:
   - Packs $(c_2, \dots, c_{12})$ with $S(c) = \sum_{i=2}^{12} c_i F_i \le 250$ into a 44-bit key (shifts `{0, 7, 14, 20, 25, 30, 34, 37, 40, 42, 43}`), bucketed by $W(c) = \sum_{i=2}^{12} c_i (F_i - 1) = n - \sum_{i=1}^{12} c_i$ and ordered within each $W$-bucket by $\Psi(c) = \sum_{i=2}^{12} c_i (F_i^2 - F_i)/2$.
   - Verifies across all $21,890,964$ states and all $n \in [2, 250]$ that the only state in $\{c : S(c) \le n\}$ with zero incoming moves (reverse Split or reverse Combine) is the unique Zeckendorf decomposition $z(n)$, proving by finite induction on the strict topological rank $(W, \Psi)$ that $100\%$ of partitions of $n$ into $\{F_1, \dots, F_{12}\}$ are reachable from $z(n)$.
   - Computes the exact vertex count, edge count, and 1st/2nd-player normal-play winner for all $249$ contiguous integers $2 \le n \le 250$.
   - **Result**: Matches all $249$ rows of `object/reversed_zeckendorf_n2_250.tsv` identically ($0$ mismatches).

3. **Calibration & Integrity Checks on `object/reversed_zeckendorf_n2_250.tsv`**:
   - **SHA-256**: Verified `386a7153a5f084483101a9b9a1eab089f072a8106234535c4bf2b896beab82c1`.
   - **Row count & format**: Header `n	winner	edges	vertices` followed by $249$ contiguous rows $n = 2 \dots 250$.
   - **Table A1 baseline (`the-record-we-beat/snapshot.md`)**: Exact match on all $128$ published rows $2 \le n \le 129$ of Table A1 of `arXiv:2309.12748v2` (including $n=64$: $10,936$ vertices, $63,222$ edges, winner $2$; $n=65$: $11,744$ vertices, $68,351$ edges, winner $1$; $n=129$: $384,715$ vertices, $2,945,040$ edges, winner $2$).
   - **OEIS `A389617` (`b389617.txt`, recorded in `the-record-we-beat/snapshot.md`)**: Exact match on all $64$ published edge counts ($2 \le n \le 65$).
   - **OEIS `A389618` (`b389618.txt`, recorded in `the-record-we-beat/snapshot.md`)**: Exact match on all $49$ published second-player wins ($P$-positions) in $2 \le n \le 129$.
   - **OEIS `A389619` (`b389619.txt`, recorded in `the-record-we-beat/snapshot.md`)**: Exact match on all $79$ published first-player wins ($N$-positions) in $2 \le n \le 127$ (plus $a(1) = 1$ by OEIS convention).
   - **OEIS `A003107` identity**: Every vertex count for $2 \le n \le 250$ matches the exact partition DP count of $n$ into Fibonacci parts $\{F_1, \dots, F_{12}\}$ (reaching $21,890,964$ vertices and $209,975,689$ edges at $n = 250$).
   - **Extension summary ($130 \le n \le 250$)**: Across the $121$ new rows $130 \le n \le 250$, `awk` on `object/reversed_zeckendorf_n2_250.tsv` gives $91$ first-player wins (`winner = 1`) and $30$ second-player wins (`winner = 2`); overall for $2 \le n \le 250$, there are $170$ first-player wins and $79$ second-player wins.

---

## 3. Inspection and Execution of the Author's Two Solvers

After completing independent verification, the package's two solvers (`how-we-built-it/universal_delta_solver.cpp` and `how-we-built-it/colex_rank_solver.cpp`) and standalone verifier (`verify-it-yourself/check_table.py`) were inspected and executed:

1. **Architectural Independence Verification**:
   - **Solver 1 (`how-we-built-it/universal_delta_solver.cpp`)**: Eliminates $h_1 = n - \sum_{i=2}^{12} h_i F_i$, packs $(h_2, \dots, h_{12})$ into a 45-bit `uint64_t` key, stratifies states into $251$ levels by deficit $d = \sum_{i=2}^{12} h_i (F_i - 1)$, orders states within each level by descending $(m, \sum_{i=2}^{12} i \cdot h_i)$, resolves transitions via an open-addressed `FlatHash` table (with an explicit missing-key guard in `FlatHash::find`), and evaluates all $n \in [2, 250]$ simultaneously using 256-bit `WinBits` bitvectors, verifying output stream integrity on write.
   - **Solver 2 (`how-we-built-it/colex_rank_solver.cpp`)**: Evaluates each $n \in [2, 250]$ separately without any shared universal DAG, hash table, or packed 64-bit keys. Represents full partitions $(h_1, \dots, h_{12})$ of $n$ by their colexicographic rank $r \in [0, A003107(n) - 1]$ using a partition DP offset table `off_tbl[k][s][c]`. Exploits the fact that every Split and Combine move strictly decreases the highest modified coordinate $h_{i+1}$ by $1$ (so colex rank $r$ is a strict topological order), performing a bottom-up 1-bit-per-rank retrograde pass over $r = 0 \dots V-1$ followed by an explicit top-down reachability pass from the Zeckendorf seed at $r = V - 1$ down to $0$ (unconditionally verifying at runtime that `reachable_verts == V` and `reachable_edges == total_edges` for every $n$, and checking output stream status on write).
   - The two solvers use genuinely distinct state representations, topological invariants, neighbor lookup mechanisms, and evaluation algorithms.

2. **Compilation, Determinism, and Exact Reproduction**:
   - Both solvers compiled cleanly using the portable flags documented in `RUN_IT_YOURSELF.md` and `how-we-built-it/README.md` (`g++ -O3 -std=c++17 -Wall -Wextra` for `how-we-built-it/universal_delta_solver.cpp` and `g++ -O3 -fopenmp -std=c++17 -Wall -Wextra` for `how-we-built-it/colex_rank_solver.cpp`) with zero warnings.
   - Each solver was executed twice in succession:
     - `how-we-built-it/universal_delta_solver.cpp`: Run 1 completed in `10.2729 s`, Run 2 in `10.1711 s`. Both outputs produced SHA-256 `386a7153a5f084483101a9b9a1eab089f072a8106234535c4bf2b896beab82c1` and `diff -u` against `object/reversed_zeckendorf_n2_250.tsv` was empty.
     - `how-we-built-it/colex_rank_solver.cpp`: Run 1 completed in `25.4686 s`, Run 2 in `24.6739 s`. Both outputs produced SHA-256 `386a7153a5f084483101a9b9a1eab089f072a8106234535c4bf2b896beab82c1` and `diff -u` against `object/reversed_zeckendorf_n2_250.tsv` was empty.
   - The standalone verifier `verify-it-yourself/check_table.py` passed all positive checks ($n = 2 \dots 35$) and negative control checks.
   - All temporary build and scratch directories were removed after verification.

pass: true
