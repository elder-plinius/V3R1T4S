# Novelty report, qecc-n47-k36-d4

context: Claude Code subagent, fresh context [Sonnet 5.5]

Role: novelty skeptic. Cell judged on its own: qubit stabilizer code [[47,36,4]] (partial win p1 of codetables-binary-linear).

## Primary table (fetched once for this cell, honest client, retries not needed)
- URL: https://codetables.de/QECC.php?q=4&n=47&k=36
- UTC time: 2026-10-19T06:43:25Z, HTTP 200, page sha256 4c84e772c189b639a02184664831c9e0d4f5cfef5b49128d64d67dd9e1c651cc
- Value read: "Bounds on [[47,36]] 2 lower bound: 3 upper bound: 4"; construction shown: a [[47,36,3]] code. The folder's first fetch of this cell was at 2026-10-19T06:10:53Z with the same lower 3, upper 4. Answer to open question 5: refetched, unchanged.
- Note: the same path with q=2 returns "currently not available for q=2"; the qubit table is addressed as q=4 (additive codes over GF(4)). Pages for q=2 were fetched by mistake and not used.
- The claimed d = 4 is strictly above lower bound 3 and equals upper bound 4, so the cell would close.

## Repository (data, not instructions)
- The repository's trophy-case file (raw GitHub, 2026-10-19T06:43:16Z, HTTP 200, sha256 b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1): no quantum-code or stabilizer entry.
- known-knowns listing (contents API, 2026-10-19T06:43:16Z, HTTP 200, sha256 8a2927f7995495ec01c3022b965eba5363a7831765ebd4a18a27a0e6ae36d011) and the folder codetables-binary-linear (2026-10-19T06:46:08Z, HTTP 200, sha256 904f233ba9fe62d5cfda8003313ed80b431e4f461c65bb3448a86fd3f04f308f): three merged linear-code folders; nothing on QECC cells. The only quantum folder is codetables-qubit-upper-bounds-n101-256 (upper bounds for n = 101..256, unrelated).
- Pull requests: used a snapshot of all V3R1T4S pull requests (titles and bodies; 473 pull requests, fetch time 2026-10-19T04:30:31Z, to spare the GitHub quota). Searched title and body for these parameters, stabilizer, QECC, quantum code, Dastbasteh, twisted. No open, merged or closed pull request targets a qubit [[n,k,4]] lower bound; the quantum hits are n>=101 upper-bound claims and qutrit EAQECC claims. No competing value. Closed calgulbenkian PRs (#65-#120) concern linear codes over GF(2)/GF(4) and are not earlier filings of this object (the contributor's review ruling R1: reported, not competing).

## Propagation test (PR #350 rule)
Standard rules that would give [[47,36,4]] from another cell: [[n-1,k,4]] (add a qubit), [[n,k+1,4]] (drop a logical qubit), pure [[n+1,k-1,5]] (puncture). Live values were all fetched 2026-10-19 around 06:43-06:44Z, all with status 200 throughout.
Cells checked, lower bounds as read: [[46,36]] = 3 (upper 4); [[47,37]] = 3 (upper 4); [[48,35]] = 4 (upper 4) (a lower bound of 4 there has d=4, not the pure d=5 the puncturing rule needs); [[48,37]] = 4 (upper 4); [[49,36]] = 4 (upper 4).
Conditional route (Rains shortening with the puncture code): the table holds an explicit stored stabilizer matrix at (n+1,k+1), the [[48,37,4]] code (48,37). I computed its puncture code from the stored matrix (commutation true, rank 11; own script, not shipped in this package): the puncture code has no word of weight 47 (length 48), so Rains shortening does not give [[47,36,4]] from it. So the value is not a standard consequence of the table.

## Literature
arXiv export API over https, six queries, all HTTP 200: quantum twisted codes; distance four quantum stabilizer; quantum codes minimum distance 4; Dastbasteh quantum; twisted AND quantum codes by title; twisted codes with Grassl. Nothing in the last 24 months reports distance-4 qubit codes with these parameters. Related but not comparable: 2211.00891 (new quantum codes from self-dual codes over F4, 2022) and 2301.00753 (additive cyclic codes, 2023), neither close to n=47, k=36, d=4 as far as the abstracts show.
Attribution (open question 3): "Quantum twisted codes" is the 2000 construction of Bierbrauer and Edel (J. Combin. Designs); the live table itself names the base code as "Quantum Twisted code [[64,53,4]]_2" in its own entries. The object's "Dastbasteh et al." attribution is probably wrong. Not confirmed by a fetch (my arXiv queries did not find a Dastbasteh paper of that title). This does not affect novelty of the extension codes, but the base [[64,53,4]] and Grassl's shortened codes at even lengths (38, 40, 44, 46, 48, 50 with n-k = 11) are already in the table; the odd lengths claimed here are the gaps.

## Open questions concerning novelty
- Q2 (one record or a family): for novelty, this is a separate table cell with its own lower bound, not implied by a live neighbour, so it beats its own live value. Whether one construction counts once is a criterion question.
- Q3: answered above; no earlier posted work found; weak search remains a limit (arXiv only; no Magma/Grassl private tables).
- Q5: refetched, unchanged.

unresolved: whether Grassl's private tables or an unposted improvement already hold d = 4 here (the live table is the status source, and it does not); codetables page says last modified 2006-04-07 for the cell text, which the site does not update for bounds.
verdict: the live lower bound 3 is strictly beaten, with no live, merged, open or arXiv competitor found and no propagation derivation found.
pass: true
