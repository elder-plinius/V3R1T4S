# How we found it (contributor text, unverified)
An agent run picked the bank target, fetched the 971-row list, and froze its rule (how-we-built-it/PREREG*.md) before
scoring. The idea: the listed orbits start on the fixed set of a reversor S, so the half-period condition is a square
3x3 system G(vx, vy, t) = 0 that Krawczyk's test can certify, and half a period of variational equations gives the full
monodromy as S A^-1 S A. A small validated Taylor integrator in arb ball arithmetic (Cauchy-estimate remainders from a
complex Picard inclusion) produced the enclosures. What failed first: a 12x12 characteristic polynomial with a 1e-30
box (too wide), and a prereg invariant that was not invariant (fixed before scoring, PREREG.v2). What worked: smaller
boxes with more precision, and the 4x4 reduced monodromy on U^omega / span(f, Rx0) (PREREG.v3). Controls: the
figure-eight passes; a shifted box fails existence; the unstable Butterfly I passes existence but is certified hyperbolic.
