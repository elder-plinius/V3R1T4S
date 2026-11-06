# Finite-library reweighting obstruction

## Statements to check

For every nonnegative real degree-normalized weighting of the 92 integer polynomials in
`original_library.json`, the associated normalized norm on x in [0,1] is strictly greater
than the exact rational 0.4226846. The supplied computation also gives the conservative
lower bound 0.422684674774607313.

For every nonnegative real degree-normalized weighting of the 258 integer polynomials in
`union_library.json`, the associated normalized norm is strictly greater than the exact
rational 0.42267. The supplied computation also gives the conservative lower bound
0.422684490944649449. This union includes every original upper factor and a symmetric
representative of every factor in the shipped lower certificate.

These statements concern the specified finite libraries only. They do not give a lower
bound on the unrestricted integer Chebyshev constant and do not constrain additional factors.

## Certificate lemma

Let R_j be nonzero integer polynomials of positive degrees d_j in w, and let
`mu = sum_k lambda_k delta_(w_k)` be a probability measure with rational positive masses
and rational support in [0,1/4]. Assume all R_j(w_k) are nonzero. Set

`C_j = sum_k lambda_k log|R_j(w_k)| / d_j`.

For all real b_j>=0 with sum b_j=1,

`sup_w sum_j b_j log|R_j(w)|/d_j >= sum_j b_j C_j >= min_j C_j`.

The first inequality follows by averaging values at support points of a probability measure.
For integer exponents e_j and N=sum e_j d_j>0, put b_j=e_j d_j/N. Substitution w=x(1-x)
preserves the norm and changes the degree from N to 2N. Hence the normalized x-norm is
at least `exp(min_j C_j/2)`. The same inequality covers arbitrary nonnegative real b.

`verify.py` checks exact rational positivity and unit mass, domain membership, factor types
and degrees, and the library hash. It evaluates every R_j(p/q) as an exact integer numerator
over q^d_j, then encloses its logarithm with Arb. Each C_j must be rigorously greater than
twice the logarithm of the stated rational threshold. The stronger displayed bounds are
integer decimal floors of rigorous lower endpoints of `exp(min_j C_j/2)`.

## Coverage of both published libraries

`transport_coverage.py` works directly from the integer coefficient lists in the supplied
lower certificate. If Q(x)=Q(1-x), it descends Q to an integer polynomial in w. Otherwise
it descends Q(x)Q(1-x). Descent uses integral leading-term subtraction and is checked by
an exact round-trip. Only an overall sign is changed to choose a positive leading coefficient.
Every resulting polynomial must occur in the union, and every original upper factor must
also occur there.

For any weighted logarithmic objective formed from the original upper factors and lower
library factors, average it with its reflection x->1-x. Its supremum cannot increase.
This average is a degree-normalized combination of the audited symmetric representatives.
Thus the union obstruction applies even to combinations of the two libraries before
symmetrization. No assumption of rational weights or LP optimality is used.

## Reproduction

From this directory, with Python and python-flint installed:

```sh
python verify.py --library original_library.json --measure original_measure.json --precision 384 --out original_result.json
python verify.py --library union_library.json --measure union_measure.json --precision 384 --out union_result.json
python transport_coverage.py --lower lower_certificate.json --union union_library.json --original original_library.json --out transport_result.json
```

Exact equality at a proposed threshold may remain inconclusive. A positive-mass root makes
that dual witness unusable. Canonical measures omit zero-mass atoms. Constants are excluded
from normalized columns; integer constants cannot improve an upper norm because their
absolute values are at least one.

The JSON fixture catalog contains analytic and deliberately corrupted witness cases for
independent calibration. Its expected outcomes are input specifications, not verifier results.
