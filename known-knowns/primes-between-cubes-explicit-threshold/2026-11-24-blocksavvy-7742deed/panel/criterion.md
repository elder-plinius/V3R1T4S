role: criterion
context: fresh subagent (CRITERION skeptic; saw only kit/RULES.md, PANEL_BRIEFS.md header + CRITERION section, PREREG.md, and a copy of claim/; did not open attempts/, notes/, scout.md, BRIEF.md or other panel files)
claim: For every integer n >= exp(exp(29.735)) there is a prime in (n^3 + 1/2, n^3 + 3n^2 + 1/2], hence in (n^3, (n+1)^3), assuming Yang's thesis zero-free region (I3) and Bellotti's preprint zero-density estimate (I4)
date_utc: Tue Nov 24 07:57:36 UTC 2026

## Criterion checked (PREREG.md, quoted verbatim in CLAIM.md)
"A complete written proof that for every integer n >= exp(exp(Y)) the interval (n^3, (n+1)^3) contains a prime, with
Y < 32.537, each analytic input cited by its exact statement and the final inequality certified by outward-rounded
interval arithmetic ... Scope words must name any input that is a thesis or a preprint."
Frozen thresholds: beats the record iff Y_cert <= 32.527 at prec 128 and 256 and the standalone checker agrees;
"meaningful drop" iff Y_cert <= 32.337.

## (a) Hidden quantifiers / stretched definitions
- n integer >= exp(e^Y)  =>  X = log(n^3 + 1/2) > 3 log n >= 3 e^Y = X0. x = n^3 + 1/2 and y = n^3 + 3n^2 + 1/2 are
  half odd integers for EVERY integer n (n^3 is an integer), so I1's "half odd integers x >= x_K" restriction costs
  nothing; y < (n+1)^3 = n^3 + 3n^2 + 3n + 1. No restriction to special n. PROVED-HERE (re-derived).
- Validity ranges, for every X >= X0 (X0 = 2.4596e13, L0 = log T0 = 8.1987e12, out/main_prec128.txt):
  I1 needs 50 < T < x and log x >= 10^6 (Table 2, K = 2.4798; checked in data/arxiv_2107.14468.pdf); I3 needs t >= 3
  (checked, data/yang_thesis_2025.pdf Thm 1.3, strict "sigma >", so beta <= 1 - nu(gamma)); I4 needs sigma in [0.98,1],
  T >= 3, and C1 = 9.77e21 needs T > e^481958 (checked verbatim in data/arxiv_2311.05136.pdf Thm 1.1; her N(sigma,T)
  counts 0 < gamma < T, sigma < beta < 1, matching M(sigma) in Lemma 4); I5 used only on [0.6, 1 - 1e-6].
  All hold at X0 and are monotone in the right direction as X grows.
- Monotonicity for all larger n (Lemma 6): I re-derived d log(X nu)/dX = (1 - 1/log L)/(3X), the bound
  d(X g_i)/dX >= (1 - B_i alpha sqrt(nu)) d(X nu)/dX, and that Q_i is non-decreasing; correct. A0, A1, R_E, R_T
  log-derivative conditions (M1),(M2),(M4) are correct and hold with huge margin. Lemma 4(c) (slope m_i, integral
  <= exp(-X g(nu))/m_i) re-derived; correct. Lemmas 1, 2, 3, 5 re-derived; correct.
- No hidden restriction found. Note: the statement is a threshold result only; all n >= 1 stays open (CLAIM says so).

## (b) Scope words
CLAIM.md's sentence and PROOF.md name I3 as a UNSW PhD thesis (2025) and I4 as arXiv:2311.05136v1, an unrefereed
preprint. I fetched https://arxiv.org/abs/2311.05136 once (honest UA naming V3R1T4S, HTTP 200, 2026-11-24 07:55:13 UTC):
only [v1] (9 Nov 2023), no journal-ref. So "unrefereed preprint" is accurate as of today. Requirement met.
Sensitivity (out/mutation_out.txt, and my own float check): I4's C1 x 1.2 already breaks Y = 29.735, so the result
rests on I4's exact constant; I1, I2, I5, I6 have slack of > e^100.
Transitive dependency (KNOWN, from data/arxiv_2311.05136.pdf footnotes 1-2): I4's T > e^481958 constants assume the
zero-free region 53.989, which itself used a Littlewood constant 21.233 "communicated by the author" (Yang). That is
inside I4's own (preprint) proof and is now covered by Yang's thesis (Thm 1.2), so the named I3/I4 dependency covers it.

## (c) Frozen thresholds (PREREG.md)
Y_cert = 29.735 at prec 128 and prec 256 (out/scan_out.txt, agree=True), standalone mpmath.iv checker PASS at 29.735 and
FAIL at 29.734 (out/standalone_main.txt, out/standalone_29.734_expect_FAIL.txt). 29.735 <= 32.527 (beats record) and
<= 32.337 (meaningful drop). Null tests N1-N5 report as required (out/null_tests_out.txt ALL_CONTROLS_BEHAVE;
out/replay_ch_out.txt 32.891867 and MTY 32.753, within the frozen +-0.001 / +-0.01). Independent check (mine, written
before reading code/, mpmath.iv at 200 bits, dominant term A2 only, other terms < e^-10000): Phi(3e^29.735) in
[0.93425334448811, 0.93425334448811] < 1; Phi(3e^29.734) = 1.04447 > 1. Matches out/ to 13 digits. NUMERICAL (interval).
PREREG was frozen 07:36:41 UTC after disclosed float scouting (~29.73); the frozen thresholds do not depend on the
result, and the main/variant input sets are all reported, so no forking-path concern.

## (d) Is 32.537 the right comparison?
Yes: it is the smallest previously stated value (ch_thesis.pdf Thm 4.3, quoted as best by arXiv:2601.15564v2 p.2);
32.76 (OEIS A060199 comment, MTY 2024) and 32.892 (JNT 2023) are larger, so Y < 32.537 is the most demanding
comparison and 29.735 beats all three. Not subsumed: arXiv:2601.15564 proves only n^3 <= 1.649e40 computationally
and an Omega <= 2 result; arXiv:2402.04272 (Cully-Hugill-Johnston, I fetched it, HTTP 200, sha256 9bf784f2...) treats
90th powers, not cubes; data/rstation_130.html §2.3 gives ~30.07 explicitly as "model, not a theorem" with Bellotti
Thm 1.3 and Ford's c -- it anticipates the idea but states no rigorous threshold and its value is above 29.735
(the package's own Ford+Thm1.3 row, 30.062, is consistent with it). Wider literature search is NOVELTY's job.

## Concerns (do not change the verdict on the main claim)
1. Variant row "Bellotti JMAA 536 (2024) c = 53.989 -> 29.906" is not backed by any file in data/: data/arxiv_2306.10680.pdf
   is v1 and states 54.004. With c = 54.004 my float check gives Phi(29.906) = 1.096, Phi(29.907) = 0.980, i.e. ~29.907.
   The journal-only variant figure should be labelled unverified or recomputed from the journal text. Same caution for
   the "32.676, no preprint/thesis input" row (it uses that c too).
2. HEURISTIC, possible flaw in the record itself (retraction duty, for the human): ch_thesis.pdf (1.13) gives Ford's
   c = 51.82 only for |t| >= exp(exp(33)); out/replay_ch_out.txt reproduces the thesis's 32.536 only with c = 51.82, but
   at that threshold log log T ~ 32.54 < 33. If the thesis did use 51.82, 32.537 may not be rigorous as stated. This
   only makes the comparison easier for this claim.
3. Process: data/fetch_log.txt says first fetches used a 'Mozilla/5.0' UA (Rule 5 concern); arXiv PDFs and the Yang thesis were
   re-fetched honestly; it is unclear from the log which UA the OEIS status fetch used. NOVELTY/gate should confirm.
4. I5 is cited via Cully-Hugill's restatement rather than the KLN text; harmless given its > e^100 slack (Remark 2,
   out/mutation_out.txt "KLN C1 x 1e100 ... PASS").

## Verdict
The main claim meets the full frozen criterion (threshold improvement, Y = 29.735 < 32.527, interval-certified at two
precisions plus an independent checker, inputs quoted exactly, thesis/preprint named). Genuine, not subsumed by any
source in the package or the two extra arXiv records I opened.

confirmed_scope: Conditional on Yang's 2025 UNSW PhD thesis Theorem 1.3 (zero-free region, c = 51.34) and Bellotti's unrefereed preprint arXiv:2311.05136v1 Theorem 1.1 (zero density near sigma = 1), plus published results, for every integer n >= exp(exp(29.735)) there is a prime in (n^3 + 1/2, n^3 + 3n^2 + 1/2], and so between n^3 and (n+1)^3; this is a threshold result, and the claim for all n >= 1 stays open.
pass: true
