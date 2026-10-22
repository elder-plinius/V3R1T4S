# Criterion report: code-25-6-11-8720

context: Claude Code subagent, fresh context [Sonnet 5.5]

Role: criterion skeptic. Cell A(25,6,11), claim M = 8720. Read only the package; one live fetch of Andw.html (2026-10-18T17:54:36Z, HTTP 200, sha256 15b15c8df1a507e2403b84b322dfb2268f16c8597794b9ece23dd03532513349, same as the author's recorded fetch, so the table is unchanged since the author's check). The contributor's hash list: all 10 files verified OK.

## Criterion clauses, checked literally
- Explicit list of M distinct binary vectors: met. Own script (fresh, not the author's) read the object file: 8720 non-empty lines, each a 0/1 string of length 25, all distinct (set of ints has size 8720).
- Each has Hamming weight exactly 11: met (count of ones per line checked for every line).
- All pairwise distances >= 6, d even: met. Exhaustive all-pairs XOR popcount (no sampling); minimum distance found = 6. d = 6 is even.
- M strictly greater than the lower bound shown in the (n,d,w) cell at verification time: met. Live cell text for (25,6,11) = "8718Pl-24630" i.e. lower bound 8718, upper bound 24630; M = 8720 > 8718, margin 2. Direction is max, so larger is better: correct direction.
- Mirror cell A(25,6,14): met (nothing to beat). The page has no cell for it (checked with the parser; it prints None). By complement symmetry the mirror equals this cell, so the same comparison applies.
- Strictly greater than any value for the cell in arXiv:2608.13906, arXiv:2607.19550 or newer arXiv: cannot be decided from the folder. The README gives the author's stated paper value for this cell, which is below the table value, so it is below M if true; I did not fetch the papers and newer arXiv papers are not checked here (novelty skeptic's job).
- M must not exceed the tabulated upper bound: met. 8720 <= 24630.
- Table-implied lower bound (null model: monotonicity A(n,d,w) >= A(n-1,d,w), A(n-1,d,w-1), A(n,d+2,w)) from neighbour cells on the same live page: [((24, 6, 11), '5376BJLÖ-14682'), ((24, 6, 10), '4237-12186'), ((25, 8, 11), '1722E-3422S')]. The maximum of the neighbours and the printed cell is 8718, so no implied bound reaches M; M beats the table-implied bound too.
- Hidden quantifiers or stretched definitions: none found. The object is a plain constant-weight code at the stated n, d, w; no padding, no weight change, no relabelling of the cell. Format requirement (explicit list) is met by the object file. Partial wins p1 and p2 are not used; this is the full criterion (new lower bound).
- Caveat: the printed lower bound carries label Pl (a code from this project's own merged family), so the win is over the table as printed, which is what the criterion states.

Own checker output (script written from scratch, not shipped in this package), line for this cell:
code-25-6-11-8720 lines 8720 M 8720 fmt/weight True distinct True mind 6 cell 8718Pl-24630 lb 8718 ub 24630 M>lb True M<=ub True neighbour-implied 8718 [((24, 6, 11), '5376BJLÖ-14682'), ((24, 6, 10), '4237-12186'), ((25, 8, 11), '1722E-3422S')]

confirmed_scope: A word list of 8720 distinct binary words of length 25, weight exactly 11 and minimum pairwise distance 6 (>= 6, d even) was verified exactly, so A(25,6,11) >= 8720, strictly above the lower bound 8718 printed in that cell of Andw.html as fetched 2026-10-18T17:54:36Z (page sha256 15b15c8df1a507e2403b84b322dfb2268f16c8597794b9ece23dd03532513349, identical to the author's fetch) and below the printed upper bound 24630; the page has no mirror cell A(25,6,14); comparison with the arXiv papers rests on the author's stated lower values and was not re-checked here.
pass: true
