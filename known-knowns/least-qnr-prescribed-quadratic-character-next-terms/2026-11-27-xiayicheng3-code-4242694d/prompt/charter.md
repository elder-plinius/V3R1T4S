# Research charter v1 (2026-11-27)

## Thesis
The human asked for mathematics and said "surprise me". The seeds were drawn at random: two categories
(packings-physics, number-hunts) and three method cards (footnotes, same-object, oldest-source). The edge here is
patience and bookkeeping, not brilliance. Many records sit in sibling tables that bound each other, in old tables
that nobody has rerun since 1994, and in brackets that recent b-files imply but nobody has closed. The charter hunts
where one exact, cheap, exhaustive computation can close a gap that the literature already narrowed in its footnotes.

## Quarries
1. **id: least-qnr-prescribed-quadratic-character-next-terms**. Question: what is A000229(39), the least prime
   whose least quadratic non-residue is 167? Shape: record/next term with a minimality certificate. Defined: OEIS
   A000229; Lehmer, Lehmer and Shanks, Math. Comp. 24 (1970); bank entry. Status to confirm first: the b-file
   still ends at n = 38, and A002223/A002224 still bracket it. Why us: the sibling b-files reduce it to a window,
   and a wheel sieve settles it in minutes. Weight 5. Wild: no.
2. **id: least-qnr-prescribed-quadratic-character-next-terms (A000229(41) / A002224(42))**. Question: push the
   same character sieve past the bracket to settle the term for least QNR 179, and A002224(42). Shape: next term.
   Defined: OEIS A000229, A002224. Status to confirm first: the b-file ends. Why us: same tool, longer nights.
   Weight 3. Wild: no.
3. **id: sloane-cohn-spherical-coverings-s2**. Question: does a configuration of N points on S^2 (N = 15..130)
   beat the 1994 Hardin-Sloane-Smith covering radius, and do the posted files reproduce the table? Shape:
   record, or a table-integrity finding. Defined: neilsloane.com/coverings; cohn.mit.edu/sloane. Status to confirm
   first: Cohn's live table. Why us: oldest-source card; the 1994 searches for large N were short. Weight 3. Wild: no.
4. **id: sloane-cohn-max-volume-polyhedra-s2**. Question: N points on S^2 whose convex hull beats the best of the
   Sloane, Deeter and Cohn volumes. Shape: record. Defined: neilsloane.com/maxvolumes; deetour.net maxvol tables.
   Status to confirm first: all three tables. Why us: same-object card; Deeter's dual-of-roundest-polyhedra
   construction already beat Sloane twice, so other polyhedral dualities may too. Weight 2. Wild: no.
5. **id: wieferich-other-bases-fischer-table**. Question: a new base-b Wieferich pair beyond Fischer's stated
   limits. Shape: record/existence. Defined: fermatquotient.com tables. Status to confirm first: the live
   FermQ_Sorg.txt limits. Why us: patience; one machine for many nights. Weight 2. Wild: no.
6. **id: largest-small-even-polygons-area**. Question: a convex n-gon of diameter 1 with larger area than the
   best known. Shape: record. Defined: bank entry and its cited literature. Status to confirm first: the bank's
   sources. Why us: none obvious, which is the point. Weight 1. Wild: yes.

## Lenses
- **sieve-first** (skeptic: no): You build the fastest exact evaluator before you think. Use a CRT wheel, then
  bitmask filters, then a primality proof. First moves: reproduce known terms from 1. Dead sign: the enumerator
  misses a known term.
- **sibling-tables** (skeptic: no): You read neighbouring sequences and tables as constraints on each other.
  First moves: list every implied bracket. Dead sign: no bracket tighter than the trivial one.
- **independent-recheck** (skeptic: yes): You assume the result is wrong and rebuild it with a different
  method: a plain segmented sieve over a sub-range, or a different modulus split. Dead sign: the two methods agree
  and the claim survives.
- **old-table-rerun** (skeptic: no): You rerun the oldest public table's own files with a modern optimiser from
  many random starts. Dead sign: 500 restarts never beat the table.
- **dual-construction** (skeptic: no): You treat the best known object as data and build its dual or another
  name for the same object, then polish it. Dead sign: every dual lands in a known basin.
- **settled-already** (skeptic: yes): You try to show that the quarry is already settled, trivial or ill-posed:
  search OEIS history, arXiv and the repo's pull requests first. Dead sign: nothing found after a real search.

## Scout voice
Read b-files and tables as dated claims. Quote the last line, note the edit date, and look for siblings that imply
more than the main sequence says.

## Attacker voice
Calm and exhaustive. Prefer one complete search with a certificate over ten clever partial ones.

## Heuristics
- If two sequences bound each other, the gap between them is the cheapest result in sight.
- Reproduce known terms from 1 before trusting any window.
- A search you cannot state exactly is not a covered space.
- Small moduli first, cheap rejections early.
- Record the residue count and candidate count; they are your sanity checks.

## Kill criteria
- The enumerator fails to reproduce a known term: stop and fix it, never patch around it.
- The live table moved past what one machine can reach in a week.
- The result is implied by already-published values (not new).
- Two independent methods disagree and the cause is not found within the budget.

## Self-critique
The charter favours easy-to-close gaps, which are also the ones most likely closed by someone else last week; the
scout must re-check every status on the day. Sieve results can hide off-by-one indexing and composite-modulus
subtleties, so definitions get quoted verbatim before any search.

## Method cards used
footnotes, same-object, oldest-source (random draw).
