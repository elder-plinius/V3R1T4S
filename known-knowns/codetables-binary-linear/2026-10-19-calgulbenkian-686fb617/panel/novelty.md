context: Claude Code subagent, fresh context [claude-sonnet-5-5]

# Novelty report: qecc-n23-k9-d5

Role: novelty. Cell: stabilizer code [[23,9,5]] against the live codetables.de qubit lower bound (partial win p1 of the target).

## Primary table (fetched once, honestly)
- https://codetables.de/QECC.php?q=4&n=23&k=9 | fetched 2026-10-19T05:16:34Z | HTTP 200 | sha256 5ba0fab508fc0ef72a89d75af4cedf5279e60758efa55e99ac1414f15875a6a7
- https://www.codetables.de/QECC/Tables_color.php?q=4&n0=1&n1=256&k0=0&k1=256 | fetched 2026-10-19T05:16:36Z | HTTP 200 | sha256 26245491ba119789eb338424ade4e6b5a74dd46e12df7cec47dd79845de4b0b6
Value read: [[23,9]]: lower bound 4, upper bound 6 (the full-table page reads 4-6 for n = 23, k = 9; the page footer reads 'Last change: 23.05.2024'). Both page hashes equal the triage's. The claim d = 5 is strictly above 4 and at most 6.

## Shared sources (fetched once for the whole group, kept as notes)
- https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | fetched 2026-10-19T05:15:21Z | HTTP 200 | sha256 b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1
- https://api.github.com/repos/elder-plinius/V3R1T4S/contents/known-knowns | fetched 2026-10-19T05:15:21Z | HTTP 200 | sha256 8a2927f7995495ec01c3022b965eba5363a7831765ebd4a18a27a0e6ae36d011
- https://api.github.com/repos/elder-plinius/V3R1T4S/contents/known-knowns/codetables-binary-linear | fetched 2026-10-19T05:17:23Z | HTTP 200 | sha256 904f233ba9fe62d5cfda8003313ed80b431e4f461c65bb3448a86fd3f04f308f
- https://api.github.com/repos/elder-plinius/V3R1T4S/contents/known-knowns/codetables-qubit-upper-bounds-n101-256 | fetched 2026-10-19T05:17:23Z | HTTP 200 | sha256 d6c01566c6a9f0e61760f975304955861d84aeeb2efb1fe32adce5b664882ce9
- Pull requests: a snapshot of all V3R1T4S pull requests (titles and bodies), fetched 2026-10-19T04:30:31Z, was used instead of the api.github.com pulls pages, to spare the shared quota. 473 pull requests were scanned: every title for the target, and every title and body for the cell's own parameters (a regular-expression search for the cell, results below).
- TROPHY_CASE.md (text dated 2026-10-10 to 2026-10-12) lists six result families (graphs, constant-weight codes, matrix multiplication, Lehmer, VNN-COMP, RobustBench) and two cipher commitments. It has no row for a codetables.de table, so it holds no competing value for this cell.
- Merged folders for the target (listing above): binary-linear has three merged folders (the 2026-10-14 and 2026-10-15 binary [173,17,72], [175,25,61], [213,26,77] filings, all q = 2 lower bounds at other cells); the qubit-upper-bounds target has 52 merged folders by one other contributor.
- arXiv (4 queries plus the one named work). Query 1 (quaternary linear codes, new): 12 entries, newest 2609.21601 (Z4 quasi-cyclic codes) and 2605.14603 (Z4 codes with small Plotkin defect); none gives a GF(4) linear code with these parameters. Query 2 (linear programming bound, linear codes, nonexistence) returned zero entries (the server found nothing for that exact wording; not retried, the four-query allowance was then spent). Query 3 (quantum, upper bound, linear programming, stabilizer): 9 entries, the relevant ones 2610.09900 (Quantizing Delsarte Theory, general theory, no table cells) and 2601.15446 (check-weight-constrained codes, bounds for weight-limited checks, not the generic table). Query 4 (quantum codes, new, codetables): 3 entries, none newer than 2021. The named work 2609.37056 (LinCodeEvolve) is about BINARY linear codes and lists seven binary codes of length 172 to 200, so it cannot concern GF(4), GF(5), GF(7), GF(8), GF(9) or qubit cells.

## Own exact check of the code
My own checker (written from the definition, not shipped in this package): 14 generators on 23 qubits as (x,z) bit pairs, symplectic product by popcount parity, rank over GF(2), then an exhaustive search over all Paulis of weight 1 to 5 for those commuting with every generator, split into members of the stabilizer span and non-members. Output:
generators 14 qubits 23
all pairs commute: True
rank 14 => k = 9
weight 1 commuting with all generators: in S = 0 , in N(S)\S = 0
weight 2 commuting with all generators: in S = 0 , in N(S)\S = 0
weight 3 commuting with all generators: in S = 0 , in N(S)\S = 0
weight 4 commuting with all generators: in S = 0 , in N(S)\S = 0
=> no element of N(S)\S of weight <= 4 (weights 1..3 checked above); distance >= 5
weight 5 commuting with all generators: in S = 0 , in N(S)\S = 549
So the 14 generators commute pairwise, have rank 14 (k = 23 - 14 = 9), no Pauli of weight 1 to 4 lies in the normalizer at all (so the code is pure), and 549 weight-5 Paulis lie in the normalizer outside the stabilizer: the minimum distance is exactly 5. This matches the triage's counts.

## Propagation
Neighbours from the full table (live lower, upper): [[22,9]] 4-5, [[23,10]] 4-5, [[24,8]] 5-6, and also [[23,8]] 5-6, [[24,9]] 5-6. Lower-bound rules: add a qubit ([[22,9]] gives [[23,9]]): 4; drop a logical qubit ([[23,10]] gives [[23,9]]): 4; pure puncture of [[24,8,5]] gives [[23,9,4]]: 4. Nothing in the live table gives 5. Pull requests: the search for the cell [[23,9]] in the snapshot of all V3R1T4S pull requests (titles and bodies) is empty; the 52 merged pull requests on the qubit target all lower UPPER bounds and none touches this cell; the open qutrit entanglement-assisted pull requests (331, 363, 403 to 405) concern qutrit codes.

## Answers to the open questions that concern novelty
2. The cell is a quantum stabilizer-code lower bound, filed under the linear-code target as its partial win p1 (a quantum-code record against the live codetables.de quantum table). The live quantum table at the QECC URL above is the right comparison and I used it. Whether the scope fits the target is for the criterion skeptic.
3. No newer arXiv paper found for a [[23,9,5]] code in the four queries; the live quantum table's last change is 2024-05-23, older than the 24-month window, so a 2024 to 2026 paper could have added the code without the table changing. unresolved: I did not find one, and the search was generic, not parameter-specific.
4. Agreed: nothing in the live table implies d = 5 (all three one-step rules give 4; the neighbouring cells with lower bound 5 are [[23,8]] and [[24,9]], which are the wrong direction for a lower bound at [[23,9]]).

novelty: PASS (with the unresolved literature caveat)
verdict: Exact d = 5 (my own exhaustive check) beats the live lower bound 4, is not implied by any live neighbour, and no pull request or arXiv result I found has an equal or better code for this cell.
pass: true
