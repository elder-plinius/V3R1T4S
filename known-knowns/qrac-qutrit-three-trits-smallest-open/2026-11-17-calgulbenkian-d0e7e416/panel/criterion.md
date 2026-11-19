context: Claude Code subagent, fresh context [Sonnet 5.5]

# Criterion skeptic report (partial win p1)

[Edited 2026-11-19 when answering the maintainer's review: a reference to a working file not shipped in this package was removed. The checks, numbers and verdict are unchanged.]

## What I did
- Read the claim record, README.md, HOW_WE_FOUND_IT.md, how-we-built-it/PREREG.md, verify-it-yourself/verify_qrac333.py, and object/qrac_333_naimark_dual_p1.json. SHA256SUMS all OK.
- Ran sh verify-it-yourself/run_checks.sh: calibration passes and the dual passes with U = 4368312591/6250000000 = 0.69893001456 <= 699/1000, all in fractions.Fraction.
- Wrote my own independent numeric check (pure Python, not using the package's word-reduction code). It builds random actual operator instances: a random rank-3 projector V on C^N, random rank-1 states R_x inside V H, random projective 3-outcome measurements on H (N = 6 and 9, complex). It assembles Z from the shipped LDL^T blocks and basis maps and evaluates the ASP and Tr(Z Gamma) directly with matrix products. Result: ASP + Tr(Z Gamma) = 0.69893001456 to about 1e-14 on three random instances (and Tr(Z Gamma) > 0 each time). So the polynomial identity the verifier checks symbolically is a true identity on genuine operators. It does not rely on the package's canonical-key reduction being right, and any false cancellation in that reduction would have shown up as a mismatch.

## Literal check of each word of p1
- "proven upper bound of at most 0.6990": U = 0.69893001456 <= 0.6990. Met (by about 7e-5).
- "on the ASP for n = d = D = 3": The ASP formula in the verifier (weight 1/(n d^n) = 1/81, 27 states, 3 questions, Tr(rho_x M^i_{x_i}), the last outcome written as I - sum of the others) matches the target's formula. My independent numeric ASP uses the same formula. Also calibrated on the (2,3,3) 1/2(1+1/sqrt3) value and the 3-MUB value 0.697146. Met.
- "valid for general POVMs": The relaxation is a Naimark dilation. Any triple of 3-outcome POVMs on C^3 dilates to projective measurements on H = C^3 (x) (C^3)^3 (an ancilla of dimension 3 per measurement suffices, and the three can share H by using separate ancilla factors), with V the projector onto C^3 (x) |000>, so M^i_a = V P^i_a V. The shared dilation is therefore valid. The relaxation imposes only: V, R_x, P^i_a are projectors; V R_x = R_x V = R_x; P^i_a P^i_b = delta P^i_a; Tr V = 3; Tr R_x = 1; no relation on V P V P V, and no relation between different questions. All of these hold for every POVM on C^3. Mixed states are covered by convexity (the ASP is linear in each rho_x). Tr_H(I_H), the unbounded dilation dimension, has coefficient exactly 0 in the certificate, so the bound does not depend on dim H. The relaxation does not assume projectivity of the physical measurements on C^3. Met.
- "shared randomness or other resources": none enter. The ASP is the plain one-shot formula; even if shared randomness were allowed, linearity would leave the bound unchanged. Not an issue.
- "given as an exactly verified certificate (a rational SDP dual whose feasibility and value are checked in exact arithmetic ...)": The JSON ships 78 rational LDL^T blocks (D >= 0, unit lower triangular L) plus rational basis maps. The shipped verifier assembles Z exactly, checks every non-constant cyclic trace-moment coefficient is exactly 0 (and the Tr_H(I) coefficient is 0), and computes the value exactly. It is a stdlib-Fraction check, reproducible in a few seconds. This is a rational SDP dual verified in exact arithmetic, which p1 explicitly permits (a machine-checked proof is the alternative, not required). Met. The remaining trust is in the verifier's moment bookkeeping, which my independent numeric identity test supports but does not formally replace.

## Full criterion (b)
Not met, and the package says so. 0.69893 > 0.69853, so (b) fails. It also fails (a) (no strategy). The package does not claim either.

## Caveats and limits
- Hidden-quantifier hunt: "at most 0.6990" is a threshold, and the package's threshold_rational is 699/1000 with strict_less false, consistent with p1 wording. I found no stretched definition. The README's phrase "first rigorous POVM-valid bound at the level of the floating-point Pauwels value" comes from the criterion text itself, not the package.
- The checker has a stdlib fallback for calibration when mpmath is absent; the dual check does not depend on mpmath.
- Null model: not applicable (exact object). I checked the identity on random operator instances as a substitute sanity test.
- Subsumption and later-record rules (repository review rule) I cannot settle from the folder: I did not check other merged packages or unmerged PRs. A live arXiv abs fetch shows versions v1 to v3 of 2312.14142 and no newer paper in that page; I did not search for newer upstream tables beyond that. A later upstream exact POVM-valid bound at or below 0.69893 would count against it. The bound is also weaker than the (unproven-exact) float 0.699 level only by being slightly below it, so it is a modest but genuine first exact certificate at that level.

confirmed_scope: The shipped rational dual certificate, verified exactly in Fraction arithmetic and independently confirmed numerically on random operators, proves ASP(3,3,3) <= 4368312591/6250000000 = 0.69893001456 <= 0.6990 for all states and all 3-outcome POVMs on C^3 via a Naimark-dilation relaxation that assumes no projectivity of the physical measurements, which meets enumerated partial win p1 only and does not meet criterion (b) (< 0.69853) or (a).

pass: true
