## Success criterion (copied verbatim from repo/bank/targets.json, kit pinned at 1ebdef4)
(1) An m x n pattern with 5 <= min(m,n) and m*n STRICTLY LESS than the smallest orphan area listed on LifeWiki's Garden of Eden page as confirmed by a human in a browser at verification time (96 as of 2026-10-03 per Wikipedia). (2) Two independently written CNF encodings of 'there exists an (m+2) x (n+2) predecessor' are both UNSAT under CaDiCaL and kissat, and at least one DRAT/LRAT proof is checked by drat-trim or cake_lpr. (3) Sanity: the encoders return SAT with simulation-verified predecessors on 100 random non-orphans and on Eker's 8x12 with one cell flipped where applicable. (4) A human confirms on LifeWiki's Garden of Eden page that no orphan of area <= m*n is already listed. Do not bypass Cloudflare; the human gate is mandatory.

## Partial wins (verbatim)
- p1: A DRAT/LRAT-certified proof (two independent encodings, checked by drat-trim or cake_lpr) that no orphan exists in some h x w box with h >= 5 that is not already ruled out in the literature (human LifeWiki/forum check required; height <= 4 is already known).
- p2: An orphan of height h in {5, 6, 7} strictly narrower than the narrowest height-h orphan listed on LifeWiki at verification time (human-checked; 2016 values for context: widths 83, 21, 15), certified as in (2)-(3).

