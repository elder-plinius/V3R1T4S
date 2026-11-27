# Research charter v1 (2026-10-15)

## Thesis

An unattached generalist with one 20-core machine and every night: the edge is tolerance for
monotonous exact grind at neglected table cells, not cleverness at famous ones. Aim a fast exact
evaluator at record tables where records fall to search speed; let symmetry tricks travel between
packing geometry and Diophantine hashing; read the oldest sources for constructions modern compute
could finish; and let a skeptic check whether a cell is already settled before touching it. The
seed categories (number-hunts, packings-physics) and method cards were drawn at random.

## Quarries

1. **id: packomania-cci-equal-circles-in-circle** — question: beat the per-N best packing of N
   equal circles in the unit circle for some N. shape: record (one table cell). defined:
   bank id packomania-cci-equal-circles-in-circle; live table https://packomania.com/cci/cci.html
   and its radius.txt. status to confirm first: the live per-N best radius and which cells are
   stale. why us: the feasible-radius evaluator is exact and trivial; hundreds of cells, many
   untouched for years; symmetric seeds plus symmetry-breaking local search suit a nightly machine.
   weight 5. wild no.
2. **id: taxicab-7-upper-bound** — question: find the smallest N with 7 pairwise-distinct
   representations as a sum of two positive cubes, lowering the known upper bound. shape: record.
   defined: bank id taxicab-7-upper-bound; OEIS A011541 (https://oeis.org/A011541). status to
   confirm first: the current smallest known upper bound on A011541. why us: pure evaluator-first
   grind (hash sums of two cubes); nightly accumulation compounds. weight 4. wild no.
3. **id: hall-conjecture-good-examples** — question: find integers x, y with x^3 − y^2 ≠ 0 whose
   Hall ratio √x/|x^3 − y^2| exceeds every ratio listed in OEIS A078933. shape: record. defined:
   bank id hall-conjecture-good-examples; OEIS A078933 and its b-file. status to confirm first:
   the largest ratio in the live b-file. why us: modular sieving is a long, unattended, exact
   grind; older searches left measurable headroom. weight 4. wild no.
4. **id: spherical-codes-cohn-table** — question: raise the best known minimal angle for some
   (d, N) row of the live spherical-codes table. shape: record (one table cell). defined: bank id
   spherical-codes-cohn-table; https://spherical-codes.org/plain. status to confirm first: the
   live row value and its holder. why us: same exact-evaluator edge; high-dimensional rows get
   little human attention. weight 3. wild no.
5. **id: pte-ideal-size-11-13** — question: find an ideal Prouhet–Tarry–Escott solution of size
   11, or of size ≥ 13. shape: existence (explicit object). defined: bank id
   pte-ideal-size-11-13; the open-size list on the Prouhet–Tarry–Escott Wikipedia page and
   arXiv:2304.11254. status to confirm first: that size 11 (and ≥13) is still listed without a
   known ideal solution. why us: structured-family search with symmetry is cheap to run
   exhaustively at these sizes; a solver can certify emptiness of a family. weight 3. wild no.
6. **id: packomania-hyperspheres-hsp4-hsp6** — question: beat the per-N record packing of equal
   hyperspheres in a 4-, 5- or 6-dimensional unit hypersphere. shape: record (one table cell).
   defined: bank id packomania-hyperspheres-hsp4-hsp6; https://packomania.com/hsp4/hsp4.html and
   sibling hsp5/hsp6 radius.txt files. status to confirm first: the live per-N radius. why us:
   almost nobody hunts these dimensions; symmetry constructions port up from the 2-D and 3-D
   tables. weight 2. wild yes.

## Lenses

- **key: evaluator-first** (card). You build the table's scoring function before anything else and
  test it on the current record-holder: it must reproduce the published value exactly (or to the
  stated precision) before any search starts. First move: implement the feasible-radius / angle /
  ratio evaluator and validate it against the record object. The line is dead when the evaluator
  cannot reproduce published values — then the cell is PENDING, not huntable.
- **key: symmetry** (card). You impose the symmetry group of the best known object to shrink the
  search space, search inside the invariant subspace, then break the symmetry on purpose and
  re-run. First move: find the symmetry of the record object; enumerate its orbits. The line is
  dead when symmetric families score strictly below the record across a stated, exhaustive
  enumeration with no near-misses.
- **key: archaeologist** (oldest-source card). You read the oldest sources on the cell — original
  papers, theses, errata, non-English tables — for constructions abandoned before modern compute
  existed, then finish them. The line is dead when the modernized old method still loses to the
  current record.
- **key: extender**. You take the strongest published computation for the cell and push it
  strictly further, saving a certificate. The line is dead when the published method's cost curve
  says the next step needs more than a week of nights.
- **key: skeptic** (statistician). You try to show the quarry is already settled, the table stale,
  or the would-be claim a tie. First move: re-fetch the live cell, check its last-improved date,
  hunt a recent preprint claiming the same improvement. This lens never dies; it serves the others.

## Scout voice

Read primary tables and old papers as possibly stale: verify a cell's value, holder and
last-improved date on the live page before believing the cell is neglected. Prefer primary
sources (the table's own txt files, OEIS b-files, the original paper) over summaries. A cell that
moved in the last two years has an active owner; note it and look elsewhere.

## Attacker voice

You are a grind, not a genius: pick the cell where exact arithmetic and hours of compute beat
cleverness, build the evaluator first, and distrust any line of work that skips it. Never claim
one cell wider than the checker reproduces; a near-miss within 1% of the record means the cell is
alive — note it, improve the search, return tomorrow. Boredom is not a reason to stop; a dead
line, stated exactly, is.

## Heuristics

1. No search before the evaluator reproduces the current record from the published object.
2. Prefer neglected cells (unchanged for years, few recent citations) over famous targets.
3. A near-miss within 1% of the record marks a live cell; revisit with a better search.
4. Port tricks across the two seed worlds: packing-geometry constructions ↔ Diophantine hashing
   and sieving.
5. Re-fetch the live table the same night as any claim.
6. Symmetric constructions first; symmetry-breaking perturbation second.
7. Save each search's checkpoint and certificate so the next night resumes rather than restarts.
8. If a cell moved recently, someone active owns it — move to the next quarry.

## Kill criteria

1. The cell is solved or overtaken on the live table (or a proof of optimality appeared) — dead,
   pick the next cell.
2. The evaluator cannot reproduce the published record value — PENDING TABLE CHECK; stop that
   cell.
3. A structured family was enumerated exhaustively (certified) below the record — record the
   covered space exactly and move on.
4. The next meaningful step needs more than a week of nights — keep only as a checkpointed
   background job and prefer another cell.
5. A would-be claim merely ties the criterion — not a win; do not package.
6. The target needs data or terms nobody here accepted — out of scope, mark off-limits.

## Self-critique

Grind loses to a specialist with a cluster; the protection is cell neglect, and neglect can be
misjudged from stale "last improved" dates. Cells can also fall to optimality proofs rather than
search — runs must check for proofs, not just new numbers. The taxicab and Hall cells attract
periodic attention; this charter may systematically arrive just after someone else. And the seeds
were drawn at random (number-hunts, packings-physics; cards symmetry, oldest-source,
evaluator-first), not chosen for any person at all — that is the point.

## Method cards used

symmetry, oldest-source, evaluator-first — drawn at random together with the two seed categories.
