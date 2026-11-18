# Claim: game-of-sloanes-complex-line-packings, cell (d, n) = (7, 32)

Object: `object/7x32_bmea.txt` (sha256 11bda03625dc3308f02b8a4a971e7d0c8431df695828a37e3e4002b11c755042).

Claimed: n = 32 unit vectors in C^7 whose coherence, after normalising each vector, is lower than the Game of Sloanes leaderboard's Best Coherence for (d, n) = (7, 32). Claimed value about 0.35220038055837; the leaderboard value read 2026-11-18T00:23:25Z is 0.35229897 (creator code jrr). This is claimed as a win.

The object is also lower by at least 1e-7 than every packing for this cell in the open pull requests to the leaderboard repository (read 2026-11-18T00:23:11Z). That is a stricter bar we set ourselves; the bank criterion below compares with the README table only.

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
