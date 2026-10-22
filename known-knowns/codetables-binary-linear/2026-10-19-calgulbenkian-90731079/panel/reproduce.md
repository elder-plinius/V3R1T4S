# reproduce report, cell qecc-n43-k32-d4

context: Claude Code subagent, fresh context [Claude Sonnet 5.5]

Hash check: The contributor's hash list verified from inside the package folder (all 9 files OK) before copying it to a private workspace.

Definition (p1, verbatim): "an explicit stabilizer code [[n,k,d]] (symplectic self-orthogonality checked exactly, minimum distance computed exactly) whose d is strictly greater than the lower bound in the live codetables.de quantum-code table for that (n,k)." Claim: the entry n=43, k=32 of the object file is a [[43,32,4]] code with 11 independent commuting generators, no normalizer element of weight 3 or less, and a weight-4 logical.

Method (own checker, written from scratch before reading the author's code and not shipped in this package; Python integers as bitsets, no sampling):
1. Read HX, HZ (11 rows of length 43); generator i = Pauli with X part HX[i], Z part HZ[i]. Check pairwise symplectic product 0 for all i, j.
2. GF(2) rank of the 11 vectors of length 2n by Gaussian elimination; need rank n-k = 11.
3. The Pauli strings in the file agree with the binary rows.
4. Distance at least 4: compute the 11-bit syndrome of all 3n single-qubit Paulis, then exhaustively test every Pauli of weight 1, 2 and 3 (all qubit subsets, all X/Y/Z assignments) for zero syndrome. None exists, so N(S) has no nonidentity element of weight 3 or less (hence the code is pure and d is at least 4).
5. Distance at most 4: meet-in-the-middle over pairs of single-qubit Paulis on disjoint qubits with equal syndrome gives a weight-4 element of N(S); its GF(2) membership in the span of S is tested and it lies outside S, so it is a nontrivial logical of weight 4. Hence d = 4 exactly.

Command:
    (own checker, run on object/new_optimal_stabilizer_codes_r11_d4.json with n = 43, k = 32)

Real output:
    n,k,r 43 32 11
    pairwise commute (incl self): True
    rank: 11
    strings match rows: True
    zero syndrome singles: 0
    nonzero Paulis of weight 1,2,3 commuting with all gens (counts; 1 = zero-syndrome singles): {1: 0, 2: 0, 3: 0}
    weight-4 element of normalizer outside S: weight 4 commutes with all gens: True
    RESULT PASS [[43,32,4]]

Only after this I ran the author's sh verify-it-yourself/run_checks.sh in a private copy of the package. Its output ends with:
    == negative control: a copy with one bit of the first X row flipped must FAIL
    negative control rejected as expected: RESULT FAIL [[43,32,None]] live [3,4]
    ALL CHECKS PASS

Comparison: no disagreement. Both agree on commutation, rank 11, pure distance 4, and a weight-4 logical. Deterministic (no randomness). The author's negative control (one flipped bit) is rejected.

Scope of this role: I did not judge the live-table value or novelty (other skeptics). Reproduction only confirms that the object is a valid [[43,32,4]] stabilizer code. Open question 4 (third implementation): my checker is an independent third implementation (syndrome enumeration over all weights 1 to 3 plus rank-based membership test), so the concern is answered. Open question 5 (refetch of the live cell) is a novelty matter.

Mismatches: none.

pass: true
