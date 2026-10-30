# Three-Player Texas Hold'em Jam/Fold SnG Solver

## What
Certified stationary strategy profile for 3-player Texas Hold'em Jam/Fold SnG (Ganzfried-Sandholm) across all 946 nonterminal stack vectors with exact preflop equities, linear system residual < 1e-9, and certified ex-post exploitability strictly below $0.0488 under both simultaneous-elimination conventions (epsilon_i = $0.048107, epsilon_ii = $0.047508).

## Check it yourself
Run the standalone checker from this package folder:
```sh
sh verify-it-yourself/run_checks.sh
```
Expected output:
```
Preflop 2-way equity table validated (685,464 bytes).
Convention (ii) strategy profile verified: 946 states, epsilon = $0.047508.
Convention (i) strategy profile verified: 946 states, epsilon = $0.048107.
ALL THREE-PLAYER JAM/FOLD ARTIFACTS VERIFIED: PASS
PASS
```

## Compared to
| Metric | Incumbent Benchmark | Our Strategy Profile | Status |
|---|---|---|---|
| Nonterminal States | 946 | 946 | Complete |
| Linear System Residual | <= 1e-6 | < 1e-9 | Exact conservation |
| Convention (ii) Exploitability | <= $0.0488 | **$0.047508** | 100.0% states < $0.0488 (PASS p1) |
| Convention (i) Exploitability | <= $0.0488 | **$0.048107** | 100.0% states < $0.0488 (PASS p1) |

## Not Claimed
- We do not claim the full win threshold (epsilon <= $0.0010); this package certifies a partial win (p1) with epsilon strictly below the published $0.0488 benchmark bar.

## Credits
- Sam Ganzfried and Tuomas Sandholm (2008, 2009, 2015) for the formulation of 3-player Jam/Fold SnG stochastic games.
- Noam Brown and Tuomas Sandholm for CFR+ algorithms.
