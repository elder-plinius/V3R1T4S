# PREREG

frozen_at: 2026-11-03T07:08:00Z
The clock line below is filled from `date -u` before any attack output is scored. If that command time is later than this placeholder, the command time is the freeze time.

id: quaternary-legendre-pairs-open-lengths
cell: l = 70

criterion verbatim:
Success means an explicit pair A, B of a length l in {70, 76, 88, 92, 94, 100} with entries in {1, -1, i, -i} and PAF_A(k) + PAF_B(k) = -2 exactly (Gaussian-integer arithmetic) for every k = 1..l-1, verified by two independent programs, where no qLP of that length is reported at claim time in a fresh arXiv search for 'quaternary Legendre' (direction: none; existence target). A rigorous nonexistence proof for one of these lengths (DRAT/LRAT-checked on a CNF the skeptic regenerates, or an exhaustive search the skeptic re-runs) also counts.

partial win p1 verbatim:
A certified exhaustion, at l = 70 or 76, of a precisely stated structured family that Lebedev's recorded queues do not cover and that no publication or public note already rules out, with code and logs the skeptic re-runs to the same empty result. Examples: pairs whose four Gray rows are invariant under a stated multiplier subgroup of Z_l^*, or decompositions in which only one Gray-row pair is symmetric about a common integer centre. Families already excluded by a short necessary condition do not count. At l = 70 and 76 the midpoint-frequency identity (the four squared alternating sums of the Gray rows add to 4l + 4) rules out every family in which some Gray-row pair is symmetric about a half-integer centre, because l + 1 = 71 or 77 is not a sum of two squares (Kumar, NOTES.md section 8).

statistic:
A candidate is a win only if both checkers print PASS on that exact digit string, every shift k = 1..69 has PAF sum equal to -2+0i, entries are in {0,1,2,3}, and length is 70. A partial win is only an exhaustive empty result for a family named here before the search, with the range stated as exact counts from the program's output. A tie cannot occur: there is no published pair at 70 to match. A near miss, a capped search, or an empty reversible all-centres-at-0 family is not a win and not p1.

thresholds:
- solution: both independent checkers PASS, length 70, exact -2+0i at all 69 nonzero shifts
- p1: the named family finishes with pairs_found = 0, skipped = 0, and the log states the subgroup or centre and the candidate count
- anything else: nothing

families named before scoring, and only these may be claimed as p1 if they finish empty:
- F_mult(H): both sequences constant on orbits of H, for each subgroup H of (Z/70Z)* that does not contain -1 and is not {1}. Lebedev's reversible queue is not this family.
- F_one_centre(H, c=0): Gray rows p, q symmetric about integer centre 0, Gray rows r, s not required to be symmetric, and all four rows constant on orbits of the same H as above. Claimed only if the program finishes the whole cartesian product.

Not claimed as p1 even if empty: H containing -1 (inside the published reversible shape), the half-integer-centre family (short necessary condition, 71 not a sum of two squares), and any search that hits its time cap.

null_test: not needed because an explicit pair, or an exhaustive empty family, is judged by a deterministic Gaussian-integer checker against the bank criterion, not by a score against chance.

baseline: not applicable. The criterion is an explicit object checked by a deterministic checker, not a score on a dataset. No published baseline code is being compared. Step 3c does not apply.

arXiv API note, not a change of criterion: the export.arxiv.org query returned HTTP 429 and was not retried. No solution_claim will be written unless a later fresh search, not a retry of that blocked request, is actually read. An empty family does not need that search to be reported as a negative result.
