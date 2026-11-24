# REPRODUCE skeptic verdict (rerun, v2) - Brun's constant under GRH, B < 2.156967

role: REPRODUCE
context: fresh subagent (knowledgeWork delegation), started with no prior conversation; it saw only the kit rules, the claim_v2/ package and the staged submission package, and did not open any earlier panel verdict
claim: Assuming GRH for Dirichlet L-functions (and RH), Brun's constant satisfies B < 2.156967 (partial win p1: strictly below Dunn's GRH bound 2.1594).
date_utc: 2026-11-23T18:20:19Z (work 17:48Z-18:20Z)
files_judged: claim/ = claim_v2 (CLAIM.md, PROOF.md, REPRODUCE.md, CHANGES.md, code/, out/, verify/); out/a_bound_certificate.json sha256 a26bba477468eeacdb146bdd65d3649166d9b116de0f874411859b5af0fd8ee8 (byte-identical to the staged package's object/a_bound_certificate.json; staged SHA256SUMS: 44/44 OK)
scratch: panel/scratch-reproduce2/ (own venv: python-flint 0.9.0, numpy, scipy; no sudo; jobs pinned to 4 cores with taskset, nice)

## 1. Own checker first, from the definitions (written before opening the author's code)
Definitions used (quoted from Dunn arXiv:2504.15658v2 Thm 3.1, fetched by this skeptic, HTTP 200, and PROOF.md B-D):
"B <= 1.840518 + 2 sum_i [c1(m_i,m_{i+1})/V(z_i) + c_pi(m_i) r^2(z_i) c2(m_i,m_{i+1})] + 32 pi_2/log m_k + 8/sqrt(m_k) - 2 pi_2(m_1)/m_1",
with V(z) = sum_{d<=z, d|P_z} prod_{p|d} 1/(p-2), r(z) = #{odd squarefree d <= z} (Dunn Lemma 2.2 formula 4z/pi^2 + 3.038 sqrt z + 5.744 z^(1/4) above 1e7),
c1 = int li(t)/t^2, c2 = int t^(-3/2) log t, and the claim's c_pi = 1/(8pi) + (1/(2pi) + 3/log m)lambda + 1/(4pi log m) + 6/log^2 m + li(2)/(sqrt(m) log m), lambda = min(1/2, 2 log z/log m).
- own/mysieve.c (my segmented sieve, exact u128 fixed point floor/ceil(2^64/prod(p-2))), checked against an exact-fraction brute force for n <= 20000 (8 points, all equal). Result: V(1e10) in [18.40171086159521191, 18.40171086181491720], M(1e10) = 4052847232, M(1e7) = 4052875; identical to the author's vsieve_fx/vsieve outputs (Vlo=18.401710861595212, Vhi=18.401710861814917, count 4052847232). NUMERICAL (rigorous bounds)
- own/mylemma.py (my arb code, P = 1e7, tail via pi(x) <= 1.25506 x/log x): S(0.44) <= 21.2718848066823, A(1e10) <= 0.0107000905918479 <= 0.0107001; kappa+4 = 4.6352 >= 1/(2s) = 1.1364; twin-prime constant C2 <= 0.660161819715455 < 0.6601619 (partial products decrease to C2). PROVED-HERE (given the cited pi(x) bound)
- own/mycheck.py: re-evaluates all 9906 interval terms in arb from my own V/M table and these formulas, taking only z_i from the certificate.
  scheme mode (claim's V rounding: 1e4-multiples above 1e8), 128 bits: sum of terms 0.31337339236625120511; B (no pi_2(z) term) = 2.156966935529957806590 +/- 3.3e-22; pi_2(z) correction 2 sum z_i/m_i = 1.0328e-15; total 2.156966935529958839 < 2.156967 (True), < 2.1594 (True); every certificate term matches my value to <= 2.7e-16 relative (float display); 0 inadmissible z_i (all z_i < m_i^(1/4)).
  exact mode (V(floor z) everywhere, 256 bits): total 2.156966935366080706 (slightly smaller, as expected).
- Spot check of the inherited Dunn r(z) formula against my exact counts at 123 thresholds in [2.77e6, 1e10]: r(z) >= M(z) at all, min (r - M)/sqrt(z) = 3.06. NUMERICAL (spot check only; Dunn Prop 2.1 is inherited, not re-proved).

## 2. Rebuild from scratch per claim/REPRODUCE.md (fresh copy, BRUN_WORK = scratch work/, tables rebuilt; chunks run with 4 threads instead of 5)
- vsieve: M(1e7) = 4052875; vsieve_fx chunks: Vlo(1e10) = 18.401710861595212; dense: Vlo(1e8) = 14.913800709097165.
- R  (replay.py --prec 128)                                = 2.1593210323778804655  (matches claim)
- U' (replay.py --cpi q --prec 256)                        = 2.1569562895056571339  (matches claim)
- U''(replay.py --cpi q --c1 li --vlemma own --prec 256)   = 2.1569669355299578202  (matches claim; 128 bits gives the same sup)
- vlemma.py: A(1e10) <= 0.010700091 at s = 0.44 (matches claim)
- Regenerated certificate (--cert, prec 128): "intervals" list identical to the shipped certificate; deterministic.

## 3. Standalone checker of the staged package (copied to scratch; run with flint 0.9.0, 4 cores)
Original: check 0 (vcount = definition at 2859 points), 1-2 (9906 admissible, max rel diff 4.8e-20), 3 (A(1e10) <= 0.01070009059), B <= 2.1569669355299588530, check 4 -> PASS.
Mutations (each on a fresh copy):
- one digit changed in the certificate text, interval 0 term 0.00758... -> 0.00759...: FAIL (stated != recomputed)
- 5th significant digit of interval 500 term: FAIL
- one hex digit of z_0: FAIL (term mismatch)
- last z just above m^(1/4): FAIL (not admissible); z_0 = 1.01 m_0^(1/4): FAIL
- interval deleted: FAIL; 't'/'z' kind swapped: FAIL
- checker's sieve mutated (p-2 -> p-1): FAIL at check 0
- checker's V-lemma constant tightened to 0.0106: FAIL (terms no longer match)
- last (20th) digit of one stated term: PASS. This is harmless: the checker's total uses its own recomputed sups, not the stated terms, so stated digits below its 1e-18 tolerance cannot change the verdict.

## 4. Proof steps re-derived
- PROOF.md B: Grenie-Molteni Cor. 1.2 (arXiv:1709.07609v3, fetched by this skeptic, HTTP 200) has exactly the form quoted (sqrt(x)[(1/(2pi)+3/log x) log Delta_L + (log x/(8pi) + 1/(4pi) + 6/log x) n_L], x >= 2, GRH); with L = Q(zeta_q), n_L = |G|/|C| = phi(q), log Delta_L <= phi(q) log q, q = [d1,d2] <= z^2 odd so gcd(-2,q) = 1, dividing by phi(q) gives the claim's c_pi; lambda = 1/2 recovers Dunn's c_pi; every term decreases in x. Checked.
- PROOF.md C (V lemma): h = u*f identity at p, p^2, p^k; O(t) = H(t) - H(t/2)/2, |eps| <= 4/t (both ranges); sum f = 1/C2; the error decomposition; Rankin bounds; max at u = 1. All re-derived, no gap found. PROVED-HERE (with the cited pi(x) bound).
- PROOF.md D: d/dt[log log t - li(t)/t] = li(t)/t^2; c2 antiderivative checked. PROOF.md A pi_2(z) correction: a twin pair is sieved out only if p+2 <= z; adds <= 2 sum z_i/m_i = 1.03e-15, included.
- Inherited and not reproduced here (KNOWN, trusted as published): Dunn Thm 2.1 / Klyve Thm 5.7 (Selberg sieve form), Dunn Prop 2.1 / Lemma 2.2 above 1e7, Platt-Trudgian B(4e18) <= 1.840518, pi_2(4e18) = 3023463123235320. These are the same inputs Dunn's 2.1594 relies on.

## 5. Notes
- Mid-run the box was restored to an earlier snapshot, which erased this skeptic's first set of outputs. Every step above was re-run after the restore, and all numbers quoted come from the re-run outputs in panel/scratch-reproduce2/ (own/*.txt, claim/work/, runmut.log). The first run's numbers were identical.
- No mismatch, missing object or non-determinism found. Margin below 2.156967 at the certified z_i: 6.4e-8 (total 2.15696693552995884).

verdict: REPRODUCED. R, U', U'' reproduce to all printed digits from rebuilt tables; an independent evaluation from my own sieve and formulas gives B <= 2.156966935529958839 < 2.156967 < 2.1594; the standalone checker passes on the original and fails on every meaningful corruption.
pass: true
