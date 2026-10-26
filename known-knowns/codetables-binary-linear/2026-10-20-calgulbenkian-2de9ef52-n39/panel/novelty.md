# Novelty, [[39,23]] distance 5 (p1, codetables-binary-linear)

context: Claude Code subagent, fresh context [claude-sonnet-5-5]

Scope: judged on this cell alone. Every fetch used is given below with its UTC time, status and sha256.

## Primary table (live)
- URL: https://codetables.de/QECC.php?q=4&n=39&k=23 (q=4 is the qubit page; q=2 answers "currently not available")
- Fetched 2026-10-20T02:59:07Z, HTTP 200, sha256 6bdb853e4af5d1fa9d31f30ea5192616a93d635a7acacf35e4086c9114d78a45.
- Value read: "Bounds on [[39,23]] 2 lower bound: 4 upper bound: 6", construction shown "[[39,23,4]] quantum code", page "Last change: 10.06.2024".
- The claim is d = 5, which is strictly above the live lower bound 4 and below the upper bound 6. The cell is not closed by the claim.
- Full qubit table (fetched 2026-10-20T03:00:33Z, HTTP 200, sha256 26245491ba119789eb338424ade4e6b5a74dd46e12df7cec47dd79845de4b0b6) agrees: (39,23) = 4-6.

## Propagation (PR 350 rule)
Neighbours in the live table: (38,23) = 4-6, (39,24) = 4-6, (39,22) = 5-6, (40,23) = 5-6, (38,24) = 4-5, (40,22) = 5-6, (40,24) = 5-6.
- Rule [[n,k,d]] to [[n+1,k,d]] and [[n,k-1,d]]: needs a d=5 code at some (n', k') with n' <= 39, k' >= 23. My scan of the whole table finds none (lower bound >= 5 nowhere in that quadrant).
- Rule [[n,k,d]] to [[n-1,k+1,d-1]]: needs d=6 at (40,22); that cell is 5-6, and (41,21), (42,20) are 6-7 and 7-8. No d=6 chain reaches this cell.
- The one near neighbour with d=5 at larger n and the same redundancy, (40,24) = 5-6, is not a standard rule (it would be Rains shortening). I tested it: I computed the puncture code (Rains) from the stored stabilizer matrices on the table pages (own scripts, not shipped in this package).
  - [[40,24,5]] (stored matrix): puncture code is {0, all-ones}, so there is no weight-39 word; no shortening to length 39.
  - Every table code with n-k = 16, d = 5 and length 41 to 70 (stored matrices; the odd-length ones were enumerated, the others shown to have only even-weight words) has no weight-39 word in its puncture code: odd-length ones were enumerated and have no weight 39; even-length ones have only even weights.
  - So no Rains shortening of a live table code yields [[39,23,5]]. (Only the table's stored codes were tested; codes with other redundancy cannot give n-k = 16 at this length.)

## This repository
- PR list: a snapshot of all V3R1T4S pull requests (titles and bodies), fetched 2026-10-20T02:41:51Z, up to #576; it was used instead of the pulls API pages (rules for this group).
- Searched every PR title and body for the strings [[39,23, new_stabilizer_codes_d5 and Plucker: no match. Open PRs on qubit stabilizer codes are the author's own (#509 [[23,9,5]], #528 to #533 distance-4 codes); none is [[39,23]].
- Known-knowns listing (HTTP 200, sha256 d5cfdc9c50d89b8a49dc5917b1715181d471a509b84e6b517251e2981d266d2c) and its codetables-binary-linear folder (3 merged entries, all linear codes over GF(2) or GF(4)): no quantum code.
- The repository's trophy-case file (HTTP 200, sha256 b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1): no mention of quantum, stabilizer, QECC or codetables.
- Author's own earlier filings: none for this cell (README.md: new filing, not a refile).

## Literature
- arXiv export API (https): every attempt returned HTTP 429 over about 10 minutes of backed-off retries (logged). Another route used instead: arXiv HTML search, six queries (quantum codes distance five; quantum caps stabilizer; quantum twisted codes; quantum BCH minimum distance 5; Hermitian curve quantum codes qubit; Hermitian self-orthogonal caps). Nothing relevant to qubit distance-5 codes at these parameters turned up in the last 24 months. Closest items: 2610.02392 (qudit Singer-difference-set stabilizer codes, odd q, different object), 0905.1059 (quantum caps in PG(4,4), 2010, distance 4 and small length), 2609.36273 (puncturing for entanglement-assisted codes), 2007.13309 (older quantum BCH).
- unresolved: arXiv API blocked (429), so the keyword searches were done through the HTML search, which is less complete; the 2024 to 2026 literature on Hermitian-curve and quantum-twisted constructions could hold a [[39,23,5]] code that the searches did not surface. Open question 1 (earlier literature): not found, within that limit. A better value is unlikely: the live table (changed 10.06.2024) and the cell above show no d=5 here.

## Open question answers (novelty side)
- Q1 (earlier distance-5 codes): none found; see above.
- Q3 (one record or a family): in the live table this (n,k) is a separate cell, and no cell implies it by a standard rule (the odd lengths cannot come from even ones by Rains shortening, and adding a qubit does not raise k), so for novelty it is a strict improvement. Whether the panel counts the construction as one family is a criterion matter.
- Q4 (longer propagation chain): tested above, none.
- Q6 (refetch): done for this report, same value as the saved excerpt.

## Verdict
The claimed d = 5 strictly exceeds the live lower bound 4, is not implied by the table or merged or open claims, and no competing literature value was found (with the arXiv API caveat). Distance correctness itself is for the reproduce role.

pass: true
