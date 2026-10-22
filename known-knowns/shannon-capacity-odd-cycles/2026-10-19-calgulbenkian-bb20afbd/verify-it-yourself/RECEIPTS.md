# Receipts (real output of `sh verify-it-yourself/run_checks.sh`)

```
== object files against INDEX.csv
sha256 ok  object/schedule.json
sha256 ok  object/rules.json
sha256 ok  object/argon_shannon_certificates.json
sha256 ok  object/base_g5.json
sha256 ok  object/cert_input.json
sha256 ok  object/bpz_lean_c7_schedule.json
== shannon_check.py: separation property of every table and code used, exact recomputation of M, exact comparison with the live records
== claim C7 (S3b(Phi(P0), Phi(P1), Phi(P2)) then K4a on four copies; P0,P1,P2 have dimensions 40, 60, 40; d = 4 x 140 = 560), key new_record_best
-- 1. separation relation
  [ok]   label separation relation equals Definition 4 of the paper (22 ordered pairs)
  [ok]   separation relation is symmetric
-- 2. admissibility of every table and terminal code used: ['S2a', 'S3a', 'S3b'] ; ['K4a']
  [ok]   table S2a (arity 2, 20 words): Definition 6 (i) and (ii), 0 violations
  [ok]   table S3a (arity 3, 58 words): Definition 6 (i) and (ii), 0 violations
  [ok]   table S3b (arity 3, 45 words): Definition 6 (i) and (ii), 0 violations
  [ok]   terminal code K4a (arity 4, 49 words): pairwise separated, 0 violations
-- 3. recompute M along the schedule (Tandon gadget calculus + BPZ top level)
  [ok]   gadget G10 profile equals the value printed in the paper
  [ok]   gadget G10A profile equals the value printed in the paper
  [ok]   gadget G10D profile equals the value printed in the paper
  [ok]   gadget G15X profile equals the value printed in the paper
  [ok]   gadget G15h profile equals the value printed in the paper
  [ok]   gadget G15AX profile equals the value printed in the paper
  [ok]   gadget G15Ah profile equals the value printed in the paper
  [ok]   gadget G15DX profile equals the value printed in the paper
  [ok]   gadget G15Dh profile equals the value printed in the paper
  [ok]   gadget G15Dh equals sigma(G15Ah)
  [ok]   gadget G30_6 profile equals the value printed in the paper
  [ok]   gadget G25_8 profile equals the value printed in the paper
  [ok]   gadget G40_8 profile equals the value printed in the paper
  [ok]   gadget G30L profile equals the value printed in the paper
  [ok]   gadget Gh30 profile equals the value printed in the paper
  [ok]   gadget Gh25 profile equals the value printed in the paper
  [ok]   gadget G55 profile equals the value printed in the paper
  [ok]   known-answer: Tandon n6 vector equals eq. (119)/(160) of the paper
  [ok]   known-answer: Tandon n8 vector equals eq. (127)/(162) of the paper
  [ok]   known-answer: Tandon n11 vector equals eq. (142)/(161) of the paper
  [ok]   known-answer: Tandon's d=500 integer (257 digits) recomputed equals Theorem 2 of the paper
  [ok]   known-answer: M500^(1/500) = 3.25883262035326630912153905181047543760538759432195 starts with the paper's 3.2588326203532663091215390518104754376053875943219
  [ok]   known-answer: BPZ Lean C7 schedule recomputes the Lean integer (257 digits)
  child P0   dim 40 profile [331752422981032566145, 26158021392280384832, 329527817669082110849, 176106171878551246405, 67809009278844437238, 85612636511686427206]
  child P1   dim 60 profile [6057695260227493703397667114561, 508621887739588144587762647808, 5986287061858070256705570571905, 2904914064800094180917939512707, 1790529741218474635086091592208, 1290843255839501440701539466990]
  child P2   dim 40 profile [331752422981032566145, 26158021392280384832, 329527817669082110849, 176106171878551246405, 89250516720400951188, 64171129070129913256]
  top vector w140 = [630766696962094779919284434617341868416010350084817566525940219475161281, 143484926071391475014250112679318528983164949334707852963844375181504075, 253607180236259210997631571157482273650003990245919037028644104108812492, 262239353627695794777508098705300532815055102315728514419774692317660266, 0, 42885596719613999009464472928234665903014173297488667102621689492629632, 42885596719613999009464472928234665903014173297488667102621689492629632]
  [ok]   top 140-dimensional vector equals the contributor's claimed vector
  [ok]   profile of P0 equals the contributor's pi_P0
  [ok]   profile of P1 equals the contributor's pi_P1
  [ok]   profile of P2 equals the contributor's pi_P2
-- 4. M and degree against the contributor's claim
  [ok]   recomputed M equals the contributor's M (288 digits)
  [ok]   recomputed degree d = 560 equals the contributor's degree
  the set lives in C_7^(box 560)
-- 5. bound and exact comparison with every record
  bound M^(1/d) with d=560: 3.25883477557614484751818055569792750605282670056114 (floor at 50 digits, certified by exact integer powers)
  [ok]   bound equals the contributor's 50-digit value
  record tandon_d500                        d=500   bound 3.25883262035326630912153905181047543760538759432195  margin +0.00000215522287853839664150388745206844743910623919  direct M^d_rec > M_rec^d: True
  [ok]   bound strictly greater than Tandon (arXiv:2608.30273 Theorem 2, d=500; the live top entry of 9a.md) (exact integer test)
  record bpz_lean                           d=500   bound 3.25882798592000703452647896579422134484566287064872  margin +0.00000678965613781299170158990370616120716382991242  direct M^d_rec > M_rec^d: True
  [ok]   bound strictly greater than BPZ Lean repository CertC7.lean at aa21eeb12b75 (d=500) (exact integer test)
  [ok]   bound strictly greater than 9a.md, C7 table, Tandon row (8 decimals shown) = 3.25883262 (even after rounding the displayed decimal up one unit in its last place)
  record 9a_tandon_rounded                  decimal 3.25883262  margin over the displayed decimal 0.00000215557614484751818055569792750605282670056114
  [ok]   bound strictly greater than 9a.md, C7 table, BPZ row = 3.258805369885 (even after rounding the displayed decimal up one unit in its last place)
  record 9a_bpz                             decimal 3.258805369885  margin over the displayed decimal 0.00002940569114484751818055569792750605282670056114
  [ok]   bound strictly greater than 9a.md, C7 table, Gao row = 3.258789153908 (even after rounding the displayed decimal up one unit in its last place)
  record 9a_gao                             decimal 3.258789153908  margin over the displayed decimal 0.00004562166814484751818055569792750605282670056114
  record ircr_134753_d10                    d=10    bound 3.25802073729324535952785870883064553932884830825483  margin +0.00081403828289948799032184686728196672397839230631  direct M^d_rec > M_rec^d: True
  [ok]   bound strictly greater than Itty-Rosin-Carstensen-Reichman 134,753 in C7^10 (arXiv:2607.21517) (exact integer test)
  record polak_schrijver_367_d5             d=5     bound 3.25786596678351595041247966865578245402043969655005  margin +0.00096880879262889710570088704214505203238700401109  direct M^d_rec > M_rec^d: True
  [ok]   bound strictly greater than Polak-Schrijver 367 in C7^5 (arXiv:1808.07438) (exact integer test)

RESULT C7 d=560 M_digits=288 bound=3.25883477557614484751818055569792750605282670056114 headline_margin_vs_tandon_d500=+0.00000215522287853839664150388745206844743910623919 all_records_beaten=True time=0.1s
== negative control 1: one duplicated word in a substitution table must be rejected
negative control 1 rejected as expected
== negative control 2: one input changed by 1 (a certificate, or the base vector) must change M and be rejected
negative control 2 rejected as expected
== G5 base gadget: every axiom of Definition 2, exhaustive
  [ok]   all words are valid codes of C_7^5
  [ok]   I has 367 distinct words
  [ok]   X has 367 distinct words
  [ok]   I is independent (all 67161 pairs)
  [ok]   X is independent (all 67161 pairs)
  [ok]   t = 8 private pairs
  [ok]   each pair (r, q): r in I, q not in I, and the only word of I confusable with q is r (exhaustive over I)
  [ok]   the 16 endpoints are pairwise distinct (endpoint-disjoint pairs)
  [ok]   P^H and P^V contain exactly one endpoint of each pair, and complementary ones
  [ok]   P^H and P^V are independent (all pairs)
  [ok]   X meet N(P^H) meet N(P^V) is empty
  profile (a,t,s,o,h,v) = (367, 8, 367, 322, 26, 19)
  [ok]   profile equals (367, 8, 367, 322, 26, 19) of eq. (47)
  [ok]   X = X^0 + X^H + X^V
RESULT G5 Definition 2 axioms all verified exhaustively; profile (367, 8, 367, 322, 26, 19)
== BPZ Lean C7 schedule: known answer (the integer defined in CertC7.lean)
  table S2a: Definition 6 violations 0
  table S3a: Definition 6 violations 0
  table S3b: Definition 6 violations 0
  code K4a: pairwise separation violations 0
  child exponents agree with the Lean exponents; E = 100, d = 500
  M (257 digits) equals the integer defined in CertC7.lean (d = 500)
RESULT BPZ Lean C7 schedule known answer reproduced: d=500, 257 digits
== set-level test: Lemma 1, Theorem 1, sigma, Phi, S3b, K4a on explicit vertex sets
  [ok]   g: Definition 2 holds on the explicit sets (dim 1, profile (3, 1, 3, 1, 1, 1))
  [ok]   base gadget g
  [ok]   g has the profile (3,1,3,1,1,1) of the paper's Example 1
  [ok]   g+1: Definition 2 holds on the explicit sets (dim 1, profile (3, 1, 3, 1, 1, 1))
  [ok]   g+3: Definition 2 holds on the explicit sets (dim 1, profile (3, 1, 3, 1, 1, 1))
  [ok]   -g: Definition 2 holds on the explicit sets (dim 1, profile (3, 1, 3, 1, 1, 1))
-- Lemma 1 on gadgets of dimensions 1 and 2
  [ok]   Gao(g,g+1): profile of the explicit sets equals eq. (21): (10, 2, 9, 5, 2, 2)
  [ok]   Gao(g,g+1) (Lemma 1 output): Definition 2 holds on the explicit sets (dim 2, profile (10, 2, 9, 5, 2, 2))
  [ok]   Gao(-g,g+3): profile of the explicit sets equals eq. (21): (10, 2, 9, 5, 2, 2)
  [ok]   Gao(-g,g+3) (Lemma 1 output): Definition 2 holds on the explicit sets (dim 2, profile (10, 2, 9, 5, 2, 2))
-- configuration A: one-dimensional left gadget L = g, heterogeneous codebooks (J0, JH, JV)
  [ok]   inner HetGao(g+1,g+3) (right gadget R1): J0, JH, JV independent in the left graph
  [ok]   inner HetGao(g+1,g+3) (right gadget R1): J0 meet N(P_L^H) meet N(P_L^V) is empty (eq. 33)
  [ok]   inner HetGao(g+1,g+3) (right gadget R1): code, pairs and transversals are those of the ordinary product
  [ok]   inner HetGao(g+1,g+3) (right gadget R1): profile of the explicit sets equals eqs (38),(39): (10, 2, 7, 3, 2, 2)
  [ok]   inner HetGao(g+1,g+3) (right gadget R1) (Theorem 1 output): Definition 2 holds on the explicit sets (dim 2, profile (10, 2, 7, 3, 2, 2))
  [ok]   A: P0 = HetGao(L,R0): J0, JH, JV independent in the left graph
  [ok]   A: P0 = HetGao(L,R0): J0 meet N(P_L^H) meet N(P_L^V) is empty (eq. 33)
  [ok]   A: P0 = HetGao(L,R0): code, pairs and transversals are those of the ordinary product
  [ok]   A: P0 = HetGao(L,R0): profile of the explicit sets equals eqs (38),(39): (10, 2, 8, 5, 2, 1)
  [ok]   A: P0 = HetGao(L,R0) (Theorem 1 output): Definition 2 holds on the explicit sets (dim 2, profile (10, 2, 8, 5, 2, 1))
  [ok]   A: HetGao(L,R1): J0, JH, JV independent in the left graph
  [ok]   A: HetGao(L,R1): J0 meet N(P_L^H) meet N(P_L^V) is empty (eq. 33)
  [ok]   A: HetGao(L,R1): code, pairs and transversals are those of the ordinary product
  [ok]   A: HetGao(L,R1): profile of the explicit sets equals eqs (38),(39): (29, 5, 18, 11, 5, 2)
  [ok]   A: HetGao(L,R1) (Theorem 1 output): Definition 2 holds on the explicit sets (dim 3, profile (29, 5, 18, 11, 5, 2))
  [ok]   A: HetGao(L,R2): J0, JH, JV independent in the left graph
  [ok]   A: HetGao(L,R2): J0 meet N(P_L^H) meet N(P_L^V) is empty (eq. 33)
  [ok]   A: HetGao(L,R2): code, pairs and transversals are those of the ordinary product
  [ok]   A: HetGao(L,R2): profile of the explicit sets equals eqs (38),(39): (10, 2, 8, 5, 2, 1)
  [ok]   A: HetGao(L,R2) (Theorem 1 output): Definition 2 holds on the explicit sets (dim 2, profile (10, 2, 8, 5, 2, 1))
  [ok]   A: P1 = sigma(HetGao(L,R1)): Definition 2 holds on the explicit sets (dim 3, profile (29, 5, 18, 11, 2, 5))
  [ok]   A: P2 = sigma(HetGao(L,R2)): Definition 2 holds on the explicit sets (dim 2, profile (10, 2, 8, 5, 1, 2))
  [ok]   A:: Phi(P0) is a seven-family representation (7 independent sets, all separated pairs separated), dim 2
  [ok]   A:: Phi(P1) is a seven-family representation (7 independent sets, all separated pairs separated), dim 3
  [ok]   A:: Phi(P2) is a seven-family representation (7 independent sets, all separated pairs separated), dim 2
  [ok]   A:: S3b output sizes equal the polynomial map [2123, 528, 577, 594, 0, 365, 365] (dim 7)
  [ok]   A:: every S3b output family is an independent set in C_7^7
  [ok]   A:: every separated pair of S3b output families is separated (no word of one confusable with a word of the other)
-- configuration B: two-dimensional left gadget L = Gao(g, sigma(g+1)) with J0 from the sibling gadget over the same ordered pair
  [ok]   L = Gao(g, sigma(g+1)): profile of the explicit sets equals eq. (21): (10, 2, 9, 5, 2, 2)
  [ok]   L = Gao(g, sigma(g+1)) (Lemma 1 output): Definition 2 holds on the explicit sets (dim 2, profile (10, 2, 9, 5, 2, 2))
  [ok]   sibling Gh = HetGao(g, sigma(g+1)): J0, JH, JV independent in the left graph
  [ok]   sibling Gh = HetGao(g, sigma(g+1)): J0 meet N(P_L^H) meet N(P_L^V) is empty (eq. 33)
  [ok]   sibling Gh = HetGao(g, sigma(g+1)): code, pairs and transversals are those of the ordinary product
  [ok]   sibling Gh = HetGao(g, sigma(g+1)): profile of the explicit sets equals eqs (38),(39): (10, 2, 9, 4, 2, 3)
  [ok]   sibling Gh = HetGao(g, sigma(g+1)) (Theorem 1 output): Definition 2 holds on the explicit sets (dim 2, profile (10, 2, 9, 4, 2, 3))
  [ok]   sibling and L have the same code, pairs and transversals, so the sibling's auxiliary set is admissible as J0 for L
  [ok]   JH = JV = image of the main code of L under x -> -x (independent)
  [ok]   B: P0 = HetGao(L,R0): J0, JH, JV independent in the left graph
  [ok]   B: P0 = HetGao(L,R0): J0 meet N(P_L^H) meet N(P_L^V) is empty (eq. 33)
  [ok]   B: P0 = HetGao(L,R0): code, pairs and transversals are those of the ordinary product
  [ok]   B: P0 = HetGao(L,R0): profile of the explicit sets equals eqs (38),(39): (31, 7, 29, 8, 10, 11)
  [ok]   B: P0 = HetGao(L,R0) (Theorem 1 output): Definition 2 holds on the explicit sets (dim 3, profile (31, 7, 29, 8, 10, 11))
  [ok]   B: HetGao(L,R1): J0, JH, JV independent in the left graph
  [ok]   B: HetGao(L,R1): J0 meet N(P_L^H) meet N(P_L^V) is empty (eq. 33)
  [ok]   B: HetGao(L,R1): code, pairs and transversals are those of the ordinary product
  [ok]   B: HetGao(L,R1): profile of the explicit sets equals eqs (38),(39): (31, 7, 29, 8, 10, 11)
  [ok]   B: HetGao(L,R1) (Theorem 1 output): Definition 2 holds on the explicit sets (dim 3, profile (31, 7, 29, 8, 10, 11))
  [ok]   B: HetGao(L,R2): J0, JH, JV independent in the left graph
  [ok]   B: HetGao(L,R2): J0 meet N(P_L^H) meet N(P_L^V) is empty (eq. 33)
  [ok]   B: HetGao(L,R2): code, pairs and transversals are those of the ordinary product
  [ok]   B: HetGao(L,R2): profile of the explicit sets equals eqs (38),(39): (31, 7, 29, 8, 10, 11)
  [ok]   B: HetGao(L,R2) (Theorem 1 output): Definition 2 holds on the explicit sets (dim 3, profile (31, 7, 29, 8, 10, 11))
  [ok]   B: P1 = sigma(HetGao(L,R1)): Definition 2 holds on the explicit sets (dim 3, profile (31, 7, 29, 8, 11, 10))
  [ok]   B: P2 = sigma(HetGao(L,R2)): Definition 2 holds on the explicit sets (dim 3, profile (31, 7, 29, 8, 11, 10))
  [ok]   B:: Phi(P0) is a seven-family representation (7 independent sets, all separated pairs separated), dim 3
  [ok]   B:: Phi(P1) is a seven-family representation (7 independent sets, all separated pairs separated), dim 3
  [ok]   B:: Phi(P2) is a seven-family representation (7 independent sets, all separated pairs separated), dim 3
  [ok]   B:: S3b output sizes equal the polynomial map [28706, 7428, 10436, 9976, 0, 1687, 1687] (dim 9)
  [ok]   B:: every S3b output family is an independent set in C_7^9
  [ok]   B:: every separated pair of S3b output families is separated (no word of one confusable with a word of the other)
-- terminal code K4a on four copies of the base representation (real sets)
  [ok]   K4a on 4 copies of Phi(g): 100 words in C_7^4 = formula
  [ok]   K4a output is an independent set in C_7^4 (exhaustive)
RESULT set-level test passed: Lemma 1, Theorem 1, sigma, Phi, S3b, K4a on explicit sets
== box-level axioms: I15 and I30++ independent, dimension-15 private pairs, condition (33) for Xhat30 at dimension 30
  [ok]   J+ rebuilt (134753 words)  [1s]
  [ok]   |I15| = 49495055, |R15| = |Q15| = 2504616  [1s]
  [ok]   X15het classes (o,h,v) = [35275258, 6703815, 7454670]  [1s]
-- A. independence of the 15-dimensional sets (box level, exhaustive)
  [ok]   I15 (49,495,055 words; J15 = T^3(I15) is its image under an automorphism): 7 boxes, all factors independent, 0 of 21 box pairs not separated in any factor  [5s]
  [ok]   PH15: 2 boxes, all factors independent, 0 of 1 box pairs not separated in any factor  [5s]
  [ok]   PV15: 2 boxes, all factors independent, 0 of 1 box pairs not separated in any factor  [5s]
  [ok]   X15X = X10 x X5: 15 boxes, all factors independent, 0 of 105 box pairs not separated in any factor  [8s]
  [ok]   X15het (eq. 156, auxiliary set of G15het): 9 boxes, all factors independent, 0 of 36 box pairs not separated in any factor  [10s]
  [ok]   X15^{A,het} (auxiliary set of G15Ah): 12 boxes, all factors independent, 0 of 66 box pairs not separated in any factor  [10s]
-- B. private-pair property of G15 = Gao(G10, G5), exhaustive over the 2,504,616 pairs
  [ok]   the centres R15 are boxes of I15  [10s]
  [ok]   private-pair property at dimension 15: 2504616 private neighbours q tested; each is confusable with exactly one word of I15 (the centre r, which is confusable with q since r, q differ by a private pair of G5 in one block); violations 0  [21s]
  [ok]   the two boxes of Q15 are disjoint (all 2504616 endpoints q distinct); the endpoints r are distinct because R15 sits in the independent set I15 as two disjoint boxes  [21s]
-- C. independence of I30++ (main code of Gao(G15het, G15het)) at box level
  [ok]   I15 = B15 + R15  [21s]
  [ok]   I30++ as 61 four-factor boxes, 2455726444728097 words in total (eq. 137)  [21s]
  [ok]   I30++ (2,455,726,444,728,097 words; J30++ = T^6(I30++) is its image under an automorphism): 61 boxes, all factors independent, 0 of 1830 box pairs not separated in any factor  [22s]
-- D. condition (33) for Xhat30 against the transversals of G30L, dimension 30
  [ok]   |Xhat30| = 2444076335041121 (paper: 2444076335041121)  [23s]
  [ok]   Xhat30 (auxiliary set of the sibling gadget), four-factor boxes: 138 boxes, all factors independent, 0 of 9453 box pairs not separated in any factor  [28s]
  [ok]   Xhat30 meet N(P^H_30L) meet N(P^V_30L): 0 words (condition (33) holds)  [37s]
  [ok]   Xhat30 classes relative to G30L: (o,h,v) = (1435184942161465, 420235140891852, 588656251987804) = the paper's (j0 decomposition, eq. 132)  [37s]
  [ok]   ordinary auxiliary set of G30L (X15X x X15^{A,het}): axiom X meet N(PH) meet N(PV) empty, classes (o,h,v) = (1446768903083453, 420235140891852, 576488425905496) = eq. (129)  [41s]
RESULT box-level axioms verified: I15, I30++ independent; dimension-15 private pairs; condition (33) for Xhat30 at dimension 30 (zero words in both neighbourhoods); J30++ independent as an automorphic image of I30++ time=41s
== certificates C1 to C4 re-derived from their definitions (not Tandon's script), with a word-by-word enumeration for C2
  [ok]   T is a bijection of the 16807 words
  [ok]   T maps confusable pairs to confusable pairs (all 16807 x 243 pairs); T is a bijection, so it is an automorphism of C_7^5
  [ok]   X5 = X5^0 + X5^H + X5^V (322, 26, 19)
  [ok]   X10 = X10^0 + X10^H + X10^V
  [ok]   X10 sizes (s,o,h,v) = [134689, 105709, 14490, 14490] (Table 6(a))
  [ok]   neutral part of X10 is the same for the orientation A (G10A = Gao(sigma G5, G5)) as for G10
  [ok]   |I10| = 134753 and the 5152 pair centres lie in I10
  [ok]   I10 is independent (exhaustive)  [2s]
  [ok]   (T x T)(I10) is an independent set of 134753 words (T is an automorphism)
  [ok]   |(T x T)(I10) minus N(X10^0)| = 27480 before the exchanges (eq. 151: 27480)
  [ok]   J+ (after eight exchanges) has 134753 words and is independent (exhaustive)
  [ok]   C1 = |J+ minus N(X10^0)| = 27488 (Table 4: 27,488)
  X10 groups by signature: {(0, 0, 0, 0, True): 105709, (0, 1, 0, 1, False): 8372, (1, 0, 1, 0, False): 6118, (1, 0, 0, 1, False): 8372, (0, 1, 1, 0, False): 6118}
  J+ groups by 'in N(X10^0)': {True: 107265, False: 27488}
  [ok]   neutral part of the ordinary X10 x X5 is the same for transversals of G15X and of G15AX
  [ok]   |X15^{0,X}| = 35342398 (Table 6: 35342398)
  [ok]   X15 (eq. 156) class sizes (s,o,h,v) = [49433743, 35275258, 6703815, 7454670] (Table 6(a): 49433743, 35275258, 6703815, 7454670)
  [ok]   |neutral part of X15^{A,het}| = 35303606 (Table 6: 35303606)
  [ok]   |I15| = (a10-t10)(a5-t5) + t10 s5 + s10 t5 = 49495055
  [ok]   C2 = |J15 minus N(X15^{0,X})| = 12839823 (Table 4: 12,839,823)  [27s]
  [ok]   C3 = |X15 minus N(X15^{0,X})| = 14045805 (Table 4: 14,045,805)
  [ok]   I15 = B15 + R15
  [ok]   t15 = 2504616
  flag histograms done  [30s]
  [ok]   component B15xB15      size 2208101357412721 contribution 827599599610592 (Table 5)
  [ok]   component R15xX15^0    size 88350975590928 contribution 6686131598464 (Table 5)
  [ok]   component P15^HxX15^H  size 16790482310040 contribution 194829147616 (Table 5)
  [ok]   component P15^VxX15^V  size 18671085756720 contribution 194829147616 (Table 5)
  [ok]   component X15^0xR15    size 88350975590928 contribution 6694533241984 (Table 5)
  [ok]   component X15^HxP15^V  size 16790482310040 contribution 195073609696 (Table 5)
  [ok]   component X15^VxP15^H  size 18671085756720 contribution 195073609696 (Table 5)
  [ok]   |I30++| = 2455726444728097 (eq. 137)
  [ok]   |X30^{0,L}| = |U0||V0| + |U1||V1| = 1446768903083453 (Table 6: 1446768903083453)
  [ok]   C4 = |J30++ minus N(X30^{0,L})| = 841760069965664 (Table 4: 841,760,069,965,664)  [30s]
-- word-by-word enumeration of J15 (49495055 words) for C2
  [ok]   brute-force enumeration of all 49495055 words of J15 gives C2 = 12839823 (agrees with the histogram method)  [34s]
RESULT certificates re-derived: C1=27488 C2=12839823 C3=14045805 C4=841760069965664 time=34s
== negative control 3: a corrupted base set (one word of I5 replaced by another word of I5) must fail the G5 check
negative control 3 rejected as expected
== negative control 4: a wrong value for C1 in the comparison ledger must be reported as a mismatch
negative control 4 rejected as expected
RESULT C7 d=560 M_digits=288 bound=3.25883477557614484751818055569792750605282670056114 headline_margin_vs_tandon_d500=+0.00000215522287853839664150388745206844743910623919 all_records_beaten=True time=0.1s
RESULT G5 Definition 2 axioms all verified exhaustively; profile (367, 8, 367, 322, 26, 19)
RESULT BPZ Lean C7 schedule known answer reproduced: d=500, 257 digits
RESULT set-level test passed: Lemma 1, Theorem 1, sigma, Phi, S3b, K4a on explicit sets
RESULT box-level axioms verified: I15, I30++ independent; dimension-15 private pairs; condition (33) for Xhat30 at dimension 30 (zero words in both neighbourhoods); J30++ independent as an automorphic image of I30++ time=41s
RESULT certificates re-derived: C1=27488 C2=12839823 C3=14045805 C4=841760069965664 time=34s
ALL CHECKS PASS
sh verify-it-yourself/run_checks.sh  151.77s user 0.75s system 99% cpu 2:32.74 total
```
