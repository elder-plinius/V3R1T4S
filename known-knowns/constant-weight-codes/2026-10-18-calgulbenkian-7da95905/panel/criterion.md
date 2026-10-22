# Criterion report: code-45-8-7-1913

context: Claude Code subagent, fresh context [Sonnet 5.5]

Role: criterion skeptic. Cell A(45,8,7), claim M = 1913. Read only the package; one live fetch of Andw.html (2026-10-18T17:54:36Z, HTTP 200, sha256 15b15c8df1a507e2403b84b322dfb2268f16c8597794b9ece23dd03532513349, same as the author's recorded fetch, so the table is unchanged since the author's check). The contributor's hash list: all 10 files verified OK.

## Criterion clauses, checked literally
- Explicit list of M distinct binary vectors: met. Own script (fresh, not the author's) read the object file: 1913 non-empty lines, each a 0/1 string of length 45, all distinct (set of ints has size 1913).
- Each has Hamming weight exactly 7: met (count of ones per line checked for every line).
- All pairwise distances >= 8, d even: met. Exhaustive all-pairs XOR popcount (no sampling); minimum distance found = 8. d = 8 is even.
- M strictly greater than the lower bound shown in the (n,d,w) cell at verification time: met. Live cell text for (45,8,7) = "1907Pl-4050" i.e. lower bound 1907, upper bound 4050; M = 1913 > 1907, margin 6. Direction is max, so larger is better: correct direction.
- Mirror cell A(45,8,38): met (nothing to beat). The page has no cell for it (checked with the parser; it prints None). By complement symmetry the mirror equals this cell, so the same comparison applies.
- Strictly greater than any value for the cell in arXiv:2608.13906, arXiv:2607.19550 or newer arXiv: cannot be decided from the folder. The README gives the author's stated paper value for this cell, which is below the table value, so it is below M if true; I did not fetch the papers and newer arXiv papers are not checked here (novelty skeptic's job).
- M must not exceed the tabulated upper bound: met. 1913 <= 4050.
- Table-implied lower bound (null model: monotonicity A(n,d,w) >= A(n-1,d,w), A(n-1,d,w-1), A(n,d+2,w)) from neighbour cells on the same live page: [((44, 8, 7), '1806g-3784'), ((44, 8, 6), '475Bo-630'), ((45, 10, 7), '293E-372')]. The maximum of the neighbours and the printed cell is 1907, so no implied bound reaches M; M beats the table-implied bound too.
- Hidden quantifiers or stretched definitions: none found. The object is a plain constant-weight code at the stated n, d, w; no padding, no weight change, no relabelling of the cell. Format requirement (explicit list) is met by the object file. Partial wins p1 and p2 are not used; this is the full criterion (new lower bound).
- Caveat: the printed lower bound carries label Pl (a code from this project's own merged family), so the win is over the table as printed, which is what the criterion states.

Own checker output (script written from scratch, not shipped in this package), line for this cell:
code-45-8-7-1913 lines 1913 M 1913 fmt/weight True distinct True mind 8 cell 1907Pl-4050 lb 1907 ub 4050 M>lb True M<=ub True neighbour-implied 1907 [((44, 8, 7), '1806g-3784'), ((44, 8, 6), '475Bo-630'), ((45, 10, 7), '293E-372')]

confirmed_scope: A word list of 1913 distinct binary words of length 45, weight exactly 7 and minimum pairwise distance 8 (>= 8, d even) was verified exactly, so A(45,8,7) >= 1913, strictly above the lower bound 1907 printed in that cell of Andw.html as fetched 2026-10-18T17:54:36Z (page sha256 15b15c8df1a507e2403b84b322dfb2268f16c8597794b9ece23dd03532513349, identical to the author's fetch) and below the printed upper bound 4050; the page has no mirror cell A(45,8,38); comparison with the arXiv papers rests on the author's stated lower values and was not re-checked here.
pass: true
