# Derivation: why the iterated Collatz-Wielandt ratios reproduce He's Table 2

Self-contained. Source: Qidong He, "A new upper bound on the dimer constant of Z^3", arXiv 2607.28810 (v2), LaTeX
source fetched 2026-10-19 (see table-record/). Quotations are copied from that source (LaTeX markup lightly
simplified). Numbers such as "Theorem 2.1" are inferred from statement order.

## 1. The inequality used, and its source

Same as in the main-win folder: He, Theorem (label `thm: bound`), quoted: "For all $m,n\ge 2$, $\ell_3\le\frac{1}{mn}\log\rho(T_{m,n})$."
and, for a computable bound, He's Corollary (label `cor: CW corollary`, Cor. 3.4 by order), quoted:

    Let $m,n\ge 2$ be integers. For $0\le i\le \floor{mn/2}$, let $\ket{\vec{1}_i}$ denote the all-ones vector in the basis
    indexed by $\cS_i^-$. For $p\ge 0$, define
    $C_{m,n;p}^{(i)}:=\frac{1}{2mn}\log\{\max_{[U]\in\cS_i^-} \frac{\bra{[U]}(X^{(i)}Y^{(i)})^{p+1}\ket{1_i}}{\bra{[U]}(X^{(i)}Y^{(i)})^{p}\ket{1_i}}\}$.
    Then $(C_{m,n;p}^{(i)})_{p\ge 0}$ is non-increasing, and
    $\ell_3 \le \frac{1}{mn}\log\rho(\widehat{T}_{m,n}) = \lim_{p\to\infty}\max_{i}C^{(i)}_{m,n;p} = \inf_{p\ge0}\max_{i}C^{(i)}_{m,n;p}$.

This relies on He's Proposition (label `prop: iterated CW`, Prop. 3.3, proved in his Appendix A from Friedland-Schneider 1980):
"Let $A$ be an $n\times n$, nonnegative matrix with positive diagonal and $x\in\R^n$ be a positive vector. For $q\ge 0$ define
$C_q:=\max_{i}(A^{q+1}x)_i/(A^q x)_i$. Then $(C_q)_{q\ge 0}$ is non-increasing, and $\rho(A)=\lim C_q=\inf_{q\ge0}C_q$."

The bound reproduced for each (m,n) is max over sectors i of C^{(i)}_{m,n;p}, rounded up to six decimals. Only
the weaker half is needed for validity: rho(A) <= C_q for every q (the plain Collatz-Wielandt inequality applied
to the positive vector A^q x, which is positive here because A has positive diagonal).

## 2. Definitions (He, Section 2; quoted)

    Let $m,n\ge 2$ be integers. Write $V_{m,n}:=\Z/m\Z\times\Z/n\Z$ ... Define the matrix $A_{m,n}$ ... by
    $\bra{\vec{u}}A_{m,n}\ket{\vec{v}} := \indicator{\set{(0,0),(1,0),(0,1)}}(\vec{v}-\vec{u})$.
    For $R,C\subseteq V_{m,n}$, write $A_{m,n}[R,C]$ for the submatrix of $A_{m,n}$ with row set $R$ and column set $C$.
    Define the matrix $T_{m,n}$, whose rows and columns are indexed by the power set of $V_{m,n}$, by
    $\bra{U}T_{m,n}\ket{V} := \per A_{m,n}[U,V_{m,n}\setminus V]$ if $|U|+|V|=mn$, and $0$ otherwise,
    where $\per$ denotes the permanent, with the convention that the permanent of the empty matrix is $1$.
    Let $\rho(T_{m,n})$ be the spectral radius of $T_{m,n}$.

In words: a state is a subset of the layer V = Z/m x Z/n (mn vertices; for the (5,5) entry, 25). T[U,W] is the number of ways to match every
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

## 5. Hypotheses and the matrices used

A = X^(i) Y^(i) is a nonnegative integer matrix with positive diagonal: for every i-set U,
<[U]|XY|[U]> >= <[U]|X|[V minus U]> <[V minus U]|Y|[U]> >= 1 (He's proof of Cor. 3.4; the injection u -> u is
allowed since (0,0) is in D, and it maps U onto U whose complement orbit is V minus U). The start vector is the
all-ones vector (positive). The checker (cwcheck.py iter) builds X, Y from the definition, iterates v_{p+1} = XY v_p
in exact integers, picks the row maximising v_{p+1}/v_p by cross multiplication, and computes the logarithm only
afterwards with 80-digit decimal arithmetic to round upward to six places.

For (5,5) at p = 2 the same computation is done by the compiled checker cwsec.c (u128 integers with overflow
detection); in pure Python, (5,5) sector 12 is feasible only for one multiplication (see RECEIPTS.md), so (5,5) p = 2 uses
the C program for all 13 sectors.

## 6. What is and is not from the source

The whole table is He's method; the claim is reproduction only (p1 asks for exactly that). He's Table 2 entries are
rounded upward to six decimals: 
    \begin{tabular}{ccccc} m / n & 2 & 3 & 4 & 5 ;  m=2: 0.486478 ;  m=3: 0.471408, 0.458558 ;
    m=4: 0.465970, 0.457380, 0.454673 ; m=5: 0.463401, 0.454663, 0.453365, 0.452130 ; m=6: 0.462010, 0.454618 \end{tabular}
    "Upper bounds on $\ell_3$ obtained from Corollary~\ref{cor: CW corollary}. ... Every entry is rounded upward to six decimal places."
    (He, Section 4: "All bounds were obtained from a Java implementation of Corollary 3.4, using $p=4$ except for
    $(m,n)=(5,5)$, for which $p=2$ was used to reduce the computation time. All vector updates used arbitrary-precision
    integer arithmetic, and ratios were compared by exact cross multiplication.")
