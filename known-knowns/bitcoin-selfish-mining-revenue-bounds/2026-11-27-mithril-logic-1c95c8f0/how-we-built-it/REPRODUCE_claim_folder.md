# Reproduce (all paths relative to claim/)
Requirements: python3 (standard library) for the checkers; numpy for part 4 of verify_compensation.py and for the
builders in code/build/. Times below are from this machine (8 cores, one used).

1. All certificate checks and negative controls (~30 s total; expected verdicts in CLAIM.md):
     sh run_checks.sh
   Main line to look for:
     python3 code/check_cert.py certs/upper_a45_T2000_rho67005787.txt.gz both
     -> variant printed / corrected: max residual g = -29177/5497558138880 ... CERT_OK ; last line CERT_OK
   Lower:  python3 code/check_policy.py certs/lower_a45_T1500_rho67005786.txt.gz certs/lower_a45_T1500_rho67005786.pol.gz under
     -> exact min residual g_lo = 837/1374389534720 ... POLICY_GAIN_POSITIVE
2. The corrected expectations (E1, E2):  python3 code/verify_compensation.py   (~20 s)
3. Rebuild (numpy; float Gauss-Seidel solver of the label-collapsed SSP form, see code/build/ssp.py):
     python3 code/build/roots.py 0.425 95 under 0.5 0.7 1e-6        # calibration, SSZ 0.56808
     python3 code/build/roots.py 0.45 95 under 0.6 0.75 1e-6        # calibration, SSZ 0.66891
     python3 code/build/roots.py 0.45 2000 max 0.67005 0.67008 1e-10 # corrected+printed max root (~80 s)
     python3 code/build/roots.py 0.45 1500 under 0.67005 0.67007 1e-10 # lower root (~6 min)

     (from claim/) sh code/build/make_all.sh   # rebuilds every file in certs/ except the tampered one (~10 min)
   Builder modes: under | printed | corrected | max (max = pointwise max of printed and corrected compensation, so
   its certificate is checked under both).
Certificate file format: gzip text; line 1 JSON header (alpha, rho, T, scale_log2 = 40, label_invariant), then T+1
lines, line a holds the integers H[a][0..T]; bias h(a,h,f) = H[a][h] / 2^40. Policy files: T+1 lines of T+1 chars
(a = adopt, w = wait, o = override), same for every label.
Skeptics: please write your own builder/checker from 1507.06183.pdf (Table 1, Sec. 4.2, Lemma 13, Prop. 3 proof)
and the derivation in CLAIM.md rather than trust code/; only the H integers are needed from certs/.
