context: Claude Code subagent, fresh context [Sonnet 5.5]

# Criterion skeptic report: qecc-n23-k9-d5

Cell: [[23,9]] qubit stabilizer code, claimed d = 5. Target id named by README.md: codetables-binary-linear. Win claimed: p1. The contributor's hash list checked from inside the package folder: all files OK.

## Named partial win p1, clause by clause

p1 text (verbatim): "A quantum-code record: an explicit stabilizer code [[n,k,d]] (symplectic self-orthogonality checked exactly, minimum distance computed exactly) whose d is strictly greater than the lower bound in the live codetables.de quantum-code table for that (n,k)."

My own check (a checker written from the definitions, not shipped in this package; I did not read or run the author's verifier scripts or receipts for this cell). Output:

{'kind': 'qecc', 'n': 23, 'k': 9, 'd': 5, 'd_lo_codetables': 4, 'd_up_codetables': 6, 'construction': 'GF(4) Hermitian self-orthogonal code via weight-4 unitary transvection climb', 'X': '...', 'Z': '...'}
n 23 rows 14 all rows len n: True bits only: True
all pairs commute: True
GF(2) rank of generator matrix: 14 -> k = 9
|S|= 16384 distinct: True
A_j (j<=7): [1, 0, 0, 0, 0, 0, 0, 0]
B_j (j<=7): ['1', '0', '0', '0', '0', '549', '4647', '32487']
B_j-A_j j=1..6: ['0', '0', '0', '0', '549', '4647']
weight 1 commuting non-stabilizer: 0 in S: 0
weight 2 commuting non-stabilizer: 0 in S: 0
weight 3 commuting non-stabilizer: 0 in S: 0
weight 4 commuting non-stabilizer: 0 in S: 0
weight 5 commuting non-stabilizer: 549 in S: 0
weight 4 commuting non-stabilizer: 0 in S: 0
weight 5 commuting non-stabilizer: 549 in S: 0
LP constraints hold for this code: B>=A: True B=A below 5: True shadow>=0: True

- Explicit stabilizer code, 14 generators on 23 qubits: met (14 rows of 23 X bits and 23 Z bits, all entries 0 or 1).
- Symplectic self-orthogonality, exactly: met. All 14 x 14 pairs satisfy x_a.z_b + z_a.x_b = 0 (mod 2).
- Independence: met. GF(2) rank of the 14 x 46 matrix is 14, so k = 23 - 14 = 9 and the group has 2^14 = 16384 distinct elements.
- Minimum distance computed exactly and equal to 5: met, by two methods. (a) Exact stabilizer weight distribution from all 16384 elements (A_1..A_7 = 0; the code is pure) and the quantum MacWilliams transform in exact Fractions: B_j - A_j = 0 for j = 1..4 and 549 for j = 5. (b) Direct enumeration of every Pauli operator of weight 1 to 5 (about 800 thousand operators): none of weight at most 4 commutes with all generators, and 549 of weight 5 do; none lies in the stabilizer. Both agree (549 = 549).
- Strictly above the live lower bound: met. Live cell fetched once by me: https://codetables.de/QECC.php?q=4&n=23&k=9 at 2026-10-19T05:22:24Z, HTTP 200, page sha256 5ba0fab508fc0ef72a89d75af4cedf5279e60758efa55e99ac1414f15875a6a7 (the same sha256 as the triage fetch); it reads "Bounds on [[23,9]] 2 lower bound: 4 upper bound: 6". 5 is above 4 and at most 6.
- Not implied by the live table (Open question 4): met. From the full live table snapshot recorded in the-record-we-beat/README.md (sha256 of the page 26245491..., unchanged when I refetched it at 2026-10-19T05:26:27Z) the one-step lower bounds are: [[22,9]] 4 (add a qubit), [[23,10]] 4 (drop a logical qubit), [[24,9]] 5 minus 1 = 4 (puncture), [[24,8]] 5 minus 1 = 4 (pure puncture). The best implied value is 4, so 5 is not implied.
- Scope (Open question 2): the p1 text of this very target names the quantum table explicitly ("the live codetables.de quantum-code table"), and the sibling target's bank says qubit lower-bound improvements are covered by this entry's partial win. In scope.
- Criterion item 4 (LinCodeEvolve; newer arXiv claim): the LinCodeEvolve codes are classical binary codes, no overlap; a newer arXiv claim of a [[23,9,5]] code cannot be decided from the folder (Open question 3) and I did not search arXiv.
- Open question 1 (a third, structurally different check): the two methods above are already structurally different (weight enumerator plus MacWilliams versus brute-force over Paulis), both written by me; a GF(4)-additive-code route was not run.
- Null model: the construction field says a transvection climb; irrelevant to validity, which is checked from the matrices alone.

Fetch note: I fetched each page below once (curl with the honest user agent, no retry); times are UTC from the machine clock, status 200 for all.

confirmed_scope: The object is a pure qubit stabilizer code [[23,9,5]] (14 independent commuting generators on 23 qubits, exact distance 5 by exact MacWilliams and direct enumeration of all Paulis of weight at most 5) whose distance exceeds the live lower bound 4 (upper 6) of the codetables.de quantum cell [[23,9]] as fetched on 2026-10-19 and is not implied by the live one-step neighbours; whether a newer arXiv paper already has it is not decided here.

pass: true
