# How we found it (contributor text, unverified)

*Note: contributor text, unverified.*

## Brief & prior obstacle

Whether the rank-$3$ elliptic quadric $Q^-(7,3) = \Omega^-(8,3)$ ($1{,}066$ singular points, $22{,}960$ totally singular planes) admits a spread of $82$ pairwise-disjoint planes is a classic open question in Galois geometry; Kiermaier, Schmidt, and Wassermann (`arXiv:2403.11188v3`, Oct 2025) narrowed any spread automorphism's prime-power order divisors to $\{2, 3\}$. Prior exploratory work solved $4$ of the $5$ order-$3$ conjugacy classes quickly with MILP/DLX, but stalled on two obstacles:
1. Random group sampling could not certify $100\%$ conjugacy-class completeness across tiny unipotent classes in $\mathrm{PGO}^-(8,3)$.
2. Raw Dancing Links on the remaining viable order-$3$ class `C3_13` ($364 \times 6{,}598$ Kramer-Mesner exact cover, where every non-fixed row has uniform degree $243$) blew up past tens of millions of nodes without closing even a single root branch.

## What worked

1. **Cayley skew-form bijection for constructive completeness**: Because $(A - I)^3 = 0$ in characteristic $3$ makes $A + I = -(I - (A - I))$ invertible everywhere on order-$3$ elements, Cayley's map $S = G(A - I)(A + I)^{-1}$ gave an exact bijection with skew-symmetric $8 \times 8$ matrices of even rank $d \in \{2, 4\}$ satisfying $X(U) \subseteq \operatorname{rad}_B(U)$ ($U = \operatorname{im}(G^{-1}S)$, $\dim \operatorname{rad}_B(U) \ge d/2$). That decomposed all $430{,}408{,}160$ order-$3$ elements into four explicit geometric strata and allowed exact centralizer and BFS orbit enumeration with zero random sampling.
2. **Fixed-plane geometry + $1{,}889{,}568$-element normalizer staged reduction on `C3_13`**: Inspecting the $37$ fixed planes of `C3_13` showed that one is $\Pi_*$ ($13$ fixed points) while all $36$ others meet $\Pi_* \cong \mathrm{PG}(2,3)$ in $4$-point lines, forcing $\Pi_* \in \mathcal{S}$. Enumerating the full normalizer $N_{\mathrm{PGO}^-(8,3)}(\langle A \rangle)$ of order $1{,}889{,}568$ in `0.3s` revealed that $N$ acts **transitively** on all $6{,}561$ disjoint plane $3$-orbits, and that $\mathrm{Stab}_N(O_0)$ ($288$ elements) has an uncovered point-orbit $r_1$ of size $2$, collapsing Depth $1$ from $144$ branches to $4$ canonical branches. Ordering those $4$ branches by largest pair-stabilizer and eliminating each proved-`UNSAT` $N$-orbit of pairs shrank the entire `C3_13` search to `8.8M` branching nodes (`15.6s` in our 64-bit SWAR solver and `52.3s` in our independent Row-Elimination DLX verifier).
3. **Self-contained extension to $\mathrm{PO}^-(8,3)$ and odd primes**: Checking the unique Sylow-$p$ classes for $p \in \{5, 7, 13, 41\}$ and all $5$ orthogonal involution classes in $\mathrm{PO}^-(8,3)$ proved from first principles that $\mathrm{Aut}(\mathcal{S}) \cap \mathrm{PO}^-(8,3) = \{1\}$, leaving only $|\mathrm{Aut}(\mathcal{S})| \in \{1, 2\}$.
