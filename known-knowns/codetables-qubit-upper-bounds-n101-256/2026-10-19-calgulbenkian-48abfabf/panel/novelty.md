context: Claude Code subagent, fresh context [claude-sonnet-5-5]

# Novelty report: qubit-ub-n107-k2-d35

Role: novelty. Cell: qubit table upper bound for [[107,2]] lowered to 35, an exact Farkas certificate of the quantum weight-enumerator LP with shadow constraints.

## Primary table (fetched once, honestly)
- https://www.codetables.de/QECC/Tables_color.php?q=4&n0=1&n1=256&k0=0&k1=256 | fetched 2026-10-19T05:16:36Z | HTTP 200 | sha256 26245491ba119789eb338424ade4e6b5a74dd46e12df7cec47dd79845de4b0b6
Value read (own parser of the fetched page, 33152 cells): [[107,2]] live lower/upper and my closures below. The page hash equals the triage's. The footer reads 'Last change: 23.05.2024'; the page note says 'For n>100, the upper bounds on qubit codes are weak (and not necessarily monotone in k)'.

## Shared sources (fetched once for the whole group)
- https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | fetched 2026-10-19T05:15:21Z | HTTP 200 | sha256 b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1
- https://api.github.com/repos/elder-plinius/V3R1T4S/contents/known-knowns | fetched 2026-10-19T05:15:21Z | HTTP 200 | sha256 8a2927f7995495ec01c3022b965eba5363a7831765ebd4a18a27a0e6ae36d011
- https://api.github.com/repos/elder-plinius/V3R1T4S/contents/known-knowns/codetables-binary-linear | fetched 2026-10-19T05:17:23Z | HTTP 200 | sha256 904f233ba9fe62d5cfda8003313ed80b431e4f461c65bb3448a86fd3f04f308f
- https://api.github.com/repos/elder-plinius/V3R1T4S/contents/known-knowns/codetables-qubit-upper-bounds-n101-256 | fetched 2026-10-19T05:17:23Z | HTTP 200 | sha256 d6c01566c6a9f0e61760f975304955861d84aeeb2efb1fe32adce5b664882ce9
- Pull requests: a snapshot of all V3R1T4S pull requests (titles and bodies), fetched 2026-10-19T04:30:31Z, was used instead of the api.github.com pulls pages, to spare the shared quota. 473 pull requests were scanned: every title for the target, and every title and body for the cell's own parameters (a regular-expression search for the cell, results below).
- TROPHY_CASE.md (text dated 2026-10-10 to 2026-10-12) lists six result families (graphs, constant-weight codes, matrix multiplication, Lehmer, VNN-COMP, RobustBench) and two cipher commitments. It has no row for a codetables.de table, so it holds no competing value for this cell.
- Merged folders for the target (listing above): binary-linear has three merged folders (the 2026-10-14 and 2026-10-15 binary [173,17,72], [175,25,61], [213,26,77] filings, all q = 2 lower bounds at other cells); the qubit-upper-bounds target has 52 merged folders by one other contributor (cells listed in the qubit reports).
- arXiv (4 queries plus the one named work). Query 1 (quaternary linear codes, new): 12 entries, newest 2609.21601 (Z4 quasi-cyclic codes) and 2605.14603 (Z4 codes with small Plotkin defect); none gives a GF(4) linear code with these parameters. Query 2 (linear programming bound, linear codes, nonexistence) returned zero entries (the server found nothing for that exact wording; not retried, the four-query allowance was then spent). Query 3 (quantum, upper bound, linear programming, stabilizer): 9 entries, the relevant ones 2610.09900 (Quantizing Delsarte Theory, general theory, no table cells) and 2601.15446 (check-weight-constrained codes, bounds for weight-limited checks, not the generic table). Query 4 (quantum codes, new, codetables): 3 entries, none newer than 2021. The named work 2609.37056 (LinCodeEvolve) is about BINARY linear codes and lists seven binary codes of length 172 to 200, so it cannot concern GF(4), GF(5), GF(7), GF(8), GF(9) or qubit cells.

## Own exact check of the certificate
My own checker (not shipped in this package), written from the LP definition: stabilizer enumerator A_0..A_n with A_0 = 1 and sum A_i = 2^(n-k); normalizer enumerator B_j = (1/2^(n-k)) sum_i K_j(i) A_i with the 4-ary Krawtchouk polynomial K_j(i) = coefficient of z^j in (1+3z)^(n-i)(1-z)^i (built by polynomial products, not the explicit sum); B_j = A_j for 1 at most j below d; B_j at least A_j for j at least d; shadow sum_i (-1)^i K_j(i) A_i at least 0; A_i at least 0. The certificate (free multipliers on equalities, non-negative on inequalities) must give every column coefficient at most 0 with right-hand side u_E0 + u_E1 * 2^(n-k) above 0. Output:
qubit-ub-n107-k2-d35 [[107,2]] excluded d>=36 VALID [] rhs digits 612 max column <=0: True
So the certificate is valid in exact integers: no stabilizer code [[107,2,d']] with d' at least 36 exists (impure codes included, since only B_j = A_j below d is used), and the upper bound is at most 35.

## Propagation closure (the claim must be strictly below it)
Rules used (the target's bank rules): R1 U(n,k) at most U(n,k-1) for k at least 2; R2 U(n,k) at most U(n+1,k); R3 U(n,k) at most U(n-1,k+1) + 1. My own fixed-point closure over all 32896 cells with k at least 1 (my own script, not shipped in this package) with the live table lowered by all merged and open verexxi pull-request values for the target (57 values parsed from the pull-request snapshot titles; every one starts from the live value):
(107, 2) claim 35 live U/L (23, 36) closure(live) 36 closure(live+PR) 36 closure(live+PR+other claims) 36 STRICT
The claim is strictly below the closure in every variant (also if the closed pull request 260 is counted as a known value). Note R3 holds only for pure codes; using it makes the closure smaller, which only makes this test stricter, and the claim is still below it.

## Pull requests, TROPHY_CASE, literature
- Pull requests for the target: 57 values from one other contributor (52 merged, open pull requests 296, 302, 326, 328, and the closed 260). The pull-request search for [[107,2]] in titles and bodies is empty: no one else has filed this cell. The merged cells nearest in parameters are listed in the closure test, which includes them.
- arXiv: the two quantum-bound papers found (2610.09900 Quantizing Delsarte Theory, 2601.15446 check-weight-constrained codes) do not publish cell values for n = 107.

## Answers to the open questions that concern novelty
2. Should values of open, unmerged pull requests count as known bounds? I tested both ways; the answer is the same either way, so it does not matter for this cell: closure of everything else is 36, the claim is 35.
4. A second Krawtchouk implementation: my checker builds K by polynomial products, a different construction from the explicit-sum checker in the folder, and it agrees.

unresolved: the table's n above 100 upper bounds are called 'weak' on the page and the full quantum LP with shadow constraints may have been run privately by the maintainers; no public record of that was found. The literature search was generic (four queries).

novelty: PASS (with the unresolved literature caveat)
verdict: The certificate is exactly valid (own checker), the new bound 35 is strictly below the live upper bound 36 and below the propagation closure of live plus merged and open pull-request values plus the other batch cells, and nobody else has filed the cell.
pass: true
