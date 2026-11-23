# Pre-Registration (`PREREG.md`)

- **Frozen at (UTC)**: `2026-11-21T16:57:58+00:00`
- **Target ID**: `non-attacking-queens-game-nimbers-a344227`
- **Null test**:
null_test: not needed because the claim consists of exact deterministic game-theoretic values (Sprague-Grundy nimbers and exhaustive finite game-tree win/loss counts) verified by two independent exact bitboard solvers and calibrated against published exact ground truth.

## 1. Success Criterion & Enumerated Partial Wins (Copied Verbatim from `repo/bank/targets.json`)

- **Success criterion**:
  `CONFIRMED: any one of: (1) the exact Sprague-Grundy value a(18) = G(Q_{18}) (certified via exact mex evaluation or heap-sum P-position verification of Q_{18} + Nim(a(18)) plus N-position verification of Q_{18} + Nim(k) for 0 <= k < a(18)) or the 1st/2nd-player win/loss outcome of Q_{20}, established by two independently written bitboard solvers that both reproduce A344227 for n = 0..17; OR (2) a kernel-checked formal proof (Lean, Rocq or Isabelle; no sorry, admitted goals or axioms beyond the system's standard ones) of Rudd's full Toroidal Conjecture T1 (G(TQ_n) = n mod 2 for all n >= 4); OR (3) an explicit toroidal counterexample refuting Conjecture T1 (necessarily at an even n), or the exact computation of G(TQ_n) for every even n = 12, 14, 16, by two independent bitboard solvers that both reproduce G(TQ_n) for n = 1..10.`
- **Partial win `p1`**:
  `Compute the exact toroidal values G(TQ_{12}) and G(TQ_{14}) (testing the even half of Conjecture T1 beyond n = 10), plus the exact central-strike refutation margins on R_{14} and R_{16} (Section 6.6 of Rudd 2026: the number of legal replies on R_n = Q_n minus N[c*] that leave a P-position, calibrated against Rudd's published margins 0/36 at n = 8, 8/64 at n = 10 and 100/100 at n = 12), verified by two independent bitboard solvers.`

## 2. Exact Checker, Calibration Gates, and Acceptance Thresholds

1. **Two Independently Written Bitboard Solvers**:
   - **Solver A (`attempts/evaluator-first/`)**: Bit-parallel C++20 solver using $D_4$ board-automorphism canonicalization, Zobrist-keyed flat lockless transposition table, and precomputed complete Node-Kayles bitset tables $W_0 \dots W_8$ (`32 MiB`) with BMI2 `_pext_u64` dense leaf evaluation (`getK`).
   - **Solver B (`attempts/retrograde-dag/`)**: Independently written C++20 solver using a distinct state encoding and canonicalization algorithm (induced-graph degree-sequence / 1-WL neighborhood-signature canonicalization and embedded odd-subboard $\tau$-reflection quotient on $S = [0 \dots n-2]^2$, with an independent transposition table and distinct move-ordering/leaf architecture).
2. **Mandatory Calibration Suite (0 Discrepancies Required)**:
   - **Toroidal calibration**: Both solvers must reproduce $G(TQ_n)$ for $n = 1..10$: `1, 1, 1, 0, 1, 0, 1, 0, 1, 0` (and odd $n = 11, 13, 15$: `1, 1, 1`).
   - **Central-strike refutation-margin calibration**: Both solvers must reproduce Rudd's published central-strike refutation margins on $R_n = Q_n \setminus N[c^*]$ ($c^* = (n/2 - 1, n/2 - 1)$): `0/36` at $n = 8$, `8/64` at $n = 10$, and `100/100` at $n = 12$.
   - **Standard-board calibration**: Both solvers must reproduce $A344227(n)$ across the published calibration range (exact `mex` and/or heap-sum $Q_n + \text{Nim}(k)$ verification for $n = 0..16$: `0, 1, 1, 2, 1, 3, 1, 2, 3, 1, 0, 1, 0, 1, 0, 1, 0`, plus checking $n = 17$ within the laptop budget or documenting exact scaling).
3. **Decision Rule**:
   - **Full win (`solution_claim` via Branch (3))**: Both independent solvers reproduce `G(TQ_n)` for `n = 1..10` and agree with `0` discrepancies on either an explicit toroidal counterexample refuting Conjecture T1 (`G(TQ_n) != n mod 2` for some even $n \ge 12$, i.e. $G(TQ_n) = 1$) OR the exact values of $G(TQ_{12})$, $G(TQ_{14})$, and $G(TQ_{16})$.
   - **Partial win (`partial_win_claim` via `p1`)**: Both independent solvers reproduce the calibration suite (`G(TQ_1..10)` and the central-strike refutation margins `0/36` at $n=8$, `8/64` at $n=10$, `100/100` at $n=12$, and planar $A344227$ calibration) and agree with `0` discrepancies on all four target quantities:
     1. Exact toroidal value $G(TQ_{12})$,
     2. Exact toroidal value $G(TQ_{14})$,
     3. Exact central-strike refutation margin on $R_{14}$ (and full list of refuting replies $(r, c) \in R_{14}$),
     4. Exact central-strike refutation margin on $R_{16}$ (and full list of refuting replies $(r, c) \in R_{16}$).
   - **Resource & Disk Cap (`LOCAL_RULES.md`)**: All solver runs stay strictly under 5.5 GiB total RAM (half of free memory) and under 10 GiB total generated disk files.
