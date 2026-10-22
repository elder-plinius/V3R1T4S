# Derivation: why the Collatz-Wielandt ratio of the shipped vector bounds the dimer constant l3

Self-contained. Everything below is either quoted from the source named, or derived here from the definitions.
The source is Qidong He, "A new upper bound on the dimer constant of Z^3", arXiv 2607.28810 (v2). The quotations
are copied from the LaTeX source of that paper (the source archive was fetched on 2026-10-19; see table-record/).
The numbering "Theorem 2.1" etc. is inferred from the order of statements in the source (the source uses
LaTeX labels, not numbers); the labels are given too.

## 1. The inequality used, and its source

He, Theorem (label `thm: bound`, Theorem 2.1 by order), quoted:

    For all $m,n\ge 2$, $\ell_3\le\frac{1}{mn}\log\rho(T_{m,n})$.

where l3 is the dimer constant (He, introduction, quoted):

    $$\ell_3:=\lim_{\substack{a_1,a_2,a_3\to\infty\\a_1a_2a_3\text{ even}}}\frac{1}{a_1a_2a_3}\log f(a_1,a_2,a_3)$$

with f(a1,a2,a3) the number of perfect matchings of the box {0<=x_i<a_i} in Z^3, and T_{m,n} the diagonal transfer
matrix of Section 2 below. The bound used for the claim is this theorem at (m,n) = (5,5), combined with the
Collatz-Wielandt inequality (a standard fact, Horn and Johnson, Matrix Analysis, Theorem 8.1.26, as cited by He):
for a nonnegative square matrix A and a vector x with all entries positive, rho(A) <= max_u (Ax)_u / x_u.

The claim is therefore: l3 <= (1/25) log rho(T_{5,5}) = (1/50) log rho(T^2) <= (1/50) log max over sectors of
the Collatz-Wielandt ratios. The shipped vector gives the ratio for one sector (sector 12); the other twelve
sectors are covered by builder-generated vectors (verify-it-yourself/sectors). This is He's method; the only
new ingredient is that the test vector is the converged one (He used p = 2 iterations from the all-ones vector at
(5,5) for running time; his Corollary 3.4 says every p gives a valid bound, quoted in section 5).

## 2. Definitions (He, Section 2; quoted)

    Let $m,n\ge 2$ be integers. Write $V_{m,n}:=\Z/m\Z\times\Z/n\Z$ ... Define the matrix $A_{m,n}$ ... by
    $\bra{\vec{u}}A_{m,n}\ket{\vec{v}} := \indicator{\set{(0,0),(1,0),(0,1)}}(\vec{v}-\vec{u})$.
    For $R,C\subseteq V_{m,n}$, write $A_{m,n}[R,C]$ for the submatrix of $A_{m,n}$ with row set $R$ and column set $C$.
    Define the matrix $T_{m,n}$, whose rows and columns are indexed by the power set of $V_{m,n}$, by
    $\bra{U}T_{m,n}\ket{V} := \per A_{m,n}[U,V_{m,n}\setminus V]$ if $|U|+|V|=mn$, and $0$ otherwise,
    where $\per$ denotes the permanent, with the convention that the permanent of the empty matrix is $1$.
    Let $\rho(T_{m,n})$ be the spectral radius of $T_{m,n}$.

In words: a state is a subset of the layer V = Z/5 x Z/5 (25 vertices). T[U,W] is the number of ways to match every
vertex of U to a distinct vertex of the next layer, each matched along one of the three forward edges
v -> v, v+(1,0), v+(0,1), such that the vertices of the next layer left unmatched from below are exactly W
(W = V minus the image).

## 3. Proof that the matrix bounds l3 (He's proof, restated with its hypotheses)

(a) Graph. For even l >= 4, Lambda_{m,n,l} = <m(e1-e3), n(e2-e3), l e3> and T_{m,n,l} = Z^3 / Lambda_{m,n,l}.
He shows (quoted): "Under the assumptions on $m,n,l$, no nonzero difference between two elements of
$\{0,\pm e_1,\pm e_2,\pm e_3\}$ belongs to $\Lambda_{m,n,l}$. Hence the six neighbors ... are distinct and none coincides
with $[x]$, so that $T_{m,n,l}$ is simple and 6-regular. Moreover, every element of $\Lambda_{m,n,l}$ has even
coordinate sum, ... making $T_{m,n,l}$ bipartite."

(b) Trace formula. He, Lemma (label `lem: transfer`, Lemma 2.2): "For all $m,n\ge 2$ and even $l\ge 4$,
$\pmatch{T_{m,n,l}}=\tr(T_{m,n}^l)$." Proof idea: the map [x] -> ((x1 mod m, x2 mod n), x1+x2+x3 mod l) is a group
isomorphism onto V x Z/l; every edge goes from the layer at height k to the layer at height k+1, with biadjacency
matrix A_{m,n}; a perfect matching is a cyclic sequence of states S_k (the vertices of layer k matched upward),
consecutive states being U, V with |U|+|V| = mn, and the number of matchings between the layers is T[U,V].
(Checked by computer in this folder: verify-it-yourself/cwcheck.py trace, which builds the quotient graph by a
triangular reduction of Z^d modulo the lattice, independently of the isomorphism, and counts matchings by brute
force: 4752, 194244, 190992 for (2,2,4), (3,2,4), (2,2,6) equal tr(T^l), as in the receipts.)

(c) 2-lifts. A graph H is a 2-lift of G if there is a 2-to-1 map pi: V(H) -> V(G) mapping the neighbourhood of each
vertex of H bijectively onto the neighbourhood of its image. He's lemma: T_{2m,n,l}, T_{m,2n,l}, T_{m,n,2l} are
2-lifts of T_{m,n,l} (the lattice Lambda for the larger graph has index 2 in the smaller one, so the identity map on
Z^3 induces the 2-to-1 map). The inequality of Csikvari, quoted by He (label `thm: 2-lift`, Theorem 2.4 by order,
attributed by He to Csikvari, "Lower matching conjecture, and a new proof of Schrijver's and Gurvits's theorems",
J. Eur. Math. Soc. 2017, Lemma 4.2; we did not fetch Csikvari's paper, so this is quoted as He states it):

    If $G$ is a bipartite graph and $H$ is a $2$-lift of $G$, then, for all $t\ge 0$, $M(H,t)\le M(G,t)^2$.

where M(G,t) = sum_k m_k(G) t^k is the matching generating function. Its corollary (He, label `cor: 2-lift`):
"If $G$ is a bipartite graph and $H$ is a $2$-lift of $G$, then $\pmatch{H}\le\pmatch{G}^2$." (Take t to infinity after
dividing by t^{|V(G)|}.) Hypothesis: the graphs T_{m,n,l} are bipartite by (a).

(d) Box in torus, then lifts. For p >= 2 the lattice Lambda_{2^p m, 2^p n, 2^p} = <2^p m e1, 2^p n e2, 2^p e3> is
rectangular, so the box with sides (2^p m, 2^p n, 2^p) embeds as a spanning subgraph of the torus and every perfect
matching of the box is a perfect matching of the torus: f(2^p m, 2^p n, 2^p) <= pm(T_{2^p m, 2^p n, 2^p}).
Applying the corollary 2p times (each doubling of m or n is a 2-lift, all intermediate graphs have l = 2^p >= 4 even
and m, n >= 2),
pm(T_{2^p m,2^p n,2^p}) <= pm(T_{m,n,2^p})^{2^{2p}}. By (b), pm(T_{m,n,2^p}) = tr(T^{2^p}) <= 2^{mn} rho(T)^{2^p},
since the trace is the sum of the eigenvalues with algebraic multiplicity, at most 2^{mn} of them (the matrix has
2^{mn} rows), each of modulus at most rho. Dividing the logarithm by the volume 2^{3p} m n gives

    (1/(2^{3p} mn)) log f(2^p m, 2^p n, 2^p)  <=  (1/(2^p mn)) log( 2^{mn} rho(T)^{2^p} ).

Let p -> infinity: the left side tends to l3 (the limit defining l3 exists along any sequence of boxes with all
sides to infinity; Hammersley 1966, as cited by He), the right side tends to (1/mn) log rho(T_{m,n}). This is
Theorem 2.1. The direction is the correct one: the torus bounds the box from above, and the 2-lift inequality
bounds the large torus above by a power of the small one; there is no step that reverses an inequality.

## 4. Symmetry compression and sectors (He, Section 3)

G_{m,n} = V x| K_{m,n}, where K_{m,n} is the set of automorphisms phi of the group V such that phi(D) = t + D for some t
(D = {(0,0),(1,0),(0,1)}); G acts on V by (u,phi).v = u + phi(v). For m = n = 5, K = S_3 and |G| = 150
(checked by the program; the group is rebuilt from this definition in cwcheck.py and cwsec.c).

He, Proposition (label `prop: property C`, Prop. 3.1): the partition of the power set into G-orbits has property C:
"if $O_1,O_2$ are orbits and $U_1,U_2\in O_1$, then $\sum_{V\in O_2}\bra{U_1}T\ket{V}=\sum_{V\in O_2}\bra{U_2}T\ket{V}$."
Hence the compressed matrix \hat T[O1,O2] := sum over V in O2 of T[U,V] (any U in O1) is well defined.
He, Proposition (label `prop: compression preserves spectral radius`, Prop. 3.2): rho(T) = rho(\hat T).
(Proof in the paper by the intertwining T P = P \hat T and Gelfand's formula.)

Sectors. T[U,V] = 0 unless |U|+|V| = mn. For 0 <= i <= floor(mn/2) let S_i^- be the orbits of i-sets and
S_i^+ the orbits of (mn-i)-sets; X^(i) maps S_i^+ to S_i^- and Y^(i) maps S_i^- to S_i^+ (restrictions of \hat T).
He (quoted): \hat T^2 is the direct sum of X^(i)Y^(i) and Y^(i)X^(i) (i < mn/2), hence

    rho(\hat T)^2 = rho(\hat T^2) = max_{0<=i<=floor(mn/2)} rho(X^(i) Y^(i)),

using rho(XY) = rho(YX). For (5,5), mn = 25 is odd, so the sectors are i = 0..12 and the largest sector pairs
12-sets with 13-sets (X: 13-set orbits to 12-set orbits). Thus

    l3 <= (1/25) log rho(\hat T) = (1/50) max_i log rho(X^(i) Y^(i)).

Explicitly, with F = V minus the image,
  (X^(i) y)(U) = sum over injections f: U -> V with f(u)-u in D of y(orbit of V minus f(U)),   |U| = i,
  (Y^(i) x)(W) = the same with |W| = 25-i and x indexed by orbits of i-sets.
(In the leaf count each injection f is a choice of one of three forward neighbours for every u in U with all
choices distinct; its number is the permanent in the definition.) The matrices have nonnegative integer entries.

## 5. The test vector and the exact inequality

Hypothesis of Collatz-Wielandt: A = X^(i) Y^(i) is a nonnegative matrix (it is, by construction), and the test vector
x is positive. For each sector i, the shipped or generated vector x^(i) has all entries positive integers. Then

    rho(X^(i)Y^(i)) <= max_u (X^(i)Y^(i)x^(i))_u / x^(i)_u .

For sector 12 the file object/cert_he_55_converged_sector12.txt (reassembled from the three parts) lists
35070 rows "orbit_id canonical_mask x_u (T*x)_u". The checker recomputes (XYx)_u from the definition and compares
every ratio by cross multiplication (u v' > u' v in integers), so no floating point enters the decision. The
maximum is attained at orbit 53: 68004910275217693829986 / 10405826313374, whose logarithm divided by 50 is
0.4520095976 (rounded outward to six decimals: 0.452010). Sectors 0..11 give at most 0.4492950875 with the vectors in
verify-it-yourself/sectors. The final bound is the maximum over the 13 sectors.

He's iterated formula (label `prop: iterated CW`, Prop. 3.3) and corollary (label `cor: CW corollary`, Cor. 3.4),
quoted for completeness:

    Let $A$ be an $n\times n$, nonnegative matrix with positive diagonal and $x\in\R^n$ be a positive vector. For
    $q\ge 0$, define $C_q:=\max_i (A^{q+1}x)_i/(A^q x)_i$. Then $(C_q)$ is non-increasing and
    $\rho(A)=\lim C_q=\inf C_q$.

and Corollary 3.4: "$\ell_3 \le \frac{1}{mn}\log\rho(\widehat T_{m,n}) = \lim_{p\to\infty}\max_{0\le i\le\lfloor mn/2\rfloor} C_{m,n;p}^{(i)} = \inf_p \max_i C_{m,n;p}^{(i)}$".
The claim does not need the positive-diagonal hypothesis: the plain Collatz-Wielandt inequality for a positive
vector suffices, and the shipped vector is a (converged, approximate Perron) vector, not an iterate from the
all-ones vector. (The matrices do have positive diagonal, since [U] -> [V minus U] -> [U] contributes at least 1.)

## 6. What is and is not from the source

From He: Theorem 2.1, Lemmas 2.2-2.3, the 2-lift theorem (Csikvari, as quoted), Props. 3.1-3.2, the sector
decomposition. Not in the source and the author's own: the choice of a converged test vector at (5,5) (He computed
p = 2 only: his Table 2 entry for (5,5) is 0.452130, "p=2 was used to reduce the computation time", running time
about 16.5 hours) and the arithmetic of the certificate. He himself states that the sequence C_p converges to rho
(quoted above). The comparison value used by the claim is He's 0.452130 (arXiv abstract and Theorem 1.1).
Open to the panel: whether a deeper iterate of the same published inequality at the same (m,n) is a new result; the
checker verifies correctness, not novelty.

Credit, as the fetched sources show: the lower bound 0.441075... = (1/2)log(5^5/6^4)+0.001 is credited by He to
Csikvari (2016); it is not used here. The previous upper bound 0.457547 is credited by He to Lundow (2001), based on
Ciucu (1998).
