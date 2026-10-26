# Claim

**Claim (one sentence):** the recursive construction specified by object/schedule.json (with the substitution tables and terminal codes in object/rules.json) is a recursion that gives an independent set of size M (288 digits, written out in the contributor's JSON) in C_7^{box 560}, hence Theta(C_7) >= M^(1/560) = 3.25883477557614484751818055569792750605282670056114, which is strictly greater than Tandon's d=500 value 3.25883262035326630912153905181047543760538759432195 (the top entry of 9a.md), by the exact margin +0.00000215522287853839664150388745206844743910623919 (computed by verify-it-yourself/shannon_check.py in exact integer arithmetic).

**Target id:** `shannon-capacity-odd-cycles`

**Win claimed:** full win (the bank's success_criterion below). No partial win is claimed.

## Bank statement (verbatim, bank/targets.json at origin/main commit 69e90f785b77, status_checked 2026-10-03)

An independent set S in the strong product C_m^{⊠d} gives Theta(C_m) >= |S|^(1/d). Improve the best known lower bound for Theta(C_m), m odd. For C7 this is Ben Green's open problem #38 (formal-conjectures GreensOpenProblems/38.lean): the largest A in F_7^d with (A-A) ∩ {-1,0,1}^d = {0}. Tao's optimization-constants repo lists Theta(C7) as constant C_9 (constants/9a.md). As of 2026-10-03: Theta(C7) >= 3.25883262... (Ravi Tandon, arXiv:2608.30273, 31 Aug 2026, heterogeneous recursion in C7^{⊠500}; cited on 9a.md under the key [Tan2026]), with other 2026 C7 values 3.25878915 (Gao, arXiv:2607.27869), 3.25880537 (Buys-Polak-Zuiddam, Lean-verified, arXiv:2607.29681) and 3.2580207 (Itty-Rosin-Carstensen-Reichman, 134,753 in C7^{⊠10}, arXiv:2607.21517). Buys-Polak-Zuiddam also give C11 >= 5.294502522, C13 >= 6.302455083, C15 >= 7.301600534, C19 >= 9.357192706, C21 >= 10.342455853, C23 >= 11.328224258, superseding Itty et al. X-evolve found an independent set of size 19,946 in C15^{⊠5}. The published alpha(C7^{⊠5}) baseline is 367 (Polak-Schrijver 2018, arXiv:1808.07438). EinsteinArena hosts 'Shannon Capacity C7^5: find 368 words' (arena best 367). Because 368^(1/5) ~ 3.259639 > 3.25883262 (equivalently record^5 ~ 367.545 < 368), a 368-element independent set in C7^{⊠5} would itself beat the capacity record; 367^(1/5) ~ 3.257866 does not.

## Success criterion (verbatim)

Capacity record: an explicit independent set S in C_m^{⊠d} (m odd; pairwise non-adjacent, verified exhaustively), or a fully specified recursive construction whose every finite ingredient is explicitly listed and verified and whose limiting rate is independently re-derived, giving a lower bound on Theta(C_m) (|S|^(1/d), computed with mpmath to 30 digits) STRICTLY GREATER (direction: max) than the best lower bound for that m at verification time: the max over the live primary table https://github.com/teorth/optimizationproblems/blob/main/constants/9a.md (C7 table; the other odd cycles are in its comments), arXiv:2608.30273, 2607.29681, 2607.27869, 2607.21517 and any newer arXiv result, using the record's exact digits. A finite-dimension set must beat the asymptotic record itself, not just an earlier fixed-dimension value. Against the 2026-10-03 C7 record 3.25883262... (recompute against the live record) this means |S| >= 368 in d=5, >= 1198 in d=6, >= 3904 in d=7, >= 12,721 in d=8, >= 41,454 in d=9, or >= 135,090 in d=10. In particular a verified 368-element independent set in C7^{⊠5} (the EinsteinArena target) IS a full capacity record, since 368^(1/5) ~ 3.259639 > 3.25883262; 367 (Polak-Schrijver 2018) gives only 3.257866. A fixed-d independence-number record below these thresholds is not claim-level.

## Status source and primary sources named by the bank

status_source: https://arxiv.org/abs/2608.30273

Primary table: https://github.com/teorth/optimizationproblems/blob/main/constants/9a.md

Primary sources:
- https://arxiv.org/abs/2608.30273
- https://arxiv.org/abs/2607.21517
- https://arxiv.org/pdf/2607.29681
- https://teorth.github.io/optimizationproblems/
- https://einsteinarena.com/
- https://arxiv.org/abs/2607.27869
- https://github.com/teorth/optimizationproblems/blob/main/constants/9a.md
- https://github.com/nathanielitty/lower-bounds-for-shannon-capacity
- https://github.com/xyz2606/recursive_construction_of_the_Shannon_capacity_of_C_7
- https://github.com/spectra-research/shannon-capacity-lean
- https://github.com/tandonravi/C7-Shannon-Capacity-Heterogeneous-Recursion
- https://arxiv.org/abs/2607.29681
- https://github.com/google-deepmind/formal-conjectures/blob/main/FormalConjectures/GreensOpenProblems/38.lean

## What the object is

This is the criterion's second route: a fully specified recursive construction, not an explicit set. The recursion defines an independent set in a strong power of the cycle; the checker recomputes its exact size from the definition and compares the resulting rate with the records.

The construction, in words (details and proofs in DERIVATION.md):

- Base: the 367-word independent set of Polak and Schrijver in C_7^{box 5}, as the Gao gadget G5 with profile (a,t,s,o,h,v) = (367, 8, 367, 322, 26, 19), taken from the BPZ Lean data.
- Tandon's gadgets: ordinary Gao products G10, G10A, G10D (d=10), the heterogeneous G15 gadgets (d=15), and the thirty-dimensional left gadget G30L = Gao(G15AX, sigma(G15Ah)) with its heterogeneous codebooks Xhat30 (the auxiliary set of Gh30) and J30++ (certified by C4). These are exactly the left-hand data of Tandon's G55.
- New top level: S3b(Phi(P0), Phi(P1), Phi(P2)) followed by the terminal code K4a on four copies, where P0 = HetGao(G30L, G10) (d=40), P1 = sigma(HetGao(G30L, R30)) with R30 = sigma(HetGao(G15AX, G15Dh)) (d=60), P2 = sigma(HetGao(G30L, G10D)) (d=40). The three vectors have dimensions 40, 60, 40, so the inner representation lies in C_7^{box 140} and the final set in C_7^{box 560}. In Tandon's d=500 construction the same top level S3b is applied to (n6, n11, n8) of dimensions 30, 55, 40 (sum 125).
- Final integer M has 288 digits, d = 560.

## Result

```
RESULT C7 d=560 M_digits=288 bound=3.25883477557614484751818055569792750605282670056114 headline_margin_vs_tandon_d500=+0.00000215522287853839664150388745206844743910623919 all_records_beaten=True time=0.1s
```

Runtime of the checker on this machine: 0.1s. The margin is the difference of the two 50-digit certified floors of the roots; the exact integer test (new bound strictly above the record) is also printed by the checker.

## Files in this folder

- `object/schedule.json`: the recursion DAG. The object has no explicit list of words: the set has about 10^287 elements and is defined by this finite recursion.
- `object/rules.json`: the label separation relation (22 ordered pairs), and the substitution tables and terminal codes the schedule uses, as data transcribed from the BPZ Lean sources (sha256 of the sources in table-record/README.md).
- `object/argon_shannon_certificates.json`: the contributor's file, copied byte for byte (sha256 in INDEX.csv). It holds the claimed integers for all six cycles; the checker reads only the entry for this cell (C7, key new_record_best) and compares.
- `verify-it-yourself/shannon_check.py`: the standard-library checker, written from the definitions (identical in the six sibling folders). `verify-it-yourself/run_checks.sh` runs it and the further checkers with four negative controls. `verify-it-yourself/RECEIPTS.md` has the real output.
- `table-record/`: the records the claim is compared against, with URL, UTC fetch time, HTTP status and sha256; `records.json` holds the exact integers; `9a_excerpt.md` is the relevant excerpt of 9a.md.
- `object/base_g5.json`: the 367-word base gadget G5 as data (5,399 bytes). `object/cert_input.json`: Tandon's automorphism T, the eight exchanges and the published certificate and table values the derivation is compared with. `object/bpz_lean_c7_schedule.json`: the BPZ Lean C7 schedule.
- `verify-it-yourself/check_g5.py`, `check_box_axioms.py`, `derive_certificates.py`, `set_level_test.py`, `bpz_lean_c7_check.py`, `c7_lib.py`: the further checkers described below (standard library only).
- `REPRODUCE.md`: commands to re-check from a clean copy.
- `INDEX.csv`: target, cell, value, table value, fetch time, file, sha256.
- `DERIVATION.md`: the written derivation that the schedule is valid under Tandon's Lemma 1 and Theorem 1, the known-answer test, and the C1 to C4 certificates with how each was obtained.

## What is verified inside this folder, and what is not

Verified here, by code in verify-it-yourself/ that uses only the standard library and was written from the definitions (the output is in verify-it-yourself/RECEIPTS.md; `sh verify-it-yourself/run_checks.sh` runs all of it in about two and a half minutes):

1. The base gadget G5 (object/base_g5.json, 367 + 367 words and 8 private pairs, transcribed as data from the BPZ Lean file BaseC7Data.lean): every axiom of Definition 2 of Tandon's paper, exhaustively (check_g5.py): I and X independent over all 67,161 pairs each, each private pair has its centre in I and its private neighbour confusable with exactly that one word of I, the 16 endpoints are distinct, P^H and P^V are complementary independent transversals, X meet N(P^H) meet N(P^V) is empty, and the profile is (367, 8, 367, 322, 26, 19).
2. The finite certificates (derive_certificates.py, about 33s). C1 = 27,488, C2 = 12,839,823, C3 = 14,045,805 and C4 = 841,760,069,965,664 are each re-derived from their definitions in Tandon's paper (Table 4 and Appendix B) starting from G5 alone: the sets G10, J+ (with the eight exchanges of eq. 152, independence checked exhaustively at 134,753 words), I15, J15, the auxiliary sets of the ordinary and heterogeneous 15-dimensional gadgets, I30++, J30++ and the neutral reference set X30^{0,L} of the left gadget G30L. The neutral parts are computed from the transversals, class by class, not taken from a formula. All four values agree with Tandon's Table 4, all seven component contributions of C4 agree with his Table 5, and the sizes of every auxiliary class agree with his Table 6(a). C2 is also obtained by a word-by-word enumeration of all 49,495,055 words of J15. Tandon's own script (verify_certificates.py in his repository at head c753408492dd) was not used; it gives the same four values (the orchestrator's triage ran it), so the two computations agree.
3. A set-level test (set_level_test.py, about a minute) of Lemma 1, Theorem 1, the orientation reversal sigma, the map Phi, the rule S3b and the terminal code K4a on real vertex sets in C_7^n for n at most 9. It builds, in the configuration of the object, a left gadget L with heterogeneous codebooks (J0, JH, JV) and three right gadgets (one a Theorem 1 output, as R30 is in the object), forms P0, sigma(P1), sigma(P2) by Theorem 1, converts to seven-family representations by Phi, applies S3b from object/rules.json, and checks by brute force that every output family is independent, every separated pair of output families is separated, and every size equals the cardinality formula. Two configurations: a one-dimensional left gadget (families in C_7^7) and a two-dimensional left gadget built the way the object builds G30L, with J0 taken from the sibling gadget over the same ordered pair (families in C_7^9). K4a is checked on four copies of a base representation (100 words in C_7^4, independent).
4. Known answers: Tandon's own d=500 integer and bound (shannon_check.py) and, as a further known answer, the BPZ Lean C7 schedule transcribed from CertC7.lean (object/bpz_lean_c7_schedule.json, bpz_lean_c7_check.py): its integer (257 digits, d=500) equals the integer defined in the Lean source, and Definition 6 holds for the tables and the code it uses.
5. As before: Definition 6 for S3b and K4a, the exact recomputation of M (288 digits) and d = 560, and strict exceedance over every record by exact integer comparison.

6. Box-level exhaustive checks of the large gadgets (check_box_axioms.py, about 40 s). Every large set is a finite union of products of explicit factors (dimension 10 and 5); each factor is checked independent word by word, and each pair of boxes is checked separated in some factor. In this way:
   - I15 (49,495,055 words), hence J15 = T^3(I15), is independent; so are PH15, PV15, the ordinary auxiliary set X10 x X5, X15het (eq. 156) and X15^{A,het}.
   - The private-pair property of G15 = Gao(G10, G5) holds at dimension 15: for all 2,504,616 private neighbours q, q is confusable with exactly one word of I15 (its centre r, which lies in I15 and is confusable with q), and the endpoints are distinct.
   - I30++ (2,455,726,444,728,097 words as 61 four-factor boxes, 1,830 box pairs), hence J30++ = T^6(I30++), is independent (T is an automorphism).
   - Condition (33) at dimension 30: Xhat30 (2,444,076,335,041,121 words, 138 four-factor boxes, independent) meets N(P^H) and N(P^V) of G30L = Gao(G15AX, sigma(G15Ah)) in no common word (0 words), using the transversals PH = (PH15A x V0) u (U0 x PH15A), PV = (PV15A x V0) u (U0 x PV15A) from eq. (18); its class sizes relative to G30L are (1,435,184,942,161,465; 420,235,140,891,852; 588,656,251,987,804), as in the paper. The ordinary auxiliary set of G30L also satisfies the axiom, with classes (1,446,768,903,083,453; 420,235,140,891,852; 576,488,425,905,496), as in eq. (129). J30++ (used in the JH and JV positions) needs only independence, which is the previous item.

Not verified inside this folder as theorems: the composition theorems used as published results, namely Tandon's Lemma 1 (Gao's product lemma), Theorem 1 (heterogeneous refinement) and Proposition 1 (BPZ combining rules, with the S3b step at dimension 140 and the K4a step at dimension 560 as instances of it). They are used as published results; their formulas are re-derived in DERIVATION.md and each is instance-tested on real vertex sets in item 3 and, for the actual large gadgets, through the axioms checked in items 1, 2 and 6 (the hypotheses of the theorems hold for the actual sets). The final set in C_7^560 itself is not enumerated.

Inputs taken as stated and checked only indirectly: the definitions of J+, J15, J30++ and the assignment of codebooks to classes are read from the paper (every class size and every number of Tables 4 to 6 is reproduced from them); the base data was transcribed from the BPZ Lean file (the Definition 2 check in item 1 does not depend on Lean).

## Provenance

Found on 2026-10-18/19 by the author's team (an AI search agent, Gemini "Argon", working for the contributor calgulbenkian). Checked by the orchestrator's triage agent with its own checker on 2026-10-19 (c7.py and c7_argon.py, plus gadget_sets.py/test_sets.py for set-level tests of Lemma 1, Theorem 1 and the rules); the triage recomputed the integer and the 50-digit root and found them equal to the contributor's. This is a new find, not a refile of an earlier pull request.

## Credits (names and titles as given on the arXiv abstract pages fetched for this folder)

- Ravi Tandon, "Strengthening Recursive Constructions for Zero-Error Shannon Capacity", arXiv:2608.30273, v1 submitted 31 Aug 2026: the Gao-gadget calculus used here (Lemma 1, Theorem 1, the profile map Phi), the heterogeneous refinement, the finite certificates C1 to C4, and the C7 record at d=500. Companion code and certificates: the repository tandonravi/C7-Shannon-Capacity-Heterogeneous-Recursion (head c753408492dd, 2026-08-31).
- Pjotr Buys, Sven Polak and Jeroen Zuiddam, "Lean-verified lower bounds for the Shannon capacity of odd cycles", arXiv:2607.29681, submitted 31 Jul 2026: the seven-family framework, the combining rules S2a to S3h, the terminal codes K3a, K4a, K4b, the base port systems, and the Lean 4 formalisation (repository spectra-research/shannon-capacity-lean, head aa21eeb12b75). Every schedule here is built in their grammar.
- Yu Gao, "A Recursive Construction Improving the Lower Bound on the Shannon Capacity of C_7", arXiv:2607.27869, submitted 30 Jul 2026: the gadget and product lemma that the later work generalises.
- Nathaniel Itty, Christopher D. Rosin, Chase Carstensen and Daniel Reichman, "Improved lower bounds for the Shannon capacity of odd cycles", arXiv:2607.21517 (submitted 23 Jul 2026, last revised 30 Jul 2026): the 134,753-word set in C7^10 on which Gao's construction builds.
- Sven Polak and Alexander Schrijver, "New lower bound on the Shannon capacity of C7 from circular graphs", Information Processing Letters 143 (2019), arXiv:1808.07438: the 367-word independent set in C7^5 that is the base of the C7 gadgets.

## Corrections to the contributor's own write-up (RESULTS.md of the snapshot)

The contributor's JSON (object/argon_shannon_certificates.json, shipped byte for byte) is correct and agrees with the checker to the last digit. Its prose has errors that the orchestrator's triage listed; none changes the claimed integer. They are corrected here and the panel should not rely on the prose:

- Titles and date. Tandon's paper is "Strengthening Recursive Constructions for Zero-Error Shannon Capacity" (arXiv:2608.30273, submitted 31 Aug 2026), not a paper on heterogeneous product constructions submitted on 30 Aug. The Buys-Polak-Zuiddam paper is "Lean-verified lower bounds for the Shannon capacity of odd cycles" (arXiv:2607.29681, submitted 31 Jul 2026); the title "Recursive constructions of independent sets in strong powers of graphs" given to it in the prose is not its arXiv title. Gao's paper is "A Recursive Construction Improving the Lower Bound on the Shannon Capacity of C_7" (arXiv:2607.27869, submitted 30 Jul 2026).
- The "9a.md baseline" for C7 in the prose is 3.258805326092. The live 9a.md has the BPZ value 3.258805369885 and, on top, the Tandon value 3.25883262. For C11 to C23 the 9a.md comment values (BPZ version 1) are older and lower than the Lean repository head values; this folder compares against both.
- Codebook sizes (C7 only): the prose gives |Xhat30| = 197,884,335,705,225 and j30++ = 219,024,043,669,249. These cannot be right (q30++ = C4 = 841,760,069,965,664 would exceed them). Tandon's values are j(Xhat30) = 2,444,076,335,041,121 and |J30++| = 2,455,726,444,728,097. The prose also calls Xhat30 a subset of the neutral part X30^{0,L}; it is not (its h0 = 420,235,140,891,852 and v0 = 588,656,251,987,804 are nonzero). The profiles of the three branches in the JSON come out of the correct values.
- RESULTS.md decimals: none: the text of RESULTS.md for C7 matches the exact value to all 50 digits.
- The prose says every construction was checked by a script at a path on the contributor's machine. That script is not part of this folder and is not used; the checker here was written from the definitions.

## Open questions for the panel

1. The certificates are derived twice, by Tandon's script (run by the orchestrator's triage) and by the independent code in this folder, with the same four values; the first derivation of C2, C3 and C4 outside Tandon's own repository is the code here. Does the reproduce skeptic find any definition (J+, J15, J30++, the reference set X30^{0,L}, or the class assignment of codebooks) that the code here reads from the paper in a way the paper does not intend? Both derivations take those definitions from the same paper.
2. Lemma 1, Theorem 1 and Proposition 1 are used as published results (Theorem 1 is from a single-author version-1 preprint). They are re-derived in DERIVATION.md, instance-tested on real sets, and every hypothesis and conclusion they are used for is checked on the actual large gadgets at box level (item 6). Is that enough, or does the panel want the proof of Theorem 1 re-examined?
3. The three new branches reuse Tandon's left gadget G30L and its codebooks (Xhat30, J30++) and change only the right-hand gadget (G10, R30, G10D). Condition (33) for Xhat30 against G30L is now checked directly at dimension 30. Is there any further hypothesis on the right-hand gadget that Theorem 1 needs and that the three right gadgets fail?
4. Strictly greater than what? The bank asks to beat the maximum over the live 9a.md and every newer arXiv result. 9a.md shows Tandon's 3.25883262 (8 decimals); the comparison uses Tandon's exact d=500 integer, which the checker recomputes. Is a comparison of the d=560 value against the d=500 value acceptable (both are lower bounds of the form M^(1/d))?
5. A simpler variant, S3b(n6, n11, n11) with K4a at d=560 on Tandon's own gadgets (value 3.25883436223771079435326297235859444166490482822313), also beats Tandon; the contributor's JSON lists it as new_record_simple. It is not the object claimed here.
6. The record cascade moves every few weeks (five C7 records in July and August 2026). Nothing newer than Tandon's version 1 was seen on 2026-10-20 (02:53 UTC). Please re-fetch 9a.md and arXiv before filing.
