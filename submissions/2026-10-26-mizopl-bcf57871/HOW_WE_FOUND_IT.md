# How We Found It (`conway-99-graph`, Tracks `p2` and `p1`)

*Note: contributor text, unverified (for the machine-verified claims and proof certificates, see `object/certificate.json`, `object/proofs/`, and `verify-it-yourself/verify.py`).*

## Methodology
1. **Anchoring the Forced-Structure Reduction at a Fixed Vertex $x$:**
   In Section 2.3 of `arXiv:2608.11211`, Thakkar & Severini showed that fixing a root vertex $x \in V(\Gamma)$ of a hypothetical $\Gamma = \mathrm{srg}(99, 14, 1, 2)$ identifies the $84$ vertices of $\Gamma_2(x)$ with the $84$ non-matched pairs $P_u \in \binom{\Gamma_1(x)}{2} \setminus M_x$ and reduces the SRG conditions to inner-outer degree balance (`Constraint 4`) and outer pair common-neighbor counts (`Constraints 2 & 3`). However, in Section 2.4 of `arXiv:2608.11211`, their symmetry experiments switched to generic block-circulant matrices without anchoring at a fixed vertex $x$.
2. **Equivariant Orbit Quotient on $\Gamma_2(x)$:**
   Whenever a prime-order automorphism $g \in \mathrm{Aut}(\Gamma)$ ($p \in \{2, 3, 7\}$) fixes at least one vertex $x$, it preserves $\Gamma_1(x)$ and its unique perfect matching $M_x$ of $7$ edges, inducing a canonical permutation $g(P_u) = \{g(a), g(b)\}$ on the $84$ outer vertices $\Gamma_2(x)$. Identifying each unordered outer pair $\{u, v\}$ with its canonical $G$-orbit representative compresses the $\binom{84}{2} = 3,486$ outer edge variables directly inside the forced-structure reduction.
3. **Pure-RUP Proof Generation Across Dual SAT Encodings:**
   By encoding all cardinality constraints $\sum L_i = k$ independently in both Sinz's (2005) linear sequential counter (Encoding A) and Bailleux & Boufkhad's (2003) binary tree unary totalizer (Encoding B), and running `kissat` with RAT-producing inprocessing disabled (`--eliminate=0 --substitute=0 --sweep=0 --congruence=0 --factor=0`) followed by `drat-trim -L`, every UNSAT proof across both Track `p2` and Track `p1` was emitted with **zero RAT lemmas** (100% pure Reverse Unit Propagation), enabling fast, zero-dependency verification in pure Python.
