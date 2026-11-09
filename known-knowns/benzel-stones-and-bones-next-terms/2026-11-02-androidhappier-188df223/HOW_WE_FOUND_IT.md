# How we found it (contributor text, unverified)

The brief was a V3R1T4S run (heavy effort) on the bank target benzel-stones-and-bones-next-terms: compute the next
term of OEIS A364416 or A364417, the stones-and-bones tiling counts of Propp's (n,2n-4)- and (n,2n-3)-benzels
(arXiv:2206.06472, Problems 15 and 16). Both must come from two independent runs that agree exactly, and the code
must reproduce every published term. The scout re-read OEIS and Propp's paper: A364416 stopped at a(20) and A364417
at a(19), both added by Propp in April 2024, and nothing newer turned up.

- exact-eval-first: a plain row-sweep frontier DP was exact, but its state count grew about 3.1x per n. That made it
  hopeless past n = 18. Lookahead by bounded DFS cost more than it saved.
- obstruction-map: there are no frozen cells. A Conway-Lagarias style invariant removed only about 9% of the dead
  states. Extra linear colouring invariants gave nothing new, and a d-band filter was weak. What survived was a
  sound feasibility check: drop a frontier state only if an exhaustive MRV exact-cover search proves that the next
  K = 3 rows cannot be covered. This cut the state count enough for n = 20.
- search-engineer: Program A (benzZQ.c) combined the row sweep, overflow-checked 64-bit counts, OpenMP and
  checkpointing. It gave A364417(20) = 225354012176304818 after one declared stop and a resume from its own
  checkpoint. It then reproduced every published term, A364416(3..20) and A364417(3..19).
- contrarian: wrote a definition-level checker (indep_check.py, from the complex-plane hexagon, no transfer matrix)
  and Program B (benzB64.c / benzB128.c), built differently: region from hexagon vertices, a different line family
  and sweep order, and its own hash table and pruning code. B reproduced the published terms through n = 18, and its
  single uninterrupted n = 20 run gave the same 18-digit number. B switched from 128-bit to overflow-checked 64-bit
  counts for n = 20 because of memory, a change recorded in PREREG.v2.md before B started.
- Meet-in-the-middle was considered and dropped: the middle profile is the peak state set, so it saves nothing.
- The run itself could not start fresh contexts, so it stopped at PROMISING. A three-skeptic panel (reproduce,
  novelty, criterion), each in a fresh subagent context working on a copy of claim/, then ran. The reproduce
  skeptic reran B at n = 20 (same value, same peak state count) and wrote its own small-n counter. The novelty
  skeptic re-fetched OEIS and searched arXiv, GitHub and the web. The criterion skeptic read the bank criterion
  clause by clause and recorded the caveat that only Program A reproduces all published terms. The honesty gate
  re-fetched OEIS once more at 2026-11-02T07:41:24Z and wrote the confirmed scope quoted in README.md.
- Live lead, not claimed: A364416(21) = T113(21,38) looks reachable with the same programs (estimated peak 30-50
  million states).
