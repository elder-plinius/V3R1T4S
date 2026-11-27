context: Claude Code subagent, fresh context Opus 5.5

# Criterion review: erdos-7-odd-covering-system, partial win p2

Claim under review: every finite covering system of Z with pairwise distinct odd moduli greater than 1 has L = lcm >= X0 = 6,557,114,959,770,375 = 3^5 * 5^3 * 7^2 * 11^2 * 13^2 * 17 * 19 * 23 * 29. The claimed win is p2.

p2 (verbatim, from the claim record): "A rigorous proof raising the lower bound on L strictly above 11,486,475 (Egeozturk, forum Aug 2026), rechecked by independent code."

Fetches: none. This role needed no network.

## 1. The package's checks (run by me)

- I copied the package into my work folder and verified all 51 entries of the package's SHA256SUMS list against the copy: 51 OK, 0 failures.
- I ran `sh verify-it-yourself/run_checks.sh` in the copy under `nice -n 10` with a 3000 s alarm. It ran from 2026-11-27T02:10:07Z to 02:13:22Z (195 s), exit code 0, last line `PASS`.
  - The `object/MANIFEST.json` sha256 909804ef...c715d6 matched `INDEX.csv`.
  - Checker 1 (`verify-it-yourself/check.py`, 4 processes) passed in 181 s: 738 scalar certificates (max B = 0.999141), domination of 5028/1484/248/21/1 vectors for r = 9..13, and 37 anchored models with 29,485 rows (least margins: A8 0.002004, F9 0.016067, G 0.238151).
  - Checker 2 (`verify-it-yourself/alternate/`, C++17 kernel) passed in 14 s including the build, with the same counts and an exact least surplus per group.
- The output matches `RUN_IT_YOURSELF.md` and `verify-it-yourself/RECEIPTS.md` line for line, apart from the timings.

## 2. Clause "a rigorous proof"

I read all of `object/PROOF.md` as a referee would, asking for each step whether it is proved in the text or reduced to a stated finite computation.

- **Reduction (Sections 1, 2; proved in the text, checked by me in full).**
  - Lemma 1.1 (covering Z is the same as covering the digit space) is correct, including infinite caps.
  - Lemma 1.2 (monotonicity under domination) is correct.
  - Lemma 2.1 (prime replacement) is proved inside the document and is correct. Exponents are kept. Distinct exponent vectors give distinct moduli. Classes whose digits are too large have empty preimages.
  - Corollary 2.2 is correct: the m-th prime of L is at least the m-th odd prime, so p_1^f_1...p_r^f_r <= L.
  - Proposition 2.3 settles every value of r:
    - r >= 14 is impossible because p_1...p_14 = 307,444,891,294,245,705 > X0. I checked this.
    - r <= 8 is excluded by (inf^8). That is Theorem A, proved inside the document with its own certificate A8, not cited from the unrefereed preprint.
    - 9 <= r <= 13 is reduced to finitely many cap vectors.
  - So the statement covers every finite odd covering: any number of primes, any exponents, any moduli. I found no hidden restriction to a subclass. The only properties used are odd, distinct and greater than 1. Oddness enters through the comparison with the first r odd primes, through rho_p <= 1/2 in Proposition 4.1, and through the fixed anchor primes 3 and 5.
- **Scalar criterion (Section 4; re-derived by me).**
  - Proposition 4.1 follows from Lemmas 3.1, 3.2, 3.4, 3.6 and 3.7. The steps are completion with prime powers, the anchor measure, the union bound, Lemma 3.7 with S_j = 1 (which needs C_j <= p_j), Lemma 3.4 in each anchor coordinate with C = 1/(1 - rho_m), and the inventory bound rho(prod(1+T_m) - 1).
  - The exact evaluation in Section 4.2 is correct.
- **Anchored criterion (Sections 5 to 8, Schroeder's method written out with exponent caps).** I re-derived these steps and found no gap:
  - the completion table in Section 5.2 (the largest sum is 86/105);
  - the normal form, Lemma 5.1, including the signature argument for C_45;
  - the reserve bookkeeping of Lemma 5.2(iii): the g15 and g45 credits and the 75-credit;
  - the level masses of Lemma 5.3 (pi(0) = gamma_x(0), then alpha_x(0));
  - the padding at 7 in Lemma 6.2 and the category counts w(u, v) with the four padded pairs;
  - the grouping in Lemma 6.4 (a: M_J - 1; b: the class 15*q_2; c: the rest);
  - the concavity and vertex argument of Lemma 7.2;
  - Lemma 8.0;
  - Steps 1 to 4 of Lemma 8.1, including the release step (G2) and the bound kappa <= 1 - C_7/7 = 11/14.

  I did not re-derive every line of these sections, and I did not audit the roughly 700 lines of checker code that evaluate S line by line against Section 8.5 (see Section 3 of this report for what stands in for that).
- **Finite computations.** Section 9.4 lists exactly three: (i) B < 1 for 738 scalar rows; (ii) for 37 anchored certificates, an admissible header, recomputed R > S on every row, and completeness; (iii) the enumeration of the 6,782 vectors and their domination, plus p_1...p_14 > X0. The proof states that it rests on nothing else.
- **Not claimed (Section 10 of the proof, `README.md`).** These limits are honest and do not shrink p2:
  - existence of an odd covering stays open;
  - omega(L) >= 10 is not proved;
  - the vector (5,3,2,2,2,1,1,1,1), whose product is exactly X0, is not covered. I confirmed that its product equals X0, so the bound is ">= X0", not "> X0";
  - the lemma chain is not formalised;
  - no claim is made about the rest of the preprint.
- **Outside results.** The argument does not depend on any unrefereed result. Schroeder's preprint is credited as the source of the method, but every lemma it uses is proved in `object/PROOF.md`, and Theorem A (omega(L) >= 9) gets its own certificate. Simpson and Zeilberger are cited only for credit; Lemma 2.1 is self-contained.
- **Verdict on this clause.** It is a complete written proof that reduces to stated finite computations. It is not refereed and not checked by a proof assistant. p2, unlike p1, does not require Lean or a line-by-line external check. I found no error.

## 3. Clause "rechecked by independent code"

- **Do the two checkers do what Section 9.4 asks?**
  - `verify-it-yourself/check.py`:
    - recomputes B by the mean-plus-correction formula of Section 4.2, with an exact law truncated at max p + 2, which is safe because only k < delta/rho < p matters;
    - checks 1 < C_i <= p_i;
    - adds the stricter test delta >= rho;
    - enforces (H1) to (H4); it enforces (H4) always, which is stricter than the proof requires;
    - recomputes R and S exactly and requires R > S (`margin > 0`);
    - walks the completeness tree of Section 8.6 and rejects any unused row;
    - enumerates the vectors by depth-first search and checks domination at each rank.
  - `verify-it-yourself/alternate/check_alternate.py` with `verify_scalar.py`:
    - recomputes B by summing the hinge over the whole product law, with no truncation;
    - enumerates the vectors by factoring multipliers of the squarefree kernel;
    - computes the geometric maximum with a separate C++ integer kernel that uses a structural reduction and checks the reduction's invariant at run time. Checker 1 uses a pure-Python dynamic program instead;
    - computes the fixed165 stage as the free stages minus an exact "saving", where checker 1 evaluates Fix directly;
    - requires R > S (`margin <= 0` is rejected) and that every row is used.
  - The two code paths are genuinely different. Both checkers also require the recomputed values to equal the stored ones, which is more than the proof needs.
- **Independence caveat.** Both checkers come from the contributor. To test whether checker 2 was merely tuned to reproduce the stored numbers, I ran both checkers' row evaluators on cap vectors that are not in the package, using the 32 basic rows on nine primes:
  - The two agreed exactly on all 96 rows.
  - At the boundary vector (5,3,2,2,2,1,1,1,1), 3 rows fail (least R - S = -0.2559).
  - For (inf^9), all 32 rows fail (least R - S = -4.49).
  - For the package's F9_04 caps, all 32 rows pass (least R - S = 0.1036).

  So the inequality checks are not vacuous, and the agreement is not an artefact of fitting to stored values.
- **My own recheck, written from the proof text only, not from either checker.**
  - I recomputed B of Proposition 4.1 for all 738 scalar rows by brute force over the full joint law. All 738 equal the stored values exactly, and all are below 1.
  - I enumerated the vectors below X0 and found 5,028, 1,484, 248, 21 and 1 for r = 9..13. Every one is dominated by a declared cap (scalar rows, F9 headers or G headers), and p_1...p_13 = 6,541,380,665,835,015 < X0 < p_1...p_14.
  - I did not independently recompute the 29,485 anchored rows. For those, the evidence is the two contributor checkers.
- **Verdict on this clause.** Met: two separately written exact implementations both pass, and my own code rechecks parts (i) and (iii).

## 4. Clause "raising the lower bound on L strictly above 11,486,475"

X0 = 6,557,114,959,770,375 > 11,486,475 (by a factor of 570,855,285). Every other public bound that the package lists for comparison, 1,527,701,174 and 9,704,539,845, is also smaller than X0. Whether a published result already reaches X0 is the novelty skeptic's question; nothing in the package suggests one does.

## 5. Null model

- **Even moduli.** Coverings with even moduli exist. I applied the scalar criterion of Proposition 4.1, as I implemented it, to cap vectors that do admit such coverings:
  - 2^2 * 3 (the covering 0(2), 0(3), 1(4), 5(6), 7(12));
  - 2^3 * 3 (a covering with least modulus 3);
  - 2^3 * 3 * 5 (Erdős's covering of period 120).

  I tried every prime ordering, every k0, and a grid of C values. When 2 is an anchor prime, the law is invalid (Prob(T >= 1) > 1, because rho_2 > 1/2). Every valid choice gives B >= 1: the least values are 1.1406, 1.3516 and 1.7383. So the criterion does not "prove" a false exclusion.
- **The anchored criterion.** It is built on the fixed primes 3, 5, 7, so it cannot be run on even moduli. On odd inputs it rejects the boundary vector and (inf^9), as shown in Section 3.
- **Distinctness.** It is used essentially: one class per modulus in the completion, and distinct exponent vectors in the inventories. Without it the odd covering 0, 1, 2 mod 3 would exist.

## 6. Residual limits

- The proof is a written proof. No proof assistant has checked it, and no referee has published a review. `verify-it-yourself/alternate/REFEREE.md` was written by the contributor's own pipeline.
- I re-derived the reduction and the scalar criterion in full and the anchored method in spot checks. I did not audit the anchored S code line by line against Section 8.5. The exact agreement of two different implementations, including on inputs outside the package, is the evidence for that part.

## Decision

Each clause of p2 holds as written:
- a complete written proof with no gap I could find, whose finite part is exactly what the checkers recompute;
- a bound strictly above 11,486,475;
- a recheck by two separately written exact checkers, both passing in my run, plus my own recomputation of the scalar and enumeration parts.

confirmed_scope:
A written proof (`object/PROOF.md`), unrefereed and not checked by any proof assistant, together with exact rational recomputation of its finite part (738 scalar certificates, 37 anchored certificates with 29,485 inequalities, and the domination of 6,782 exponent vectors) by two separately written checkers that both pass, shows that every finite covering of Z by residue classes with pairwise distinct odd moduli greater than 1 has L >= 6,557,114,959,770,375, strictly above 11,486,475.

pass: true
