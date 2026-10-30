# BRIEF: three-player-jamfold-sng-epsilon

## Quoted Definition from Primary Sources
From Ganzfried and Sandholm (IJCAI 2009 / CMU-CS-15-104 Section 9.4):
"In this chapter, I will present new algorithms for approximating equilibrium strategies in a class of multiplayer games — undiscounted multiplayer stochastic games, where the stage games are imperfect-information games... We analyze the tournament in which there are 13500 total chips, and blinds are SB = 300, BB = 600... Each state in our game G is defined by a triple $(x_1, x_2, x_3)$, where $x_1$ denotes the stack of the button, $x_2$ denotes the stack of the small blind, $x_3$ denotes the stack of the big blind, $\sum_i x_i = 13500$, and all $x_i$ are multiples of 300... G has 946 non-terminal states... Terminal values use the Independent Chip Model (ICM)... In Texas hold 'em there are 169 strategically distinct preflop hands and two jam/fold moves each player can make at each information set... The button has 169 information sets, the small blind has $2 \times 169$, and the big blind has $3 \times 169$."

## Current Best & Live Bar
- **Baseline Bar**: $\epsilon = \$0.0488$ (Ganzfried & Sandholm, IJCAI 2009; CMU PhD thesis Section 9.4.2).
- **Target Partial Win (p1)**: Certified ex-post $\epsilon < \$0.0488$ under both conventions (i) and (ii).
- **Target Full Win (CONFIRMED_SOLUTION)**: Certified ex-post $\epsilon \le \$0.0010$ under both conventions (i) and (ii).

## What Failed Before
1. **VI-FP Incompleteness**: Value Iteration with Fictitious Play can converge to non-equilibrium profiles if initialized optimistically or if the outer loop updates without policy evaluation.
2. **Undiscounted Value Iteration Trap**: Standard value iteration on undiscounted total-reward MDPs can converge to spurious non-minimal solutions unless initialized pessimistically ($v_0 \le v^*$).
3. **Simultaneous Elimination Ambiguity**: Earlier work did not formalize whether two players eliminated in the same hand are ranked by starting chip count (Convention i) or split prizes equally (Convention ii).

## Pitfalls & Model Invariants
1. **Terminal Payoffs**: Evaluated via 2-player ICM ($V_A = 30 + 20 \frac{s_A}{13,500}$), not heads-up jam/fold equilibrium.
2. **Split Pot Discretization**: If a pot splits with an odd 300-chip unit, the odd unit is awarded 50/50 to keep all stacks in exact integer multiples of 300 chips.
3. **Short Stack Blind Posting**: When BB has 300 chips (1 unit), they are all-in for 1 unit; active bets create side pots and uncalled refunds.
4. **Clockwise Blind Rotation**: At state $s_i$ with position Button, transitioning to nonterminal state $s_j$ shifts the player to Big Blind for the next hand.
5. **Exact Card Removal**: Preflop equities must be computed over genuine 52-card deck combinations with card removal, not independent approximations.
6. **Worst-Case Metric**: Epsilon is the maximum over all 946 stack vectors and all 3 positions, not an average.

## Concrete Attack Angles
1. **Angle 1 — Fast Canonical Suit-Isomorphism Equity Tables**:
   Compute exact 2-way ($\binom{170}{2} = 14,365$) and 3-way ($\binom{171}{3} = 818,855$) showdown equity lookup tables across 169 hand classes in compiled multi-threaded Rust using canonical suit-orbit symmetry and fast 7-card evaluators.
2. **Angle 2 — Exact 2,838 Position-State Markov Game Modeling**:
   Build the exact absorbing Markov chain transition matrix $P^\sigma$ and terminal reward vector $b^\sigma$ across all $946 \times 3 = 2,838$ position-states under both Convention (i) (chip-rank priority) and Convention (ii) (equal-split priority).
3. **Angle 3 — Coupled Policy-Iteration / CFR+ Solver**:
   Solve the stage games across all 946 stack vectors using CFR+ (Counterfactual Regret Minimization with regret matching+) inside a policy iteration outer loop, using ICM as warm-start continuation values.
4. **Angle 4 — Newton-Raphson Indifference-Threshold Polishing**:
   Extract marginal boundary hands (hands where $0 < p_{\text{jam}} < 1$) and apply Newton-Raphson to the indifference equations $E[U(\text{Jam})] - E[U(\text{Fold})] = 0$, contracting ex-post exploitability $\epsilon$ below $\$0.0010$.
5. **Angle 5 — Exact Undiscounted Policy-Iteration Verifier**:
   Evaluate $\epsilon_{(i)}$ and $\epsilon_{(ii)}$ via exact policy iteration for the undiscounted MDP best responses ($V_i^*$) and linear system solver for $(I - P^\sigma) V^\sigma = b^\sigma$, certifying $\epsilon \le \$0.0010$ (or $< \$0.0488$).
