# Claim: game-of-sloanes-complex-line-packings, cell (d, n) = (5, 36)

Object: `object/5x36_bmea.txt` (sha256 8f47404a6ab8b0baa40e1a24d3a9fc5a968aa21da1bafc97ed89bb2bdfa69896).

Claimed: n = 36 unit vectors in C^5 whose coherence, after normalising each vector, is lower than the Game of Sloanes leaderboard's Best Coherence for (d, n) = (5, 36). Claimed value about 0.49920080365459; the leaderboard value read 2026-11-19T05:00:43Z is 0.49998890 (creator code AUTO). This is claimed as a win.

The object is also lower by at least 1e-7 than every packing for this cell in the open pull requests to the leaderboard repository (read 2026-11-19T05:00:45Z). That is a stricter bar we set ourselves; the bank criterion below compares with the README table only.

Starting point: the object descends from the (5, 37) packing in open pull request 15 to the leaderboard repository (author djma, file 5x37_djma.txt, https://github.com/gnikylime/GameofSloanes/raw/6f4a1bd2b3c14f0dee6d4cb52eafca77eb794b9c/SubmittedPackings%2F5x37_djma.txt, sha256 c7eeddfa7fd7028d353a0c5d5e3271df4b9067453c8f809d657e1c5643eb637d, coherence 0.499552981708) with one vector removed. Open pull request 17 (author JosiahPark, file 5x37_grai.txt, https://github.com/gnikylime/GameofSloanes/raw/134bb4bd8ef2d433f5a24a0bf8227fc98855607d/CurrentBestPackings%2F5x37_grai.txt, sha256 f21c4d6c281b1577e8efd392e75fdb422dd545af53aab330d61e4ec7e8877cf1) holds the same (5, 37) packing in the same vector order, slightly polished (coherence 0.499552163073); the search was given both files. After the removal the search continued with basin hops (complex noise, then descent) and a sequential linear-programming polish. The object was not started from any (5, 36) packing.

Success criterion (V3R1T4S bank target game-of-sloanes-complex-line-packings, quoted verbatim):

> Success means n unit vectors in C^d, 3 <= d <= 7, for a (d,n) row of the live leaderboard (https://github.com/gnikylime/GameofSloanes README table, re-fetched live immediately before claiming) whose coherence mu = max_{j<k} |<phi_j,phi_k>|, computed in mpmath at 40 digits after normalising each vector, is STRICTLY LOWER (direction: min) than the listed 'Best Coherence' by at least 1e-8 (the table's resolution and the maintainers' stated acceptance threshold), the row is not marked provably optimal, mu is at least the listed lower bound (a value below it means a bug), and the vectors are given to >= 16 significant digits in the repository's file format (real parts of all vectors vector-by-vector, then imaginary parts).

Partial win p1, quoted verbatim:

> A strict improvement (same rules) for a sporadic (d,n) outside the d <= 7, n <= 49 grid where the leaderboard lists an entry, or for a d = 3..7 row that matches a known lower bound to 1e-10 (a new putatively optimal packing, reported with the bound it meets).

The bank's verification method:

> Download the claimed .txt (2dn numbers), reshape as vectors[j] = re[j*d:(j+1)*d] + i*im[j*d:(j+1)*d] (this layout reproduces the posted coherences, checked on 3x13_dgm and 4x9_hlc on 2026-10-15), normalise in mpmath, compute all n(n-1)/2 overlaps, take the max. Parse the live README table row for (d,n) and compare. Also recompute the posted file for that row to make sure the comparison uses the same convention. Under a minute for n <= 49.

Live sources (fetch them yourself):

- https://github.com/gnikylime/GameofSloanes (README table; posted files under CurrentBestPackings/; raw README at https://raw.githubusercontent.com/gnikylime/GameofSloanes/main/README.md)
- Open pull requests to that repository: https://github.com/gnikylime/GameofSloanes/pulls
- Prior claims: open, merged and closed pull requests at https://github.com/elder-plinius/V3R1T4S for target game-of-sloanes-complex-line-packings, and TROPHY_CASE.md on its main branch.
