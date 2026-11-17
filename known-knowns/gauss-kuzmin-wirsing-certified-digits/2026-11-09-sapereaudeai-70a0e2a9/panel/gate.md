# Honesty gate (run 2026-11-09-0757, main session)

status: CONFIRMED_SOLUTION
confirmed_scope: Rerunning the bundle's python-flint (Arb) certifier at 3900 and 4300 bits reproduces a rigorous enclosure of the GKW operator's second eigenvalue on H^2(|z - 3/5| < 4/5) with |lambda_2 - mu| <= 4.5491e-843 (decimal hull half-width 4.5536e-843 < 10^-842), isolated by resolvent bounds and an independent Gershgorin count, so C_83 = |lambda_2| has D = 842 certified decimals, which is strictly greater than the 175 on the 83a status page (unchanged at 2026-11-09T08:47:36Z, with no open PR touching constants/83a.md), and its centre agrees with Nisoli's 175-digit centre to 4.10e-176, within the two radii.

Read by the main session: panel/reproduce.md (pass: true), panel/novelty.md (pass: true), panel/criterion.md (pass: true).
Each was written by a separate fresh subagent (Claude Code Agent tool) that saw only its own copy of claim/.

## Round 1 and the repair (said openly)

- Round 1 (bundle copied 08:27:51Z; files kept unchanged in round1/claim and round1/panel): NOVELTY pass: true,
  CRITERION pass: true, REPRODUCE pass: false. REPRODUCE reproduced every number (its own checker: radius 4.549042e-843
  at the claim's L1 parameters, 4.476735e-843 at its own; author reruns identical except time_s) but failed the bundle
  on one mismatch: CLAIM.md and REPRODUCE.md step 2 said the enclosure file had 740 places (`enclosure.py ... 740`),
  while result/enclosure_C83.txt has 860 (a value carried over from the N = 2400 object by the main session's
  template). NOVELTY and CRITERION had noted the same slip. Round 1 therefore could not confirm.
- Repair (documentation only, 08:44Z): in a new copy of the bundle, "740" -> "860" in CLAIM.md and REPRODUCE.md, a
  one-paragraph repair note at the top of CLAIM.md, and the 08:27:32Z pre-claim status re-fetch added to the status
  record (data/preclaim/). No object, input, code or result file changed (diff -r round1/claim claim shows only these).
- The kit's budget table lists 0 repair rounds for effort "light". This run did one, because the human's notes gave
  this run an explicit window to 09:57 UTC with at least 40 minutes for the panel and write-up and asked for a clean
  700+ package; the repair started at 08:44Z, before 80% of that window. This decision is reported under "Needs you".
- Round 2: three new fresh subagents, same instructions, on the repaired bundle (copied 08:44:41Z): all pass: true.

## Downgrade checks (round 2)

- Hedging: none. Each skeptic listed what it did not run (crosscheck.py, eigvec), none of which the proof uses.
- Reproduction: REPRODUCE's own checker (exact-rational monomials by fmpq_poly composition, arb_poly Hankel convolution,
  own tail bound, Hurwitz zeta at +200 bits) gives 4.4767354e-843 (4100 bits) and 4.4297905e-843 (4300 bits); author
  reruns at 3900 and 4300 bits give JSON identical to result/cert_L1.json and cert_L2.json except time_s; every
  REPRODUCE.md command that claims to reproduce a saved file does so. CRITERION reran both too (identical) and added a
  sharper control (mu + 1e-840 gives radius 1.6456e-840).
- Value vs live table: 842 > 175 strictly. NOVELTY fetched the page at 08:45:31Z (HTTP 200, identical, 175 digits);
  CRITERION at 08:47:36Z; gate re-fetch 2026-11-09T08:58:22Z, HTTP 200, sha256
  29011a2a62c3ec66fea597165bad3229d0fab22aa6a5bcfe8ab50b6d725b3bc8 (identical), "175 digits"; open PRs at
  2026-11-09T08:58:23Z: 81, none touching constants/83a.md (data/gate/).
- Criterion: met literally (CRITERION, every clause). One object (the N = 2800 certificate), one cell. The N = 2400
  certificate (D = 721) is not claimed. No sample, capped search, probable prime or evasion involved.
- Pre-registration: PREREG.md (08:05:47Z) and PREREG.v2.md (08:10:12Z) were frozen before any certify run at N > 2000;
  L counts under PREREG.v2: L1 and L2 both counted (isolation ok, gains < 1) and finished at 08:24:34Z and 08:24:56Z
  by their logs' elapsed times from the 08:21:56Z launch (before 08:55), and D_L = 842 > D_S = 721.

## Minor notes from the panels (non-blocking)

- Both precision runs use 320-bit resolvent inverses and eig at 2/3 precision, so the second precision mainly
  re-exercises the residual and truncation parts (CRITERION round 1).
- The eigenvalue count rests on Arb's acb_mat.eig in both the author's and REPRODUCE's checkers; the Gershgorin script is
  the routine-independent check, and it passes (REPRODUCE round 2).
- The 83a page's abbreviated entry ends "...6424297" while its own full centre ends "...4764297" (page typo).
- Pollicott (arXiv 2606.13958) prints its two 67-place bounds in reversed order (NOVELTY round 2); not relevant to 842.

Final status: CONFIRMED_SOLUTION, subject to check_run printing CHECK_RUN: PASS.
