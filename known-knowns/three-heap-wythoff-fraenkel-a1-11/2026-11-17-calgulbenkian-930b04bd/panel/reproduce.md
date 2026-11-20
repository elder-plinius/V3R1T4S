context: Claude Code subagent, fresh context [Sonnet 5.5]

# REPRODUCE skeptic report: Fraenkel 3-heap Wythoff, smallest heap A1 = 11

Everything below was recomputed by my own programs (a C++ solver, a C++ brute force, a C++ independence checker and Python analysis scripts, none shipped in this package and none read from the claimant's files). I read only the claim text, the source paper (not shipped in this package) and the certificate as data (object/wythoff_a1_11_certificate.json) before writing the solver. I opened the author's checker only after my verdict (step 4).

## 1. What the paper says (quoted)

Game rules (abstract): "Players take turns removing any number of tokens from a single pile, or removing (a1,...,aN) from all piles, ai tokens from the i-th pile, providing that 0 <= ai <= Ai, sum ai > 0 and a1 xor ... xor aN = 0 ... The first player that cannot make a move loses."

Convention (Section 3): "[a, b, c], a >= 0, b >= 0, c >= 0, is a three-heap Wythoff's position having a, a + b and a + b + c tokens in the piles; [m, A^m_n, B^m_n], where n >= 1 and A^m_n < A^m_{n+1}, are all the P-positions whose first piles have m tokens; P^m is the set of P-positions whose first piles have m tokens".

Definitions (Section 3):
- "T^m = Z>=0 - {A^m_i, A^m_i + B^m_i : i >= 1} - {i : 0 <= i < m}"; Claim 3.1: "T^m = {b : exists a < m, such that [a, m - a, b] in P^a}".
- "S^m = Z>=0 - {B^m_i : i >= 1}".
- "alpha^m_n = m + A^m_n - floor(B^m_n phi)".
- "N1^m is the integer such that when n > N1^m, A^m_n = mex{A^m_i, B^m_i : 1 <= i < n} and B^m_{n+1} = B^m_n + 1".
- "N2^m, alpha^m, and eps^m_n are the integers such that when n > N2^m; A^m_n = mex{...}, B^m_{n+1} = B^m_n + 1; and eps^m_n = m + A^m_n - floor(B^m_n phi) - alpha^m in {0, +-1}".
- "N3^m is the integer such that if N2^m exists and when n > N3^m, eps^m_n eps^m_{n+1} = 0".
- "p(m) = 2^(floor(log2(m))+1)".

Claim 3.3 (membership in S^m; S1^m(n) is "all such numbers"): "if there exists [a,b,c] in P^a and a + b = m, then b + c in S^m; if there exists [a,b,c] in P^a and a + b + c = m, then b in S^m; if there exists n such that B_i != c when i < n; B_n > c; and coeff(F_{2,n}(x1), x1, i) <= 0 with A_n <= i <= A_n + p(m), then c in S^m." Its proof says the coefficients are "positive"/">= 0" (see the flaws below).

Claim 3.4: "There exists an integer N such that when n > N, A^m_n > max{T^i : i <= m} and B^m_n > m + max{T^i : i <= m}. If for a given n > N, B = max({B^m_i : i <= n}), mex({B^m_i : i <= n} U S1^m(n)) = B + 1, and B + 1 - B^i_{n'} > m - a [sic, i] whenever i + A^i_{n'} <= m + A^m_{n+1} with 0 <= i < m, then B^m_{n+1} = B + 1."

Claim 3.5: "For a given m, if N1^i, N2^i and N3^i exist for i < m, the following conditions imply both conjectures for m: given an integer N as in Claim 3.4, if there exist n1 > n2 > N such that
(1) A_{n2+3} + B_{n2+3} < A_{n1};
(2) B_{j+1} = B_j + 1 for n2 <= j <= n1;
(3) B_{n1} = max({B_i : i <= n1});
(4) mex({B_i : i <= n1} U S1(n1)) = B_{n1} + 1;
(5) max(alpha_j : n2 <= j <= n1) - min(alpha_j : n2 <= j <= n1) <= 2;
(6) B^m_{n1} > B^i_{N3^i}, i < m.
Furthermore if alpha' = floor((max(alpha_j) - min(alpha_j))/2) and eps_i = m + A_i - floor(B_i phi) - alpha', we also assume
(7) alpha^i - alpha' >= 4(m - i), 0 <= i < m;
(8) eps_j eps_{j-1} eps_{j-2} = 0, n2 < j < n1."

Lemma 2.4: "Given a Wythoff's sequence {(A_n,B_n)}_{n>=n0}, assume there exist integers N, alpha, and m2 > m1 > N + 2, such that A_n > max(T) when n > N; A_{m2} > B_{m1}; A_n = floor(n phi) + alpha + eps_n where m1 - 2 <= n <= m2 and -1 <= eps_n <= 1; and eps_{i-2} eps_{i-1} eps_i = 0 when m1 - 2 <= i <= m2; then eps_{i-1} eps_i = 0 for any i > m2." Definition 1: a Wythoff's sequence has A_n = mex({A_i,B_i : n0 <= i < n} U T), B_n = A_n + n, {B_n} disjoint from T, T finite. The paper adds that a sequence with "B_{n+1} - A_{n+1} = B_n - A_n + 1 for large n" is made into one "by chopping off a number of pairs ... and reorganizing the indices".

Do Claims 3.4 and 3.5 together imply both conjectures? As the paper states it, yes: Claim 3.5 is stated as a sufficient condition with a half-page inductive proof that calls Claim 3.4 (which has its own proof) and Lemma 2.4 (long case proof), and Claim 3.6 uses it to settle m <= 10. So it is a theorem in the paper, with proof, for a given m once the hypotheses (including existence of N1^i, N2^i, N3^i for all i < m) hold. But the text has typos that I had to resolve, listed below. I judged each one a typo whose intended reading is unambiguous and which is confirmed by Table 1. I did not re-derive the proof of Claim 3.5 or Lemma 2.4 beyond checking their hypotheses. Whether the chain is sound is the paper's, not mine.

Flaws and ambiguities found in the paper text (all handled below, none changes the outcome):
- (F1) Claim 3.5 "alpha' = floor((max - min)/2)": taken literally this is 1 here, and condition (7) then fails for every row (alpha^0 = 0, 0 - 1 >= 4 is false). Only the midpoint floor((max+min)/2) (= alpha^m, = -61) makes (7) and eps_i in {0,+-1} meaningful. I used the midpoint and also report the literal result.
- (F2) Claim 3.3 rule 3 says "coeff <= 0" but the proof says positive. I used the proof's meaning: the row c is attacked at every A in the window.
- (F3) The definition of T^m subtracts "{i : 0 <= i < m}". Taken literally, that removes members of Table 1's T (m = 3 would give {3}, not {1,2,3}). Table 1 and Claim 3.1 agree with the version without that subtraction, which is what I used.
- (F4) N1/N2 are defined with "n > N", but Table 1's values are the first index of the regime ("n >= N"); with strict n > N each is one smaller for m >= 1. I report both. Both satisfy Claim 3.5 trivially.
- (F5) Lemma 2.4 needs the eps product to vanish also at i = m2 (= n1), while Claim 3.5 (8) only asks n2 < j < n1. I checked j = n1 as well (it holds).
- (F6) The paper's mex formula and Z>=0 - {...} sets mix offsets and absolute heap values; I read A^m_n + m as the second heap and A^m_n + B^m_n + m as the third, consistent with alpha = m + A - floor(B phi) and with the Table 1 value alpha^1 = -4 for [1,32,23].

## 2. My solver and its validation

Solver (my own, from the move rules): for each smallest heap m = 0..11 in turn, scanning second heap x upward and third heap y upward, the first position (m,x,y) not yet reachable from an already found P-position is P; all positions that can move to a found P-position (single-heap move or xor-zero removal) are marked. Every move gives a componentwise smaller sorted triple, so this order is valid. Range: second heap x <= 6000, third heap y <= 10200 (largest y found 9746; the program aborts if a y gets near the cap). Output: 3707..3710 P-positions per level, 44,500 in all, index 3250 (= n1 + 1) is covered for m = 11. Re-running gave an identical file (sha256 56d96e05...74db8 both runs): deterministic.

Validation, all from the literal rules:
- A separate brute force (my own, tries every single-heap move and every xor-zero removal for every sorted triple) on all heaps <= 420: 1841 P-positions with smallest heap <= 11, identical to my solver's list restricted to y <= 420 (also checked at <= 260: 1107, identical). Brute force over all smallest heaps gave 9254 P-positions below 420, first ones (0,0,0), (0,1,2), (0,3,5).
- Independence check (my own, over my whole list): from each of the 44,500 P-positions, every single-heap and xor-zero move was tried; moves into the P-set: 0.
- T^m via Claim 3.1 equals the complement definition without the {i<m} subtraction for all m = 0..11.

Constants recomputed from my P-lists (paper definitions; alpha_n = m + A_n - floor(B_n phi), using exact integer floor(B phi) = (B + isqrt(5B^2))//2):

Table 1 comparison, m = 0..10: T, S and alpha match the paper's printed Table 1 in all 11 rows (T by Claim 3.1; S = non-B values; the S lists are identical entry by entry, including the 36 entries for m = 10). N1 and N2: Table 1 values (m=0..10: N1 = 1, 21, 28, 48, 126, 71, 113, 227, 388, 645, 656; N2 = 1, 28, 58, 73, 208, 123, 232, 343, 648, 645, 656) all match under the "n >= N" convention (strict n > N gives each minus 1 for m >= 1, see F4). After the table's N2 the alpha_n take exactly the three values alpha-1, alpha, alpha+1 in every row, through index ~3700. Result: all 11 rows reproduce. No error found in Table 1.

N3 (smallest N with eps_n eps_{n+1} = 0 for all n >= N in my range; strict n > N is one less) and B at that index, mine vs certificate:
i=0: 1, 0; i=1: 75, 77; i=2: 157, 162; i=3: 206, 216; i=4: 561, 573; i=5: 345, 361; i=6: 637, 657; i=7: 937, 962; i=8: 1739, 1767; i=9: 1070, 1102; i=10: 1766, 1801. All equal to the certificate's N3 and B_N3 (11 of 11), including i = 0.

m = 11 constants: T^11 = {1, 7, 11, 13, 17, 21, 23} (matches). S^11 = 40 values, max 1252, equal to the certificate's S. alpha_j over j = n2..n1 takes values -62, -61, -60 (spread 2); alpha^11 = -61. N1 = N2 = 1214 and N3 = 1381 with B_{N3} = 1420 (n >= N convention; 1213, 1213, 1380 strict). Claimed positions: P_{n2+3} = [11,1964,1258], P_{n1} = [11,5248,3288], as in the certificate. Also B_j - j = 39 for every j from 1214 to the end of my range (3706).

## 3. Conditions for m = 11 with n2 = 1216, n1 = 3249

- Claim 3.4 N: max of all T^i, i <= 11, is 23; A_n > 23 and B_n > 34 hold for all n >= 15 (largest failing index 14; the certificate's 15 is the n >= convention). n2 = 1216 > N. OK.
- (1) 1964 + 1258 = 3222 < 5248. OK.
- (2) B_{j+1} = B_j + 1 for 1216 <= j <= 3249. OK.
- (3) B_{3249} = 3288 = max of B_1..B_3249. OK.
- (4) S1(3249) computed from the three rules of Claim 3.3 by my own code: rule 1 gives {8,18,20,21,22,23,24}; rule 2 gives {2,7}; rule 3 (window of p(11) = 16, i.e. A..A+16, attack by an xor-zero removal that lowers the first heap to a smaller P-position, from my P-lists, with the c not-yet-used / B_n > c condition) gives 40 values; the union is exactly all 40 values of S^11 (max 1252). mex({B_i : i <= 3249} U S1) = 3289 = B_{3249} + 1. OK.
- (5) spread of alpha_j over [1216, 3249] is 2. OK.
- (6) B^11_{3249} = 3288 exceeds B^i at both N3^i and N3^i + 1 for every i = 0..10 (largest is 1801/1802). OK.
- (7) with alpha' = -61: alpha^i - alpha' = 61, 57, 51, 45, 41, 35, 29, 22, 15, 9, 5 for i = 0..10 against 4(m - i) = 44, 40, 36, 32, 28, 24, 20, 16, 12, 8, 4. All OK, tightest is i = 10 (5 >= 4). With F1's literal alpha' = 1 it fails.
- (8) eps_j eps_{j-1} eps_{j-2} = 0 for all 1216 < j < 3249; also |eps| <= 1 for 1215..3250, also holds at j = 3249 itself (F5). Longest run of consecutive nonzero eps in range is 2. OK.
- Claim 3.4's quantified hypothesis at n = n1: for every lower P-position [i, ., .] with second heap <= m + A^m_{n1+1}, B + 1 - B^i_{n'} > m - i; zero violations, minimum slack 2 (i = 10, n' = 3251).
- Lemma 2.4: chopping the sequence at n2 = 1216 (re-indexing by B_j = j + 39), the exceptional set T' = Z>=0 minus {A_i, A_i+B_i : i >= 1216} (taking absolute heap values) has max 3222 (= third heap of index 1215) and A_n > 3222 for every n > N = 1990 (the certificate's j_chop = 1990 is this N). Taking m1 = 1993 (the largest index with third heap below A_{n1}: 5258 < 5259) gives m1 > N + 2 = 1992, m2 = 3249 > m1, A_{m2} > B_{m1} (5259 > 5258), |eps| <= 1 for 1991 <= n <= 3249 (and eps_{1989}, eps_{1990} = -1, 0), and the eps triple product is 0 for 1991 <= i <= 3249. The mex form holds for the chopped sequence over my whole range. The margin 5259 vs 5258 is tight but exact. As a consistency check, the lemma's conclusion (no two consecutive nonzero eps) also holds on my computed range beyond n1 up to index 3706.

## 4. Author's checker (after my verdict)

Ran the shipped checker (python3 -I, 47 s). It printed the same constants (m = 1..11 alphas, N1/N2/N3, B_N3, n2, n1), "All 11 rows of Table 1 match", T^11, |S^11| = 40, max 1252, N = 15, n2 = 1216, n1 = 3249, and PASS. Agrees with my numbers on every item compared.

## 5. Limits (stated honestly)

- This is a finite check of the eight hypotheses and of the data used; it is not a re-proof of Claim 3.5 or Lemma 2.4. The inductive and case proofs and the infinite-range statements (T' stays finite, B keeps incrementing, eps bounded forever) rest on the paper; my computed range runs to index ~3706 and shows no break.
- Claim 3.5 also needs N1^i, N2^i, N3^i to exist for i < 11. I recomputed their values (above) but did not independently re-run all eight conditions of Claim 3.5 for each i = 1..10; that existence rests on the paper's Claim 3.6 plus my finite observation that the regimes are stable out to index ~3700.
- Paper typos F1..F6 were resolved by reading intent (checked against Table 1); a reader who insists on the literal alpha' formula would find condition (7) false.
- I could not check the criterion's "not already published as proved" (it needs the GONC column, arXiv and journals; no network was used).

## Verdict

Every property I could check from the paper's definitions and my own from-the-rules solver holds: Table 1 reproduces in full, N3^i and B^i_{N3^i} for i = 0..10 equal the certificate, and all eight hypotheses of Claim 3.5, the quantified hypothesis of Claim 3.4, and the Lemma 2.4 hypotheses hold for m = 11 with n2 = 1216, n1 = 3249, alpha = -61, with the stated limits.

pass: true
