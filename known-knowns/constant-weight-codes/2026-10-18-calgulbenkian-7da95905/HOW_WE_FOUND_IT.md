contributor text, unverified

# How A(45,8,7) >= 1913 was found

The brief was to beat the lower bounds printed in A. E. Brouwer's table of binary constant-weight codes. The contributor's AI search agent (Argon, a Gemini-based agent) took the code the table already lists for this cell (1907, from the merged V3R1T4S bigger-codes family) and ran a large-neighbourhood search on it: remove a connected cluster of words, then refill the gap exactly with a maximum independent set solved by bit-parallel branch and bound, and keep swaps that gain words or keep the size. Its main trick, as the run's own results file describes it, was to relabel the coordinates in descending order of how often each is a one in the seed code before ranking words, which breaks ties differently and exposed improvements where earlier runs had stopped.

The contributor had earlier filed 1910 words for this cell (pull request #58, closed unmerged); this search pushed it to 1913. The snapshot's results/codes_search/ folder holds intermediate improvements of this cell with sizes 1911, 1912, 1913.

What failed or what was tried first is not recorded in the snapshot beyond that. How the object was checked is independent of this story: see `verify-it-yourself/`.
