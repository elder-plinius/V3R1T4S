# Target llrl-ant-minimal-seed (local, user-added) — success criterion and partial wins, verbatim from targets-local/llrl-ant-minimal-seed.md
Claim level sought here: partial win p1 only.

## Success criterion (copy verbatim into target.md)
The complete table g(k) for k = 0..K0, where K0 is the least number of non-zero cells allowing onset 0, together with the minimisers for each k (fixed frame, modulo cells never read), such that: (i) every value and every minimiser is re-confirmed by exact simulation with an independent simulator and an exact translation certificate; (ii) completeness (no configuration with <= k non-zero cells has a smaller onset) is shown EXHAUSTIVELY, uncapped, for every k = 1..K0-1 by TWO independently written exhaustive checkers, each with controls (blank-grid onset, a planted positive, a known negative); (iii) K0 itself and its minimiser list come from exhaustive T = 0 searches by both checkers (K0-1 cells give none). The result must not already be published (checked against GLR arXiv 2409.10124, OEIS and a fresh literature search) and must pass a fresh three-skeptic panel.

## Partial wins
- p1: g(k) for k = 1..5 (and g(0) = blank onset), with conditions (i) and (ii) met for those k, and with K0 = 12 established as in (iii).
- p2: g(k) for k = 1..6 with conditions (i) and (ii) met for those k.
