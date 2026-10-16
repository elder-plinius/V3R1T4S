# Research charter v1 (2026-10-15)

## Thesis
This charter belongs to someone who reads sequences as signals, writes the exact evaluator before the search, and is
happy to replicate a record object faithfully before changing one thing. It aims at small, checkable objects on
public tables (binary sequences, hypercube paths, comparator networks, tile puzzles, circle packings) where a
bit-sliced evaluator on one small machine, run patiently night after night with checkpoints, is the whole edge.
Famous crowded targets are set aside; two crowded ones are kept only because the objective is literally this
person's native representation.

## Quarries
- id: labs-merit-factor-records · question: a ±1 sequence of length 67–600 with exactly computed energy strictly
  below the best published value (unrestricted or skew-symmetric partial win p1) · shape: record · defined in:
  bank id labs-merit-factor-records; Packebusch & Mertens, "Low autocorrelation binary sequences", 2016
  (arXiv:1512.02475); tables in arXiv:2504.00987 and arXiv:2607.09688 · status to confirm first: the minimum
  energy per length across those three tables at run time · why us: aperiodic autocorrelation is the native
  representation here; evaluator-first and nightly patience are the method · weight: 4 · wild: no
- id: snake-coil-in-the-box · question: an induced path or cycle in Q_n (9 ≤ n ≤ 13) strictly longer than the live
  table, or a symmetric coil (partial p1) · shape: record · defined in: bank id snake-coil-in-the-box; the
  minortriad snake table; Orland-Fagan et al., arXiv:2607.15270 (2026) · status to confirm first: live table values
  per dimension and per kind · why us: bit-level evaluator, distance-profile pruning borrowed from signal work,
  resume-able beam search · weight: 4 · wild: no
- id: sorting-network-size-records · question: a comparator network on 13–32 channels with strictly fewer
  comparators (or smaller depth at equal size) than the live table · shape: record · defined in: bank id
  sorting-network-size-records; Dobbelaere's sorting-network tables; Knuth, TAOCP vol. 3 §5.3.4 · status to confirm
  first: the live (size, depth) pairs for n = 13..32 · why us: the 0-1 principle makes a bit-sliced exact evaluator
  the entire game, and prefix/suffix reverse engineering of record networks is what this person does with other
  people's artifacts · weight: 3 · wild: no
- id: slide-24-puzzle-lower-bound · question: a 5×5 sliding-tile position with an admissible-heuristic certificate
  of optimal length ≥ 154, or an independent reproduction of the 182 upper bound (partial p1) · shape: bound ·
  defined in: bank id slide-24-puzzle-lower-bound; OEIS A087725; the cubeman forum threads cited there · status to
  confirm first: best certified lower bound and the status of the 182 claim · why us: game-feel for hard
  positions plus disjoint pattern databases that fit in 8 GB · weight: 3 · wild: no
- id: packomania-cci-equal-circles-in-circle · question: N equal circles in the unit circle with feasible radius
  strictly above the live table value for one N, computed at 50 digits from raw coordinates · shape: record ·
  defined in: bank id packomania-cci-equal-circles-in-circle; the Packomania cci tables (Specht et al.) · status
  to confirm first: the live radius and author per N · why us: contact graphs and tangencies read like pixel
  geometry; replicate the record configuration, perturb one contact, re-optimise · weight: 3 · wild: no
- id: superpermutations-n7-n8 · question: a superpermutation for n = 7 shorter than the live record (5905 at last
  check) or n = 8 shorter than its record · shape: record · defined in: bank id superpermutations-n7-n8; the
  superpermutators group and repository; Egan's superpermutation pages · status to confirm first: the live record
  per n · why us: local rewriting of a long string is a signal-editing job; low weight because the crowd is
  active · weight: 2 · wild: no
- id: life-smaller-orphan · question: a Game of Life orphan with bounding-box area below 96, or a certified UNSAT
  proof for a box not yet ruled out (partial p1) · shape: existence / bound · defined in: bank id
  life-smaller-orphan; Hartman, Heule, Kwekkeboom & Noels, "Symmetry in Gardens of Eden", 2013; LifeWiki "Garden
  of Eden" · status to confirm first: the smallest listed orphan area · why us: it looks too strange to work, but
  two independent CNF encodings plus a DRAT check is exactly the gated workflow here · weight: 2 · wild: yes

## Lenses
- key: evaluator-first · title: The evaluator is the search · text: Spend the first hour on the fastest exact
  evaluator you can write (bit-sliced, incremental, memory-light), test it on a known record and a known loser,
  then let a plain local search run at full speed. First moves: port the objective to 64-bit words; measure
  evaluations per second; only then search. Dead when: a day of search at that speed cannot reach the record's
  neighbourhood even in principle. · skeptic: no
- key: object-as-data · title: Reverse-engineer the record · text: Treat the best known object as a specimen.
  Compute its invariants (autocorrelation profile, contact graph, prefix structure, symmetry group) and look for
  a regularity its authors did not state. Build from that regularity, not from scratch. First moves: fetch the
  record object, write the invariant report, cluster the records by structure. Dead when: the record's structure
  is fully explained by a published construction you cannot extend. · skeptic: no
- key: spectral-import · title: Signals, not combinatorics · text: Carry autocorrelation, spectral flatness and
  periodicity tools from signal processing into whatever the quarry is. Score candidates by spectrum, seed searches
  from flat-spectrum objects, prune by distance profile. First moves: define the transform for the object class;
  check whether records are spectral outliers. Dead when: records and random objects have indistinguishable
  spectra. · skeptic: no
- key: night-shift · title: Resume, do not restart · text: Every run continues the last checkpoint at low priority
  with a hard time cap, and writes down the exact state before stopping. Prefer one line of work pushed further
  over three lines started. First moves: read the dossier's live lead; resume it. Dead when: three consecutive
  resumed runs show no new best. · skeptic: no
- key: solver-argue · title: Let a solver argue · text: Encode the question as SAT, CP or ILP with symmetry
  breaking and let the solver prove or refute at small sizes; keep every proof certificate. First moves: the
  smallest instance where the answer is already known; match it exactly before scaling. Dead when: the encoding
  blows past memory at the first open size. · skeptic: no
- key: settled-already · title: Prove it is already over · text: Before attacking, try to show the quarry is
  settled, trivial or ill-posed: a newer paper, a tie disguised as a record, a table that moved last week, a
  criterion with a hidden quantifier. First moves: read the newest source first; recompute the record's value
  yourself. Dead when: you have an honest, dated statement that the cell is still open. · skeptic: yes

## Scout voice
Read for this person like a reverse engineer: what is the exact object, who holds it, since when, in which file, and
what does its structure look like. Skip narrative; quote definitions verbatim. Flag anything that would need a GPU,
a licence, more than a few gigabytes, or a human in the loop.

## Attacker voice
At their sharpest, this person builds the measuring instrument first, replicates the current record exactly, then
changes one thing at a time and lets the machine run while they sleep. Patient, literal, allergic to "it reads
well". Verification is never looser; the temperament is simply to keep the job alive and checkpointed.

## Heuristics
1. If the evaluator is slower than a million evaluations per second for small objects, fix that before anything else.
2. Replicate the record exactly before trying to beat it; a failed replication is a finding.
3. Prefer the lowest dimension or length where the table is still "best known", not "proven".
4. One quarry per run; one cell per claim; the dossier remembers the rest.
5. Warm-start from the record object; random restarts are a last resort.
6. A tie is a hint about structure, not a result.
7. Keep memory under 4 GB and disk under 2 GB per run.
8. When a line is dead, write where it died before starting the next one.

## Kill criteria
1. Memory above 6 GB or disk above 3 GB needed: kill the line.
2. The primary table cannot be fetched honestly: no claim, PENDING TABLE CHECK, move to a lens that does not need it.
3. Replication of the record fails after two attempts: stop attacking, report the discrepancy.
4. Search speed is more than 100× below what the published approach reports: kill, rethink the evaluator.
5. A result depends on a tolerance or a rounding choice: not a result.
6. Three resumed runs on the same lead without a new best: retire the lead to the dossier.

## Self-critique
The two strongest quarries (binary sequences, sorting networks) are crowded by people with faster machines; this
charter bets on patience and representation, which may just mean arriving second. The signal-processing lens may
be a metaphor rather than a method for discrete objects. The 24-puzzle lower bound might need more memory than
this machine has. The wild quarry could consume whole nights in a solver with nothing to show. The charter also
risks mistaking "a cell moved" for science: every quarry here is a table cell, none is a theorem.

## Method cards used
evaluator-first · object-as-data · far-import · solver · structured-family
