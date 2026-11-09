# Honesty gate - graph-automata-max-period

Read: panel/reproduce.md (pass: true), panel/novelty.md (pass: true), panel/criterion.md (pass: true).
No hedging panelist. Reproduce: own checker written from the definition, exhaustive over all 12005168 graphs on
10 vertices twice (r/4 and r/8 splits), max 46 on exactly 2 graphs; per-period histogram identical to Program A's;
Program A rerun byte-identical (deterministic); Program B orders 1..9 byte-identical. Shared dependency on geng is
guarded by A000088/A001349 counts (noted, not a downgrade: the criterion names geng).
Novelty: OEIS A384209 text, draft and b-file fetched 09:29:55Z; DATA ends a(9); nothing published elsewhere. A LODA
fitted formula extrapolates to 50 but is a fit to 9 terms with no witness (not a contradiction of an exhaustive count).
Criterion: full success criterion met for A384209(10); not a partial; lcm route of Program B judged valid.
Gate re-fetch (one GET, 2026-11-02T09:43:11Z, HTTP 200): https://oeis.org/search?q=id:A384209&fmt=text, sha256
a2d2fe9c9ff2aab776502142000c0bd3bc4d5b2e120022d1679f0990a8c84247 (unchanged since the scout), DATA 1,1,1,1,2,4,8,14,27, no a(10).
Downgrade triggers checked (kit/RUN.md step 7): no hedging, no mismatch, value is a new term (not a tie), no
stretched criterion, scope equals what was reproduced, exhaustive not sampled, no capped search, no primes, no
evasion, one cell, no benchmark baseline involved.

status: CONFIRMED_SOLUTION
confirmed_scope: Exhaustive enumeration of all 12005168 simple graphs on 10 vertices and all 1024 states, by two independent programs that both reproduce a(1..9), shows that A384209(10) = 46 (a term absent from the live OEIS entry on 2026-11-02), with witness graph6 I?zUvYujw, Life rule B3/S23, start state 62, whose directly simulated cycle length is 46.
