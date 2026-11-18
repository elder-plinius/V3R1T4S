# game-of-sloanes-complex-line-packings, (6, 24): coherence 0.3696053676390932

## What

24 unit vectors in C^6 (object/6x24_bmea.txt) with coherence mu = 0.36960536763909315599 (exact integer arithmetic with a 60-digit square root; mpmath at 40 or more digits), lower than the Game of Sloanes leaderboard Best Coherence 0.36998252 for (d, n) = (6, 24) by 0.000377; the row is not marked provably optimal, mu is above the listed lower bound 0.36115756, every coordinate is written with at least 16 significant digits, and mu is also at least 1e-7 below every packing for this cell in the open pull requests to the leaderboard repository other than our own pull request 20 (lowest: 0.3697027536772281 in pull request 17).

This package contains one object only: object/6x24_bmea.txt, in the leaderboard's file format (2dn numbers, one per line: the real parts of all 24 vectors, vector by vector, then the imaginary parts).

## Check it yourself

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. Python 3 standard library; under a second on a laptop. It checks the object's sha256, the count of numbers and the digits per coordinate, recomputes the coherence from the definition with exact integers, and compares it with the claimed value, the leaderboard value and the lower bound, and with the lowest coherence among the other open pull requests for this cell. Details: RUN_IT_YOURSELF.md.

## Compared to

| source | cell | coherence | URL | fetched (UTC) |
|---|---|---|---|---|
| Game of Sloanes leaderboard | (d, n) = (6, 24) | 0.36998252 | https://raw.githubusercontent.com/gnikylime/GameofSloanes/main/README.md | 2026-11-18T00:23:25Z |
| posted packing for the row (hlc) | (6, 24) | 0.3699825175 (recomputed) | https://raw.githubusercontent.com/gnikylime/GameofSloanes/main/CurrentBestPackings/6x24_hlc.txt | 2026-11-18T00:23:36Z |
| open pull request 17 (JosiahPark) | (6, 24) | 0.3697027536 (recomputed) | https://github.com/gnikylime/GameofSloanes/raw/134bb4bd8ef2d433f5a24a0bf8227fc98855607d/CurrentBestPackings%2F6x24_grai.txt | 2026-11-18T00:24:21Z |

Details in the-record-we-beat/.

## Not claimed

- Not an optimal packing, only one with a lower coherence than the leaderboard row; the listed lower bound 0.36115756 is 0.00845 below mu.
- Only (6, 24). Other cells from the same searches are in packing-records and in pull request 20; each cell we claim here has its own package.
- Not new to the public record today: the same packing is in packing-records version 1.0.0 (https://github.com/TheBenMeadows/packing-records, https://doi.org/10.5281/zenodo.23906182, released 2026-11-02) and in pull request 20 to the leaderboard repository (https://github.com/gnikylime/GameofSloanes/pull/20, opened 2026-11-03, open and unmerged; the repository has had no commit since 2026-04-28).

## Credits

- John Jasper, Emily J. King and Dustin G. Mixon, the Game of Sloanes leaderboard, https://github.com/gnikylime/GameofSloanes (arXiv:1907.07848, https://arxiv.org/abs/1907.07848)
- Henry Cohn, the posted (6, 24) packing the leaderboard lists (https://raw.githubusercontent.com/gnikylime/GameofSloanes/main/CurrentBestPackings/6x24_hlc.txt, sha256 0165a81a56d704da8c660f0a2fdc7a30805da59e8a33e32b0ad55a4462eece8f), which we compared against; it was not a starting point
- JosiahPark, pull request 17 to the leaderboard repository (https://github.com/gnikylime/GameofSloanes/pull/17), file 6x24_grai.txt, which we compared against
- Benjamin Meadows (search, checking and packaging).
