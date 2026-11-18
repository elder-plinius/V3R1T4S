# game-of-sloanes-complex-line-packings, (4, 29): coherence 0.5773298205869568

## What

29 unit vectors in C^4 (object/4x29_bmea.txt) with coherence mu = 0.57732982058695676154 (exact integer arithmetic with a 60-digit square root; mpmath at 40 or more digits), lower than the Game of Sloanes leaderboard Best Coherence 0.57733882 for (d, n) = (4, 29) by 9e-06; the row is not marked provably optimal, mu is above the listed lower bound 0.55136195, every coordinate is written with at least 16 significant digits, and mu is also at least 1e-7 below every packing for this cell in the open pull requests to the leaderboard repository other than our own pull request 20 (lowest: 0.5773373993891876 in pull request 18).

This package contains one object only: object/4x29_bmea.txt, in the leaderboard's file format (2dn numbers, one per line: the real parts of all 29 vectors, vector by vector, then the imaginary parts).

## Check it yourself

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. Python 3 standard library; under a second on a laptop. It checks the object's sha256, the count of numbers and the digits per coordinate, recomputes the coherence from the definition with exact integers, and compares it with the claimed value, the leaderboard value and the lower bound, and with the lowest coherence among the other open pull requests for this cell. Details: RUN_IT_YOURSELF.md.

## Compared to

| source | cell | coherence | URL | fetched (UTC) |
|---|---|---|---|---|
| Game of Sloanes leaderboard | (d, n) = (4, 29) | 0.57733882 | https://raw.githubusercontent.com/gnikylime/GameofSloanes/main/README.md | 2026-11-18T00:23:25Z |
| posted packing for the row (hlc) | (4, 29) | 0.5773388158 (recomputed) | https://raw.githubusercontent.com/gnikylime/GameofSloanes/main/CurrentBestPackings/4x29_hlc.txt | 2026-11-18T00:23:32Z |
| open pull request 18 (owhs) | (4, 29) | 0.5773373993 (recomputed) | https://github.com/gnikylime/GameofSloanes/raw/b0f64bccff9751542f9cb0803131542e37cb75e5/SubmittedPackings%2F4x29_owhs.txt | 2026-11-18T00:24:29Z |

Details in the-record-we-beat/.

## Not claimed

- Not an optimal packing, only one with a lower coherence than the leaderboard row; the listed lower bound 0.55136195 is 0.026 below mu.
- Only (4, 29). Other cells from the same searches are in packing-records and in pull request 20; each cell we claim here has its own package.
- Not new to the public record today: the same packing is in packing-records version 1.0.0 (https://github.com/TheBenMeadows/packing-records, https://doi.org/10.5281/zenodo.23906182, released 2026-11-02) and in pull request 20 to the leaderboard repository (https://github.com/gnikylime/GameofSloanes/pull/20, opened 2026-11-03, open and unmerged; the repository has had no commit since 2026-04-28).

## Credits

- John Jasper, Emily J. King and Dustin G. Mixon, the Game of Sloanes leaderboard, https://github.com/gnikylime/GameofSloanes (arXiv:1907.07848, https://arxiv.org/abs/1907.07848)
- Henry Cohn, the posted (4, 29) packing the leaderboard lists (https://raw.githubusercontent.com/gnikylime/GameofSloanes/main/CurrentBestPackings/4x29_hlc.txt, sha256 f3116a427d8681cb81dc8ecdab0b5972cf92bfb239a683c28ccbc323e9f8a217), which we compared against; it was not a starting point
- owhs, pull request 18 to the leaderboard repository (https://github.com/gnikylime/GameofSloanes/pull/18), file 4x29_owhs.txt, which we compared against
- Benjamin Meadows (search, checking and packaging).
