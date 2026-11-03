# Research charter v1 (2026-10-31)

## Thesis
Seeds were drawn at random: chemistry-materials and recreational-math, with the method cards representation,
evaluator-first and smaller-first. The edge is a chemist's habit carried into puzzle tables: treat every search as an
energy landscape with funnels and basins, build a fast exact evaluator before searching, and calibrate on small
cases whose answers are proved. One quiet machine with modest free memory favours CPU-bound, small-state searches
that accumulate across many short runs.

## Quarries
1. **lj-zpe**: bank `ccd-quantum-lj-zpe-rare-gas-clusters`. Question: for some N on the Calvo–Doye–Wales LJ+ZPE
   table (J. Chem. Phys. 114, 7312, 2001), is there a certified classical LJ_N minimum whose harmonic zero-point-corrected
   energy E_sp (Xe, Ar or Ne) is strictly below the table's row? Shape: record. Where defined: the bank entry and the
   table page it cites. Status to confirm first: the live table and any later quantum-cluster paper that re-ranked
   these sizes. Why us: a 2000-era list ordered by classical energy, re-screened with a fast analytic Hessian over
   many more low-lying minima. Weight 5. Wild: no.
2. **perkins**: bank `mrs-perkins-quilt-large-sides`. Question: for some n in 19..39, a dissection of a k x k square
   into at most n integer squares with gcd 1, with k strictly above the best-known A089047(n). Shape: record. Where
   defined: OEIS A089047 and Wynn, arXiv:1308.5420 (2013). Status to confirm first: A089047 DATA and Pegg's comment
   terms, and squaring.net's quilt list. Why us: quilts are electrical networks (Brooks–Smith–Stone–Tutte 1940);
   generating from networks rather than from tilings is a representation change. Weight 4. Wild: no.
3. **water**: bank `magic-square-water-retention-records`. Question: a normal magic square of order 10..15 whose
   water retention beats the A201126 lower bound. Shape: record. Where defined: OEIS A201126 and Knecht's model as
   stated there. Status to confirm first: the A201126 bounds (contest values from 2010 may have moved). Why us: a
   priority-flood evaluator with incremental updates, inside a funnel-aware annealer seeded from the published
   squares. Weight 3. Wild: no.
4. **fullerene**: bank `fullerene-isomer-counts-beyond-c400`. Question: the exact count A007894(201) or A046880(201)
   (C402), with every earlier term reproduced. Shape: bound or proof (exact enumeration). Where defined: OEIS A007894
   and A046880; Brinkmann, Goedgebeur and McKay, arXiv:1207.7010 (2012); the oriented-count formula cited by the
   bank (arXiv:2304.01655). Status to confirm first: whether the b-files already extend past n = 200. Why us: the
   counting becomes lattice arithmetic in the Eisenstein-integer parameterisation; the hard part is the achiral
   correction, a symmetry-restricted count. Weight 3. Wild: no.
5. **monostable**: bank `monostable-polyhedron-fewer-than-14-faces`. Question: a homogeneous convex polyhedron with
   exact rational vertices, fewer than 14 faces, resting stably on exactly one face. Shape: existence / record.
   Where defined: Conway and Guy (1969); Reshetov, IJCGA 24(1), 2014; the bank entry. Status to confirm first: any
   smaller monostable polyhedron published since 2014. Why us: treat the centroid's projection margins as a
   potential surface and search shapes the way one searches cluster geometries. Weight 2. Wild: yes.

## Lenses
1. **evaluator-first**, *Make the judge fast before you search* (skeptic: no). Spend the first block of time on an
   exact, fast evaluator: analytic gradients and Hessians, incremental updates for local moves, exact rational
   arithmetic only for the final check. Benchmark it against a naive version on the same inputs and keep both
   outputs equal. Dead sign: after the first block the evaluator is not at least 10x faster than naive, or the two
   disagree on any input.
2. **landscape**, *Search it like a cluster* (skeptic: no). Treat the objective as a potential energy surface:
   basin-hopping, parallel tempering, and restarts from the published best objects, with moves that respect the
   problem's symmetry. Track how many distinct basins you have seen and how often you land in the known best one.
   Dead sign: every funnel ends in the known best value or a symmetric copy, across at least three independent
   move sets.
3. **smaller-first**, *Prove the small cases, then lift* (skeptic: no). Solve the smallest instances exactly where
   the answer is known (small LJ_N minima in the Cambridge Cluster Database, quilts for n <= 18 as proved by Wynn,
   retention for n <= 9 as listed in A201126, fullerene counts for small C_n) and make the method reproduce every one. Tabulate the winners' structure and lift the pattern one size up.
   Dead sign: the method misses a proved small value, or the lifted pattern fails at the first new size.
4. **representation**, *Change the coordinates until it looks easy* (skeptic: no). Recast the object: quilts as
   Smith-diagram networks or Bouwkamp codes, fullerenes as Eisenstein-lattice data, clusters in normal-mode
   coordinates, magic squares as complementary-pair permutations. Search in the new space and map back exactly.
   Dead sign: the new space is no smaller than the old one, or everything it yields is already published.
5. **distant-import**, *Bring the other seed's tools* (skeptic: no). Use the method of the other seed category on
   this quarry: chemistry's global-optimisation and normal-mode analysis on recreational objects, and recreational
   exhaustive enumeration and symmetry breaking on chemical ones. Dead sign: the imported method cannot reproduce a
   known value in its first hour.
6. **already-settled**, *Prove it isn't open* (skeptic: yes). Try to show the quarry is settled, trivial or
   ill-posed: reproduce the table's own values first, look for a later paper or b-file extension, and check whether
   a "new" object is a trivial edit (deletion, relabelling, symmetry, local polish) of a published one. Dead sign:
   you cannot reproduce the table's values; then nothing else is trustworthy until you can.

## Scout voice
Read like a lab notebook referee: quote the definition exactly, copy the current best value and its date, and note
who last moved it. Distrust any number you did not recompute. Prefer the oldest primary source next to the newest
update, and say plainly when a table looks stale or abandoned.

## Attacker voice
Patient and empirical, like a computational chemist mapping a landscape: measure before guessing, keep every
negative, and let the evaluator decide. Willing to try an odd move set for an hour if it ends in an object the
checker can judge.

## Heuristics
1. The first hour builds the evaluator; the search inherits its speed.
2. Reproduce one known value before attempting a new one.
3. Seed from the published best object and say so; beat what trivial edits of it give.
4. Count distinct basins; a search that keeps finding the same one is telling you something.
5. Small proved cases are test oracles, not warm-ups.
6. Keep memory small: stream, chunk, or recompute rather than store.
7. Record covered spaces only when they are exhaustive and stated exactly.
8. A strange move set is fine if it ends in a checkable object.

## Kill criteria
1. The table or b-file already lists a value equal to or better than anything within reach.
2. The method cannot reproduce a proved small case.
3. The only gains come from loosening the definition (tolerances, counting convention, ring or scope).
4. The computation needs more memory than half the free memory, even after chunking.
5. Three independent move sets or representations all stall at the known best value.
6. The quarry turns out to be a duplicate of another quarry in this charter.

## Self-critique
The seeds are random, so the "edge" is a stance, not an expertise: a chemist's landscape view may add little where
specialists already ran strong annealers (water retention, quilts). The LJ+ZPE quarry carries most of the weight; if
its table was re-done after 2001, the charter loses its best quarry. Fullerene counting may be cluster-scale in
practice despite the bank's laptop estimate. The wild quarry has resisted strong searches since 2014.

## Method cards used
representation, evaluator-first, smaller-first (drawn at random).
