# Reversed Zeckendorf Game Outcomes, Vertex Counts, and Edge Counts for $2 \le n \le 250$ (`reversed-zeckendorf-game-p-positions-a389618`)

## What

- **Target ID**: `reversed-zeckendorf-game-p-positions-a389618`
- **Instance / Cell**: Contiguous integer range $2 \le n \le 250$ (reproducing $2 \le n \le 129$ and newly resolving $130 \le n \le 250$)
- **Value Achieved**:
  - Single verified table `object/reversed_zeckendorf_n2_250.tsv` (SHA-256 `386a7153a5f084483101a9b9a1eab089f072a8106234535c4bf2b896beab82c1`, 4,920 bytes) giving `(n, winner, edges, vertices)` for all $2 \le n \le 250$.
  - **30 new second-player winning starting numbers ($P$-positions, `PROVED-HERE`, extending OEIS `A389618` for $a(50)\dots a(79)$ across $130 \le n \le 250$)**:
    `131, 136, 137, 142, 146, 152, 156, 157, 165, 166, 167, 173, 174, 175, 190, 197, 205, 206, 212, 220, 221, 225, 228, 231, 233, 234, 238, 240, 244, 245`
  - **91 new first-player winning starting numbers ($N$-positions, `PROVED-HERE`, extending OEIS `A389619` for $a(81)\dots a(171)$ across $130 \le n \le 250$)**:
    `130, 132, 133, 134, 135, 138, 139, 140, 141, 143, 144, 145, 147, 148, 149, 150, 151, 153, 154, 155, 158, 159, 160, 161, 162, 163, 164, 168, 169, 170, 171, 172, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 191, 192, 193, 194, 195, 196, 198, 199, 200, 201, 202, 203, 204, 207, 208, 209, 210, 211, 213, 214, 215, 216, 217, 218, 219, 222, 223, 224, 226, 227, 229, 230, 232, 235, 236, 237, 239, 241, 242, 243, 246, 247, 248, 249, 250`
  - **DAG edge counts (`PROVED-HERE`)**: Extends OEIS `A389617` (`b389617.txt`, $2 \le n \le 65$) by 185 terms ($66 \le n \le 250$), of which 121 terms ($130 \le n \le 250$) extend Table A1 of `arXiv:2309.12748v2` ($2 \le n \le 129$), reaching $209,975,689$ directed edges and $21,890,964$ vertices at $n = 250$, and satisfies the exact identity $A389617(n) = \sum_{i=2}^{12}\bigl(A003107(n - F_i) + A003107(n - 2F_i)\bigr)$.
- **Confirmed Scope (`panel/gate.md`)**:
  Full success criterion (Branch B) met for reversed-zeckendorf-game-p-positions-a389618: exact 1st/2nd-player normal-play outcomes, DAG vertex counts, and DAG edge counts of the Reversed Zeckendorf Game are determined contiguously for all integers 2 <= n <= 250 in object/reversed_zeckendorf_n2_250.tsv, reproducing all 128 published rows (2 <= n <= 129) of Table A1 of arXiv:2309.12748v2 and all published entries for n >= 2 of OEIS A389617, A389618, and A389619 while extending all three sequences contiguously across 130 <= n <= 250 via two independent solvers with distinct state representations that agree on every n in 2..250.

## Check it yourself

Run from the root of this package:
```sh
sh verify-it-yourself/run_checks.sh
```
- **What `run_checks.sh` verifies**:
  1. Runs `python3 verify-it-yourself/check_table.py object/reversed_zeckendorf_n2_250.tsv` (verifies exact DP vertex and edge identities for $2 \le n \le 250$, all 128 published Table A1 / OEIS rows $2 \le n \le 129$, Theorem 1.1, literal BFS game evaluation for $2 \le n \le 35$, all 121 extension outcomes $130 \le n \le 250$, and 4 built-in negative controls including flipping the frontier winner at $n = 130$).
  2. Runs an explicit CLI negative-control test confirming `check_table.py` rejects a mutated copy of `object/reversed_zeckendorf_n2_250.tsv` with `winner(130)` flipped.
  3. Compiles and runs **Solver 1** (`how-we-built-it/universal_delta_solver.cpp`) and verifies `diff -u` against `object/reversed_zeckendorf_n2_250.tsv` is empty.
  4. Compiles and runs **Solver 2** (`how-we-built-it/colex_rank_solver.cpp`) and verifies `diff -u` against `object/reversed_zeckendorf_n2_250.tsv` is empty.
- **Expected output**: `PASS` on the final line (exit code `0`).
- **Expected runtime (`NUMERICAL`)**: ~38 seconds wall clock (`121,968 kbytes` peak RSS; requires `python3 >= 3.9` and `g++` with C++17 and OpenMP support).

## Compared to

- **Previous best published values (`KNOWN`)**:
  - Table A1 of Zoë X. Batterman, Aditya Jambhale, Steven J. Miller, Akash L. Narayanan, Kishan Sharma, Andrew K. Yang, and Chris Yao, *"The Reversed Zeckendorf Game"*, `https://arxiv.org/abs/2309.12748` (`arXiv:2309.12748v2`; *The Fibonacci Quarterly* 63(2):215–239, 2025, `https://www.tandfonline.com/doi/abs/10.1080/00150517.2024.2417193`), which tabulates 1st/2nd-player outcomes, DAG vertex counts, and DAG edge counts for $2 \le n \le 129$ (stopping at $n = 129$ with $384,715$ vertices, $2,945,040$ edges, and `winner = 2`).
  - OEIS `https://oeis.org/A389618` ($P$-positions for $2 \le n \le 129$, 49 terms), `https://oeis.org/A389619` ($N$-positions for $2 \le n \le 127$, 79 terms with $n \ge 2$, plus $a(1) = 1$ by OEIS convention), and `https://oeis.org/A389617` (DAG edge counts for $2 \le n \le 65$, 64 terms).
- **Snapshot fetched UTC**: `2026-11-08T01:14:31Z` (HTML status pages and abstract), `2026-11-08T01:14:43Z` (LaTeX source archive), and `2026-11-08T01:15:19Z` (OEIS b-files); see `the-record-we-beat/snapshot.md`.

## Not claimed

- This package settles **Branch B** (exact computational extension for all $130 \le n \le 250$) of `reversed-zeckendorf-game-p-positions-a389618`.
- It does **not** settle **Branch A** (the qualitative Batterman et al. Conjecture 1.2 on whether OEIS `A389618` is infinite or finite as $n \to \infty$, or Conjecture 1.3 on the limiting fraction of Player 1 wins), nor does it compute outcomes for $n \ge 251$.
- Note on $n = 1$: In OEIS `A389619`, $a(1) = 1$ is listed by convention; under the normal-play Reversed Zeckendorf Game definition in Branch B ($n \ge 2$), the single-chip state at $n = 1$ has zero legal moves, so this package restricts its table and reproduction claims to $2 \le n \le 250$.

## Credits

- **Credit**: RainRat
- **Prior work cited**:
  - Zoë X. Batterman, Aditya Jambhale, Steven J. Miller, Akash L. Narayanan, Kishan Sharma, Andrew K. Yang, and Chris Yao (2025), *"The Reversed Zeckendorf Game"*, *The Fibonacci Quarterly* 63(2):215–239 (`https://www.tandfonline.com/doi/abs/10.1080/00150517.2024.2417193`; preprint `https://arxiv.org/abs/2309.12748`).
  - OEIS sequences `https://oeis.org/A389617`, `https://oeis.org/A389618`, `https://oeis.org/A389619`, and `https://oeis.org/A003107` (*The On-Line Encyclopedia of Integer Sequences*).
- **Software used**: GCC (`g++` with C++17 and OpenMP) and Python $\ge 3.9$ standard library.
