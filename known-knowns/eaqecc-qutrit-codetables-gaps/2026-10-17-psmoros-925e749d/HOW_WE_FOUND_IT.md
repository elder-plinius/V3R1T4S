# How we found it (contributor text, unverified)

- **Brief.** Raise a d_lower in Grassl's qutrit EAQECC table with c >= 1. The table's sources are GF(9)-linear codes through the Hermitian construction, plus propagation rules.
- **Search.** Five independent lenses each ran about 100 minutes:
  - quasi-cyclic GF(9) codes with hull scaling;
  - algebraic and Hermitian-curve GF(9) codes;
  - GF(3)-additive codes;
  - exact small cases;
  - literature.
- **What worked.**
  - The small-cases lens noticed that impure (degenerate) codes with k = 1 are outside the table's GF(9)-linear sources.
  - It wrote down an explicit class construction. The positions are split into classes; on each class the logical Z parts sit on a point of PG(1,3), and the radical is a sum of small X-type pieces. This gives [[n,1,n-1;n-1-T]] codes, and then d = n-2 codes.
  - In the cell (33,1,24) it gives d = 31 against the table's 25.
- **Independent rediscovery.** A separate lens reached [[33,1,30;24]] by repeatedly extending a [[10,1,7;1]] code.
- **What failed.**
  - Random hill-climbing for k = 2 impure codes.
  - Quasi-cyclic searches at n = 17..20.
  - Raising Hermitian hulls by sign scaling.
- **The panel.** The NOVELTY skeptic found that the elementary k = 1 extension rule on the table's own teleportation codes already gives 30. Over easily derived codes the margin is therefore +1.
