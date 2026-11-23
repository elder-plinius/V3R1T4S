context: subagent

# Criterion Panelist Report — non-attacking-queens-game-nimbers-a344227

confirmed_scope: Full confirmation of target success_criterion clause (3) and partial_wins p1: two independent C++ bitboard solvers plus a pure-Python strategy-certificate verifier establish the exact toroidal Sprague-Grundy values G(TQ_1..TQ_{16}) = (1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0) — providing both the explicit even-n counterexample G(TQ_{14}) = 1 (0/144 winning replies in H_{14}) that refutes Rudd's Toroidal Conjecture T1 and the exact values G(TQ_n) for all even n = 12, 14, 16 calibrated against G(TQ_1..TQ_{10}) — as well as the exact planar central-strike refutation margins 140/144 on R_{14} and 146/196 on R_{16} calibrated against 0/36 on R_8, 8/64 on R_{10}, 100/100 on R_{12}, and planar A344227(0..16).

## 1. Word-for-Word Comparison Against `success_criterion`

The target's `success_criterion` in `claim/claim.md` is a three-way disjunction:
- **Clause (1)**: Exact Sprague-Grundy value $a(18) = G(Q_{18})$ or the 1st/2nd-player win/loss outcome of $Q_{20}$, established by two independently written bitboard solvers that both reproduce A344227 for $n = 0 \dots 17$.
  - *Status*: Not claimed.
- **Clause (2)**: Kernel-checked formal proof (Lean, Rocq, or Isabelle) of Rudd's full Toroidal Conjecture T1 ($G(TQ_n) = n \bmod 2$ for all $n \ge 4$).
  - *Status*: Refuted rather than proved (Conjecture T1 is false at $n = 14$).
- **Clause (3)**: *"an explicit toroidal counterexample refuting Conjecture T1 (necessarily at an even n), or the exact computation of G(TQ_n) for every even n = 12, 14, 16, by two independent bitboard solvers that both reproduce G(TQ_n) for n = 1..10."*
  - *Status*: **Fully satisfied on both sub-clauses of (3)**:
    1. **Explicit even-$n$ toroidal counterexample refuting Conjecture T1**: At even $n = 14$, Conjecture T1 predicts $G(TQ_{14}) = 14 \bmod 2 = 0$, whereas the claim establishes $G(TQ_{14}) = 1$, because all $144$ legal second-player replies in $H_{14} = TQ_{14} \setminus N[(0,0)]$ across all $21$ $D_4((0,0))$ orbits are N-positions ($0/144$ winning replies for Player 2, so $H_{14}$ is a P-position). In addition to independent evaluation by both C++ bitboard solvers, `claim/result/toroidal_queens_and_margins.json` provides an explicit 21-orbit ply-3 winning strategy certificate (`tq14_counterexample_certificate`) giving a concrete winning Player 1 response $w_3$ for each orbit representative $u_2$, verified from first principles in pure Python by `claim/code/check_claim.py`.
    2. **Exact computation of $G(TQ_n)$ for every even $n = 12, 14, 16$**: The claim computes $G(TQ_n)$ for all $n = 1 \dots 16$, establishing in particular for every even $n \in \{12, 14, 16\}$:
       - $G(TQ_{12}) = 0$ ($20/100$ winning replies in $H_{12}$),
       - $G(TQ_{14}) = 1$ ($0/144$ winning replies in $H_{14}$),
       - $G(TQ_{16}) = 0$ ($196/196$ winning replies in $H_{16}$),
        as well as the odd values $G(TQ_{11}) = G(TQ_{13}) = G(TQ_{15}) = 1$.
    3. **Calibration on $G(TQ_n)$ for $n = 1 \dots 10$**: Both independent bitboard solvers (`claim/code/solver_a_full.cpp` and `claim/code/solver_b_tq.cpp`) and the standalone Python verifier (`claim/code/check_claim.py`) reproduce the entire known sequence $G(TQ_1 \dots TQ_{10}) = (1, 1, 1, 0, 1, 0, 1, 0, 1, 0)$.

## 2. Word-for-Word Comparison Against `partial_wins` (`p1`)

The target's `partial_wins` entry `p1` in `claim/claim.md` requires:
- *"Compute the exact toroidal values G(TQ_{12}) and G(TQ_{14}) (testing the even half of Conjecture T1 beyond n = 10)"*:
  - **Satisfied**: $G(TQ_{12}) = 0$ ($20/100$ winning replies in $H_{12}$) and $G(TQ_{14}) = 1$ ($0/144$ winning replies in $H_{14}$), plus $G(TQ_{16}) = 0$ ($196/196$ winning replies in $H_{16}$).
- *"plus the exact central-strike refutation margins on R_{14} and R_{16} (Section 6.6 of Rudd 2026: the number of legal replies on R_n = Q_n minus N[c*] that leave a P-position, calibrated against Rudd's published margins 0/36 at n = 8, 8/64 at n = 10 and 100/100 at n = 12), verified by two independent bitboard solvers"*:
  - **Satisfied**: Using $c^* = (n/2 - 1, n/2 - 1)$ in $0$-based coordinates, both `claim/code/solver_a_full.cpp` and `claim/code/solver_b_margins.cpp` reproduce the published central-strike refutation margins $0/36$ on $R_8$, $8/64$ on $R_{10}$, and $100/100$ on $R_{12}$, and establish the exact margins $140/144$ on $R_{14}$ (all replies except $(4,7), (7,4), (7,8), (8,7)$ leave a P-position) and $146/196$ on $R_{16}$ ($146$ refuting and $50$ non-refuting replies, all explicitly enumerated in `claim/result/toroidal_queens_and_margins.json`).

## 3. Verification Method, Scope, Parameters, Format, and Independence Audit

1. **Vertex-transitivity reduction for $TQ_n$**:
   - In accordance with `verification_method`, since $TQ_n$ is vertex-transitive, every opening move is isomorphic to $(0,0)$, leaving $H_n = TQ_n \setminus N[(0,0)]$ of size $(n-2)^2$ for even $n \ge 4$ and $(n-1)(n-3)$ for odd $n \ge 3$. Thus $G(TQ_n) = 1$ iff $H_n$ is a P-position ($0$ winning replies in $H_n$), and $G(TQ_n) = 0$ iff $H_n$ has at least one winning reply leaving a P-position. Both solvers evaluate all $D_4((0,0))$ orbits of $H_n$ and report both $G(TQ_n) \in \{0, 1\}$ and the exact count of winning replies in $H_n$.
2. **Heap-sum / exact mex evaluation for standard planar boards $Q_n$**:
   - In accordance with `verification_method`, neither solver relies on boolean alpha-beta on $Q_n$ alone for standard-board nimbers $a(n) = G(Q_n)$. Both `claim/code/solver_a_full.cpp` (`solve_planar_nimber` via `solve_heap_win`) and `claim/code/solver_b_margins.cpp` (`solve_planar_nimber_b` via `solve_heap_node`) certify $a(n) = G(Q_n)$ via the heap-sum game $Q_n + \operatorname{Nim}(k)$ for $k = 0, 1, \dots, a(n)$, while `claim/code/check_claim.py` also performs direct recursive mex evaluation (`solve_planar_nimber_exact`) for $n = 0 \dots 8$.
   - *Calibration range note*: The combined calibration sentence in `verification_method` mentions reproducing $G(TQ_n)$ for $n = 1 \dots 10$, A344227 for $n = 0 \dots 17$, and the published central-strike refutation margins for $n = 8, 10, 12$ across targets (1), (3), and `p1`. The package reproduces $G(TQ_n)$ for $n = 1 \dots 10$, the central-strike refutation margins for $n = 8, 10, 12$, and planar A344227 for $n = 0 \dots 16$ (the $n = 0 \dots 17$ planar requirement belongs specifically to clause (1) for $a(18)$ / $Q_{20}$, whereas clause (3) specifies $G(TQ_n)$ for $n = 1 \dots 10$ and `p1` specifies the margins at $n = 8, 10, 12$).
3. **Architectural independence of the solvers and verifier**:
   - `claim/code/solver_a_full.cpp` (Solver A — evaluator-first): Uses a 6-word 384-bit bitboard (`Mask384`), BMI2 `_pext_u64` extraction into a recursive scalar leaf evaluator (`eval_local16_rec`, `eval_local16_is_g1`, `eval_local_grundy_rec` for $k \le 15$), 128-bit SplitMix64 Zobrist $D_4$-minimum hashing mixed into a 64-bit key, a flat lockless `std::atomic<u64>` fingerprint transposition table, and Enhanced Transposition Cutoff (ETC).
   - `claim/code/solver_b_tq.cpp` (Solver B for $TQ_n$ — retrograde-DAG): Precomputes a bottom-up Node-Kayles table $W_0 \dots W_7$ (`BottomUpW7`) over all $2^{\binom{k}{2}}$ labeled graphs on $k \le 7$ vertices, detects P-positions via fixed-point-free non-attacking involutive point reflection $\tau(r,c) = (-r \bmod n, -c \bmod n)$ (Theorem S1 / Copying Lemma), canonicalizes boards by computing the exact lexicographically minimal 384-bit `BitBoard324` across the $8$ $D_4((0,0))$ bit-permutations without Zobrist hashing, and stores full 384-bit canonical keys in a collision-free open-addressed table (`ExactSlot`).
   - `claim/code/solver_b_margins.cpp` (Solver B for $R_n$ and planar A344227 — retrograde-DAG): Precomputes a 32 MiB bottom-up Node-Kayles bitset table $W_0 \dots W_8$ (`BottomUpW8`) over all $2^{28}$ labeled graphs on $k \le 8$ vertices with single-instruction `_pext_u32` subgraph projection, applies embedded odd-subboard $\tau$-reflection leaf detection and canonical quotienting on $S = [0 \dots n-2]^2$ under $\tau(r,c) = (n-2-r, n-2-c)$, and stores full 256-bit canonical `Board256` keys in a lock-striped collision-free table (`ExactBoardSlot`).
   - `claim/code/check_claim.py` (Standalone Python verifier): Uses only the Python standard library and arbitrary-precision integer bitmasks to verify every schema constraint, coordinate list, symmetry invariant, direct game-tree evaluation for $TQ_1 \dots TQ_{12}$ and $R_8, R_{10}, R_{12}$, the 4-square mutual reply certificate on $R_{14}$, the 21-orbit ply-3 winning strategy certificate refuting Conjecture T1 at $TQ_{14}$, and exact mex values for planar $A344227(0 \dots 8)$.
4. **Package format and file size limits**:
   - All files in `claim/` (`claim/claim.md`, `claim/result/toroidal_queens_and_margins.json`, `claim/code/solver_a_full.cpp`, `claim/code/solver_b_tq.cpp`, `claim/code/solver_b_margins.cpp`, and `claim/code/check_claim.py`) are well under the 1 MB file size limit (the largest file is `claim/result/toroidal_queens_and_margins.json` at ~58 KB).

## 4. Conclusion

The claim satisfies both branches of `success_criterion` clause (3) and every requirement of `partial_wins` (`p1`).

pass: true
