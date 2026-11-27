# A lower bound for the least common multiple of a covering system with distinct odd moduli

*Proof document. The status of each section is given at its head (DONE or UNFINISHED).*

## 0. Statement and plan (DONE)

A *covering system* is a finite set of residue classes a_1 mod n_1, ..., a_k mod n_k whose union is the set Z of all integers. It is an *odd covering* if the moduli n_i are odd, greater than 1 and pairwise distinct. Whether an odd covering exists is the question of Erdős and Selfridge (Erdős Problem 7); it is open. Write L = lcm(n_1, ..., n_k) and omega(L) for the number of primes dividing L.

**Theorem 1.** Every odd covering satisfies

    L >= 6,557,114,959,770,375 = 3^5 * 5^3 * 7^2 * 11^2 * 13^2 * 17 * 19 * 23 * 29.

Throughout, X0 denotes this number.

**How the proof is organised.**

1. Sections 1 and 2 reduce Theorem 1 to finitely many statements of one kind: *a certain finite or infinite product of digit spaces cannot be covered by classes with pairwise distinct moduli* ("an excluded cap vector"). The reduction uses prime replacement (Lemma 2.1) and an enumeration of exponent vectors.
2. Section 3 collects seven general lemmas (completion; a capped kernel; three convexity inequalities; an accounting identity for a product of kernels; and the comparison that these give together).
3. Section 4 proves a criterion for exclusion that needs one rational number per cap vector (the *scalar bound*, Proposition 4.1).
4. Sections 5 to 8 prove a second, stronger criterion (the *anchored bound*, Theorem 8.2), which needs a finite list of inequalities between rational numbers per cap vector. This is the method of M. Schroeder's preprint [S]; it is written out here in full, with exponent caps added.
5. Section 9 lists the cap vectors, says which certificate file is checked against which inequality, and proves Theorem 1. In particular it contains a proof that omega(L) >= 9 (Theorem A; due to Schroeder), so nothing here rests on a preprint.
6. Section 10 says what is not claimed. Section 11 gives the sources.

**What is proved by hand and what by machine.** Every lemma is proved in this document. The finite computations are of three kinds, all in exact rational arithmetic: (i) the value B of Proposition 4.1 for 738 cap vectors; (ii) the two sides R and S of the inequalities of Section 8 for 37 cap vectors (29,485 inequalities); (iii) the enumeration of 6,782 exponent vectors in Proposition 2.4. Section 9.4 states exactly what a checking program has to recompute. The proof is complete only together with a successful run of such a program on the certificate files.

**Conventions.** Primes are odd unless said otherwise. p_1 = 3 < p_2 = 5 < p_3 = 7 < ... is the sequence of odd primes. [.] and 1[.] denote indicators, (x)_+ = max(x, 0). An *exponent cap* is a positive integer or the symbol inf.

---

## 1. Digit spaces, classes, excluded cap vectors (DONE)

**1.1 Digit spaces.** For a prime p and a cap e, let X(p, e) be the set of digit sequences (x_1, ..., x_e) with x_j in {0, ..., p-1} (infinite sequences if e = inf), with the product of the uniform probability measures on the digits. For 0 <= t <= e (t finite) and digits d_1, ..., d_t, the set of sequences that begin with d_1, ..., d_t is a *cylinder of depth t*; it has measure p^(-t); the cylinder of depth 0 is the whole space. Two cylinders of X(p, e) are nested or disjoint.

Let P be a finite set of primes and e = (e_p) a cap for each p in P; the pair (P, e) is a *cap vector*. Put X = X(P, e) = prod_{p in P} X(p, e_p) with the product measure H. A *class* is a product of cylinders, one in each coordinate, of depths (t_p), not all zero. Its *modulus* is m = prod p^(t_p) > 1, its *exponent vector* is (t_p), and H(class) = 1/m. If d divides m, a class of modulus m is contained in, or disjoint from, any class of modulus d.

**1.2 Residues.** A cylinder of depth t in X(p, e) with digits d_1, ..., d_t is named by the residue d_1 + d_2 p + ... + d_t p^(t-1) modulo p^t, and a class of modulus m is named by a residue modulo m through the Chinese remainder theorem. So "the class a mod m" has a meaning in X(P, e) whenever m is a product of powers p^(t_p) with p in P and t_p <= e_p. For example "1 mod 9" is the cylinder of the coordinate 3 with digits (1, 0).

**Lemma 1.1.** Let (P, e) be a cap vector and a_i mod n_i (i = 1, ..., k) residue classes whose moduli are products of powers p^t with p in P, t <= e_p. They cover Z if and only if the classes of X(P, e) with the same names cover X(P, e).

*Proof.* Let t_p be the largest exponent of p in the n_i and M = prod p^(t_p). The residues modulo M correspond one to one to the classes of X(P, e) with exponent vector (t_p); these classes partition X(P, e), and under the correspondence the residues modulo M that lie in a_i mod n_i are exactly the classes of that kind contained in the class named a_i mod n_i. So both statements say that every residue modulo M lies in some a_i mod n_i. QED

**Definition.** A cap vector (P, e) is *excluded* if no finite family of classes of X(P, e) with pairwise distinct moduli covers X(P, e). A cap vector (P, e) *dominates* (P', e') if P' is contained in P and e'_p <= e_p for all p in P'.

**Lemma 1.2 (monotonicity).** If (P, e) is excluded and dominates (P', e'), then (P', e') is excluded.

*Proof.* A covering family of X(P', e') with distinct moduli gives, by Lemma 1.1, residue classes with the same distinct moduli that cover Z; the same residue classes name classes of X(P, e), which cover X(P, e) by Lemma 1.1 again. QED

**1.3 Tree automorphisms.** A *tree automorphism* of X(p, e) is a bijection that maps every cylinder of depth t onto a cylinder of depth t, for every t. (It is given by a permutation of the p children at every node of the digit tree.) A product of tree automorphisms, one in each coordinate, preserves H, maps classes to classes with the same modulus, and therefore maps a covering family with distinct moduli to a covering family with distinct moduli. Disjointness and inclusion of classes are preserved.

---

## 2. Reduction to finitely many cap vectors (DONE)

**Lemma 2.1 (prime replacement).** Let L = q_1^(f_1) ... q_r^(f_r), with primes q_1 < ... < q_r, be the least common multiple of the moduli of an odd covering, and let p'_1 < ... < p'_r be odd primes with p'_m <= q_m for all m. Then the cap vector ({p'_1, ..., p'_r}, (f_1, ..., f_r)) is not excluded.

*Proof.* By Lemma 1.1 the covering gives a covering family F of Y = prod_m X(q_m, f_m) with pairwise distinct moduli. Let Y' = prod_m X(p'_m, f_m) and let i: Y' -> Y be the map that keeps every digit (possible because the digits of the m-th coordinate of Y' are < p'_m <= q_m). Let K be a class of Y with exponent vector (t_m) and digits d_(m,1), ..., d_(m,t_m). Its preimage under i is empty if some d_(m,j) >= p'_m, and otherwise it is the class of Y' with the same exponent vector and the same digits. The preimages of the members of F cover Y'. The non-empty ones are classes of Y' whose exponent vectors are those of their originals; these are non-zero and pairwise distinct, so their moduli prod p'_m^(t_m) are pairwise distinct. QED

*Remark.* This is the prime replacement principle; [S, Lemma 2.1] attributes it to Simpson and Zeilberger [SZ]. Exponents are kept: the m-th smallest prime of L and its replacement carry the same cap f_m.

**Corollary 2.2.** Let L be the least common multiple of an odd covering, r = omega(L), q_1 < ... < q_r its primes and f_m the exponent of q_m. Then the cap vector ({p_1, ..., p_r}, (f_1, ..., f_r)) on the first r odd primes is not excluded, and p_1^(f_1) ... p_r^(f_r) <= L.

*Proof.* q_1 < ... < q_r are distinct odd primes, so q_m >= p_m. Apply Lemma 2.1. QED

From now on a cap vector on the first r odd primes is written as the list of its caps, (e_1, ..., e_r).

**Proposition 2.3 (reduction).** Suppose that

- (E8) the cap vector (inf, inf, inf, inf, inf, inf, inf, inf) on the first eight odd primes is excluded, and
- (E9-13) for each r in {9, 10, 11, 12, 13}, every vector f = (f_1, ..., f_r) of positive integers with p_1^(f_1) ... p_r^(f_r) < X0 is dominated by an excluded cap vector on the first r odd primes.

Then Theorem 1 holds.

*Proof.* Suppose an odd covering has L < X0, and let r and f be as in Corollary 2.2. Then (f_1, ..., f_r) is not excluded and prod p_m^(f_m) <= L < X0. If r >= 14, then prod p_m^(f_m) >= p_1 p_2 ... p_14 = 307,444,891,294,245,705 > X0, a contradiction. If r <= 8, the vector f on the first r odd primes is dominated by the vector of (E8), so it is excluded by Lemma 1.2, a contradiction. If 9 <= r <= 13, f is dominated by an excluded cap vector by (E9-13), so it is excluded by Lemma 1.2, a contradiction. QED

**Proposition 2.4 (the exponent vectors; by enumeration).** The numbers of vectors f of r positive integers with prod_{m <= r} p_m^(f_m) < X0 are

    5,028 for r = 9,    1,484 for r = 10,    248 for r = 11,    21 for r = 12,    1 for r = 13

(for r = 13 it is the vector of ones: p_1 ... p_13 = 6,541,380,665,835,015 < X0). Each of the 5,028 vectors with r = 9 is dominated by one of the 23 cap vectors F9_01, ..., F9_23 of Section 9.2. Each of the 1,754 vectors with 10 <= r <= 13 is dominated by one of the 751 cap vectors of Section 9.3 on the first r odd primes (738 of type U and 13 of type G). *This is a finite check: item (iii) of Section 9.4.*

So Theorem 1 follows once the cap vector of (E8), the 23 cap vectors F9_01, ..., F9_23 and the 751 cap vectors of Section 9.3 are shown to be excluded. The rest of the document is about proving that a given cap vector is excluded.

---

## 3. Seven lemmas (DONE)

### Lemma 3.1 (completion) [S, Lemma 2.2]

Let (P, e) be a cap vector and D a finite or countable set of moduli of classes of X(P, e) such that

    sum of 1/d over all d in D with d | m, d < m   is less than 1,   for every m in D.

Let F be a finite family of classes of X(P, e) with pairwise distinct moduli. Then there is a family F' of classes with pairwise distinct moduli such that: (i) every point covered by F is covered by F'; (ii) F' contains exactly one class C_m of modulus m for every m in D; (iii) C_d and C_m are disjoint whenever d, m are in D, d | m and d < m; (iv) the classes of F' whose modulus is not in D are the classes of F whose modulus is not in D (in particular they are finitely many).

*Proof.* Treat the elements m of D in increasing order. When m is reached, a class C_d has been fixed for every proper divisor d of m in D. The class C_d contains m/d classes of modulus m, so the fixed classes contain at most m * sum 1/d < m of the m classes of modulus m, and a class Q of modulus m disjoint from all of them exists. If F has no class of modulus m, put C_m = Q. If F has a class K of modulus m that is disjoint from every fixed C_d (d | m, d < m, d in D), put C_m = K. If F has a class K of modulus m that meets a fixed C_d, then K is contained in C_d (Section 1.1); put C_m = Q. A class once fixed is never changed. Let F' consist of the C_m (m in D) and of the classes of F with modulus outside D. Properties (ii), (iii), (iv) are clear. For (i): a class K of F with modulus m in D either equals C_m or is contained in some C_d, and both are in F'. QED

### Lemma 3.2 (capped kernel) [S, Lemma 3.1]

Let (Y, H) be a probability space, E a measurable subset, G = Y minus E, and C >= 1. Put delta = 1 - 1/C. The function k = min(C, 1/H(G)) 1_G (k = 0 if H(G) = 0) satisfies 0 <= k <= C, k = 0 on E, and

    integral of k dH = 1 - l,   where l = (1 - C H(G))_+ = C (H(E) - delta)_+ .

*Proof.* The integral is min(C H(G), 1), and 1 - C H(G) = 1 - C (1 - H(E)) = C (H(E) - 1 + 1/C). QED

### Lemma 3.3 (ordered increments) [S, Lemma 4.1]

Let mu be a measure of total mass at most S on some space, f a non-decreasing convex function from [0, inf) to [0, inf), b >= 0, w_1, ..., w_K >= 0, and E_1, ..., E_K measurable sets with mu(E_j) <= lambda_j. Put S_0 = b and S_j = b + w_1 + ... + w_j. Then

    integral of f(b + sum_j w_j 1[E_j]) dmu  <=  S f(S_0) + sum_{j=1..K} lambda_j (f(S_j) - f(S_{j-1})).

*Proof.* Fix a point, and let j_1 < ... < j_n be the indices j with the point in E_j. Then f(b + w_{j_1} + ... + w_{j_n}) - f(b) is the sum over i of the increase of f when w_{j_i} is added to the base b + w_{j_1} + ... + w_{j_(i-1)}. This base is at most S_{j_i - 1}, and for a convex function the increase f(x + w) - f(x) is non-decreasing in x. So the i-th increase is at most f(S_{j_i}) - f(S_{j_i - 1}). Hence, at every point, f(b + sum_j w_j 1[E_j]) <= f(b) + sum_j (f(S_j) - f(S_{j-1})) 1[E_j]. Integrate; f(b) >= 0 and the increments f(S_j) - f(S_{j-1}) are >= 0 because f is non-decreasing. QED

### Lemma 3.4 (cylinder comparison) [S, Lemma 4.2]

Let p be a prime, e a cap, and mu a finite measure on X(p, e). Let S >= 0 and C >= 0 be numbers with C/p <= S such that mu has total mass at most S and mu(Q) <= C p^(-t) for every cylinder Q of depth t >= 1. Let f be as in Lemma 3.3, b >= 0, and let finitely many *labels* i be given (possibly none), each with a weight c_i >= 0 and a cylinder Q_i of depth t_i >= 1. Then

    integral of f(b + sum_i c_i 1[x in Q_i]) mu(dx)  <=  sum_{j >= 0} pi(j) f(b + sum_{i : t_i <= j} c_i),

where j runs over the integers 0 <= j <= e and

    pi(0) = S - C/p,   pi(j) = C (p-1)/p^(j+1) for 1 <= j < e,   pi(e) = C p^(-e) if e is finite.

The numbers pi(j) are >= 0 and their sum is S.

*Proof.* If there are no labels, the left side is f(b) times the total mass of mu, which is at most S f(b), the right side. Otherwise put lambda(t) = C p^(-t), number the labels so that t_1 <= ... <= t_K, and apply Lemma 3.3 with lambda_i = lambda(t_i). With lambda_{K+1} = 0, summation by parts turns the bound into

    (S - lambda(t_1)) f(S_0) + sum_{i=1..K} (lambda(t_i) - lambda(t_{i+1})) f(S_i).

For an integer j let n(j) be the number of labels with t_i <= j; then f(b + sum_{t_i <= j} c_i) = f(S_{n(j)}). The numbers pi(j) with j >= 1 are lambda(j) - lambda(j+1) (with lambda(e+1) = 0 for finite e), so the pi(j) with n(j) = 0, that is j < t_1, add up to S - lambda(t_1); those with n(j) = i for an i with t_i < t_{i+1}, that is t_i <= j < t_{i+1}, add up to lambda(t_i) - lambda(t_{i+1}); and those with n(j) = K add up to lambda(t_K). If t_i = t_{i+1} the coefficient of f(S_i) is zero on both sides. So the two expressions agree. QED

### Lemma 3.5 (weighted aggregation) [S, Lemma 4.3]

Let K be a finite set, a_x >= 0 and b_x real numbers (x in K), f a non-decreasing convex function on the real line, g a positive integer, x -> x mod g a map from K to Z/g, and c_1, ..., c_n >= 0 weights with c_1 + ... + c_n <= C, attached to residues r_1, ..., r_n modulo g. Then

    sum_x a_x f(b_x + sum_i c_i [x = r_i mod g])  <=  max over r in Z/g of  sum_x a_x f(b_x + C [x = r mod g]).

*Proof.* If C = 0 there is nothing to prove. Put c_0 = C - (c_1 + ... + c_n) >= 0 and let r_0 be any residue. For each x, since f is non-decreasing, the left argument is at most b_x + sum_{i=0..n} c_i [x = r_i mod g], which is the convex combination with weights c_i/C of the numbers b_x + C [x = r_i mod g]. By convexity the left side is at most sum_{i=0..n} (c_i/C) Phi(r_i), where Phi(r) = sum_x a_x f(b_x + C [x = r mod g]); and an average is at most the maximum. QED

### Lemma 3.6 (first-hit accounting) [S, Lemma 3.2]

*Setting.* Let (P, e) be a cap vector. Split P into a non-empty set of *anchor primes* and the *later primes*, listed in a fixed order q_1, ..., q_s (s >= 1). Write Y_0 for the product of the anchor coordinates, Y_i = X(q_i, e_(q_i)), and call a point of Y_0 x Y_1 x ... x Y_(i-1) a *prefix of length i* (for i = 1: a point of Y_0). Let F' be a finite or countable family of classes of X(P, e). The *stage* of a class is the largest i such that q_i divides its modulus (stage 0 if no later prime does). A class is *pure* if its modulus is a prime power, *mixed* otherwise.

*Data.* (a) A finite measure nu_0 on Y_0 such that nu_0(K) = 0 for the anchor part K of every class of F' of stage 0. (b) For each i >= 1, a measurable subset P_i of Y_i containing every pure class of F' of the prime q_i (regarded as a cylinder of Y_i). (c) For each i >= 1 and each prefix x of length i, a subset B_i(x) of Y_i, depending measurably on x, that contains the q_i-cylinder of every mixed class of F' of stage i whose projection to the coordinates of the prefix contains x. (d) Numbers C_i >= 1.

*Construction.* For a prefix x of length i let G_i(x) = Y_i minus (P_i u B_i(x)), let k_i(. | x) be the density of Lemma 3.2 for E = P_i u B_i(x) and C = C_i, and put

    l_i(x) = 1 - integral of k_i(. | x) dH = C_i (H(P_i u B_i(x)) - delta_i)_+ ,   delta_i = 1 - 1/C_i,   m_i(x) = 1 - l_i(x).

Define measures nu_i on Y_0 x ... x Y_i by nu_i(dx, dx_i) = nu_(i-1)(dx) k_i(x_i | x) H(dx_i), and the *losses* L_i = integral of l_i(x) nu_(i-1)(dx).

*Claims.*
1. nu_s(K) = 0 for every class K of F'.
2. nu_s(X) = nu_0(Y_0) - (L_1 + ... + L_s).
3. For every prefix x of length i and every cylinder Q of Y_i of depth t: the k_i(. | x)-mass of Q is at most min(m_i(x), C_i q_i^(-t)), and m_i(x) <= 1.
4. If nu_0^+ is a measure on Y_0 with nu_0 <= nu_0^+, and nu_i^+, L_i^+ are defined from nu_0^+ with the same kernels, then L_i <= L_i^+ for all i.
5. Consequently, if F' covers X(P, e), then L_1^+ + ... + L_s^+ >= nu_0(Y_0).

*Proof.* (1) Let K be a class of F'. If its stage is 0, K is the product of its anchor part K_0 with the remaining coordinates, and nu_s(K) <= nu_0(K_0) = 0 (kernels have mass at most 1). If its stage is i >= 1, write K as the set of points whose prefix of length i lies in a set K' and whose i-th coordinate lies in a cylinder Q. If K is pure, Q is contained in P_i; if K is mixed, Q is contained in B_i(x) for every x in K'. In both cases k_i(. | x) vanishes on Q for every x in K', so nu_i(K' x Q) = 0, and nu_s(K) <= nu_i(K' x Q). (2) nu_i has total mass integral of m_i dnu_(i-1) = nu_(i-1)(total) - L_i. (3) k_i <= C_i, and H(Q) = q_i^(-t); m_i(x) = min(C_i H(G_i(x)), 1). (4) L_i is the integral of a non-negative function against nu_0 followed by kernels, hence monotone in nu_0. (5) By (1) and countable subadditivity nu_s(X) = 0, so by (2) and (4) nu_0(Y_0) = sum L_i <= sum L_i^+. QED

### Lemma 3.7 (nested comparison) [S, Section 4]

In the setting of Lemma 3.6 fix a stage i >= 1 and a measure nu_0^+ on Y_0, and suppose that for each j < i there is a measurable function S_j on Y_0 with

    C_j/q_j <= S_j(y) <= 1   and   m_j(x) <= S_j(y) for every prefix x of length j whose anchor point is y.

Let f be non-decreasing and convex from [0, inf) to [0, inf), b >= 0, and let finitely many labels t be given, each with a weight c_t >= 0, a measurable subset R_t of Y_0, and for each j < i a cylinder Q_(t,j) of Y_j of depth e_j(t) >= 0. Then

    integral of f(b + sum_t c_t 1[y in R_t] prod_{j<i} 1[x_j in Q_(t,j)]) dnu_(i-1)^+
        <=  integral over Y_0 of nu_0^+(dy) sum_J pi_y(J) f(b + sum over the t with e_j(t) <= J_j for all j < i of c_t 1[y in R_t]).

Here J = (J_1, ..., J_(i-1)) runs over the vectors of integers with 0 <= J_j <= e_(q_j), pi_y(J) = prod_j pi_(j,y)(J_j), and pi_(j,y) is the sequence of Lemma 3.4 for the prime q_j, the cap e_(q_j), C = C_j and S = S_j(y):

    pi_(j,y)(0) = S_j(y) - C_j/q_j,   pi_(j,y)(n) = C_j (q_j - 1)/q_j^(n+1) for 1 <= n < e_(q_j),   pi_(j,y)(e_(q_j)) = C_j q_j^(-e_(q_j)) for a finite cap.

For i = 1 the statement is empty (both sides are the integral of f(b + sum_t c_t 1[y in R_t]) against nu_0^+).

*Proof.* Induction on the number of later coordinates, the last one first. Fix a prefix x of length i-1 with anchor point y and integrate over the coordinate x_(i-1) against k_(i-1)(. | x) H. As a function of x_(i-1) the integrand is f(b' + sum c_t 1[x_(i-1) in Q_(t,i-1)]), the sum over the labels t that are *alive at x* (y in R_t and x_j in Q_(t,j) for j < i-1) and have e_(i-1)(t) >= 1, and b' is b plus the weights of the labels alive at x with e_(i-1)(t) = 0. By Lemma 3.6(3) the measure k_(i-1)(. | x) H has total mass at most S_(i-1)(y) and gives mass at most C_(i-1) q_(i-1)^(-t) to a cylinder of depth t. Lemma 3.4 bounds the integral by sum over J_(i-1) of pi_(i-1,y)(J_(i-1)) f(b + sum of c_t over the labels alive at x with e_(i-1)(t) <= J_(i-1)). For each fixed value of J_(i-1) this is again a function of the required form of the prefix x of length i-1, with the labels restricted to those with e_(i-1)(t) <= J_(i-1) and the coefficient pi_(i-1,y)(J_(i-1)) >= 0, which depends on the anchor point only. Repeat with the coordinate i-2, and so on. QED

*Remark.* The variables J_j are bookkeeping. No independence of the real coordinates is claimed or used.

---

## 4. The scalar bound (DONE)

**Proposition 4.1.** Let p'_1 < ... < p'_r be odd primes (r >= 2) with finite caps e_1, ..., e_r, let 1 <= k0 < r, and for each i with k0 < i <= r let C_i be a rational number with 1 < C_i <= p'_i. Put

    rho_m = (1 - p'_m^(-e_m))/(p'_m - 1),    theta_m = rho_m/(1 - rho_m),    delta_i = 1 - 1/C_i.

Let T_1, ..., T_(r-1) be independent random variables, T_m with values in {0, 1, ..., e_m}, with

    Prob(T_m >= t) = p'_m^(-t)/(1 - rho_m)  for m <= k0,     Prob(T_m >= t) = C_m p'_m^(-t)  for m > k0     (1 <= t <= e_m).

Put

    B = prod_{m <= k0} (1 + theta_m) - 1 - sum_{m <= k0} theta_m + sum_{i > k0} C_i E[(rho_i prod_{m < i} (1 + T_m) - delta_i)_+].

If B < 1, the cap vector ({p'_m}, (e_m)) is excluded.

(The tail probabilities define laws: they decrease in t, and Prob(T_m >= 1) <= 1 because rho_m <= 1/2 and C_m <= p'_m.)

*Proof.* Suppose a finite family F with pairwise distinct moduli covers X = X({p'_m}, (e_m)). Here X is a finite set and H is the uniform measure.

*Completion.* Let D be the set of all prime powers p'_m^t, 1 <= t <= e_m. For m = p^t in D the sum of 1/d over the proper divisors in D is 1/p + ... + 1/p^(t-1) < 1/(p-1) <= 1/2. Apply Lemma 3.1; write F' for the result. In F' the pure classes of the prime p'_m are pairwise disjoint cylinders of depths 1, ..., e_m; their union P_m has H(P_m) = sum_{t=1..e_m} p'_m^(-t) = rho_m.

*Anchor.* The anchor primes are p'_1, ..., p'_k0; the later primes are p'_(k0+1), ..., p'_r in this order. Let mu_m be the uniform probability measure on X(p'_m, e_m) minus P_m, and nu_0^+ the product of mu_1, ..., mu_k0, a probability measure on Y_0. A cylinder of depth t has mu_m-mass at most p'_m^(-t)/(1 - rho_m). Let nu_0 be the restriction of nu_0^+ to the complement of the union of the mixed classes of F' of stage 0. Then nu_0 vanishes on every class of F' of stage 0, pure or mixed. A mixed class of stage 0 with exponent vector (t_m) has nu_0^+-mass at most the product over the m with t_m > 0 of p'_m^(-t_m)/(1 - rho_m). Exponent vectors of distinct classes are distinct, and a mixed class has at least two non-zero exponents; summing over all such vectors with t_m <= e_m gives

    nu_0(Y_0) >= 1 - sum over subsets I of {1..k0} with |I| >= 2 of prod_{m in I} theta_m = 1 - ( prod_{m <= k0}(1 + theta_m) - 1 - sum_{m <= k0} theta_m ),

because sum_{t=1..e_m} p'_m^(-t)/(1 - rho_m) = theta_m.

*Kernels.* Use Lemma 3.6 with P_i the union of the pure classes of the i-th later prime, B_i(x) the union of the cylinders of the mixed classes of stage i that are alive at x (whose projection to the prefix coordinates contains x), and the caps C_i. Fix a later prime, write q for it, i for its index in p'_1, ..., p'_r, and rho, delta, C for rho_i, delta_i, C_i. By the union bound H(P_i u B_i(x)) <= rho + sum q^(-e_t) over the mixed classes t of stage q alive at x, where e_t >= 1 is the q-exponent of t. So l_i(x) <= f(rho + sum_t q^(-e_t) 1[t alive at x]) with f(s) = C (s - delta)_+, a non-decreasing convex function with values >= 0.

*Comparison.* Apply Lemma 3.7 with b = rho, the labels t = the mixed classes of stage q, c_t = q^(-e_t), S_j = 1 (allowed because C_j <= p'_j), and then Lemma 3.4 in each anchor coordinate in turn (the measure nu_0^+ is a product; for the coordinate m <= k0 take S = 1 and C = 1/(1 - rho_m), so that C/p'_m <= 1). The outcome is

    L_i^+ <= E[ f( rho + sum of q^(-e_t) over the labels t whose depth at the m-th prime is at most T_m for every m < i ) ],

with T_1, ..., T_(i-1) independent with the laws stated in the proposition: for m <= k0 the sequence pi of Lemma 3.4 is Prob(T_m = j), since pi(j) = lambda(j) - lambda(j+1) with lambda(t) = p'_m^(-t)/(1 - rho_m); for k0 < m < i it is the sequence of Lemma 3.7 with S = 1.

*Inventory.* A label is determined by its exponent vector: its q-exponent e in {1, ..., e_i} and its depths (d_m) at the earlier primes, not all zero. Distinct labels have distinct vectors. For given T, the vectors with d_m <= T_m for all m < i number at most (prod_{m<i}(1 + T_m) - 1) for each value of e, so the sum of q^(-e_t) over those labels is at most (prod_{m<i}(1 + T_m) - 1) sum_{e=1..e_i} q^(-e) = rho (prod_{m<i}(1 + T_m) - 1). As f is non-decreasing,

    L_i^+ <= C_i E[(rho_i prod_{m<i}(1 + T_m) - delta_i)_+].

*Conclusion.* By Lemma 3.6(5), sum_i L_i^+ >= nu_0(Y_0). With the two displayed bounds this says B >= 1. QED

**4.2 Exact evaluation.** Write M = prod_{m<i}(1 + T_m), a positive integer. Since (x)_+ = x + (-x)_+,

    E[(rho M - delta)_+] = rho E[M] - delta + sum over the integers k with rho k < delta of Prob(M = k)(delta - rho k),

and E[M] = prod_{m<i}(1 + sum_{t=1..e_m} Prob(T_m >= t)). So B is a rational number that is computed exactly from the law of M on the finitely many integers k < delta/rho. *This is the computation of item (i) of Section 9.4.*

*Remarks.* (1) The proof does not use any relation between delta_i and rho_i; a checking program may impose delta_i >= rho_i as an additional restriction on its input. (2) Proposition 4.1 is the scalar form of the method of [S]: one anchor measure, capped kernels, and the comparison of Lemma 3.7, with no geometry kept. It is weaker than the anchored bound below, and much cheaper.

---

## 5. The anchored method: the anchor (DONE)

Sections 5 to 8 prove Theorem 8.2: a cap vector is excluded if a finite list of inequalities holds. Sections 5 to 7 are mathematics; Section 8 defines the inequalities.

### 5.1 Standing assumptions

The cap vector is (P, e) with P = {3, 5, q_1, ..., q_s}, where q_1 = 7 < q_2 < ... < q_s are primes (s >= 2), and e_3 >= 3, e_5 >= 2 (finite or inf); the caps of the later primes are arbitrary. For p in P put

    rho_p = sum_{t=1..e_p} p^(-t) = (1 - p^(-e_p))/(p - 1)   (= 1/(p-1) for e_p = inf),      n_p = 1/rho_p.

The anchor primes are 3 and 5, Y_0 = X(3, e_3) x X(5, e_5), and the later primes are taken in increasing order. A *cell* is a class of Y_0 of modulus 135 = 27 * 5: a cylinder of depth 3 of the coordinate 3 (its *row*, named by a residue modulo 27) times a cylinder of depth 1 of the coordinate 5 (its *column*, named by a residue modulo 5). Cells are named by residues x modulo 135. For g in

    G = (3, 9, 27, 5, 15, 45, 135)

and a residue r modulo g, "x = r mod g" means that the cell x lies in the class r mod g of Y_0. **Masses on Y_0 are measured in cells: one cell is Haar measure 1/135.** So a cell has mass 1, a class of modulus 15 has mass 9, and so on.

We assume, for a contradiction, that a finite family F of classes with pairwise distinct moduli covers X(P, e).

### 5.2 The completed family

Let D consist of: all prime powers p^t with p in P and 1 <= t <= e_p; the seven moduli 15, 45, 75, 21, 35, 63, 105; and the modulus 15 q_2 (it is 165 when q_2 = 11). All are moduli of classes of X(P, e) because e_3 >= 3 and e_5 >= 2. The sums of 1/d over the proper divisors d in D are:

| m | proper divisors in D | sum |
|---|---|---|
| p^t | p, ..., p^(t-1) | < 1/(p-1) <= 1/2 |
| 15 | 3, 5 | 8/15 |
| 45 | 3, 9, 5, 15 | 32/45 |
| 75 | 3, 5, 25, 15 | 16/25 |
| 21 | 3, 7 | 10/21 |
| 35 | 5, 7 | 12/35 |
| 63 | 3, 9, 7, 21 | 40/63 |
| 105 | 3, 5, 7, 15, 21, 35 | 86/105 |
| 15 q_2 | 3, 5, 15, q_2 | 3/5 + 1/q_2 <= 38/55 |

All are below 1, so Lemma 3.1 applies. Let F' be the completed family and C_m its class of modulus m (m in D). Then: F' covers X(P, e); F' has pairwise distinct moduli; F' has finitely many mixed classes; for each p the pure classes C_(p^t) are pairwise disjoint, and their union P_p, a subset of X(p, e_p), has measure rho_p; and C_d, C_m are disjoint whenever d | m, d < m, both in D.

### 5.3 Normal form

**Lemma 5.1 (normal form) [S, Section 5].** After applying a suitable product of tree automorphisms (Section 1.3) to F', there are

    a in {1, 2},   b in {2, 4},   c in {a, 3 - a},   r in Rep(a, b, c),   d in {1, 2},   k in {1, 2, 3, 4} with (d, k) != (a, a)

such that C_3 = 0 mod 3, C_9 = 1 mod 9, C_27 = b mod 27, C_5 = 0 mod 5, C_15 = a mod 15, C_25 is contained in the class c mod 5, C_45 = r mod 45, and C_75 is contained in the class of modulus 15 that is d mod 3 and k mod 5. Here Rep(a, b, c) is defined as follows: call r in {0, ..., 44} *admissible* if 3 does not divide r, r != 1 mod 9, 5 does not divide r and r != a mod 15; the *signature* of r is (r mod 3, [r = b mod 9], [r = a mod 5], [r = c mod 5]); Rep(a, b, c) is the set of the least admissible residues of each signature.

Moreover, with R15(a) = {x mod 15 : 3 does not divide x, 5 does not divide x, x != a mod 15} (seven residues) and

    Xi(a) = {1, 2} x {1, 2, 3, 4} x {2, 4, 5, 7, 8} x R15(a)      (280 elements),

the residues xi = (xi_3, xi_5, xi_9, xi_15) of the anchor parts of C_21, C_35, C_63, C_105 modulo 3, 5, 9, 15 form an element of Xi(a), and the residue eta modulo 15 of the anchor part of C_(15 q_2) is in R15(a). The classes C_21, C_35, C_63, C_105 are disjoint from C_7.

*Proof.* Tree automorphisms preserve everything listed in Section 5.2. (1) Permute the first digits of the coordinate 3 so that C_3 has first digit 0, and likewise at 5 for C_5. (2) C_9 is disjoint from C_3, so its first digit is 1 or 2; permute the first digits 1 and 2 so that it is 1, and then the three children of the node (1) so that C_9 has digits (1, 0), that is, C_9 = 1 mod 9. (3) C_15 is disjoint from C_3 and from C_5, so its digit at 3 is some a in {1, 2} and its digit at 5 is not 0; permute the non-zero first digits at 5 so that the latter equals a. Then C_15 = a mod 15. (4) C_27 is disjoint from C_3 and C_9. If its first digit is 2, permute the children of the node (2) and then the children of the node of depth 2 that contains C_27, so that C_27 has digits (2, 0, 0) = 2 mod 27. If its first digit is 1, its second digit is not 0; permute the children (1, 1) and (1, 2) of the node (1) so that it is 1, and then the third digit to 0; then C_27 has digits (1, 1, 0) = 4 mod 27. Steps (2) and (3) are not disturbed. (5) C_25 is disjoint from C_5, so its first digit c' is not 0. If c' = a put c = a; otherwise permute the first digits at 5 other than 0 and a so that c' becomes 3 - a, and put c = 3 - a. (6) C_45 is a cylinder of depth 2 at 3 (a node of depth 2, named by r mod 9) times a first digit at 5 (r mod 5); it is disjoint from C_3, C_9, C_5 and C_15, so r is admissible. The following tree automorphisms preserve steps (1) to (5): at the coordinate 3, a permutation of the nodes of depth 2 below one first digit that fixes the node (1, 0) and the node containing C_27; at the coordinate 5, a permutation of the first digits that fixes 0, a and c. If r and r' are admissible with the same signature, their nodes of depth 2 have the same first digit and either both contain C_27 or neither does (and neither is (1, 0)), and their first digits at 5 are both a, or both c, or both different from 0, a, c. So such automorphisms move C_45 to the class of the least admissible residue of its signature. (7) C_75 is a first digit d at 3 times a cylinder of depth 2 at 5 in a column k; it is disjoint from C_3 and C_5, so d and k are not 0, and from C_15, so (d, k) != (a, a). (8) C_21 is disjoint from C_3; C_35 from C_5; C_63 from C_3 and C_9; C_105 and C_(15 q_2) from C_3, C_5 and C_15; this gives the ranges of xi and eta. Finally 7 divides 21, 35, 63, 105, so these classes are disjoint from C_7. QED

From now on F' is in normal form. The numbers a, b, c, r, d, k, the tuple xi and the residue eta are the *discrete data* of the family.

### 5.4 Core, budgets, cell weights

*Rows.* Rows(b) is the set of the 14 residues h modulo 27 with 3 not dividing h, h != 1 mod 9, h != b. These are the rows disjoint from C_3, C_9, C_27.

*Core.* K = K(a, b, r) is the set of cells x modulo 135 with: 3 does not divide x, x != 1 mod 9, x != b mod 27, 5 does not divide x, x != a mod 15, x != r mod 45. These are the cells disjoint from C_3, C_9, C_27, C_5, C_15, C_45. Let K(a, b, -1) be the larger set defined without the last condition. Let B be the set of x in K with x = d mod 3 and x = k mod 5.

*Budgets.* Every pure class C_(3^t) with t >= 4 is disjoint from C_3, C_9, C_27, so it lies in one row of Rows(b). For h in Rows(b) let z_h be 27 times the total measure of the classes C_(3^t), t >= 4, in the row h. Then

    z_h >= 0,    sum_h z_h = Zbud := sum_{t=4..e_3} 3^(3-t) = (1 - 3^(3-e_3))/2     (1/2 for e_3 = inf, 0 for e_3 = 3).

Every pure class C_(5^t) with t >= 3 lies in one of the columns 1, 2, 3, 4. For a column h let t_h be 5 times the total measure of the classes C_(5^t), t >= 3, in the column h, and let eps be 5 times the total measure of those of them that lie in the 5-cylinder of C_75 (a class C_(5^t) with t >= 3 is contained in that cylinder or disjoint from it). Then

    t_h >= 0,    sum_h t_h = Tbud := sum_{t=3..e_5} 5^(1-t) = (1 - 5^(2-e_5))/20     (1/20 for e_5 = inf, 0 for e_5 = 2),     0 <= eps <= t_k.

Put D_h = [h = c]/5 + t_h for a column h: the fraction of the column h covered by the pure classes of 5 other than C_5 (C_25 covers one fifth of the column c).

The *budget sets* are the simplex ZZ of all z = (z_h) with z_h >= 0 and sum z_h = Zbud, and the set WW of all w = (t_1, ..., t_4, eps) with t_h >= 0, sum t_h = Tbud, 0 <= eps <= t_k. The true budgets of the family are written z*, w*. The *vertices* of ZZ are the 14 points Zbud e_h (h in Rows(b)). The *vertices* of WW are the five points

    (Tbud e_j, 0) for j = 1, 2, 3, 4,    and    (Tbud e_k, Tbud).

Every point of ZZ is a convex combination of the vertices of ZZ, and every point (t, eps) of WW is a convex combination of the vertices of WW: with weights t_h/Tbud on (Tbud e_h, 0) for h != k, (t_k - eps)/Tbud on (Tbud e_k, 0) and eps/Tbud on (Tbud e_k, Tbud). (If Zbud = 0 or Tbud = 0 the set is a point and all its vertices coincide.)

*Levels.* The set U3 of 3-levels is {0} if e_3 = 3, {0, 1, ..., e_3 - 3} if 3 < e_3 < inf, and {0, 1, 2, ...} if e_3 = inf. The set U5 of 5-levels is {0, 1, ..., e_5 - 1} if e_5 is finite and {0, 1, 2, ...} otherwise. The *level masses* are

    p3(0) = 1,   p3(u) = 2/3^(u+1) for u >= 1, except p3(u) = 3^(-u) for u = e_3 - 3 (finite e_3);
    p5(0) = 1,   p5(v) = 4/5^(v+1) for v >= 1, except p5(v) = 5^(-v) for v = e_5 - 1 (finite e_5).

So the sum of p3(u) over u >= 1 is 1/3 (0 if e_3 = 3), and the sum of p5(v) over v >= 1 is 1/5. A *level* is a pair (u, v) in U3 x U5; its mass is p(u, v) = p3(u) p5(v).

*Cell weights.* For z in ZZ, w = (t, eps) in WW, a cell x in K and a level (u, v):

    alpha_x(0) = theta3 - z_(x mod 27)   with theta3 = 2/3 (theta3 = 1 if e_3 = 3),     alpha_x(u) = 1 for u >= 1;
    gamma_x(0) = 4/5 - D_(x mod 5) - (1/5 - eps)[x in B],                                   gamma_x(v) = 1 for v >= 1;
    a_x(u, v) = alpha_x(u) gamma_x(v).

These are non-negative on ZZ x WW (z_h <= 1/2; D_h <= 1/5 + 1/20). For fixed w they are affine functions of z, and for fixed z they are affine functions of w.

### 5.5 The anchor measure and the reserve

Let A be the set of points of Y_0 that lie in no pure class of the primes 3 and 5 and in no mixed class of F' of modulus 3^i 5^j. Let nu_0 be 135 H restricted to A (so nu_0 is measured in cells). Let A+ be the set of points y of Y_0 such that: y lies in a cell x of K; the 3-coordinate of y lies in no class C_(3^t), t >= 4; the 5-coordinate of y lies in no class C_(5^t), t >= 2; and y is not in C_75. Let nu_0^+ be 135 H restricted to A+.

**Lemma 5.2 (anchor measure and reserve) [S, Section 5].**
(i) A is contained in A+, so nu_0 <= nu_0^+; and nu_0 vanishes on the anchor part of every class of F' of stage 0.
(ii) For x in K, the part of A+ in the cell x is a product E_x x F_x, where E_x is a subset of the row of x of relative measure 1 - z_(x mod 27) (the row minus the deeper pure classes of 3) and F_x is a subset of the column of x of relative measure 1 - D_(x mod 5) - (1/5 - eps)[x in B].
(iii) nu_0(Y_0) >= Rfine(z*, w*), where for z in ZZ and w = (t, eps) in WW

    Rfine(z, w) = R0 + g15 + (9 - g15) D_a + g45 + (3 - g45) D_(r mod 5) + 9/5 - sum_{x in B} (1 - z_(x mod 27)) (1/5 - eps),
    R0 = 135 (1 - rho_3 - rho_5),
    g15 = 3 [a = 1] + [b = a mod 3] + sum of z_h over the h in Rows(b) with h = a mod 3,
    g45 = [b = r mod 9] + sum of z_h over the h in Rows(b) with h = r mod 9.

*Proof.* (i) A point of A is outside C_3, C_9, C_27, C_5, C_15 and C_45, so its cell is in K; it is outside the other pure classes and outside C_75. (ii) In the cell x the conditions defining A+ are a condition on the 3-coordinate (not in a class C_(3^t), t >= 4: these remove the fraction z_(x mod 27) of the row) and a condition on the 5-coordinate. The latter removes from the column the pure classes of 5 other than C_5 (fraction D_(x mod 5)) and, if x is in B, the 5-cylinder of C_75, which is one fifth of the column k and of which the fraction eps is already removed by pure classes. (C_75 meets the cell x only if x = d mod 3 and x = k mod 5, and then its part in the cell is the row times that 5-cylinder; C_25 is disjoint from C_75.)

(iii) Let S be the set of points of Y_0 in no pure class; H(S) = (1 - rho_3)(1 - rho_5). The mixed classes of F' of modulus 3^i 5^j have distinct moduli, and the sum of 3^(-i) 5^(-j) over all i, j >= 1 within the caps is rho_3 rho_5. A is S minus the union of these classes, hence

    H(A) >= H(S) - H(S n C_15) - H(S n C_45) - H((S n C_75) minus (C_15 u C_45)) - (rho_3 rho_5 - 1/15 - 1/45 - 1/75).

Since (1 - rho_3)(1 - rho_5) - rho_3 rho_5 = 1 - rho_3 - rho_5, this gives, in cells,

    nu_0(Y_0) >= R0 + [9 - 135 H(S n C_15)] + [3 - 135 H(S n C_45)] + [9/5 - 135 H((S n C_75) minus (C_15 u C_45))].

C_15 is the product of the cylinder "first digit a" at 3 and the column a. The pure classes of 3 inside that cylinder are: C_9 if a = 1 (one third of the cylinder), C_27 if b = a mod 3 (one ninth), and the classes C_(3^t), t >= 4, in the rows h = a mod 3 (each row is one ninth of the cylinder, and the fraction z_h of it is removed). So the fraction g15/9 of the cylinder is removed, the fraction D_a of the column is removed, 135 H(S n C_15) = (9 - g15)(1 - D_a), and the first bracket is g15 + (9 - g15) D_a. In the same way C_45 is the node r mod 9 times the column r mod 5; the pure classes inside the node are C_27 if b = r mod 9 (one third of it) and the deeper classes in the rows h = r mod 9 (each row is one third of the node); so 135 H(S n C_45) = (3 - g45)(1 - D_(r mod 5)). Finally a point of S outside C_15 and C_45 lies in a cell of K; if it lies in C_75, the cell is in B, and the part of S n C_75 in a cell x of B has mass (1 - z_(x mod 27))(1/5 - eps) by (ii). QED

*Properties of Rfine used later.* (R1) For fixed w it is affine in z, and for fixed z it is affine in w. (R2) Each of the three credits g15 + (9 - g15) D_a, g45 + (3 - g45) D_(r mod 5), 9/5 - sum_{x in B}(1 - z_x)(1/5 - eps), regarded as a function of numbers z_h >= 0, is non-decreasing in every z_h (because D_h <= 1 and eps <= 1/5), and the last two are >= 0 for z in ZZ and for z = 0 (then g45 <= 3/2 and 0 <= z_h <= 1, and B has at most nine cells). (R3) If b = 2, the last credit is at least 1/5 for z in ZZ and for z = 0: if d = 1, the cells of B have rows h = 1 mod 3 with h != 1 mod 9, at most six rows; if d = 2, their rows are = 2 mod 3 and different from b = 2, at most eight rows; so the sum is at most 8/5. (This is the credit of [S, Lemma 5.1].)

### 5.6 The anchor comparison

For a finite set K of cells, numbers a_x >= 0 and b_x (x in K), a number sigma and c = (c_g) with c_g >= 0 for g in G, define the *geometric maximum*

    Gmax(K, a, b; sigma, c) = max over (r_g), r_g a residue modulo g for each g in G, of   sum_{x in K} a_x (sigma + b_x + sum_{g in G} c_g [x = r_g mod g])_+ .

(Residues r_g that no cell of K meets contribute nothing, so the maximum may be taken over the residues met by K.) Its properties:

- (G1) It is non-decreasing in K (add cells with any weights >= 0), in each a_x, b_x, sigma and c_g. It is convex in the vector a (a maximum of linear functions of a with coefficients >= 0), and Gmax(K, lambda a, ...) = lambda Gmax(K, a, ...) for lambda >= 0. Hence if 0 <= phi_x <= lambda for all x, then Gmax(K, phi a, b; sigma, c) <= lambda Gmax(K, a, b; sigma, c).
- (G2) (*release*) If g0 is in G, rho is a residue modulo g0 and 0 <= omega <= c_g0, then Gmax(K, a, b + omega [. = rho mod g0]; sigma, c - omega e_g0) <= Gmax(K, a, b; sigma, c). (Lemma 3.5 with the two weights omega at rho and c_g0 - omega at r_g0, for each choice of the other residues, with f(s) = (sigma + s)_+.)
- (G3) Gmax(K, a, b; sigma, c) <= sum_x a_x (sigma + b_x)_+ + sum_g c_g h_g(a), where h_g(a) is the largest value of sum of a_x over the x in K with x = r mod g, over the residues r modulo g. If sigma + b_x >= 0 for all x, then Gmax(K, a, b; sigma, c) = sum_x a_x (sigma + b_x) + sum_g c_g h_g(a) exactly (all arguments are >= 0, the sum is linear, and the maximum is taken separately for each g).
- (G4) Gmax(K, a, 0; m sigma, m c) = m Gmax(K, a, 0; sigma, c) for m > 0.

**Lemma 5.3 (anchor comparison) [S, Section 5 and Lemma 4.3].** Let f be a non-decreasing convex function from the real line to [0, inf). Let phi_x >= 0 and b_x >= 0 be given for x in K, and a finite set of labels t, each with a weight c_t >= 0 and an *anchor class* R_t, a class of Y_0 of modulus 3^(i_t) 5^(j_t) > 1. The *category* of t is g(t) = 3^min(i_t, 3) 5^min(j_t, 1), an element of G, and r_t is the residue modulo g(t) of the class of modulus g(t) that contains R_t. For a level (u, v) let c_g(u, v) >= 0 be numbers such that, for every g in G, the labels t of category g with i_t <= 3 + u and j_t <= 1 + v have total weight at most c_g(u, v). Then, with the cell weights a_x(u, v) of Section 5.4 at the true budgets,

    sum_{x in K} phi_x * integral over the cell x of f(b_x + sum_t c_t 1[y in R_t]) nu_0^+(dy)
        <=  sum over the levels (u, v) of p(u, v) * max over (r_g) of sum_{x in K} phi_x a_x(u, v) f(b_x + sum_g c_g(u, v) [x = r_g mod g]).

For f(s) = (sigma + s)_+ the maximum on the right is Gmax(K, phi a(u, v), b; sigma, c(u, v)).

*Proof.* Fix x in K. By Lemma 5.2(ii), nu_0^+ on the cell x is the product of a measure on the row (27 H on E_x, total mass 1 - z_(x mod 27)) and a measure on the column (5 H on F_x, total mass 1 - D_(x mod 5) - (1/5 - eps)[x in B]). Write R_t = Q3_t x Q5_t. For y in the cell x, 1[y in R_t] = 1[y_3 in Q3_t] 1[y_5 in Q5_t]. If i_t <= 3, the first factor is constant on the row (1 if Q3_t contains the row, else 0). If i_t > 3 and Q3_t meets the row, then Q3_t is contained in the row and is a cylinder of depth i_t - 3 of the row, regarded as a copy of X(3, e_3 - 3); the row measure gives it at most 3^(-(i_t - 3)). The same holds at 5 with depth j_t - 1 inside the column, a copy of X(5, e_5 - 1), and bound 5^(-(j_t - 1)).

Integrate first over y_5, for fixed y_3: Lemma 3.4 with p = 5, C = 1 and S = 1 - D_(x mod 5) - (1/5 - eps)[x in B] >= 1/5 gives the bound sum over v in U5 of p5(v) gamma_x(v) f(b_x + sum of c_t 1[y_3 in Q3_t] over the labels with j_t <= 1 + v whose class of modulus 5^min(j_t, 1) contains the column). (Indeed pi(0) = S - 1/5 = gamma_x(0) and pi(v) = p5(v) for v >= 1.) For each v this is again of the same form as a function of y_3; integrate over y_3 with Lemma 3.4, p = 3, C = 1, S = 1 - z_(x mod 27) >= 1/3 (if e_3 = 3 the row is a single point and there is nothing to do). The result: the integral over the cell x is at most

    sum over (u, v) of p(u, v) a_x(u, v) f(b_x + sum of c_t over the labels t with i_t <= 3 + u, j_t <= 1 + v and x = r_t mod g(t)).

Multiply by phi_x, sum over x, and fix a level (u, v). The labels in the inner sum are grouped by category; in the category g they sit on residues r_t modulo g and have total weight at most c_g(u, v). Apply Lemma 3.5 to the seven categories one after the other, the other categories being part of the background b_x. This replaces each category by one residue r_g with the weight c_g(u, v) and can only increase the sum; the final value is at most the maximum over all (r_g). QED

---

## 6. The anchored method: the losses (DONE)

### 6.1 Parameters and kernels

The parameters are a rational C_7 and rationals tau_q for q = q_2, ..., q_s. Put, for every later prime q,

    tau_7 = n_7 (1 - 1/C_7),     beta_q = n_q - tau_q,     C_q = n_q/beta_q  (q >= 11),     omega_q = n_q/q.

**Side conditions (SC).** For every later prime q (including 7): 0 < tau_q < n_q and C_q <= q.

Then C_q > 1, delta_q := 1 - 1/C_q = tau_q/n_q, C_q/n_q = 1/beta_q, and 0 < omega_q <= 1 (because rho_q >= 1/q).

Apply Lemma 3.6 to F' with the anchor primes 3, 5, the later primes q_1 < ... < q_s, the measure nu_0 of Section 5.5, the sets P_i = P_(q_i), the caps C_i = C_(q_i), and the following sets B_i. For i >= 2, B_i(x) is the union of the q_i-cylinders of the mixed classes of F' of stage i that are *alive at x* (their projection to the prefix coordinates contains x). B_1 is defined in Lemma 6.2. Hypothesis (a) of Lemma 3.6 holds by Lemma 5.2(i). We bound the losses L_i^+ computed from the larger measure nu_0^+.

**Lemma 6.1 (load).** For i >= 2, q = q_i and every prefix x of length i,

    l_i(x) <= (1/beta_q) (1 + Z_q(x) - tau_q)_+ ,     Z_q(x) = n_q * sum of q^(-e(t)) over the mixed classes t of stage i alive at x,

where e(t) >= 1 is the exponent of q in the modulus of t.

*Proof.* H(P_i u B_i(x)) <= rho_q + sum q^(-e(t)) by the union bound, and l_i = C_q (H(P_i u B_i(x)) - delta_q)_+ by Lemma 3.2. Multiply out with C_q/n_q = 1/beta_q and n_q delta_q = tau_q. QED

**Lemma 6.2 (padding at the prime 7) [S, Lemma 6.1].** For a cell x in K let s(x) be the number of g in {3, 5, 9, 15} with x = xi_g mod g (0 <= s(x) <= 4). The set B_1(y) can be chosen so that for every y in a cell x of K:

(i) l_1(y) <= (1/beta_7) (omega_7 s(x) + Z'_7(y) - (tau_7 - 1))_+ , where Z'_7(y) = n_7 * sum of 7^(-e(t)) over the mixed classes t of stage 1, other than C_21, C_35, C_63, C_105, whose anchor part contains y;

(ii) m_1(y) <= S_(s(x)), where S_s = min(1, C_7 (6 - s)/7), and C_7/7 <= S_(s(x)) <= 1.

*Proof.* The classes C_21, C_35, C_63, C_105 are a class of Y_0 of modulus 3, 5, 9, 15 times a cylinder of depth 1 at 7 whose digit differs from the digit of C_7 (Lemma 5.1). For the cell x let T(x) be the set of the digits of those of the four whose anchor part contains the cell; it has at most s(x) elements. Choose a set T+(x) of exactly s(x) digits, containing T(x) and not containing the digit of C_7 (possible since s(x) <= 4 <= 6). For y in the cell x let B_1(y) be the union of the 7-cylinders of all mixed classes of stage 1 whose anchor part contains y and of the s(x) cylinders of depth 1 with digits in T+(x). (For y outside the cells of K take the first union only; such y have nu_0^+-measure 0.) This B_1 is admissible in Lemma 3.6. Those of the four classes that are alive at y have their 7-cylinders inside the padding, so the union bound gives H(P_7 u B_1(y)) <= rho_7 + s(x)/7 + Z'_7(y)/n_7, and (i) follows from Lemma 3.2 as in Lemma 6.1. For (ii): G_1(y) avoids the cylinder of C_7 and the s(x) padding cylinders, so H(G_1(y)) <= (6 - s(x))/7 and m_1(y) = min(C_7 H(G_1(y)), 1) <= S_(s(x)). Finally S_s >= C_7/7 because s <= 4 and C_7 <= 7. QED

Put kappa_s = S_s - C_7/7 for s = 0, ..., 4. Then 0 <= kappa_s <= 1 - C_7/7. (For C_7 = 3/2: kappa = 11/14, 11/14, 9/14, 6/14, 3/14.)

### 6.2 The stage 7

The *category counts* at a level (u, v) are

    w(u, v) = (1, 1, 1 + u, 1 + v, 1 + v, 1 + v, (1 + u)(1 + v))      for g = (3, 9, 27, 5, 15, 45, 135):

w_g(u, v) is the number of pairs (i, j) != (0, 0) with 3^min(i,3) 5^min(j,1) = g, i <= 3 + u, j <= 1 + v. Put

    wrem(u, v) = w(u, v) - omega_7 (1, 1, 0, 1, 1, 0, 0).

**Proposition 6.3 (stage 7).**

    L_1^+ <= Fine_7 := (1/beta_7) * sum over the levels (u, v) of p(u, v) Gmax(K, a(u, v), omega_7 s; 1 - tau_7, wrem(u, v)),

where a(u, v) are the cell weights at the true budgets and s = (s(x)).

*Proof.* By Lemma 6.2(i), L_1^+ is at most 1/beta_7 times the integral against nu_0^+ of f(omega_7 s(x) + Z'_7(y)) with f(s') = (s' + 1 - tau_7)_+. Apply Lemma 5.3 with phi_x = 1, b_x = omega_7 s(x), the labels t = the mixed classes of stage 1 other than the four padded ones, c_t = n_7 7^(-e(t)) and R_t their anchor parts. The labels with a given pair (i_t, j_t) = (i, j) have distinct exponents e(t) in {1, ..., e_7}, so their total weight is at most n_7 rho_7 = 1; for the four pairs (1, 0), (0, 1), (2, 0), (1, 1), the label with exponent 1 is one of the four padded classes, which are not among the labels, so the total is at most 1 - omega_7. Hence the labels of category g with i_t <= 3 + u, j_t <= 1 + v have total weight at most wrem_g(u, v). QED

### 6.3 The later stages

For i >= 2 let J_2, ..., J_(i-1) be independent random variables, J_j with the law pi_j of Lemma 3.7 for the prime q_j, the cap e_(q_j), C = C_(q_j) and S = 1:

    Prob(J_j = 0) = 1 - C_(q_j)/q_j,   Prob(J_j = n) = C_(q_j)(q_j - 1)/q_j^(n+1)  (1 <= n < e_(q_j)),   Prob(J_j = e_(q_j)) = C_(q_j) q_j^(-e_(q_j))  (finite cap).

Let pi_7(n), n >= 1, be the same expressions for the prime 7 and C_7 (their sum is C_7/7). For q = q_i put M' = prod_{1 < j < i} (1 + J_j) (M' = 1 for i = 2) and define two measures on the positive integers, the *channels*:

    Pi0_q(m) = Prob(M' = m)          (total mass 1),
    Pi1_q(m) = sum over n >= 1 of pi_7(n) Prob((1 + n) M' = m)          (total mass C_7/7).

For q = q_2 these are: Pi0 is the unit mass at m = 1, and Pi1(m) = pi_7(m - 1) for m >= 2.

**Lemma 6.4 (later stages; one fixed class at the stage q_2) [S, Section 8; Proposition 7.1 for the class 165].** Let i >= 2 and q = q_i. Put fix = 1 if q = q_2 and fix = 0 otherwise, let eta in R15(a) be the residue of the anchor part of C_(15 q_2), and let e_15 = (0, 0, 0, 0, 1, 0, 0) be the unit vector of 15 in G. Then

    L_i^+ <= Fine_q := (1/beta_q) * sum over ch in {0, 1}, m >= 1 and levels (u, v) of
                 Pich_q(m) p(u, v) Gmax(K, phi^ch a(u, v), fix omega_q [. = eta mod 15]; m - tau_q, m w(u, v) - fix omega_q e_15),

where phi^0_x = kappa_(s(x)), phi^1_x = 1, and a(u, v) are the cell weights at the true budgets.

*Proof.* By Lemma 6.1, L_i^+ is at most 1/beta_q times the integral against nu_(i-1)^+ of f(1 + Z_q(x)), f(s') = (s' - tau_q)_+. Apply Lemma 3.7 with b = 1, the labels t = the mixed classes of F' of stage i (finitely many), c_t = n_q q^(-e(t)), R_t the anchor part of t (R_t = Y_0 if t has none), Q_(t,j) the cylinder of t in the coordinate q_j, and S_1(y') = S_(s(x)) for y' in a cell x of K (Lemma 6.2(ii)), S_1(y') = 1 for y' outside the cells of K (where nu_0^+ vanishes), S_j = 1 for 2 <= j < i (allowed since C_(q_j) <= q_j). This gives

    L_i^+ <= (1/beta_q) * integral of nu_0^+(dy') sum_J pi_(y')(J) f(1 + sum over the t with e_j(t) <= J_j for all j of c_t 1[y' in R_t]).      (*)

Fix J and put M_J = prod_{j<i}(1 + J_j). A label is determined by its exponent vector: its exponent e in {1, ..., e_q} at q, its depths (e_j) at the earlier later primes, and the exponents (i', j') of 3 and 5. For a fixed pair (i', j') the labels with e_j <= J_j for all j have distinct vectors (e, (e_j)), so their total weight is at most M_J * n_q * sum_e q^(-e) = M_J. Sort the labels with e_j(t) <= J_j for all j into three groups. (a) Those without anchor part ((i', j') = (0, 0)): the vector (e_j) = 0 does not occur (that would be a pure class), so their total weight is at most M_J - 1, and they are alive at every y'. (b) If q = q_2: the class C_(15 q_2). It has weight omega_q (its exponent at q is 1) and depth 0 at the prime 7, so it is present for every J, and its anchor part is the class eta mod 15. (c) The others; each has an anchor part, and for each pair (i', j') their total weight is at most M_J, and at most M_J - fix omega_q for the pair (1, 1) of the class in (b). Since f is non-decreasing, for y' in a cell x the integrand of (*) is at most

    f(M_J + fix omega_q [x = eta mod 15] + sum over the labels t in (c) of c_t 1[y' in R_t]).

By the product form of pi_(y')(J), the factor that depends on y' is pi_(1,y')(J_1), which equals kappa_(s(x)) if J_1 = 0 and pi_7(J_1) if J_1 >= 1, for y' in the cell x. Apply Lemma 5.3 with phi_x = this factor, b_x = M_J + fix omega_q [x = eta mod 15], the labels of (c), and c_g(u, v) = M_J w_g(u, v) - fix omega_q [g = 15] >= 0 (the pair (1, 1) belongs to the category 15). The result for the given J is the factor prod_{1<j<i} Prob(J_j = J_j) times

    sum over (u, v) of p(u, v) Gmax(K, phi a(u, v), fix omega_q [. = eta mod 15]; M_J - tau_q, M_J w(u, v) - fix omega_q e_15),

with phi = kappa_(s(.)) if J_1 = 0 and phi = pi_7(J_1) if J_1 >= 1. Summing over J, the terms with J_1 = 0 and M' = m give the channel 0 and the terms with J_1 = n >= 1 and (1 + n) M' = m give the channel 1 (by (G1), a constant factor of the weights may be taken out). QED

*Remark.* The sums defining Fine_7 and Fine_q have non-negative terms; they are finite, by the bounds of Section 8, but this is not needed: all statements hold in [0, inf].

---

## 7. The anchored method: the budgets (DONE)

**Theorem 7.1.** Under the assumptions of Section 5.1 and (SC), let the completed family F' be in normal form, with discrete data a, b, c, r, d, k, xi, eta. For z in ZZ and w in WW define

    Dfine(z, w) = Rfine(z, w) - Fine_7(z, w) - sum_{q = q_2..q_s} Fine_q(z, w),

where Fine_7 and Fine_q are the expressions of Proposition 6.3 and Lemma 6.4 with the cell weights a_x(u, v) computed from (z, w) instead of the true budgets. Then Dfine(z*, w*) <= 0 at the true budgets.

*Proof.* F' covers X(P, e). By Lemma 3.6(5), Lemma 5.2(iii), Proposition 6.3 and Lemma 6.4: Rfine(z*, w*) <= nu_0(Y_0) <= sum_i L_i^+ <= Fine_7 + sum_q Fine_q at the true budgets. QED

**Lemma 7.2 (vertices) [S, Lemma 9.1].** In the situation of Theorem 7.1, Dfine(z*, w*) is at least the least of the 14 x 5 numbers Dfine(v, w'), v a vertex of ZZ and w' a vertex of WW. Consequently Dfine(v, w') <= 0 for at least one pair of vertices.

*Proof.* Fix w. Each cell weight a_x(u, v) is an affine function of z with values >= 0 (Section 5.4), and Gmax is convex in the vector of cell weights (G1); the factors phi_x, the masses p(u, v) and Pich_q(m) are constants >= 0. So Fine_7 and each Fine_q are convex functions of z (sums of non-negative multiples of convex functions; the value +inf is allowed), while Rfine is affine in z (R1). Hence Dfine(., w) is concave, and with z* = sum_h lambda_h v_h (a convex combination of the vertices) we get Dfine(z*, w) >= sum_h lambda_h Dfine(v_h, w). The same argument for fixed z and variable w gives Dfine(v_h, w*) >= sum_j mu_j Dfine(v_h, w_j) for w* = sum_j mu_j w_j. Together, Dfine(z*, w*) >= sum_{h,j} lambda_h mu_j Dfine(v_h, w_j) >= min. The last sentence follows from Theorem 7.1. QED

So a cap vector is excluded as soon as one can show, for every possible discrete data, that Dfine > 0 at all 70 pairs of vertices. Section 8 organises this as a finite computation.

---

## 8. The anchored method: the inequalities of a certificate (DONE)

An *anchored certificate* for a cap vector (P, e) as in Section 5.1 consists of a *header* and a list of *rows*. This section defines two rational numbers R and S for every row, from the header and the row alone, and proves (Theorem 8.2) that the cap vector is excluded if R > S on every row and the list of rows is complete in a sense defined in Section 8.6.

### 8.1 Header

The header gives: the later primes q_1 = 7 < q_2 < ... < q_s (s >= 2); the caps e_3, e_5, e_(q_1), ..., e_(q_s); the rational C_7; the rationals tau_q for q = q_2, ..., q_s; two positive integers Ucut, Vcut (the *truncation*). From these, rho_p, n_p, tau_7, beta_q, C_q, omega_q are defined as in Sections 5.1 and 6.1, kappa_s as in Section 6.1, Zbud and Tbud, the levels and the level masses as in Section 5.4. Put Delta_7 = tau_7 - 1 - omega_7.

**The header is admissible for a list of rows** if
- (H1) e_3 >= 3 and e_5 >= 2;
- (H2) the side conditions (SC) of Section 6.1 hold: 0 < tau_q < n_q and C_q <= q for every later prime q;
- (H3) tau_7 >= 1, if a row of phase spatial, pure3 or fixed165 occurs;
- (H4) Delta_7 >= 0, that is tau_7 >= 1 + n_7/7, if a row of phase coarse occurs.

(For C_7 = 3/2, which all certificates of Section 9 use, tau_7 = n_7/3 >= 2 and Delta_7 = 4 n_7/21 - 1 > 0, since n_7 >= 6.)

### 8.2 Keys and their weights

A *key* is a tuple kk = (a, b, c, r, j, d, k, ie, z), possibly followed by xi = (x3, x5, x9, x15), possibly followed by eta, with

- a in {1, 2}, b in {2, 4}, c in {a, 3 - a};
- r = -1, or r in Rep(a, b, c) (Lemma 5.1);
- (d, k) = (0, 0), or d in {1, 2}, k in {1, 2, 3, 4}, (d, k) != (a, a);
- j in {1, 2, 3, 4}; ie in {0, 1}, and ie = 1 only if d != 0 and j = k;
- z = -1, or z in Rows(b);
- xi in Xi(a); eta in R15(a).

A key determines the following objects, by the formulas of Sections 5.4 and 5.5 with the *budgets of the key*: z_h = Zbud [h = z] (all z_h = 0 if z = -1); t = Tbud e_j; eps = ie Tbud.

- The core K(kk) = K(a, b, r) (K(a, b, -1) if r = -1) and the set B(kk) of the x in K(kk) with x = d mod 3, x = k mod 5 (empty if d = 0).
- The cell weights a_x(u, v) = alpha_x(u) gamma_x(v), x in K(kk), with D_h = [h = c]/5 + Tbud [h = j].
- The reserve

      R(kk) = R0 + g15 + (9 - g15) D_a + [r >= 0] (g45 + (3 - g45) D_(r mod 5)) + [d != 0] (9/5 - sum_{x in B(kk)} (1 - z_(x mod 27)) (1/5 - eps)),

  with g15 = 3[a = 1] + [b = a mod 3] + Zbud [z >= 0 and z = a mod 3] and g45 = [b = r mod 9] + Zbud [z >= 0 and z = r mod 9].
- If xi is given: s(x) = the number of g in {3, 5, 9, 15} with x = xi_g mod g, for x in K(kk).

### 8.3 Truncation and envelopes

A level (u, v) is *explicit* if (e_3 is finite or u < Ucut) and (e_5 is finite or v < Vcut); otherwise it is *omitted*. Omitted levels exist only if e_3 = inf or e_5 = inf. For cell weights a(u, v) on a core K write

    Mass(u, v) = sum_x a_x(u, v),      Lin_c(u, v) = sum_{g in G} c_g h_g(a(u, v))   for a vector c >= 0,

with h_g as in (G3). All sums over omitted levels below are sums of p(u, v) times an expression that depends on (u, v) only through the signs of u and v (the cell weights) and through the counts w(u, v), which are polynomials of degree at most one in u and in v; so they are evaluated in closed form from

    sum_{u >= U} p3(u) = 3^(-U),   sum_{u >= U} u p3(u) = 3^(-U)(U + 1/2),   sum_{v >= V} p5(v) = 5^(-V),   sum_{v >= V} v p5(v) = 5^(-V)(V + 1/4)     (infinite caps),

and the finite sums over the explicit levels.

A *system of cell weights* on K is a family aa = (a_x(u, v)) of numbers with 0 <= a_x(u, v) <= 1 (x in K, (u, v) a level). The weights of Section 5.4 at any budgets, the weights of a key, and their products with the numbers kappa_s are such systems. For such a system every sum over levels in this section is finite, because Mass(u, v) + Lin_w(u,v)(u, v) <= 8 |K| (1 + u)(1 + v) and the sum of p(u, v)(1 + u)(1 + v) over all levels is finite. Define the *ordinary envelope*:

    F_aa(T) = sum over explicit levels of p(u, v) Gmax(K, a(u, v), 0; 1 - T, w(u, v)) + sum over omitted levels of p(u, v) (Mass(u, v) + Lin_w(u,v)(u, v)),       for T > 0,
    W_aa = sum over all levels of p(u, v) (Mass(u, v) + Lin_w(u,v)(u, v)),
    M_aa = sum over all levels of p(u, v) Mass(u, v).

For a measure Pi on the positive integers with finite total mass |Pi| and finite mean mu(Pi) = sum_m m Pi(m), and tau > 0, put

    Ord(aa; Pi, tau) = sum_{m < tau} Pi(m) m F_aa(tau/m) + (mu(Pi) - sum_{m < tau} m Pi(m)) W_aa - tau (|Pi| - sum_{m < tau} Pi(m)) M_aa.

**Lemma 8.0.** For every system of cell weights aa on K (so that W_aa and M_aa are finite), every Pi and tau as above,

    sum_{m >= 1} Pi(m) * sum over all levels of p(u, v) Gmax(K, a(u, v), 0; m - tau, m w(u, v))  <=  Ord(aa; Pi, tau),

and Ord(aa; Pi, tau) is linear in Pi.

*Proof.* For m < tau, (G4) gives Gmax(K, a, 0; m - tau, m w) = m Gmax(K, a, 0; 1 - tau/m, w); on an omitted level this is at most m (Mass + Lin_w) by (G3), since (1 - tau/m)_+ <= 1. So the terms with m < tau add up to at most Pi(m) m F_aa(tau/m). For m >= tau the second part of (G3) gives Gmax(K, a, 0; m - tau, m w) = (m - tau) Mass + m Lin_w = m (Mass + Lin_w) - tau Mass on every level, and the sum over the levels and over m >= tau is (mu(Pi) - sum_{m<tau} m Pi(m)) W_aa - tau (|Pi| - sum_{m<tau} Pi(m)) M_aa. Linearity in Pi is visible. QED

### 8.4 Laws

Let J_7, J_(q_2), ..., J_(q_s) be independent, J_p with the law of Lemma 3.7 for the prime p, the cap e_p, C = C_p and S = 1 (as in Section 6.3; Prob(J_7 = 0) = 1 - C_7/7 and Prob(J_7 = n) = pi_7(n)). For a later prime q let Pi_q be the law of M_q = prod over the later primes p < q of (1 + J_p) (the unit mass at 1 for q = 7), and Pi0_q, Pi1_q the channels of Section 6.3. Then

    Pi_q = (1 - C_7/7) Pi0_q + Pi1_q        (q >= 11),

    mu(Pi_q) = prod_{7 <= p < q} (1 + C_p/n_p),     mu(Pi0_q) = prod_{11 <= p < q} (1 + C_p/n_p),     |Pi1_q| = C_7/7,     mu(Pi1_q) = (C_7/7 + C_7/n_7) mu(Pi0_q),

because E[J_p] = sum_{n >= 1} Prob(J_p >= n) = C_p rho_p and sum_{n>=1} (1 + n) pi_7(n) = C_7/7 + C_7 rho_7. Only the values Pi(m) with m < tau_q are needed besides the masses and the means, and they are finite sums of products of the explicit probabilities.

### 8.5 The numbers R and S of a row

A row has a *phase* and a key. For the key kk write aa for its system of cell weights and K for its core; if xi is given, write kappa aa for the system kappa_(s(x)) a_x(u, v). Define the following *stage expressions*.

- **Ordinary stage** (any later prime q):  OrdSt_q(kk) = (1/beta_q) Ord(aa; Pi_q, tau_q). For q = 7 and tau_7 > 1 this is (1/beta_7) F_aa(tau_7).

- **Coarse stage 7:**

      Coarse_7(kk, xi) = (1/beta_7) [ sum over explicit levels of p(u, v) Gmax(K, a(u, v), 0; -Delta_7, wrem(u, v)) + sum over omitted levels of p(u, v) Lin_wrem(u,v)(u, v) ]
                         + (C_7/7) sum_{x in K} col_x (s(x) - 1)_+ ,        col_x = sum over all levels of p(u, v) a_x(u, v).

- **Padded stage 7:**

      Pad_7(kk, xi) = (1/beta_7) [ sum over explicit levels of p(u, v) Gmax(K, a(u, v), omega_7 s; 1 - tau_7, wrem(u, v))
                                   + sum over omitted levels of p(u, v) (Lin_wrem(u,v)(u, v) + omega_7 sum_x a_x(u, v) s(x)) ].

- **First-hit stage** (q >= 11):  FH_q(kk, xi) = (1/beta_q) [ Ord(kappa aa; Pi0_q, tau_q) + Ord(aa; Pi1_q, tau_q) ].

- **Fixed stage** (only for q = q_2; write tau, beta, omega for tau_(q_2), beta_(q_2), omega_(q_2)). For ch in {0, 1} let aa^ch be kappa aa (ch = 0) or aa (ch = 1), and for an integer m >= 1 put

      Psi^ch_m(eta) = sum over explicit levels of p(u, v) Gmax(K, a^ch(u, v), omega [. = eta mod 15]; m - tau, m w(u, v) - omega e_15)
                      + m * sum over omitted levels of p(u, v) (Mass^ch(u, v) + Lin^ch_w(u,v)(u, v)).

  Let N be the set of the integers n >= 1 (n <= e_7) with 1 + n < tau. Then

      Fix(kk, xi, eta) = (1/beta) [ Psi^0_1(eta) + sum_{n in N} pi_7(n) Psi^1_(1+n)(eta)
                                    + (C_7/7 + C_7/n_7 - sum_{n in N} (1 + n) pi_7(n)) W_aa - tau (C_7/7 - sum_{n in N} pi_7(n)) M_aa ].

  The coefficients m w_g(u, v) - omega [g = 15] are >= 0 because m >= 1, w_g >= 1 and omega <= 1.

The phases, their keys, and the numbers R and S:

| phase | key | R | S |
|---|---|---|---|
| basic | (a, b, c, -1, j, 0, 0, 0, -1) | R(kk) | sum over all later primes q of OrdSt_q(kk) |
| basic75 | the same, only for b = 2 | R(kk) + 1/5 | the same |
| mixed | (a, b, c, r, j, d, k, ie, -1), r >= 0, d != 0 | R(kk) | sum over all later primes q of OrdSt_q(kk) |
| coarse | the key of a mixed row, and xi | R(kk) | Coarse_7(kk, xi) + sum_{q >= 11} OrdSt_q(kk) |
| spatial | the key of a mixed row, and xi | R(kk) | Pad_7(kk, xi) + sum_{q >= 11} FH_q(kk, xi) |
| pure3 | (a, b, c, r, j, d, k, ie, z) with r >= 0, d != 0, z in Rows(b), and xi | R(kk) | Pad_7(kk, xi) + sum_{q >= 11} FH_q(kk, xi) |
| fixed165 | the key of a pure3 row, and eta | R(kk) | Pad_7(kk, xi) + Fix(kk, xi, eta) + sum_{q > q_2} FH_q(kk, xi) |

A row is *valid* if R > S for the numbers R and S recomputed by these formulas. (The name fixed165 refers to the case q_2 = 11, the only one that occurs in Section 9.)

### 8.6 Leaves, covering, completeness

A *leaf* is a tuple (a, b, c; r, d, k; xi; eta; h; j, ie) with a, b, c as above, r in Rep(a, b, c), d in {1, 2}, k in {1, ..., 4}, (d, k) != (a, a), xi in Xi(a), eta in R15(a), h in Rows(b), and (j, ie) one of (1, 0), (2, 0), (3, 0), (4, 0), (k, 1). A leaf stands for discrete data (a, b, c, r, d, k, xi, eta) of a family together with the vertex v_h = Zbud e_h of ZZ and the vertex of WW with t = Tbud e_j and eps = ie Tbud. A row *covers* the following leaves:

- a row of phase basic or basic75 with key (a, b, c, -1, j, 0, 0, 0, -1): all leaves with the same (a, b, c) and the same j;
- a row of phase mixed: all leaves with the same (a, b, c, r, d, k, j, ie);
- a row of phase coarse or spatial: all leaves with the same (a, b, c, r, d, k, j, ie) and the same xi;
- a row of phase pure3: all leaves with the same (a, b, c, r, d, k, j, ie), the same xi and h = z;
- a row of phase fixed165: the leaf with the same (a, b, c, r, d, k, j, ie), the same xi, h = z and the same eta.

A certificate is *complete* if every leaf is covered by at least one of its rows. This holds in particular if, for every (a, b, c): either the four rows of phase basic with j = 1, 2, 3, 4 are present, or (if b = 2) the four rows of phase basic75, or for every r in Rep(a, b, c), every (d, k) and every (j, ie): a mixed row is present, or for every xi in Xi(a): a coarse or a spatial row is present, or for every z in Rows(b): a pure3 row is present, or the seven fixed165 rows with eta in R15(a) are present.

### 8.7 The theorem

**Lemma 8.1 (a valid row settles the leaves it covers) [S, Lemma 9.2].** Let the header be admissible. Let a leaf (a, b, c; r, d, k; xi; eta; h; j, ie) be covered by a valid row. Then the function Dfine of Theorem 7.1, formed with the discrete data (a, b, c, r, d, k, xi, eta), satisfies Dfine(v, w) > 0 at the vertex v = Zbud e_h of ZZ and the vertex w = (Tbud e_j, ie Tbud) of WW.

*Proof.* Write K, aa for the core K(a, b, r) and the cell weights of the leaf, that is, the weights of Section 5.4 at the budgets (v, w), and K', aa' for the core and the weights of the key kk of the row. Write Rrow, Srow for the numbers R and S of the row.

*Step 1: K is contained in K' and a_x(u, v) <= a'_x(u, v) for all x in K and all levels.* For the phases pure3 and fixed165 the two are equal. For mixed, coarse, spatial the only difference is that the key has all z_h = 0, which makes alpha_x(0) larger. For basic and basic75, in addition K' = K(a, b, -1) contains K(a, b, r) and the key has no set B, which makes gamma_x(0) larger; the budget t = Tbud e_j is the same.

*Step 2: Rrow <= Rfine(v, w).* By (R2), Rfine(v, w) >= Rfine(0, w), the same expression with all z_h = 0, which is R(kk) for the phases mixed, coarse, spatial; for pure3 and fixed165, R(kk) = Rfine(v, w). For basic: R(kk) = R0 + g15 + (9 - g15) D_a at z = 0, and Rfine(v, w) is this plus two credits that are >= 0 by (R2), with a 15-credit that is not smaller at v than at 0. For basic75 (b = 2): the 75-credit is at least 1/5 by (R3).

*Step 3: Fine_7(v, w) <= the stage-7 term of Srow.* By (G1), Fine_7(v, w) <= Fine_7' := (1/beta_7) sum over all levels of p(u, v) Gmax(K', a'(u, v), omega_7 s; 1 - tau_7, wrem(u, v)) (for the basic phases, where xi is not part of the key, s is the function of the leaf, extended to K' by the same formula).
(a) Phases spatial, pure3, fixed165: on an omitted level (G3) gives Gmax <= sum_x a'_x (omega_7 s(x) + 1 - tau_7)_+ + Lin_wrem <= omega_7 sum_x a'_x s(x) + Lin_wrem, because tau_7 >= 1 (H3). So Fine_7' <= Pad_7(kk, xi).
(b) Phase coarse: for real numbers Rr >= 0 and an integer s >= 0, (Rr + omega_7 s - (tau_7 - 1))_+ <= (Rr - Delta_7)_+ + omega_7 (s - 1)_+ (for s = 0 because tau_7 - 1 >= Delta_7; for s >= 1 because the left argument is (Rr - Delta_7) + omega_7 (s - 1) and (A + B)_+ <= A_+ + B for B >= 0). Apply this for each choice of the residues (r_g) with Rr = sum_g wrem_g [x = r_g mod g] and take the maximum: Gmax(K', a', omega_7 s; 1 - tau_7, wrem) <= Gmax(K', a', 0; -Delta_7, wrem) + omega_7 sum_x a'_x (s(x) - 1)_+ on every level. On an omitted level Gmax(K', a', 0; -Delta_7, wrem) <= Lin_wrem by (G3) and Delta_7 >= 0 (H4). Summing over the levels, and using omega_7/beta_7 = C_7/7, Fine_7' <= Coarse_7(kk, xi).
(c) Phases basic, basic75, mixed: by (G2), applied to g0 = 3, 5, 9, 15 with omega = omega_7 and the residues xi_g (allowed because omega_7 <= 1 <= w_g(u, v)), Gmax(K', a', omega_7 s; 1 - tau_7, wrem) <= Gmax(K', a', 0; 1 - tau_7, w). By Lemma 8.0 with Pi the unit mass at 1 and tau = tau_7, Fine_7' <= (1/beta_7) Ord(aa'; Pi_7, tau_7) = OrdSt_7(kk).

*Step 4: for q >= 11, Fine_q(v, w) <= the stage-q term of Srow.* By (G1), Fine_q(v, w) is at most the same expression with (K', aa') in place of (K, aa); call its terms

    Term(ch, m, u, v) = Pich_q(m) p(u, v) Gmax(K', phi^ch a'(u, v), fix omega_q [. = eta mod 15]; m - tau_q, m w(u, v) - fix omega_q e_15).

For q > q_2 there is no fixed class (fix = 0). For q = q_2, by (G2) a term can only increase when the fixed class is *released*, that is, when the offset omega_q [x = eta mod 15] is removed and omega_q is added back to the coefficient of 15; a released term is the term with fix = 0.
(a) Phase fixed165 and q = q_2. Here Pi0 is the unit mass at m = 1 and Pi1(m) = pi_7(m - 1). For the term with ch = 0 and m = 1, and the terms with ch = 1 and m = 1 + n, n in N: keep them on the explicit levels; on the omitted levels release and use (G3) with (m - tau)_+ <= m. Their sum over the levels is at most Psi^0_1(eta), respectively pi_7(n) Psi^1_(1+n)(eta). For the terms with ch = 1 and m = 1 + n >= tau: release; by the second part of (G3) each equals pi_7(n) p(u, v) ((m - tau) Mass + m Lin_w), and their sum over the levels and over these n is the last line of the definition of Fix (the mass of Pi1 is C_7/7 and its mean is C_7/7 + C_7/n_7). Hence Fine_(q_2)(v, w) <= Fix(kk, xi, eta).
(b) Phases spatial and pure3 with any q >= 11, and phase fixed165 with q > q_2: release (if q = q_2); by Lemma 8.0 applied to the weights kappa aa' with Pi0_q and to aa' with Pi1_q, the sum of the terms is at most FH_q(kk, xi).
(c) Phases basic, basic75, mixed, coarse: release (if q = q_2). In the channel 0 the weights are kappa_(s(x)) a'_x with kappa_(s(x)) <= 1 - C_7/7, so by (G1) the channel-0 terms are at most (1 - C_7/7) Pi0_q(m) p(u, v) Gmax(K', a'(u, v), 0; m - tau_q, m w(u, v)). Since (1 - C_7/7) Pi0_q + Pi1_q = Pi_q, the sum of all terms is at most sum_m Pi_q(m) sum over levels of p(u, v) Gmax(K', a'(u, v), 0; m - tau_q, m w(u, v)) <= Ord(aa'; Pi_q, tau_q) by Lemma 8.0. So Fine_q(v, w) <= OrdSt_q(kk).

*Conclusion.* Dfine(v, w) = Rfine(v, w) - Fine_7(v, w) - sum_q Fine_q(v, w) >= Rrow - Srow > 0. QED

**Theorem 8.2 (anchored bound).** Let (P, e) be a cap vector as in Section 5.1. If there is an anchored certificate for (P, e) with an admissible header, all of whose rows are valid, and which is complete, then (P, e) is excluded.

*Proof.* Suppose not. Sections 5.1 to 5.3 give a completed covering family F' in normal form with discrete data a, b, c, r, d, k, xi, eta; here r is in Rep(a, b, c), (d, k) is one of the seven admissible pairs, xi is in Xi(a) and eta in R15(a). By Lemma 7.2 there are a vertex v = Zbud e_h of ZZ and a vertex w of WW with Dfine(v, w) <= 0; the vertex w is (Tbud e_j, ie Tbud) with (j, ie) one of (1, 0), ..., (4, 0), (k, 1). The leaf (a, b, c; r, d, k; xi; eta; h; j, ie) is covered by a valid row, because the certificate is complete; so Dfine(v, w) > 0 by Lemma 8.1. Contradiction. QED

*Remarks.* (1) The proof uses the stored numbers of a certificate nowhere: only the keys and phases of its rows, and the header. (2) The stopping rule with which a certificate was generated plays no role. (3) If Tbud = 0 (cap 2 at the prime 5) the rows that differ only in (j, ie) have the same R and S; if Zbud = 0 (cap 3 at the prime 3) the same holds for rows that differ only in z. (4) [S] proves Theorem 8.2 for the cap vector of Theorem A (s = 6, all caps infinite). The changes for finite caps are the level sets and masses of Section 5.4, the numbers n_p, and the last atoms of the laws.

---

## 9. The certificates and the proof of Theorem 1 (DONE)

The certificate files are plain text. Their formats are described in the package (file `FORMAT.md`); the dictionary to the notation of this document is in Section 9.5.

### 9.1 Eight primes: Theorem A

**Certificate A8** (files `certs/thmA_8p.part01.tsv` to `certs/thmA_8p.part06.tsv`, to be read as one list of rows): an anchored certificate for the cap vector (inf, inf, inf, inf, inf, inf, inf, inf) on (3, 5, 7, 11, 13, 17, 19, 23), with header C_7 = 3/2, (tau_11, tau_13, tau_17, tau_19, tau_23) = (4, 4, 8, 8, 12), Ucut = 10, Vcut = 7. (So tau_7 = 2; these are the thresholds of [S].) It has 28,057 rows: 16 basic, 4 basic75, 604 mixed, 25,840 coarse, 1,003 spatial, 506 pure3, 84 fixed165.

**Theorem A (Schroeder [S, Theorem 1.1]).** If certificate A8 has an admissible header, is complete, and all its rows are valid, then the cap vector (inf^8) on the first eight odd primes is excluded, and consequently every odd covering has omega(L) >= 9.

*Proof.* The first statement is Theorem 8.2. If an odd covering had r = omega(L) <= 8, Corollary 2.2 would give a non-excluded cap vector on the first r odd primes, which is dominated by (inf^8); this contradicts Lemma 1.2. QED

### 9.2 Nine primes

**Certificates F9_01 to F9_23** (file `certs/nine_finite.tsv`): 23 anchored certificates on (3, 5, 7, 11, 13, 17, 19, 23, 29), each with header C_7 = 3/2, (tau_11, ..., tau_29) = (4, 4, 6, 8, 12, 16), Vcut = 7 and Ucut = 9 (Ucut = 10 for F9_15), and each consisting of 32 rows of phase basic (all (a, b, c) and all j). Their cap vectors (caps at 3, 5, 7, 11, 13, 17, 19, 23, 29):

| id | caps | id | caps |
|---|---|---|---|
| F9_01 | (3, inf, inf, inf, inf, inf, inf, inf, inf) | F9_13 | (8, 2, inf, 2, 3, 1, 1, 2, 1) |
| F9_02 | (inf, inf, 1, inf, inf, inf, inf, inf, inf) | F9_14 | (4, inf, 3, 2, 1, 1, 1, 1, 2) |
| F9_03 | (10, 2, 2, 3, 4, 1, 1, 3, 2) | F9_15 | (12, 2, inf, 4, 1, 1, 2, 3, 3) |
| F9_04 | (6, 4, 2, 2, 1, 1, 1, 1, 1) | F9_16 | (7, 2, 3, 1, 2, 2, 1, 2, 1) |
| F9_05 | (4, 3, 2, 2, 3, 1, 1, 2, 2) | F9_17 | (5, 3, 3, 1, 2, 1, 4, 1, 2) |
| F9_06 | (4, 3, 3, 2, 2, 1, 1, 1, 1) | F9_18 | (7, inf, 2, 1, 2, 1, 1, 1, 1) |
| F9_07 | (5, 3, 3, 2, 1, 1, 1, 1, 1) | F9_19 | (4, 2, 2, 2, 2, 2, 3, 3, 2) |
| F9_08 | (9, 2, 2, 3, 3, 4, 1, 1, 2) | F9_20 | (6, 2, inf, 2, 1, 2, 2, 1, 2) |
| F9_09 | (4, 3, 2, 2, 2, 3, 1, 1, 1) | F9_21 | (4, 3, 2, 2, 1, 3, 3, 3, 1) |
| F9_10 | (7, 3, 2, 3, 1, 1, 1, 1, 1) | F9_22 | (7, 4, 3, 1, 1, 1, 3, 2, 2) |
| F9_11 | (4, 3, 2, 2, 3, 1, 3, 1, 2) | F9_23 | (9, inf, inf, 1, 1, 3, 1, 1, 2) |
| F9_12 | (7, 2, 2, 2, 3, 2, 2, 1, 1) | | |

By Theorem 8.2 each of these cap vectors is excluded if its certificate has an admissible header and 32 valid rows (32 basic rows with all (a, b, c) and all j form a complete certificate).

### 9.3 Ten to thirteen primes

**Certificates U001 to U738** (file `certs/scalar_lemma_u.tsv`): 738 rows, each giving a number r in {10, 11, 12, 13}, finite caps e_1, ..., e_r on the first r odd primes, a number k0 and rationals C_i (k0 < i <= r). By Proposition 4.1 the cap vector of a row is excluded if 1 <= k0 < r, 1 < C_i <= p_i and the number B computed from the row is less than 1. (603 rows have r = 10, 120 have r = 11, 14 have r = 12 and one has r = 13.)

**Certificates G01 to G13** (file `certs/global_anchored.tsv`): 13 anchored certificates, twelve on the first ten odd primes (3, ..., 31) with (tau_11, ..., tau_31) = (4, 4, 6, 8, 12, 16, 18) and one (G13) on the first eleven (3, ..., 37) with (tau_11, ..., tau_37) = (4, 4, 6, 8, 12, 16, 18, 22); all with C_7 = 3/2, Ucut = 8, Vcut = 6. Their cap vectors:

| id | caps | id | caps |
|---|---|---|---|
| G01 | (4, 4, 2, 1, 1, 1, 1, 1, 1, 1) | G08 | (4, 3, 2, 2, 1, 1, 1, 1, 1, 1) |
| G02 | (7, 2, 2, 1, 1, 1, 1, 1, 1, 1) | G09 | (5, 2, 2, 1, 1, 1, 2, 1, 1, 1) |
| G03 | (5, 2, 2, 2, 1, 1, 1, 1, 1, 1) | G10 | (6, 2, 3, 1, 1, 1, 1, 1, 1, 1) |
| G04 | (4, 3, 3, 1, 1, 1, 1, 1, 1, 1) | G11 | (4, 3, 2, 1, 2, 1, 1, 1, 1, 1) |
| G05 | (5, 2, 2, 1, 2, 1, 1, 1, 1, 1) | G12 | (5, 2, 2, 1, 1, 1, 1, 2, 1, 1) |
| G06 | (6, 3, 2, 1, 1, 1, 1, 1, 1, 1) | G13 | (4, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1) |
| G07 | (5, 2, 2, 1, 1, 2, 1, 1, 1, 1) | | |

Each consists of 32 basic rows, except G08, which has 28 basic rows and 280 mixed rows (one triple (a, b, c) is treated by its 280 mixed rows). There are 692 rows in all. By Theorem 8.2 each cap vector is excluded if its certificate has an admissible header, is complete and has valid rows.

### 9.4 What a checking program must verify

The proof of Theorem 1 rests on the following finite computations, all in exact rational arithmetic, and on nothing else that is not proved in this document.

- **(i) Scalar certificates.** For each of the 738 rows of `certs/scalar_lemma_u.tsv`: the primes are the first r odd primes; the caps are positive integers; 1 <= k0 < r; 1 < C_i <= p_i for k0 < i <= r; and the number B of Proposition 4.1, computed as in Section 4.2, satisfies B < 1.
- **(ii) Anchored certificates.** For each of the 37 anchored certificates (A8; F9_01, ..., F9_23; G01, ..., G13): the primes are the first 8, 9, 10 or 11 odd primes as stated; the header is admissible (Section 8.1); for every row the numbers R and S recomputed from the key by the formulas of Section 8.5 satisfy R > S; and the list of rows is complete (Section 8.6). The cap vector of A8 is (inf^8).
- **(iii) Enumeration.** For r = 9, ..., 13: every vector f of r positive integers with p_1^(f_1) ... p_r^(f_r) < X0 (there are 5,028, 1,484, 248, 21, 1 of them) is dominated by the cap vector of a certificate verified in (i) or (ii) on the first r odd primes; and p_1 p_2 ... p_14 > X0.

A program that also compares the recomputed R, S and B with numbers stored in the files, or checks hashes of the files, does more than the proof needs.

### 9.5 Dictionary between the files and this document

- Scalar file: columns `omega` = r; `primes`; `exps` = (e_1, ..., e_r); `k0`; `Cs` = (C_(k0+1), ..., C_r), the caps of the later primes in increasing order of the primes; `B_exact` = the value of B.
- Anchored files: header lines `primes` (3, 5, then the later primes q_1 = 7 < ... < q_s); `exps` (the caps, `inf` allowed); `C7` = C_7; `taus_later` = (tau_(q_2), ..., tau_(q_s)); `U_cut` = Ucut; `V_cut` = Vcut. Each row has a phase, a key, and two stored numbers `R_exact`, `S_exact`. The key lists (a, b, c, r, j, d, k, ie, z) for the phases basic, basic75, mixed; then (x3, x5, x9, x15) = xi for coarse, spatial, pure3; then eta for fixed165.

### 9.6 Proof of Theorem 1

Assume the computations (i), (ii), (iii) of Section 9.4. By (ii) and Theorem 8.2 the cap vector (inf^8) on the first eight odd primes is excluded: this is (E8) of Proposition 2.3. By (ii) and Theorem 8.2 the cap vectors of F9_01, ..., F9_23 and of G01, ..., G13 are excluded, and by (i) and Proposition 4.1 the cap vectors of U001, ..., U738 are excluded. By (iii), every vector of r positive integers with p_1^(f_1) ... p_r^(f_r) < X0, 9 <= r <= 13, is dominated by one of these excluded cap vectors on the first r odd primes: this is (E9-13). Proposition 2.3 gives Theorem 1. QED

### 9.7 Sizes of the margins (for orientation only; not used in the proof)

The least value of R - S over the rows is 0.0020037017 cells for A8 (on a mixed row), 0.0160669315 for the F9 certificates (F9_13) and 0.2381510142 for the G certificates (G06). The largest B among the scalar certificates is 0.9991409521.

---

## 10. What is not claimed (DONE)

1. **The existence of an odd covering remains open.** Theorem 1 is a lower bound for L in a hypothetical odd covering; it does not decide the question of Erdős and Selfridge.
2. **omega(L) >= 10 is not proved.** The document proves omega(L) >= 9 (Theorem A, due to Schroeder) and nothing more about the number of primes. The nine-prime certificates F9 are used only for the 5,028 exponent vectors with product below X0. They do not exclude every nine-prime exponent vector: the vector (5, 3, 2, 2, 2, 1, 1, 1, 1), whose product is X0, is dominated by none of the 23 cap vectors, and no claim is made about it.
3. **No structural statement about nine-prime coverings is claimed here** (which primes divide L, which powers divide L). Only the inequality of Theorem 1 is claimed.
4. **The bound is not claimed to be the limit of the method.** X0 is the least product of an exponent vector not dominated by the certificates of Section 9; other certificates might give more.
5. **The lemma chain is not formalised.** Sections 1 to 8 are a written proof; they have not been checked by a proof assistant. The finite computations are verified by recomputation with independent programs, not by a formally verified program.
6. **Nothing is claimed about the other results of [S]** (its formalisation, its corollary on the uncovered density). The present document uses [S] as the source of the method and proves what it uses.
7. **No claim of priority or of novelty is made in this document.** For orientation only: the bound of [S, Corollary 1.3] is L >= 9,704,539,845, and X0 is 675,675 = 3^3 * 5^2 * 7 * 11 * 13 times that number. Whoever uses Theorem 1 should compare it with the bounds known at the time; this document does not survey them.
8. **Exponent caps cannot give a proof of non-existence by themselves**, and none is suggested: from an odd covering one obtains odd coverings on the same primes with larger exponents (let n_0 be the largest modulus and replace its class a_0 mod n_0 by the classes a_0 + n_0 a_i mod n_0 n_i, one for every class a_i mod n_i of the covering, the class of n_0 included; the new moduli exceed all old ones and are pairwise distinct, and a point a_0 + n_0 y is covered by the new class of an i with y in a_i mod n_i).

---

## 11. Sources and credit (DONE)

**[S]** M. Schroeder, *Nine prime divisors in odd distinct covering systems*, author preprint, version 1.0.1, Zenodo, dated 13 September 2026, revised 15 September 2026, DOI 10.5281/zenodo.22759614. Its Theorem 1.1 is Theorem A above (omega(L) >= 9); its Corollary 1.3 is the bound L >= 9,704,539,845. The method of Sections 3 and 5 to 8 is the method of [S]. The correspondence is:

| here | in [S] |
|---|---|
| Lemma 2.1 (prime replacement) | Lemma 2.1 |
| Lemma 3.1 (completion) | Lemma 2.2 |
| Lemma 3.2, Lemma 3.6 (kernel, accounting) | Lemma 3.1, Lemma 3.2 |
| Lemmas 3.3, 3.4, 3.7 (convex comparison) | Lemmas 4.1, 4.2 and Section 4 |
| Lemma 3.5 (aggregation) | Lemma 4.3 |
| Lemmas 5.1, 5.2, 5.3 (normal form, reserve, anchor comparison) | Section 5 |
| property (R3) of the reserve (the phase basic75) | Lemma 5.1 |
| Lemma 6.2, Proposition 6.3 (padding at 7) | Section 6 (Lemma 6.1) |
| Lemma 6.4 (later stages, the class 165) | Section 7 (Proposition 7.1) and Section 8 |
| Lemma 7.2 (vertices) | Lemma 9.1 |
| Lemma 8.1 (every row dominates the fine bound) | Lemma 9.2 |
| Theorem 8.2 for the cap vector (inf^8), and Theorem A | Section 10 (Proposition 10.1) and Theorem 1.1 |

What is added here to [S]: the statements with exponent caps (finite level sets, the numbers n_p, the last atoms of the comparison laws); the scalar criterion in the form of Proposition 4.1; the reduction of Theorem 1 to exponent vectors (Propositions 2.3 and 2.4); and the certificates of Section 9. About the scalar criterion: [S] says that its author's two earlier preprints (*Seven prime divisors in odd distinct covering systems*, Zenodo DOI 10.5281/zenodo.22739035, and *Eight prime divisors in odd distinct covering systems*, Zenodo DOI 10.5281/zenodo.22747841; titles and identifiers as given in the reference list of [S]) use a scalar comparison. Those preprints were not consulted for this document; Proposition 4.1 is proved here from the lemmas of Section 3 and is presumably of that kind. The certificate A8 uses the thresholds of [S], and its numbers of rows per phase are those of [S, Table 3], except in the last phase, where all twelve residual vertices are treated directly (84 rows) instead of four representatives (28 rows); the certificate of [S] has 28,001 inequalities. The rows of A8 were computed independently of the certificate published with [S], with the conventions of Section 8 (which differ from those of [S] in the truncation and in some of the bounds used on the omitted levels and, for the fixed class, in the linear part).

**[SZ]** R. J. Simpson and D. Zeilberger, *Necessary conditions for distinct covering systems with square-free moduli*, Acta Arithmetica 59 (1991), 59-70, DOI 10.4064/aa-59-1-59-70. Cited in [S] (for its Theorem 1 and Corollary 1, pages 59 to 61) as the source of the prime replacement principle; the paper itself was not consulted, and the proof of Lemma 2.1 above is self-contained.

**Background (not used in the proof).** The problem goes back to P. Erdős, *On integers of the form 2^k + p and some related problems*, Summa Brasiliensis Mathematicae 2 (1950), 113-123. R. D. Hough and P. P. Nielsen, *Covering systems with restricted divisibility*, Duke Mathematical Journal 168 (2019), 3261-3295, proved that every covering system with distinct moduli has a modulus divisible by 2 or 3. P. Balister, B. Bollobás, R. Morris, J. Sahasrabudhe and M. Tiba, *The Erdős-Selfridge problem with square-free moduli*, Algebra and Number Theory 15 (2021), no. 3, 609-626, proved that a covering system with distinct square-free moduli has an even modulus; the kernels of Lemma 3.2 belong to the line of their distortion method (*On the Erdős covering problem: the density of the uncovered set*, arXiv:1811.03547; Inventiones Mathematicae 228 (2022), 377-414).

Other statements about L for an odd covering that we know of, besides [S]: I. Mian and S. Siddique, *Kernel-checked exclusions for the Erdős-Selfridge odd covering problem: any odd covering of Z has lcm exceeding 10000*, arXiv:2607.25628 (28 July 2026); X. Dai, H. Li, J. Li and S. Yi, *On the moduli of distinct covering systems*, arXiv:2611.15110 (11 November 2026), where, according to the abstract, L is shown to be divisible by 45 and the least modulus to be at most 9. This is not a survey.

*How the bibliographic data were obtained.* The statements about [S] were checked against the text of [S], version 1.0.1. The data of [SZ], of the Algebra and Number Theory paper and of the three arXiv items were checked on the publishers' and arXiv pages; the data of the papers of Erdős, of Hough and Nielsen and of the Inventiones paper are taken from the reference list of [S].
