# PREREG — square-grid-lattice-gas-exact-counts-oeis
Frozen 2026-10-17T12:26Z (date -u), before any attack output exists. First live run, effort: light.

## Criterion being measured (verbatim from bank / target.md)
Success means the exact integer value of the first unknown term a(N) of A028420, A006506 or A063443, where N is
one more than the largest index in the sequence's DATA and b-file re-fetched live immediately before claiming,
computed by two independent runs that agree exactly (different primes/CRT moduli sets AND a different
decomposition, e.g. row vs column sweep or a different state encoding, or one exact big-integer run), with the
same code reproducing every published term for n <= N-1 exactly, and the result consistent with the known growth
constant (a(N)^(1/N^2) within 1e-3 of the corresponding entropy constant).

Partial wins (verbatim):
- p1: next unknown term(s) of A054759 (square ice on n x n torus) or A027683 (hard squares on n x n torus), same
  two-run and reproduction rules.
- p2: a new row of an associated rectangular table (A210662 monomer-dimer m x n, A089980 hard squares m x n)
  extending the largest published m by one for all n up to the published range, same rules.

## Exact statistic / checker that will judge a win
Deterministic integer equality, no statistics:
1. REPRODUCTION gate: the attacking code must reproduce EVERY published term of the sequence (from the live
   b-file saved in data/) exactly, with no term skipped.
2. TWO-RUN gate: the new term a(N) must come from two runs that differ in BOTH the CRT prime set AND the
   decomposition/encoding, and agree digit-for-digit. A single big-integer exact run also satisfies this if a
   second modular run agrees.
3. CRT-BOUND gate: product of moduli must exceed the entropy-constant upper bound on a(N) by at least 2^64
   (charter heuristic), so the CRT reconstruction is the true integer, not a residue.
4. GROWTH gate (as written): a(N)^(1/N^2) within 1e-3 of the corresponding entropy constant. NOTE/CAVEAT
   (HEURISTIC, from BRIEF F5): for the OPEN-boundary sequences (A028420/A006506/A063443) this clause as written
   may be unmeetable at these finite N because open-boundary finite-size corrections exceed 1e-3; recorded as a
   criterion ambiguity under "Needs you". For the torus sequences (A054759/A027683) the finite-size gap is also
   nonzero; any claim states measured a(N)^(1/N^2) and the reference constant literally and does not round in its
   own favour.
5. index / offset gate: N is taken as (largest index in the live b-file) + 1, using the sequence's own offset.

## Thresholds
- Win requires gates 1-3 and 5 fully met and reported from command output, and gate 4 reported literally
  (value and reference constant both printed; if it fails as written, the result is reported as `progress` /
  `PROMISING` with the growth clause flagged, never silently rounded to pass).
- No partial credit for a term that matches mod the product but was not CRT-bounded above the true value.

## Null design
null_test: not needed because every claim here is an explicit exact integer verified by a deterministic checker
(two independent modular transfer-matrix computations that agree digit-for-digit, AND reproduction of every
published b-file term, AND a CRT bound above the entropy-constant estimate). This is deterministic verification of
a named object against published table values, not a search over a hypothesis space or a "beats chance" claim, so
the 400-control null test does not apply (kit RUN.md step 3b; LESSONS 4 example of a deterministic object check).
The independence of the two runs (different primes AND different decomposition) is the control against a shared
reconstruction coincidence; a shared frontier-encoding bug is addressed by the two decompositions differing
(charter self-critique).
