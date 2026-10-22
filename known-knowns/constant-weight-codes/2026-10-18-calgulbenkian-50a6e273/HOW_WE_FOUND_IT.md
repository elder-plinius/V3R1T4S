contributor text, unverified

# How A(55,8,7) >= 4432 was found

The brief was to beat the lower bounds printed in A. E. Brouwer's table of binary constant-weight codes. The contributor's AI search agent (Argon, a Gemini-based agent) took the code the table already lists for this cell (4426, from the merged V3R1T4S bigger-codes family) and ran a large-neighbourhood search on it: remove a connected cluster of words, then refill the gap exactly with a maximum independent set solved by bit-parallel branch and bound, and keep swaps that gain words or keep the size. Its main trick, as the run's own results file describes it, was to relabel the coordinates in descending order of how often each is a one in the seed code before ranking words, which breaks ties differently and exposed improvements where earlier runs had stopped.

The contributor had earlier filed 4431 words for this cell (pull request #55, closed unmerged); this search pushed it to 4432. The snapshot's results/codes_search/ folder holds intermediate improvements of this cell with sizes 4432.

What failed or what was tried first is not recorded in the snapshot beyond that. How the object was checked is independent of this story: see `verify-it-yourself/`.
