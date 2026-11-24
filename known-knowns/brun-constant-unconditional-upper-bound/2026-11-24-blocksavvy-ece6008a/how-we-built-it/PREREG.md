# PREREG: rigorous per-modulus Selberg remainder (lens "rho_exact"), GRH Brun bound, partial win p1

frozen_utc: Tue Nov 24 07:33 UTC 2026 (written before any computation in this run; the float/long-double lead it tests is
runs/2026-11-24-0527/attempts/rho, U_lead = 2.1257394267371707605, which used long-double weights with a stated margin)

## Hypothesis
In Dunn's framework as modified by submission 2026-11-24-blocksavvy-e6b84d42 (exact Selberg weights, error factor
Lambda(z)^2 = (sum_d |lambda_d|)^2), the Selberg remainder sum_{d1,d2} lambda_d1 lambda_d2 R_[d1,d2] equals sum_q rho_q R_q with
rho_q = sum_{[d1,d2]=q} lambda_d1 lambda_d2, so the factor Lambda^2 may be replaced by Sigma(z) = sum_q |rho_q| <= Lambda^2.
Scope (fixed): only intervals whose chosen z_i <= 20000 use Sigma (as in the lead); all other intervals exactly as in e6b84d42.

## Method of rigour (fixed before measuring)
lambda_d (Klyve (5.24)-(5.26), n = floor(z)) evaluated in arb at the working precision; each rounded to an integer
L_d = round(2^40 lambda_d) with |2^40 lambda_d - L_d| <= 1 certified by the ball. P_q = sum_{[a,b]=q} L_a L_b is computed EXACTLY
in 128-bit integers; then Sigma <= (sum_q |P_q| + 2 N sum_d |L_d| + N^2) / 2^80 (N = number of d), evaluated exactly.
No floating point enters the certified value.

## Statistic and thresholds
U3 = upper end of the arb ball of the full bound (author program) at 128 and at 256 bits; plus the standalone checker's
recomputed total C3. Reference U_ref = 2.1269872000642055706 (e6b84d42 program value).
- "improvement" iff U3 <= U_ref - 1e-4 at both precisions AND the standalone checker passes at both precisions with C3 <= the
  claimed bound. Smaller gain = polish, not claimed.
- Claimed bound = U3 rounded UP at the 6th decimal (or 7th if it still sits strictly above C3 and U3), decided mechanically.
- Status ceiling this session: PROMISING (no panel run here; briefs only).

## Controls (all must behave as stated, else void)
 K1 --rho off reproduces 2.1269872000642055706 exactly.
 K2 Exact-integer identity: sum_q P_q == (sum_d L_d)^2 exactly, for every n used.
 K3 Sigma upper bound vs exact rationals (Fraction weights, exact rho) for >= 8 values of n in [3, 300]: upper >= exact, and
    within 1e-6 relative.
 K4 Sigma upper bound vs the lead's long-double rho.c for every n used: agree within 1e-8 relative.
 K5 lambda_1 = 1 (ball contains 1) and sum |lambda_d| agrees with W(n)/V(n) (exact tables) within 1e-12 relative for every n used.
 K6 Checker tamper tests: lowered rho term, raised rho term (> 1e-5), "rho" flag removed (Lambda^2 used, must FAIL), a z_i
    moved to another integer part (must FAIL), all must FAIL; the untouched certificate must PASS at 128 and 256 bits.
null_test: not needed because the result is a deterministic interval/exact-integer bound checked at two precisions with the controls above, not a search score.

## Budget
~4 h wall (to ~11:30Z), <= 3 cores at nice 10, RAM < 2 GB, box only, no cloud. Stop new work at 80%.
