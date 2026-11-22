# Reproduce report, kings-a247413-d33

context: Claude Code subagent, fresh context [Sonnet 5.5]

Claim folder checked against the contributor's hash list: all files OK. Copied to a private location and worked only there. No network used.

## Definition used (from the claim)
Lambda = lim Z(m,n)^(1/(mn)), Z(m,n) = number of independent sets of the m x n king graph (A063443), i.e. e^kappa at unit activity (A247413). lambda_m = dominant eigenvalue of the column transfer matrix of the open king strip of m rows. Criterion clauses checked here: (a) two methods agree on D = 33 decimals, (b) both begin with the 18 published digits, (c) stable over four successive truncations.

## Step 1. My own checker, written before opening the author's programs (my own files, not shipped in this package)
- My own transfer-matrix script: independent-set row states, compatibility a&b = a&(b<<1) = a&(b>>1) = 0, exact-integer power iteration (400 sweeps, 2^400 scaling), lambda^2 ~ |Tv|^2/|v|^2. Widths 2..16 at about 60 digits.
- tm.c: separate broken-profile (cell by cell) double-precision transfer matrix, widths 6..26.
- Result against object/lam_open.txt: widths 2..16 agree to 58-61 digits (width 2 exactly; the object's own values carry a rounding error near 1e-60, mine used more sweeps). Widths 6..26 in double precision agree to relative difference 1e-16 to 3e-16 (all within double rounding; width 25 and 26 included; see my script outputs, not shipped). Widths 27..40 could not be reached by my own code in the time (state space 2^m for my C code); they were checked only through the author's program rerun (below).
- My own Wynn script: a Wynn epsilon implementation (recipe of PREREG_B.md: ratios r_m = lambda_m/lambda_(m-1) from m=3, last entry of highest even epsilon column, mmax = 22..40, mpmath at 60 digits; repeated at 120 digits) run on the object's lambda lists (lam_open.txt for widths up to 28, lam_open_lean.txt for 29..40). Output:
  E(37) = 1.3426439511246012978517301618757402929...
  E(38) = 1.3426439511246012978517301618757403859...
  E(39) = 1.3426439511246012978517301618757403932...
  E(40) = 1.3426439511246012978517301618757403963110527103542
  Windows of four successive mmax ending at 40, 39, 38, 37, 36, 35, 34: 33, 32, 31, 30, 29, 28, 27 common decimals. Same at 120 digits. E(40) and the claimed method A value share 35 decimals. These match the object's prereg_b_output.txt claims exactly (33 common decimals for mmax = 37..40).

## Step 2. Author's programs
- sh verify-it-yourself/run_checks.sh: failed checks 0, PASS.
- Built programs/tmlean.c (cc -O3 -march=native); ./tmlean 11 10 4 x count printed 60711713670028729 = A063443(12).
- Reran drivelean.py 100 for width 39 (300 s) and then width 40 (486 s), one after the other, 12 threads (machine was shared and loaded). The lines "39 100 lambda" and "40 100 lambda" in my output files (not shipped) are byte-identical to the shipped lines in object/lam_open_lean.txt (lambda_39 = 112025.49379014986801701350756553..., lambda_40 = 150410.35160877654742050504459253...).
- prereg_b.py rerun in the work copy: output byte-identical to object/prereg_b_output.txt (diff empty).
- Method A: ran sitechain2.sh (python from the shared venv instead of python3), the whole warm-started ladder chi = 20..100 with ctmgen2.py site, 256 bits. For chi = 90 and chi = 100 every iteration line (index and kappa digits) is identical to the shipped sitef_90.log and sitef_100.log. Last lines: chi = 100 kappa-based value 1.34264395112460129785173016187574039571943773385025452179048, chi = 90 ...3957194077485.... My own comparison (my own script, not shipped): chi = 70, 80, 90, 100 share 36 decimals; chi = 80, 90, 100 share 38; A(chi=100) vs E(40) share 35.
- Method C (domino) not rerun (87 minutes each, start files not shipped); it is supporting only and not needed for clauses (a) to (c).

## Clause readings from the reproduced data
- (c) per method: A four chi values 36 common decimals, B four mmax values 33 common decimals. Both at least 33.
- (a)/(b): first 33 decimals of A(100) and E(40) are identical to 1.342643951124601297851730161875740 and both begin with the published 1.34264395112460129. Next digits are 39 in both, so truncation = rounding.
- Mismatches found: none.

## Limits (not hidden)
- Numerical agreement only; no rigorous error bound. Method B accuracy rests on its own convergence plus my reproduction of the same recipe; the start width m0 = 3 was chosen after seeing widths up to 28 (disclosed in PREREG_B.md).
- Widths 27..40 are confirmed by rerunning the author's tmlean (same code, bit-identical), not by independent code of mine; the exact count A063443(12) and my independent widths up to 26 and the matching of tm and tmlean at widths 24 and 28 (shipped) support the program. Method A rests on the author's ctmgen2.py, reproduced by rerun, not by an independent CTM of mine; however B (a different algorithm from my own up to width 26 plus the author's tmlean) agrees with it to 35 decimals, which would be very unlikely by chance.
- Whether D = 33 meets the OEIS-term-count bar, and novelty, are for the other skeptics.

pass: true
