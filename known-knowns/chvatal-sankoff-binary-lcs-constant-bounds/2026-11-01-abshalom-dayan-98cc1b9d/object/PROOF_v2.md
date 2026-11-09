# Proof, revised presentation: gamma_2 >= m/K from an adaptive-strip certificate

Written 2026-11-08. This file restates object/PROOF.md with a displayed theorem, notation in which no letter has two
meanings, and two steps written out in full. The mathematics is the same as in object/PROOF.md, which stays
unchanged because its sha256 names this package. Symbols that changed from object/PROOF.md:

| object/PROOF.md | here | meaning |
|---|---|---|
| b, b_p | w, w_p | the window of B (positions p = 0..N-1) |
| c(h, b) | kappa(h, w) | the complement map |
| m_p | mu_p | match indicator in the ROW update |
| x_p | z_p | new cell value in the increment form |
| m, n in Fekete's lemma | j, k | lengths in the superadditivity inequality |
| unnamed (the checkers' E) | D(s) | the left side of C3; E is kept for expectation |

Kept: m is only the certificate integer, x and y only the numbers of characters of A and B read, c only the
character read by SHIFT, and b_1, b_2, ... only the characters of B.

## 0. Setting and main statement

A = a_1 a_2 ... and B = b_1 b_2 ... are independent sequences of independent uniform bits. For x, y >= 0, L(x, y) is
the length of a longest common subsequence of A_x = a_1..a_x and B_y = b_1..b_y. By concatenation,
E L(j+k, j+k) >= E L(j, j) + E L(k, k), so by Fekete's lemma [Fe] gamma_2 = lim_n E L(n, n)/n = sup_n E L(n, n)/n
[CS]. N >= 1 is the window size.

A state is s = (h, w) with h = (h_0..h_{N-1}) and w = (w_0..w_{N-1}) in {0,1}^N. The complement map is
kappa(h, w) = (h, not w), where "not" flips every bit; canon(s) = s if w_{N-1} = 0 and kappa(s) otherwise. A state is
canonical if w_{N-1} = 0. Section 1 defines the two moves ROW and SHIFT. For a canonical state s, a move
q in {ROW, SHIFT} and a bit e, next_e(s, q) is canon of the state reached from s by q when the character read is
e; the reward of SHIFT at s is r(s) = h_0, and the reward of ROW is 0.

**Theorem 1.** Let K > 0 and m be integers, S a finite set of canonical states, pi: S -> {ROW, SHIFT} and
V: S -> Z, such that

- (C1) (0, w) is in S for every canonical w (here 0 is the all-zero h);
- (C2) for every s in S, next_0(s, pi(s)) and next_1(s, pi(s)) are in S;
- (C3) for every s in S, writing next_e = next_e(s, pi(s)),
  D(s) := 2 K r(s) + V(next_0) + V(next_1) - 2 V(s) >= m, with r(s) = 0 if pi(s) = ROW and r(s) = h_0 if
  pi(s) = SHIFT. (The checkers print the minimum of D over S as min_E or minE.)

Then gamma_2 >= m/K.

S may contain states the process never visits: the proof uses that S contains the start states (C1) and is closed
under pi (C2), not that every state of S is reached.

**Corollary.** The N = 17 certificate of object/CERTIFICATE.md (242,084,334 canonical states, K = 2^24 = 16777216,
m = 13332272) satisfies (C1), (C2) and (C3); each of the three checkers in verify-it-yourself/ tests all three
conditions on every state in exact integer arithmetic and accepts (verify-it-yourself/RECEIPTS.md). Hence

    gamma_2 >= 13332272/2^24 = 833267/1048576 = 0.794665336609...

## 1. The process

Besides the state (h, w), the process carries, for the proof only, counters x (characters of A read), y (characters
of B read), l = y - N, and integers F_0..F_N with F_{p+1} - F_p = h_p. The index conventions are:

| quantity | column of the DP table L(x, .) |
|---|---|
| F_p, p = 0..N | column l + p |
| w_p, p = 0..N-1 | w_p = b_{l+p+1}, the character of column l + p + 1 |

Start: x = 0, y = N, l = 0, F_0 = ... = F_N = 0 (so h = 0), and w = (b_1, ..., b_N). At each step a fixed policy
chooses one of two moves as a function of the state only (section 4 makes this precise):

ROW: read a = a_{x+1}. Put F'_0 = F_0 and, for p = 0..N-1,

    F'_{p+1} = max(F_{p+1}, F'_p, F_p + mu_p),   where mu_p = 1 if w_p = a and mu_p = 0 otherwise.

Then x increases by 1. Reward 0. The window w is unchanged.

SHIFT: read c = b_{y+1}. The new frontier is (F_1, ..., F_N, F_N), that is F'_p = F_{p+1} for p < N and F'_N = F_N.
The new window is w' = (w_1, ..., w_{N-1}, c): window position p of w' holds old position p + 1 for p <= N - 2, and
position N - 1 holds c. Then y and l increase by 1. Reward r = h_0 = F_1 - F_0.

Each step leaves F_0 unchanged (ROW) or replaces it by F_1 = F_0 + r (SHIFT), so the sum of the rewards up to time t
is R_t = F_0(t) - F_0(0) = F_0(t).

## 2. The update stays in increment form

**Lemma A.** In ROW, put v_p = F'_p - F_p and z_p = max(h_p, v_p, mu_p). Then for p = 0..N-1, v_p and h_p lie in
{0, 1}, F'_{p+1} = F_p + z_p, the new increment is h'_p = F'_{p+1} - F'_p = z_p - v_p, and
v_{p+1} = z_p - h_p, all in {0, 1}.

Proof. v_0 = 0. If v_p and h_p are in {0, 1}, the three terms of the max are F_p + h_p, F_p + v_p and F_p + mu_p, so
F'_{p+1} = F_p + z_p with z_p in {0, 1}. Since z_p >= v_p and z_p <= 1, h'_p is in {0, 1}; since z_p >= h_p,
v_{p+1} is in {0, 1}. Induction on p. SHIFT keeps the increment form trivially (the new last increment is 0). So the
next state (h', w') is a function of (h, w) and the character read only. []

## 3. Every frontier value is a lower bound on an LCS length

**Lemma B.** At every time and for each p = 0..N, F_p <= L(x, l + p).

Proof. At the start all F_p are 0. ROW, by induction on p: F'_0 = F_0 <= L(x, l) <= L(x+1, l). For p >= 0, each term
of the max defining F'_{p+1} is at most L(x+1, l+p+1): F_{p+1} <= L(x, l+p+1) <= L(x+1, l+p+1);
F'_p <= L(x+1, l+p) <= L(x+1, l+p+1); and if mu_p = 1, then a_{x+1} = w_p = b_{l+p+1}, so a common subsequence of A_x
and B_{l+p} extends by this pair and F_p + 1 <= L(x, l+p) + 1 <= L(x+1, l+p+1). SHIFT, with l' = l + 1: for p < N
the new value is the old F_{p+1} <= L(x, l+p+1) = L(x, l'+p); for p = N it is the old F_N <= L(x, l+N) <=
L(x, l'+N). []

Hence R_t = F_0(t) <= L(x_t, l_t) <= L(x_t, y_t) for every outcome and every t.

## 4. Symmetry, the policy on all states, and the uniform next character

Complement symmetry. Write Row(h, w, a) for the new h after ROW reads a. Since mu_p depends only on whether w_p = a,
Row(h, not w, not a) = Row(h, w, a). For SHIFT, Shift(kappa(s), not c) = kappa(Shift(s, c)), with the same reward
h_0. Extend pi and V from S to all states by pi(s) = pi(canon(s)) and V(s) = V(canon(s)). Then, for any state s
with canon(s) in S, the two states canon(successor of s for character 0) and canon(successor of s for character 1)
are next_0(canon(s), pi(s)) and next_1(canon(s), pi(s)), possibly in the other order, and the reward is r(canon(s)).
So D(canon(s)) computed in (C3) is also the two-successor sum at s.

Uniform next character. Let G_t be the sigma-field generated by b_1..b_N and the characters read in steps 1..t.
Since pi is deterministic, each atom of G_t is a cylinder event {a_1..a_{x_t} = alpha, b_1..b_{y_t} = beta} on
which the counts x_t and y_t are constant: this holds at t = 0, and on an atom of G_t the state s_t is fixed, so the move
pi(s_t) and the index of the next character are fixed, and splitting the atom by the value of that character gives
atoms of G_{t+1} of the same form. The next character, a_{x_t+1} or b_{y_t+1}, is not among the characters fixed by the
atom, so it is independent of that event and uniform given G_t. The state s_{t+1} is a function of s_t and that
character (Lemma A).

## 5. Telescoping

The state stays in S. canon(s_0) = (0, canon(b_1..b_N)) is in S by (C1). If canon(s_t) is in S, then
canon(s_{t+1}) is next_0 or next_1 of canon(s_t) under pi (section 4), which is in S by (C2). By induction on t,
canon(s_t) is in S for every t, so (C3) applies at every step.

Drift. By section 4, on each atom of G_t,

    E[K r_{t+1} + V(s_{t+1}) | G_t] - V(s_t) = D(canon(s_t))/2 >= m/2.

Summing over t = 0..T-1 and taking expectations (T is fixed and V is bounded, so no stopping argument is needed):
K E[R_T] + E V(s_T) - E V(s_0) >= T m/2. S is finite, so |V| <= V_max on S, and

    E[R_T] >= T m/(2K) - 2 V_max/K.

## 6. From reward per character to gamma_2

Each step reads one character and y_0 = N, so x_T + y_T = N + T =: n. The policy may read the two strings at
different rates, so a conversion is needed.

**Lemma 1.** For fixed x + y = n, E L(x, y) <= n gamma_2/2.

Proof. Let A', B' be independent copies of A, B. Concatenation gives L(A_x A'_y, B_y B'_x) >= L(A_x, B_y) +
L(A'_y, B'_x). The two concatenated strings are independent uniform strings of length n, so E L(n, n) >=
E L(x, y) + E L(y, x) = 2 E L(x, y), by exchanging the roles of A and B. And E L(n, n) <= n gamma_2, since gamma_2
is the supremum. []

Why Lemma 2 is needed. The split (x_T, y_T) is random and depends on the strings through the policy, so Lemma 1
cannot be applied to it directly. The bound below uses instead the maximum of L(x, y) over the n + 1 fixed pairs
with x + y = n, and Lemma 2 controls that maximum. Bounding R_T by L(n, n) instead would give only
gamma_2 >= m/(2K).

**Lemma 2.** E max_{x+y=n} L(x, y) <= n gamma_2/2 + sqrt(n ln n) + 2 for n >= 2.

Proof. L(x, y) is a function of the n independent characters a_1..a_x, b_1..b_y and changes by at most 1 when one
of them changes. By McDiarmid's inequality [McD], P(L(x, y) >= E L(x, y) + u) <= exp(-2 u^2/n). With
u = sqrt(n ln n) this is n^(-2), and a union bound over the n + 1 pairs gives probability at most (n+1)/n^2 that
some pair exceeds its mean by u. Off that event the maximum is below n gamma_2/2 + u (Lemma 1); on it the maximum is
at most n. So the expectation exceeds n gamma_2/2 + u by at most n (n+1)/n^2 = (n+1)/n <= 2. []

Lueker [Lu, preprint eq. (1)] uses the same fact for his lower bounds, a maximum over unequal splits i + j = n, and
attributes to Alexander [Al] that the strings need not be padded with equal numbers of characters. Lemmas 1 and 2
prove the form used here in full.

Conclusion. By section 3, R_T <= max_{x+y=n} L(x, y) for every outcome. With section 5 and Lemma 2,

    T m/(2K) - 2 V_max/K <= E R_T <= (N+T) gamma_2/2 + sqrt((N+T) ln(N+T)) + 2.

Divide by T and let T -> infinity: m/(2K) <= gamma_2/2, that is gamma_2 >= m/K. This proves Theorem 1. []

## 7. Tests of the steps (paths in this package)

- verify-it-yourself/exact_small.py: exact gain by fractions, compared with m/K, and an exhaustive check of
  F_p <= L for all reveal sequences (section 3). Reads object/small_old/.
- verify-it-yourself/sim_check.py: section 3 on long random strings, against a plain DP.
- verify-it-yourself/sim_rate17.c: a long simulation against m/K (numerical only, no weight in the bound).
- verify-it-yourself/check_a17.c, check_d.c, check_e.c: (C1) to (C3) on every state; negative controls in
  RUN_IT_YOURSELF.md and run_checks.sh.
- verify-it-yourself/lemma1_small.py: exact enumeration of Lemma 1 for x + y <= 7.

## References

- [Al] K. S. Alexander, The rate of convergence of the mean length of the longest common subsequence, Ann. Appl.
  Probab. 4(4) (1994) 1074-1082, https://doi.org/10.1214/aoap/1177004903.
- [CS] V. Chvatal and D. Sankoff, Longest common subsequences of two random sequences, J. Appl. Probab. 12(2)
  (1975) 306-315.
- [Da] V. Dancik, Expected length of longest common subsequences, PhD thesis, University of Warwick, 1994; and
  M. Paterson and V. Dancik, Longest common subsequences, MFCS 1994, LNCS 841, 127-142,
  https://doi.org/10.1007/3-540-58338-6_63.
- [Fe] M. Fekete, Uber die Verteilung der Wurzeln bei gewissen algebraischen Gleichungen mit ganzzahligen
  Koeffizienten, Math. Z. 17 (1923) 228-249, https://doi.org/10.1007/BF01504345.
- [Lu] G. S. Lueker, Improved bounds on the average length of longest common subsequences, J. ACM 56(3) (2009),
  https://doi.org/10.1145/1516512.1516519; preprint of 22 July 2005 read.
- [McD] C. McDiarmid, On the method of bounded differences, in Surveys in Combinatorics 1989, Cambridge University
  Press, 148-188, https://doi.org/10.1017/CBO9781107359949.008.
