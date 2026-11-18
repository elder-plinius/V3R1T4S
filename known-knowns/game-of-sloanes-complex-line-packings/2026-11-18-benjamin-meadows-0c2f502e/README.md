# game-of-sloanes-complex-line-packings, (5, 32): coherence 0.4868147199854489

## What

32 unit vectors in C^5 (object/5x32_bmea.txt) with coherence mu = 0.48681471998544894573 (exact integer arithmetic with a 60-digit square root; mpmath at 40 or more digits), lower than the Game of Sloanes leaderboard Best Coherence 0.48688165 for (d, n) = (5, 32) by 6.69e-05; the row is not marked provably optimal, mu is above the listed lower bound 0.45812285, every coordinate is written with at least 16 significant digits, and mu is also at least 1e-7 below every packing for this cell in the open pull requests to the leaderboard repository other than our own pull request 20 (lowest: 0.4868816023864200 in pull request 19).

This package contains one object only: object/5x32_bmea.txt, in the leaderboard's file format (2dn numbers, one per line: the real parts of all 32 vectors, vector by vector, then the imaginary parts).

## Check it yourself

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. Python 3 standard library; under a second on a laptop. It checks the object's sha256, the count of numbers and the digits per coordinate, recomputes the coherence from the definition with exact integers, and compares it with the claimed value, the leaderboard value and the lower bound, and with the lowest coherence among the other open pull requests for this cell. Details: RUN_IT_YOURSELF.md.

## Compared to

| source | cell | coherence | URL | fetched (UTC) |
|---|---|---|---|---|
| Game of Sloanes leaderboard | (d, n) = (5, 32) | 0.48688165 | https://raw.githubusercontent.com/gnikylime/GameofSloanes/main/README.md | 2026-11-18T00:23:25Z |
| posted packing for the row (hlc) | (5, 32) | 0.4868816482 (recomputed) | https://raw.githubusercontent.com/gnikylime/GameofSloanes/main/CurrentBestPackings/5x32_hlc.txt | 2026-11-18T00:23:33Z |
| open pull request 19 (arhancanli) | (5, 32) | 0.4868816023 (recomputed) | https://github.com/gnikylime/GameofSloanes/raw/526507270147c45e8eb5210ea43e6e9f5f5693c7/SubmittedPackings%2F5x32_ARC.txt | 2026-11-18T00:24:41Z |

Details in the-record-we-beat/.

## Not claimed

- Not an optimal packing, only one with a lower coherence than the leaderboard row; the listed lower bound 0.45812285 is 0.0287 below mu.
- Only (5, 32). Other cells from the same searches are in packing-records and in pull request 20; each cell we claim here has its own package.
- Not new to the public record today: the same packing is in packing-records version 1.0.0 (https://github.com/TheBenMeadows/packing-records, https://doi.org/10.5281/zenodo.23906182, released 2026-11-02) and in pull request 20 to the leaderboard repository (https://github.com/gnikylime/GameofSloanes/pull/20, opened 2026-11-03, open and unmerged; the repository has had no commit since 2026-04-28).

## Credits

- John Jasper, Emily J. King and Dustin G. Mixon, the Game of Sloanes leaderboard, https://github.com/gnikylime/GameofSloanes (arXiv:1907.07848, https://arxiv.org/abs/1907.07848)
- Henry Cohn, the posted (5, 32) packing the leaderboard lists (https://raw.githubusercontent.com/gnikylime/GameofSloanes/main/CurrentBestPackings/5x32_hlc.txt, sha256 120111f07de771971403b85fb7f20f8c33231ecd7dba6adf205fb96082b61991), which we compared against; it was not a starting point
- arhancanli, pull request 19 to the leaderboard repository (https://github.com/gnikylime/GameofSloanes/pull/19), file 5x32_ARC.txt, which we compared against
- Benjamin Meadows (search, checking and packaging).
