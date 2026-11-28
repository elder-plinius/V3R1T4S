# PREREG — dom(Q_12), written before any computation of this run (time stamp from `date -u` on the last line)

Criterion: verbatim in target.md (bank entry queens-graph-domatic-numbers). Cell: dom(Q_12), currently {20, 21}.

Definitions. Q_12: 144 squares; two squares are adjacent when they share a row, a column or a diagonal. A set D
dominates when every square is in D or adjacent to a square of D. A domatic k-partition: all 144 squares split into k
classes, each dominating.

Lower-bound claim (partial win p1) is made only for a grid file with 21 classes on n = 12 for which BOTH
runs/2026-11-05-0019-queens/attempts/checker/code/check.py and check_bits.py (independent of all search programs,
validated on 2026-11-05 on Lauri's published partitions: PASS, and on a mutated grid: FAIL) print PASS, and after a
panel. Nothing else counts as a win.

Upper-bound side. Counting lemma (PROVED-HERE, elementary): in a domatic 21-partition, shrink every class that
contains a dominating 6-set to that 6-set (moving the extra squares to another class keeps all classes dominating).
Then each class is one of the dominating 6-sets (a of them), or a minimal dominating 7-set (b of them), or has at least
8 squares. Sizes sum to 144, so 6a + 7b + 8(21 - a - b) <= 144, that is 2a + b >= 24, with the a + b sets pairwise
disjoint. Statistic: M = max of 2a + b over families of pairwise disjoint sets taken from the complete list of
dominating 6-sets and minimal dominating 7-sets of Q_12.
- If an exact certificate (rational dual checked in exact arithmetic, or an exhaustive integer search) gives M < 24:
  dom(Q_12) = 20 as mathematics. This is NOT a bank win (the criterion demands a DRAT/LRAT-checked UNSAT proof) and
  will be reported with claim level "negative"/"progress", never as p2.
- If M >= 24: the cell stays open; the families reaching 24 are the only possible skeletons of a 21-partition and the
  second lens searches them for a full partition.
The lists count only if (i) the new enumerator reproduces the known values: Q_11 m = 5 -> 2 sets, Q_11 minimal
m = 6 -> 432 sets, Q_12 m = 6 -> 8 sets; (ii) two runs with different branching rules give the identical list for Q_12
m = 7; (iii) an independent Python script confirms every listed set is dominating and minimal. Completeness then rests
on the enumerator's correctness argument plus (i) and (ii); this limit will be stated.

null_test: not needed because the claims are explicit objects or exact certificates checked deterministically
written_utc: 2026-11-11T17:29:27Z
