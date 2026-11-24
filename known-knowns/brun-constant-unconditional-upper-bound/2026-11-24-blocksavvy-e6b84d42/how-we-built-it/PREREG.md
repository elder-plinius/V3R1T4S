null_test: not needed because every result is a deterministic interval-arithmetic (arb) bound checked by rerunning at two precisions plus negative controls listed below, not a search score or chance-level claim.
frozen_utc: Tue Nov 24 05:27:37 UTC 2026 (date -u at run start; written before any Selberg-weight computation)

# PREREG: Selberg-weight refinement of the GRH Brun bound (and an unconditional feasibility probe)

## Hypothesis H1 (lens "selberg", GRH, partial win p1 follow-up)
Dunn's error term uses |lambda_d| <= 1, i.e. sum_{d1,d2<=z} |lambda_d1 lambda_d2| |E| <= r(z)^2 max|E| with r(z) = M(z).
Klyve's own proof (thesis 2007, (5.16), (5.24)-(5.26)) gives the exact optimal weights; we replace r(z) by
Lambda(z) = sum_{d<=z} |lambda_d|, bounded rigorously above, everything else exactly as in the submitted package (U'' route:
q-dependent Grenie-Molteni constant, direct li, own V lemma, pi_2(z) correction).
Reference: U0 := 2.15696693552995885 (submitted package, arb). Statistic: U1 = upper end of the arb ball for the new bound.
Thresholds (frozen):
- "improves our own GRH bound" iff U1 <= U0 - 1e-4 at prec 128 AND 256, and the improvement comes from the stated method
  change (Lambda instead of M), shown by an ablation with the identical optimiser and Lambda := M reproducing U0 to 1e-12.
- Any improvement < 1e-4 is "polish", reported, never claimed above PROMISING.
- Status ceiling for this session: PROMISING (single-context, unpanelled). No package, no outward step.
Negative controls (must all behave as stated, else the result is void):
 C1 Lambda := M(z): reproduces U0 (|diff| < 1e-12).
 C2 Brute-force check of the Lambda identity/inequality against directly computed Selberg weights (from Klyve (5.26))
    for at least 50 values of z <= 2e4 (exact rational arithmetic); any violation voids H1.
 C3 A deliberately wrong Lambda (halved) must be flagged by the brute-force checker.
 C4 Float/rigorous agreement: arb result vs float model within 1e-9.

## Hypothesis H2 (lens "uncond", unconditional, main win)
Main win per bank text: unconditional U < smallest unconditional bound on 81a (2.288513 as of the last fetch; re-fetch once,
plain request, before any comparison). Probe only: a float (non-rigorous) estimate of an unconditional tail bound using the
Selberg sieve with exact weights for {n(n+2)} (dimension 2, |r_d| <= 2^omega(d)) and partial summation from 4e18 with
Platt-Trudgian's head 1.840518. Outcome classes (frozen): float estimate >= 2.2885 -> "dead for this method";
< 2.2885 -> "lead" (needs a rigorous arb implementation + proof; status at most PROMISING-lead, never claimed tonight).
The parent's phrase "unconditional below 2.1594" is recorded as a stretch reference only; the bank criterion is 2.288513.

## Budget
~2 h wall, box only, nice, no cloud. Stop new work at 80%.
