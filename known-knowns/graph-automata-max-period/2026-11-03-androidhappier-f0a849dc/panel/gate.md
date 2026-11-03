# Honesty gate — graph-automata-max-period / A384209(11)=71 (run 2026-11-03-0324)

Read: panel/reproduce.md (pass: true), panel/novelty.md (pass: true), panel/criterion.md (pass: true).
Gate time: 2026-11-03T09:56:51Z. Claim-time OEIS fetch was 2026-11-03T07:36:52Z and the novelty skeptic's live fetch 2026-11-03T07:53:58Z (both byte-identical, sha256 a2d2fe9c…a84247, DATA ends a(9)=27); 2 h 20 min before this gate (< 6 h), so the claim-time fetch is cited as fresh enough and no re-fetch was made.

## Panel summary
- reproduce: pass. Own C checker (chk.c, written from the OEIS definition before opening lifeA11/lifeB2, own graph6 parser, own connectivity test) re-ran all 64 residue classes of geng -q 11: 1018997864 graphs (= A000088(11)), 1006700565 connected (= A001349(11)); max 71, reached by exactly 2 graphs (J?qrdjivb}_, JCpbdo}ttv_), next best 61/60/59 as claimed; per-residue histograms identical to Program A's saved outputs (0 diffs over 64); a(1..9) and a(10)=46 reproduced; witnesses simulated to cycle 71 by its own pure-Python simulator. Did not rerun Program B (saved B_order11 consistent).
- novelty: pass. Live OEIS A384209 2026-11-03T07:53:58Z still %I #8, DATA 1,1,1,1,2,4,8,14,27; no a(10)/a(11); no TROPHY_CASE / known-knowns hit; only repo PR is #904 (a(10), says it does not claim a(11)); no literature value 71.
- criterion: pass. "a later term" of A384209 met by a(11); all simple graphs incl. disconnected (A direct, B via lcm over components); single rule B3/S23; all 2^11 starts; two distinct implementations agree (histograms, 1718 high graphs, max); a(1..9) reproduced; witness simulated; term absent at claim time. Full criterion, not partial; a(10)=46 excluded from credit.

## Downgrade audit (never upgrade)
- Hedging panelist: none (residual caveats in criterion — shared author and shared geng binary, n=11 B outputs accepted as recorded — are disclosed, not hedges; reproduce independently recomputed n=11 in full).
- Reproduction mismatch: none.
- Value not strictly better / tie: novelty pass; new term (no published a(11)).
- Stretched criterion / wrong class: criterion confirmed Life B3/S23 on all simple graphs (A384209), not A357951/2/3.
- Scope wider than reproduced: no. Only a(11)=71 is claimed; a(10)=46 (prior own claim, PR #904) is reproduced but not credited here.
- Sample as complete / capped search / probable prime / evasion / bundled cells / unresolved baseline: none. One cell only; exhaustive over all 1018997864 graphs and all 2048 starts.
- Partial vs full: full success criterion ("or a later term"); not packaged as p2 bundling a(10)+a(11).

## Decision
Full success criterion is met. Status is CONFIRMED_SOLUTION.

status: CONFIRMED_SOLUTION
confirmed_scope: A384209(11) = 71: exhaustive enumeration of all 1018997864 simple graphs on 11 vertices (geng -q 11, = A000088(11), disconnected included) and all 2048 initial states under the Game of Life rule B3/S23, by two independent programs that agree (Program A over all graphs; Program B over all 1006700565 connected graphs plus the lcm over connected components) and reproduce a(1..9) = 1,1,1,1,2,4,8,14,27, gives a maximum eventual cycle length of 71, attained by exactly two graphs, J?qrdjivb}_ (witnessed under direct simulation from start state 752) and JCpbdo}ttv_ (start 1728), and the term is absent from the live OEIS entry and its draft at claim time; a(10) = 46 is not part of this claim.
