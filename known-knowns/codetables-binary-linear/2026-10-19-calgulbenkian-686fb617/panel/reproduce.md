context: Claude Code subagent, fresh context [claude-sonnet-5-5]
cell: qecc-n23-k9-d5   role: reproduce

The contributor's hash list: 12 files listed, 0 not OK (checked from inside the package folder).

## Definition (quoted)
Claim: "a qubit stabilizer code [[23,9,5]] (23 - 9 = 14 independent, mutually commuting Pauli generators on 23 qubits, given as X and Z rows) whose exact minimum distance is 5, strictly greater than the lower bound 4 (upper bound 6) shown for [[23,9]] in the live codetables.de quantum table". Criterion p1 (verbatim): "A quantum-code record: an explicit stabilizer code [[n,k,d]] (symplectic self-orthogonality checked exactly, minimum distance computed exactly) whose d is strictly greater than the lower bound in the live codetables.de quantum-code table for that (n,k)."
Definition used: generators g_i = (x_i | z_i) in F2^(2n); mutually commuting iff x_i.z_j + z_i.x_j = 0 mod 2 for all i, j; independent iff GF(2) rank = n - k = 14; d = minimum weight of an element of N(S) minus S, N(S) = all Paulis commuting with every generator (d is the minimum weight of N(S)\S, which covers degenerate codes).

## My checker (written before opening verify-it-yourself/)
My checker (written from scratch, not shipped in this package): checks entries are bits and shapes are 14 x 23; all 14 x 14 symplectic products; GF(2) rank of the 14 generators; then enumerates EVERY Pauli of weight 1, 2, 3, 4 (positions and the 3 non-identity types per position, using single-qubit syndrome vectors XORed together), keeps those with zero syndrome (in N(S)) and tests membership in S by reduction against the GF(2) basis; for weight 5 it searches until it finds one element of N(S)\S (upper bound d at most 5). Sanity test on the [[5,1,3]] code (generators XZZXI cyclic): it reports 0 elements at weights 1, 2 and 4 and 30 at weight 3, matching the known B_j - A_j = (0,0,30,0,18).

## Command and real output
    (own checker, run on object/qecc_p1_n23_k9_d5.json)
n,k,rows: 23 9 14 r==n-k: True
noncommuting pairs: 0
GF(2) rank of generators: 14
weight 1 : elements of N(S)\S found: 0
weight 2 : elements of N(S)\S found: 0
weight 3 : elements of N(S)\S found: 0
weight 4 : elements of N(S)\S found: 0
weight 5: element of N(S)\S exists: True [((0, 1, 2, 7, 14), (1, 2, 3, 1, 3))]
RESULT: valid stabilizer [[23,9]] with exact distance 5

So: the generators commute (0 anticommuting pairs), rank 14 = 23 - 9, no element of N(S) outside S has weight 1 to 4 (exhaustive), and a weight-5 element of N(S) outside S exists. Exact minimum distance 5. Live bounds in the-record-we-beat/: lower 4, upper 6: 5 is strictly above 4 and within 6.

## Author's checker, run only after mine
== qecc_check.py (exact stabilizer-code check, d = 5, comparison with live bounds and neighbours)
{"n": 23, "k": 9, "rank": 14, "self_orthogonal": true, "d": 5, "claimed_d": 5, "consistent": true, "VALID": true}
PASS exact d=5; live lower=4 (d > lower: True); live upper=6 (d <= upper: True); best lower bound implied by live neighbours = 4 (< claimed 5: True)
== negative control: one X bit of generator 1 flipped (must fail self-orthogonality or change the distance) (must be rejected)
PASS (negative control rejected)
ALL CHECKS PASS
Agreement: author's MacWilliams route gives B_j - A_j = 0 for j = 1..4 and 549 at j = 5 and the direct count agrees; mine finds the same absence below weight 5 by a different (syndrome enumeration) method and a weight-5 witness. No mismatch.

## Notes
Open question 1: a structurally different check is supplied by this report (direct syndrome enumeration, no weight enumerators). Open question 4: neighbours.csv lists live rows (22,9) lower 4, (23,10) lower 4, (24,8) lower 5 with offset 1 (best implied 4); using the saved full qubit table I also looked at (22,10), (23,8) (24,9): none gives 5 for [[23,9]] under the three rules quoted there. Not decidable here: newer literature (Open question 3), and scope of the quantum cell for this target (Open question 2).

pass: true
