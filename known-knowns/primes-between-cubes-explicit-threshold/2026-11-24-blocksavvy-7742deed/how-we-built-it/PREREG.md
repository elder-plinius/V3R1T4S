null_test: not needed because the result is a deterministic interval-arithmetic (arb) certificate of an explicit analytic inequality, checked at two precisions, by an independent second implementation, and by negative controls listed below; there is no search score or chance-level claim.
frozen_utc: Tue Nov 24 07:36:41 UTC 2026 (date -u, written before any rigorous/interval computation; see "Disclosed before freezing")

# PREREG: explicit threshold for primes between consecutive cubes (outside-bank target, like A034793)

## Criterion (our own; no bank criterion exists)
A complete written proof that for every integer n >= exp(exp(Y)) the open interval (n^3, (n+1)^3) contains a prime,
with Y < 32.537, the best value quoted in the literature (Cully-Hugill PhD thesis 2021, Thm 4.3; Bull. Aust. Math. Soc.
abstract doi:10.1017/S0004972723000588; quoted as best by Johnston-Sorenson-Thomas-Webster arXiv:2601.15564v2).
Every analytic input must be cited by its exact statement, and the final numerical inequality must be certified by
outward-rounded interval arithmetic. Published comparison points: 32.892 (Cully-Hugill, J. Number Theory 247 (2023)),
32.76 (Mossinghoff-Trudgian-Yang 2024, OEIS A060199).

## Method (fixed now)
Ingham/Cully-Hugill route with x = n^3 + 1/2, y = n^3 + 3n^2 + 1/2 (half odd integers), T = x^alpha, alpha = 1/3 + 1e-9:
- explicit formula error: Cully-Hugill JNT 2023 Theorem 2 with K = 2.4798 (log x >= 1e6);
- psi - theta: Rosser-Schoenfeld 1962 Thm 9, theta(t) < 1.01624 t;
- N(T): Hasanalizade-Shen-Wong Cor 1.2 (only a crude consequence used);
- zero density sigma in [0.6, 1-u2]: Kadiri-Lumley-Ng type bound exactly as stated and used by Cully-Hugill
  (C1 = 17.418, C2 = 5.272);
- zero density sigma in [1-u2, 1-nu(T)], u2 = 1e-6: Bellotti arXiv:2311.05136 Thm 1.1 (main) and Thm 1.2 (cross-check);
- zero-free region nu(T) = 1/(c (log T)^(2/3) (log log T)^(1/3)): c = 51.34 (Yang, PhD thesis UNSW 2025, Thm 1.3, t >= 3)
  for the main claim; variants c = 53.989 (Bellotti, JMAA 536 (2024)) and c = 57.54 (Ford 2002) reported alongside.
Statistic: Y_cert = the smallest Y on the grid {k/1000} for which the arb checker proves Phi(X0) < 1 at X0 = 3 exp(Y)
together with the monotonicity conditions (stated in the proof) at X0. Both prec 128 and prec 256 must agree.

## Thresholds (frozen)
- "beats the record" iff Y_cert <= 32.527 (i.e. at least 0.01 below 32.537) for the main input set, at both precisions,
  and the standalone checker (independent implementation, mpmath interval arithmetic) also certifies Y_cert.
- "meaningful drop" iff Y_cert <= 32.337 (>= 0.2 below the record).
- A result that needs an input that is only a preprint or thesis is reported with those inputs named in its scope
  words; the variant with only journal-published zero-free region (c = 53.989) is reported separately.
- Status ceiling for this session: PROMISING (single-context, unpanelled). If it clears the thresholds, write
  PANEL_BRIEFS.md for the parent to run the 3-skeptic panel. Nothing outward.

## Negative controls / null tests (must all behave as stated, else the result is void)
 N1 Replay: the float replay of Cully-Hugill's inequality (21) with her inputs reproduces loglog n0 = 32.892 (+-0.001)
    with c = 57.54, and the MTY value 32.76 (+-0.01) with c = 55.241.
 N2 Ablation: the rigorous checker with the Bellotti near-unity density switched off (KLN bound used up to 1-nu) must
    NOT certify any Y below 32.8 (it should land near 32.89 with c = 57.54); i.e. the gain comes from the stated input.
 N3 Tamper: the checker must FAIL at Y_cert - 0.01 (shows the certificate is near-tight, not vacuous), and must FAIL
    when C' (Bellotti constant) is multiplied by e^50 at Y_cert.
 N4 Float/rigorous agreement: arb midpoint of Phi vs mpmath float within 1e-9 relative at X0.
 N5 Second implementation (standalone checker, mpmath.iv, written separately) certifies the same Y_cert.

## Disclosed before freezing
Before this file, float (non-rigorous) scouting was run: replay of Cully-Hugill (attempts/replay/replay_ch_out.txt,
reproduces 33.990/32.892, MTY 32.75, and the thesis 32.536 only when Ford's c = 51.82 (stated for T0 = exp(exp(33)))
is used), and float estimates of the new threshold: about 29.73 (c = 51.34, Bellotti Thm 1.1), 29.91 (c = 53.989),
30.12 (c = 57.54). No interval computation had been run. rStation paper 130 (AI-agent preprint, Nov 2026) contains a
non-rigorous "model" remark that Bellotti's estimate would give about 30.07; see scout.md.

## Budget
About 5 h wall from 07:30 UTC, box only, nice 10, at most 3 cores, no cloud, nothing outward.
