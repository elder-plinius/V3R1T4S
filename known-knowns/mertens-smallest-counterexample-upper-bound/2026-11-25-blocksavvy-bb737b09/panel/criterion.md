# CRITERION skeptic: claim p4 (mertens-smallest-counterexample-upper-bound)

context: fresh-context knowledgeWork skeptic, sandbox panel-0045-criterion

Written 2026-11-25T04:41Z (`date -u`). I read only claim/ and RULES.md in the sandbox. I did not open private/ or any credentials, and I took no outward action.
Light local checks only: SHA256SUMS, the checker on the saved chunks, chunk metadata and contiguity, and 8 single-core chunk
recomputations (about 70 s of CPU in total, run under nice 19). The checks used python-flint 0.9.0 in a throwaway venv inside the sandbox.

## Bank text tested (p4, quoted verbatim in claim/CLAIM.md)
"An independent check of the bzyzz/mertens_bound certificate, done with separately written code: either the
ball-arithmetic K_2 sum at its point over all zeros below 1.3e6, or ...; the result either confirms it or documents a
concrete error." The claim uses only the first option.

## Check 1: separately written code
- code/k2_chunks.py (about 40 lines) and code/aggregate_claim.py are this run's own code. They are structurally unlike the
  certificate's certify_K2.py/certio.py: they use no HI_DPS/LO_DPS split, no batch-250 cache, and a different chunk layout. The certificate records those code hashes, and its code is not in the package.
- Shared dependency: both codes get their zeros from FLINT/Arb's acb_dirichlet_zeta_zeros (python-flint acb.zeta_zeros). The
  bzyzz README lists this routine as a dependency. So the code is separately written, but the zero computation is not
  independent of the certificate's. p4 asks only for "separately written code", so this check is met. The caveat must be stated (see the wording fixes).
- Result: MET.

## Check 2: ALL zeros below 1.3e6 (count, boundary)
- sha256sum -c SHA256SUMS.txt: all files OK. Every file except SHA256SUMS.txt itself is listed.
- Chunk metadata: chunks_head128 has 1,500 files, all prec 128, all cnt 400 (n = 1..600,000). chunks_tail has 4,314 files, all prec 96,
  cnt 400 except a final cnt 373 at n0 = 2,325,201 (n = 600,001..2,325,573). Every filename matches its n0/cnt. Head and tail are contiguous with no
  gaps. g_last < g_first holds across every chunk boundary. The first zero is gamma_1 = 14.1347... The checker finds no stray files (kh = fh, kt = ft).
- Boundary: the checker recomputes gamma_2325572 = [1299999.536327494617836 +/- 4.03e-16] < 1.3e6 <
  gamma_2325573 = [1300000.182865248898197 +/- 1.77e-16] and subtracts the n = 2,325,573 term. Because the zeros come by
  rigorous index, N(T0) = 2,325,572. This agrees with the certificate's N_T0 = 2325572 and with its delta_lower
  [0.182865248898197 +/- 1.77e-16] (= gamma_2325573 - T0).
- Caveat: N(T0) = 2,325,572 is not recomputed independently by zeta_nzeros (python-flint 0.9.0 does not expose it). It
  rests on the index-rigour of Arb's zeta_zeros, which the certificate shares.
- Result: MET.

## Check 3: ball arithmetic
- Every term is an arb/acb ball: zeta'(rho) comes from acb_series at the zero ball, and exp(-k g^2) and exp(i g v)/(rho zeta') are balls too. The phase
  error (gamma radius x v ~ 3.5e18) is carried by the balls. That is why the 96-bit head ball is wide ([1.0003 +/- 1.68e-5])
  and the 128-bit head ball is tight. Chunk sums are stored as Arb radius strings (str(..., radius=True), which encloses the ball) and re-read and
  summed at 192 bits. Min |zeta'(rho)| over all chunks is 0.10901933652..., so no division by a ball containing 0 occurs.
- I reran `python code/aggregate_claim.py`: its output is byte-identical to result/aggregate_claim.json. With `chunks_head` it is
  byte-identical to result/aggregate_claim_head96.json.
- I recomputed 8 chunks from scratch with code/k2_chunks.py and got S, Abs, g_first and g_last identical to the saved files: head128 n0 = 1, 40801, 54401,
  516001; tail n0 = 654401, 1262001, 2148801, and the boundary chunk 2325201 (cnt 373). This is a spot check only.
- For all 1,500 head chunks, the 128-bit S ball overlaps the 96-bit S ball.
- Result: MET.

## Check 4: comparison with the certificate
- Our K2 = [1.00030525038651 +/- 5.07e-15]. arb containment test: it is CONTAINED in the certificate's K2 = [1.0003052504 +/- 2.30e-11]
  (the checker itself only tests overlap; I tested containment separately).
- Head part [1.00030525038650 +/- 4.03e-15] overlaps the certificate's K2_main [1.000305250386499012059 +/- 3.21e-22].
- Tail part [1.3e-14 +/- 9.56e-16] lies inside the certificate's K2_tail_ball [+/- 9.43e-12], so the certificate's tail bound is
  consistent with the tail as evaluated.
- lower(K2 - E - 1) = 3.0525036e-4 > 0 with E = 2.391e-11. Our lower end also exceeds the certificate's K2_lower_ball by 9.43e-12.
- E itself is a hard-coded constant in aggregate_claim.py, and no file in the package gives its source (the bzyzz README says only
  "E <= 2.4e-11"). E comes from J1..J6 and M, so it is taken from the certificate and not checked.
- Result: MET. The outcome "confirms it" is supported for the K_2 sum and the inequality K2 > 1 + E at the certificate's E.

## Check 5: no stretch to reviewing the whole bzyzz bound
- The "Not claimed" section of CLAIM.md says explicitly that Pintz Theorem A / Corollary A as used (Y = e^u), Pintz Lemmas 4-5, J1..J6
  and the 1/zeta constant M = 22.767 are not checked, that the bzyzz bound is not made reviewed, and that no new bound and no p1/p2/p3 are claimed.
- Minor stretch: "J1..J6 (numerically reproduced in an earlier run of ours, ...)" asserts work that has no evidence in the
  package. It is fenced as "not part of this claim", but it should be removed or cited (fix 3).
- The closing sentence "This confirms the K_2 inequality of the certificate" is acceptable only with E marked as taken from the certificate (fix 2).
- Result: MET, given the wording fixes below.

confirmed_scope: With separately written python-flint/Arb ball-arithmetic code, the K_2 sum of the bzyzz/mertens_bound certificate at v = 3484971332733132396.5383341489440461, k = 1.5e-10, over all 2,325,572 zeta zeros with 0 < gamma < 1.3e6 (zeros from Arb's acb_dirichlet_zeta_zeros, which the certificate also uses) is enclosed in [1.00030525038651 +- 5.07e-15]; this ball lies inside the certificate's K2 ball [1.0003052504 +- 2.30e-11] and exceeds 1 + E by 3.0525e-4 at the certificate's own, here unchecked, E = 2.391e-11, which confirms the certificate's K_2 inequality and finds no error in it, while Pintz Theorem A/Corollary A as used, Pintz Lemmas 4-5, J1..J6 (hence E) and the 1/zeta constant M remain unchecked.

## Required wording fixes (none changes the verdict)
1. State the shared dependency: zeros and their indexing come from the same Arb routine (acb_dirichlet_zeta_zeros) that the
   certificate uses. The code is separately written, but the zeros are not independently computed, and N(T0) relies on Arb's index rigour.
2. Give the source of E = 2.391e-11 (the bzyzz THEOREM.md / check_theorem.py value) and say that it is taken from the certificate and
   unchecked. Change the final sentence to "This confirms the certificate's K_2 inequality K2 > 1 + E at its stated E, and finds no error in the K_2 sum."
3. Remove "(numerically reproduced in an earlier run of ours, ...)", or cite that run's evidence. As written it is an unevidenced side claim.
4. Files section and the k2_chunks.py docstring: "per-chunk sums (96-bit arb balls)" is wrong for chunks_head128 (128 bits). Say
   "precision given by the PREC argument (128 for chunks_head128, 96 for chunks_head and chunks_tail)".
5. RULES.md rule 1: add a label to the claim. Suggested: `NUMERICAL` (rigorous ball-arithmetic computation; bzyzz criterion unreviewed).
6. Optional: make aggregate_claim.py test containment (bz.contains(K2)) and not only overlap, since CLAIM.md says "lies inside".

pass: true
