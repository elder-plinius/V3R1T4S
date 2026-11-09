# PREREG.v2 (frozen 2026-11-09T08:10:12Z, before any certify run of this run at N = 2400 and before any N = 2800 vector exists)

Why a v2: at 08:09Z the human's assistant reported that the other run on this machine finished at about 08:08 UTC and
that heavy work may start now (up to 14 threads, free RAM above about 6 GB), instead of after 08:45. PREREG.md's
start-time clause ("only after 08:45 UTC") was a machine limit, not part of the success rule; the S eigvec was started at
08:09:16Z with 7.04 GB free. PREREG.md also said "No N above 2400 is attempted in this run (time)". With the extra time,
this v2 adds one stretch object L. Everything in PREREG.md (criterion, route, S schedule and controls, count rule,
thresholds, positive and negative checks) stays in force unchanged.

## What was already seen when this was written

- The S eigvec (N 2400, 3400 bits, warm start from v_N2000) had printed cycles 0 and 5: setup 20.7 s, section residual
  1.5181e-606 at 27 s and 1.7018e-630 at 52 s (midpoint arithmetic; nothing certified). No certify run at N 2400 has
  started.

## Added stretch object L (N = 2800)

- Order (memory): S's eigvec, then S1, S2 and NEG (about 0.6 GB each), then the L eigvec alone, then L1, L2, NEG_L.
- L eigvec: N 2800, PREC 3900, CYCLES 40, warm start from inputs/v_N2400.txt (S's vector), 14 threads, MUOUT
  inputs/mu_N2800.txt -> inputs/v_N2800.txt. Started only if S's eigvec ended with EXIT 0, free RAM is above about 6 GB,
  and the peak predicted from S's measured eigvec peak (scaled by N^2 and by bytes per entry) is below free RAM minus
  1.5 GB.
  - L1: certify K 80, PREC 3900, J 11200, r0 0.01, rho 0.2, Q2 64, Qrho 256.
  - L2: certify K 80, PREC 4300, J 12320, r0 0.01, rho 0.2, Q2 96, Qrho 256.
  - NEG_L: L's vector with mu shifted by +10^-800, PREC 3900, J 11200, Q2 64, Qrho 256; radius must be >= 10^-800 / 2.
- The same count rule: D_L = min(D_L1, D_L2), each run counting only with isolation_ok and both small gains < 1.

## Which object is claimed (fixed)

- L is the claim object only if L1 and L2 both count, both finish by 08:55 UTC, and D_L > D_S. Otherwise S is the claim
  object (PREREG.md rules). Only one object is claimed and panelled (one cell per claim); the other is reported as
  context.
- Thresholds, positive checks (Nisoli 175 within radius + 10^-175, OEIS 382 within radius + 10^-382, the independent 649
  decimals within radius + 10^-649) apply to whichever object is claimed.
- Expected: D_S about 720, D_L about 840 (0.30 certified decimals per N).

null_test: not needed because the claim is an explicit rigorous enclosure checked by a deterministic program in ball arithmetic against a table value; no search or statistical claim is made.
