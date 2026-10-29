# Stage 1 Preregistration — `moore-graph-57` (`p2`)

> **Dated Scope Note (`2026-10-29`):** Per `@elder-plinius`'s review on PR `#770`, this standalone package extracts strictly the **Partial Win `p2`** exact computational verification of `arXiv:2606.29183v2` (`object/certificate.json`, `sha256: d13344783df1b7cf33f19e9b3408bad1bbe96939c5e087b02460113f03dc9c07`), with all unformalized `p1` written group-action arguments removed.

target: moore-graph-57
category: graphs-games-automata
kind: moonshot
direction: exact_verification_of_no_involutions_theorem
null_test: not needed because exact deterministic integer/rational and finite-field linear algebra verification has zero stochastic variance
frozen_utc: 2026-10-26T03:31:15Z

## 1. Preregistered Metadata & Win Thresholds
- **Target ID:** `moore-graph-57` (*"The missing Moore graph (degree 57, diameter 2)"*)
- **Category:** `graphs-games-automata` | **Kind:** `moonshot` | **Tractability:** `1`
- **Primary Source Verified:** Yawara Ishida, *"No involutions in the missing Moore graph"*, `arXiv:2606.29183v2` (8 July 2026).
- **Preregistered Success Rule (`p2`):**
  - **Partial Win `p2` (`CONFIRMED_PARTIAL`):** An independent, 100% reproducible exact-computation verification (exact rational/integer linear algebra and finite-field $\mathbb{F}_p$ Gaussian elimination in Python standard library) of the `arXiv:2606.29183v2` theorem that a Moore graph of degree 57 ($\mathrm{srg}(3250, 57, 0, 1)$) has no involutory automorphisms (Theorem 1.1 & Corollary 6.1), together with the Brauer trace–rank identity on existing diameter-2 Moore graphs ($C_5$, Petersen, Hoffman–Singleton), all odd-prime restrictions of Theorem 1.2 ($p \in \{7, 11, 13, 19\}$), and the five auxiliary strongly regular graph families in Section 8 Table 1 of `arXiv:2606.29183v2`.

## 2. Verification & Exact Arithmetic Protocol
- All matrix identities, spectral idempotent projections $E_{57}, E_7, E_{-8}$ ($m_7 = 1729, m_{-8} = 1520$), $p$-adic denominator checks, $\mathbb{F}_p$-ranks, and fixed-point subgraph equations are verified in exact arbitrary-precision integer and rational arithmetic (`int`, `fractions.Fraction`, and exact modular row reduction over $\mathbb{F}_p$), with zero floating-point approximations.
