# PREREG (frozen 2026-10-18T21:50:01Z, before any block computation of this run)

Criterion (target.md, verbatim): A rigorous proof that p_c^site(Z^3) <= p* for an explicit rational p* < 1/2,
strictly below every explicit rigorous upper bound published at verification time, whose finite part is an
exhaustive computation in exact rational (or verified interval) arithmetic released with code a stranger can rerun.

Method fixed now (the proof skeleton; the block design is what the attack searches):
- Tile Z^3 (or a slab of it) by disjoint translates of a finite block B; the coarse graph is Z^3 (box tiling) or the
  triangular lattice T (running-bond bricks in a slab). Each block state eps in {0,1}^B has a designated connected
  set of open sites G(eps), a deterministic function of eps (and possibly of the entry direction). eta(v, w) = 1
  iff G(v) and G(w) are nonempty and some site of G(v) is Z^3-adjacent to some site of G(w).
- Growth process and coupling exactly as in the square-site proof (explore/square-site-lower/PROOF.md, Lemma 1 with
  the die-out/survival split; Lemma 2 tree information, which uses only that children are unexplored).
- Comparison: coarse Z^3 at q >= 1/2 (theta_{Z^3}(1/2) > 0 by Campanino-Russo's strict inequality), or coarse T at
  q > 1/2 (p_c^site(T) = 1/2). A later link may use q >= p_k once p_c <= p_k is proved here (chain of certificates).
- Checker: for every nonempty parent-face trace U (adversarial over the parent's posterior, which makes the bound
  depth 0 and valid for every history), and for the root, the children's xi law must dominate Bernoulli(q)^children,
  decided by an exact monotone-coupling (max-flow = 1) or up-set certificate; P(xi(root) = 1) >= q.

Thresholds:
- Stage-3 gate (guide only, floats allowed): some block and rule reach worst-case margin >= 0 at a p <= 0.499.
  If none does with blocks up to 27 sites, the quarry is paused and the dossier says why.
- A claim: the checker passes in exact rational arithmetic (or verified intervals with outward rounding) at the
  claimed rational p*, and an independent implementation reproduces it.
null_test: not needed because the result is a deterministic proof certificate checked exactly; no search statistic
or "beats chance" claim is made.
