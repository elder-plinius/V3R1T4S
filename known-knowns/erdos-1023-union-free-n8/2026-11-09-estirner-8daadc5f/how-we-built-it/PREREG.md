# PREREG: erdos-1023-union-free-n8, cell n = 8 (run 2026-11-09-1306)

Frozen at 2026-11-09T13:15:16Z (date -u), before any search output of this run exists. Disclosure: the
bank scan's deep check reported an 80-family (n = 8) and a 150-family (n = 9) earlier today; this run regenerates
candidates with its own search and judges every candidate with the checker below.

## Criterion (verbatim, bank repo commit 06b61ea)

Success means an explicit list of at least 80 distinct nonempty subsets of {1..8} (direction: max, strictly above 79) such that no member S equals the union of the other members contained in S. The verifier checks this for every S, which covers unions of any number of other members. The size must exceed every value in the live https://oeis.org/A347025 entry, its comments, links and history, re-fetched immediately before claiming, and any value found in a fresh literature check. More than 89 sets contradicts Loo's bound and means a bug.

Partial win p1 (verbatim): An explicit union-free family (same check) of at least 145 subsets of {1..9} or at least 271 subsets of {1..10}, beating Schoenfield's construction values 144 and 270.

## The judge

A family F of subsets of {1..8} counts only if a stdlib checker, written from the definition, confirms:
1. every member is a nonempty subset of {1..8}; members are pairwise distinct;
2. for every S in F: the union of all T in F with T a proper subset of S is not equal to S (this covers unions of any
   number of other members, since any union of members inside S is contained in that maximal union);
3. |F| >= 80 (and <= 89, else a bug).
The checker is first calibrated: by brute force over all families it must reproduce a(1..4) = 1, 2, 4, 7.
The live OEIS entry is re-fetched before claiming; the claim stands only if |F| exceeds every value there.

null_test: not needed because the claim is an explicit finite object checked by a deterministic checker against a published table value.
