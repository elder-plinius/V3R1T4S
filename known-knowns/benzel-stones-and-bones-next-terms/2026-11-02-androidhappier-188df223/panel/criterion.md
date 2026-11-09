# Criterion review: A364417(20) = 225354012176304818

- context: subagent (criterion), fresh context, worked on a copy of claim/ (claim/ untouched)
- paths are relative to the run directory (claim/..., panel/...)

## Criterion, read literally
"The exact next term A364416(21) or A364417(20), not in the DATA when re-fetched immediately before claiming. It must
come from two independent runs that agree exactly, and the same code must reproduce every published term of A364416
and A364417."

The clauses, checked one at a time:

1. **Exact next term.** A364417 DATA ends at a(19) = 20915277691567206 (offset 3). The claimed value is a(20), so it is the next term. MET.
2. **Not in DATA.** The string 225354012176304818 does not appear in claim/data/A364417.txt, A364416.txt, b364417.txt or draft_A364417.html (fetched 2026-11-02 00:49 ET; claim.md mtime 00:50 ET). I re-fetched all four URLs myself at 01:40 ET (06:40 UTC). All returned HTTP 200, A364417 still ends at 20915277691567206, A364416 still ends at a(20) = 87817595880192684, and the value appears 0 times. MET.
3. **Two independent runs that agree exactly.** claim/result/A_final/A364417_n20.out (benzZQ.c) and claim/result/B_final/B_A364417_n20.out (benzB64.c) both say 225354012176304818. Both runs exited 0 with overflow 0.
   - The two programs are written separately. A builds the region from (i,j,k) inequalities and sweeps along lines i = const. B builds it from complex-plane hexagon vertices and Euclidean tile distances, and sweeps along k ascending, then i descending. Each has its own hash table and its own feasibility search.
   - Both use the same general method (frontier DP plus exact-cover pruning that cannot change the count). With different sweep orders and different region and tile construction, a shared systematic error is unlikely to give the same 18-digit number.
   - A was interrupted once (SIGTERM, exit 143) and resumed from its own checkpoint at t=210. claim/result/A_ckpt_test supports the resume (on (16,28) it gives A364416(16)). B ran once without interruption.
   - Null check: the value is about 10.77 × a(19), which fits the ratios of earlier A364417 terms (about 10.7 to 10.8). That is consistent, but it is not evidence of correctness.
   
   MET.
4. **Same code reproduces every published term.** In claim/result/A_repro, benzZQ reproduces every published term: A364416(3..20) (18 terms) and A364417(3..19) (17 terms). Every run exited 0 with overflow=0, and repro_matrix.py reports 0 mismatches and 0 missing. The runs used the same parameters as A_final (K=3, NL=4000).
   - I compiled claim/code/benzZQ.c and benzB64.c fresh and spot-checked both at n = 3, 6, 9, 12, 13 for both sequences. All 20 values match OEIS.
   
   MET for program A, the code whose run gives the claimed value.

## Hidden quantifiers and stretched definitions (caveats)
- **"The same code" is satisfied by A only.** B's published-term runs (claim/result/B_repro) used benzB128.c, not the benzB64.c that produced B's n=20 value. The two differ only in count width and hash load factor (I checked with diff). B also never ran A364416(19), A364416(20) or A364417(19). So the criterion is met on the singular reading: one code (benzZQ) produced the claimed value and reproduces every published term, and a second independent run agrees. It is NOT met on the stricter reading that both programs must reproduce every published term. The claim sentence itself states the reproduction only for Program A, which is accurate.
- **The claim was written before its evidence finished.** claim.md was last modified at 00:50 ET. A's A364417(19) reproduction finished at 00:52 ET and A364416(20) at 01:07 ET, after the claim text existed. The evidence is now complete and my 01:40 ET re-fetch covers the "not in DATA" clause. Still, the claim text came before its own support.
- The header comment in benzZQ.c says "unsigned __int128 counts", but the code uses u64 counts, with every addition overflow-checked. This is a stale comment and does not affect the result.
- I did not rerun the n=19/n=20 computations myself (each takes 20–40 minutes or more). Checks at those sizes rest on the saved logs.

## Partial wins
This is the full criterion (one exact next term, two agreeing runs, and full published-term reproduction by the producing code). It is not a partial win (p1/p2) presented as a full one, and it is not subsumed by one.

confirmed_scope: Two independently written exact frontier-DP programs (benzZQ.c and benzB64.c) each give A364417(20) = 225354012176304818, a value absent from the OEIS A364417/A364416 DATA, b-file and draft as re-fetched 2026-11-02 01:40 ET, and benzZQ.c (but not benzB64.c) reproduces every published term A364416(3..20) and A364417(3..19).

pass: true
