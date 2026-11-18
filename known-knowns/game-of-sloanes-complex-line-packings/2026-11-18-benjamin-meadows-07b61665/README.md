# game-of-sloanes-complex-line-packings, (3, 41): coherence 0.7784778326431421

## What

41 unit vectors in C^3 (object/3x41_bmea.txt) with coherence mu = 0.77847783264314213607 (exact integer arithmetic with a 60-digit square root; mpmath at 40 or more digits), lower than the Game of Sloanes leaderboard Best Coherence 0.77848806 for (d, n) = (3, 41) by 1.02e-05; the row is not marked provably optimal, mu is above the listed lower bound 0.68765248, every coordinate is written with at least 16 significant digits, and no open pull request to the leaderboard repository other than our own pull request 20 has a packing for this cell.

This package contains one object only: object/3x41_bmea.txt, in the leaderboard's file format (2dn numbers, one per line: the real parts of all 41 vectors, vector by vector, then the imaginary parts).

## Check it yourself

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. Python 3 standard library; under a second on a laptop. It checks the object's sha256, the count of numbers and the digits per coordinate, recomputes the coherence from the definition with exact integers, and compares it with the claimed value, the leaderboard value and the lower bound. Details: RUN_IT_YOURSELF.md.

## Compared to

| source | cell | coherence | URL | fetched (UTC) |
|---|---|---|---|---|
| Game of Sloanes leaderboard | (d, n) = (3, 41) | 0.77848806 | https://raw.githubusercontent.com/gnikylime/GameofSloanes/main/README.md | 2026-11-18T00:23:25Z |
| posted packing for the row (hlc) | (3, 41) | 0.7784880572 (recomputed) | https://raw.githubusercontent.com/gnikylime/GameofSloanes/main/CurrentBestPackings/3x41_hlc.txt | 2026-11-18T00:23:29Z |

Details in the-record-we-beat/.

## Not claimed

- Not an optimal packing, only one with a lower coherence than the leaderboard row; the listed lower bound 0.68765248 is 0.0908 below mu.
- Only (3, 41). Other cells from the same searches are in packing-records and in pull request 20; each cell we claim here has its own package.
- Not new to the public record today: the same packing is in packing-records version 1.0.0 (https://github.com/TheBenMeadows/packing-records, https://doi.org/10.5281/zenodo.23906182, released 2026-11-02) and in pull request 20 to the leaderboard repository (https://github.com/gnikylime/GameofSloanes/pull/20, opened 2026-11-03, open and unmerged; the repository has had no commit since 2026-04-28).
- Not byte-identical to the packing-records and pull request 20 file: see HOW_WE_FOUND_IT.md (same packing, more digits here).

## Credits

- John Jasper, Emily J. King and Dustin G. Mixon, the Game of Sloanes leaderboard, https://github.com/gnikylime/GameofSloanes (arXiv:1907.07848, https://arxiv.org/abs/1907.07848)
- Henry Cohn, the posted (3, 41) packing the leaderboard lists (https://raw.githubusercontent.com/gnikylime/GameofSloanes/main/CurrentBestPackings/3x41_hlc.txt, sha256 1ae78e6a24950748efa671792a0546800a2a88ad96ae6c355bf9f6c2f22f43ba), which we compared against; it was not a starting point
- Benjamin Meadows (search, checking and packaging).
