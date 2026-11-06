context: Claude Code subagent, fresh context [claude-sonnet-5-5]

# Reproduce report: kg8-e8-p2

Claim under test (partial win p2 only). The 120 x 120 matrix A = 3G - 13I of object/d8_n1_120x120.mat (G = Gram matrix of the 120 positive roots of E8, in some order and with some signs) has exact local bound L = max over a, b in {-1,+1}^120 of a^T A b equal to 6104; with u_i = r_i / sqrt(2) the quantity Q = sum_ij A_ij <u_i, u_j> is 9240, so K_G(8) >= 9240/6104 = 165/109 = 1.5137614678899083. Definition of the bound, quoted from the criterion text: 'Q divided by the exact local bound L = max over a in {+-1}^m1, b in {+-1}^m2 of sum M_ij a_i b_j'. The verification method asks that L be certified exactly 'with an open exact solver or a custom bound with symmetry, plus a second independent run'.

Preparation. The folder was checked against the contributor's hash list from inside the package folder (all lines OK) and copied to a private location. No network.

## My own derivation and checker (written before opening verify-it-yourself/)

The matrix file is MATLAB 7.3 (HDF5); no HDF5 library is available, so I located the 14400-entry int64 block directly (byte offset 2576, column-major) with a small numpy scan, then did everything else from the definition.

Step 0 (what the matrix is). My own script (not shipped in this package) reads A and checks: symmetric; diagonal all -7; off-diagonal entries in {-3, 0, 3}; G = (A + 13 I)/3 has diagonal 2, rank 8, and G@G = 30 G exactly; the 240 vectors +-v_i are closed under reflection (v_i - G_ij v_j is again +-v_k for all i, j: 0 failures), which makes them a rank-8 root system with 240 roots, i.e. E8. Independently I built the E8 roots (112 of type +-e_i +-e_j and 128 half-integer vectors), chose a generic positive system, and found an exact signed permutation matching the matrix to my Gram matrix (all 14400 entries). Output:

    A symmetric True  diag unique {-7}  offdiag values [-3, 0, 3]
    G diag {2}  rank 8  G@G==30G: True
    reflection-closure failures 0  => 240 vectors +-v form a root system of rank 8 with 240 roots (E8)
    basis [17, 72, 108, 102, 97, 8, 32, 15]
    assignment of basis [0, 1, 88, 27, 107, 6, 30, 143]
    G_mat == signed permutation of my Gram: True

Step 1 (reduction, my own proof). Since a, b range freely, L = max_a ||A a||_1. With rho_j = a_j r_j (one root from each antipodal pair) and x = sum_j rho_j, (A a)_j = 3 r_j.x - 13 a_j, so |(A a)_j| = |13 - 3 rho_j.x|, hence f(a) = sum_j |13 - 3 rho_j.x|.
Step 2 (Weyl symmetry). An element w of the Weyl group permutes the 240 roots, so replacing every rho_j by w rho_j gives another system with one root per pair, x becomes w x and every product rho_j.x is unchanged. Thus f depends only on the W-orbit of x and we may take x dominant.
Step 3 (which dominant x occur). x = sum of roots one from each pair is congruent mod 2 (root lattice) to the sum of the 120 positive roots, which is 2 rho_W, and E8 is unimodular so rho_W lies in the root lattice: x = 2 lambda, lambda = sum m_k omega_k with integers m_k >= 0 (omega_k = fundamental weights). For a dominant omega_k, x.omega_k = sum_j rho_j.omega_k <= sum_j |r_j.omega_k| = 2 rho_W.omega_k, so lambda.omega_k <= rho_W.omega_k for all k. I enumerated all integer m with these 8 inequalities (inverse Cartan matrix has positive integer entries; det of Cartan matrix printed as 1). Output:

    det Cartan 1
    rho.omega_i [68, 91, 135, 110, 84, 57, 29, 46]  |2rho|^2 = 2480
    number of dominant x = 2*lambda candidates: 14869

(The author's list has 18454 vectors because it uses the weaker condition |v|^2 <= 620; mine is the tighter, equally valid set of 14869. Both are supersets of what can occur; see the sampling test below.)
Step 4 (exact dual bound per x). For a sign vector a with sum_j a_j r_j = x and any vector mu: f(a) = sum_j (|3 s_j - 13 a_j| + a_j r_j.mu) - mu.x <= sum_j max_{s=+-1}(|3 s_j - 13 s| + s r_j.mu) - mu.x, where s_j = r_j.x (an integer). I took mu = lambda_x * x with a rational scalar chosen by a float search and then evaluated the bound EXACTLY with Python Fractions (my own script, not shipped in this package). Because f(a) is an integer, a bound below 6105 proves f(a) <= 6104. Output:

    dominant vectors 14869   max exact bound 6104.0   count with bound >= 6105: 0
    count with bound in [6104,6105): 2
    m (0, 0, 0, 5, 0, 1, 0, 0) |x|^2 2424 bound 6104.0 lam 3
    m (0, 6, 0, 0, 0, 0, 0, 1) |x|^2 2368 bound 6104.0 lam 6495373/571849
    m (0, 0, 0, 0, 7, 0, 0, 0) |x|^2 2352 bound 6094.0 lam 9628889/686986
    m (0, 0, 1, 4, 0, 0, 1, 0) |x|^2 2384 bound 6092.0 lam 3
    m (0, 5, 1, 0, 0, 0, 0, 0) |x|^2 2320 bound 6092.0 lam 1533/1000
    m (6, 0, 0, 0, 0, 0, 0, 4) |x|^2 2368 bound 6090.0 lam 1113703/102593

So for all 14869 dominant vectors the exact bound is at most 6104 (none reaches 6105); exactly two dominant vectors reach 6104, matching the author's count of two tight vectors.
Step 5 (lower bound and Q). A further script of mine (not shipped) solves, with the bundled CBC solver, the integer program max f(a) subject to sum_j a_j r_j = x for the two tight x, finds a sign vector with f(a) = 6104, transports it through the signed permutation to the matrix in the .mat file and evaluates it there directly (b = sign(A a)). It also computes Q = sum A_ij G_ij / 2 from the matrix and runs two sanity tests of the reduction: 3000 random sign vectors (largest f = 3810) and 40 hill-climbed local maxima (largest f = 6104; the dominantised x of every one of them lies in my enumerated set). Output:

    Q = sum A_ij G_ij/2 = 9240 (remainder 0 )
    m (0, 0, 0, 5, 0, 1, 0, 0) status Optimal
      f(a) on my A = 6104
    m (0, 6, 0, 0, 0, 0, 0, 1) status Optimal
      f(a) on my A = 6104
    on the .mat matrix: ||A a||_1 = 6104  a^T A b with b=sign(Aa): 6104  (b entries all +-1: True )
    Q/L =  9240 / 6104 = 1.5137614678899083  165/109 = 1.5137614678899083
    max f over 3000 random sign vectors 3810
    hill-climbed local maxima: max f 6104 ; dominant x of 40 of them not in enumerated set: 0

Result of my checker: L = 6104 (lower bound by explicit vectors on the .mat matrix, upper bound by the 14869 exact dual bounds), Q = 9240, Q/L = 9240/6104 = 165/109 = 1.5137614678899083 (9240 = 56 x 165, 6104 = 56 x 109).

## Author's checker, run only afterwards

sh verify-it-yourself/run_checks.sh, lines that matter:

    == e8_check.py: identification with the E8 roots, Q, lower bound, 18454 dual certificates (about 5 s)
    == Phase A: matrix from the MATLAB file
    matrix found (byte offset 0, element 322): 120 x 120, symmetric, diagonal all -7, entries [-7, -3, 0, 3]
    == Phase B: identification with the positive roots of E8
    == Phase C: Q
    A.A = 66360, trace A = -840, Q = (A.A + 13 trace A)/6 = 9240
    == Phase D: lower bound L >= 6104
    witness b has 96 entries +1 and 24 entries -1; a = sign(A b); a^T A b = 6104 ; ||A b||_1 = 6104
    == Phase E: upper bound L <= 6104
    dominant w = 2v with v = sum c_k omega_k, |v|^2 <= 620: 18454 vectors
    certificate lines read: 18454
    dominant vectors without a certificate: 0; certificates with dual value above 6104: 0; with dual value exactly 6104: 2
    largest certified dual value: 6104 at c = (0, 0, 0, 0, 5, 0, 1, 0)
    elapsed 7.7 s
    RESULT PASS: L = 6104, Q = 9240, Q/L = 165/109 = 1.5137614678899083
    == negative control 1: one symmetric pair of matrix entries changed; the check must FAIL
    negative control 1 rejected as expected: RESULT FAIL
    == negative control 2: the certificate of the first tight vector is replaced by zeros; the check must FAIL
    negative control 2 rejected as expected: dominant vectors without a certificate: 0; certificates with dual value above 6104: 1; with dual value exactly 6104: 1
    ALL CHECKS PASS

The author's checker reaches the same L, Q and ratio by a different set of dual certificates (LP-based multipliers over 18454 vectors, exact integers). No disagreement.

## Remarks and answers to open questions that concern reproduction

- The upper-bound argument rests on the Weyl-group symmetry and the dominance condition. I re-derived both (steps 2 and 3 above); they use only that the Weyl group permutes the roots, that E8 is unimodular (Cartan determinant 1 printed above), and that positive roots have non-negative inner product with dominant weights. I did not use any file of the author's beyond the matrix itself. My dual multipliers are a single rational scalar per vector, so they are much simpler than the author's (which use 8 free multipliers and, per the author, values up to 3000 for some vectors); that simple certificates suffice is a second, independent exact method for the bound (open questions 3 and 4).
- Open question 2 (is the matrix the authors' own, and is the proof independent of the paper's files): I read the matrix only as an integer array and rebuilt the root system myself, so my proof does not use the stored values 9240 and 6104 or any Julia data; the matrix being the paper authors' file is not checkable from the folder.
- Open question 1 (what p2 credits given 165/109 is already printed as heuristic) and open question 5 (newer papers; no network here): not reproduction questions; left to the criterion and novelty skeptics.

pass: true
