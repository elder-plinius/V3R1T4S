# Criterion report: maxdet-gram-49

context: Claude Code subagent, fresh context [claude-sonnet-5-5]

Method. I read the package folder and wrote my own exact checker (Python integers and Fractions) for every clause of the enumerated partial win p2. The checker is my own and is not shipped in this package. I did not read the author's or the orchestrator's verifier scripts. The record value comes from the saved Orrick excerpt in the-record-we-beat/ (order 49: 96 * 12^23 = 635974777627126753067532288); I did not fetch it again. For other sources I used the Rokicki page and the arXiv 2608.22518 abstract that I fetched (neither covers order 49; Rokicki's list has no N = 48 row, and the arXiv paper is for orders 3 mod 4 and 51 only).

p2, literally: 'an explicit symmetric positive-definite integer matrix G with diagonal n, off-diagonal entries obeying the parity/congruence conditions of Gram matrices of +-1 matrices of that order, det G strictly greater than the square of the live record, and passing the rational (Hasse-Minkowski) equivalence test to n*I, all checked exactly; plus at least n-2 rows of a +-1 matrix realising the leading principal block of G', for 'an order n whose record is below its bound'.

Clauses:
1. Symmetric integer matrix of order 49, diagonal 49: MET (checked).
2. Positive definite: MET. All 49 Fraction elimination pivots are positive; det G > 0.
3. Off-diagonal parity and congruence: MET. Every off-diagonal entry is odd (values used: -3 and 1), and for all triples i, j, k the sum G_ij + G_ik + G_jk is congruent to 3n modulo 4 and at least -n (zero violations over all triples). These are the necessary conditions for Gram matrices of +-1 rows of odd order. I know of no further condition that the criterion names.
4. det G strictly greater than the square of the live record: MET. det G is a perfect square, sqrt(det G) = 2^48 * 768469522966111493289934848, and the record is 96 * 12^23 = 635974777627126753067532288; compared exactly, sqrt(det G)/2^48 is larger than the record. Also det G <= (2n-1)(n-1)^(n-1) (Barba) with sqrt ratio 0.98150.
5. Rational equivalence to n*I: MET, by a stronger certificate than the local-invariant test. The folder gives an exact rational matrix Q with Q Q^T = G (verified entry by entry in Fractions; Q is nonsingular). Because n = 49 = 7^2, P = Q/7 is rational and nonsingular with P (nI) P^T = G, so G is rationally congruent to nI. An explicit congruence implies every Hasse-Minkowski local condition, so it passes the test.
6. At least n-2 rows of a +-1 matrix realising the leading principal block: MET. The folder gives 48 rows of width 49 with all entries +-1; their Gram matrix equals the leading 48 x 48 block of G exactly. 48 >= 47.
7. Order's record below its bound: MET (Orrick ratio to the bound about 0.81).

Hidden quantifiers and null models. p2 asks for a frozen Gram target and a partial realisation only. It does not ask for a full +-1 matrix of order 49, and the claim does not assert one exists; the claim should not be read as a determinant record or as a matrix. The margin to the Barba bound (0.98150) is far above what any known +-1 matrix achieves (Orrick's best is about 0.81), which is a reason to expect that no completion exists, but p2 as written does not require one, and a Gram matrix below the bound with the stated congruences is allowed.

Open questions in the claim record (not shipped) that concern this role.
- Does the panel accept an explicit congruence in place of the Hasse-Minkowski computation? Answer: yes. p2 says 'passing the rational (Hasse-Minkowski) equivalence test'; an explicit rational P with P(nI)P^T = G is a proof of the same fact, and Hasse-Minkowski is only a way to decide it.
- Is a Gram target with n-1 realised rows what p2 means by a frozen Gram target? Answer: p2 asks for 'at least n-2' realised rows, so n-1 rows meets the text. No full completion is claimed and none is required.
- Is the margin to the bound consistent with the Gram conditions as stated? Answer: yes, the stated conditions are necessary, not sufficient, and my checks show G satisfies them and stays below the bound. Whether G is realisable by a full +-1 matrix is outside p2.
- A newer record above 96 * 12^23 = 635974777627126753067532288 for order 49? Not found in what I read; for the novelty role.

confirmed_scope: This is an enumerated partial win p2 only: a frozen Gram target for order 49 (symmetric positive-definite integer G with diagonal 49, odd off-diagonals obeying the triple congruence, sqrt(det G)/2^48 = 768469522966111493289934848 above the Orrick record 96 * 12^23 = 635974777627126753067532288, an exact rational Q with Q Q^T = G, and 48 realised +-1 rows matching the leading block), not a +-1 matrix of order 49 and not a determinant record.

pass: true
