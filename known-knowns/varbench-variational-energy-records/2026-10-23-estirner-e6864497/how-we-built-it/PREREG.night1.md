# PREREG: varbench-variational-energy-records, J1J2/square_100_P_0.9.md (run 2026-10-22-1610)

written: 2026-10-22T16:12:53Z (date -u), before any lens of this folder has computed anything.

null_test: not needed because a claim here is an explicit variational state whose energy expectation is re-estimated by an independent Monte Carlo sampler and compared with fixed table and literature values; no search statistic, key, period or "beats chance" claim is made.

## The claim rule (for any night; a claim is not expected tonight)

Criterion verbatim in target.md. Operationally, for the file J1J2/square_100_P_0.9.md (Pauli convention, 10x10,
periodic, J1 = 1, J2 = 0.9):
- E_bar = min(every row's Energy in the live file, every published variational energy for the identical system
  converted to Pauli units). Today E_bar = -250.78657331066935 (DMRG 1024, sigma_best = 0), until lens
  leakage-and-settled reports a lower published value.
- Statistic: E_new = mean local energy over >= 10^5 effective samples from |psi|^2 with an independent sampler seed;
  sigma_new by blocking (binning until the error plateaus; autocorrelation-corrected).
- Pass iff E_new < E_bar - max(3 * sqrt(sigma_new^2 + sigma_best^2), 1e-6 * |E_bar|), the state's parameters and model
  code are saved and loadable, and a second independent re-estimate agrees within 3 sigma. A claim is partial win p1
  only by the p1 text (lower V-score with energy within the best row's error bar or below), stated as such.

## Tonight's scored reproductions (night 1; these are checks of the instruments, not claims)

R1 (lens exact-scorer-first): exact diagonalisation of the 4x4 periodic J1-J2 model in the Pauli convention.
- Known positive: J2 = 0.5 must give -33.83169340557936 (VarBench J1J2/square_16_P_0.5.md) within 1e-8.
- Known negative: J2 = 0.55 must differ from that value by more than 1e-3.
- Then the 4x4 J2 = 0.9 ground energy (reference for R2 and R3).

R2 (lens exact-scorer-first): the Monte Carlo energy estimator (local energy, Metropolis exchange sampler at Sz = 0,
blocking error) on 4x4 J2 = 0.9 with psi = the exact ground state: its estimate must agree with R1's exact energy
within 3 sigma_blocked, with sigma_blocked < 1e-2 (Pauli units) at >= 10^5 samples; with a perturbed state (exact
ground state times a random positive factor per configuration, a known negative) the exact <H> must be higher and the
estimator must agree with that exact <H> within 3 sigma.

R3 (lens representation-transfer): a torch NQS trained by MinSR.
- 4x4 J2 = 0.9: energy (exact sum over the Sz = 0 sector) within relative error 1e-3 of R1's exact value.
- 6x6 J2 = 0.8: Monte Carlo energy (>= 10^5 samples, blocking) per site within relative error 1e-3 of the exact
  -0.586487 (arXiv:2206.14307, Table 5; the CNN of that table reached 1.0e-3); relative error below 2e-4 (their RBM
  level) is reported, not required.
- 10x10 J2 = 0.9: throughput (samples/s, MinSR step time) measured; any training run there is checkpointed and reported
  as progress only. No 10x10 energy is claimed tonight. A 10x10 energy is compared with E_bar only through the claim
  rule above, in a later run with a fresh panel.

A failed R1 or R2 means the scorer is wrong: nothing that uses it is reported. A failed R3 is a negative result for
that representation (the lens writes where and why).
