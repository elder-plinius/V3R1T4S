# How We Found It (`HOW_WE_FOUND_IT.md`)

*contributor text, unverified*

## 1. The Brief and Target Structure

The Non-Attacking Queens game (OEIS A344227; Node-Kayles on the $n \times n$ queens graph $Q_n$ or toroidal queens graph $TQ_n$) asks players to alternately place non-attacking queens until no unattacked square remains. On the toroidal board $TQ_n = \mathrm{Cay}(\mathbb{Z}_n \times \mathbb{Z}_n, S_n)$, vertex-transitivity implies every opening move is isomorphic to $(0,0)$ and leaves the residual graph $H_n = TQ_n \setminus N[(0,0)]$, so $G(TQ_n) \in \{0, 1\}$, with $G(TQ_n) = 1$ iff $H_n$ is a P-position (0 winning replies for Player 2 in $H_n$).

In Section 6.7 of his 2026 paper, Tavis Rudd computed $G(TQ_n)$ for $n = 1 \dots 10$ (`1, 1, 1, 0, 1, 0, 1, 0, 1, 0`) and formulated **Conjecture T1 (Toroidal Parity)**: $G(TQ_n) = n \bmod 2$ for all $n \ge 4$. In Section 6.6, Rudd analyzed the planar central-strike residual board $R_n = Q_n \setminus N[c^*]$ ($c^* = (n/2-1, n/2-1)$) for even $n$, finding refutation margins $0/36$ at $n = 8$, $8/64$ at $n = 10$, $100/100$ at $n = 12$, and $0/256$ at $n = 18$. The draft left $R_{14}$ and $R_{16}$ open.

## 2. What Worked and What Failed

1. **Lens 1 (`evaluator-first`)**:
   - We built a bit-parallel C++20 solver (`how-we-built-it/solver_a_full.cpp`) combining 8-way $D_4$ board-symmetry Zobrist canonicalization, a lockless 64-bit fingerprint transposition table, and a hardware BMI2 `_pext_u64` local bitmask leaf evaluator for subpositions with $k \le 14$ surviving squares.
   - Folding the second-ply moves of $H_n = TQ_n \setminus N[(0,0)]$ by the 8 symmetries of $D_4((0,0))$ reduced $H_{14}$ ($144$ squares) to $21$ orbits and $H_{16}$ ($196$ squares) to $28$ orbits.
   - While $G(TQ_{12}) = 0$ ($20/100$ winning replies in $H_{12}$) matched Conjecture T1, at **$n = 14$** the solver discovered in `0.077s` (`631,430` nodes) that **all 21 $D_4((0,0))$ orbits of $H_{14}$ ($0/144$ replies) lose for Player 2**, so $H_{14}$ is a P-position and **$G(TQ_{14}) = 1 \ne 14 \bmod 2$**—an explicit counterexample refuting Conjecture T1! At $n = 16$, parity resumes with $G(TQ_{16}) = 0$ ($196/196$ winning replies in $H_{16}$).
   - Extracting the explicit winning Player 1 reply $w_3$ for each of the 21 $D_4((0,0))$ orbit representatives $u_2 \in H_{14}$ produced a compact certificate that pure Python verifies in ~3.5 seconds from scratch.
2. **Lens 2 (`retrograde-dag`)**:
   - To eliminate any possibility of Zobrist hash collisions or shared leaf-evaluator bugs, we built an independent solver suite (`how-we-built-it/solver_b_tq.cpp` and `how-we-built-it/solver_b_margins.cpp`) that precomputes complete Node-Kayles win/loss bitset tables $W_0 \dots W_7$ and $W_0 \dots W_8$ (`32 MiB`, covering all $2^{28}$ labeled graphs on $\le 8$ vertices) bottom-up at startup, uses exact collision-free 256-bit and 384-bit lexicographical canonical keys, and applies fixed-point-free $\tau$-reflection P-position detection (Theorem S1).
   - Solver B reproduced 100% of Solver A's toroidal values $G(TQ_1 \dots TQ_{16})$, all $H_n$ winning-reply counts, the planar OEIS A344227($0 \dots 16$) calibration sequence, and the exact planar central-strike refutation margins: **`140/144` on $R_{14}$** (where the only 4 non-refuting squares $(4,7), (7,4), (7,8), (8,7)$ form two mutual winning-reply pairs!) and **`146/196` on $R_{16}$**.
