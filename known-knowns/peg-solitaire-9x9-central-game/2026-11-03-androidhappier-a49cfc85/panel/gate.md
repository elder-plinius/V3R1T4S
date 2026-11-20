# Honesty gate — peg-solitaire-9x9-central-game / 31-move central solution (run 2026-11-03-1321)

Read: panel/reproduce.md (pass: true), panel/novelty.md (pass: true), panel/criterion.md (pass: true).
Gate time: 2026-11-03T14:13:57Z. Claim-time Bell main-page fetch was 2026-11-03T14:09:43Z (sha256 0cab8355…); novelty skeptic live fetch 2026-11-03T14:10:42Z byte-identical; dedicated 9x9 subpage re-fetched at gate prep 2026-11-03T14:11:36Z (HTTP 200, sha256 59f3a9d9…, still Maye 34). All under 6 h before this gate.

## Panel summary
- reproduce: pass. Own simulator (written from the success criterion before reading author checkers) replays every jump on the 81-hole board, counts moves as maximal same-peg runs, reports VALID: 79 jumps, 31 moves, one peg at e5. Author check9.py and replay9.c agree. Five negative fixtures rejected; 34-move calibration accepted. Beam search not re-run (optional).
- novelty: pass. Live Bell main page and 9x9 subpage both still list Maye 34 as best / open. No literature, TROPHY_CASE, known-knowns, or PR under 34 for this cell. 31 is a strict improvement, not a tie or trivial edit of Maye.
- criterion: pass. Full bank success criterion (≤33 and strictly shorter than Bell's 34 at claim time). Confirmed object is the 81-hole square board (not the 33-hole English cross). No minimality claim.

## Downgrade audit (never upgrade)
- Hedging panelist: none. Residual notes (claim.md once said "English"; 9x9 subpage was 500 at scout) were fixed or re-fetched before gate; not hedges against the criterion.
- Reproduction mismatch: none.
- Value not strictly better / tie: novelty pass; 31 < 34.
- Stretched criterion / wrong class: criterion confirmed 81-hole square central game with orthogonal jumps; English misnomer excluded from confirmed_scope; partial wins (33-sweep / 32-loop / lower-bound proof) not claimed.
- Scope wider than reproduced: no. Only the explicit sol31.txt object.
- Sample as complete / capped search / probable prime / evasion / bundled cells / unresolved baseline: none. Single explicit object; search method optional to re-run.
- Partial vs full: full success criterion met; not packaged as a partial win.

## Decision
Full success criterion is met. Status is CONFIRMED_SOLUTION.

status: CONFIRMED_SOLUTION
confirmed_scope: result/sol31.txt is a legal 9x9 (81-hole) square-board central-game solution from e5 vacancy to a single peg at e5 using orthogonal jumps only, of 79 jumps and 31 moves (maximal same-peg runs), independently replayed, which is shorter than the 34-move Maye solution listed as best on Bell's main index page as fetched at 2026-11-03T14:09:43Z.
