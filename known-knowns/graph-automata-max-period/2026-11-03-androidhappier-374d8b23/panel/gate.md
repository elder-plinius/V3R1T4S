# Honesty gate — graph-automata-max-period / A357951(8)=150 (run 2026-11-03-0236)

Read: panel/reproduce.md (pass: true), panel/novelty.md (pass: true), panel/criterion.md (pass: true).
Gate time: 2026-11-03T04:29:37Z. Novelty live OEIS fetch was 2026-11-03T04:15:37Z (< 6 h); no re-fetch required.

## Panel summary
- reproduce: pass. Independent checkers (written from the OEIS definition before opening otA/otB) re-ran geng -cq 8 over all 11117 graphs × 65536 outer-totalistic rules × 256 starts; max 150 uniquely on GCQfBg; per-graph maxima match saved A and B (byte-identical to A); a(1..7)=2,2,4,6,16,26,66; witness GCQfBg / B={0,2} S={1,3,4} / start 1 simulates to period 150; rebuilt otA/otB parts byte-identical; determinism on re-run.
- novelty: pass. Live OEIS A357951 still ends a(7)=66; draft "No pending changes"; no TROPHY_CASE / known-knowns / PR / literature rival (PR #904 explicitly does not claim A357951).
- criterion: pass. Full success criterion met for A357951(8); outer-totalistic class correctly distinguished from A357952/A357953/A384209; exhaustive; two programs; witness simulated; term absent from OEIS.

## Downgrade audit (never upgrade)
- Hedging panelist: none.
- Reproduction mismatch: none.
- Value not strictly better / tie: novelty pass; new term.
- Stretched criterion / wrong rule class: criterion confirmed outer-totalistic (A357951), not self-counting or neighbours-only or Life.
- Scope wider than reproduced: no.
- Sample as complete / capped search / probable prime / evasion / bundled cells / unresolved baseline: none. One cell only.

## Decision
Full success criterion is met. Status is CONFIRMED_SOLUTION.

status: CONFIRMED_SOLUTION
confirmed_scope: A357951(8) = 150: exhaustive enumeration of all 11117 connected 8-node graphs (geng -cq 8), all 65536 outer-totalistic (B,S) rules and all 256 initial states, by two independent programs that agree graph by graph and reproduce a(1..7) = 2,2,4,6,16,26,66, gives a maximum eventual cycle length of 150, attained uniquely by the graph GCQfBg (witnessed under direct simulation by rule B={0,2}, S={1,3,4} from start state 1), and the term is absent from the live OEIS entry and its draft at claim time.
