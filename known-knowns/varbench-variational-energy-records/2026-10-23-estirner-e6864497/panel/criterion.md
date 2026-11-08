# CRITERION skeptic: varbench-variational-energy-records, J1J2/square_100_P_0.9.md

context: subagent (Claude Code Agent tool, opus, fresh context, saw only claim/)
written: 2026-10-23T19:10:04Z (date -u at assembly)
injection_suspected: none (nothing in claim/, the fetched pages or program output asked me to act)

criterion_met: full
confirmed_scope: For VarBench J1J2/square_100_P_0.9.md (10 x 10, periodic in x and y, J1 = 1, J2 = 0.9, Sz = 0, Pauli convention; file re-fetched unchanged at 2026-10-23T17:32:29Z), the fixed state object/r10_J0.9_B1.pt has a fresh-sample Monte Carlo energy below every row of that file (best -250.78657331066935) and below the lowest published variational value I found, -253.668 (arXiv:2606.04558 v1 and v2, Table I, 10 x 10 J2 = 0.90 ViT -0.634170 per site times 400), by more than the success margin, as shown by the claimant's bounded-weight DIS estimate -253.7473816594384 +- 0.0032485374695990594 and by my own independent plain estimate -253.74398860968137 +- 0.011353681212836501 (41984 samples, 39745 effective), the >= 10^5-effective-sample skeptic re-estimate itself being the REPRODUCE skeptic's to supply.

Verdict in one paragraph: the result is the full success criterion, not a partial win (p1 and p2 do not apply:
no V-score claim; the file has three rows). Hamiltonian, lattice, boundary conditions, filling, convention and the
bar check out; the margin is exceeded by a factor of 6 or more under the literal reading (sigma_best = 0) and by
3.66 or more under the strictest reading I could construct. The one stretched definition is the claim's
"N_eff": the two claim measurements do NOT have 10^5 autocorrelation-corrected samples by a consistent count
(S2 83176, S3 Kish 97096); only the screening run S1 does (101824). Because the criterion's sample clause binds the
skeptic's re-estimate rather than the claimant's, this is a reporting defect, not a criterion failure, but the
panel must count the REPRODUCE skeptic's samples consistently (raw samples / tau, or Kish ESS / tau for weighted
samples); a run of 102400 raw samples cannot qualify. My pass is conditional on that re-estimate.

## Clause-by-clause reading of the success criterion

1. **Identical Hamiltonian, lattice, boundary conditions, filling.** Met.
   - VarBench file `inputs/varbench/square_100_P_0.9.md`: 10 x 10, periodic both ways, J2 = 0.9; rows DMRG
     -250.78657331066935 (no sigma), RBM -238.966 (0.013), Jastrow -235.905 (0.010); no ED row (file eligible).
   - Convention check with my own ED (mycode/my_ed.py, independent of the claim's tools/ref/ed.py): 4 x 4 periodic,
     H = sum_NN sigma.sigma + J2 sum_diag sigma.sigma, each bond once, Sz = 0: J2 = 0.5 gives E0 = -33.83169340557941,
     equal to VarBench's square_16_P_0.5.md ED row -33.83169340557936 (and E0/(4N) = -0.52862021, the known S.S value),
     so VarBench is the Pauli convention, E_Pauli = 4 N e_S.S = 400 e on 10 x 10. J2 = 0.9 gives -44.59940054626244,
     equal to the claim's calibration E0 -44.599400546262565.
   - The claim's model code uses the same bond list (NN (x+1,y), (x,y+1); diagonals (x+1,y+1), (x+1,y-1); periodic;
     2N + 2N bonds); my own E_loc code agrees with nqs.local_energy on 64 10 x 10 configurations (5 sweeps from random starts) to
     max |d E_loc| = 1.043e-03 (float32 path noise; means -253.7564 both).
   - The state lives in Sz = 0 (all samplers conserve Sz); a state in one symmetry sector (B1, flip-even) is still a
     state of the full Hilbert space, so its <H> bounds the ground energy from above.
   - Golubev et al. Table I is per site in the S.S convention (their 6 x 6 ED J2 = 0.5 -0.503809 and 10 x 10 J2 = 0
     ViT -0.671476 vs QMC -0.67155266 are S.S values), "periodic L x L": -0.634170 x 400 = -253.668. Correct.

2. **"Strictly lower than every row's Energy in that file."** Met by about 2.97 (DMRG -250.7866 vs all measurements
   near -253.75); RBM and Jastrow rows trivially.

3. **"... and than every published variational energy for the identical system found by an arXiv search."**
   Met as far as my search reached (it is not exhaustive):
   - arXiv:2606.04558: v1 (3 Jun 2026) and v2 (15 Sep 2026) both print 10 x 10, J2 = 0.90, ViT -0.634170 and "-" for
     previous works (my fetches HTTP 200; v2 PDF sha256 9064b3c7893c4e6692524eb19fc2ef73b82e04096b5c4431664c5030da414f19,
     identical to the claim's record; v1 PDF sha256 341be5e085635203a9b9d8d9b47634bdc454f983d2078adc953b8e0182286ee9).
   - Their 10 x 10 large-J2 "previous works" source [68] (Chen, Hendry, Weinberg, Feiguin, arXiv:2206.14307, RBM +
     Lanczos) tabulates 10 x 10 J2 = 0.8, 1.0, 1.2, 1.5 and no 0.9; ANTN (arXiv:2304.01996) stops at J2 = 0.8;
     the SDP certification paper (arXiv:2310.05844) L = 10 table has J2 = 0.8, 1.0 and no 0.9; Szabo-Castelnovo
     (arXiv:2002.04613) is J2 = 0.5 on 10 x 10. Web searches for 10 x 10 J2 = 0.9 energies found nothing lower.
   - The bar the claim uses (-253.668, Table I, likely a training-time value) is lower, hence stricter, than the
     authors' re-estimate it quotes (-253.6416(60)).

4. **Margin max(3 sqrt(sigma_new^2 + sigma_best^2), 1e-6 |E|).** Met with large slack under every reading I tried.
   - sigma_best: Table I prints no error bar. The criterion's "stated statistical errors" gives sigma_best = 0 on a
     literal reading; the stricter reading (sigma_best = 0.0060, the error of the authors' re-estimate quoted in
     PREREG.md) still leaves gap/margin >= 3.66 for every measurement. Rounding of the printed 6 decimals is
     +-2e-4 in Pauli units, negligible. 1e-6 |E| = 2.54e-4 never binds.
   - With tail-aware sigma_new (see 6) and sigma_best = 0: margins 0.012667 (S1), 0.014015 (S2), 0.009746 (S3)
     against gaps 0.080447, 0.085424, 0.079382 (gap/margin 6.35, 6.1, 8.15).

5. **"A genuine variational state."** Met: an explicit amplitude psi(s) = sum_g chi_B1(g) psi0(g s) given by
   object/model/nqs.py and the checkpoint (sha256 e68644979db4d9764ac1787d1c064fe18c4750cb4cb47ee573e40588bcd9c485,
   matches the claim and PREREG.md); its pickle references only OrderedDict, torch storages and _rebuild_tensor_v2,
   and loads with weights_only=True. Not an extrapolation, not a training-batch value: S1, S2, S3 are fresh-chain
   measurements with seeds fixed in PREREG.md; S2 was named the claimed value before it ran (not a best-of-three
   selection; the most conservative of the three, S3, is also far below the bar). Float32 effects on the measured
   chains are 1e-7 to 1e-5 (I3c), negligible.

6. **">= 10^5 effective samples, autocorrelation-corrected" and honest error bars.** This is where the claim's
   wording is stretched (finding F1 below). The clause binds the skeptic's own re-estimate (the REPRODUCE skeptic's);
   my own estimate (below) is shorter and does not meet 10^5 by itself.
   - Claimant's runs (results/*.json): S1 plain n 153600, S2 plain n 102400, S3 DIS n 102400, 2048 chains each.
   - My own run (independent code mycode/my_mc.py, sha256 a15148075c2ef248eb9fb021fcc36511135886b45e0366d076d5f44510f8b988;
     seed 8086 written down before the start, 1024 fresh chains from random Sz = 0 states, 100 thermalisation
     sweeps (claim: 50), other proposal mix (1/2 NN bond, 1/4 diagonal bond, 1/4 random up-down pair), measurement
     every 2 sweeps, own E_loc in float64 composition from the float32 network, own statistics):
     E = -253.74398860968137, sigma = 0.011353681212836501 (spread of 1024 chain means; blocking levels 0.01057 to
     0.01211), n = 41984, tau 1.056, N_eff = 39745, acceptance 0.2016; halves -253.75186813446348 and
     -253.7364843003651 (half sigma 0.013365); gap to -253.668 = 0.07598860968136023 = 6.69 sigma, 2.23 times my own
     3-sigma margin 0.034061. It agrees with S3 (DIS) within 0.3 of my sigma and with S1, S2.
     Pre-committed 80 rounds; I stopped after 41 because the CPU package read 90-100 C (19:02:06Z to 19:08:20Z,
     shared load) while chunks ran. GPU time used: 766.2 s in four chunks of <= 202 s under gpu1.sh, plus two tests.
   - What my run adds about the tail (data for the panel): my sample variance is 5.123318121563564 with
     max |E_loc - E| = 342.8276808429175, far above the claimant's plain sample variances (1.4294, 1.3303) and the
     DIS estimate Var(H) = 1.8152283827002975 +- 0.08437496142347141. Of the 12 samples with |dev| > 20, 9 are
     positive; the 2 with |dev| > 100 are both positive and move the mean by +0.01339 (mean without |dev| > 20:
     -253.76087). The local-energy tail is rare and skewed upward, so a plain run that happens to miss it comes out
     low (as both plain 4 x 4 calibration runs did). The plain error bars of S1 and S2 are therefore optimistic; the
     DIS value S3 is the number to rely on, and it alone clears the bar by 24.4 of its sigma. Rare events of this size
     also occur in the claimant's runs (max |dev| 198.73556573633584 in S1, 99.07046895254442 in S2), so the tail is
     common to both samplers; their rate is poorly determined by runs of this length.

## Stretched items found (none changes the verdict; all are recorded)

- **F1, effective samples overstated.** The claim's N_eff = Var(H)_DIS / sigma^2 mixes the DIS variance (1.8152)
  with a plain-run sigma that was built from the plain run's own, smaller sample variance. As a count of
  autocorrelation-corrected samples this is impossible: S2 states N_eff = 113495 from n = 102400 raw samples, S3
  states 172011 from 102400. Consistent counts (n / tau with tau = sigma^2 n / sample_var): S1 101824 (n 153600,
  tau 1.508), S2 83176 (n 102400, tau 1.231). S3 is importance-weighted: Kish ESS 97096 (fraction 0.948) before any
  autocorrelation; its 172011 is a "|psi|^2-equivalent" variance ratio, not a sample count. So, literally, only the
  screening run S1 has >= 10^5 autocorrelation-corrected samples; the headline S2 does not. Pooled S1 + S2 (both
  plain, independent seeds) have 185000 by the consistent definition, E = -253.7507735 +- 0.0027343.
  S2's stop at the first permitted check (50 rounds) was triggered by the inflated number.
- **F2, plain error bars not fully honest under the heavy tail.** Plain sample variances 1.4294 (S1) and 1.3303 (S2)
  are 0.7875 and 0.7329 of Var(H)_DIS = 1.8152 +- 0.0844; tail-aware plain sigmas sqrt(Var_DIS tau / n) are 0.004222 (S1)
  and 0.004672 (S2) against stated 0.003747 and 0.003999. On the 4 x 4 calibration state the plain runs captured
  53% and 16% of the exact Var(H) and came out below the exact <H> both times (z -0.47, -2.20). The DIS estimate (S3)
  does not have this problem: its weights are bounded (w <= 2, max seen 1.9641) and so are its summands
  |w E_loc| (|psi| |H psi| / m with m >= |psi|^2/2 and m >= nu/2), so its jackknife error is a genuine CLT error;
  it passed its 4 x 4 calibration (z 1.86, Var ratio 1.091). The claim survives on S3 alone (gap 0.079382 =
  24.4 sigma_DIS).
- **F3, "file re-fetched live immediately before claiming".** The claim's fetch was 2026-10-23T15:08:00Z and the
  last claim measurement (S2) ended 2026-10-23T17:23:55Z, so the fetch was not immediately before claiming. My own fetch at 2026-10-23T17:32:29Z (HTTP 200)
  gives the identical sha256 0d0e85250570199179a9696a8ab8e71292b99993788ab492f64039b5d8c5a34d, and the commits API
  (HTTP 200, 2026-10-23T17:32:30Z) still shows last commit 390a21eab7eb (2024-10-22T08:50:50Z). Satisfied in
  substance.
- **F4, pre-registration change.** PREREG.md (15:12:57Z) closed its claim line when I2a and I3(b) failed
  (15:43:46Z, 15:44:02Z); PREREG.v2 (15:48:29Z) replaced the two instruments and dropped candidate (2), before the
  first 10 x 10 estimate (S1 start 15:55:14Z per results/S1_plain_31337.json). The object, seeds, bar, margin and
  layout are unchanged; the changes were made after seeing 4 x 4 instrument results, not 10 x 10 energies. Not a
  result-driven loosening of the claim bars. (The checkpoint itself comes from a previous night's run whose
  numbers the claimant had seen; that does not bias fresh-seed re-estimates of a fixed, hashed state.)

## Null models and sanity checks

- Instrument nulls in the package: exact 4 x 4 ground state gives zero-variance E_loc (7.08e-11) and MC = E0 to
  1.07e-13; the perturbed known negative is reproduced (z -0.19).
- Rigorous floor: the SDP lower bounds of arXiv:2310.05844 at L = 10 (-0.59945283 at J2 = 0.8, -0.72475248 at 1.0)
  and H(0.9) = (H(0.8) + H(1.0))/2 give E0(0.9) >= -0.662102655 per site (-264.84 Pauli); the claimed -0.63438 is
  above it. With the lowest published 10 x 10 values at J2 = 0.8 (-0.574130) and 1.0 (-0.69670) the claimed value gives slopes -0.602536 and -0.623164 per unit J2 (S2; S3: -0.602385, -0.623315), decreasing as concavity of E0(J2) requires (weak check).
- The claim's energy is 2.1e-4 per site below the ViT value; no physical bound is violated.

## Arithmetic I re-did (python on results/*.json)

- E_bar = -0.634170 x 400 = -253.668; 1e-6 |E_bar| = 0.000253668.
- Claim margin 3 max(sigma_S2, sigma_S3) = 0.011997693193300431; S2 gap 0.08542431118172544; S2 below DMRG by
  2.966851000512378; S3 gap 0.07938165943838271 (24.4 sigma_DIS).
- Tail-aware sigma_new, sigma_best = 0: margins 0.012667 / 0.014015 / 0.009746 (S1 / S2 / S3), gap/margin
  6.35 / 6.1 / 8.15. With sigma_best = 0.0060: margins 0.02201 / 0.022813 / 0.020469, gap/margin 3.66 / 3.74 / 3.88.
- Per site (S.S): S2 -0.6343835607779543, S3 -0.634368454148596 vs bar -0.634170 (S2 lower by 0.00021356).

## Files I used (relative to claim/ unless marked)

- CLAIM.md, REPRODUCE.md, inputs/prereg/PREREG.md, inputs/prereg/PREREG.v2.md, inputs/varbench/*,
  inputs/bar/arxiv_2606.04558v2_tableI.txt, inputs/instrument_checks/*.json, results/*.json, tools/estimator2.py,
  tools/checks.py, tools/tail_sign.py, object/model/nqs.py, object/model/load_example.py, object/r10_J0.9_B1.config.json.
- Hashes I computed match the claim: object/r10_J0.9_B1.pt e68644979db4d9764ac1787d1c064fe18c4750cb4cb47ee573e40588bcd9c485,
  object/model/nqs.py 122e54f2cdecae6a5bad5820d14165abd8e849ee20ff4e3d83dd9901ea00c03d,
  inputs/varbench/square_100_P_0.9.md 0d0e85250570199179a9696a8ab8e71292b99993788ab492f64039b5d8c5a34d.
- My scratch (panel-criterion/mycode/, not published): my_ed.py (sha256 a50280498d3347263943a846398a1805ab976a39cf2a9abdf0c18b8942a972e3),
  my_mc.py, analyse.py, snap41.pt (my 41 rounds, sha256 fd209a962f4ae3c7ad91bfef0d139c00837cf724bc5ee95ab2de74dd47a7ca2f).
- Web (HTTP 200 each): raw.githubusercontent.com varbench J1J2/square_100_P_0.9.md and api.github.com commits
  (2026-10-23T17:32:29Z / 17:32:30Z); arxiv.org abs and pdf of 2606.04558v1 and v2 (17:32:52Z to 17:32:59Z);
  pdf of 2206.14307 (17:33:54Z), 2310.05844, 2602.02665, 2204.07816, 2304.01996, 2608.21291 (17:34:50Z to 17:35:06Z),
  2002.04613 (17:35:42Z); plus web searches. The literature search is a modest one; a NOVELTY reader should not treat
  it as exhaustive.

pass: true
