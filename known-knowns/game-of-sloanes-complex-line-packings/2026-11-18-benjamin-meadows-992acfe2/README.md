# game-of-sloanes-complex-line-packings, (7, 19): coherence 0.3088364002013680

## What

19 unit vectors in C^7 (object/7x19_bmea.txt) with coherence mu = 0.30883640020136799853 (exact integer arithmetic with a 60-digit square root; mpmath at 40 or more digits), lower than the Game of Sloanes leaderboard Best Coherence 0.30884718 for (d, n) = (7, 19) by 1.08e-05; the row is not marked provably optimal, mu is above the listed lower bound 0.30860670, every coordinate is written with at least 16 significant digits, and no open pull request to the leaderboard repository other than our own pull request 20 has a packing for this cell.

This package contains one object only: object/7x19_bmea.txt, in the leaderboard's file format (2dn numbers, one per line: the real parts of all 19 vectors, vector by vector, then the imaginary parts).

## Check it yourself

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. Python 3 standard library; under a second on a laptop. It checks the object's sha256, the count of numbers and the digits per coordinate, recomputes the coherence from the definition with exact integers, and compares it with the claimed value, the leaderboard value and the lower bound. Details: RUN_IT_YOURSELF.md.

## Compared to

| source | cell | coherence | URL | fetched (UTC) |
|---|---|---|---|---|
| Game of Sloanes leaderboard | (d, n) = (7, 19) | 0.30884718 | https://raw.githubusercontent.com/gnikylime/GameofSloanes/main/README.md | 2026-11-18T00:23:25Z |
| posted packing for the row (hlc) | (7, 19) | 0.3088471825 (recomputed) | https://raw.githubusercontent.com/gnikylime/GameofSloanes/main/CurrentBestPackings/7x19_hlc.txt | 2026-11-18T00:23:42Z |

Details in the-record-we-beat/.

## Not claimed

- Not an optimal packing, only one with a lower coherence than the leaderboard row; the listed lower bound 0.30860670 is 0.00023 below mu.
- Only (7, 19). Other cells from the same searches are in packing-records and in pull request 20; each cell we claim here has its own package.
- Not new to the public record today: the same packing is in packing-records version 1.0.0 (https://github.com/TheBenMeadows/packing-records, https://doi.org/10.5281/zenodo.23906182, released 2026-11-02) and in pull request 20 to the leaderboard repository (https://github.com/gnikylime/GameofSloanes/pull/20, opened 2026-11-03, open and unmerged; the repository has had no commit since 2026-04-28).

## Credits

- John Jasper, Emily J. King and Dustin G. Mixon, the Game of Sloanes leaderboard, https://github.com/gnikylime/GameofSloanes (arXiv:1907.07848, https://arxiv.org/abs/1907.07848)
- Henry Cohn, the posted (7, 19) packing the leaderboard lists (https://raw.githubusercontent.com/gnikylime/GameofSloanes/main/CurrentBestPackings/7x19_hlc.txt, sha256 da6c93125d8b856b694e6dc2a1090714a677d7244e628ea05057152aebcfe675), which we compared against; it was not a starting point
- Benjamin Meadows (search, checking and packaging).
