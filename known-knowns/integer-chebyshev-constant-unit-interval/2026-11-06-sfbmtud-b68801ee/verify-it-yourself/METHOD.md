# Mathematical verification method

This document describes the frozen portable Bernstein checker used by the runner. The wrapper reuses that checker; it is not a second independent mathematical verification. The object, threshold and expected hashes are supplied by `config.json`. Nothing below depends on a particular factor library or numerical threshold.

## Integer object and normalized norm

The object is a list of nonzero polynomials R_j in Z[w] with positive integer exponents e_j. Its product is P(w)=product_j R_j(w)^e_j. The checker requires integer JSON coefficients and exponents, excludes Boolean values, rejects leading zeros and zero polynomials, and verifies every declared degree. Put

N=sum_j e_j deg R_j, and D=2N>0.

Here D is the x-degree of Q(x)=P(x(1-x)). Substitution preserves integer coefficients. It doubles each nonconstant factor's degree because its nonzero leading coefficient multiplies a nonzero leading coefficient of (x-x²)^deg R_j. Thus the exact product degree is D. The map x↦x(1-x) sends [0,1] onto [0,1/4], so

||Q||_[0,1] = ||P||_[0,1/4].

Away from product zeros define F(w)=sum_j e_j log|R_j(w)|. At a product zero set F(w)=-infinity. It is enough to establish F(w)<D log T on a complete finite cover, where T is the exact positive rational decimal in the configuration. Then ||Q||_[0,1]^(1/D)<T.

This gives an upper bound for the integer Chebyshev constant itself. Define a_n as the infimum of ||H||_[0,1] over nonzero integer polynomials of degree at most n. Multiplication gives a_(m+n)<=a_m a_n, so the usual submultiplicative-limit argument gives t_Z([0,1])=lim_n a_n^(1/n)=inf_n a_n^(1/n). In particular t_Z<=a_D^(1/D)<=||Q||^(1/D). The power argument is also explicit: Q^k is an integer polynomial of degree kD and norm ||Q||^k. For n=kD+r with 0<=r<D it is admissible for a_n, hence limsup_n a_n^(1/n)<=||Q||^(1/D). The proof requires an explicit feasible product, not an assertion that it is optimal.

## Exact Bernstein hull and subdivision

For a degree-d polynomial R(w)=sum_(k=0)^d c_k w^k, use t=4w on the initial interval. Write

R(t/4)=sum_(i=0)^d beta_i B_i^d(t),

where B_i^d(t)=C(d,i)t^i(1-t)^(d-i) and

beta_i=sum_(k=0)^i c_k 4^(-k) C(i,k)/C(d,k).

Store beta_i=b_i/Delta with integer b_i and positive common denominator

Delta=4^d lcm_(0<=k<=d) C(d,k).

The Bernstein basis functions are nonnegative and sum to one on [0,1]. Therefore min_i beta_i<=R<=max_i beta_i on the whole interval. In particular |R|<=max_i |beta_i|.

For any later cell [A,B], the stored coefficients represent R(A+(B-A)t) in the same basis. Midpoint de Casteljau subdivision repeatedly replaces neighbouring coefficients by their averages. A numerator row after r steps has denominator Delta*2^r. Collecting the left and right edge entries and scaling them to common denominator Delta*2^d produces exact coefficients on the two children. The implementation uses integer additions and shifts, so no rounding enters these transformations.

## General second-order bound

Suppose every factor's Bernstein coefficient range on a cell has one strict sign. This certifies that every factor is nonzero throughout that cell. Let m=(A+B)/2, h=(B-A)/2 and u=(w-m)/h, with |u|<=1.

For a factor of degree d>0, let v_0,v_1 be the last two integer numerators before the final midpoint step of de Casteljau. Then

R(m)=(v_0+v_1)/(Delta*2^d),

h R'(m)/R(m)=d(v_1-v_0)/(v_0+v_1).

The signed weighted ratios are summed before taking an absolute value; cancellation is therefore retained. Constants contribute zero derivative.

For each factor the general identity

(d²/du²) log|R| = R''_u/R - (R'_u/R)² <= |R''_u|/min_cell |R|

holds without any assumption on its roots. The Bernstein coefficients of R''_u are d(d-1)(b_(i+2)-2b_(i+1)+b_i)/(4 Delta). Define the positive integer

L=min(|min_i b_i|,|max_i b_i|)

and M=max_i |b_(i+2)-2b_(i+1)+b_i|. The denominator Delta cancels, giving

(d²/du²) log|R| <= d(d-1) M/(4L).

Taylor's theorem consequently gives the whole-cell upper bound

F(w)<=F(m)+|hF'(m)|+sum_j e_j d_j(d_j-1) M_j/(8L_j).

The last term is zero for degrees below two. This is a general curvature bound, not a global concavity claim. Factors may have nonreal or repeated roots.

If any factor's coefficient range contains zero, the sign test cannot justify this Taylor bound. The checker instead uses the Bernstein hull bound

F(w)<=sum_j e_j log U_j, where U_j=max_i |b_(j,i)|/Delta_j.

This fallback is valid whether or not the cell actually contains a root. Each U_j is positive because zero polynomials are excluded. At actual product zeros the desired norm bound holds directly.

## Outward logarithms using integers

All logarithm arguments are positive rationals. Exact comparisons write x=2^k y with integer k and 1<=y<2. Set z=(y-1)/(y+1), so 0<=z<1/3. For K>=0,

log y = 2 sum_(n=0)^(K-1) z^(2n+1)/(2n+1) + E,

0<=E<=(9/4) z^(2K+1)/(2K+1).

For the tail bound, replace each denominator in the tail by its first denominator and sum the resulting geometric series; (1-z²)^(-1)<=9/8. The same formula at z=1/3 encloses log 2.

The implementation uses K=48 and fixed-point scale S=2^128. Floor and ceiling integer division enclose z, its squared powers, each positive series term and the tail. The signed k log 2 contribution is assembled with its endpoints reversed when k is negative. Thus the function returns integer lower and upper bounds for S log x. The truncation length affects tightness only: the explicit tail bound guarantees validity.

The midpoint logarithms are rounded upward and multiplied by the positive integer exponents. Each signed derivative ratio is separately floored and ceiled at scale S; after summation, the larger absolute endpoint bounds S|hF'(m)|. Each nonnegative curvature allowance is rounded upward. Consequently the computed integer U bounds S F(w) on the whole cell.

Separately the checker obtains an integer lower bound L_T<=S log T. Acceptance requires the strict integer inequality U<D L_T. Every accepted cell therefore satisfies F(w)<D log T. Floating-point values are used only for time limits and resource counters; they do not participate in acceptance.

## Complete finite dyadic cover

A cell with depth d and index i denotes [i/2^(d+2),(i+1)/2^(d+2)]. The search starts at [0,1/4]. Rejection replaces a cell by its two dyadic children. It never discards an unaccepted cell. A run stopped by time, node or depth limits is inconclusive and cannot produce a successful result.

Completion also requires a second, order-independent exact coverage check. It scales all accepted endpoints to the finest common dyadic grid, sorts the intervals, requires the first endpoint to be zero, each next left endpoint to equal the preceding right endpoint, and the final endpoint to be 1/4. Gaps, positive-length overlaps and duplicate leaves are rejected. Thus the finitely many certified cell bounds cover every point of the interval, including shared endpoints. Their largest integer upper bound remains strictly below D L_T.

## Scope and limitations

The method certifies the stated upper bound for the configured integer product. It does not prove global concavity, optimality, a matching lower bound, novelty, or any official review outcome. A failed or capped enclosure is inconclusive unless a separate mathematical counterexample is supplied.

Only Python's standard library is used. The `resource` module is Unix-specific and serves only resource reporting. Supported execution is Unix with Python 3.9 or later. The portable checker refuses optimized Python (`-O`, `-OO`, or optimization inherited from the environment), since its exact validation uses assertions. The shell runner explicitly sets `PYTHONOPTIMIZE=0` and invokes system `python3 -S`; the child also uses `-S`, so site packages are not loaded. The runner assumes a trusted Python/standard-library installation and a reviewed, frozen configuration. SHA checks establish consistency with that configuration; they do not independently authenticate its provenance.
