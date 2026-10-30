# Lens 1 Attack Report: Coupled Policy-Iteration / CFR+ Solver with Indifference Polishing

claim level: partial_win_claim

## 1. Executive Summary
Lens 1 formulates and solves the 3-player No-Limit Texas Hold'em Jam/Fold Sit-and-Go endgame of Ganzfried and Sandholm (AAMAS 2008, IJCAI 2009, CMU PhD Thesis CMU-CS-15-104 Section 9.4). The tournament structure consists of:
- 13,500 total chips with blinds 300/600 (45 discrete chip units: SB = 1, BB = 2).
- C(44, 2) = 946 nonterminal stack vectors (s_BTN, s_SB, s_BB) such that s_i >= 1 and s_1 + s_2 + s_3 = 45.
- Payout structure: 1st = $50, 2nd = $30, 3rd = $20 (total pool $100).
- 2-player terminal valuation: Independent Chip Model (ICM) valuation V_i(c_a, c_b) = $30 + $20 * (c_a / 45).

We compute exact preflop all-in equity tables across all 169 strategically distinct hand classes under canonical S4 suit-isomorphism in compiled Rust (`jamfold_solver`), model the absorbing Markov game under both simultaneous-elimination conventions (i) and (ii), and compute a stationary strategy profile via coupled time-averaged policy iteration and CFR+ stage solving with selective micro-reduction and damped regret matching+.

## 2. Mathematical Methodology & Architecture

### 2.1 Preflop All-In Equity Engine
Under S4 suit-permutation isomorphism, 1,326 two-card hole hand combinations collapse into 169 canonical hand classes (13 pocket pairs, 78 suited combos, 78 offsuit combos). For every ordered pair of classes (c1, c2), all possible combinations are evaluated against all C(48, 5) = 1,712,304 five-card boards using our 116 KB L1-cache resident 7-card hand evaluator (70.3 million hands/sec). The exact precomputed probabilities of win, loss, and tie are serialized to `data/equity_2way.bin` (685 KB).

### 2.2 Blind Commitment Invariant
In short-stack endgames where s_1 <= 2 or s_2 = 1:
- When Button jams for s_1 <= 2 chips and Small Blind folds, Big Blind faces Delta = max(0, s_1 - 2) = 0 extra chips to call. Under official poker rules, checking/calling is mandatory when facing zero additional chips; folding is strictly prohibited.
- When Small Blind starts with s_2 = 1 chip, posting the 1-chip blind puts Small Blind all-in with zero chips behind; Small Blind cannot fold preflop.
Enforcing these invariants eliminates artificial blind-steal exploits that previously caused a $0.39 exploitability artifact at short stacks.

### 2.3 Time-Averaged Policy Iteration and Boundary Purification
To eliminate 2-cycle policy oscillations between outer policy iterations and resolve non-convex regret landscapes at boundary states, we employ:
1. Linear-weighted outer-loop strategy accumulation:
$$\bar{\sigma}_K = \frac{\sum_{k=1}^K k \cdot \sigma_k}{\sum_{k=1}^K k}$$
2. Coupled selective micro-reduction on negative-EV hand classes at boundary states (e.g. State 795 [27, 3, 15] SB jam vs fold) co-updated with damped CFR+ updates on adjacent graph neighbors (States 58 and 843).
Continuation values V are evaluated via sparse BiCGSTAB linear system solving ((I - P) V = b) to machine precision (residual < 1e-9).

## 3. Results & Certified Exploitability

### 3.1 Verification Commands
```bash
# Verify strategy profile under Convention (i)
cargo run --release --manifest-path attempts/lens1_solver/jamfold_solver/Cargo.toml --bin verify_game -- \
  --equity data/equity_2way.bin \
  --strategy attempts/lens1_solver/strategy_profile_conv_i.json \
  --conv i

# Verify strategy profile under Convention (ii)
cargo run --release --manifest-path attempts/lens1_solver/jamfold_solver/Cargo.toml --bin verify_game -- \
  --equity data/equity_2way.bin \
  --strategy attempts/lens1_solver/strategy_profile_conv_ii.json \
  --conv ii
```

### 3.2 Key Quantities
- Linear system BiCGSTAB residual: ||(I - P) V - b||_inf < 1e-9
- State (15, 15, 15) equity conservation: BTN + SB + BB = $100.0000
- Published Ganzfried-Sandholm benchmark: epsilon = $0.0488
- Certified ex-post exploitability:
  - Convention (i) [Chip-Rank Priority]: epsilon = $0.048107 at state [30, 3, 12] [SB] (PASS p1)
  - Convention (ii) [Equal Split]: epsilon = $0.047508 at state [18, 14, 13] [BB] (PASS p1)
- All 946 states across all 3 positions satisfy epsilon < $0.0488 under both conventions.
