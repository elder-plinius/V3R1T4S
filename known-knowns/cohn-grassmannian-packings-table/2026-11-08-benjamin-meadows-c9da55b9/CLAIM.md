# Claim: cohn-grassmannian-packings-table, cell 11-1-62

Object: `object/11-1-62.txt` (sha256 c9da55b9f9cfe7a4711ded4bae4c1f46700366b616fa820fd31e794eba3bb9d2).

Claimed: N = 62 one-dimensional subspaces of R^11 (lines; m = 11, n = 1) whose minimum squared chordal distance is higher than the table value for (m, n, N) = (11, 1, 62). Claimed value about 0.88917055455047; the table value read 2026-11-07 is 0.8891152435.

Success criterion (V3R1T4S bank target cohn-grassmannian-packings-table, quoted verbatim):

> Success means N matrices U_i (m x n, >= 20 significant digits) for an UNSTARRED (m, n, N) row of the live table at https://cohn.mit.edu/grassmannian (re-fetched immediately before claiming) whose note does not say 'optimal packing' or 'proof of optimality', such that after orthonormalising each U_i in mpmath at 50 digits, the minimum over i < j of n - ||U_i^T U_j||_F^2 is STRICTLY GREATER (direction: max) than the table's squared chordal distance for (m, n, N) by at least 1e-9. It must also not exceed the row's listed bound by more than 1e-10 (a larger value means a bug). And no value for (m, n, N) published after the table's last change, found in an arXiv search (Grassmannian / line packing / fusion frame with m, n, N), is larger.

The bank's verification method:

> Checker (seconds): parse the vectors (the first n lines span subspace 1, and so on), orthonormalise each block by QR in mpmath, compute all pairwise n - ||U_i^T U_j||_F^2, and take the minimum. Compare it with the live row (10 decimals, rounded down) and its bound. Reproduce the posted file for the row first.

Live sources (fetch them yourself):

- https://cohn.mit.edu/grassmannian (the table: value, bound, star, note per row)
- arXiv search for "Grassmannian packing" / "line packing" / "fusion frame", for example http://export.arxiv.org/api/query?search_query=all:%22Grassmannian+packing%22&sortBy=submittedDate&max_results=15
- Prior claims: open, merged and closed pull requests at https://github.com/elder-plinius/V3R1T4S for target cohn-grassmannian-packings-table, and TROPHY_CASE.md on its main branch.
