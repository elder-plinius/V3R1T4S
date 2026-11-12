# How we found it (contributor text, unverified)

The brief was to reproduce Frolov's Table I before trying to beat it. We generated closed-form matrix elements for
L = 1 and L = 2 exponential bases with sympy (Cartesian tensors instead of bipolar harmonics), ran them in GMP
multiprecision, and wrote a second, independent derivation for the arb checker; the two agree to 45 digits.
What failed: complex exponents (worse than real ones at equal size in a short test) and the dtmu (2,0) cell (our
1,280-function value is 3e-12 above the table). What worked: three real-exponent boxes (tensor types rr, xy, xx)
whose bounds were optimised by a greedy random search at 240 functions and then doubled. The ddmu (2,0) column of
Table I turned out to be far from converged, so a few hundred well-placed functions already lie below its
last row.
