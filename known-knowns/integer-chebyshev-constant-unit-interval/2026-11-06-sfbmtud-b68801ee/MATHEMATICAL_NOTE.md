# A certified upper bound for the integer Chebyshev constant of [0,1]

**Proof status: complete for the exact object below.** Two independently developed claimant checkers and an isolated independent reproducer certify the bound. The latter separately replayed every cell. A separate criterion reviewer also recomputed the complete cover. This is an AI-assisted computational proof record, not external peer review.

## Object and certified bound

The accompanying [factor file](object/candidate.json) defines an integer polynomial through 213 factors and positive integer exponents. Its exact structural data are:

| Quantity | Value |
|---|---:|
| Number of factors | 213 |
| Degree in $w$ | $N=1{,}000{,}000{,}000{,}026$ |
| Degree in $x$ | $D=2N=2{,}000{,}000{,}000{,}052$ |
| Certified upper bound | $T=422640947/10^9=0.422640947$ |

The SHA-256 digest of the factor file is

```text
b68801eed7ca3043a7b817aa6567d92b6d73519c3be888936589519de71055ce
```

The verified finite-cover certificates establish

\[
t_{\mathbb Z}([0,1])\leq T.
\]

The comparison source, Niedbala Giraudin's preprint [G], states the bounds

\[
0.422228600019\leq t_{\mathbb Z}([0,1])\leq0.422684697505.
\]

The certified $T$ is strictly smaller than that reference upper bound by the exact decimal $0.000043750505$. This is a comparison with the specified source, not a claim that the exact constant or an optimal polynomial has been determined. The separate novelty review reread the primary source and found no better competing numerical bound in its documented searches.

## Why one integer polynomial is sufficient

For $n\geq1$, define

\[
a_n=\inf\{\|Q\|_{[0,1]}:0\ne Q\in\mathbb Z[x],\ \deg Q\leq n\},
\qquad
\|Q\|_{[0,1]}=\max_{x\in[0,1]}|Q(x)|.
\]

Products give $a_{m+n}\leq a_ma_n$. Submultiplicativity therefore gives the limit

\[
t_{\mathbb Z}([0,1])=\lim_{n\to\infty}a_n^{1/n}
=\inf_{n\geq1}a_n^{1/n}.
\]

In particular, if $P\in\mathbb Z[x]$ has positive degree $D$, then $P^k$ has degree $kD$ and norm $\|P\|^k$. Hence

\[
a_{kD}^{1/(kD)}\leq\|P\|_{[0,1]}^{1/D},
\qquad
t_{\mathbb Z}([0,1])\leq\|P\|_{[0,1]}^{1/D}.
\]

No claim that $P$ minimizes the norm in its degree is needed.

Write the supplied factors as $R_j(w)\in\mathbb Z[w]$, with positive degrees $d_j$, and their exponents as $e_j\in\mathbb Z_{>0}$. The object is

\[
W(w)=\prod_{j=1}^{213}R_j(w)^{e_j},
\qquad P(x)=W(x(1-x)).
\]

Substitution gives integer coefficients and invariance under $x\mapsto1-x$. A nonzero leading term of degree $d_j$ becomes a nonzero leading term of degree $2d_j$, so $\deg P=2\sum_j e_jd_j=D$ exactly. Since $x(1-x)$ maps $[0,1]$ onto $[0,1/4]$, the two supremum norms agree. Irreducibility of the factors is not required for this upper-bound argument.

## Finite-cover proof obligations

Define the extended-real logarithmic function

\[
F(w)=\frac1D\sum_j e_j\log|R_j(w)|,
\qquad w\in[0,1/4].
\]

At a factor zero, $F=-\infty$. Elsewhere it is finite, and

\[
\log\bigl(\|P\|_{[0,1]}^{1/D}\bigr)=\sup_{[0,1/4]}F.
\]

A sufficient certificate consists of a finite rational partition $I_1,\ldots,I_m$ of $[0,1/4]$, together with rigorously computed upper bounds $U_k\geq\sup_{I_k}F$. In the completed certificates, every $U_k$ is strictly below a rigorous lower enclosure for $\log T$. Finiteness therefore proves $\|P\|^{1/D}<T$, and the powers argument proves the displayed conclusion.

The verification must check the exact file digest; integer coefficient and exponent types; positive exponents and actual factor degrees; the sums defining $N,D$; and exact coverage with no gaps or overlapping interiors. All retained cells must pass the bound, with no unresolved cells. A timeout, a depth limit, or an unfinished partition is inconclusive.

One elementary bounding mechanism is entirely algebraic. On $I=[a,b]$, express

\[
R_j(a+(b-a)t)=\sum_{r=0}^{d_j}\beta_{jr}\binom{d_j}{r}t^r(1-t)^{d_j-r},
\qquad0\leq t\leq1.
\]

The coefficients $\beta_{jr}$ are rational. The Bernstein basis is nonnegative and sums to one, so $|R_j|\leq\max_r|\beta_{jr}|$ on $I$. Outward logarithm bounds then give an upper bound for $F$. Subdivision, derivative signs and rigorously bounded Taylor remainders can sharpen this bound. Any such sharpening must retain its own verified hypotheses. Complex roots are allowed; global concavity of the logarithmic objective is not assumed.

The implementation record uses separately developed arithmetic representations: outward interval arithmetic and rational Bernstein calculations with certified logarithmic bounds. Their final receipts refer to the digest above. A rounded decimal maximum or a dense sampling grid is not a substitute for this finite-cover proof.

## Search procedure and a limited library obstruction

Candidate generation used semi-infinite linear-programming ideas, additional sample constraints near suspected extrema, weighted lattice reduction, exact factorization, and rationalization to integer exponents. Those steps select a possible object. Only the subsequent verification establishes its norm bound. Searches are bounded and do not prove global optimality.

A useful separate lemma distinguishes additional factors from reweighting a fixed library. Let $S_j\in\mathbb Z[w]$ have degrees $s_j>0$, and let $\lambda$ be a probability measure on $[0,1/4]$ for which all integrals below are finite. For $L>0$, suppose

\[
\frac1{s_j}\int\log|S_j(w)|\,d\lambda(w)\geq2\log L
\quad\text{for every }j,
\]

Then every nonnegative real weighting $b_j$, with $\sum_jb_j=1$, satisfies the following inequality, with zero-weight terms omitted at their zeros:

\[
\sup_{w\in[0,1/4]}\sum_jb_j\frac{\log|S_j(w)|}{s_j}
\geq\sum_jb_j\frac1{s_j}\int\log|S_j|\,d\lambda
\geq2\log L.
\]

For integer products with nonnegative exponents $e_j$, not all zero, take $b_j=e_js_j/\sum_i e_is_i$; their normalized $x$-norm is therefore at least $L$. This is a lower bound only for products from the specified finite library, not for unrestricted integer polynomials.

Separate rational atomic witnesses and outward checks in the [library-obstruction record](the-record-we-beat/fixed-library-obstruction/STATEMENT.md) give the conservative floors:

| Audited finite library | Normalized norm lower floor |
|---|---:|
| The original 92 upper-certificate factors | $0.422684674774607313$ |
| The 258-factor union with audited symmetric transports of the original lower library | $0.422684490944649449$ |

The second statement also covers the corresponding unsymmetrized products. If $Q$ has degree $d>0$ and $Q^\#(x)=Q(1-x)$, then $QQ^\#$ has degree $2d$ and

\[
\|QQ^\#\|_{[0,1]}^{1/(2d)}\leq\|Q\|_{[0,1]}^{1/d}.
\]

The exact transport audit places these reflected products in the symmetric library, up to sign. Its floor therefore also bounds the original products. Both floors exceed the certified $T$. Thus reweighting these particular libraries cannot attain $T$. This does not exclude other published factors or establish broad novelty by itself. The novelty reviewer independently rederived and recomputed these finite-library witnesses; they support the comparison and are not additional unrestricted lower-bound claims.

## Limitations and credits

The construction builds on published factor libraries and methods, particularly the work of Niedbala Giraudin [G], Hare and Hodges [HH], Hare's Gorshkov–Wirsing constructions cited in [G], and Flammang [F]. Pritsker's weighted-potential approach [P] supplies important lower-bound context. Qu and Yang [QY] give a structural characterization of the constant; that identity does not itself supply the decimal comparison used here. Exact factor provenance is recorded separately. No claim is made that every factor, the optimization framework, or the underlying inequalities are new.

The completed checks establish the bound for this object only. They do not determine $t_{\mathbb Z}([0,1])$, prove optimality of the 213-factor library, or replace external mathematical review.

| Final verification field | Actual result |
|---|---|
| Exact-object finite-cover receipts | 9,174 cells at 384-bit Arb, 120.31 s; 9,609 exact Bernstein cells, 222.18 s |
| Isolated independent proof and replay | 10,576 cells; proof 53.10 s and complete replay 22.46 s; frozen checker SHA ac927e7aff6c6f9c63aafe7404c171ba31e03e33b3da38eb88535d95091073fa |
| Criterion and current-source comparison | All three final reviews pass for the exact object SHA above; source receipt 2026-11-05T22:56:49.458826Z, search refresh 2026-11-06T00:03:29.434Z |

## References

- **[G]** David Niedbala Giraudin, *New bounds for the integer Chebyshev constant of [0,1]*, [arXiv:2610.00386v3](https://arxiv.org/abs/2610.00386v3), especially Theorems 1–2 and the accompanying certificates. Preprint.
- **[HH]** Kevin G. Hare and Philip W. Hodges, *Applications of Integer and Semi-Infinite Programming to the Integer Chebyshev Problem*, [arXiv:1804.05985v2](https://arxiv.org/abs/1804.05985v2). Title follows the arXiv metadata.
- **[F]** Valérie Flammang, *On the absolute length of polynomials having all zeros in a sector*, *Journal of Number Theory* **143** (2014), 385–401, [doi:10.1016/j.jnt.2014.04.002](https://doi.org/10.1016/j.jnt.2014.04.002).
- **[P]** Igor E. Pritsker, *Small polynomials with integer coefficients*, *Journal d'Analyse Mathématique* **96** (2005), 151–190, [arXiv:math/0101166](https://arxiv.org/abs/math/0101166).
- **[QY]** Binggang Qu and Chengyuan Yang, *Limit distribution of algebraic integral points on curves*, [arXiv:2609.39505v1](https://arxiv.org/abs/2609.39505v1), Section 1.5, Theorem H.
