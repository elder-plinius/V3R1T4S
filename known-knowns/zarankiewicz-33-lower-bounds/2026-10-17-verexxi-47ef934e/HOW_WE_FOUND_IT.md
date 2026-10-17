# How we found it (contributor text, unverified)

Method: a plain local search, no public matrix as input. Start from a random greedy fill of the 16 x 19 grid. Then repeat: remove 1 to 6
random ones, refill every zero cell that keeps the matrix free of an all-ones 3 x 3 submatrix (in random order), and keep the result
if the number of ones did not drop. Restart after a long stall. The saved matrix came from a 20-second run of
how-we-built-it/search/initial_program_ls.py (the short form of the search, found in an earlier session); the seed was not recorded, so
that exact file is not re-found by a command.

What a rerun shows: six fresh runs of how-we-built-it/search/zsearch.py (seeds 101 to 106, 10 minutes each, one core each) all reached
142, the first after about 16 seconds and the last after about 3 minutes 15 seconds. None reached 143. One of the six matrices is the
same as the claimed one up to row and column permutations. So 142 is easy to reach with this search; we do not know whether 143 exists.

What we tried to break it with:
- An independent checker (column triples and a literal test of every set of 3 rows and 3 columns) found no violation. All 162
  single-cell flips from 0 to 1 create one, so no cell can be added.
- Trivial derivations of public matrices (the repository's policy says those are not records): delete the lightest rows and columns of
  each of the 12 public witness matrices, add the best admissible line, fill greedily. 192000 runs reached at best 141 (66663 runs) and
  never 142. This is a bounded sample of one family of derivations, evidence and not proof.
- No sub-matrix of the object is an exact copy of any of the 10 public matrices that fit in 16 x 19.
- Closing the published numbers by the elementary rules gives 139 for the cell.

What failed or was left: no search for 143 beyond the plain method (six 10-minute runs). Ideas not run: exact line extension of
sub-matrices of the object, warm starts from public witnesses, SAT or ILP completion, cyclic-symmetry search.

Status pages: the scout that produced the table values was written 2026-10-17 without web access; a separate reviewer then read the
arXiv page and the Afrasyab table once (the-record-we-beat/RECORD.md).
