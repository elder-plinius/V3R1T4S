# Criterion skeptic: A357953(10) = 624

context: subagent (executor Task)
inputs: claim copy only (claim.md, VALUE.txt, table_record.md, code/, result/, data/). No REPORT, attempts, or other runs read.

## Bank criterion, clause by clause
1. **New exact term of one of the four sequences, A357953(9) "or a later term".** The cell is A357953(10). That is a later term of A357953, so it is in scope. It is an exact maximum, not a bound.
2. **Sequence identity (neighbours only, not A357952/A357951/A384209).**
   - The claim quotes the %N line of A357953 from data/A357953_claimtime.txt: "(not counting the state of the updated node itself)".
   - code/A/totF.c defaults to `popcount(s&adj[v])` and adds the node's own bit only when run with `self`. code/runA.sh calls `./totF 150`, with no `self`.
   - code/B/main.go adds the node's own bit only when given `self`.
   - Every output header reads `mode=neighbours`.
   - code/stepper.py counts neighbours only. The graph6 parser never sets a self-loop, and I checked that the witness graph has none.
   - Rules are plain subsets R, with ON next step iff count ∈ R. That is totalistic, not outer-totalistic (A357951), and not Life (A384209).
   - The reproduced small terms 1,2,2,6,7,18,38,96 equal A357953's DATA exactly.
   - Verdict: no confusion between the sequences.
3. **Exhaustive over graphs, rules and states.**
   - Graphs: `geng -cq 10` over residue classes 0..31 of 32. Both programs count 11716571 graphs in total, which equals A001349(10) (data/A001349.txt). No class is missing in result/compare_AB.txt.
   - Rules: both programs use all subsets of {0..maxdeg}. This shortcut is sound: a count never exceeds deg(v) ≤ maxdeg, so higher bits of R never act. code/spot.py cross-checks it over all 1024 rules with no pruning, for 170 sampled graphs plus the top 20, with 0 mismatches.
   - States: all 1024 start states.
   - Hidden quantifier "connected": A357953 requires connected graphs, and `-c` is used. Satisfied.
4. **Two independent implementations agree and reproduce every listed term.**
   - The two programs are C (Gray-code rule walk, epoch-stamped cycle finder) and Go (binary rule order, Kahn peeling).
   - result/compare_AB.txt: 0 of 32 classes differ, with per-class counts, maxima, high-graph lists and FNV hashes compared. VERDICT AGREE M = 624.
   - result/A_n1_9.txt and result/B_n1_9.txt both give 1,2,2,6,7,18,38,96 (all listed OEIS terms), plus 180 at n = 9.
   - Caveat: both programs use the same geng binary. The criterion names geng, and the A001349 count controls completeness, so this is acceptable.
5. **Witness simulated directly.** I re-ran `python3 code/stepper.py 'I?AAD@oIg' 0,2 2` myself and got preperiod 0, cycle_length 624. The graph is connected, has 10 nodes and 11 edges, and has no self-loops.
6. **Term absent from the live OEIS at claim time.**
   - data/A357953_claimtime.txt (%I #13 Oct 24 2022) has %S 1,2,2,6,7,18,38,96 and ends at a(8).
   - data/draft_A357953_claimtime.html says "No pending changes".
   - Neither a(9) nor a(10) is present.

## Subsumption and credit checks
- The only repo hit (data/gh_A357953_claimtime.json) is PR #904, which claims A384209(10) = 46 (Life). It explicitly lists A357953 as "not claimed". It does not subsume this claim.
- a(9) = 180: claim.md calls this the contributor's own earlier, unsubmitted result. It is reproduced here only as a check, and the package does not claim it. **a(9) is excluded from this package's credit.** Only a(10) counts.
- Possible stretch, noted but not disqualifying: the criterion's example list names A357953(9) as the "next" term. Because a(9) is not in the OEIS either, a(10) is not adjacent to the live DATA. The criterion's "or a later term" covers this. For an OEIS submission, a(9) would have to go in alongside it, and that is outside this criterion.
- Not checked by me: whether the programs are correct beyond the agreement, spot-check and reproduction evidence above. This is an exact computer enumeration, not a proof.

## Decision
FULL success criterion met (not a partial win). No hidden quantifier or definition is stretched.

confirmed_scope: Exhaustive enumeration of all 11716571 connected graphs on 10 nodes (= A001349(10)), all totalistic rules R, and all 1024 start states, counting ON neighbours only with the node itself not counted, by two independent programs that agree class by class and both reproduce A357953(1..8), gives A357953(10) = 624 (absent from the live OEIS entry, whose DATA ends at a(8), at claim time 2026-11-03), with witness graph6 I?AAD@oIg, R = {0,2}, start state 2, whose directly simulated cycle length is 624; a(9) = 180 is prior own work and not credited here.

pass: true
