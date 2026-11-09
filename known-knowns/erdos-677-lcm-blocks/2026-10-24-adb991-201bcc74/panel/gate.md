# Honesty gate: erdos-677-lcm-blocks (JSP-000550 = Erdős 677), claim "no counterexample with k ≤ 25 and n ≤ 10^494" (run 2026-10-24-0818)

status: CONFIRMED_PARTIAL
confirmed_scope: For every 1 ≤ k ≤ 25, every 0 ≤ n ≤ 10^494 and every m ≥ n + k (no cap on m), lcm(m+1..m+k) ≠ lcm(n+1..n+k), as a computer-assisted, not kernel-checked result. It rests on a hand proof of Lemma A, an exact hash-plus-verification search for n + k ≤ 1.1·10^6, a margin proved in exact rational interval arithmetic for X ≥ 10^6, and a continued-fraction enumeration to q ≤ 10^495 with exact final tests. That enumeration uses float64 pre-filters and 1090-digit non-interval arithmetic, whose correctness is supported by error analysis and an independent exact cross-check on 123 sampled curves but not formally proved.

Read by the run's main session at 2026-10-24T11:52:08Z. All three panel files were written by fresh subagent contexts that saw only
claim/, plus what each fetched or computed itself:
- reproduce.md: pass: true
- novelty.md: pass: true
- criterion.md: pass: true

The scope line above is CRITERION's sentence, copied exactly. The partial win met is "an exhaustive, uncapped
verification of the statement for a stated range of (n, k) with a checkable certificate". The claim is not a solution
of the problem and is not prize-eligible.

## Downgrade checks (kit/RUN.md step 7)

### Hedging
- **NOVELTY** passes "conditional on the record noting the k ≤ 3 prior coverage".
  - k ≤ 2 is trivial. k = 3 is settled for all n by Chan, arXiv:2408.01306 (Period. Math. Hung. 2025), Theorem 1,
    which NOVELTY read in the PDF.
  - The condition is about how the result is described, not doubt that the range beats what is known. No known
    result covers the claimed range or contains it: per NOVELTY, the largest recorded searches are k ≤ 150 with
    n < m ≤ 1.5·10^5, and n, m ≤ 2·10^5 with k ≤ 12.
  - I record it here: **the new content is 4 ≤ k ≤ 25** (for n ≤ 10^494, any m).
  - NOVELTY could not read one 2026 paper (Danesh–Bianchetti, IJMTT 72(9); proxy 403, not retried). A third-party
    audit says it leaves k = 6 open, so it cannot contain this claim. At most it settles k = 4, 5, which would narrow
    the new content to 6 ≤ k ≤ 25. This is a limit of the novelty check, stated here; it is not a reason to doubt
    novelty of the range as a whole.
- **CRITERION** names its main risks inside the scope sentence: not kernel-checked; float64 pre-filters and 1090-digit
  non-interval arithmetic supported by error analysis and cross-checks, not formally proved. The scope is honest about
  them, so this is not a hedge on the verdict.
- **REPRODUCE** passes without hedging and lists gaps it closed itself:
  - an error analysis of the ±2 s-widening, with bound errors ≤ about 0.4;
  - a margin run with η = 10^-6, which covers the non-rigorous L and U.

### Reproduction
- **Enumeration.** REPRODUCE reran deep_rig.py for every k = 3..25 in full. All 23 per-k lines are identical to
  object/out (times ignored), with 1,174,616 window candidates and 0 product solutions. Validate mode (brute force for
  q ≤ 4000) is OK for k = 3..18. An independent exact-integer enumerator agrees for k = 3..10 at QMAX = 10^495.
- **Small X.** Its own small-X program (exact prime-part multisets) and the rerun of search677b both agree.
- **Ratio set and margin.** Its own ratio generator agrees with admissible_r. The interval margin checker was rerun
  for k = 3..25 and the exact checker for k = 3..24, all identical to the saved outputs.
- **Criterion's spot checks.** CRITERION reran search677b with a different seed and deep_rig for k = 3..14, and ran a
  brute force for k ≤ 25, n < m ≤ 30000. All agree.

### Literalness
CRITERION checked:
- m uncapped (p unbounded in Step 5);
- k = 1, 2;
- n = 0;
- both parities of k;
- m = n + k;
- the X = 10^6 split, where the ranges overlap;
- q ≤ 2·10^494 + 26 < 10^495;
- lcmInterval = lcm(n+1..n+k).

### Other checks
- **Scope.** It is no wider than what was reproduced, and it names the non-rigorous components.
- **Completeness.**
  - The search is exhaustive, not a sample.
  - The small-X search is capped only in n (n + k ≤ 1.1·10^6) and is complete in m by Lemma A.
  - No probable prime is used: primes come from a deterministic sieve.
- **Evasion.** None: one request per page; proxy blocks were recorded and not retried.
- **Bundling.** One claim and one range.
  - The R1 extension to 2·10^8 (extender-r1) is a separate lens result, not panelled and not bundled.
  - The workspace's earlier "n ≤ 5871·k" claim (run 2026-10-15-0724, CONFIRMED_PARTIAL tonight) is separate.
    NOVELTY checked that neither claim contains the other.
- **Freshness.** NOVELTY's catalog fetch at 2026-10-24T10:28:17Z (HTTP 200, sha256 78ecc0e2…7834, "Open") is less
  than 6 hours old at this gate.

## Main-session notes (context, not part of the verdict)
- The completeness hole in the float pre-filter was found and fixed by the main session during this run
  (attempts/extender-r2/NOTES.md). The 2026-10-15 R2 result for k ≤ 22 was never panelled; this claim replaces it.
- Process note from REPRODUCE: it paused its own processes with SIGSTOP/SIGCONT to stay within 3 cores, and stopped
  only its own worker shells. These are its own PIDs, logged in panel_work/reproduce/pids.txt.
