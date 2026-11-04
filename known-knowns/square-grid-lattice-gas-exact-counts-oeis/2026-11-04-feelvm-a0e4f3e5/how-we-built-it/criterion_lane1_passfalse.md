# CRITERION skeptic — verdict on the A054759 a(15) p1 partial win

context: subagent

Scope: I judge the claim package in claim/ only (CLAIM.md, REPRODUCE.md, value.txt,
residues_run1.json, residues_run2.json, crt_check.py, crt_check_output.json,
ladder_run1.json, ladder_run2.json, growth.json, programs/iso_row.py, programs/iso_ht.py),
against the bank criterion and the p1 partial text quoted verbatim in CLAIM.md
("same two-run and reproduction rules" as the full criterion). All arithmetic below was
recomputed independently by me (stdlib-only script, run with python -I); I did not rerun
the claimant's programs — authenticity-of-execution is the numeric skeptic's fresh-prime
lane; my judgments are on the recorded evidence's internal consistency and sufficiency.

## Clause 1 — N = one more than the largest DATA index, b-file re-fetched live immediately before claiming

VERDICT: PASS (with a recording caveat).

- CLAIM.md status facts: live OEIS DATA and b-file for A054759 end at n = 14
  (a(14) = 15844635835975276495290739119895808472, Brendan McKay, Apr 18 2024), re-fetched
  at 18:09:53Z on 2026-11-04, immediately before the claim (claim file written 19:11). So
  N = 14 + 1 = 15, and the claim is exactly a(15). Consistent throughout the package.
- The recorded fetch also asserts the negative check that the claimed a(15) value appears
  nowhere in the live entry — the right check to rule out a already-published "unknown" term.
- CAVEAT (flagged, not fatal): the fetches are recorded as timestamped summary assertions,
  not raw captures or hashes of the HTTP responses. I cannot re-fetch, so I judge from the
  recording; it is internally consistent (the recorded a(14) matches the ladder b-file
  entries exactly) and adequate here because the bank's own verification method directs the
  skeptic to re-check the b-file live. The panel should note the limitation.

## Clause 2 — two independent runs, exact agreement (different primes/CRT sets AND different decomposition)

VERDICT: PASS on the recorded evidence.

- Prime sets: 14 + 14 primes. I verified every prime is prime, distinct within its set, and
  congruent 1 (mod 15) as the programs require. Sets are disjoint: run1 = {31231..32611},
  run2 = {30091..31081}. residues_run2.json honestly documents that an overlapping prime
  (32611) was replaced by fresh 30091 with the CRT recomputed — good hygiene, not a defect.
- CRT: I recomputed both CRT reconstructions independently (my own implementation, not
  crt_check.py). Both reconstruct exactly value.txt = 4310182149988584261406143524214457416387448;
  all 28 recorded residues equal value.txt mod their prime individually. Residue count and
  the recorded "modulus" fields check out.
- Sufficiency of each run alone: rigorous bound 2^15 * 1220^15 = 646915258962549275091904510950375424000000000000000
  = 2^168.79 (I verified the recorded bound equals this recomputation exactly). Run-1
  modulus = 2^209.52, run-2 modulus = 2^208.61. EACH modulus alone exceeds the bound by
  2^40.7 and 2^39.8 respectively, and each alone exceeds the value — so either residue set
  on its own uniquely determines the integer. The two runs do not share CRT capacity; the
  agreement is a genuine two-run exact agreement, with margin far beyond the "x 1e6 margin"
  REPRODUCE.md claims (actual margin ~2^40).
- Different decomposition/state encoding: I read programs/iso_row.py and programs/iso_ht.py.
  Run-1: 2^15-state row transfer matrix, wrap edge integrated into the transfer element,
  flip-set enumeration of alternating cyclic flips. Run-2: 2^16-state (s, c) space with the
  wrap-edge direction carried explicitly, independent per-row walk-DFS transfer element,
  orbit-pair isotypic extraction. Different state spaces AND different transfer-element
  constructions — the criterion's "different primes/CRT moduli sets AND a different
  decomposition ... or a different state encoding" is satisfied on both branches.
- Residual risk (recorded residues could in principle not be the programs' actual outputs)
  is exactly what the bank's verification method (fresh-prime rerun) and the numeric
  skeptic cover; nothing in the package is inconsistent with authenticity.

## Clause 3 — same code reproducing every published term for n <= N-1 = 14

VERDICT: PASS (on the recorded ladders, with a reading note).

- ladder_run1.json and ladder_run2.json both contain n = 1..14 with every entry marked
  matches/isotypic_matches = true. I verified every recorded congruence independently:
  isotypic_mod == bfile mod validation prime for all 28 entries; run-1's "ref" fields are
  consistent too (exact published integer for n = 1..7; direct_mod refs for n = 8..14 match
  bfile mod p = 17, 19, 31, 23, 37, 53, 29). The b-file values are identical across the two
  ladder files, and a(14) matches the status-fact value in CLAIM.md.
- Validation primes {101, 103, 109, 113, 131, 199} are disjoint from the claim primes
  (31231..32611 and 30091..31081), as required — the ladder checks are not rigged by the
  claim's own moduli.
- Reading note (flagged, judged satisfied): "reproducing exactly" is implemented as exact
  modular agreement with the published b-file terms (one validation prime per n per code),
  not full big-integer equality for n >= 3; for n <= 7 the recorded ref IS the exact
  published integer. This matches the bank's own operationalization ("rerun for all n <= 20
  and compare with the b-file") and the purpose of the clause (validating the code against
  independently published values). A skeptic can rerun any n with any fresh prime.

## Clause 4 — growth constant: a(N)^(1/N^2) within 1e-3 of the entropy constant

VERDICT: LITERAL FAIL — and the failure is a defect of the criterion's tolerance at N = 15,
not of the value.

- Literal check: ln(a(15)^(1/225)) - ln W = 0.43630912920511505 - 0.4315231086776713 =
  0.004786020527443757 (I recomputed from value.txt; matches growth.json's
  literal_logdiff exactly). 0.004786 > 1e-3, so the clause as written FAILS.
- It fails for ANY correct value at N = 15. The published terms themselves deviate the same
  way: for every published n = 4..14, d(n) = ln a(n)/n^2 - ln W satisfies n^2 * d(n) ≈ 1.077-1.092
  (my recomputation from the ladder b-file values):

    n=4: 0.068247 (n^2 d = 1.0919)    n=10: 0.010779 (1.0779)
    n=5: 0.043363 (1.0841)            n=11: 0.008904 (1.0774)
    n=6: 0.030025 (1.0809)            n=12: 0.007483 (1.0775)
    n=7: 0.022027 (1.0793)            n=13: 0.006373 (1.0770)
    n=8: 0.016854 (1.0786)            n=14: 0.005497 (1.0774)
    n=9: 0.013308 (1.0780)            n=15 (computed): 0.004786 (1.0769)

  The PUBLISHED a(14) fails the literal 1e-3 clause by MORE than the claimed a(15)
  (0.005497 vs 0.004786), and the computed a(15)'s deviation continues the published
  sequence's own trend seamlessly. The deviation decays like ~1.08/n^2 (Lieb's constant is
  a thermodynamic limit); the literal tolerance first becomes attainable only at N >= 33.
  Stated plainly: the literal clause fails at N = 15 for ANY correct value, as witnessed by
  the published a(14).
- The value itself is consistent with the entropy constant under the documented finite-size
  model: growth.json's model prediction (fitA = 1.0753, fitB = 0.0252, in a model
  ln a(n) = c n^2 + A + B/n) gives predicted_a15 with |log-ratio| to the computed value =
  1.354e-4 < 1e-3 — I verified the magnitude directly from the two integers. My independent
  refits agree: free-c fit gives c ≈ 0.4315333-0.4315378 (documented free_fit_c = 0.43153334,
  within 1.1e-5 of Lieb), and my predicted a(15) values land within 1.4e-4-2.8e-4 relative of
  the computed value. The finite-size-model check passes.
- Minor flags on growth.json (immaterial): (a) log_ratio_computed_vs_pred is recorded as
  +1.354e-4 but computed < predicted, so the log ratio is -1.354e-4 — the magnitude matches
  my recomputation exactly; a sign-convention slip. (b) fitA/fitB are not exactly
  reproducible by my unweighted A + B/n least squares (my n = 7..14 fit reproduces
  free_fit_c to 7 decimals; A, B differ in the 3rd decimal, presumably a different range or
  weighting); the prediction itself was verified directly from the integers, so nothing
  rests on the exact fitting recipe. (c) growth.json's lieb_lnW = 1.5 ln(4/3) =
  0.4315231086776713 is exact; CLAIM.md quotes the entry's "0.431523058..." (5e-8 off,
  likely entry rounding — irrelevant at 1e-3 scale).

## Clause 5 — digit-count sanity (bank verification method)

VERDICT: PASS. value.txt has 43 digits; the entropy estimate floor(225 * lnW / ln 10) + 1 = 43.
ln(v)/225 = 0.43630912920511505 (matches growth.json). Also a(15) > a(14) with ratio ~2.72e5,
in line with the growth model (e^(29 lnW + ~1.08) ≈ 2.7e5).

## Overall

Clauses 1, 2, 3, 5: PASS. Clause 4: the literal 1e-3 growth clause FAILS at N = 15 — for any
correct value whatsoever, as witnessed by the published a(14) deviating even more (5.50e-3)
and by n^2 * d(n) ≈ 1.08 across the entire published range; the value itself is consistent
with Lieb's constant under the documented (and independently refitted) finite-size model,
with |log-ratio| 1.35e-4. The claim package is otherwise exact, internally consistent, and
meets the two-run and reproduction rules with wide margins. Recommendation to the bank: the
growth clause needs recalibration for small N (e.g. tolerance max(1e-3, C/N^2) with C ~ 1.1,
or consistency with a pre-registered finite-size model); if recalibrated, no clause blocks.

pass: false

Failing clause: the growth-consistency clause as literally written ("a(N)^(1/N^2) within 1e-3
of the corresponding entropy constant") — fails at N = 15 (logdiff 4.786e-3) for any correct
value, a defect of the criterion's tolerance at N = 15, not of the claimed value.
