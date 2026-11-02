# How we found it (contributor text, unverified)

The brief was a V3R1T4S run on the bank target windmill-kn2-harmonious-graham-sloane: decide whether the windmill
K_8^(2) (two copies of K_8 sharing one vertex, q = 56) is harmonious, either with an explicit labeling or with an
exhaustive search by two independent programs. Gallian's DS6 (28th ed.) still lists the Graham-Sloane conjecture
("K_n^(2) is harmonious iff n = 4") as open, and n = 8 is its smallest case not excluded by Levine or Liu.

- Scouting (lens already-settled) re-read DS6, Graham-Sloane Theorem 20, Levine 1983 and Liu 1994. None decides
  n = 8. The open list up to 50 came out as 8, 10, 16, 18, 20, 26, 32, 34, 36, 40, 50.
- What worked (lens exact-eval-first): a plain C backtracker (P1, wsearch.c) with 128-bit sum masks and f(c) = 0.
  It finishes n = 8 in about 40 s and finds no labeling. The translation reduction was checked by an unreduced brute
  force at n = 4 before the n = 8 run.
- A second, differently built program (lens drop-symmetry, P2, mitm.py) lists all 449,472 sum-distinct 8-sets
  containing 0 and joins complementary sum masks in about 12 s. It gives the same counts, the same 48 solutions at
  n = 4, and 0 at n = 8. A multiplier-orbit speed-up was dropped on purpose, so no second symmetry needs justifying.
- Obstruction lens: class-count projections mod 14 and mod 28 already leave no compatible pair (mod14.c,
  mod_multiset.py). This is extra evidence, not the decision. Projections mod 2, 4, 7 and 8 alone are not decisive.
  CP-SAT was far too weak (UNKNOWN at n = 5 and 6 after 120 s) and was dropped.
- Table-as-data lens: a third C join (wjoin.c) agreed at n = 8. It also reported 0 labelings at n = 10, but that is
  one program only. It is not claimed here and is left as a lead.
- A same-session self-check enumerated all C(55,7) = 202,927,725 candidate 7-sets with no pruning and got the same
  449,472. A three-skeptic panel (reproduce, novelty, criterion), each in a fresh context, wrote its own searches,
  re-fetched DS6, and confirmed the scope quoted in README.md. For this package, check_decision.py was written to
  tie the rerun numbers to object/DECISION.txt and to re-derive the n = 4 solution list independently.
