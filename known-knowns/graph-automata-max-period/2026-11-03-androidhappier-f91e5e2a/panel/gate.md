# Honesty gate — graph-automata-max-period / A357953(10)=624 (run 2026-11-03-0423)

Read: panel/reproduce.md (pass: true), panel/novelty.md (pass: true), panel/criterion.md (pass: true).
Gate time: 2026-11-03T13:29:57Z. Claim-time OEIS fetch was 2026-11-03T11:17:59Z (claim/table_record.md, sha256 e217d9de…0244754c, byte-identical to the scout fetch 2026-11-03T04:23:02Z; DATA ends a(8)=96, %I #13 Oct 24 2022; draft "No pending changes") and the novelty skeptic's live fetch 2026-11-03T11:54:38Z (same bytes); 2 h 12 min before this gate (< 6 h), so the claim-time fetch is cited as fresh enough and no re-fetch was made.

## Panel summary
- reproduce: pass. Own C checker (mychk.c / mychk2.c, written from the OEIS definition before reading code/A or code/B, own graph6 parser, neighbours-only count, rules over {0..maxdeg}, all 1024 starts) re-ran all 32 residue classes of geng -cq 10: 11716571 graphs (= A001349(10)), max 624 reached only by I?AAD@oIg (rule {0,2}), next 470/464/429/413/410; per-class counts, maxima, full histograms and full lists of graphs with max >= 150 identical to Program A's saved outputs (0 of 32 differ); fresh build of Program B on the witness class r7 byte-identical to the saved B output; a(1..8) and a(9)=180 reproduced; witness re-simulated naively to preperiod 0, cycle 624; all 81 VALUE.txt pins verify.
- novelty: pass. Live OEIS A357953 2026-11-03T11:54:38Z still %I #13, DATA 1,2,2,6,7,18,38,96; draft no pending changes; sequence searches with ...,180 and ...,180,624 give no results; only repo hit PR #904 (A384209(10), lists A357953 as not claimed); no TROPHY_CASE / known-knowns hit; no literature value beyond n = 8.
- criterion: pass. "or a later term" of A357953 met by a(10); neighbours-only totalistic rule (not A357951/A357952/A384209), connected graphs (geng -c), all rules (pruning to {0..maxdeg} sound, cross-checked over all 1024 rules on 190 graphs), all 2^10 starts; two distinct implementations (C Gray-code walk, Go binary order + Kahn peeling) agree class by class and reproduce every listed term a(1..8); witness simulated directly; term absent at claim time. Full criterion, not partial; a(9)=180 excluded from credit.

## Downgrade audit (never upgrade)
- Hedging panelist: none. Residual caveats (both programs and the reviewer use the same nauty 2.8.8 geng binary; programs written in the same run; reviewer's checker resembles A's Gray-code design but B uses a different design) are disclosed, not hedges.
- Reproduction mismatch: none (reviewer's full n = 10 recompute matches in all 32 classes).
- Value not strictly better / tie: novelty pass; new term (no published a(10), nor a(9)).
- Stretched criterion / wrong class: criterion confirmed neighbours-only totalistic CA on connected graphs (A357953), mode=neighbours in every output.
- Scope wider than reproduced: no. Only a(10)=624 is claimed. a(9)=180 is this contributor's own earlier package (cell A357953(9), object sha256 474e2771…, packaged 2026-11-02, not submitted), reproduced here only as a check and not credited.
- Sample as complete / capped search / probable prime / evasion / bundled cells / unresolved baseline: none. One cell only; exhaustive over all 11716571 connected graphs, all rules, all 1024 starts.
- Partial vs full: full success criterion ("or a later term"). Not packaged as p2 bundling a(9)+a(10). Note for an OEIS submission: a(9) would have to accompany a(10); outside this criterion.

## Decision
Full success criterion is met. Status is CONFIRMED_SOLUTION.

status: CONFIRMED_SOLUTION
confirmed_scope: A357953(10) = 624: exhaustive enumeration of all 11716571 connected graphs on 10 nodes (geng -cq 10, = A001349(10)), all neighbours-only totalistic rules R (the node itself not counted) and all 1024 initial states, by two independent programs that agree class by class over all 32 geng residue classes and both reproduce A357953(1..8) = 1,2,2,6,7,18,38,96, gives a maximum eventual cycle length of 624, attained only by the graph I?AAD@oIg (witnessed under direct simulation with rule R = {0,2} from start state 2), and the term is absent from the live OEIS entry and its draft at claim time; a(9) = 180 is not part of this claim.
