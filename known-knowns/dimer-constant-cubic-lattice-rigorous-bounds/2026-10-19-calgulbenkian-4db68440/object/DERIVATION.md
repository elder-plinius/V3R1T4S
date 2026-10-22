# Derivation: an upper bound on the 3D monomer-dimer entropy h3 from the monomer-dimer diagonal layer

STATUS: THE EXTENSION OF HE'S ARGUMENT TO MONOMER-DIMER (ALL MATCHINGS) USED HERE IS THE AUTHOR'S OWN. IT IS NOT
PUBLISHED. He's paper (arXiv 2607.28810) has no monomer-dimer theorem. Argon cited it as "He's Theorem 2.4";
the statement at that number is Csikvari's 2-lift inequality (quoted below), valid for all t >= 0, which is
what makes the extension short, but the extension itself (transfer matrix, trace identity, box in torus, limit) is
written out here for the first time, by the triage agent's re-derivation and the author's notes.

OPEN QUESTION 1 for the panel: is this extension proved? The steps to scrutinise are marked (E1)-(E5) below.

## 1. Definitions of the quantity and the comparator (from the fetched sources)

Friedland, Krop, Lundow, Markstrom (arXiv math/0603001), source fetched 2026-10-19, quoted:

    Let $\psi(x,G):=\sum_{l=0}^{\infty}\phi(l,G) x^l$ denote the matching generating polynomial of $G$.
    ... Let $h_d(p):=h_{G(\Z^d)}(p)$ for any $p\in [0,1]$ and $h_d:=\sup_{p\in[0,1]} h_d(p)$.
    ($h_d$ and $\tilde h_d:=h_d(1)$ are called the $d$-monomer-dimer entropy and the $d$-dimer entropy respectively.)

Here phi(l,G) is the number of matchings with l dimers (the text "monomer-dimer covers"), and for boxes
G(m) of Z^d (their equation boxdefhdp), quoted:

    Then for any sequence $l_n\in [0,\frac{\vol(\m_n)}{2}]\cap\N$ the following conditions hold:
    $\lim_{n\to\infty} \frac{\log\phi(l_n,G(\m_n))}{\vol(\m_n)}=h_d(p)$ if $\m_n\to\infty$ and
    $\lim_{n\to\infty} \frac{2l_n}{\vol(\m_n)}=p\in[0,1]$.

The comparator, quoted from the same paper's introduction: "The numerical computations in [FP] yield the best known
upper bound $h_3\le 0.7862023450$." ([FP] = Friedland and Peled, arXiv math/0402009, which we did not read; the
credit for 0.7862023450 is as FKLM state it.) FKLM also state the lower bound h_3 >= 0.7849602275; it is not used.

## 2. The inequality to be proved

(E0) For all m,n >= 2:  h3 <= (1/(mn)) log rho(T^MD_{m,n}),  where T^MD is defined in section 3.

Consequence used by the claim: h3 <= (1/20) log max_U (T^MD x)_U / x_U for any positive vector x, at (m,n) = (5,4)
(Collatz-Wielandt: Horn and Johnson, Matrix Analysis, Thm 8.1.26, for a nonnegative matrix and a positive vector).

## 3. The matrix (the monomer-dimer analogue of He's definition)

Same layer V = Z/m x Z/n, D = {(0,0),(1,0),(0,1)}, A as in He (quoted below). States are subsets of V: U is the
set of vertices of a layer already matched by a dimer coming from the layer below. Define, with per as in He,

    T^MD[U,W] := sum over S subset of (V minus U) of per A[S, W]      (per A[S,W] = 0 unless |S| = |W|),

i.e. the vertices of the layer outside U are each either a monomer or matched upward (the set S), and W is the set of
vertices of the next layer hit by those dimers. The full matrix has 2^{mn} rows; at (5,4) it has 1048576 rows and the
checker applies it entirely (no symmetry reduction is needed for validity).

He's definitions of V, D, A (He, Section 2; quoted)

    Let $m,n\ge 2$ be integers. Write $V_{m,n}:=\Z/m\Z\times\Z/n\Z$ ... Define the matrix $A_{m,n}$ ... by
    $\bra{\vec{u}}A_{m,n}\ket{\vec{v}} := \indicator{\set{(0,0),(1,0),(0,1)}}(\vec{v}-\vec{u})$.
    For $R,C\subseteq V_{m,n}$, write $A_{m,n}[R,C]$ for the submatrix of $A_{m,n}$ with row set $R$ and column set $C$.
    Define the matrix $T_{m,n}$, whose rows and columns are indexed by the power set of $V_{m,n}$, by
    $\bra{U}T_{m,n}\ket{V} := \per A_{m,n}[U,V_{m,n}\setminus V]$ if $|U|+|V|=mn$, and $0$ otherwise,
    where $\per$ denotes the permanent, with the convention that the permanent of the empty matrix is $1$.
    Let $\rho(T_{m,n})$ be the spectral radius of $T_{m,n}$.


## 4. The proof of (E0), step by step

(E1) Trace identity. Let T_{m,n,l} = Z^3 / span(m(e1-e3), n(e2-e3), l e3) be He's quotient graph (simple, 6-regular,
bipartite for m,n >= 2 and even l >= 4; He, quoted in the main-win folder's DERIVATION). Under He's isomorphism
[x] -> ((x1 mod m, x2 mod n), x1+x2+x3 mod l) every edge joins height k to height k+1 with biadjacency A. A matching
of T_{m,n,l} (not necessarily perfect) determines, for every height k, the set U_k of vertices of layer k matched to
the layer below (k-1); the set S_k of vertices of layer k matched upward is disjoint from U_k, and the vertices of
layer k+1 hit are W = U_{k+1}. The number of matchings between layers k and k+1 for given (U_k, U_{k+1}) is
sum_S per A[S, U_{k+1}] over S subset of V minus U_k, which is T^MD[U_k, U_{k+1}]. The matching is the cyclic
sequence (U_k), so  #matchings(T_{m,n,l}) = tr((T^MD)^l).  This is He's Lemma 2.2 with the all-ones weight on
monomers. Checked by computer: cwcheck.py trace builds the quotient graph by a triangular reduction (independent of
the isomorphism) and counts all matchings by brute force: 306305, 162589284, 162465104 for (2,2,4), (3,2,4), (2,2,6)
and 1880275257729 for the 4D (2,2,2,4); each equals the trace.

(E2) Two-lift inequality at t = 1. Csikvari's theorem as quoted by He (label `thm: 2-lift`, Theorem 2.4 by order;
Csikvari, J. Eur. Math. Soc. 2017, Lemma 4.2, not fetched by us), quoted:

    If $G$ is a bipartite graph and $H$ is a $2$-lift of $G$, then, for all $t\ge 0$, $M(H,t)\le M(G,t)^2$,

with M(G,t) = sum_{k} m_k(G) t^k, m_k the number of matchings with k edges. Taking t = 1 gives
(total number of matchings of H) <= (total number of matchings of G)^2. No limit t -> infinity is taken. The
graphs T_{m,n,l} are bipartite (He) and T_{2m,n,l}, T_{m,2n,l}, T_{m,n,2l} are 2-lifts of T_{m,n,l} (He's lemma,
quoted in the main-win DERIVATION). Hypotheses are therefore the same as for the dimer case.

(E3) Box inside the torus. Let Phi(G) be the number of all matchings of G. If G' is a spanning subgraph of G then every
matching of G' is a matching of G, so Phi(G') <= Phi(G). The box with sides (2^p m, 2^p n, 2^p) is a spanning subgraph
of the rectangular torus Z^3/span(2^p m e1, 2^p n e2, 2^p e3) = T_{2^p m,2^p n,2^p} (p >= 2; the lattice equals He's
Lambda_{2^p m,2^p n,2^p}). Hence Phi(box) <= Phi(T_{2^p m,2^p n,2^p}) <= Phi(T_{m,n,2^p})^{2^{2p}} by (E2) applied 2p times
(l = 2^p >= 4 even at every step), and Phi(T_{m,n,2^p}) = tr(T^MD^{2^p}) <= 2^{mn} rho(T^MD)^{2^p}.

(E4) From the box to h3. With vol = 2^{3p} m n, (1/vol) log Phi(box) <= (1/(2^p mn)) log(2^{mn} rho^{2^p}) =
(mn)^{-1} log rho + (log 2)/2^p. By FKLM's box limit (quoted in section 1), for every density p0 and l_n with
2 l_n/vol -> p0, (1/vol) log phi(l_n, box_n) -> h3(p0). Since Phi >= phi(l_n, .), liminf_p (1/vol) log Phi(box_p) >=
h3(p0) for every p0, hence >= sup_{p0} h3(p0) = h3. (Boxes with sides 2^p m, 2^p n, 2^p, all tending to infinity,
satisfy FKLM's m_n -> infinity requirement.)

(E5) Conclusion. h3 <= liminf_p [ (mn)^{-1} log rho + (log 2)/2^p ] = (mn)^{-1} log rho(T^MD_{m,n}). QED (E0).

The steps that are not in He's paper: the definition of T^MD and the trace identity (E1), the use of the theorem at
t = 1 (E2), and the comparison of Phi with the entropy of FKLM (E4). (E3) is He's argument verbatim for a different
count. There is no symmetry compression in the verification: the checker applies the entire 1048576 x 1048576 matrix (never stored, applied row by row through a dynamic program) and
expands the shipped vector (given on the 52488 orbits of the 20 translations of Z/5 x Z/4; the swap is not a symmetry as 5 differs from 4) to all 1048576 states, so the
validity of the bound does not depend on any symmetry claim.

## 5. The exact inequality checked

For the shipped positive integer vector x (52488 orbit values, expanded to 1048576 states) the checker computes
(T^MD x)_U for every state U and the maximum of (T^MD x)_U / x_U by cross multiplication. Result:
1891821269973664 / 281869529 (= 6711691.315784843...), whose logarithm divided by 20 is 0.785968076808533...
(rounded outward: 0.785968076809 at 12 places; the claimed bound is h3 <= 0.7859681 at 7 places). Collatz-Wielandt
hypotheses: T^MD is nonnegative (integer entries) and x is positive. The value is smaller than FKLM's comparator
0.7862023450 by 2.34e-4.

## 6. Provenance of the idea

The monomer-dimer transfer layer and t = 1 application are the author's (Argon's) extension; the triage agent
rederived them independently (trace identity checked by brute force; ratio recomputed on the full matrix). Nothing in
the fetched sources states this bound.
