# Honesty gate — graph-automata-max-period / A357952(9)=200 (run 2026-11-02-2104)

Read: panel/reproduce.md (pass: true), panel/novelty.md (pass: true), panel/criterion.md (pass: true).
Gate time: 2026-11-02T21:56:04Z. Novelty live OEIS fetch was 2026-11-02T21:50:44Z (< 6 h); no re-fetch required.

## Panel summary
- reproduce: pass. Independent C checker (self-counting, written from the definition before opening totA/totB) re-ran geng -cq 9 over all 261080 graphs × 1024 rules × 512 starts; max 200 on unique graph H?o|]|~; per-graph maxima and histograms match saved A and B; n=1..8 match OEIS 2,2,4,6,8,18,42,112; witness H?o|]|~ / {1,3,5} / start 1 simulates to period 200; determinism on re-run parts.
- novelty: pass. Live OEIS A357952 still ends a(8)=112; 200 absent. No TROPHY_CASE / known-knowns / PR / literature rival (PR #904 lists A357952 as not claimed).
- criterion: pass. Full success criterion met for A357952(9); self-counting class correctly distinguished from A357953; exhaustive; two programs; witness simulated; term absent from OEIS.

## Downgrade audit (never upgrade)
- Hedging panelist: none.
- Reproduction mismatch: none.
- Value not strictly better / tie: novelty pass; new term.
- Stretched criterion / wrong rule class: criterion confirmed self-counting (A357952), not neighbours-only.
- Scope wider than reproduced: no.
- Sample as complete / capped search / probable prime / evasion / bundled cells / unresolved baseline: none. One cell only.

## Decision
Full success criterion is met. Status is CONFIRMED_SOLUTION.

status: CONFIRMED_SOLUTION
confirmed_scope: Exhaustive enumeration of all 261080 connected 9-node graphs (geng -cq 9), all 1024 self-counting totalistic rules R ⊆ {0..9} and all 512 states, by two separately written programs that agree graph by graph and reproduce A357952(1..8), gives A357952(9) = 200, uniquely attained on graph H?o|]|~, with witness rule {1,3,5} from start state 1 directly simulated to a 200-cycle, and the term was absent from the live OEIS entry as of 2026-11-02 21:35Z.
