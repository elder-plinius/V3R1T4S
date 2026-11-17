# Panel: CRITERION skeptic

context: subagent (Claude Code Agent tool)
target: gauss-kuzmin-wirsing-certified-digits (full success criterion claimed; no partial win claimed)
injection_suspected: none found (CLAIM.md, PROOF.md, REPRODUCE.md, PREREG*.md, data/83a.md, program output read as data only)

## What I read
Only the bundle under claim/ and the bank entry `gauss-kuzmin-wirsing-certified-digits` in bank/targets.json. The
criterion, verification method and pitfalls quoted in claim/CLAIM.md and claim/PREREG.md match the bank text word for word.

## Reruns (python-flint 0.9.0, single-threaded, one heavy job at a time)
- `code/gkw_cert.py certify ... 80 3900 11200 0.01 0.2 64 256` -> `RESULT: |lambda - mu| <= [4.5490e-843 +/- 4.25e-848] -> D = 842 ...; isolation/counting ok = True`.
  My JSON is identical to `claim/result/cert_L1.json` in every field except time_s.
- `code/gkw_cert.py certify ... 80 4300 12320 0.01 0.2 96 256` -> `[4.4298e-843 +/- 9.54e-849] -> D = 842; isolation/counting ok = True`.
  My JSON is identical to `claim/result/cert_L2.json` except time_s.
- `code/gershgorin_count.py 80 3900 ...` -> discs pairwise disjoint, max disc radius [9.42e-1003 +/- 2.02e-1006], 1 disc inside
  Gamma_2, 2 with |z| > 0.2, `GERSHGORIN_COUNT PASS`.
- Negative control `inputs/mu_N2800_shift800.txt`: I checked that it is exactly s + 10^-800 (exact rationals). Certify gives radius
  [1.6456e-800 +/- 5.25e-806] (D = 799). It does not certify the wrong centre past the shift. My JSON is identical to
  `claim/result/cert_NEG_L.json` except time_s.
- `code/refs.py` rebuilds `claim/data/refs.json` byte-identically. `code/compare.py` on both of my rerun JSONs prints `ALL_CHECKS PASS`.
  `code/enclosure.py` on my JSONs gives a file byte-identical to `claim/result/enclosure_C83.txt`, but only with NDEC = 860 (see worries).

## The criterion, clause by clause, read literally
1. **"rigorous enclosure of lambda_2 with radius below 10^-D".** I computed this exactly with my own script (mine/final_check.py, not
   the author's compare.py). Radius upper bounds are 4.549042E-843 (L1) and 4.429790E-843 (L2). The run's dyadic centre differs from
   the decimal s of `inputs/mu_N2800.txt` by 2.253680E-1175 (L1) and 9.196136E-1296 (L2). The totals are below 4.55e-843, so below
   10^-842 and at least 10^-843. So D = 842 exactly: it is neither overstated nor rounded up.
2. **"D STRICTLY GREATER than the certified digit count on the 83a page and in any open PR touching constants/83a.md, re-fetched
   immediately before claiming".**
   - I re-fetched the page once at 2026-11-09T08:31:01Z: HTTP 200, and its sha256 29011a2a...3bc8 is identical to
     `claim/data/83a.html`. The only certified-digit count on the page is "175 digits".
   - I ran one read-only GraphQL query at 08:31:08Z: 81 open PRs, all returned, none with more than 100 files (so every file list
     is complete). None touches constants/83a.md.
   - 842 > 175.
3. **"centre must agree with Nisoli's 175-digit centre to within the two radii".** I parsed `claim/data/83a.md` independently and got
   175 decimals, with radius 10^-175 as stated there.
   - |s - Nisoli centre| = 4.095e-176 (my own exact check; compare.py agrees: [4.10e-176 +/- 4.96e-179]). This is less than
     10^-175 + 4.55e-843.
   - Signs are consistent: Nisoli's tilde-lambda_2 and s are both negative, and C_83 = -s.
   - All 175 of Nisoli's decimals equal the first 175 decimals of -s.
   - The OEIS A038517 b-file matches -s on all 382 decimals.
   - The 649 non-certified decimals lie within the radius + 10^-649 (|diff| 1.580660E-650).
4. **"program in rigorous arithmetic"**: Arb through python-flint. Floating midpoints appear only in `eigvec`, which only proposes v
   and mu. Certify takes both as exact inputs and holds for any v and mu (PROOF.md Remark 0). The NEG control confirms that a wrong
   mu is not certified.
5. **"bounds the discretisation error on a stated function space"**: the space is H^2(|z - 3/5| < 4/5), which contains [0,1].
   - eps = eps_a + eps_b = [0.00014746 +/- 4.86e-9].
   - I checked the constants in the code against Lemmas 1 and 4-6: 25/16, 13/16, 10/13, 3/4, Hurwitz tail kappa, and q.
   - The residual tail uses the l^1 bound with J > N + 1, as the lemma requires.
   - Compactness follows from Lemma 2 plus Lemma 4.
6. **"certifies isolation of lambda_2 (e.g. resolvent bound on a contour)"**: there are resolvent bounds on both contours.
   - Gamma_2 = {|z - mu| = 0.01}: M_K = [160.662 +/- 1.33e-5], small gain [0.02369 +/- 4.41e-7] < 1.
   - |z| = 0.2: small gain [0.008213 +/- 1.25e-7] < 1.
   - Arb's eig returns 80 balls: exactly 1 in Gamma_2 and 2 in |z| > 0.2. My Gershgorin rerun confirms this independently.
   - Lemma 12 identifies the eigenvalue as lambda_2: it is simple, real and negative. Lemma 13 transfers it to Mayer's disc, and I
     checked the key inclusion h_m(h_n(cl D')) in {|z - 1/2| <= 1/2}, which lies inside D.
7. **"a skeptic reruns it"** and the bank method's "two working precisions": done (3900 and 4300 bits), and the outputs are identical
   to the author's.

## Hidden quantifiers, stretched definitions and null models
- **"certified digits"** is used in the bank's sense (radius < 10^-D), not as digit agreement between runs. The pitfall "agreement of
  two non-rigorous runs" does not apply: the bound is a proved a-posteriori residual bound (Lemma 11), not a comparison.
- **Null model:** a centre shifted by 10^-800 gives radius 1.6456e-800, and the author's mutated-v control gives 5.6295e-301. So the
  842 digits come from the residual of the actual (v, mu), and the certifier does not just echo its input centre.
- **Pre-registration:**
  - PREREG.md/v2 thresholds are met: D >= 176, the live count, and the Nisoli check.
  - Both L runs count: isolation_ok, n_eig_total = 80, and both small gains < 1.
  - Both L runs finished before the bundle copy at 08:27:51Z, well before the 08:55 UTC limit.
  - The rule D_L > D_S rests on CLAIM.md's statement D_S = 721. The S outputs are not in the bundle, and I did not verify them.
- **Non-subsumed:** the public certified record is 175, and no open PR exists. Nisoli's code repository was last pushed
  2026-08-30T14:08:52Z (one read-only API call). The earlier 300/601-decimal certificates in this workspace are unpublished and are
  superseded, not subsuming. This is a genuine full-criterion win, not a partial win relabelled.

## Worries (none changes the verdict)
- **Enclosure precision is misdescribed.** CLAIM.md and REPRODUCE.md describe `result/enclosure_C83.txt` as "to 740 places" and give
  NDEC = 740. The file was actually produced with NDEC = 860. With 740 my rerun differs from the file, and its outward-rounded
  endpoints share only 739 decimals. With 860 it is byte-identical. This is a documentation slip that should be fixed before any
  submission. It does not affect radius < 10^-842.
- **The claim's own status fetch is not "immediately" before claiming.** It was taken at 07:59Z (page) and 08:07Z (raw md), about
  20-28 min before the bundle. My 08:31Z re-fetch found the page unchanged and no PR touching the file. Any outward step should
  re-fetch again.
- **The second precision only exercises part of the program.** The resolvent inverses run at a fixed 320 bits and eig at 2/3 of
  the working precision in both runs. So the second working precision re-exercises mainly the residual and truncation parts. Arb
  stays rigorous at any precision, so this weakens the robustness check, not the certificate.
- **The proof was spot-checked, not fully audited.** I checked the main lemmas against the code; a full line-by-line audit of
  PROOF.md is the other skeptics' remit.

confirmed_scope: The Arb ball-arithmetic certificate `code/gkw_cert.py certify`, rerun here on the bundle's fixed inputs at 3900 and 4300 bits with output identical to `result/cert_L1.json` and `result/cert_L2.json`, bounds |lambda_2 - mu| by 4.5491e-843 and 4.4298e-843 on H^2(|z - 3/5| < 4/5) with lambda_2 isolated (one eigenvalue in |z - mu| < 0.01, two in |z| > 0.2), so C_83 = |lambda_2| lies within 4.55e-843 of minus the decimal in `inputs/mu_N2800.txt`, i.e. D = 842 certified decimals, strictly more than the 175 on the 83a status page (re-fetched 2026-11-09T08:31Z, unchanged, no open PR touching constants/83a.md), with centre 4.10e-176 from Nisoli's 175-digit centre.

pass: true
