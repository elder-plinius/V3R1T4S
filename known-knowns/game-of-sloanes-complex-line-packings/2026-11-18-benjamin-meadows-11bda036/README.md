# game-of-sloanes-complex-line-packings, (7, 32): coherence 0.3522003805583704

## What

32 unit vectors in C^7 (object/7x32_bmea.txt) with coherence mu = 0.35220038055837041551 (exact integer arithmetic with a 60-digit square root; mpmath at 40 or more digits), lower than the Game of Sloanes leaderboard Best Coherence 0.35229897 for (d, n) = (7, 32) by 9.86e-05; the row is not marked provably optimal, mu is above the listed lower bound 0.33942212, every coordinate is written with at least 16 significant digits, and mu is also at least 1e-7 below every packing for this cell in the open pull requests to the leaderboard repository other than our own pull request 20 (lowest: 0.3522962643637698 in pull request 18).

This package contains one object only: object/7x32_bmea.txt, in the leaderboard's file format (2dn numbers, one per line: the real parts of all 32 vectors, vector by vector, then the imaginary parts).

## Check it yourself

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. Python 3 standard library; under a second on a laptop. It checks the object's sha256, the count of numbers and the digits per coordinate, recomputes the coherence from the definition with exact integers, and compares it with the claimed value, the leaderboard value and the lower bound, and with the lowest coherence among the other open pull requests for this cell. Details: RUN_IT_YOURSELF.md.

## Compared to

| source | cell | coherence | URL | fetched (UTC) |
|---|---|---|---|---|
| Game of Sloanes leaderboard | (d, n) = (7, 32) | 0.35229897 | https://raw.githubusercontent.com/gnikylime/GameofSloanes/main/README.md | 2026-11-18T00:23:25Z |
| posted packing for the row (jrr) | (7, 32) | 0.3522989657 (recomputed) | https://raw.githubusercontent.com/gnikylime/GameofSloanes/main/CurrentBestPackings/7x32_jrr.txt | 2026-11-18T00:23:47Z |
| open pull request 18 (owhs) | (7, 32) | 0.3522962643 (recomputed) | https://github.com/gnikylime/GameofSloanes/raw/b0f64bccff9751542f9cb0803131542e37cb75e5/SubmittedPackings%2F7x32_owhs.txt | 2026-11-18T00:24:37Z |

Details in the-record-we-beat/.

## Not claimed

- Not an optimal packing, only one with a lower coherence than the leaderboard row; the listed lower bound 0.33942212 is 0.0128 below mu.
- Only (7, 32). Other cells from the same searches are in packing-records and in pull request 20; each cell we claim here has its own package.
- Not new to the public record today: the same packing is in packing-records version 1.0.0 (https://github.com/TheBenMeadows/packing-records, https://doi.org/10.5281/zenodo.23906182, released 2026-11-02) and in pull request 20 to the leaderboard repository (https://github.com/gnikylime/GameofSloanes/pull/20, opened 2026-11-03, open and unmerged; the repository has had no commit since 2026-04-28).

## Credits

- John Jasper, Emily J. King and Dustin G. Mixon, the Game of Sloanes leaderboard, https://github.com/gnikylime/GameofSloanes (arXiv:1907.07848, https://arxiv.org/abs/1907.07848)
- Juan Román-Roche and Sebastián Roca-Jerat (using FrameOpt, https://github.com/chuan97/frameopt), the posted (7, 32) packing the leaderboard lists (https://raw.githubusercontent.com/gnikylime/GameofSloanes/main/CurrentBestPackings/7x32_jrr.txt, sha256 f3a443590860d14aadd06389113a638d314172c024119f20c354e4c21e2e0c16), which we compared against; it was not a starting point
- owhs, pull request 18 to the leaderboard repository (https://github.com/gnikylime/GameofSloanes/pull/18), file 7x32_owhs.txt, which we compared against
- Benjamin Meadows (search, checking and packaging).
