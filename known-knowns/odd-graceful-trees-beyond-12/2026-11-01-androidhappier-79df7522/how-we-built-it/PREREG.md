# PREREG: odd-graceful-trees-beyond-12

frozen_at_utc: 2026-11-01T02:28:42Z

Nothing has been computed for this target before this file (no search output exists yet).

## Criterion (verbatim, bank)
Success means EITHER (a) a certificate that every tree on at most 22 vertices is odd-graceful: for each n in 13..22, a
file giving every unlabeled tree on n vertices (as from nauty gentreeg) with an odd-graceful labeling, where an
independent checker regenerates the trees, confirms the counts equal A000055(n), matches every tree by canonical form,
and checks the labels are distinct in [0, 2n-3] with edge differences exactly {1, 3, ..., 2n-3}; OR (b) a tree with no
odd-graceful labeling, certified by two independent exhaustive methods. Before claiming, re-check the latest DS6
edition and the literature for a higher verification bound.
Partial p1: certificate as in (a) for every tree on at most 16 vertices. p2: at most 20 vertices.

## Checker and thresholds
- Certificate file per n (13..22): one tree per line (parent array of the generator's tree) and its labels.
- Checker K (written separately from the searcher; C): (1) regenerates all trees on n vertices by leaf addition to all
  trees on n-1 vertices, deduplicated by a canonical code (min over the tree's centres of the rooted AHU code);
  (2) count must equal A000055(n) as fetched (data/A000055.txt); (3) for each certificate line: it is a tree on n
  vertices, labels distinct integers in [0, 2n-3], the multiset of |f(u)-f(v)| over edges equals {1,3,...,2n-3}
  exactly; (4) the set of canonical codes of certificate trees equals the regenerated set (no missing, no duplicate,
  no extra). PASS for order n only if all four hold. Also: the checker must accept a known positive (a hand-made
  odd-graceful path labeling) and reject known negatives (a duplicated label, a wrong difference set, a missing tree).
- Full win: PASS for every n = 13..22. p2: every n = 13..20. p1: every n = 13..16. (Orders <= 12 are known; the
  certificate also covers 2..12 as a regression if cheap.)
- Counterexample route (b): a tree for which the searcher fails would be re-examined by two independent exhaustive
  methods before any claim; a heuristic failure alone is never evidence.

null_test: not needed because the result is a set of explicit labelings checked deterministically, with coverage
checked against an independent regeneration and A000055; there is no search score or statistic to beat chance.

Baseline (step 3c): not applicable.
