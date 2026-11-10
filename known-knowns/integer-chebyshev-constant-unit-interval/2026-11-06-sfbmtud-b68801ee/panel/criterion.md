# Criterion audit: frozen final upper-bound object

context: Fresh criterion subagent at the initial assignment, resumed to audit the frozen final object; initial context was only the claim package, and later reads were limited to that package and this subagent's own checker/evidence, with no attempt histories, root notes, other panel verdicts, previous conversations, or workspace inventory read.

confirmed_scope: The explicit 213-factor integer polynomial in ../claim/object/candidate.json with SHA-256 b68801eed7ca3043a7b817aa6567d92b6d73519c3be888936589519de71055ce has degree 2000000000052 and normalized supremum norm on [0,1] strictly below the exact rational 0.422640947, which is strictly below 0.422684697505.

The frozen object passes the explicit-polynomial, strict-threshold, and complete
interval-coverage requirements of criterion (A) in [TARGET.md](../claim/TARGET.md).
This is an A-target mathematical improvement, not merely the named partial win
p1: the audited object is a new factor product, not the shipped published
polynomial whose independent re-verification defines p1. The literal additional
requirement to compare against the best bounds published at verification time,
including rereading the abstract, version history, and 2026 literature, remains
a dependency on the separate current-source/novelty review. This claim-only
audit does not establish that literature review. The pass below is restricted
to the confirmed scope and mathematical criterion audit; it must not be used
alone to assert a current global record.

The final candidate SHA above was checked before and after the computation.
The exact target is 422640947/1000000000. The exact criterion comparator is
84536939501/200000000000, with positive difference
8750101/200000000000 = 0.000043750505. Both decimals were parsed as exact
rationals, never as binary floating-point numbers. The final claim asks for a
strict inequality even against its own threshold; the independent computation
proves this stronger strict comparison.

The independent implementation is
[final_independent_criterion_check.py](criterion_evidence/final_independent_criterion_check.py),
with [configuration](criterion_evidence/final/configuration.json),
[result](criterion_evidence/final/result.json), and
[complete per-cell evidence](criterion_evidence/final/independent_cover.json).
It imports no claimant checker. The previous v2 checker and evidence remain
unchanged. Claimant reference mathematics was inspected during the initial v2
audit, so the implementation was not blind; its separate formulation and full
recomputation are the basis of this audit. The final revision sets Arb precision
to 384 bits before calculation, pins the expected object hash and target, and
adds an explicit strict maximum-upper-versus-log-lower assertion. No sampled
pass or unrecorded precision change was used.

All 213 coefficient lists consist of exact integers with nonzero leading
coefficient. Every exponent is a positive exact integer; fractional, negative,
and Boolean exponents are rejected. Every degree is independently recomputed
from the actual coefficient list. Exact integer expansion of R_j(x-x²)
confirms degree 2 deg R_j and coefficientwise invariance under x→1-x for every
factor. The exact weighted w-degree is 1000000000026 and the exact x-degree is
2000000000052. A product of nonzero polynomials has the sum of its factor
degrees with multiplicity, so the large displayed degree is an exact finite
degree, not an asymptotic or rounded normalization. Integer arithmetic avoids
overflow or coefficient truncation. Primitivity, irreducibility, and distinctness
are not requirements for this upper-bound construction.

The supplied interval cover contains 9,174 cells and has SHA-256
4ba700f17c0a9ac847cbbbda52373d42c64b99c710e1073c7f994fbe24e1de0f.
The independent checker maps all dyadic endpoints to integers on a common
grid, then checks exact adjacency from 0 through 1/4, rejecting any gap,
overlap, missing endpoint, or out-of-domain cell. Supplied success flags are
not used to establish the result. All stored upper bounds are checked against
the target, but their validity as function enclosures is not assumed.

Every initial cell is independently bounded; where the independent estimate
does not suffice, the cell is bisected and both children are required. This
evaluated 11,526 cells and produced 10,350 certified final leaves, at maximum
depth 22, with no pending cells. Exact coverage was checked again on the final
partition. Every final leaf carries its independently recomputed upper log
endpoint as an exact integer mantissa times a power of two.

For each cell midpoint m and radius h, outward Arb arithmetic encloses the
coefficients of R_j(m+t). The triangle bound Σ|a_i|h^i encloses |R_j| for all
|t|≤h. The sum of its logarithms with positive exponent weights proves 4,744
leaves. It remains valid at polynomial roots, where the actual logarithmic
objective is minus infinity.

For the other 5,606 leaves, all factor ranges exclude zero. The checker
encloses F(m), F′(m), and F″ throughout the cell for
F=Σ e_j log|R_j|, using R′/R and R″/R−(R′/R)². Taylor's theorem gives
F(m+t)≤upper(F(m))+upper(|F′(m)|)h+max(0,upper(F″))h²/2.
Discarding negative curvature is conservative and avoids any maximizer or
quadratic-vertex assumption. The full outward-enclosed expression is divided
by the exact x-degree. No assumption that all factor roots are real, no finite
grid maximum, and no optimization solver's output is used as proof.

The worst independently certified log upper endpoint is approximately
-0.86123228545110983852405374964433082361. Its exact dyadic representation is
strictly below the independently enclosed lower endpoint of log(0.422640947).
The exponential enclosure is approximately
0.42264094699992893686546934201769280968, rigorously below the exact claimed
threshold. These displayed approximations are diagnostic; the comparisons use
the exact dyadic endpoints recorded in the result and outward logarithm
enclosures. Because w=x(1-x) maps [0,1] onto [0,1/4], this finite complete cover
bounds the supremum on the entire x-domain, not just half the x-domain or a
set of sample points.

All 17 structural, coverage, and calibration controls passed at the final
precision. They include rejection of noninteger or Boolean coefficients,
negative/fractional/Boolean exponents, a zero leading coefficient, incorrect
factor and total degrees, an incorrect factor count, malformed covers, and
positive/negative threshold tests against the known exact normalized norm
1/2 of x(1-x). Squaring that polynomial checks the exponent/degree scaling.

Criterion (B), Theorem 7's lower-bound hypotheses, and Pritsker's lower method
are not bundled with this upper claim and were not used. The supplied finite
library obstruction statements, if separately verified, concern only those
specified libraries; they are not unrestricted lower bounds on the integer
Chebyshev constant. No such obstruction is needed for the upper certificate
proved here. No exact value of the constant, globally optimal polynomial,
degree-optimal polynomial, or new lower bound is confirmed.

Null-model requirements for empirical discovery claims do not apply to this
deterministic finite polynomial certificate. Its guarantees come from exact
integer structure, complete domain coverage, outward enclosures, and the
explicit strict rational comparison. Novelty and source-currentness remain
separate dependencies rather than conclusions inferred from numerical search.

pass: true
