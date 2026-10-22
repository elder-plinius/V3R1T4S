# How we found it (contributor text, unverified)

- **The brief.** No rigorous lower bound for square-lattice site percolation had beaten 0.556 since 1996. The
  1996 proof (van den Berg and Ermakov) rests on a finite stochastic-domination check in a small conditioning
  window. We wanted to know whether that window was set by 1990s hardware.
- **Step 1, reproduction.** We reproduced the paper exactly, in rational arithmetic: all 13 rows of its table, and
  the method's exact optimum 0.5560829. Checking every per-history inequality instead of the paper's envelope gained
  nothing, as the paper's own Remark (ii) says.
- **What worked.** The history of the growth process lives on a tree, so the posterior of the vertex being expanded
  can be computed exactly by belief propagation. The domination condition is multilinear in the incoming messages,
  so only the extreme rays of the message cones matter. Those cones are 2D, so their hulls are exact and small, and
  outward rounding to a 2^-40 grid keeps the numbers small while staying sound. The bound rises to 0.556677 at depth
  1, 0.556770 at depth 2 and 0.556785 at depth 3. We froze p = 4433/10000 at depth 3, which gives 0.5567.
- **Checks before the panel.** A fresh-context reviewer re-implemented the check without our code and enumerated
  real growth-process histories exactly. Its corrections to the write-up were applied.
- **What failed, or is capped:**
  - **Deeper windows** saturate at 0.556788. That is the limit of this relaxation, which ignores geometry.
  - **Two-step domination** gains nothing under the site-by-site coupling, because the children's single-step
    condition is forced.
  - **The Hammersley/Simon-Lieb finite-size criterion** would need an exact box of half-width about 60 at
    p = 0.557. An exact transfer matrix reaches about 10.
- **Live leads.** Restricting to realizable histories (real ones sit about 5 times above the cone's worst margin),
  and other comparison lattices inside S* (the two-layer lattice caps the method near 1 - p_c(L), about 0.576).
- **Who.** A human contributor (Kaust-a-laut) proposed the directions, including the larger conditioning windows,
  and steered every decision. Claude Code (claude-opus-5-5) wrote the code and the proof under the V3R1T4S kit's
  rules: preregistration, then a three-skeptic panel in fresh contexts.
