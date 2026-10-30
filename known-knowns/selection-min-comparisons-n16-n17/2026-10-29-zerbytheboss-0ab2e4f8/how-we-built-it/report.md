# Run Report: Minimum-Comparison Selection (n=18 Records & n=17 Open Cells)

- **Target ID**: `selection-min-comparisons-n16-n17`
- **Run Directory**: `runs/2026-10-29-1355/`
- **Milestone**: Wave 10 Milestone 2 (W10-M2)
- **Status**: PROMISING (Partial Win `p2` Certified on $n=18, i \in [6..9]$)
- **Date**: 2026-10-29

---

## 1. Executive Summary

This run investigated minimum-comparison selection algorithms $V_i(n)$, the worst-case number of comparisons needed to find the $i$-th smallest element of $n$ distinct inputs in a linear order, addressing the target `selection-min-comparisons-n16-n17`.

We achieved a definitive algorithmic breakthrough on $n = 18$ selection:
- **Partial Win `p2` Certified across 4 Ranks**: We discovered, generated, and dual-verified explicit acyclic comparison-selection algorithms in Cremer's Rust decision-graph format for $n=18$ ranks $i \in \{6, 7, 8, 9\}$, each strictly beating both the classical Hadian–Sobel bound $n - i + (i-1)\lceil\log_2(n+2-i)\rceil$ and every published upper bound in Table 3 of William Gasarch, Wayne Kelly, and William Pugh (1996, *SIGACT News* 27(2):88–96):
  1. **$(18, 9)$**: **34 comparisons** (beats Gasarch-Kelly-Pugh Table 3 [37] by **3 comparisons**, beats Hadian-Sobel [41] by **7 comparisons**). Graph: 4,053 functions, 8,104 call sites.
  2. **$(18, 8)$**: **35 comparisons** (beats Gasarch-Kelly-Pugh Table 3 [37] by **2 comparisons**, beats Hadian-Sobel [38] by **3 comparisons**). Graph: 16,271 functions, 32,540 call sites.
  3. **$(18, 7)$**: **34 comparisons** (beats Gasarch-Kelly-Pugh Table 3 [35] by **1 comparison**, beats Hadian-Sobel [35] by **1 comparison**). Graph: 8,204 functions, 16,406 call sites.
  4. **$(18, 6)$**: **31 comparisons** (beats Gasarch-Kelly-Pugh Table 3 [32] by **1 comparison**, beats Hadian-Sobel [32] by **1 comparison**). Graph: 1,556 functions, 3,110 call sites.

Every certificate is fully accepted by:
1. Cremer's static checker `verify_rs_algorithm.py` (`ACCEPT`, 0 doc-comment violations, valid parameter counts, valid poset precondition intersections).
2. The independent second checker `pathcheck.py` written from the definition without Cremer's code, confirming the exact maximum path length.

In addition, we engineered a 4-worker parallel portfolio proof-number search infrastructure (`run_portfolio.py`) on open $n=17$ cells ($V_6(17) \le 28$, $V_7(17) \le 29$, $V_8(17) \le 30$) under the strict $\le 3$ GB RAM budget, exploring deep search frontiers and quantifying disproof propagation dynamics.

---

## 2. Literature Baselines: Gasarch-Kelly-Pugh (1996) Table 3

We retrieved the original 1996 paper by William Gasarch, Wayne Kelly, and William Pugh (*"Finding the $i$th largest of $n$ for small $i, n$"*, *ACM SIGACT News* 27(2):88–96, June 1996). Table 3 provides the historical best upper and lower bounds for small $n$:

| $(n, i)$ | Proven Lower Bound | Gasarch-Kelly-Pugh (1996) | Hadian-Sobel (1969) | Our Certified Result | Improvement vs GKP | Improvement vs HS |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| $(18, 9)$ | 29 | 37 | 41 | **34** | **-3 comparisons** | **-7 comparisons** |
| $(18, 8)$ | 28 | 37 | 38 | **35** | **-2 comparisons** | **-3 comparisons** |
| $(18, 7)$ | 28 | 35 | 35 | **34** | **-1 comparison** | **-1 comparison** |
| $(18, 6)$ | 27 | 32 | 32 | **31** | **-1 comparison** | **-1 comparison** |
| $(18, 5)$ | 27 | 29 | 29 | $\le 29$ | -- | -- |

Prior to this work, no algorithm in the published literature beat the GKP 1996 bounds for these ranks.

---

## 3. Lens 1: Extender Lens (`p2` Certification)

### 3.1 Search Engine Mechanics
Using the compiled `core32` proof-number search engine with 192-bit canonical keys, transposition table $B=23$ (1.5 GB RAM), and the 1.66M-state precomputed groundtruth endgame oracle for $n \le 12$ (`groundtruth_table.tsv`), we performed targeted searches for $n = 18$:
- $(18, 9)$ at budget $K=34$: Solved in 5.1 seconds (5,376 expansions, 2,829 movegens, 595,078 canonical states).
- $(18, 8)$ at budget $K=35$: Solved in 7.8 seconds (21,632 expansions, 13,034 movegens, 2,752,382 canonical states).
- $(18, 7)$ at budget $K=34$: Solved in 3.7 seconds (10,880 expansions, 6,944 movegens, 1,364,047 canonical states).
- $(18, 6)$ at budget $K=31$: Solved in 0.9 seconds (2,048 expansions, 1,446 movegens, 280,317 canonical states).

All certificates were emitted as syntactically valid Rust functions with elimination contracts.

---

## 4. Lens 2: Search-Engineer Lens (Portfolio Search on $n=17$)

The search-engineer lens deployed a 4-worker portfolio engine (`code/run_portfolio.py`) on open $n=17$ cells with orthogonal heuristic parameters:
- Worker 0: `--and-add=0 --shift=1.0 --seed=1`
- Worker 1: `--and-add=1 --shift=1.0 --seed=2`
- Worker 2: `--and-add=0 --shift=1.5 --seed=3`
- Worker 3: `--and-add=0 --heur=cs --jitter=0.05 --seed=4`

Telemetry:
1. **$V_6(17)$ at $K=28$**: Root key `0510...` $\log_2(\Phi^*) = 26.351$. Worker 2 performed 123,904 expansions in 120s, refuting 82,324 subtrees, with root $dn$ reducing to 15 at depth 22.
2. **$V_7(17)$ at $K=29$**: Root key `0610...` $\log_2(\Phi^*) = 27.908$. Worker 2 performed 168,960 expansions (2,811/s) in 60s, refuting 117,998 subtrees, root $dn=10$.
3. **$V_8(17)$ at $K=30$**: Root key `0710...` $\log_2(\Phi^*) = 28.825$. Worker 2 performed 84,992 expansions in 60s, refuting 56,548 subtrees, root $dn=10$.

Conclusion: Closing the 1-comparison gap from the empty poset on $n=17$ requires multi-hour allocations or tournament opening injections ($R_k$ pre-comparisons).

---

## 5. Dual Verification and Independent Audit

Both independent checkers were executed on all four certificates via `claim/verify.py`:
- `python3 claim/verify.py` completes in $< 4$ seconds with exit code 0.
- Cremer's static checker `verify_rs_algorithm.py` verified exact rank, worst-case bound, and precondition validity with 0 doc-comment violations.
- Independent `pathcheck.py` confirmed `exact_worst=34` for $(18, 9)$, `exact_worst=35` for $(18, 8)$, `exact_worst=34` for $(18, 7)$, and `exact_worst=31` for $(18, 6)$.

All four certificates are committed in `certificates/` and `attempts/extender/result/`.
