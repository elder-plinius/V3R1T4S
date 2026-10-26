# Criterion skeptic report

context: subagent (fresh, claim/ copy only; addendum re-checked against the corrected claim/ and the run's data/georgakopoulos_panagiotis_arxiv_2107.06272.pdf)

Inputs read: CLAIM.md, PROOF.md, REPRODUCE.md, code/par/main.go, code/par/go.mod, code/verify_cert.py,
code/kcheck.py, outputs/*, result/bound.json, table/literature_record.md, MANIFEST.sha256 (all 16 hashes match;
the claim folder was not modified). Nothing else on the machine was read for the original analysis. Scratch
work lived outside claim/. The addendum below additionally reads the corrected claim/ and one PDF, at the
coordinator's request.

## Criterion, clause by clause

Criterion (verbatim, CLAIM.md): "A rigorous proof that p_c^site(Z^3) >= p* for an explicit rational p*, strictly
above every explicit rigorous lower bound published (or directly implied by published results) at verification
time, whose finite part is an exhaustive computation in exact integer or rational arithmetic released with code a
stranger can rerun." No partial wins are defined, so the only possible pass is the full criterion.

1. Explicit rational p*: p* = 263376/10^6. Met.

2. Rigorous proof (PROOF.md), checked lemma by lemma:
   - Parent rule (section 1): P(x) is nonempty for d(x) >= 1, and the parent is unique because distinct neighbours
     of x lie in distinct directions. Parent pointers lower d by 1, so T is a spanning tree of C(0) rooted at 0
     with at most 6 children per vertex. Correct.
   - Lemma 0 (F and gamma are disjoint): at a turn, u_k is adjacent to v_{k-1} and to v_{k+1}. If u_k = v_m, the
     NAW property forces m = k, but u_k != v_k. Correct.
   - Lemma 1: (a) d(v_k) = k by induction. (b) A chord v_i ~ v_j with j >= i + 2 would give d(v_j) <= i + 1 < j.
     (c) An open shortcut site w gives d(v_j) <= i + 2 < j; the bound j - i >= 3 is exactly the threshold where
     this works (j - i = 2 gives no contradiction). An open corner u would have d(u) = k exactly, so u would be in
     P(v_{k+1}) and would be preferred over v_k because of the rank condition. Correct.
   - Lemma 2: if C(0) is infinite, T is infinite and locally finite, so Konig's lemma gives a ray. y = v_{N+1}
     lies in E(gamma): (v_0..v_{N+1}) is a NAW, and y is open while F(gamma) is closed. The tail of the ray is an
     infinite open self-avoiding path from y that avoids gamma (d > N) and avoids F (its sites are open, F's are
     closed). Correct.
   - Lemma 3: A_gamma depends only on gamma u F (N + 1 + |F| distinct sites, by Lemma 0), so
     P(A) = p^(N+1)(1-p)^|F|. B_{gamma,y} depends only on the complement of gamma u F (y is outside it), so the two
     events are independent. P(B) <= theta by translation invariance. The union bound then gives
     theta <= K_N theta. Correct. (Measurability of B is standard and is not discussed. That is not a gap.)
   - Corollary: (1 - K_N(p)) theta(p) <= 0 with K_N(p) < 1 gives theta(p) = 0, so p is in {theta = 0} and
     p_c = sup{theta = 0} >= p. Correct, and it does not need K_N to be monotone.
   - Lemma 4 (sign flips): at a turn the two compared directions lie on different axes, and every index on axis a
     is below every index on axis b > a, so the comparison depends only on the axes, which flips preserve. The
     stabilizer is the set of flips of unused axes, so the orbit size is 2^|A|, and each orbit has exactly one
     member whose first step on each used axis is positive. Correct.
   - Monotonicity remark: d/dp of p^21 (1-p)^f has the sign of 21(1-p) - f p, so each term increases on
     [0, 21/(21+f)], and f_max = 23 gives [0, 21/44]. Correct, and only used to show that p* is the largest
     passing value on the grid, not for validity.

3. The code matches the proof:
   - code/par/main.go builds NAWs (requires adj[y] == 1, meaning the only path neighbour of y is v_k).
   - Shortcut sites are flagged at the first v_j with j >= minIdx + 3. minIdx stays correct under LIFO
     backtracking.
   - The corner test (dp^1) < (di^1) is exactly dirindex(u_k - v_{k+1}) < dirindex(v_k - v_{k+1}), and the corner
     is u = v_{k+1} - s.
   - Flagged sites have at least 2 path neighbours, so they can never become path vertices later.
   - The leaf counts E exactly as defined.
   - Canonical prefixes are covered once each. The undo logic is correct. The box (S = 49, centre 24, reach 21)
     cannot wrap.
   - Counts are int64 (maximum about 1.4e13, so no overflow). An out-of-range |F| would panic before any output,
     and an output exists.

4. Exhaustive computation in exact integer or rational arithmetic: the Go enumerator is integer-only and
   exhaustive over sign-flip canonical representatives, weighted by orbit size 2^|A|. Lemma 4 makes this
   equivalent to enumerating all N-step NAWs, so it is not a sample. code/verify_cert.py and code/kcheck.py make
   every decision with fractions.Fraction. Floats appear only in printed values and in the display-only probe
   points of code/kcheck.py. Met.

5. Code a stranger can rerun: Go and Python standard library only. I rebuilt code/par with go1.26.4 and:
   - reran N = 16 and N = 18: byte-identical to outputs/p16.txt and outputs/p18.txt;
   - reran code/verify_cert.py and code/kcheck.py: identical to outputs/verify_N20.txt, outputs/k20.txt and
     outputs/k18.txt.
   Small nit: code/par/go.mod pins `go 1.26.4`, while REPRODUCE.md says "any recent version". An older toolchain
   will auto-fetch 1.26.4 or refuse. Met.

6. Strictly above the record:
   - CLAIM.md, table/literature_record.md and result/bound.json all state the record as 0.21103 (Ponitz-Tittmann
     mu(Z^3) <= 4.7387, via p_c^site >= p_c^bond >= 1/mu). They are consistent with each other.
   - p* = 0.263376 > 0.21103. It also exceeds the unproven comparator 5/19 = 0.263158 (Torquato-Jiao), by
     0.000218.
   - Nit: 1/4.7387 = 0.2110283 < 0.21103, so "1/mu >= 0.21103" rounds the wrong way. This is immaterial.
   - I did not search the literature (that is another skeptic's job). The table records only two sources ("one
     honest request each"). Whether any published bound, or a bound directly implied by published results
     (including NAW connective-constant or series results), reaches 0.263376 is outside my evidence. My verdict on
     this clause is conditional on the literature skeptic.
   - Superseded: the corrected claim states the record as 0.2522. See the Addendum below.

## Independent checks I ran (outside claim/)

- Exact certificate, my own code (integer numerator vs denominator over the common denominator 10^(6*44)), from
  outputs/p20.txt:
  - K_20(263376/10^6) = 0.99997152602... < 1, with 1 - K = 2.847e-5;
  - K_20(263377/10^6) = 1.0000417790... > 1;
  - K_20(5/19) = 0.98475899... < 1.
  These match outputs/verify_N20.txt and result/bound.json. Totals also match: a_20 = 3516072837894 and
  sum c_f = 14334995983614.
- Independent brute force written from the PROOF.md definitions (all walks, no symmetry reduction, F and E
  recomputed from scratch at each leaf):
  - Python: matches code/par for N = 3..9;
  - separate Go implementation: matches for N = 3..12.
  - the same Go implementation also matches at N = 13 (TOTAL 184400910, every c_f equal).
- Monte Carlo check of Lemmas 0-2 on random configurations: 290 + 1563 tree paths in d = 3 (p = 0.33 and 0.45)
  and 701 + 1216 in d = 2 (p = 0.62 and 0.75).
  - Every tree path was a NAW, every site of F(gamma) was closed, and every tree child of v_N lay in E(gamma).
  - Mutation tests have power: reversing the corner rank rule, or weakening the shortcut gap to >= 2, each
    immediately produced an open F site.
- Null models:
  - The same criterion on Z^2 gives thresholds 0.4285, 0.4487, 0.4609, 0.4691 at N = 8, 12, 16, 20, all below
    p_c^site(Z^2) = 0.5927 and below the rigorous 0.556. No overshoot.
  - On Z^3 the threshold rises smoothly: 0.2546 (N = 12), 0.2598 (16), 0.2617 (18), 0.2633 (20), all below
    0.3116.
  - Sanity points: 1/5 passes and 0.3116 fails.
  - c_0(N) = 20N^2 - 8N + 14 holds for every N computed, including c_0 = 7854 at N = 20.
- N = 20 certificate table: I did not regenerate it. The protocol says I need not. I started a rerun, then
  stopped it after about 35 minutes when I saw another panel process already running the same N = 20 job; two
  runs would have halved each other's speed. The evidence that outputs/p20.txt is the true output of
  code/par/main.go is indirect:
  - the code is deterministic integer code that I reproduced byte-for-byte at N = 16 and 18;
  - it agrees with an independent brute force at N <= 13;
  - the c_0(N) pattern and the smooth threshold sequence are consistent with it;
  - the MANIFEST.sha256 hashes match.
  Because the margin is thin, the verdict relies on that table. The reproduction rerun is the decisive check.

## Stretch / quantifier hunt

- "Exhaustive enumeration of all 20-step NAWs" (CLAIM.md) really means exhaustive over orbit representatives,
  weighted by orbit size. Lemma 4 proves the two are equivalent, so this is not a stretch.
- The bound is claimed only at p* and below. Nothing is claimed for N or p values that were not computed.
- The margin is thin (relative 2.8e-5). The result is exactly as good as the integer table in outputs/p20.txt.
  No float or estimate enters the logical chain.
- No non-rigorous estimate is presented as a bound. 5/19 is labelled correctly as unproven.

## Addendum (2026-10-19): re-check against the corrected claim/

The coordinator reported that the claim was corrected after my copy was made: the NOVELTY skeptic found that the
record is 0.2522, not 0.21103. I re-checked clause 6 against the authoritative claim/ folder. This was reading and
light arithmetic only; I modified nothing under claim/.

What changed:
- `diff -rq` between my copy and the corrected claim/ shows exactly four differing files: CLAIM.md,
  table/literature_record.md, result/bound.json and MANIFEST.sha256.
- PROOF.md, REPRODUCE.md, every file in code/ and every file in outputs/ are byte-identical to my copy. So
  sections 1-5 of my analysis, and every computation above, still apply to the corrected claim unchanged.
- The corrected MANIFEST.sha256 matches all 16 files in claim/, and there are no unlisted files.

What the corrected record says, and whether it is consistent:
- All three changed files now name the same record: Georgakopoulos-Panagiotis, arXiv:2107.06272, eq. (16),
  p_c^site(Z^3) > 0.2522, obtained from their inequality (4) and Barequet-Shalah's 9.3835. The exact value they
  give is 0.252265. Ponitz-Tittmann's 0.21103 is demoted to an older bound, and 5/19 is still labelled unproven.
- In result/bound.json, margin_over_record (0.011111 against 0.252265, 0.011176 against 0.2522) matches my own
  arithmetic.

The 0.2522 figure, checked in the PDF:
- The sha256 of the run's data/georgakopoulos_panagiotis_arxiv_2107.06272.pdf matches the hash recorded in
  table/literature_record.md (0299c673...).
- On p. 4, inequality (4) reads a(Z^d) >= b(Z^d) >= b_{r(p_c)}(Z^d) = f(r(p_c(Z^d))), with f(r) =
  (1+r)^(1+r)/r^r and r(p) = (1-p)/p. The text says it "applies verbatim to the site versions".
- On p. 14, eq. (16) reads p_c^site(Z^3) > r^-1 o f^-1(9.3835) > 0.2522, from Barequet-Shalah's site-animal
  bound of 9.3835. The paper calls this the best rigorous bound known. It also says the earlier best was about
  0.21225, via the connective constant.

My arithmetic (60-digit Decimal):
- f is increasing, since d/dr log f = ln((1+r)/r) > 0. So the comparison can be done through f.
- f^-1(9.3835) = 2.96407975..., which gives r^-1(f^-1(9.3835)) = 1/(1 + 2.96407975...) = 0.25226536.
- For p* = 263376/10^6: r(p*) = 736624/263376 = 2.79685..., and f(r(p*)) = 8.92725 < 9.3835.
- Hence p* > 0.25226536, by 0.0111106. Against the rounded 0.2522 the margin is 0.011176. The gap (8.927 vs
  9.3835) is far larger than any rounding error.
- p* is therefore strictly above the corrected record. It is also above 5/19 = 0.263158, which is still unproven,
  and above 1/5 and 1/6.

Nits (none of them changes clause 6):
- result/bound.json gives the record source as "arXiv:2107.06272 / CPC 2023". The 0.2522 appears in Part II,
  which is arXiv-only ("no journal version found", per table/literature_record.md). CPC 2023 is Part I, which
  contains Proposition 4.6, the basis of (4).
- CLAIM.md and the table write a(Z^3) where the paper's 9.3835 is the site-animal rate (written with a dot over
  the a).
- I did not re-check the Torquato-Jiao wording, which changed from "proved 1/5" to "proved 1/6". All of their
  values (1/6, 1/5, 5/19) are below p* anyway.
- Whether 0.2522 is the complete record is still the NOVELTY skeptic's call.

Result: clause 6 holds against the corrected claim. p* = 263376/10^6 is strictly above the stated record 0.2522
(exact 0.252265...). My verdict is unchanged.

## Verdict

Within my remit, the criterion is met literally:
- rigorous proof: verified;
- explicit rational p*: verified;
- exhaustive exact-integer computation with Fraction verification: verified;
- rerunnable code: verified;
- strictly above the record the corrected claim states (0.2522, exact 0.252265, Georgakopoulos-Panagiotis):
  verified, by 0.0111.

Two things lie outside my evidence and are the other skeptics' checks: whether the record is complete (no
published or implied bound at or above 0.263376), and a full N = 20 regeneration of outputs/p20.txt. If either
fails, this pass should be overridden.

confirmed_scope: PROOF.md correctly proves that K_N(p) < 1 implies p_c^site(Z^3) >= p; code/par/main.go computes the exact integer coefficients c_f of K_N as PROOF.md defines them (byte-identical reruns at N = 16 and 18, agreement with an independent brute force for N <= 13); and the N = 20 table in outputs/p20.txt (not regenerated by me) gives K_20(263376/10^6) = 0.99997153 < 1 in exact rational arithmetic, so p_c^site(Z^3) >= 263376/10^6 = 0.263376, strictly above the record that the corrected claim states in table/literature_record.md (Georgakopoulos-Panagiotis, arXiv:2107.06272, eq. (16): p_c^site(Z^3) > 0.2522, exactly 0.2522653...) by 0.0111, and above the unproven 5/19.

pass: true
