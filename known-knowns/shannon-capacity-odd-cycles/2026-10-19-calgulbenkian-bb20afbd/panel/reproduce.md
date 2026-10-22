# reproduce report: shannon-c7 (second pass, extended package)

context: Claude Code subagent, fresh context [claude-sonnet-5-5]

Scope: cell shannon-c7 only. I did not read the earlier reproduce report. I worked in a private copy of the package, with my own code (not shipped in this package) and every output saved there. Single-threaded python/numpy throughout (OMP_NUM_THREADS=1).

## 0. Integrity and order of work

- the contributor's hash list checked from inside the package folder: all 21 files OK.
- Order: (1) read the claim statement (a copy is in verify-it-yourself/), the object data files (base_g5.json, rules.json, schedule.json, cert_input.json, bpz_lean_c7_schedule.json) and Tandon's paper (a PDF copy, not shipped in this package); (2) wrote and ran my own code (not shipped in this package); (3) only then ran the shipped run_checks.sh. I did not open verify-it-yourself/*.py (or the derive script) before my results were saved. schedule.json was used only as data to compare against; my evaluator is hand-coded from the paper.
- Shared-source caveat: my definitions of J+, J15, J30++, X30^{0,L} and the class assignments come from the same paper the folder uses (Section 3.1, Section 4.2, Appendix B, eqs 148-159). Answer 1 below explains why this does not weaken the correctness argument.

## 1. G5 against Definition 2 (own code, not shipped in this package)

Definition 2 (paper): a Gao gadget is an independent set I, t pairwise endpoint-disjoint private pairs (r_i, q_i) (Definition 1: r in I, q not in I, N(q) cap I = {r}), two independent complementary transversals P^H and P^V of the pairs, and an independent auxiliary set X with X cap N(P^H) cap N(P^V) = empty. Profile (a,t,s,o,h,v) = (|I|, t, |X|, |X^0|, |X^H|, |X^V|).

Checked exhaustively on the data of base_g5.json (confusable = every coordinate differs by 0 or +-1 mod 7):
- |I| = |X| = 367, distinct, codes in range.
- I and X independent over all 67,161 pairs each.
- all 8 pairs: r in I, q not in I, and the only word of I confusable with q is r.
- the 16 endpoints are distinct; P^H and P^V each take one endpoint of every pair; both independent.
- X cap N(P^H) cap N(P^V) is empty.
- classes by transversal confusability give profile (367, 8, 367, 322, 26, 19).
All True.

## 2. Certificates re-derived from their definitions (own code)

Method: the base sets give five-dimensional boolean vectors; ten- and fifteen-dimensional sets are exact unions of boxes (sparse ten-dimensional set times five-dimensional set) built from Lemma 1's formulas; closed neighbourhoods by exact dilation; "J minus N(neutral reference)" counted by exact class histograms (no sampling). Neutral parts are computed from the transversal definition (the eq. 20 form is checked equal), not taken from a formula.

- C1 (own script): I10 has 134,753 words and is independent by an exhaustive neighbourhood count over the whole 7^10 array. J = (T x T)(I10) has 27,480 words outside N(X10^0) (paper: 27,480). For the eight exchanges of eq. 152: each removed word is in J, each inserted word has exactly one confusable word in J (the removed one); J+ (134,753 words) is independent by the same exhaustive count. **C1 = 27,488.**
- C2 (own script): I15 = main code of Gao(G10,G5), |I15| = 49,495,055, |R15| = 2,504,616 (= t15); the neutral part of X10 x X5 has 35,342,398 words (Table 6a). J15 = (T x T x T)(I15). **C2 = |J15 minus N(X15^{0,X})| = 12,839,823.**
- C3 (same script): |X15het| = 49,433,743; **C3 = |X15het minus N(X15^{0,X})| = 14,045,805.**
- C4 (own script): J30++ = T^6(I30++), I30++ = main code of Gao(G15het,G15het)[X15;X15] with X15 classified against the G15 transversals (35,275,258 / 6,703,815 / 7,454,670, matches). X30^{0,L} = (neutral of X^{A,X} x neutral of X^{A,het}) union (HV part of X^{A,X} x HV part of X^{A,het}). G10A classes 105,709 / 12,236 / 16,744, G15AX aux classes 35,342,398 / 5,948,463 / 8,140,002 and X^{A,het} classes 35,303,606 / 5,948,463 / 8,180,458 all match the paper; the A-orientation neutral part is exactly the plain neutral part (same set, checked word-wise). Component contributions: 827,599,599,610,592; 6,686,131,598,464; 194,829,147,616; 194,829,147,616; 6,694,533,241,984; 195,073,609,696; 195,073,609,696 (all seven equal Table 5); component sizes sum to 2,455,726,444,728,097 (eq. 137). **C4 = 841,760,069,965,664.**

All four equal Tandon's Table 4. They were obtained before any shipped checker was run.

Dependence of the d=560 integer on each certificate (own script): changing C1, C2 or C4 by +-1 changes M; changing C3 by +-1 does NOT change M. C3 enters only Tandon's n8 branch (G40_8 and the right gadget Gh25); the d=560 chain (G30L, Gh30, Gpp30, R30h, G10, G10D) uses C1, C2 and C4 only.

## 3. Further full-size premise checks (own code)

- Own script (box-level axioms), exhaustive at box level: I15 (49,495,055 words), PH15, PV15, X15het, X15^{A,het} and X10 x X5 are independent (every factor independent, every pair of boxes separated in some factor). Private-pair property at dimension 15: all 2,504,616 private neighbours are outside I15 and each is confusable with exactly one word of I15 (0 violations).
- Own script (I30++): I30++ as 93 four-factor boxes (2,455,726,444,728,097 words): all factors independent, 0 of 4,278 box pairs unseparated. So I30++ is independent exhaustively, and J30++ (its image under T applied blockwise, an automorphism of C_7^5) is too.
- Own script (condition (33)): condition (33) for J0 = Xhat30 (auxiliary set of the sibling gadget Gh30, 2,444,076,335,041,121 words) against the transversals of G30L at dimension 30, computed directly and not through the sibling argument: number of words confusable with both transversals = 0. Class sizes relative to G30L: neutral 1,435,184,942,161,465; H 420,235,140,891,852; V 588,656,251,987,804 (equal to the paper's eq. 132). G30L's own aux classes 1,446,768,903,083,453 / 420,235,140,891,852 / 576,488,425,905,496 also match.

## 4. Theory re-derived and tested on real sets

Re-derived by reading and proof-checking: Lemma 1 (product code, private pairs, transversals, profile eq. 21), Theorem 1 (class counting, eqs 38-43; I rechecked each class, e.g. JH x X_R^H lands in H or V according to whether u is confusable with X_L^0, through P_R^V in P_LR^H), sigma (swap h and v), Phi = (a-t, o, v, h, t, t, t), Definition 6 and Proposition 1 (independence from (i), separation from (ii), cardinalities add). Theorem 1 holds for arbitrary independent J0 (with (33)), JH, JV, so correctness depends only on: those sets are independent, (33) holds, and the q values are the true counts.

Rule data: the separation relation in rules.json equals Definition 4 of the paper; S3b (45 words; per output B17 N10 A5 D5 O0 H4 V4) and K4a (49 words) in rules.json equal the paper's Appendix A lists (parsed from the paper by my own script). Definition 6 (i) and (ii) re-checked by my code for S2a, S3a, S3b; K4a words distinct and pairwise separated.

Real-vertex-set tests (own scripts): 300 Lemma 1 products, 900 Theorem 1 products with random independent J0/JH/JV (J0 limited by (33)), 900 sigma checks: every output passes Definition 2 exhaustively (private pairs, endpoint disjointness, complementary transversals, (7)) and its profile equals the formula; 0 failures. Negative control: 191 cases where J0 holds a word confusable with both transversals; each resulting set is rejected as a gadget. Object-style configuration (60 trials): a two-dimensional left gadget Gao(A, sigma B), its sibling auxiliary set as J0 (condition (33) verified), right gadgets that are base gadgets or sigma of Theorem 1 outputs, then P0, sigma(P1), sigma(P2) built and validated; Phi representations satisfy Definition 5; S3b (equal and mixed dimensions, 40 further trials) outputs satisfy Definition 5 with sizes equal to the formula; K4a on four copies (sets in C_7^4 and C_7^5, 40 trials): independent, size equals the formula.

## 5. M and d for the 3-branch S3b schedule (own evaluator)

Known answer first: my evaluator reproduces eqs 118/119, 122, 126/127 and 135/141/142 (n6, n8, n11 exactly as printed), then S3b and K4a give the 257-digit integer of Theorem 2 (eq. 106) and bound 3.25883262035326630912153905181047543760538759432195.

New schedule: G30L = Gao(G15AX, sigma G15Ah); sibling Gh30; Gpp30 = Gao(G15h,G15h) with a = 2,455,726,444,728,097; P0 = HetGao(G30L,G10); P1 = sigma(HetGao(G30L,R30)) with R30 = sigma(HetGao(G15AX,G15Dh)); P2 = sigma(HetGao(G30L,G10D)); J0 = aux of Gh30, JH = JV = J30++ with q = C4; then S3b(Phi P0, Phi P1, Phi P2) and K4a on four copies.
- d = 4 x (40+60+40) = 560.
- M has 288 digits.
- Bound (certified floor of 10^50 times M^(1/560)): 3.25883477557614484751818055569792750605282670056114.
- Margin over Tandon d=500: +0.00000215522287853839664150388745206844743910623919.
- Exact integer test M^500 > M500^560: True.
All identical to the claimed figures. The n140 vector has O = 0, as S3b has no O words.

BPZ Lean C7 schedule (own evaluator): w0 = (359,322,19,26,8,8,8); nodes n3..n11 by S3a/S2a; n25 = S3b(n6,n11,n8); K4a on four copies, d = 500: a 257-digit integer equal to the BPZ Lean integer in records.json, bound 3.25882798592000703452647896579422134484566287064872 (paper eq. 144: 3.258827985920007034526478965794221; Lean source statement: 3.258827985920007). I cannot read the Lean source here; the integer is compared with the folder's record data and the decimal with the paper.

Side check for open question 5 of the claim record (not shipped): the variant S3b(n6,n11,n11) at d=560 gives 3.25883436223771079435326297235859444166490482822313, equal to the stated figure.

## 6. Shipped checker (run after the above)

Command (from the copied package folder): sh verify-it-yourself/run_checks.sh (about 112 s). Its RESULT lines: C7 d=560 M_digits=288 bound=3.25883477557614484751818055569792750605282670056114 headline_margin_vs_tandon_d500=+0.00000215522287853839664150388745206844743910623919 all_records_beaten=True; G5 Definition 2 axioms all verified exhaustively, profile (367, 8, 367, 322, 26, 19); BPZ Lean C7 schedule known answer reproduced d=500, 257 digits; set-level test passed; certificates re-derived C1=27488 C2=12839823 C3=14045805 C4=841760069965664 (also C2 by a word-by-word enumeration of all 49,495,055 words of J15). Four negative controls rejected as expected. **Last line of run_checks.sh: ALL CHECKS PASS.** No disagreement with my own results on any number.

## 7. Is the d=560 object a valid instance?

Yes, under Lemma 1, Theorem 1 and Proposition 1 as stated. Every ingredient the schedule uses is pinned down: G5 (verified), T and the eight exchanges (verified), C1, C2, C4 (re-derived), the right-hand gadgets (G10, G10D, and R30 from G15AX and G15Dh by Theorem 1, built from verified ingredients), the left gadget G30L with codebooks Xhat30 and J30++ (condition (33), class sizes and counts verified at full size), and S3b and K4a (data equal to the paper, Definition 6 verified). Only the top-level assembly differs from Tandon's: the three inputs have dimensions 40, 60, 40 instead of 30, 55, 40, and Proposition 1 puts no condition on input dimensions. M and d = 560 are reproduced exactly.

Limits: Lemma 1, Theorem 1 and Proposition 1 are proved in the paper and checked here on instances (randomized small sets plus the full-size premises of section 3), not formalised. The gadgets at dimensions 30, 40, 60 and 140 and the final 560-dimensional set (about 10^287 words) are not enumerated (infeasible).

## 8. Open questions of the claim record (not shipped) that concern reproduction

1. (Are the definitions of J+, J15, J30++, X30^{0,L} and the class assignment read as the paper intends?) I found no reading that differs: my independently coded versions reproduce Tandon's Table 4, all seven Table 5 components, the Table 6a class sizes and the profiles of eqs 112-141 exactly. Correctness also does not rest on the paper's wording: Theorem 1 accepts any independent JH and JV, and the q values are counts, so what must hold is (a) these sets are independent and (b) the counts are the counts. I verified (a) exhaustively (J+ over 7^10; I15 and I30++ at box level, with T an automorphism) and (b) from the transversal definitions. A mistaken description in the paper would matter only if it changed an independent set or a count, and neither did.
2. (Is Theorem 1 of a single-author v1 preprint acceptable for the large steps?) For reproduction: I proof-read Theorem 1 and its class bookkeeping (sound), tested it on 900 randomized real-set instances with a negative control, and verified its large-scale premises directly (section 3). What is left unverified is only the use of the theorem's conclusion at dimensions 30, 40, 60, 140 and 560, which cannot be enumerated. Whether that is acceptable is for the criterion skeptic.
3. (Is Xhat30 in the J0 position enough, with (33) taken from the sibling argument?) Checked directly at dimension 30, without the sibling argument: zero words of Xhat30 are confusable with both transversals of G30L, and the class sizes match eq. 132. The sibling argument is correct and not needed.
4. (d=560 against d=500.) The arithmetic is verified exactly (M^500 > M500^560 as integers; 50-digit floors above). Whether this satisfies the bank's "strictly greater" wording is a criterion question, not a reproduction one.
5. (Variant S3b(n6,n11,n11).) Reproduced, 3.25883436223771079435326297235859444166490482822313; confirmed not to be the claimed object.
6. (Re-fetch before filing.) Not a reproduction question; no network was used.

## 9. Mismatches

None between my results, the shipped checker and the paper, on any integer or class size.

pass: true
