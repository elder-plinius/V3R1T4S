# Stage 1 Preregistration — `moore-graph-57`

target: moore-graph-57
category: graphs-games-automata
kind: moonshot
direction: existence_or_automorphism_exclusion
null_test: not needed because exact deterministic integer/rational and finite-field linear algebra verification has zero stochastic variance
frozen_utc: 2026-10-26T03:31:15Z

## 1. Preregistered Metadata & Win Thresholds
- **Target ID:** `moore-graph-57` (*"The missing Moore graph (degree 57, diameter 2)"*)
- **Category:** `graphs-games-automata` | **Kind:** `moonshot` | **Tractability:** `1`
- **Primary Sources:** Yawara Ishida, *"No involutions in the missing Moore graph"*, `arXiv:2606.29183v2` (8 July 2026); A. A. Makhnev & D. V. Paduchikh, *"On the automorphism group of the Aschbacher graph"*, *Proc. Steklov Inst. Math.* 267 (2009), Suppl. 1, S149–S163 (*Trudy Inst. Mat. i Mekh. UrO RAN* 15(2), 162–176); M. Mačaj & J. Širáň, *"Search for properties of the missing Moore graph"*, *Linear Algebra Appl.* 432 (2010), 2381–2398; K. Kováčiková, *"Induced subgraphs in strongly regular graphs"*, PhD Thesis, Comenius University (2015), `arXiv:1812.05353`.
- **Preregistered Success Rules:**
  1. **Partial Win `p2` (`CONFIRMED_PARTIAL`):** An independent, 100% reproducible exact-computation verification (exact rational/integer linear algebra, finite-field $\mathbb{F}_p$ rank, $p$-adic Smith normal form / Brauer quotient verification, and orbit-partition verification in Python + `sympy`) of the `arXiv:2606.29183` theorem that a Moore graph of degree 57 ($\mathrm{srg}(3250, 57, 0, 1)$) has no involutory automorphisms, together with all odd-prime restrictions of Theorem 1.2 ($p \in \{7, 11, 13, 19\}$) and the five auxiliary strongly regular graph families in Section 8 of `arXiv:2606.29183`.
  2. **Partial Win `p1` (`CONFIRMED_PARTIAL`):** A computer-verified exclusion (reproducible code, exact integer/rational arithmetic) of specific automorphism-group orders and composite/prime-power automorphism structures for $\mathrm{srg}(3250, 57, 0, 1)$ that are not already excluded in `arXiv:2606.29183` and its references, explicitly separating:
     - **Unconditional exclusions** (independent of `arXiv:2606.29183`, using only classical character integrality, fixed-point theorems, Hoffman–Singleton induced subgraph census, and exact orbit-matrix / double-counting equations), and
     - **Conditional exclusions building on `arXiv:2606.29183` (unrefereed)** (combining the exact displacement counts $a_1(x)$ of `arXiv:2606.29183` Theorem 1.1 & Theorem 1.2 with the odd-order structure theorems of Makhnev–Paduchikh 2009 and Mačaj–Širáň 2010).

## 2. Verification & Exact Arithmetic Protocol
- All matrix identities, spectral idempotent projections $E_{57}, E_7, E_{-8}$, $p$-adic valuation checks, $\mathbb{F}_p$-ranks, character trace formulas, induced subgraph linear systems, and orbit-matrix equations are verified in exact arbitrary-precision integer and rational arithmetic (`int`, `fractions.Fraction`, `sympy.Matrix`), with zero floating-point approximations.
