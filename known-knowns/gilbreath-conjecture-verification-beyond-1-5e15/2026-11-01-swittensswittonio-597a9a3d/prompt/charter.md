# Research charter v1 (2026-10-31)

## Thesis
The edge is speed and geometry: someone who writes exact evaluators fast, then profiles them until they fly, and
who thinks about rigid bodies, projections and overlap as everyday engineering. The charter aims that edge at
very old open questions (centuries old where possible) where a stranger can check the answer: geometric objects
that must fit, pass or fail to overlap, and certified computations that patience on one strong machine can push.
Seeds: the human chose "surprise me, long-standing and important"; method cards were drawn at random.

## Quarries
1. id: rupert-open-classical-solids. Question: does any of the nine undecided solids (snub cube, snub
   dodecahedron, deltoidal and pentagonal hexecontahedra, J72-J75, J77) admit a Rupert passage, or can a region of
   its configuration space be certified passage-free? Shape: existence or certified bound. Where defined: bank
   entry; Steininger and Yurkevich, arXiv:2508.18475. Status to confirm first: whether any of the nine was settled
   since 2025 (arXiv:2509.08190 and later). Why us: fast projection/containment evaluators over rotation space.
   Weight 5. Wild: no.
2. id: regular-tetrahedra-densest-packing. Question: is there a periodic packing of regular tetrahedra denser than
   4000/4671, or a non-4-per-cell packing above 100/117? Shape: record. Where defined: bank entry; Chen, Engel and
   Glotzer, arXiv:1001.0586. Status to confirm first: any packing claim after 2010 above 0.856347. Why us: overlap
   testing of rigid polyhedra at scale. Weight 4. Wild: no.
3. id: lebesgue-universal-cover-bounds. Question: certify a lower bound above 0.8344, or build a convex cover
   below 0.8440935944. Shape: bound. Where defined: bank entry; T. Tao's optimization constants page, problem 13b.
   Status to confirm first: the 2026 certificates (arXiv:2608.30538, 2609.01284). Why us: branch-and-bound over
   rigid placements with a fast interval evaluator. Weight 4. Wild: no.
4. id: gilbreath-conjecture-verification-beyond-1-5e15. Question: does the leading term of every difference row
   stay 1 for all primes up to X > 1.5e15? Shape: certified exhaustive computation. Where defined: bank entry;
   Odlyzko, "Iterated absolute values of differences of consecutive primes", Math. Comp. 1993. Status to confirm
   first: the live verified bound on Colonna's page. Why us: SIMD sieve and byte-array difference rows tuned with a
   profiler; months of weekly nights. Weight 3. Wild: no.
5. id: kissing-number-low-dim. Question: an exact kissing configuration in a dimension 9-23 larger than Cohn's
   table. Shape: record. Where defined: bank entry; H. Cohn's kissing-number table. Status to confirm first: the
   September 2026 table moves (arXiv:2609.35051). Why us: exact construction-space search with a fast exact
   checker, not float relaxation. Weight 3. Wild: no.
6. id: mertens-smallest-counterexample-upper-bound. Question: a certified point y below Kim-Nguyen's records that
   meets the Pintz or Saouter-te Riele criterion. Shape: bound. Where defined: bank entry; Kim and Nguyen, ANTS XVI.
   Status to confirm first: the 2026 claim under review (github.com/bzyzz/mertens_bound). Why us: long unattended
   lattice-reduction runs with checkpoints; 128 GB memory. Weight 2. Wild: no.
7. id: durer-convex-edge-unfolding-counterexample. Question: a convex polyhedron (or, as a partial win, a convex
   cap) with no edge unfolding. Shape: counterexample. Where defined: bank entry; Demaine and O'Rourke, Geometric
   Folding Algorithms (2007). Status to confirm first: arXiv:2607.09606. Why us: an
   overlap tester that runs over every spanning tree like a renderer runs over triangles. Weight 2. Wild: yes.

## Lenses
- key: evaluator. Title: Evaluator first. You spend the first hour building the fastest exact or interval-correct
  checker for the quarry's definition, then profile it. First moves: reference checker, then a vectorised one,
  agreeing on 1,000 random cases. Dead when the fast checker cannot beat the published method's rate by 5x.
  Skeptic: no.
- key: construct-space. Title: Search constructions, not objects. You search over rules that build the object
  (symmetry groups, gluing rules, lattices, rational rotations) instead of over raw coordinates. First moves:
  enumerate the smallest family that contains the known best object. Dead when the family's best equals the
  known record after exhaustive search. Skeptic: no.
- key: solver. Title: Let a solver argue. You recast the quarry as SAT, ILP, LP or SDP and let a solver find or
  refute. First moves: encode the smallest open instance and check that the encoding reproduces a known answer.
  Dead when the encoding cannot reproduce a known case within one hour. Skeptic: no.
- key: same-object. Title: Same object, other name. You look for the quarry's object in another field's tables
  (crystallography, lattice codes, mesh processing, robotics motion planning) and import it. First moves: list
  three fields where the object exists under another name. Dead when no imported object passes the checker.
  Skeptic: no.
- key: rigid-body. Title: Think like a physics engine. You treat the problem as rigid bodies and contacts: broad
  phase, narrow phase, separating axes, sweep tests. First moves: a separating-axis test with exact arithmetic,
  then randomised compression or passage sampling. Dead when sampling at 10^9 configurations finds nothing within
  1% of the record. Skeptic: no.
- key: skeptic. Title: Is it already settled? You try to show that the quarry is solved, trivial, ill-posed, or
  that the table value is wrong. First moves: newest arXiv and status page; replay the published certificate.
  Dead when the status is confirmed open and the certificate replays. Skeptic: yes.

## Scout voice
Read like an engineer checking a supplier's claim: what exactly was measured, with what arithmetic, over which
region, and is the code available. Note dates. Prefer the newest certificate over the oldest statement.

## Attacker voice
Impatient with slow code, patient with long runs. Builds the checker before the search, measures everything,
and keeps the machine busy overnight with checkpoints. Never trusts a float that has not been certified.

## Heuristics
1. A search is only as good as its evaluator: profile before you scale.
2. Start from the best known object and ask what local move it does not allow.
3. Impose symmetry to shrink the search, then break it on purpose.
4. A near miss within 1e-9 is a lead for exact arithmetic, not a result.
5. Reproduce one published number before trusting your pipeline.
6. Prefer quarries where a partial win is reachable within one run.
7. Checkpoint every few minutes; weekly runs must resume, not restart.

## Kill criteria
1. The status source shows the quarry settled or the record moved out of reach.
2. The checker cannot reproduce a known positive and a known negative case.
3. Three independent lines die at the same obstruction.
4. The required compute exceeds one machine for a month of weekly runs.
5. The only remaining path needs a judgement nobody can check.

## Self-critique
The charter leans on speed; many of these quarries are hard because of mathematics, not slow code, so a fast
evaluator may just reach the same wall sooner. Moonshots (tetrahedra, Durer, Mertens) will mostly yield clean
negatives; the realistic wins are partial ones (certified regions, replays, extended verifications).

## Method cards used
solver · same-object · construct-space (drawn at random).
