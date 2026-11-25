# Method

## Pieces
24 free heptiamonds, Ishino letters A–Z omitting O,W (Sicherman). Master cells extracted from an archived Ishino-letter hexagon ASCII tiling; all 24 shapes are distinct and 7-connected on the triangular lattice. Spot-check against Sicherman `labels.png` before any claim.

Coordinate system: integer cells `(r,c)` with neighbors
- even `r+c`: `(r,c±1)`, `(r−1,c)`
- odd `r+c`: `(r,c±1)`, `(r+1,c)`

Honeycomb embedding (120° bonds): `center = (c,\ r√3 + (r+c mod 2)·√3/3)`.
Aspects: full D6 orbit via 60° complex rotation + reflection, snapped back to the lattice; translations give placements.

## Compatibility model
At tile count `k`, board is an `O(√(7k))` rectangle. Joint SAT (CaDiCaL):
- `f_c`: cell in figure F; exactly `7k` true
- placement vars for all congruent copies of P and of Q; exactly `k` each
- each board cell covered by exactly one chosen P placement iff `f_c`, same for Q

Connectedness and holeless are enforced by post-filtering SAT models (blocking clauses / retries). An UNSAT result on the joint model is a board-bounded certificate that no figure of that `k` exists inside the board (even allowing disconnected F); labelled as partial win **p3** when DRAT-checked.

## Checker
`py/check_independent.py` re-validates: congruence via D6 aspects / distance signature, exact cover, connectivity, holeless, tile counts.

## Trust
CaDiCaL + drat-trim. Re-fetch live Sicherman tables and check Friedman Math Magic / Resta before claiming. Exclude `×` cells.
