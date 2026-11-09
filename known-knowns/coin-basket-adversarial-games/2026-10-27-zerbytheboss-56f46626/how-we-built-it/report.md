# Lens 1 Report: High-Performance Compiled Rust Exact Decision-Bracket Minimax Solver

claim level: solution_claim

## 1. Executive Summary

Lens 1 implemented a zero-allocation, compiled Rust minimax solver operating directly over the quotiented game graph of Ruediger Jehn's adversarial coin-basket games.
The game graph exploits the full $S_3$ permutation symmetry of the 3 baskets by canonizing basket sums $(s_0 \le s_1 \le s_2)$ and tracking the unplaced coin bitmask `mask` (with $s_2 = T_{\text{placed}} - s_0 - s_1$).

We solved:
1. **OEIS A392305 ('Fill your basket' fair compensation, Margin Game $S_{\max} - S_{\text{mid}}$)**:
   - Full calibration: $n = 1..16$ reproduced published OEIS values exactly: `[1, 1, 1, 2, 3, 3, 3, 3, 3, 4, 4, 5, 5, 5, 6, 6]`.
   - New terms computed:
     - **$a(17) = 7$** (placer forces $\ge 7$ in 14.90s; presenter caps $\le 7$)
     - **$a(18) = 7$** (placer forces $\ge 7$ in 72.04s; presenter caps $\le 7$)
     - **$a(19) = 8$** (placer forces $\ge 8$ in 428.27s; presenter caps $\le 8$)
     - **$a(20) = 8$** (placer forces $\ge 8$ in 283.95s; presenter caps $\le 8$)
   - This completes the $K = 4$ new terms required for the full `CONFIRMED_SOLUTION` threshold.

2. **OEIS A391538 ('Game of Chests' guaranteed maximum sum, MaxSum Game $S_{\max}$)**:
   - Full calibration: $n = 1..14$ reproduced published OEIS values exactly: `[1, 2, 3, 5, 8, 11, 14, 17, 21, 25, 29, 34, 39, 44]`.
   - Conjectured formula test ($a(n) = \lfloor n(n-1)/6 \rfloor + n$ for $n > 4$):
     - $a(15) = 50$ (formula: 50, matches: true) in 0.31s
     - $a(16) = 56$ (formula: 56, matches: true) in 1.89s
     - $a(17) = 62$ (formula: 62, matches: true) in 5.41s
     - $a(18) = 69$ (formula: 69, matches: true) in 16.48s
     - $a(19) = 76$ (formula: 76, matches: true) in 45.07s
     - $a(20) = 83$ (formula: 83, matches: true) in 121.58s
     - $a(21) = 91$ (formula: 91, matches: true) in 574.86s
   - Confirms the conjectured formula through $n=21$ without counterexample.

## 2. Technical Architecture & Invariants

- **State Encoding**: 64-bit compact state key: `((mask as u64) << 32) | ((s0 as u64) << 16) | (s1 as u64)`.
- **Transposition Table**: `FastTable` using power-of-2 open-addressing hash table with splitmix64 mixing, pre-allocated to 33,554,432 entries for $n \ge 19$ to eliminate dynamic allocation overhead and cache eviction penalties.
- **Two-Sided Decision Brackets**: Rather than unbounded integer alpha-beta search, each value $v$ is decided via exact boolean decision queries `can_placer_force_ge(mask, s0, s1, c_rem, v)`:
  - If `can_placer_force_ge(..., v) == true` and `can_placer_force_ge(..., v + 1) == false`, the minimax value is provably $v$.
  - Pruning invariants:
    - For Margin: if $(s_2 - s_1) + C_{\text{rem}} < v$, immediately return `false`.
    - For MaxSum: if $s_2 \ge v$, immediately return `true`; if $s_2 + C_{\text{rem}} < v$, immediately return `false`.
    - Presenter cut-off: Presenter minimizes, so if any basket choice $b$ yields `placer_success == false`, Presenter immediately picks $b$ and truncates the remaining basket branches.
    - Placer cut-off: Placer maximizes, so if any coin choice $c$ yields `can_placer_force_ge == true`, Placer immediately picks $c$ and truncates the remaining coin branches.

## 3. Artifacts

- Implementation source: `runs/2026-10-27-1730/attempts/lens1_rust_exact_decision_minimax/src/` (`main.rs`, `solve_a392305.rs`).
- Execution log: `runs/2026-10-27-1730/attempts/lens1_rust_exact_decision_minimax/solver_output.txt`.
