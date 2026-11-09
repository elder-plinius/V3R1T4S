# Panel skeptic: CRITERION

context: subagent (Claude Code Agent tool)
target: gauss-kuzmin-wirsing-certified-digits (criterion text checked against the bank entry, which matches `claim/CLAIM.md` verbatim)
claimed: the full success criterion, D = 842 (no partial win claimed)
injection_suspected: none seen

## What I ran (my own reruns, from the bundle's code and inputs)

Input and code hashes: the five `claim/inputs/*` sha256 values match `claim/REPRODUCE.md`.

| check | my result | bundle |
|---|---|---|
| certify L1 (3900 bits, J 11200, Q2 64) | `RESULT: \|lambda - mu\| <= [4.5490e-843 +/- 4.25e-848] -> D = 842 ... isolation/counting ok = True`; JSON radius `[4.54904e-843 +/- 2.41e-849]`, n_eig 80 / 1 inside Gamma_2 / 2 with \|z\| > 0.2, gains 0.02369 and 0.008213; 193.6 s (machine shared) | same JSON except `time_s` (156.7) |
| certify L2 (4300 bits, J 12320, Q2 96) | `RESULT: \|lambda - mu\| <= [4.4298e-843 +/- 9.54e-849] -> D = 842 ... ok = True`; radius `[4.42979e-843 +/- 4.67e-850]`, M_L(Gamma_2) 160.247, gains 0.02308 and 0.008213; 234.6 s | same JSON except `time_s` (178.6) |
| `code/compare.py` on my L1 and L2 JSONs (with refs rebuilt by `code/refs.py`) | `ALL_CHECKS PASS` both; output files byte-identical to `claim/result/compare_L1.txt` and `compare_L2.txt` | identical |
| `code/enclosure.py ... 860` on my two JSONs | byte-identical to `claim/result/enclosure_C83.txt`; hull half-width `[4.5535915e-843 +/- 4.76e-851] < 10^-842` | identical |
| `code/gershgorin_count.py 80 3900` | 80 pairwise disjoint discs, max radius `[9.42e-1003 +/- 2.02e-1006]`, 1 disc inside Gamma_2, 2 with \|z\| > 0.2, `GERSHGORIN_COUNT PASS` | same lines |
| my own null test (not in the bundle): same v, centre shifted by +10^-840 (two orders above the claimed radius) | `RESULT: \|lambda - mu\| <= [1.6456e-840 +/- 1.16e-845] -> D = 839`; eta 1.0000e-840 | n/a |

## Clause-by-clause reading of the criterion

1. "rigorous enclosure of lambda_2 with radius below 10^-D": the certified radii are 4.5491e-843 (L1) and 4.4298e-843 (L2)
   about each run's dyadic rounding of the decimal centre s; the decimal hull in `claim/result/enclosure_C83.txt` has
   half-width 4.5536e-843 (my exact-rational check of its 860-place endpoints). This is below 10^-842 and not below
   10^-843, so D = 842 exactly, with no rounding stretch. Both endpoints share their first 842 decimals, so the
   decimal-string reading of "842 certified decimals" also holds. Sign: lambda_2 < 0 is proved (Lemma 12: mu + r0 < 0)
   and all comparisons use C_83 = -mu (checked in `code/compare.py` and in my own exact-rational recomputation).
2. "D strictly greater than the count on the 83a page and in any open PR touching constants/83a.md, re-fetched immediately
   before claiming": I re-fetched the page myself at 2026-11-09T08:47:36Z (one request, HTTP 200). Its sha256,
   29011a2a62c3ec66fea597165bad3229d0fab22aa6a5bcfe8ab50b6d725b3bc8, is byte-identical to `claim/data/83a.html` and
   `claim/data/preclaim/83a.html`, and it still states "175 digits" (radius 10^{-175}). A read-only GraphQL listing of
   open PRs at 2026-11-09T08:47:50Z found 81 open PRs with untruncated file lists, none touching 83a, and the same PR
   set as `claim/data/preclaim/prs_open_files.json`. 842 > 175.
3. "centre must agree with Nisoli's 175-digit centre to within the two radii": independent exact-rational check from
   `claim/inputs/mu_N2800.txt` and the centre in `claim/data/83a.md`: |(-s) - Nisoli| = 4.095e-176 <= 10^-175 + 4.55e-843.
   True. Nisoli's interval also intersects the decimal hull. OEIS A038517 b-file (382 decimals): |(-s) - OEIS| = 6.16e-383,
   within radius + 10^-382.
4. "a program in rigorous arithmetic": python-flint 0.9.0 (Arb) ball arithmetic throughout `cmd_certify`. Floats appear only
   in the guess for D, which is then checked exactly (`rad < 10^-D` in arb). Exact rationals are used for the monomial
   change of basis.
5. "bounds the discretisation error on a stated function space": H^2 of the disc |z - 3/5| < 4/5, which contains [0,1]
   (real span (-1/5, 7/5)). Compactness: Lemma 2, a norm limit of finite-rank operators via Lemma 4. I checked Lemma 1's
   geometry in exact rationals (rho_1 = 13/16; rho_2 = 13/34; rho_n < 3/4, tending to 3/4). I checked that eps_a in the
   code is the formula of Lemma 4 (I recomputed 1.638e-7) and that the code's A_K and residual entries match Lemma 3's
   Hurwitz-zeta formula. The residual in Lemma 7 is for the true operator L (head computed exactly in balls for j < J,
   plus a proved l1 tail), not for a truncation. The bank's "for example H^inf" is an example, not a requirement. Lemma 13
   ties the eigenvalues to Mayer's disc, so this is the classical lambda_2, and the agreement with Nisoli and OEIS
   corroborates that.
6. "certifies isolation of lambda_2 (for example by a resolvent bound on a contour)": the resolvent is sampled on
   Gamma_2 = {|z - mu| = 1/100} and on |z| = 1/5, with Neumann interpolation between the samples, and the small-gain
   homotopy (Lemma 9) gives exactly one simple eigenvalue inside Gamma_2 and exactly two (1 and lambda) in |z| > 1/5, so
   lambda is lambda_2. The A_K counts are confirmed twice: by acb_mat.eig, whose docstring in the installed python-flint
   0.9.0 says that with default options "the method only succeeds if all eigenvalues can be isolated" (it raises
   otherwise), and by my rerun of the independent Gershgorin count.
7. "a skeptic reruns it" / bank method "rerun the certifier at two working precisions": done above (3900 and 4300 bits).
   Results are identical to the bundle's JSONs in every field except wall time.

## Null models

- Bundle control `claim/result/cert_NEG_L.log`: a +10^-800 shift gives radius 1.6456e-800 (D 799). The control
  `claim/result/cert_MUT_v1000flipped.log` (one sign of v flipped) gives radius 5.6295e-301 (D 300). Neither certifies the
  perturbation away.
- My sharper control: a +10^-840 shift gives radius 1.6456e-840 >= 10^-840 - 4.55e-843, consistent with the true
  lambda_2 lying 10^-840 from the shifted centre. The certifier does not shrink the radius below the real distance even
  two orders above the claimed radius, so the 4.5e-843 radius is not produced by the centre alone.
- The two runs share v and s, so their agreement shows numerical stability, not independent correctness. Correctness
  rests on PROOF.md plus Arb. Remark 0, that the certificate holds for any centre, is consistent with both shift controls.

## Hidden quantifiers, subsumption and pre-registration

- Full criterion, not a partial win. Nothing public subsumes it: the page and the open PRs give 175. The workspace's
  earlier 601- and 721-decimal certificates are stated to be unsubmitted and are smaller, so they do not subsume this one.
- PREREG.v2 fixes object L (N 2800; L1 at 3900 bits / J 11200 / Q2 64; L2 at 4300 bits / J 12320 / Q2 96; K 80;
  r0 0.01; rho 0.2; Qrho 256) and the count rule D = min(D_L1, D_L2) with isolation_ok and both gains < 1. The claimed
  runs and parameters match. Not verifiable from the bundle: PREREG.v2's condition that L1 and L2 finished by 08:55 UTC
  (the bundle's file times are copy times). The claim's pre-panel re-fetch at 08:27:32Z implies they finished earlier.
  That is the claim's statement, not something I checked.

## Not verified by me

- I did not do a full line-by-line audit of every lemma and of the code beyond the spot checks above (Lemmas 1, 3, 4, 8,
  11 and 12 against the code). Correctness of Arb/python-flint is assumed.
- Not run: `code/crosscheck.py`, the bundle's NEG_L and MUT controls (I read their logs and ran my own 10^-840 shift
  instead), and the eigvec step (excluded by instruction).

confirmed_scope: Rerunning the bundle's python-flint (Arb) certifier at 3900 and 4300 bits reproduces a rigorous enclosure of the GKW operator's second eigenvalue on H^2(|z - 3/5| < 4/5) with |lambda_2 - mu| <= 4.5491e-843 (decimal hull half-width 4.5536e-843 < 10^-842), isolated by resolvent bounds and an independent Gershgorin count, so C_83 = |lambda_2| has D = 842 certified decimals, which is strictly greater than the 175 on the 83a status page (unchanged at 2026-11-09T08:47:36Z, with no open PR touching constants/83a.md), and its centre agrees with Nisoli's 175-digit centre to 4.10e-176, within the two radii.

pass: true
