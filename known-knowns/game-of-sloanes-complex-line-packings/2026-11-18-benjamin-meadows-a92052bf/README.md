# game-of-sloanes-complex-line-packings, (3, 38): coherence 0.7718841532949353

## What

38 unit vectors in C^3 (object/3x38_bmea.txt) with coherence mu = 0.77188415329493526906 (exact integer arithmetic with a 60-digit square root; mpmath at 40 or more digits), lower than the Game of Sloanes leaderboard Best Coherence 0.77189089 for (d, n) = (3, 38) by 6.74e-06; the row is not marked provably optimal, mu is above the listed lower bound 0.67612340, every coordinate is written with at least 16 significant digits, and mu is also at least 1e-7 below every packing for this cell in the open pull requests to the leaderboard repository other than our own pull request 20 (lowest: 0.7718851788436402 in pull request 18, 0.7718878985284835 in pull request 14).

This package contains one object only: object/3x38_bmea.txt, in the leaderboard's file format (2dn numbers, one per line: the real parts of all 38 vectors, vector by vector, then the imaginary parts).

## Check it yourself

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. Python 3 standard library; under a second on a laptop. It checks the object's sha256, the count of numbers and the digits per coordinate, recomputes the coherence from the definition with exact integers, and compares it with the claimed value, the leaderboard value and the lower bound, and with the lowest coherence among the other open pull requests for this cell. Details: RUN_IT_YOURSELF.md.

## Compared to

| source | cell | coherence | URL | fetched (UTC) |
|---|---|---|---|---|
| Game of Sloanes leaderboard | (d, n) = (3, 38) | 0.77189089 | https://raw.githubusercontent.com/gnikylime/GameofSloanes/main/README.md | 2026-11-18T00:23:25Z |
| posted packing for the row (bmem) | (3, 38) | 0.7718908927 (recomputed) | https://raw.githubusercontent.com/gnikylime/GameofSloanes/main/CurrentBestPackings/3x38_bmem.txt | 2026-11-18T00:23:28Z |
| open pull request 18 (owhs) | (3, 38) | 0.7718851788 (recomputed) | https://github.com/gnikylime/GameofSloanes/raw/b0f64bccff9751542f9cb0803131542e37cb75e5/SubmittedPackings%2F3x38_owhs.txt | 2026-11-18T00:24:24Z |
| open pull request 14 (dustinmixon) | (3, 38) | 0.7718878985 (recomputed) | https://github.com/gnikylime/GameofSloanes/raw/04831504e5e74f42ca6742315a2eb2366503a10a/SubmittedPackings%2F3x38_sol.txt | 2026-11-18T00:24:05Z |

Details in the-record-we-beat/.

## Not claimed

- Not an optimal packing, only one with a lower coherence than the leaderboard row; the listed lower bound 0.67612340 is 0.0958 below mu.
- Only (3, 38). Other cells from the same searches are in packing-records and in pull request 20; each cell we claim here has its own package.
- Not new to the public record today: the same packing is in packing-records version 1.0.0 (https://github.com/TheBenMeadows/packing-records, https://doi.org/10.5281/zenodo.23906182, released 2026-11-02) and in pull request 20 to the leaderboard repository (https://github.com/gnikylime/GameofSloanes/pull/20, opened 2026-11-03, open and unmerged; the repository has had no commit since 2026-04-28).

## Credits

- John Jasper, Emily J. King and Dustin G. Mixon, the Game of Sloanes leaderboard, https://github.com/gnikylime/GameofSloanes (arXiv:1907.07848, https://arxiv.org/abs/1907.07848)
- Bastien Massion and Estelle Massart, the posted (3, 38) packing the leaderboard lists (https://raw.githubusercontent.com/gnikylime/GameofSloanes/main/CurrentBestPackings/3x38_bmem.txt, sha256 c0ce6c4ab12d9d4fe8c9f1781d1fc7a5bac6107ec64c5ceb36cf61891fe14686), which we compared against; it was not a starting point
- owhs, pull request 18 to the leaderboard repository (https://github.com/gnikylime/GameofSloanes/pull/18), file 3x38_owhs.txt, which we compared against
- dustinmixon, pull request 14 to the leaderboard repository (https://github.com/gnikylime/GameofSloanes/pull/14), file 3x38_sol.txt, which we compared against
- Benjamin Meadows (search, checking and packaging).
