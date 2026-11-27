context: subagent

# Reproduction Panel Report — `non-attacking-queens-game-nimbers-a344227`

## 1. Execution of Commands in `claim/REPRODUCE.md`

All reproduction commands from `claim/REPRODUCE.md` were executed from a fresh shell in `claim/` and all compiled binaries were removed after testing.

### 1.1 Standalone Pure-Python First-Principles Verifier (`claim/code/check_claim.py`)

Command executed from `claim/`:
```sh
python3 code/check_claim.py result/toroidal_queens_and_margins.json
```

Observed output:
```text
[1/4] Verified toroidal_queens_nimbers (n=1..16, direct game-tree solve for n=1..12) in 0.51s
[2/4] Verified 21-orbit ply-3 strategy certificate for G(TQ_14) = 1 (all 144 replies in H_14 refuted) in 3.56s
[3/4] Verified central_strike_refutation_margins (n=8,10,12,14,16 + R_8..12 & R_14 non-refuting game trees) in 9.11s
[4/4] Verified planar_a344227_calibration (n=0..16, exact mex solve for n=0..8) in 0.34s
All checks passed in 13.51s.
PASS
```
Exit code: `0`.

### 1.2 Independent Pure-Python Full-Tree Solve (`claim/code/verify_tq14_python.py`)

Command executed from `claim/`:
```sh
python3 code/verify_tq14_python.py
```

Observed output:
```text
[Pure Python] G(TQ_ 4) = 0 (orbits=1, nodes=0, memo=1, 0.000s)
[Pure Python] G(TQ_ 6) = 0 (orbits=3, nodes=7, memo=8, 0.000s)
[Pure Python] G(TQ_ 8) = 0 (orbits=6, nodes=51, memo=52, 0.001s)
[Pure Python] G(TQ_10) = 0 (orbits=10, nodes=1453, memo=1454, 0.004s)
[Pure Python] G(TQ_12) = 0 (orbits=15, nodes=45306, memo=45307, 0.119s)
[Pure Python] G(TQ_14) = 1 (orbits=21, nodes=2087864, memo=2087865, 7.715s)
```
Exit code: `0`.

### 1.3 C++ Bitboard Solver A (`claim/code/solver_a_full.cpp`)

Compiled and executed from `claim/`:
```sh
g++ -O3 -march=native -fopenmp -std=c++20 code/solver_a_full.cpp -o code/solver_a_full
./code/solver_a_full 1
rm -f code/solver_a_full
```

Observed output:
```text
=== Solver A Full Run (evaluator-first: D4 + Zobrist + _pext_u64 dense leaf + OpenMP) ===

--- Part 1: Toroidal Queens G(TQ_n) for n = 1..16 ---
G(TQ_ 1) = 1 | H_ 1 winning replies =   0/  0 (orbits= 0, 0.053s, nodes=         0, hits=       0)
G(TQ_ 2) = 1 | H_ 2 winning replies =   0/  0 (orbits= 0, 0.023s, nodes=         0, hits=       0)
G(TQ_ 3) = 1 | H_ 3 winning replies =   0/  0 (orbits= 0, 0.023s, nodes=         0, hits=       0)
G(TQ_ 4) = 0 | H_ 4 winning replies =   4/  4 (orbits= 1, 0.022s, nodes=         1, hits=       0)
G(TQ_ 5) = 1 | H_ 5 winning replies =   0/  8 (orbits= 1, 0.024s, nodes=         1, hits=       0)
G(TQ_ 6) = 0 | H_ 6 winning replies =  16/ 16 (orbits= 3, 0.022s, nodes=         3, hits=       0)
G(TQ_ 7) = 1 | H_ 7 winning replies =   0/ 24 (orbits= 3, 0.022s, nodes=         3, hits=       0)
G(TQ_ 8) = 0 | H_ 8 winning replies =  36/ 36 (orbits= 6, 0.023s, nodes=       116, hits=       0)
G(TQ_ 9) = 1 | H_ 9 winning replies =   0/ 48 (orbits= 6, 0.025s, nodes=        12, hits=       0)
G(TQ_10) = 0 | H_10 winning replies =   8/ 64 (orbits=10, 0.022s, nodes=       506, hits=      39)
G(TQ_11) = 1 | H_11 winning replies =   0/ 80 (orbits=10, 0.024s, nodes=      5349, hits=     536)
G(TQ_12) = 0 | H_12 winning replies =  20/100 (orbits=15, 0.025s, nodes=     22539, hits=     972)
G(TQ_13) = 1 | H_13 winning replies =   0/120 (orbits=15, 0.028s, nodes=    125644, hits=    7118)
G(TQ_14) = 1 | H_14 winning replies =   0/144 (orbits=21, 0.070s, nodes=    632817, hits=   30987)
G(TQ_15) = 1 | H_15 winning replies =   0/168 (orbits=21, 0.142s, nodes=    451558, hits=    9231)
G(TQ_16) = 0 | H_16 winning replies = 196/196 (orbits=28, 1.644s, nodes=  22815796, hits=  903117)
```

### 1.4 C++ Bitboard Solver B (`claim/code/solver_b_tq.cpp` and `claim/code/solver_b_margins.cpp`)

Compiled and executed from `claim/`:
```sh
g++ -O3 -march=native -fopenmp -std=c++20 code/solver_b_tq.cpp -o code/solver_b_tq
./code/solver_b_tq
rm -f code/solver_b_tq
```

Observed output:
```text
=== Solver B (retrograde-dag: Bottom-Up W0..W7 + Exact 384-bit Lex-Canonical Key + Theorem S1 tau-leaf) ===
Built W0..W7 bottom-up in 0.248s
G(TQ_ 1) = 1  | H_ 1 winning replies =   0/  0  (0.169s, nodes=         0, hits=       0, tau_leaves=     0)
G(TQ_ 2) = 1  | H_ 2 winning replies =   0/  0  (0.128s, nodes=         0, hits=       0, tau_leaves=     0)
G(TQ_ 3) = 1  | H_ 3 winning replies =   0/  0  (0.106s, nodes=         0, hits=       0, tau_leaves=     0)
G(TQ_ 4) = 0  | H_ 4 winning replies =   4/  4  (0.108s, nodes=         1, hits=       0, tau_leaves=     0)  [e.g. (1,2)]
G(TQ_ 5) = 1  | H_ 5 winning replies =   0/  8  (0.106s, nodes=         1, hits=       0, tau_leaves=     0)
G(TQ_ 6) = 0  | H_ 6 winning replies =  16/ 16  (0.105s, nodes=         3, hits=       0, tau_leaves=     0)  [e.g. (1,2)]
G(TQ_ 7) = 1  | H_ 7 winning replies =   0/ 24  (0.108s, nodes=         3, hits=       0, tau_leaves=     0)
G(TQ_ 8) = 0  | H_ 8 winning replies =  36/ 36  (0.107s, nodes=       116, hits=       0, tau_leaves=     0)  [e.g. (1,2)]
G(TQ_ 9) = 1  | H_ 9 winning replies =   0/ 48  (0.107s, nodes=        12, hits=       0, tau_leaves=     0)
G(TQ_10) = 0  | H_10 winning replies =   8/ 64  (0.107s, nodes=       537, hits=      84, tau_leaves=     0)  [e.g. (1,5)]
G(TQ_11) = 1  | H_11 winning replies =   0/ 80  (0.110s, nodes=      5628, hits=     454, tau_leaves=     0)
G(TQ_12) = 0  | H_12 winning replies =  20/100  (0.127s, nodes=     26552, hits=     839, tau_leaves=     0)  [e.g. (1,6)]
G(TQ_13) = 1  | H_13 winning replies =   0/120  (0.201s, nodes=    133521, hits=    4041, tau_leaves=    14)
G(TQ_14) = 1  | H_14 winning replies =   0/144  (0.581s, nodes=    744999, hits=   24202, tau_leaves=     0)
G(TQ_15) = 1  | H_15 winning replies =   0/168  (0.637s, nodes=    535608, hits=    8226, tau_leaves=    11)
G(TQ_16) = 0  | H_16 winning replies = 196/196  (23.901s, nodes=  28894016, hits=  953914, tau_leaves=     1)  [e.g. (1,2)]
```

`claim/code/solver_b_margins.cpp` also compiled cleanly with `-O3 -march=native -fopenmp -std=c++20` and its binary was removed after verification.

## 2. Independent Verification of `claim/result/toroidal_queens_and_margins.json` Against `claim/claim.md`

An independent Python script was written from scratch directly from the problem definitions in `claim/claim.md` (without importing or reusing any code from `claim/code/`) to verify every number and constraint in `claim/result/toroidal_queens_and_margins.json`:

1. **Toroidal Queens Graph $TQ_n$ and Residual Board $H_n = TQ_n \setminus N[(0,0)]$ ($n = 1 \dots 16$)**:
   - Constructed $TQ_n$ directly as sets of coordinate pairs $(r, c) \in \{0 \dots n-1\}^2$ where $(r_1, c_1)$ and $(r_2, c_2)$ attack each other iff $r_1 = r_2$, $c_1 = c_2$, $(r_1 - c_1) \equiv (r_2 - c_2) \pmod n$, or $(r_1 + c_1) \equiv (r_2 + c_2) \pmod n$.
   - Verified that $|N[(0,0)]| = 1$ for $n = 1$, $4n - 3$ for odd $n \ge 3$, and $4n - 4$ for even $n \ge 2$, matching `closed_neighborhood_size` and `Hn_live_squares` across all $n = 1 \dots 16$.
   - Verified that the $D_4((0,0))$ orbit counts on $H_n$ match `Hn_d4_orbits` ($0, 0, 0, 1, 1, 3, 3, 6, 6, 10, 10, 15, 15, 21, 21, 28$) and that all reported values $G(TQ_1 \dots TQ_{16}) = (1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0)$ and winning reply counts ($20/100$ at $n = 12$, $0/144$ at $n = 14$, $196/196$ at $n = 16$) match `claim/claim.md` and the output of both C++ solvers.
2. **Independent Certificate Check for $G(TQ_{14}) = 1$**:
   - Independently verified that the 21 $D_4((0,0))$ orbits in `tq14_counterexample_certificate` are pairwise disjoint and partition all 144 live squares of $H_{14}$.
   - For each orbit representative $u_2$, independently verified that the certified reply $w_3$ is a legal surviving vertex in $M_1 = H_{14} \setminus N[u_2]$, that the residual set $P_1 = M_1 \setminus N[w_3]$ has the exact reported cardinality, and solved each of the 21 residual positions $P_1$ via an independently written game-tree recursion to confirm all 21 are P-positions. This confirms $G(TQ_{14}) = 1 \ne 14 \bmod 2$, refuting Conjecture T1.
3. **Planar Central-Strike Refutation Margins $R_n = Q_n \setminus N[c^*]$ ($n \in \{8, 10, 12, 14, 16\}$) and OEIS A344227 ($n = 0 \dots 16$)**:
   - Constructed $Q_n$ and $R_n$ from first principles for $c^* = (n/2 - 1, n/2 - 1)$, confirming $|R_n| = (n - 2)^2$ and verifying that `refuting_squares_rc` and `non_refuting_squares_rc` are disjoint, partition $R_n$, and match every number reported in `claim/claim.md`: $0/36$ at $n = 8$, $8/64$ at $n = 10$, $100/100$ at $n = 12$, $140/144$ at $n = 14$ (with non-refuting replies $(4,7), (7,4), (7,8), (8,7)$), and $146/196$ at $n = 16$ ($146$ refuting and $50$ non-refuting replies), as well as planar $A344227(0 \dots 16) = (0, 1, 1, 2, 1, 3, 1, 2, 3, 1, 0, 1, 0, 1, 0, 1, 0)$.

Every command succeeded, all independent checks matched `claim/claim.md` and `claim/result/toroidal_queens_and_margins.json` without discrepancy, and no compiled binaries remain in `claim/`.

pass: true
