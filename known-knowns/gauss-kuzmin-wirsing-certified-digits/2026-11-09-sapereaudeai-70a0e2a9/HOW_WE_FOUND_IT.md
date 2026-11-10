# How we found it (contributor text, unverified)

- **Brief.** Push the certified decimal count of the Wirsing constant C_83 = |lambda_2| past what a single pass of the
  same route had given (300 at N = 1000, 601 at N = 2000; both unsubmitted, in the same workspace). The human asked for
  700 or more.
- **Route (unchanged).** Hardy space H^2 of the disc |z - 3/5| < 4/5. A degree N - 1 approximate eigenvector v is found
  by a filtered power iteration in midpoint arithmetic; then everything is ball arithmetic: the residual of the true
  operator (Hankel/Hurwitz-zeta coefficients for j < J plus a proved binomial-zeta tail), a truncation bound for an
  80 x 80 section, small-gain resolvent bounds on two circles, verified eigenvalue isolation and a Gershgorin cross-check,
  and a residual-to-eigenvalue lemma (object/PROOF.md). About 0.30 certified decimals per unit of N.
- **What was new this time.** (1) The Pascal-type factor of the section is applied by exact integer polynomial
  composition instead of a stored matrix, which cut the eigvec memory to 2.8 GB at N = 2400 and 4.2 GB at N = 2800.
  (2) The centre is no longer an external 649-decimal value (which capped D near 648) but the Rayleigh quotient of the
  vector itself, written at full working precision. (3) Warm starts N = 2000 -> 2400 -> 2800, 40 cycles each.
- **What happened.** N = 2400 gave 721 certified decimals at 3400 and 3800 bits (pre-registered main object); the
  machine became free early, so a pre-registered stretch object at N = 2800 was run and gave 842 at 3900 and 4300 bits.
  Controls: a centre shifted by 1e-800 is not certified past the shift (radius 1.65e-800); a sign-flipped coefficient
  drops the result to 300 decimals; the Gershgorin count and a direct evaluation of the operator agree.
- **What failed earlier (previous runs).** A Chebyshev collocation route and Taylor sections about 1/2 gave many
  non-certified digits but no rigorous bound; K = 40 sections failed the small-gain test.
