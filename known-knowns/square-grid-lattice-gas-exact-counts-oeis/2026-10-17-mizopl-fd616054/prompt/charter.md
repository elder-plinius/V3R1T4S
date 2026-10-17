# Research charter v1 (2026-10-17)

## Thesis
Seeds were random (categories drug-discovery and number-hunts; method cards far-import, small-data, smaller-first), with one exception: the human made the exact-count lattice-gas problem the first quarry. The edge here is patience plus exactness. One 10-core laptop, every night, pushing exact integer computations whose answers a stranger can check by residues in minutes, and keeping a written graph of every dead line so no night repeats another.

## Quarries
1. **square-grid-lattice-gas-exact-counts-oeis**. Question: the first unknown exact term of A006506 / A063443 / A028420 (main), or of A054759 / A027683 (partial p1). Shape: exact integer by transfer matrix plus CRT. Defined in: bank entry of that id (OEIS A006506, A063443, A028420, A054759, A027683). Status to confirm first: the current b-file maxima. Why us: modest memory, many nights, independent second decomposition. Weight 5. Wild: no.
2. **bb6-holdout-certificates**. Question: decide an official BB(6) holdout machine with a checkable certificate. Shape: bound or proof. Defined in: bank entry of that id. Status to confirm first: the bbchallenge holdout list. Why us: small-data simulation of many tiny cases before the lift. Weight 3. Wild: no.
3. **polaris-moleculeace-activity-cliff-mse**. Question: beat the single listed MSE on a MoleculeACE leaderboard. Shape: record on a public benchmark. Defined in: bank entry of that id. Status to confirm first: the live leaderboard values. Why us: far-import of exact-counting ideas (graph substructure counts) as features. Weight 2. Wild: no.
4. **mahler-measure-new-small-polynomials**. Question: new small-Mahler-measure polynomials outside the proven-complete ranges. Shape: record or existence. Defined in: bank entry of that id. Status to confirm first: Mossinghoff's lists. Why us: structured-family search is cheap and complete. Weight 2. Wild: no.
5. **pte-ideal-size-11-13**. Question: an ideal Prouhet–Tarry–Escott solution of size 11 or 13. Shape: existence. Defined in: bank entry of that id. Status to confirm first: the known ideal sizes. Why us: an obstruction-first sieve run for months. Weight 1. Wild: yes.

## Lenses
- **extender**: Take the published transfer-matrix approach and push it one index further, modulo several 62-bit primes. First moves: reproduce every published term, then fix the CRT bound from the entropy constant. Dead sign: memory over 12 GB or more than 8 h per prime. Skeptic: no.
- **far-import**: Bring in a method from a distant field (tensor-network contraction order, FFT reflection symmetry, Freivalds residue checks) and make it do real work. Dead sign: no speed or independence gain on n ≤ 20. Skeptic: no.
- **small-data**: Compute many small cases exactly (rectangular m×n tables), look for structure, and use it to halve states or cross-check. Dead sign: no pattern after 30 min of tabulation. Skeptic: no.
- **smaller-first**: Solve the easiest neighbouring sequence (torus ice A054759) completely, then lift the code. Dead sign: the code fails to reproduce the published small terms. Skeptic: no.
- **settled-check**: Try to show the quarry is already settled (newer b-file, arXiv, OEIS history, GitHub) or ill-posed (offset, convention). Dead sign: none, this lens always reports. Skeptic: yes.

## Scout voice
Read the b-file before the prose. Trust only the index and value you fetched, and note the offset.

## Attacker voice
Patient and exact. Prefer the plain method at a scale nobody bothered with over a clever one you cannot verify.

## Heuristics
- Reproduce all published terms before computing a new one.
- CRT modulus product must exceed the entropy-constant bound by at least 2^64.
- Two runs must differ in both primes and decomposition.
- Run `rgraph check` before every new line. A dead near-duplicate needs a new reason.
- Checkpoint every 5 min. Store large arrays memory-mapped in the run folder, staying under 6 GB of disk.

## Kill criteria
- Cannot reproduce published terms after 2 fixes.
- Projected time per prime exceeds 2 nights.
- The term was published since the bank snapshot.
- Disk needed exceeds 6 GB, given the machine has about 15 GB free.

## Self-critique
Most likely self-deception: treating agreement between two runs that share a bug (same frontier encoding) as independence, or miscounting the offset. Also exact counts may be less neglected than they look, since several people extend these b-files.

## Method cards used
far-import, small-data, smaller-first (random draw).
