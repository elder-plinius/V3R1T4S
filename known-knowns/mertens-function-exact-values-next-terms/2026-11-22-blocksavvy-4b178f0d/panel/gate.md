# Honesty gate (kit/RUN.md step 7): run 2026-11-22-0923, A084235 a(18)

gated: Sun Nov 22 17:29:24 UTC 2026 (11:29 CST), by the run's main session (follow-up session), after reading all three panel files in full.
panel files read (sha256): reproduce.md 6e242b8107573d06ef05a8aab4ea5f4ca286eada40be77ab649a13caabcd9967, novelty.md 52ef9e5e6967078ad6fa2e331e481de745470f71b5b361ab022233883661e421, criterion.md 17157330bc72d4673916a6e798d32e61941c10519907b27afb4d435dd801acae
panel: REPRODUCE pass: true (context: subagent), NOVELTY pass: true (context: subagent), CRITERION pass: true (context: subagent); three fresh contexts, each given only claim/
prereg: PREREG.md unchanged (sha256sum -c PREREG.sha256: OK); claim/candidate.md unchanged (sha256 349cdb82b7e6249524ef5adea6e54e7c017d3e2ae14b47d6c4aeadd567dd691e)

## Downgrade checks (kit/RUN.md step 7), each judged literally
- hedging panelist: none. Each verdict is unconditional. CRITERION defers novelty against A051402 and outside sources to NOVELTY, which is a division of roles, not a hedge, and NOVELTY covered it (A051402, A051400, A051401 b-files stop at n = 10000; no outside publication of the value).
- reproduction mismatch: none. REPRODUCE wrote its own Mobius sieve from the definition, validated it by brute force, ran it in full over 1..330100000000 (exhaustive, not a sample) and got first k = 330055906058 with M = -262144; it agrees with both claimant runs block by block (0 mismatches after aligning the empty-prefix convention) and at all 660 run-2 grid points; byte-identical rerun of blocks 0..399.
- value not strictly better than the live table: no. A084235 (b-file and entry) ends at a(17) = 108500046711; a(18) is a new, higher index. NOVELTY's fetch: https://oeis.org/A084235/b084235.txt, 2026-11-22 11:17:09 CST (17:17:09 UTC), HTTP 200, sha256 e40ebda76ec5f993ea987206d65b8b630c2c94a4a90e9aad6939d8a10ead363f, last line "17 108500046711".
- table fetch age: 12 minutes at gating time (under 6 hours), so no re-fetch is needed at the gate. The bank still requires a re-fetch immediately before any submission.
- stretched criterion or hidden quantifier: none found. "least" is covered by complete prefix max/min per block from k = 1 plus an exact in-block scan (|M| moves by at most 1 per step, so first |M| >= 2^18 is first |M| = 2^18); "full segmented Mobius sieve from 1": both claimant runs start at k = 1 with no seeded M value; "verified by a second independent run": run 2 uses a different mu test (log-sum vs product check), different segment and block sizes and a separate combiner, and REPRODUCE added a third full run from 1. Caveat kept on the record: all three full runs ran on the same machine, and the claimant runs share an author and sieve skeleton. The bank's verification_method suggests a re-run on separate hardware; that sentence is not part of the p1 text, so it does not block p1, but it is listed under "Not claimed" in the package and is left to the maintainers' independent reproduction.
- scope wider than reproduced: no. The confirmed_scope names a(18) only (not 2^19, 2^20 or the full criterion) and REPRODUCE reproduced exactly that, in full.
- sample presented as complete: no. The spot checks (9 sympy windows) are labelled as spot checks; the completeness claim rests on the full sieves.
- capped search used as an exclusion: no. No exclusion is claimed beyond 1..330055906058, which was covered completely.
- probable prime used as a proof: not applicable.
- table value obtained by evasion: no. One plain request per fetch (curl / fetch tool); no browser User-Agent, cookies or retries found in claim/ or attempts/.
- several objects bundled as one claim: no. One table cell, A084235(18).
- unresolved benchmark baseline: not applicable (exact-value target; PREREG says step 3c does not apply).
- null test: PREREG states none is needed (deterministic exact value, not a search or statistical claim); category number-hunts does not require one.

## Labels
- A084235(18) = 330055906058 with M(330055906058) = -262144: NUMERICAL (exhaustive deterministic computation, reproduced three times by separately written code).
- What this is: a new OEIS term (the next term of an existing sequence, computed by a known method). It is not a new mathematical discovery, and it says nothing about the Riemann hypothesis.

status: CONFIRMED_PARTIAL
partial_win: p1 (A084235 a(18) only)
confirmed_scope: Two separately written full segmented Mobius sieves from k = 1 (to 3.4e11 and 3.30125e11) agree that the least k with |M(k)| = 2^18 is 330055906058, where M(k) = -262144, and A084235 on OEIS ended at a(17) when re-fetched on 2026-11-22. This meets bank partial win p1 for a(18) only (not 2^19 or 2^20, and not the full criterion), with novelty against A051402 and outside sources left to the NOVELTY skeptic.
stands_only_if: python3 repo/kit/check_run.py prints CHECK_RUN: PASS (otherwise the status is PROMISING)
