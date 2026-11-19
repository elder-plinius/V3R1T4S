# potts-wsq5-ub: bound statement and certificate format

## What is certified

Let T(m, q) be the row-to-row transfer matrix for proper q-colourings of the square grid with q = 5:
the states are the proper colourings w of a cycle C_m of m vertices (w_i != w_(i+1 mod m)), and
T[w, w'] = 1 exactly when w' is also proper on the cycle and w_i != w'_i for every i (vertical neighbours differ), else 0.
theta_1(C_m) is the largest eigenvalue (Perron root) of T. W_sq(5) is the growth rate per site of the number of proper
5-colourings of the square grid, W_sq(5) = lim (number of colourings of the m x n grid)^(1/(m n)).

Inequality used: equation (6) of Lundow and Markstrom (2008), Section 4. The claim folder called it "Theorem 2.2"; that label is wrong
(the paper has no Theorem 2.2). The paper prints, in its notation (lambda_s(q) is W_sq(q), theta_1(k) is the largest eigenvalue for the
path P_k, theta_2(k) the largest eigenvalue for the cycle C_k):
    theta_1(k+1)/theta_1(k) <= lambda_s(q) <= theta_2(2k)^(1/2k)        (6)
so for even m = 2k, W_sq(5) <= theta_1(C_m)^(1/m) in the notation of this file. The panel's criterion report quotes (6) from the paper
(see panel/criterion.md). The paper gives no proof of (6) and cites its reference [7] for the general treatment.

Collatz-Wielandt: for a nonnegative irreducible matrix M and any vector v with all entries positive,
theta_1(M) <= max_i (M v)_i / v_i. The certificate gives v and y = M v for the quotient of T by the symmetry group
(colour permutations S_5 and the dihedral group of the cycle). Orbit partitions are equitable (Theorem 3.1 and Corollary 3.3 of
Lundow and Markstrom 2008), so the quotient matrix has the same Perron root as T. Hence theta_1(C_14) <= max_i y_i / v_i =: C_hi, and
W_sq(5) <= C_hi^(1/14).

## Claimed bound

Claimed (Argon, truncated at 20 decimals): W_sq(5) <= 3.25040520587854968506...
Rigorous statement in this package: the bound rounded UPWARD at 20 decimals, W_sq(5) <= 3.25040520587854968506
(the panel's gate requires the upward value; for q = 5 the claim already was the upward value).
The value computed from the certificate file by verify-it-yourself/check_cert.py is 3.2504052058785496850598... (80-digit decimal arithmetic).
The published bound the claim is compared with is 3.250407145038276 (C_12^(1/12), from the bank text); the difference is about 1.939159726e-6.

## Sizes

Full transfer matrix: 268435460 states (proper colourings of C_14 with 5 colours). Quotient: 81433 orbits, which is the length n of the vectors in the file.

## File format of the certificate (object/q5_cyl_14_cert.bin, stored as numbered parts)

Documented by Argon's source potts_kink_cert.c (the writer) and confirmed here on small cases by verify-it-yourself/orbit_check.py:
- bytes 0..3: unsigned 32-bit little-endian integer n (number of orbits);
- then n unsigned 256-bit integers v, each 32 bytes, little-endian (four 64-bit limbs, least significant first);
- then n unsigned 256-bit integers y in the same encoding, y = (quotient matrix) v, computed in exact integer arithmetic.
Total length 4 + 64 n bytes. Orbits are numbered in order of first appearance when the proper colourings are listed in
lexicographic order and each is mapped to its orbit under colour permutations, rotations and reflections of the cycle; this numbering was
checked to reproduce the files in object/format_examples/ (widths 6, 7, 8) exactly.

## Other files in object/

- PARTS.txt: sha256 of the whole certificate file and of each part.
- format_examples/: three small certificate files for the same format (byte copies from the snapshot), used only to validate the orbit numbering and the y = C v relation independently.
- THETA_TABLE_q5.txt: copy of the theta_1 table from Argon's RESULTS.md (first 32 digits), used only as data to compare an independent small-width eigenvalue computation against.
