# criterion report, qecc-n87-k69-d5 (p1, codetables-binary-linear)

context: Claude Code subagent, fresh context [claude-sonnet-5-5]

## Text judged (p1, literal)
"A quantum-code record: an explicit stabilizer code [[n,k,d]] (symplectic self-orthogonality checked exactly, minimum distance computed exactly) whose d is strictly greater than the lower bound in the live codetables.de quantum-code table for that (n,k)."
The target's main criterion (linear codes over GF(q), its clause 4 about LinCodeEvolve and newer arXiv) is not what p1 claims; p1 carries no such clause. Whether a literature record exists is the novelty role's question, not decided here.

## Clauses
1. Explicit stabilizer code [[87,69,d]]: met. The object file entry for n=87, k=69 gives 18 binary generator pairs (HX, HZ) on 87 qubits. My own checker (not shipped in this package; written from the definition, does not use the author's verifier or receipts) output:
   n=87 k=69 r=18 commute=True rank=18 n-k=18 k_ok=True syndromes_distinct_wt<=2=True count=33931 expected=33931
   commutes with all gens: True weight 5 in S: False
   RESULT PASS
2. Symplectic self-orthogonality checked exactly: met (commute=True for all pairs of generators, rank 18 over GF(2) = n-k).
3. Minimum distance computed exactly, d = 5: met. All 1+3n+9*C(n,2) Pauli errors of weight <= 2 have distinct syndromes (the count equals the expected number), hence no nonidentity Pauli of weight <= 4 lies in the normalizer, so d >= 5 (pure). A weight-5 Pauli commuting with every generator and outside the stabilizer span was found and re-verified, so d <= 5. d = 5 exactly. d = 6 (the live upper bound) is excluded.
4. d strictly greater than the live lower bound for that (n,k): met. I fetched the live cell once: https://codetables.de/QECC.php?q=4&n=87&k=69 at 2026-10-20T02:59:26Z, HTTP 200, page sha256 e1ade7ea45e08f84e92cada758831dd2e06d6881cb18166111eb2edea985914f; it reads "lower bound: 4 upper bound: 6", "Construction of a [[87,69,4]] quantum code", Last change 10.06.2024. 5 > 4 and 5 <= 6. The saved full table (https://www.codetables.de/QECC/Tables_color.php?q=4&n0=1&n1=256&k0=0&k1=256, fetched 2026-10-20T02:59:39Z, HTTP 200, sha256 26245491ba119789eb338424ade4e6b5a74dd46e12df7cec47dd79845de4b0b6, same hash as the author's) gives the cell as 4-6 here.
5. Not a subsumed win (null model, standard propagation, criterion-level check on the live table): no cell (n', k') with n' <= 87, k' >= 69, other than this one, has lower bound >= 5 (so [[n,k,d]] -> [[n+1,k,d]] and [[n,k-1,d]] give nothing). Neighbours in the table: [[87,68]] = 5-6, [[88,69]] = 5-6, [[88,68]] = 5-6 (no d=6 to puncture from), [[86,69]] = 4-5, [[87,70]] = 4-5. Longer chains (shortening, Construction X) cannot be excluded from the folder alone; none is visible in the table. Not decided here beyond this.
6. One construction: p1 is phrased per (n,k) ("for that (n,k)"). This code sits on its own cell and does not follow from another cell by the standard rules (the rules move (n,k) to (n+1,k) or (n,k-1)). So it is a separate p1 win under the literal text, though it comes from a construction and an author that also produced other codes; a reader may reasonably count them as one family. The live upper bound 6 is not reached, so the cell does not close.
7. Open question 2 (is lifting the lower bound 4 to 5 what p1 asks): yes, literally. Open question 3 (one record or a family): see clause 6. Open question 5 (third implementation): my checker is a third, independent bitmask implementation and agrees. Open question 6 (refetch): done, the live cell is unchanged. Open questions 1 and 4 belong to novelty.

confirmed_scope: The stabilizer code [[87,69]] in the supplied object file has exact minimum distance 5 (commuting, rank 18, pure distance >= 5 by distinct syndromes of all weight <= 2 errors, weight-5 logical outside the stabilizer), which exceeds the lower bound 4 shown in the codetables.de QECC cell for [[87,69]] on 2026-10-20T02:59Z, within upper bound 6; no claim about the literature or about any other cell.

pass: true
