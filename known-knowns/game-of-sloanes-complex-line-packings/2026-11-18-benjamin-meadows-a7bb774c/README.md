# game-of-sloanes-complex-line-packings, (3, 46): coherence 0.7942836704171086

## What

46 unit vectors in C^3 (object/3x46_bmea.txt) with coherence mu = 0.79428367041710855504 (exact integer arithmetic with a 60-digit square root; mpmath at 40 or more digits), lower than the Game of Sloanes leaderboard Best Coherence 0.79435710 for (d, n) = (3, 46) by 7.34e-05; the row is not marked provably optimal, mu is above the listed lower bound 0.70511609, every coordinate is written with at least 16 significant digits, and mu is also at least 1e-7 below every packing for this cell in the open pull requests to the leaderboard repository other than our own pull request 20 (lowest: 0.7943115897298045 in pull request 18).

This package contains one object only: object/3x46_bmea.txt, in the leaderboard's file format (2dn numbers, one per line: the real parts of all 46 vectors, vector by vector, then the imaginary parts).

## Check it yourself

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. Python 3 standard library; under a second on a laptop. It checks the object's sha256, the count of numbers and the digits per coordinate, recomputes the coherence from the definition with exact integers, and compares it with the claimed value, the leaderboard value and the lower bound, and with the lowest coherence among the other open pull requests for this cell. Details: RUN_IT_YOURSELF.md.

## Compared to

| source | cell | coherence | URL | fetched (UTC) |
|---|---|---|---|---|
| Game of Sloanes leaderboard | (d, n) = (3, 46) | 0.79435710 | https://raw.githubusercontent.com/gnikylime/GameofSloanes/main/README.md | 2026-11-18T00:23:25Z |
| posted packing for the row (hlc) | (3, 46) | 0.7943571030 (recomputed) | https://raw.githubusercontent.com/gnikylime/GameofSloanes/main/CurrentBestPackings/3x46_hlc.txt | 2026-11-18T00:23:30Z |
| open pull request 18 (owhs) | (3, 46) | 0.7943115897 (recomputed) | https://github.com/gnikylime/GameofSloanes/raw/b0f64bccff9751542f9cb0803131542e37cb75e5/SubmittedPackings%2F3x46_owhs.txt | 2026-11-18T00:24:26Z |

Details in the-record-we-beat/.

## Not claimed

- Not an optimal packing, only one with a lower coherence than the leaderboard row; the listed lower bound 0.70511609 is 0.0892 below mu.
- Only (3, 46). Other cells from the same searches are in packing-records and in pull request 20; each cell we claim here has its own package.
- Not new to the public record today: the same packing is in packing-records version 1.0.0 (https://github.com/TheBenMeadows/packing-records, https://doi.org/10.5281/zenodo.23906182, released 2026-11-02) and in pull request 20 to the leaderboard repository (https://github.com/gnikylime/GameofSloanes/pull/20, opened 2026-11-03, open and unmerged; the repository has had no commit since 2026-04-28).

## Credits

- John Jasper, Emily J. King and Dustin G. Mixon, the Game of Sloanes leaderboard, https://github.com/gnikylime/GameofSloanes (arXiv:1907.07848, https://arxiv.org/abs/1907.07848)
- Henry Cohn, the posted (3, 46) packing the leaderboard lists (https://raw.githubusercontent.com/gnikylime/GameofSloanes/main/CurrentBestPackings/3x46_hlc.txt, sha256 27074b61cee57c069fcc2473d2c9553cadfd442388b3a018d48d753d79bea428), which we compared against; it was not a starting point
- owhs, pull request 18 to the leaderboard repository (https://github.com/gnikylime/GameofSloanes/pull/18), file 3x46_owhs.txt, which we compared against
- Benjamin Meadows (search, checking and packaging).
