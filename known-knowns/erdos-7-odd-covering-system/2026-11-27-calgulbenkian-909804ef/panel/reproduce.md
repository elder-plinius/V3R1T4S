context: Claude Code subagent, fresh context [Opus 5.5]

# Reproduce report: odd coverings, lower bound L >= 6,557,114,959,770,375 (partial win p2)

Role: reproduce. Input: the package only. All 51 files matched the package's SHA-256 list before I started. Times are UTC on 2026-11-27 (work from 02:09 to 02:52).

## Short verdict

- I wrote my own checker before opening any of the package's checking code. It works from the definitions in object/PROOF.md (Sections 2, 4, 5.4 to 8.6, 9.4); I took only the file layout from verify-it-yourself/FORMAT.md. It recomputes every certificate row in exact rational arithmetic and redoes the whole enumeration. Its answer is PASS on all three items of PROOF.md Section 9.4, **in full, on every row of every file**. Nothing was sampled.
- Every stored number agrees exactly with my recomputation: all 738 `B_exact`, and all 29,485 pairs `R_exact`, `S_exact`.
- Afterwards I ran `sh verify-it-yourself/run_checks.sh` in a copy of the package: it prints PASS. Its exact outputs (least margins, largest B) are identical to mine.
- Determinism: a second run of the package script gave output identical apart from times, and a second run of my A8 check gave a byte-identical result.
- Refereeing PROOF.md line by line, I found every named lemma, proposition and theorem correct. There is one minor wording gap in Section 9.4, which does not affect the result (finding 1).

## The definition my checker implements (quoted)

Theorem 1 (object/PROOF.md, Section 0): "Every odd covering satisfies L >= 6,557,114,959,770,375 = 3^5 * 5^3 * 7^2 * 11^2 * 13^2 * 17 * 19 * 23 * 29."

object/PROOF.md Section 9.4: "(i) Scalar certificates. For each of the 738 rows of `certs/scalar_lemma_u.tsv`: the primes are the first r odd primes; the caps are positive integers; 1 <= k0 < r; 1 < C_i <= p_i for k0 < i <= r; and the number B of Proposition 4.1, computed as in Section 4.2, satisfies B < 1. (ii) Anchored certificates. For each of the 37 anchored certificates (A8; F9_01, ..., F9_23; G01, ..., G13): the primes are the first 8, 9, 10 or 11 odd primes as stated; the header is admissible (Section 8.1); for every row the numbers R and S recomputed from the key by the formulas of Section 8.5 satisfy R > S; and the list of rows is complete (Section 8.6). The cap vector of A8 is (inf^8). (iii) Enumeration. For r = 9, ..., 13: every vector f of r positive integers with p_1^(f_1) ... p_r^(f_r) < X0 (there are 5,028, 1,484, 248, 21, 1 of them) is dominated by the cap vector of a certificate verified in (i) or (ii) on the first r odd primes; and p_1 p_2 ... p_14 > X0."

## How my checker works

- It is about 1,100 lines of Python (standard library, `fractions.Fraction` throughout) plus a 150-line C++ kernel. I wrote it for this review; it is not part of the package. Python runs with `-I`, at most 4 processes, under `nice`.
- **Scalar rows (item i).** These follow Proposition 4.1 and Section 4.2 literally: rho_m, theta_m, the two kinds of tail laws of T_m, E[M] as a product, and the exact law of M = prod(1 + T_m) truncated at k < delta_i/rho_i. The checker also verifies that each law is a probability law (every atom >= 0, total 1). As an extra spot check of the Section 4.2 identity, I recomputed B from the untruncated law of M on 40 rows; it agreed with the stored B on all 40.
- **Anchored rows (item ii).**
  - Header quantities come from Sections 5.1, 5.4, 6.1 and 8.1: rho_p, n_p, tau_7, beta_q, C_q, omega_q, Delta_7, kappa_s, Zbud, Tbud, theta3, the level sets and the level masses.
  - The laws Pi_q, Pi0_q and Pi1_q come from Sections 6.3 and 8.4, with the means in closed form. For finite caps the checker re-sums the laws to confirm the closed forms.
  - For each key, the core K, the set B, the cell weights and the reserve R(kk) follow Sections 5.4, 5.5 and 8.2.
  - The stage expressions OrdSt, Coarse_7, Pad_7, FH_q and Fix, and the envelope F, W, M and Ord, follow Sections 8.3 and 8.5. Sums over omitted levels are computed as "all levels in closed form, minus the explicit levels".
  - The phase table of 8.5 gives R and S for each row.
  - Key validity is checked per Section 8.2 and per the key form of each phase.
  - Completeness is checked per 8.6 by expanding the leaf set level by level. A leaf counts as covered only by a row that is valid.
- **The geometric maximum Gmax (Section 5.6).** The C++ kernel computes the exact maximum over all residue choices for G = (3, 9, 27, 5, 15, 45, 135), in integers over exact common denominators. Overflow bounds are checked before every call.
  - It enumerates the residues for 3, 9 and 27.
  - For every column, and every subset of {15, 45, 135} placed in that column (with or without the class 5), it finds the best placement inside the column exactly.
  - It then combines the columns with a subset dynamic program.
  - This decomposition is exact because the classes 5, 15, 45 and 135 each lie in one column, and once the residues for 3, 9 and 27 are fixed, cells in different columns do not interact.
- **Enumeration (item iii).** A depth-first enumeration of all exponent vectors below X0 for r = 9 to 14, then a domination test against the cap vectors of the certificates that passed items (i) and (ii).

## Results of my checker (all rows, all files)

| item | what was recomputed | result |
|---|---|---|
| (i) | all 738 rows of object/certs/scalar_lemma_u.tsv | all pass: primes, caps, k0 and 1 < C_i <= p_i hold, and B < 1. All 738 stored `B_exact` equal my B. Largest B = 130157612206585412852431229/130269519960832360564391936 (0.9991409521). Rows per r: 603 / 120 / 14 / 1 for r = 10 / 11 / 12 / 13. The optional restriction delta_i >= rho_i holds on every row |
| (ii) A8 | all 28,057 rows of object/certs/thmA_8p.part01.tsv to object/certs/thmA_8p.part06.tsv, read as one list (headers identical except `part`) | header admissible (H1 to H4); 0 key errors; 0 duplicates; 28,057 valid (R > S); 0 R and 0 S mismatches with the stored values; 0 uncovered leaves; every row lies on the leaf hierarchy. Least R - S = 28353678790630767758519622060026627651479943597269246597082274387654587/14150648987289441510301945000553393239539993933702819833147809824000000000 (0.0020037017) |
| (ii) F9 | all 23 certificates, 736 rows of object/certs/nine_finite.tsv | all admissible, valid, complete; 0 mismatches. Least R - S = 7353010244456360618611/457648694712387914811075 (0.0160669315, F9_13) |
| (ii) G | all 13 certificates, 692 rows of object/certs/global_anchored.tsv | all admissible, valid, complete; 0 mismatches. Least R - S = 31892572639/133917433650 (0.2381510142, G06) |
| (iii) | all vectors for r = 9 to 13, and r = 14 | 5,028 / 1,484 / 248 / 21 / 1 vectors (6,782 in all), every one dominated; no vector below X0 at r = 14; p_1 ... p_14 = 307,444,891,294,245,705 > X0. The 9-prime vectors need the F9 certificates; 17 vectors at r = 10 need G01 to G12, and 1 at r = 11 needs G13; r = 12, 13 are covered by the scalar rows alone |

Also checked:

- The headers of all 37 certificates (caps, C_7 = 3/2, taus, Ucut, Vcut) equal the tables of PROOF.md Sections 9.1 to 9.3.
- The phase counts equal Section 9.1.
- The least margins and the largest B equal Section 9.7.
- X0 = 6,557,114,959,770,375 is the stated product, and p_1 ... p_13 = 6,541,380,665,835,015 < X0.
- The completion table of Section 5.2, the kappa values, the tail sums of Section 8.3, and "tau_7 >= 2, Delta_7 > 0 for C_7 = 3/2" all hold, recomputed exactly.

Compute: items (i) and (iii) took 2 s; G 11 s; F9 36 s; A8 100 s and, on the second run, 103 s (4 processes, 447,722 kernel calls after caching).

## Checking my checker

- **The kernel against brute force.** I compared the kernel with an independent brute-force kernel that enumerates every residue tuple:
  - 30 problems recorded from real A8 rows and 30 random synthetic ones;
  - then 156 non-trivial problems (value > 0 and some sigma + b_x < 0), drawn from every phase of A8 and from F9_13, F9_15, F9_23, G06 and G08.
  - Result: 0 mismatches.
- **Mutation tests** (in copies of the certificate files):
  - Deleting one basic row of F9_13 leaves 1,097,600 leaves uncovered, so the check fails.
  - Changing F9_04's cap vector to (5, 3, 2, 2, 2, 1, 1, 1, 1), whose product is X0 itself, makes 3 of its 32 rows invalid (least R - S = -0.2559), so the check fails. This is consistent with PROOF.md Section 10, item 2.
  - Raising F9_13's cap at 3 from 8 to 9 changes all stored numbers (32 R and 32 S mismatches flagged) but leaves every row valid. So that change is not a failure of the method, only of the stored values.

## The package's checks, run afterwards in a copy

`sh verify-it-yourself/run_checks.sh` in a full copy of the package inside my work folder, under a 2,400 s alarm, from 02:39:34 to 02:42:59. The script runs Python without `-I`; I left it unchanged, because the second checker imports a module from its own folder.

- The manifest sha256 909804ef2bf322270ec686552d0952780851e07d3c8471cbfac58507b3c715d6 equals INDEX.csv.
- Checker 1 (verify-it-yourself/check.py, 4 processes): PASS in 190 s. It reports 738 scalar certificates with max B = 0.999141, all 6,782 vectors dominated, G (692 rows, min 0.238151), F9 (736 rows, min 0.016067) and A8 (28,057 rows, min 0.002004).
- Checker 2 (verify-it-yourself/alternate/): PASS in 15 s including its build.
- The last line is `PASS`, with exit code 0.

Comparison with my checker: the same verdict on every item. Checker 2 prints exact least margins for A8, F9 and G and the exact largest scalar B; all four are identical, as fractions, to mine. Checker 1 checks the stored R, S and B for equality with its own recomputation, and I found every stored value equal to mine, so its recomputed values agree with mine on every row. A second run of the package script (02:45:38 to 02:49:02) printed output identical to the first apart from the times.

## Referee of object/PROOF.md, step by step

Verdicts: C = correct, G = gap.

- Lemma 1.1 (residues and digit spaces): C. Lemma 1.2 (monotonicity): C. The facts of Section 1.3 on tree automorphisms: C.
- Lemma 2.1 (prime replacement): C. Preimages of classes are empty or classes with the same exponent vector, so the distinct exponent vectors give distinct moduli. Corollary 2.2: C. Proposition 2.3 (reduction): C; the cases r <= 8, 9 to 13 and >= 14 are exhaustive. Proposition 2.4: C (finite check, reproduced).
- Lemma 3.1 (completion): C. With infinite caps D is countable, but every element has finitely many predecessors, so the recursion is well defined.
- Lemma 3.2: C. Lemma 3.3: C. Lemma 3.4: C (I checked the summation by parts and the regrouping of the pi(j)). Lemma 3.5: C.
- Lemma 3.6: C. The measurability of B_i(x) is not argued, but it holds: F' has finitely many mixed classes, so B_i(x) is constant on the cells of a finite partition into cylinders.
- Lemma 3.7: C. The induction carries along a non-negative factor that depends only on the anchor point; this is implicit but harmless.
- Proposition 4.1: C. Completion, the anchor bound 1 - sum over |I| >= 2 of prod theta, the kernels, the comparison through Lemma 3.7 and then Lemma 3.4 in each anchor coordinate, and the inventory count prod(1 + T_m) - 1 all check. Section 4.2: C.
- Section 5.2, the completion table: C. I recomputed all nine sums exactly; for 15 q_2 the bound 38/55 needs q_2 >= 11, which holds, and neither 3 q_2 nor 5 q_2 is in D.
- Lemma 5.1 (normal form): C. I followed steps 1 to 8, including that steps 4 to 6 do not undo earlier steps and that residues r with one signature are exchanged by automorphisms that fix C_3, C_9, C_27, C_5, C_15 and C_25.
- Lemma 5.2 (anchor measure and reserve): C. Properties R1 to R3: C.
- Properties G1 to G4 of Gmax: C. Lemma 5.3 (anchor comparison): C. The level masses agree with the pi-sequences of Lemma 3.4 with C = 1, and S >= C/p holds since z <= 1/2 and the removed fraction of a column is at most 9/20.
- Lemma 6.1: C. Lemma 6.2 (padding): C. Proposition 6.3: C. Lemma 6.4: C. I checked the three label groups, the weight M_J - omega for the pair (1, 1), the coefficients M_J w - omega e_15 >= 0, and the split into channels 0 and 1.
- Theorem 7.1: C. Lemma 7.2 (vertices): C. Concavity in z for fixed w and in w for fixed z holds, also with the value +inf allowed.
- Lemma 8.0: C. The laws of Section 8.4: C. I confirmed the closed-form means and the tail sums of Section 8.3 exactly.
- Lemma 8.1: C. I checked Steps 1 to 4 for every phase: the cell weights and cores of the keys dominate those of the leaves; the reserve inequalities (with R3 for basic75); the bounds Pad_7 (needs H3), Coarse_7 (needs H4) and the release to OrdSt_7; and Fix, FH_q and OrdSt_q at the later stages.
- Theorem 8.2: C. Theorem A: C, given item (ii) for A8. Section 9.6, the proof of Theorem 1: C.
- The remark in Section 10, item 8 (raising exponents by splitting the class of the largest modulus): C. It is not used in the proof.

**Do the checkers test the inequalities the proof needs?** Yes. Lemma 8.1 needs R > S with R and S exactly as in Section 8.5, together with admissibility, valid keys and completeness. Proposition 4.1 needs B < 1 with B as in Section 4.2. My checker computes exactly these quantities from the PROOF.md text, and they equal the stored numbers on every row. Both package checkers require equality with the stored numbers, so they test the same inequalities. The extra conditions in FORMAT.md only make the checks stricter: delta_i >= rho_i, tau_q >= 1, the cut conditions, and "no unused rows".

## Findings

1. **Wording gap in Section 9.4 (minor; no effect on the result).** Item (ii) does not list that every key must satisfy the constraints of Section 8.2 and the key form of its phase in the 8.5 table. Examples: a basic row must have r = -1, (d, k) = (0, 0), ie = 0 and z = -1; a pure3 row must have z in Rows(b). The definitions of 8.2 and 8.5 imply this, and Lemma 8.1, Step 1 needs it: a "basic" row with r >= 0 would have a smaller core than the leaves it is said to cover. My checker enforces it, and the package's hierarchy traversal rejects rows off the hierarchy. All 29,485 keys satisfy it.
2. Two nine-prime certificates (F9_06, F9_11) are redundant: every vector they dominate is also dominated by another certificate. This is harmless.
3. The bound sits exactly at the edge of these certificates. All exponent vectors with product below X0 are dominated, while (5, 3, 2, 2, 2, 1, 1, 1, 1), with product X0, is dominated by none of them. So X0 is the least undominated product, as Section 10, item 4 says.
4. Limits. My referee is a careful reading, not a formal proof check; the lemma chain is not formalised (as the package says). Kernel exactness rests on the decomposition argument above, on the brute-force agreement on 216 problems, and on exact agreement with the stored values on all 29,485 rows.

## Fetch log

No network fetches were made. My role needed none.

pass: true
