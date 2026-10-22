# Criterion report: code-51-6-6-11187

context: Claude Code subagent, fresh context [Sonnet 5.5]

Role: criterion skeptic. Cell A(51,6,6), claim M = 11187. Read only the package; one live fetch of Andw.html (2026-10-18T17:54:36Z, HTTP 200, sha256 15b15c8df1a507e2403b84b322dfb2268f16c8597794b9ece23dd03532513349, same as the author's recorded fetch, so the table is unchanged since the author's check). The contributor's hash list: all 10 files verified OK.

## Criterion clauses, checked literally
- Explicit list of M distinct binary vectors: met. Own script (fresh, not the author's) read the object file: 11187 non-empty lines, each a 0/1 string of length 51, all distinct (set of ints has size 11187).
- Each has Hamming weight exactly 6: met (count of ones per line checked for every line).
- All pairwise distances >= 6, d even: met. Exhaustive all-pairs XOR popcount (no sampling); minimum distance found = 6. d = 6 is even.
- M strictly greater than the lower bound shown in the (n,d,w) cell at verification time: met. Live cell text for (51,6,6) = "11184Pl-16660" i.e. lower bound 11184, upper bound 16660; M = 11187 > 11184, margin 3. Direction is max, so larger is better: correct direction.
- Mirror cell A(51,6,45): met (nothing to beat). The page has no cell for it (checked with the parser; it prints None). By complement symmetry the mirror equals this cell, so the same comparison applies.
- Strictly greater than any value for the cell in arXiv:2608.13906, arXiv:2607.19550 or newer arXiv: cannot be decided from the folder. The README gives the author's stated paper value for this cell, which is below the table value, so it is below M if true; I did not fetch the papers and newer arXiv papers are not checked here (novelty skeptic's job).
- M must not exceed the tabulated upper bound: met. 11187 <= 16660.
- Table-implied lower bound (null model: monotonicity A(n,d,w) >= A(n-1,d,w), A(n-1,d,w-1), A(n,d+2,w)) from neighbour cells on the same live page: [((50, 6, 6), '10825-14700'), ((50, 6, 5), '1688Bo-1960'), ((51, 8, 6), '727Bo-1020')]. The maximum of the neighbours and the printed cell is 11184, so no implied bound reaches M; M beats the table-implied bound too.
- Hidden quantifiers or stretched definitions: none found. The object is a plain constant-weight code at the stated n, d, w; no padding, no weight change, no relabelling of the cell. Format requirement (explicit list) is met by the object file. Partial wins p1 and p2 are not used; this is the full criterion (new lower bound).
- Caveat: the printed lower bound carries label Pl (a code from this project's own merged family), so the win is over the table as printed, which is what the criterion states.

Own checker output (script written from scratch, not shipped in this package), line for this cell:
code-51-6-6-11187 lines 11187 M 11187 fmt/weight True distinct True mind 6 cell 11184Pl-16660 lb 11184 ub 16660 M>lb True M<=ub True neighbour-implied 11184 [((50, 6, 6), '10825-14700'), ((50, 6, 5), '1688Bo-1960'), ((51, 8, 6), '727Bo-1020')]

confirmed_scope: A word list of 11187 distinct binary words of length 51, weight exactly 6 and minimum pairwise distance 6 (>= 6, d even) was verified exactly, so A(51,6,6) >= 11187, strictly above the lower bound 11184 printed in that cell of Andw.html as fetched 2026-10-18T17:54:36Z (page sha256 15b15c8df1a507e2403b84b322dfb2268f16c8597794b9ece23dd03532513349, identical to the author's fetch) and below the printed upper bound 16660; the page has no mirror cell A(51,6,45); comparison with the arXiv papers rests on the author's stated lower values and was not re-checked here.
pass: true
