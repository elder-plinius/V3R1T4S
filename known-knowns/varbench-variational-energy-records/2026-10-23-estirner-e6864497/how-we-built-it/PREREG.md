# PREREG: varbench-variational-energy-records, J1J2/square_100_P_0.9.md (run 2026-10-23-1501, night 2)

written: 2026-10-23T15:12:57Z (date -u), before any instrument check or estimate of this folder has run, and
before claim/ exists. It replaces nothing in run folder 2026-10-22-1610 (whose PREREG.md stays as written); the
estimator check R2 that failed there at float64 round-off is re-posed here as I1 (a new instrument check, not a changed
threshold for an old result).

null_test: not needed because a claim here is an explicit variational state whose energy expectation is re-estimated by independent Monte Carlo samplers and compared with fixed table and literature values; no search statistic, key, period or "beats chance" claim is made.

## Fixed quantities

- File: J1J2/square_100_P_0.9.md (Pauli convention, 10 x 10, periodic in both directions, J1 = 1, J2 = 0.9;
  fetched 2026-10-23T15:08:00Z, best row -250.78657331066935).
- E_bar = -253.668 (Golubev, Iakovlev and Mazurenko, arXiv:2606.04558v2, Table I, ViT, e = -0.634170 per site;
  sigma_best = 0, none printed). The authors' own 102400-sample re-estimate (-253.6416(60), via the QMBL aggregator) is
  above E_bar and does not lower it. E_bar only drops (a lower published variational value found by this run's
  literature lens or by a NOVELTY skeptic replaces it).
- Margin: m = max(3 * sigma, 1e-6 * |E_bar|) with sigma defined below (1e-6 * |E_bar| = 2.54e-4).

## The independent estimator (lens exact-scorer-first, code written in this run)

attempts/exact-scorer-first/code/estimator2.py: its own lattice (bond list built from the VarBench definition, checked
in I3), its own Sz = 0 Metropolis sampler (symmetric proposals: with probability 1/2 a random NN or diagonal bond, else a
random (up, down) site pair; swap; accept with the target-density ratio), its own local energy, its own statistics. From
the model code (run folder 2026-10-22-1610, attempts/representation-transfer/code/nqs.py, sha256 122e54f2...) it uses
only the network and the symmetry tables, to evaluate the 16 image amplitudes psi0(g s); it recomposes
psi(s) = sum_g chi(g) psi0(g s) itself and must match nqs.NQS.forward (I3). Two statistics:

- **E_MC (plain):** chains sample |psi|^2; E_MC = mean of Re E_loc over all chains and rounds; sigma_MC = standard
  deviation of the C independent chain means / sqrt(C) (each chain is one independent unit, so autocorrelation inside a
  chain is included); blocking over rounds of the chain-averaged series is reported as a diagnostic, and sigma_MC is the
  larger of the two.
- **E_IS (tail-safe):** chains sample q(s) proportional to sum_g |psi0(g s)|^2 (the incoherent sum of the images; it
  does not vanish at the projection nodes). With w(s) = |psi(s)|^2 / q(s) <= 16 (Cauchy-Schwarz), E_IS = sum w E_loc /
  sum w, where w E_loc = conj(psi(s)) (H psi)(s) / q(s) is computed without dividing by psi(s). sigma_IS = jackknife over
  the C independent chains. Var(H) is estimated the same way, as sum |H psi|^2 / q / sum w - E_IS^2.
- **Effective samples:** N_eff = Var(H)_est / sigma^2 for each statistic (Var(H)_est from E_IS's run for both, since the
  plain-MC sample variance can miss the nodal tail). Each claim measurement needs N_eff >= 1e5.
- Layout for 10 x 10 measurements: 2048 chains, 50 thermalisation sweeps from random Sz = 0 states, then rounds of
  2 sweeps (1 sweep = 100 proposals) followed by one measurement of every chain, until N_eff >= 1e5 by the rule
  above (at most 400 rounds). The heavy-job lock is held in chunks of <= 225 s.

## Instrument checks (must all pass before any 10 x 10 estimate is used; a failure stops the claim line)

- **I1 (correctness on an exact eigenstate, 4 x 4 J2 = 0.9):** psi = the ED ground state saved in run folder
  2026-10-22-1610 (attempts/exact-scorer-first/out/gs_4x4_J2_0.9.npz, E0 = -44.599400546262565). Pass iff
  max |E_loc(s) - E0| < 1e-8 over every Sz = 0 configuration with |psi(s)|^2 > 1e-12 * max |psi|^2, and E_MC (1e5
  samples) is within 1e-8 of E0. Known negative: psi' = psi * (1 + 0.5 u(s)) with u(s) uniform in [0, 1) (seed 11):
  its exact <H> (by enumeration) must be above E0 by more than 1e-3, and E_MC of psi' must agree with that <H> within
  3 sigma_MC.
- **I2 (tail calibration on a trained state, 4 x 4 J2 = 0.9):** the trained NQS of run folder 2026-10-22-1610
  (ckpt/r4_J0.9.pt, sha256 7cc43dbc..., A1 x flip, stripe prior). Exact <H>_ex and Var_ex by enumeration of all 12870
  Sz = 0 configurations. E_MC and E_IS, each with 2048 chains x 64 rounds (131072 samples), seeds 501 and 502.
  - I2a (required): |E_IS - <H>_ex| < 3 sigma_IS, and Var(H) from the IS run within 25% of Var_ex.
  - I2b (recorded and gating): b4 = (E_MC - <H>_ex) / |<H>_ex| and z4 = (E_MC - <H>_ex) / sigma_MC. If |z4| > 3, the
    plain estimator's error bar is declared unreliable, and every 10 x 10 claim must then also satisfy
    3 * |b4| * |E_bar| < (E_bar - E_MC) (the 4 x 4 bias floor, scaled to 10 x 10 in relative terms, is below a third of
    the margin found). If |z4| <= 3 this gate is void.
- **I3 (code cross-checks):** (a) the bond list has 200 NN and 200 diagonal bonds on 10 x 10, every site has 4 NN and
  4 diagonal neighbours, no bond repeats; (b) on 256 random 10 x 10 Sz = 0 configurations (seed 7), estimator2's psi
  matches nqs.NQS.forward (|d log|psi|| < 1e-4 and phase difference mod 2 pi < 1e-4 where |psi| is not below 1e-6 of the
  batch maximum) and its E_loc matches nqs.local_energy within 1e-6 * |E_bar|.

## The claim rule

- **Candidates, in this order:** (1) run folder 2026-10-22-1610, ckpt/r10_J0.9_B1.pt (step 648, sha256 e6864497...);
  (2) the final checkpoint of this run's training continuation (lens representation-transfer, one checkpoint, saved at
  that run's end), if one exists before 2026-10-23T20:00Z.
- **Screening:** each candidate gets one E_MC with seed S1 = 31337 (layout above). The carrier is the candidate with
  the lowest screening E_MC. No other checkpoint is ever screened for the claim.
- **Claim measurements on the carrier only:** E_MC with seed S2 = 4242 and E_IS with seed S3 = 2718, both with the
  layout above and N_eff >= 1e5. sigma = max(sigma_MC(S2), sigma_IS(S3)).
- **Pass iff all hold:** I1, I2a and I3 passed (and I2b if it applies);
  E_MC(S2) < E_bar - max(3 sigma, 1e-6 |E_bar|); E_IS(S3) < E_bar - max(3 sigma_IS(S3), 1e-6 |E_bar|);
  |E_MC(S2) - E_IS(S3)| < 3 sqrt(sigma_MC(S2)^2 + sigma_IS(S3)^2); |E_MC(S2) - E_MC(S1)| < 3 sqrt(sigma_MC(S2)^2 +
  sigma_MC(S1)^2); the state's parameters and model code are saved and load in a fresh process.
- The claimed value is E_MC(S2) +- sigma (Pauli units), with E_IS(S3) reported beside it. A claim is the full success
  criterion (not a partial win) and goes to a three-skeptic panel; the REPRODUCE skeptic re-samples with its own code.
- If any condition fails, no claim: the folder reports the measured numbers and the mechanism (lens audit-the-judge).

## Training continuation (lens representation-transfer; produces candidate (2) only)

Resume of run folder 2026-10-22-1610's command (train.py, --resume ckpt/r10_J0.9_B1.pt, same architecture), in this
folder's attempts/representation-transfer/ with a new tag, cosine lr 0.009 -> 0.002, 2048 samples per step, the heavy
lock in <= 225 s chunks, hard deadline 2026-10-23T20:00Z. Its training-batch energies are progress notes only and are
never compared with E_bar.
