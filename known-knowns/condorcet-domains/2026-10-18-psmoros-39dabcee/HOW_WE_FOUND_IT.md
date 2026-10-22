# How we found it (contributor text, unverified)

- Target: Q5 of the contributor's charter, an explicit Condorcet domain larger than the best published one for some
  n >= 9. The record list is Table 4 of arXiv:2601.07336v1 (January 2026); its n = 9..20 rows come from a large
  inductive search, its n = 21..25 rows from the Karpov-Slinko construction applied to smaller domains.
- An earlier session rebuilt the paper's record chain exactly with its own extension step, then went past it with a
  large-neighbourhood local search (re-optimising all triples through a pair of alternatives at once) and a
  multigrid-like cycle: polish near the top, restrict down by deleting one alternative, polish again, extend up.
  That lifted every n from 14 to 25 above Table 4; n = 21 was claimed first in its own folder.
- This verification run (the human's order: one claim folder for the other eleven rows, each judged on its own)
  re-checked every row with three independent verification lenses, the main session's own tools and a fresh
  three-skeptic panel. For n = 23, 24, 25 the explicit lists are 2.5-12.5 GB of text, so the object is the
  never-condition assignment with an exact count and a hash-pinned canonical enumeration; the CRITERION skeptic
  ruled that this is an explicit set.
- What failed (earlier sessions): annealing on single-triple moves, two-step lookahead, never-middle conditions,
  crossover of two domains, unbalanced Karpov-Slinko splits, set-alternating domains, exact star solves at n = 20
  and 21 (too slow on this machine). The records for n = 9..13 were not beaten (local optima).
