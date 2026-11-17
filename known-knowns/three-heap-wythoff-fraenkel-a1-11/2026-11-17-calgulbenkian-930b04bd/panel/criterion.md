context: Claude Code subagent, fresh context [Sonnet 5.5]

# Criterion skeptic report: three-heap-wythoff-fraenkel-a1-11

## Verdict in one paragraph
The claim meets the full success criterion as written, resting on Sun and Zeilberger's published Claim 3.5 as the reduction. I rebuilt the P-positions from the game rules with my own C++ program (checked against my own naive brute force: 239 positions, exact match). From that I recomputed every constant, and all of them agree with the claim. There are minor convention and wording issues, listed below. None of them changes a number or defeats a condition.

## What the two conjectures state (as I read them in the sources)
- Conjecture 1 (Fraenkel): for fixed A1, there is an index after which the n-th P-position is (A1, A_n, A_n + n), where A_n = mex({earlier second and third heaps} union T) for a small finite set T. In Sun and Zeilberger's [a, b, c] terms this is B_{n+1} = B_n + 1 plus the mex rule.
- Conjecture 2: the same sequence has A_n = floor(n*phi) + eps_n + a with eps_n in {-1, 0, 1}.
- Fraenkel-Krieger and Sun proved that Conjecture 1 implies Conjecture 2. Sun and Zeilberger's Claim 3.5 is a finite sufficient condition for both.
- Naming trap: Fraenkel's T (the GONC column example: T = {2, 17, 22} for A1 = 1) is Sun-Zeilberger's S^m. Sun-Zeilberger's T^m is a different, smaller set (T^1 = {1}). The package uses the Sun-Zeilberger meaning throughout and says so. That is fine.

## Is the reduction a theorem of the paper, and does the package quote it faithfully?
- The paper (downloaded from the Rutgers PDF) states Claim 3.5 as a sufficient condition, with a proof by induction that uses Lemma 2.4 and Claim 3.4. It is a stated result, not a heuristic. The proof is terse in places. Claim 3.3, the S1(n) membership rules, rests on a periodicity argument about (a xor b) - b with period p(m). The argument is sketched, not spelled out. The package inherits this exactly as the paper states it.
- The package's eight-condition check matches the paper's list. Two items differ from the paper's literal text:
  1. The paper prints alpha' = floor((max - min)/2). That is clearly a typo for (max + min)/2. The package uses (max + min)//2, which reproduces every alpha in Table 1.
  2. The paper defines N_k by "n > N_k". Table 1 matches the "n >= N_k" reading. For example, N1 for A1 = 1 is 21, and the last irregular index really is 20. The package states this shift in its certificate header and notes that Condition 6 holds under either reading. That is honest. My N1, N2 and N3 follow the Table-1 (>=) reading and match all 11 Table 1 rows.
- The package checks conditions 5 and 8 on slightly wider ranges than the paper, so it is stricter, not weaker. Rule-3 windows use p + 1 values (An to An + p), as the paper's inequality does.
- Claim 3.4: the package checks A_{N+1} > max T and covers small c. It does not check B_n > m + max T explicitly. I checked it: B_16 = 50 > 34, and B is increasing after that, so it holds.

## Literal check of each criterion condition (my own reproduction)
Files I made: C++ retrograde solver (my own derivation, not the package's code), naive brute force, and several analysis scripts. All are in my scratch folder, with a working file (not shipped).
1. P-positions: my solver computes P^m for m = 0..11, second heap up to 6000 (about 3,700 positions per layer). It matches an independent definition-level brute force on all P-positions with p3 <= 70 (239 of them).
2. Explicit n2 < n1 for A1 = 11: n2 = 1216, n1 = 3249. I verified all eight Claim 3.5 conditions with my own code, including S1:
   - Cond 1: (A+B)_{n2+3} = 1964 + 1258 = 3222, which is below A_{n1} = 5248. True.
   - Cond 2: B_{j+1} = B_j + 1 for n2 <= j <= n1. True.
   - Cond 3: B_{n1} is the maximum so far. True.
   - Cond 4: mex({B_i, i <= n1} union S1) = B_{n1} + 1. The complement of the B-values has exactly 40 elements, equal to the certificate's S^11, with max 1252. True.
   - Cond 5: the alpha spread is exactly 2 and alpha' = -61.
   - Cond 6: B_{n1} exceeds B^i_{N3^i} and B^i_{N3^i + 1} for all i < 11. True.
   - Cond 7: alpha^i - alpha' - 4(11 - i) is >= 1 for every i; the values are [17, 17, 15, 13, 13, 11, 9, 6, 3, 1, 1].
   - Cond 8: |eps| <= 1 on n2 - 2..n1, and no three consecutive nonzero eps on that range. True.
3. Claim 3.3 membership: for every c in S^m, m = 1..11, I found a Rule 1, Rule 2 or Rule 3 certificate. For Rule 3 I used a direct search for a nim-sum-zero move into a P-position at every x in the p(m) + 1 window. No c failed.
4. Derived constants for A1 = 11: T^11 = {1, 7, 11, 13, 17, 21, 23}, alpha = -61, N1 = N2 = 1214, N3 = 1381, B_{N3} = 1420, N (Claim 3.4) = 15. All reproduced.
5. N3^i and B^i_{N3^i} for every i = 0..10: all 11 recomputed values match the certificate. Examples: i = 8 gives N3 = 1739 and i = 10 gives N3 = 1766. The package's own receipts list these too.
6. Table 1 (T, S, alpha, N1, N2 for 0..10): my recomputation matches all 11 rows. I also compared the package's embedded Table-1 copy with the PDF text and found no differences. (T^9 is printed as "6, 4, 11, 15" in the paper and sorted in the package. That is cosmetic.)
7. Beyond the literal criterion, I checked the actual Fraenkel forms on the computed range for A1 = 11. The mex form (with T and {0..m-1}) holds from index 1, and y - x - n is constant (39) from the claimed N1 on. The eps form against floor(n*phi) has a 3-value window, {1, 2, 3} for offset 0. All of this is inside my horizon only. The infinite tail rests on Claim 3.5.
8. The certificate's sha256 matches the number in the claim.

## Independence of the checker
The package's verify_wythoff.py is the claimant's own program. The criterion asks for one sharing no code with the claimant's. The package's checker is by the same author, so it cannot count by itself. It does recompute from the rules, and it cross-checks against a literal brute force. It is also self-consistent with my reproduction. The independence requirement is met only by my panel reproduction, which is separate code and agrees on every number. Table 1 (partial p1) is likewise independently reproduced.

## Not published as proved
- The GONC6 Unsolved Problems column (A4(53)), fetched today, says the conjectures are proved for N = 3 with first heap up to 10, and says nothing about 11.
- arXiv API searches (Wythoff with heap, Wythoff with Zeilberger) and a Crossref lookup showed nothing extending the case.
- I could not exhaustively search the citing literature, so this is "no evidence found", not a proof of absence.
- The result is a new single case. It is not subsumed by any merged result, and A1 = 11 is not a restriction of the prior record.

## Remaining limits (do not widen the claim)
- It rests on Sun and Zeilberger's Claim 3.5 and Lemma 2.4 as published, including the paper's terse periodicity argument for Claim 3.3 and the Table-1 (>=) indexing. Nothing is formalised in a proof assistant.
- Only A1 = 11 is shown. The general case and N >= 4 are open, and the package says so.
- Window and tail checks (conditions 2, 5, 8) are finite and run to n1 = 3249 on the computed data. The tail beyond n1 is the induction in Claim 3.5, not a computation.

confirmed_scope: For N = 3 and smallest heap A1 = 11, under Sun and Zeilberger's convention, with n2 = 1216, n1 = 3249 and N3^i and B^i_{N3^i} recomputed for every i <= 10, the constants T^11, S^11, alpha = -61, N1 = N2 = 1214, N3 = 1381 and S1(3249) satisfy every hypothesis of their Claims 3.4 and 3.5, so both of Fraenkel's conjectures follow by their published Claim 3.5 and not by any independent formal proof; I reproduced this with separate code, and found no evidence it was already published.

pass: true
