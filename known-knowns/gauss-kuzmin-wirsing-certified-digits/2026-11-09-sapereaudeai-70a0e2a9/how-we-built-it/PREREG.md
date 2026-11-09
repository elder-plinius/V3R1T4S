# PREREG (frozen 2026-11-09T08:05:47Z, before any N = 2400 vector exists and before any certify run of this run at N = 2400)

## What was already seen (said openly)

- Run 2026-11-09-0627 certified N = 2000: D = 601 (radius 3.0333e-602 at 2700 bits / J 8000, 2.9538e-602 at 3000 bits /
  J 8800), v_N2000.txt sha256 a27092395d8fbdd4bce9a938f86bbd8cbf116af5657e5fd2c20225b0614d39cb, centre
  mu_649full.txt (sha256 5afb3633cc55b9b0dfc7d89fcd6423fe1161da4418ac897b2e6c439d08fc4743), panel 3/3, package
  outbox/2026-11-09-sapereaudeai-c7e57e15 (unsubmitted). That run's dossier predicted about 720 at N = 2400
  (0.30 certified decimals per N: 89 / 300 / 451 / 601 at N = 300 / 1000 / 1500 / 2000).
- Before this file, this run only: (a) checked the modified eigvec (P applied by exact integer polynomial composition
  instead of a stored matrix; Rayleigh-quotient centre written to a file) against the previous eigvec at N = 300, 500
  bits, 25 cycles cold: vectors agree to 1.4e-132; certify of that new N = 300 vector with its own Rayleigh centre
  (500 bits, J 1200): D = 89, the same as calibration C1 of run 2026-11-08-2057; that N = 300 Rayleigh centre agrees
  with mu_649full.txt to about 115 decimals; (b) a two-cycle memory calibration at N = 800, 3300 bits: peak 333 MB.
  No vector with N > 2000 has been computed or certified.

## Criterion (verbatim, bank/targets.json)

Success means a rigorous enclosure of lambda_2 with radius below 10^-D, D STRICTLY GREATER (direction: max) than the
certified digit count on https://teorth.github.io/optimizationproblems/constants/83a.html and in any open pull request
touching constants/83a.md (currently 175, Nisoli 2026), re-fetched immediately before claiming. The enclosure's centre
must agree with Nisoli's 175-digit centre to within the two radii. The certificate is a program in rigorous arithmetic
(Arb, python-flint, IntervalArithmetic.jl or exact rationals) that bounds the discretisation error on a stated function
space and certifies isolation of lambda_2 (for example by a resolvent bound on a contour), and a skeptic reruns it.

## Route (fixed; the certify mathematics is unchanged from runs 2026-11-08-2057 and 2026-11-09-0627)

H^2(D), D = {|z - 3/5| < 4/5}; program attempts/certify-N2400/code/gkw_cert.py. Its certify part (everything from
frob_upper on, except the eigvec argument parsing) is byte-for-byte the panelled version of run 2026-11-09-0627 (checked
with diff). Changes, all in the non-rigorous eigvec step: (1) the factor P is applied by exact fmpz_poly composition
(no stored N x N matrix; saves about 1.4 GB); (2) an optional MUOUT argument writes the Rayleigh quotient
<v, Mv>/<v, v> of the final v for the N-section M at the working precision. The centre mu is an input to certify like
any other: the certificate (Lemma 11 of PROOF.md) holds for every real mu and every nonzero v, so where mu came from
does not matter.

## Schedule (fixed)

- Main S (N = 2400): eigvec N 2400, PREC 3400, CYCLES 40, warm start from inputs/v_N2000.txt, 12 threads, MUOUT
  inputs/mu_N2400.txt -> inputs/v_N2400.txt. Started only after 08:45 UTC and only with free RAM above about 6 GB
  (machine note). mu = arb(first token of inputs/mu_N2400.txt).mid() at each run's precision.
  - S1: certify K 80, PREC 3400, J 9600, r0 0.01, rho 0.2, Q2 64, Qrho 256.
  - S2 (same v and mu file): certify K 80, PREC 3800, J 10560, r0 0.01, rho 0.2, Q2 96, Qrho 256.
- Fallback F (N = 2000): the already certified D = 601 of run 2026-11-09-0627 (package c7e57e15). It is NOT recomputed
  here. If S does not count, the run reports "N = 2000 stays best" and builds no new package.
- Negative control NEG: the S vector with mu shifted by +10^-700 (inputs/mu_N2400_shift700.txt), PREC 3400, J 9600,
  Q2 64, Qrho 256. Its radius must be >= 10^-700 / 2 (the certifier must not certify a wrong centre).
- S is the claim object only if S1 and S2 both count (rule below) and both finish by 09:20 UTC. No N above 2400 is
  attempted in this run (time: the panel and write-up need the last 40 minutes before 09:57 UTC).

## Certified-digit count rule (fixed)

For each certify run, D_run = the largest integer D with radius < 10^-D (checked in arb). A run counts only if
isolation_ok is true (n_eig_total = K = 80, exactly 1 eigenvalue of A_K in Gamma_2, exactly 2 with |z| > rho,
|mu| - r0 > rho) and both small-gain products are < 1. The claimed count is D = min(D_1, D_2) over S1 and S2. The C_83
enclosure is [-mu - radius, -mu + radius] with the larger of the two radii (the hull, outward-rounded, by enclosure.py).

## Thresholds (fixed)

- Claim the full win only if D >= 176, D is strictly greater than the live count on the 83a page and in every open PR
  touching constants/83a.md (re-fetched before the claim), and |(-mu) - Nisoli centre| <= radius + 10^-175 (computed
  exactly from the decimal strings by compare.py).
- A new package supersedes c7e57e15 only if D > 601. The human's goal is 700+; the report states D plainly whether or
  not it reaches 700. Expected: about 720.

null_test: not needed because the claim is an explicit rigorous enclosure checked by a deterministic program in ball arithmetic against a table value; no search or statistical claim is made.

## Known positive / negative checks (fixed)

- Positive: every counted run's centre must contain Nisoli's 175-digit centre (within radius + 10^-175), the OEIS
  A038517 b-file (382 decimals) within radius + 10^-382, and the 649-decimal non-certified value of run 2026-11-08-1936
  within radius + 10^-649. Because mu now comes from the N = 2400 Rayleigh quotient and not from that 649-decimal file,
  the last check is no longer circular.
- Negative: NEG above, and the contrarian lens's mutation control (one coefficient of v sign-flipped).
