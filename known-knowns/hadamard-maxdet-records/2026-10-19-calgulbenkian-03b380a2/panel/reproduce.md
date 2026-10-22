context: Claude Code subagent, fresh context [Claude Sonnet 5.5]
# Reproduce report, maxdet-gram-81

Folder integrity: ran the hash list from inside the package folder (the paths in that list are relative to it); every listed file reported OK. I then worked only in a private copy of the package. No network was used.

## Definition (quoted from the claim record, not shipped)
Claim: "object/G81_p2.json holds a symmetric positive-definite integer 81 x 81 matrix G with diagonal 81, off-diagonal entries obeying the parity and triple congruences of Gram matrices of +-1 matrices of order 81, with sqrt(det G) / 2^80 = 252 * 20^39 = 138538465099776000000000000000000000000000000000000000 (larger than the Orrick archive record 196 * 20^39 for order 81), an exact rational matrix Q with Q Q^T = G, and 80 rows of a +-1 matrix whose Gram matrix is the leading principal block of G."
Partial win p2 (verbatim): "A frozen Gram target: for an order n whose record is below its bound, an explicit symmetric positive-definite integer matrix G with diagonal n, off-diagonal entries obeying the parity/congruence conditions of Gram matrices of +-1 matrices of that order, det G strictly greater than the square of the live record, and passing the rational (Hasse-Minkowski) equivalence test to n*I, all checked exactly; plus at least n-2 rows of a +-1 matrix realising the leading principal block of G."
For a +-1 matrix M of odd order n, G = M M^T has diagonal n; every off-diagonal entry is x.y = n - 2 d(x,y), so it is congruent to n mod 2; and for any three rows x.y + x.z + y.z = 3n - 2(d_xy + d_xz + d_yz) with the Hamming triangle sum even, so it is congruent to 3n mod 4 (that is the triple congruence; I derived it myself rather than reading the author's).

## My checker (written before opening verify-it-yourself/; not shipped in this package)
Checks, exactly (Python ints / Fractions / python-flint): G integer, symmetric; diagonal n; off-diagonal parity of n; every one of the C(n,3) triples satisfies G_ij+G_ik+G_jk = 3n mod 4; positive definiteness by exact rational LDL (all pivots > 0); det G by LDL and by flint agree; det G = (D * 2^(n-1))^2 with D the stored integer; D greater than the saved Orrick value (and det G > (record * 2^(n-1))^2); det G within the Barba bound (2n-1)(n-1)^(n-1); Q Q^T = G exactly in rational arithmetic with Q = Q_num / Q_den; the stored M0 has n-1 distinct rows of +-1 and M0 M0^T equals the leading (n-1) x (n-1) block of G.
Command: (own checker, run on object/G81_p2.json with arguments 81 D 0 RECORD) (D and RECORD are the decimal integers of 252 * 20^39 and the saved record)
Real output (shown below):
symmetric True
diag==n True
offdiag parity == n parity True
triple cong (sum == 3n mod 4) True
offdiag abs<n True
PD (all pivots >0) True
det G == LDL det True
claimed norm_det_sqrt_G 138538465099776000000000000000000000000000000000000000
det G == (nd*2^(n-1))^2 True
nd == coef*base^e (given) True
nd > record True det G > rec^2*4^(n-1) True
Barba ok True ratio 0.9930191118612668
Q Q^T == G True
M0 rows 80 all +-1 True
M0 M0^T == leading block G True
M0 rows distinct True
I also confirmed with Python ints that the stored value equals 252 * 20^39 and the saved record equals the stated product (see README.md): both equalities True.

## Rational equivalence to n*I
Because Q is an exact rational matrix with Q Q^T = G and det G > 0, Q is invertible. n = 81 is a perfect square (9^2), so P = Q / 9 satisfies P (n I) P^T = Q Q^T = G. That is an explicit rational congruence G ~ n I, which proves the equivalence that a Hasse-Minkowski local-invariant computation would test (the explicit witness is stronger than the local test). This answers the first open question for reproduction: I accept the explicit congruence as exact evidence (checked above, Q Q^T == G True).

## Other open questions
- n-1 = 80 realised rows satisfy p2's "at least n-2" (80 >= 79); checked above (M0 rows, Gram block equal). No completion to a full +-1 matrix is claimed and none is needed by p2's text; I did not look for one.
- The margin to the Barba bound is 0.99302 (sqrt(det G)/bound, in the real output above); G does not exceed it, as required.
- Whether the Orrick value is the live record: not my role.

## Author's checker (run only after mine)
sha256 matches INDEX.csv (03b380a2074785deac39cb19b68c0853cd52ea469f7b848600cc756df42c8992)
checker verdict: PASS 
== negative control: G with one off-diagonal pair changed must NOT pass
negative control rejected as expected
ALL CHECKS PASS
Agrees; no mismatch.

## Verdict
Every p2 property I can state from the text reproduces exactly (no sampling; exact arithmetic over all triples and all entries). Limit: the object proves a Gram target, not a +-1 matrix of order 81.

pass: true
