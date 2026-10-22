# How We Found It (`ghr-sum-difference-c3a`, Partial Win `p1`)

_Contributor text, unverified._

1. **Diagnosing the Finite-vs-Limit Gap in [K2026b]:**
   In [K2026b] (`kleinwaks/masked-digit-sum-difference-bound`), the asymptotic limit lower bound `1.19519192*` uses a controlled-carry construction in even base $q = 27,022$ with $B = 26,972$ and an asymptotic carryover word-grouping argument (`Filter.Tendsto` as $N \to \infty$), whereas the explicit finite-depth ($N = 10^{13}$) certificate falls back to the **uncontrolled-carry** base $Q = 2B + 1 = 34,065$ with generators $G = \{1518, 1524, 1587, 2024, 2032, 2116\} = \{3, 4\} \times \{506, 508, 529\}$ and $B = 17,032$, giving `1.19102809`.

2. **Residue-Bijective Mod-$q$ Difference Pruning at Finite Depth:**
   In Kleinwaks's Lean 4 formalization (`CoreConstruction.lean`, theorem `residue_word_injective`), injectivity of base-$q$ evaluation $(d_0, \dots, d_{N-1}) \mapsto \sum_{i=0}^{N-1} d_i q^i$ holds for **any** odd base $q \in [B + 1, 2B + 1]$ and any symmetric pruned difference alphabet $\widetilde{D} = \{0\} \cup \{\pm d : d \in \widetilde{D}_+\} \subseteq M - M$ whose elements have pairwise distinct residues modulo $q$.
   Partitioning the non-zero residues $\{1, \dots, q - 1\} \pmod{q}$ into $(q - 1)/2$ complementary pairs $\{r, q - r\}$ and retaining the cheaper difference $d(r) \in \{r, q - r\}$ (`\kappa(r)` vs `\kappa(q - r)`) guarantees that $\{+d(r) \bmod q, -d(r) \bmod q\} = \{r, q - r\}$ are disjoint across all $1 \le r \le (q - 1)/2$.
   Furthermore, doubling $U \mapsto V = 2U$ leaves $|V - V| = |U - U|$ and $|V + V| = |U + U|$ invariant while guaranteeing $|V - V| \le 2\max U + 1 < 4\max U + 1 = 2\max V + 1 < 5 q^N$.

3. **Complete Residue System at $(B, q) = (17086, 27995)$:**
   Sweeping odd bases $q$ and mask cutoffs $B$ over $H = \operatorname{span}_{\mathbb{N}_0}(G)$ revealed that at $B = 17,086$ (`|M| = 3,153`, `|S| = 18,835`) and odd base $q = 27,995$, **all $(q - 1)/2 = 13,997$ non-zero residue pairs are realized**, so $|\widetilde{D}| = 27,995 = q$ is a complete residue system modulo $27,995$. At $N = 10^{13}$ and $x_f = 0.9996683050229444$, all $13,997$ floor counts are exact in $2^{-128}$ fixed-point arithmetic (`cfFloorOK == True`), certifying $C_{3a}(V) > 1.19230254070568368329 > 1.19230254$ (`+0.00127445` over `1.19102809`).
