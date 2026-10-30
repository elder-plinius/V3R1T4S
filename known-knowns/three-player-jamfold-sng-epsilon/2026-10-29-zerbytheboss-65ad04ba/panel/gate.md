# Honesty Gate: `three-player-jamfold-sng-epsilon`

status: CONFIRMED_PARTIAL
confirmed_scope: Certified stationary strategy profile for 3-player Texas Hold'em Jam/Fold SnG (Ganzfried-Sandholm) across all 946 nonterminal stack vectors with exact preflop equities, linear system residual < 1e-9, and certified ex-post exploitability strictly below $0.0488 under both simultaneous-elimination conventions (epsilon_i = $0.048107, epsilon_ii = $0.047508).

## Gate Summary
- **REPRODUCE (`panel/reproduce.md`)**: `pass: true` (Exact preflop 2-way equity tables precomputed via full board enumeration over 1,712,304 boards under S4 suit-isomorphism; 946-state absorbing Markov game evaluated to BiCGSTAB linear residual < 1e-9 with exact $100.0000 equity conservation; Puterman MDP policy iteration best response verified in compiled Rust and Python).
- **NOVELTY (`panel/novelty.md`)**: `pass: true` (Introduced coupled time-averaged policy iteration / CFR+ architecture eliminating 2-cycle outer oscillations; resolved authentic poker blind commitment invariants preventing artificial short-stack steal exploits; evaluated under both simultaneous-elimination conventions).
- **CRITERION (`panel/criterion.md`)**: `pass: true` (Complete mechanical compliance; all 946/946 states in Convention ii achieve exploitability <= $0.047508 < $0.0488; all 946/946 states in Convention i achieve exploitability <= $0.048107 < $0.0488; overall max exploitability certified at $0.048107 and $0.047508, meeting p1 success criterion).
- **Verdict**: CONFIRMED_PARTIAL (Certified Ex-Post Exploitability Record: Comprehensive stochastic-game framework established and certified across all 946 states, driving global max exploitability strictly below the published $0.0488 baseline under both conventions).
