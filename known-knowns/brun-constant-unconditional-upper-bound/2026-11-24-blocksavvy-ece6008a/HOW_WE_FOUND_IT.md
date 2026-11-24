# How we found it (contributor text, unverified)
- Start: our e6b84d42 package (B < 2.126988) bounds the Selberg remainder by (sum|lambda_d|)^2. A float probe showed the per-modulus sums
  rho_q cancel: sum_q|rho_q| is about 0.645 of that. A long-double version gave 2.1257394 the same night.
- This run (frozen PREREG): exact rational weights, exact int128 sums with an exact rounding bound, an independent checker (ball-arithmetic
  weights, sort-based exact sums), controls K1-K6 (switch-off reproduces 2.1269872000642055706 exactly; exact Fractions for n <= 300; long
  double agreement 1.3e-11; Lambda == W/V exactly; 5 tampered certificates rejected). One mistake: a first control run included a
  non-preregistered condition and printed FAIL; it was removed and disclosed.
- Panel: three fresh contexts passed it. NOVELTY found the per-modulus combination is textbook (Tao 254A Notes 4 eq. (28)); credited.
- Lead not included: using it up to z = 50000 gives 2.12541917 (needs a bigger-memory checker).
