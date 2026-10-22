# Derivation: the 3-branch S3b object with Tandon's 30-dimensional left gadget

This note shows why the object in object/schedule.json is a valid independent set in C_7^{box 560}, using only Lemma 1 (Gao's product lemma), Theorem 1 (Tandon's heterogeneous refinement) and Proposition 1 with Definition 6 (the BPZ combining rules), as stated in Tandon's arXiv:2608.30273 (version 1, 31 Aug 2026). Equation numbers below are the paper's. The checker (verify-it-yourself/shannon_check.py) recomputes every number in the tables; what it cannot do, and this note cannot do, is replace the proofs of Lemma 1 and Theorem 1 or the neighbourhood counts C1 to C4 (see section 6).

## 1. Definitions used

Write u ~ v when u = v or u, v are adjacent in the graph (confusable), N(S) for the closed neighbourhood of S, and Y perp Z (separated) when no vertex of Y is confusable with a vertex of Z.

A Gao gadget in a graph G (Definition 2) is: an independent set I; t pairwise endpoint-disjoint private pairs (r_i, q_i) for I (r_i in I, q_i not in I, N(q_i) meets I only in r_i); two independent sets P^H, P^V that are complementary transversals of the pairs; and an independent auxiliary set X with X intersect N(P^H) intersect N(P^V) empty. With R = {r_i}, B = I minus R, the auxiliary set splits as X = X^0 + X^H + X^V (not confusable with either transversal, confusable with P^H only, with P^V only). Its profile is pi = (a, t, s, o, h, v) = (|I|, t, |X|, |X^0|, |X^H|, |X^V|), with o + h + v = s. Reversing the orientation (swap P^H and P^V) gives sigma(G) with profile (a, t, s, o, v, h) (eq. 79).

Lemma 1 (Gao): for gadgets G1 in G_1 and G2 in G_2, I12 = (B1 x B2) union A^H union A^V is independent in G_1 boxtimes G_2 and, with auxiliary set X1 x X2 and propagated pairs and transversals (eqs 17, 18), forms a gadget Gao(G1, G2) with profile (eqs 21):
a12 = (a1-t1)(a2-t2) + t1 s2 + s1 t2, t12 = t1 o2 + o1 t2, s12 = s1 s2, o12 = o1 o2 + (h1+v1)(h2+v2), h12 = h1 o2 + o1 v2, v12 = v1 o2 + o1 h2.

Theorem 1 (Tandon): let G_L, G_R be Gao gadgets and let I_LR, the pairs and the transversals P_LR^H, P_LR^V be those of Gao(G_L, G_R). Let J0, JH, JV be independent sets in G_L (the left graph), with J0 intersect N(P_L^H) intersect N(P_L^V) empty (eq. 33). Put J0 = J0^0 + J0^H + J0^V relative to the two left transversals (eq. 34); j0, o0, h0, v0 are the sizes of J0 and of its three parts, jH = |JH|, jV = |JV|, qH = |JH minus N(X_L^0)|, qV = |JV minus N(X_L^0)| (eq. 35). Then the auxiliary set (J0 x X_R^0) + (JH x X_R^H) + (JV x X_R^V) (eq. 36) is independent, is confusable with no vertex of both transversals (eq. 37), and together with the unchanged code, pairs and transversals forms a gadget HetGao(G_L, G_R) with a and t as in Lemma 1 and
s = j0 oR + jH hR + jV vR, o = o0 oR + qH hR + qV vR, h = h0 oR + (jV - qV) vR, v = v0 oR + (jH - qH) hR (eqs 38, 39).
Every hypothesis of Theorem 1 is a statement about the left graph, the left gadget and the three codebooks. The right gadget enters the conclusion only through its profile (aR, tR, sR, oR, hR, vR) and through the fact that X_R is an independent set split into X_R^0, X_R^H, X_R^V (the proof, section 2.3 of the paper, uses nothing else about G_R). The checker's function hetgao is eqs (38), (39) and its assertion is o0 + h0 + v0 = j0, 0 <= qH <= jH, 0 <= qV <= jV.

BPZ framework (Definitions 4 to 6, Proposition 1): a seven-family representation of a graph has independent sets F_B, F_N, F_A, F_D, F_O, F_H, F_V with F_lambda perp F_mu whenever lambda perp mu (the relation of Definition 4; the checker compares object/rules.json with it). A gadget gives one by Phi(a,t,s,o,h,v) = (a-t, o, v, h, t, t, t) (eq. 77; Table 2 of the paper shows the eleven separations follow from the gadget axioms). An m-ary rule T is admissible (Definition 6) if (i) distinct tuples in one T_lambda are separated in some coordinate and (ii) for lambda perp mu, every tuple of T_lambda is separated from every tuple of T_mu in some coordinate. Proposition 1: for representations F(i) in G^{box d_i} the output families are a representation in G^{box (d_1+...+d_m)} with sizes sum over tuples of products of the input sizes. The inputs may have different dimensions d_i; the proof uses only the coordinatewise product. A terminal code is a set of m-tuples pairwise separated in some coordinate; it produces a single independent set of size sum over tuples of products.

## 2. The object

The object is: P0, P1, P2 as below, n = S3b(Phi(P0), Phi(P1), Phi(P2)) (a seven-family representation in C_7^{box 140} by Proposition 1 and the admissibility of S3b, which the checker verifies from the table), and the independent set of size M = K4a(n, n, n, n) in C_7^{box 560} (the terminal code K4a, 49 words, pairwise separated; checked).

- P0 = HetGao(G30L, G10) with codebooks (Xhat30, J30++, J30++), dimension 30 + 10 = 40.
- P1 = sigma(HetGao(G30L, R30)) with the same codebooks, where R30 = sigma(HetGao(G15AX, G15Dh)) with codebooks (X15^{A,het}, J15, J15), dimension 30 + 30 = 60.
- P2 = sigma(HetGao(G30L, G10D)) with the same codebooks, dimension 30 + 10 = 40.

## 3. Why each step is valid

Left-hand data. G30L = Gao(G15AX, sigma(G15Ah)) is the thirty-dimensional left gadget of Tandon's own step 4 (eq. 128, profile (2,455,716,185,820,961, 176,941,111,954,464, 2,443,492,469,880,801, 1,446,768,903,083,453, 420,235,140,891,852, 576,488,425,905,496)). Tandon uses it as the left gadget of G55 = HetGao(G30L, G25R) with J0 = Xhat30 (the auxiliary set of the sibling gadget Gh30 = HetGao(G15AX, sigma(G15Ah)) with codebooks (X15^{A,het}, J15, X15^X) over the right auxiliary set X15^{D,het}; eq. 130 and Table 6(b), where JV = X15^X has size 49,430,863 and q = 14,088,465) and JH = JV = J30++ = T^x6(I30++) (eqs 136 to 139). The hypotheses of Theorem 1 for (G30L; J0, JH, JV) are therefore exactly those Tandon establishes for G55:
- J0 = Xhat30 is independent and satisfies eq. (33) because Gh30 and G30L are formed from the same ordered pair of input gadgets, so they have the same product code, propagated private pairs and transversals, and Xhat30 is the auxiliary set of a gadget on those transversals (paper, Step 4, eq. 132); its decomposition relative to the transversals of G30L is (j0, o0, h0, v0) = (2,444,076,335,041,121; 1,435,184,942,161,465; 420,235,140,891,852; 588,656,251,987,804);
- JH = JV = J30++ is independent (an automorphic image T^x6 of the main code I30++ of the ordinary product Gao(G15het, G15het), Lemma 1) of size 2,455,726,444,728,097, and its count q = |J30++ minus N(X30^{0,L})| = C4 = 841,760,069,965,664 is the certificate.
None of this depends on the right-hand gadget. In all three new branches these data are reused unchanged.

Right-hand gadgets. Theorem 1 needs G_R to be a Gao gadget in C_7^{box d_R}. The three right gadgets are:
- G10 = Gao(G5, G5), a gadget by Lemma 1 (the base G5 is the BPZ/Polak-Schrijver gadget of profile (367, 8, 367, 322, 26, 19)); it is the right gadget in Tandon's own G15 steps.
- G10D = Gao(G5, sigma(G5)), a gadget by Lemma 1, used by Tandon as the right gadget of G25 (eq. 120).
- R30 = sigma(HetGao(G15AX, G15Dh)(X15^{A,het}, J15, J15)). The inner HetGao has left gadget G15AX = Gao(G10A, G5) and codebooks (X15^{A,het}, J15, J15) which are exactly Tandon's codebooks for his own G25 (eq. 120, left gadget G15AX, J0 = X15^{A,het}, JH = JV = J15 with certificate C2 = |J15 minus N(X15^{0,X})| = 12,839,823); only the right gadget differs (G15Dh, itself the output of Theorem 1 in Tandon's eq. 111, instead of G10D). By the remark above Theorem 1 holds for it, and Theorem 1's conclusion says its output is again a Gao gadget, so sigma of it is a Gao gadget and may serve as the right gadget of the next application. Tandon himself feeds a Theorem 1 output into the right slot of another Theorem 1 (G40 = HetGao(G15DX, G25), with G25 a Theorem 1 output).

So each of P0, P1, P2 is a Gao gadget (apply sigma after Theorem 1 where marked; sigma only exchanges P^H and P^V) in C_7^{box 40}, C_7^{box 60}, C_7^{box 40} with the profile that the checker computes from eqs (38), (39) below.

Top level. Phi gives a seven-family representation for each of the three gadgets (Table 2); S3b is admissible (checked here by Definition 6 on the 45-word table); Proposition 1 applies to inputs of dimensions 40, 60, 40 and yields a representation in C_7^{box 140} with the sizes the checker computes; K4a is a terminal code (checked) so the final set is an independent set in C_7^{box 560} of size M. Hence Theta(C_7) >= M^(1/560).

## 4. The numbers, step by step (computed by the checker; also printed in verify-it-yourself/RECEIPTS.md)

Certificates used as inputs: C1 = 27,488, C2 = 12,839,823, C3 = 14,045,805, C4 = 841,760,069,965,664. Changing C1, C2 or C4 by 1 changes the final integer M of this object; changing C3 does not (C3 enters only Tandon's own n8 and n11 vectors, used in the known-answer test).

| Gadget | Construction | dim | profile (a, t, s, o, h, v) |
|---|---|---|---|
| sG5 | sigma(G5) | 5 | (367, 8, 367, 322, 19, 26) |
| G10 | Gao(G5, G5) | 10 | (134,753, 5,152, 134,689, 105,709, 14,490, 14,490) |
| G10A | Gao(sG5, G5) | 10 | (134,753, 5,152, 134,689, 105,709, 12,236, 16,744) |
| G10D | Gao(G5, sG5) | 10 | (134,753, 5,152, 134,689, 105,709, 16,744, 12,236) |
| G15X | Gao(G10, G5) | 15 | (49,495,055, 2,504,616, 49,430,863, 35,342,398, 6,674,251, 7,414,214) |
| G15h | HetGao(G10, G5); J0 = the auxiliary set of G10 (its counts (s,o,h,v)); JH = a code of size a(G10) with certified count C1; JV = a code of size a(G10) with certified count C1 | 15 | (49,495,055, 2,504,616, 49,433,743, 35,275,258, 6,703,815, 7,454,670) |
| G15AX | Gao(G10A, G5) | 15 | (49,495,055, 2,504,616, 49,430,863, 35,342,398, 5,948,463, 8,140,002) |
| G15Ah | HetGao(G10A, G5); J0 = the auxiliary set of G10A (its counts (s,o,h,v)); JH = a code of size a(G10) with certified count C1; JV = the full auxiliary set X of G10A, with q = s - o | 15 | (49,495,055, 2,504,616, 49,432,527, 35,303,606, 5,948,463, 8,180,458) |
| G15DX | Gao(G10D, sG5) | 15 | (49,495,055, 2,504,616, 49,430,863, 35,342,398, 8,140,002, 5,948,463) |
| G15Dh | HetGao(G10D, sG5); J0 = the auxiliary set of G10D (its counts (s,o,h,v)); JH = the full auxiliary set X of G10D, with q = s - o; JV = a code of size a(G10) with certified count C1 | 15 | (49,495,055, 2,504,616, 49,432,527, 35,303,606, 8,180,458, 5,948,463) |
| G30_6 | HetGao(G15X, G15h); J0 = the auxiliary set of G15h (its counts (s,o,h,v)); JH = a code of size a(G15X) with certified count C2; JV = a code of size a(G15X) with certified count C2 | 30 | (2,455,719,231,434,017, 176,870,111,100,096, 2,444,563,032,022,369, 1,426,136,268,314,719, 509,731,462,042,710, 508,695,301,664,940) |
| G25_8 | HetGao(G15AX, G10D); J0 = the auxiliary set of G15Ah (its counts (s,o,h,v)); JH = a code of size a(G15X) with certified count C2; JV = a code of size a(G15X) with certified count C2 | 25 | (6,682,019,915,439, 446,844,487,240, 6,659,829,690,543, 4,104,006,957,194, 1,077,319,494,019, 1,478,503,239,330) |
| G40_8 | HetGao(G15DX, G25_8); J0 = the auxiliary set of G15Dh (its counts (s,o,h,v)); JH = a code of size s(G15h) with certified count C3; JV = a code of size a(G15X) with certified count C2 | 40 | (331,761,855,244,358,723,969, 26,071,517,201,241,409,024, 329,305,968,864,222,045,505, 179,001,784,071,649,220,449, 87,767,535,795,425,989,412, 62,536,648,997,146,835,644) |
| sG15Ah | sigma(G15Ah) | 15 | (49,495,055, 2,504,616, 49,432,527, 35,303,606, 8,180,458, 5,948,463) |
| G30L | Gao(G15AX, sG15Ah) | 30 | (2,455,716,185,820,961, 176,941,111,954,464, 2,443,492,469,880,801, 1,446,768,903,083,453, 420,235,140,891,852, 576,488,425,905,496) |
| Gh30 | HetGao(G15AX, sG15Ah); J0 = the auxiliary set of G15Ah (its counts (s,o,h,v)); JH = a code of size a(G15X) with certified count C2; JV = the full auxiliary set X of G15X, with q = s - o | 30 | (2,455,716,185,820,961, 176,941,111,954,464, 2,444,076,335,041,121, 1,435,184,942,161,465, 420,235,140,891,852, 588,656,251,987,804) |
| Gh25 | HetGao(G15AX, G10D); J0 = the auxiliary set of G15Ah (its counts (s,o,h,v)); JH = a code of size a(G15X) with certified count C2; JV = a code of size s(G15h) with certified count C3 | 25 | (6,682,019,915,439, 446,844,487,240, 6,659,079,476,911, 4,118,763,352,946, 1,061,812,884,635, 1,478,503,239,330) |
| G25R | sigma(Gh25) | 25 | (6,682,019,915,439, 446,844,487,240, 6,659,079,476,911, 4,118,763,352,946, 1,478,503,239,330, 1,061,812,884,635) |
| Gpp30 | Gao(G15h, G15h) | 30 | (2,455,726,444,728,097, 176,701,951,181,856, 2,443,694,946,990,049, 1,444,806,524,461,789, 499,444,211,264,130, 499,444,211,264,130) |
| G55 | HetGao(G30L, G25R); J0 = the auxiliary set of Gh30 (its counts (s,o,h,v)); JH = a code of size a(Gpp30) with certified count C4; JV = a code of size a(Gpp30) with certified count C4 | 55 | (16,478,688,413,981,213,775,272,008,847, 1,375,259,276,200,664,518,625,890,664, 16,304,893,524,159,967,980,117,037,071, 8,049,523,822,718,249,447,032,963,650, 3,444,579,390,015,851,502,852,512,947, 4,810,790,311,425,867,030,231,560,474) |
| P0 | HetGao(G30L, G10); J0 = the auxiliary set of Gh30 (its counts (s,o,h,v)); JH = a code of size a(Gpp30) with certified count C4; JV = a code of size a(Gpp30) with certified count C4 | 40 | (331,752,422,981,032,566,145, 26,158,021,392,280,384,832, 329,527,817,669,082,110,849, 176,106,171,878,551,246,405, 67,809,009,278,844,437,238, 85,612,636,511,686,427,206) |
| R30h | HetGao(G15AX, G15Dh); J0 = the auxiliary set of G15Ah (its counts (s,o,h,v)); JH = a code of size a(G15X) with certified count C2; JV = a code of size a(G15X) with certified count C2 | 30 | (2,455,716,185,820,961, 176,941,111,954,464, 2,444,458,178,778,017, 1,427,757,441,424,219, 428,044,485,365,994, 588,656,251,987,804) |
| R30 | sigma(R30h) | 30 | (2,455,716,185,820,961, 176,941,111,954,464, 2,444,458,178,778,017, 1,427,757,441,424,219, 588,656,251,987,804, 428,044,485,365,994) |
| P1h | HetGao(G30L, R30); J0 = the auxiliary set of Gh30 (its counts (s,o,h,v)); JH = a code of size a(Gpp30) with certified count C4; JV = a code of size a(Gpp30) with certified count C4 | 60 | (6,057,695,260,227,493,703,397,667,114,561, 508,621,887,739,588,144,587,762,647,808, 5,986,287,061,858,070,256,705,570,571,905, 2,904,914,064,800,094,180,917,939,512,707, 1,290,843,255,839,501,440,701,539,466,990, 1,790,529,741,218,474,635,086,091,592,208) |
| P1 | sigma(P1h) | 60 | (6,057,695,260,227,493,703,397,667,114,561, 508,621,887,739,588,144,587,762,647,808, 5,986,287,061,858,070,256,705,570,571,905, 2,904,914,064,800,094,180,917,939,512,707, 1,790,529,741,218,474,635,086,091,592,208, 1,290,843,255,839,501,440,701,539,466,990) |
| P2h | HetGao(G30L, G10D); J0 = the auxiliary set of Gh30 (its counts (s,o,h,v)); JH = a code of size a(Gpp30) with certified count C4; JV = a code of size a(Gpp30) with certified count C4 | 40 | (331,752,422,981,032,566,145, 26,158,021,392,280,384,832, 329,527,817,669,082,110,849, 176,106,171,878,551,246,405, 64,171,129,070,129,913,256, 89,250,516,720,400,951,188) |
| P2 | sigma(P2h) | 40 | (331,752,422,981,032,566,145, 26,158,021,392,280,384,832, 329,527,817,669,082,110,849, 176,106,171,878,551,246,405, 89,250,516,720,400,951,188, 64,171,129,070,129,913,256) |

Profiles marked in the schedule file with expect_profile are compared by the checker with the values printed in the paper (eqs 109, 112, 118, 122, 126, 129, 131, 134, 141 and Table 6(a)); all agree. The profiles of P0, P1, P2 and the 140-dimensional vector are compared with the contributor's JSON. The vector Phi(P0) etc. are then combined with S3b, and K4a is applied to four copies.

## 5. Known-answer test: Tandon's own d=500 integer

The same code (Lemma 1, Theorem 1, Phi, S3b, K4a) is run on Tandon's own schedule (his G30(6), G40(8), G55 and n6 = Phi(G30(6)), n8 = Phi(G40(8)), n11 = Phi(sigma(G55))) with C1 to C4 above. The checker asserts that it reproduces:
- n6, n8, n11, equal to eqs (119), (127), (142) of the paper;
- n25 = S3b(n6, n11, n8) and M500 = K4a(n25, n25, n25, n25), the 257-digit integer printed as Theorem 2 (eq. 106);
- the bound 3.2588326203532663091215390518104754376053875943219 (eq. 107);
and, as a second known answer, BPZ's own Lean C7 schedule (eq. 103, with S2a, S3a, S3b, K4a on w and sigma(w)), which reproduces the integer `def M` of CertC7.lean (3.258827985920007...). This tests the code paths (formulas, rules, ordering of arguments) against two independent published values before the new object is evaluated.

## 6. Certificates C1 to C4: values and how each was obtained

Each is a count of the form |J minus N(X0)| for an explicit independent set J and a reference neutral set X0 (Table 4 of the paper). They are the only inputs that are not derived from the profile formulas: they need set-level neighbourhood computations in C_7^10, C_7^15 and C_7^30.

| Certificate | Definition | Value | How it was obtained |
|---|---|---|---|
| C1 | q10 = abs(J+ minus N(X10^0)), J+ = (T x T)(I10) after eight exchanges (Appendix B.1) | 27,488 | Re-derived from the definitions by derive_certificates.py in this folder: 27,480 for (T x T)(I10) before the exchanges, 27,488 after; J+ checked independent exhaustively. Also re-derived by the triage's own code and by Tandon's script. |
| C2 | abs(J15 minus N(X15^{0,X})), J15 = (T x T x T)(I15) | 12,839,823 | Re-derived by derive_certificates.py (flag histograms over explicit factors, and a word-by-word enumeration of all 49,495,055 words of J15). Tandon's script gives the same value. |
| C3 | abs(X15 minus N(X15^{0,X})) | 14,045,805 | Re-derived by derive_certificates.py. Tandon's script gives the same value. Not used by this object (see section 4); used by Tandon's own n8, n11. |
| C4 | q30++ = abs(J30++ minus N(X30^{0,L})), J30++ = T^x6(I30++) | 841,760,069,965,664 | Re-derived by derive_certificates.py as the sum of the seven component contributions of Table 5 (B15 x B15: 827,599,599,610,592; R15 x X15^0: 6,686,131,598,464; P15^H x X15^H: 194,829,147,616; P15^V x X15^V: 194,829,147,616; X15^0 x R15: 6,694,533,241,984; X15^H x P15^V: 195,073,609,696; X15^V x P15^H: 195,073,609,696); each component agrees with Table 5. Tandon's script gives the same value. |

Method of derive_certificates.py (it does not use Tandon's code; Tandon's method is similar in spirit, because the problem forces it). Every set is described as a union of products of explicit factors of dimension 5 or 10 (for example I15 = (B10 x B5) + (R10 x X5^0) + (P10^H x X5^H) + (P10^V x X5^V) + (X10^0 x R5) + (X10^H x P5^V) + (X10^V x P5^H), by Lemma 1). The neutral part and the classes H and V of an auxiliary set are computed from the transversals (a word is in the class H if it is confusable with the H transversal only, and so on), using that a word (u, v) is in N(A x B) iff u is in N(A) and v is in N(B), and in N(union) iff in some N(part). The 10-dimensional neighbourhoods are computed exhaustively from explicit word lists (134,689 and 134,753 words), the 5-dimensional ones from the 367-word sets. For each explicit factor the code records, for every word after applying T, the pattern of memberships in the neighbourhoods of the reference factors, and multiplies the pattern counts of the two parts of a product; the count of words outside N(reference) is then exact. Checks along the way: all class sizes equal Tandon's Table 6(a) numbers, |I30++| = 2,455,726,444,728,097, |X30^{0,L}| = 1,446,768,903,083,453, and the C2 histogram count equals the word-by-word enumeration.

Comparison with Tandon's script (cited, not used): verify_certificates.py in the repository tandonravi/C7-Shannon-Capacity-Heterogeneous-Recursion at head c753408492dd (data/certificates.json sha256 c86f1db7687c3ed9e2a951d602671ce606f1b3830aa8ecf74b7ece069804ebd1) derives C1 = 27488, C2 = 12839823, C3 = 14045805, C4 = 841760069965664 in about 42 seconds (the orchestrator's triage ran it); the values equal those derived here. The ledger values are recorded in object/cert_input.json for comparison only.

## 7. What is and is not checked in this folder

Checked in exact integers or on explicit sets: the separation relation against Definition 4; Definition 6 for S2a, S3a, S3b and the pairwise separation of K4a; Lemma 1 / Theorem 1 profile arithmetic along the whole chain; the paper's printed profiles at 17 intermediate gadgets; Tandon's d=500 integer and bound; BPZ's C7 Lean integer (twice: from eq. (103) in code and from the transcribed Lean schedule); the contributor's profiles, 140-dimensional vector, integer M (288 digits) and degree 560; strict exceedance over eight records; every axiom of Definition 2 for G5; the four certificates; Lemma 1, Theorem 1, sigma, Phi, S3b and K4a on real vertex sets at small scale in the configuration of the object.

Also checked, at box level and exhaustively (check_box_axioms.py): independence of I15, I30++ (hence of J15 and J30++), PH15, PV15 and the auxiliary sets at dimension 15 and of Xhat30 at dimension 30; the private-pair property of G15 for all 2,504,616 pairs; and condition (33) for Xhat30 against both transversals of G30L at dimension 30 (zero words in both neighbourhoods), with the class sizes of the paper.

Not checked here (see CLAIM.md, "What is verified inside this folder, and what is not"): the proofs of Lemma 1, Theorem 1 and Proposition 1 as general theorems (used as published results; the formulas are re-derived above and instance-tested), and the enumeration of the final set in C_7^560.
