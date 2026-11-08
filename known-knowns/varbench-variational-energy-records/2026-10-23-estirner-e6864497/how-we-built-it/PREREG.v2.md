# PREREG.v2: varbench-variational-energy-records, J1J2/square_100_P_0.9.md (run 2026-10-23-1501)

written: 2026-10-23T15:48:29Z (date -u). Written AFTER PREREG.md's instrument checks I1 (pass), I2 and I3 (I2a and I3(b)
failed; attempts/exact-scorer-first/out/I2.json, I3.json) and BEFORE any 10 x 10 energy estimate of any candidate
has been run or seen. Under PREREG.md the claim line is closed; this file opens a new one with two replaced instruments.
No threshold of PREREG.md is loosened: the failed checks are re-posed for new instruments at the same bars, and one
candidate is dropped (a tightening).

null_test: not needed because a claim here is an explicit variational state whose energy expectation is re-estimated by independent Monte Carlo samplers and compared with fixed table and literature values; no search statistic, key, period or "beats chance" claim is made.

## Unchanged from PREREG.md

E_bar = -253.668 (sigma_best = 0); the file and convention; the margin m = max(3 sigma, 1e-6 |E_bar|); the plain
estimator E_MC (chains on |psi|^2, sigma = max(chain-mean spread, blocking)); the 10 x 10 layout (2048 chains,
50 thermalisation sweeps, 2 sweeps between measurements, N_eff rule, <= 400 rounds); I1 (passed 15:35:19Z); I2b's rule.
The literature lens of this run (attempts/leakage-and-settled/report.md, 15:44Z) found nothing below E_bar.

## Replaced instrument 1: the tail-safe estimator (replaces E_IS, whose Var(H) check I2a failed)

**E_DIS (defensive neighbour mixture).** Chains sample |psi|^2 exactly as for E_MC. At each measurement, each chain's
state s' is kept with probability 1/2, else replaced (for this measurement only; the chain itself continues from s')
by a uniformly random H-neighbour s of s' (one exchange across a uniformly chosen antiparallel bond of H). The
measured configuration then has the exact marginal density m(s) = (|psi(s)|^2 + nu(s)) / (2 Z), with
nu(s) = sum_{s'' ~ s} |psi(s'')|^2 / n(s'') (s'' over the H-neighbours of s, n(s'') = number of antiparallel H-bonds of
s''), over the same Z as |psi|^2 (each s'' contributes n(s'') neighbours times 1/n(s'')). Weights w = |psi|^2 / m <= 2;
w E_loc = conj(psi(s)) (H psi)(s) / m(s) and |H psi(s)|^2 / m(s) are computed from the neighbours' amplitudes (already
needed for E_loc) without dividing by psi(s). E_DIS = sum w E_loc / sum w; sigma_DIS = jackknife over the C chains;
Var(H)_DIS = sum |H psi|^2 / m / sum w - E_DIS^2. (Defensive importance sampling, Hesterberg 1995; the covering density
puts weight one exchange away from the high-amplitude configurations, where night 1 and I2 located the variance.)

- **I2' (required, same bars as I2a):** on the trained 4 x 4 state (ckpt r4_J0.9.pt), 2048 chains x 64 rounds, seed
  503: |E_DIS - <H>_ex| < 3 sigma_DIS and Var(H)_DIS within 25% of Var_ex = 0.09134263343298699. Plus the exact identity
  sum_s nu(s) = sum_s |psi(s)|^2 over all 12870 configurations to relative 1e-10. Plus a fresh plain run (seed 504)
  for I2b (rule unchanged).
- If I2' fails, there is no claim tonight; the 10 x 10 numbers are reported as measurements only.

## Replaced instrument 2: the code cross-check I3(b)

- **I3'(b):** on the same 256 random 10 x 10 configurations (seed 7), estimator2 with a float64 copy of the model
  (model.double()) must match nqs.NQS.forward and nqs.local_energy evaluated with that float64 model: |d log|psi|| <
  1e-8, phase difference < 1e-8, |d E_loc| < 1e-7 (absolute). The float32 differences (estimator2's float32 network
  with float64 composition, and nqs.py's all-float32 path, each against all-float64) are recorded as findings.
- **I3'(c), at claim time:** on 2048 configurations from the final chains of the S2 measurement (a |psi|^2 chain),
  |mean(E_loc[float32 network, float64 composition] - E_loc[all float64])| < sigma_claim / 10, and the same for nqs.py's
  float32 local energy (reported; required only for estimator2's path).

## The claim rule (v2)

- **One candidate only:** run folder 2026-10-22-1610, ckpt/r10_J0.9_B1.pt (step 648, sha256 e6864497...). Candidate (2)
  of PREREG.md is dropped (its training was stopped at step 674 at 15:35Z).
- Screening S1 (plain, seed 31337) is kept as the second independent re-estimate.
- Claim measurements: E_MC with seed S2 = 4242 and E_DIS with seed S3 = 2718 (replacing E_IS), both with the 10 x 10
  layout and N_eff >= 1e5, where N_eff = Var(H)_DIS / sigma^2 for both. sigma = max(sigma_MC(S2), sigma_DIS(S3)).
- **Pass iff all hold:** I1, I2', I3(a), I3'(b) and I3'(c) pass (and I2b if it applies); E_MC(S2) < E_bar - max(3 sigma,
  1e-6 |E_bar|); E_DIS(S3) < E_bar - max(3 sigma_DIS(S3), 1e-6 |E_bar|); |E_MC(S2) - E_DIS(S3)| <
  3 sqrt(sigma_MC(S2)^2 + sigma_DIS(S3)^2); |E_MC(S2) - E_MC(S1)| < 3 sqrt(sigma_MC(S2)^2 + sigma_MC(S1)^2); the state
  loads in a fresh process.
- Claimed value: E_MC(S2) +- sigma (Pauli), with E_DIS(S3) beside it. Full success criterion; three-skeptic panel.
- Decision time: if I2' and I3'(b) have not both passed by 2026-10-23T16:50Z, no claim tonight; S1 and an E_DIS run
  on the candidate are then reported as measurements only.
