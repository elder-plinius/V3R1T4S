# Excerpt of constants/9a.md (relevant rows only; not the whole third-party page)

Source: https://raw.githubusercontent.com/teorth/optimizationproblems/main/constants/9a.md, fetched 2026-10-20T02:43:09Z, HTTP 200, whole-file sha256 92f6e1ee5d7219af29572c37dbb54192f3d12c2b1bc818aaf1c3e4ffe46d9899.

Lines copied verbatim from the file (lower-bound table rows, the comment on the larger odd cycles, and the reference lines):

| Bound | Reference | Comments |
| ----- | --------- | -------- |
| $7/2 = 3.5$ | [S1956] | Fractional clique cover bound |
| $\vartheta({\mathcal C}\_{7}) \approx 3.3177$ | [L1979] | Lovász theta-function bound |
| Bound | Reference | Comments |
| ----- | --------- | -------- |
| $343^{1/5} \approx 3.2141$ | [BMRRST1971] |
| $108^{1/4} \approx 3.2237$ | [VZ2002] |
| $350^{1/5} \approx 3.2271$ | [MO2017] |  |
| $367^{1/5} \approx 3.2578$ | [PS2018] | Independent set of size $367$ in ${\mathcal C}\_{7}^{\boxtimes 5}$ |
| $134753^{1/10} \approx 3.258020$ | [IRCR2026] | Independent set of size $134753$ in ${\mathcal C}\_{7}^{\boxtimes 10}$; constructions at https://github.com/nathanielitty/lower-bounds-for-shannon-capacity |
| $3.258789153908\ldots$ | [Gao2026] | Recursive product of the size-$367$ gadget; independent set of size $M_{40}$ in ${\mathcal C}\_{7}^{\boxtimes 200}$. Verification code: commit `b13031ba76e3` of https://github.com/xyz2606/recursive_construction_of_the_Shannon_capacity_of_C_7 |
| $3.258805369885\ldots$ | [BPZ2026] | Valid-tuple product in ${\mathcal C}\_{7}^{\boxtimes 200}$. Lean 4 formalization: commit `aa21eeb12b75` of https://github.com/spectra-research/shannon-capacity-lean |
| $3.25883262\ldots$ | [Tan2026] | Heterogeneous recursion; independent set in ${\mathcal C}\_{7}^{\boxtimes 500}$. Certificates: https://github.com/tandonravi/C7-Shannon-Capacity-Heterogeneous-Recursion |
- [BPZ2026] also records improved lower bounds for larger odd cycles (not split out as separate constants): $\Theta({\mathcal C}\_{11})\ge 5.294502522149\ldots$, $\Theta({\mathcal C}\_{13})\ge 6.302455083464\ldots$, $\Theta({\mathcal C}\_{15})\ge 7.301600534487\ldots$, $\Theta({\mathcal C}\_{19})\ge 9.357192705918\ldots$, $\Theta({\mathcal C}\_{21})\ge 10.342455853338\ldots$, $\Theta({\mathcal C}\_{23})\ge 11.328224257774\ldots$.
- [PS2018] Sven Polak, Alexander Schrijver. New lower bound on the Shannon capacity of $C\_7$ from circular graphs. Information Processing Letters, 143 (2019), 37-40. arXiv:1808.07438.
- [IRCR2026] N. Itty, C. D. Rosin, C. Carstensen, D. Reichman. Improved lower bounds for the Shannon capacity of odd cycles. 2026. [arXiv:2607.21517](https://arxiv.org/abs/2607.21517)
- [Gao2026] Y. Gao. A recursive construction improving the lower bound on the Shannon capacity of $C_7$. 2026. [arXiv:2607.27869](https://arxiv.org/abs/2607.27869)
- [BPZ2026] P. Buys, S. Polak, J. Zuiddam. Lean-verified lower bounds for the Shannon capacity of odd cycles. 2026. [arXiv:2607.29681](https://arxiv.org/abs/2607.29681)
- [Tan2026] R. Tandon. Strengthening recursive constructions for zero-error Shannon capacity. 2026. [arXiv:2608.30273](https://arxiv.org/abs/2608.30273)
