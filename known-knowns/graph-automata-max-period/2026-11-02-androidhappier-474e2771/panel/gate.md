# Honesty gate — graph-automata-max-period / A357953(9)=180 (run 2026-11-02-0959)

Read: panel/reproduce.md (pass: true), panel/novelty.md (pass: true), panel/criterion.md (pass: true).
Gate time: 2026-11-02T21:03:30Z. Novelty live OEIS fetch was 2026-11-02T20:50:20Z (< 6 h); no re-fetch required.

## Panel summary
- reproduce: pass. Independent C checker (own graph6 decoder, connectedness check, exact full-state visit per rule, no sampling) wrote from the definition before opening totA/totB. n=1..8 match OEIS 1,2,2,6,7,18,38,96. Full n=9: 261080 graphs (= A001349(9)), max 180 on H?`DBbS rule {0,2} start 175; second unsplit run and third split run agree; histogram matches result/A_n9_merged.txt. Witness simulated independently at period 180. Author programs re-run match saved parts.
- novelty: pass. Live OEIS A357953 (rev #13) still ends a(8)=96; 180 absent. No TROPHY_CASE / known-knowns / PR / literature rival for this cell (PR #904 is A384209(10), different sequence).
- criterion: pass. Full success criterion met literally for A357953(9); exhaustive geng -c, all 2^9 rules, all 2^9 starts, two programs, witness simulated, term absent from OEIS snapshot.

## Downgrade audit (never upgrade)
- Hedging panelist: none.
- Reproduction mismatch: none.
- Value not strictly better / tie: novelty pass; new term.
- Stretched criterion / hidden quantifiers: criterion skeptic found none (neighbours-only class, connected graphs, full n=9).
- Scope wider than reproduced: no; confirmed_scope matches what reproduce verified.
- Sample as complete / capped search / probable prime / evasion / bundled cells / unresolved baseline: none apply. One cell only.

## Decision
Full success criterion is met. Status is CONFIRMED_SOLUTION (top-tier cell A357953(9), not a partial).

status: CONFIRMED_SOLUTION
confirmed_scope: Exhaustive enumeration of all 261080 connected 9-node graphs (nauty geng -c), all 2^9 neighbours-only totalistic rules and all 2^9 start states, by two differently-built programs that agree and reproduce A357953(1..8), gives A357953(9) = 180, with witness H?`DBbS, rule {0,2}, start 175 confirmed by direct simulation; the term is absent from the OEIS entry snapshot fetched 2026-11-02 04:58 EST.
