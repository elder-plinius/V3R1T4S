# game-of-sloanes-complex-line-packings, (6, 42): coherence 0.4311629053230761

## What

42 unit vectors in C^6 (object/6x42_bmea.txt) with coherence mu = 0.43116290532307612188 (exact integer arithmetic with a 60-digit square root; mpmath at 40 or more digits), lower than the Game of Sloanes leaderboard Best Coherence 0.43368892 for (d, n) = (6, 42) by 0.00253; the row is not marked provably optimal, mu is above the listed lower bound 0.40824829, every coordinate is written with at least 16 significant digits, and mu is also at least 1e-7 below every packing for this cell in the open pull requests to the leaderboard repository other than our own pull request 20 (lowest: 0.4332377852260275 in pull request 14).

This package contains one object only: object/6x42_bmea.txt, in the leaderboard's file format (2dn numbers, one per line: the real parts of all 42 vectors, vector by vector, then the imaginary parts).

## Check it yourself

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. Python 3 standard library; under a second on a laptop. It checks the object's sha256, the count of numbers and the digits per coordinate, recomputes the coherence from the definition with exact integers, and compares it with the claimed value, the leaderboard value and the lower bound, and with the lowest coherence among the other open pull requests for this cell. Details: RUN_IT_YOURSELF.md.

## Compared to

| source | cell | coherence | URL | fetched (UTC) |
|---|---|---|---|---|
| Game of Sloanes leaderboard | (d, n) = (6, 42) | 0.43368892 | https://raw.githubusercontent.com/gnikylime/GameofSloanes/main/README.md | 2026-11-18T00:23:25Z |
| posted packing for the row (oai) | (6, 42) | 0.4336889184 (recomputed) | https://raw.githubusercontent.com/gnikylime/GameofSloanes/main/CurrentBestPackings/6x42_oai.txt | 2026-11-18T00:23:37Z |
| open pull request 14 (dustinmixon) | (6, 42) | 0.4332377852 (recomputed) | https://github.com/gnikylime/GameofSloanes/raw/04831504e5e74f42ca6742315a2eb2366503a10a/SubmittedPackings%2F6x42_sol.txt | 2026-11-18T00:24:07Z |

Details in the-record-we-beat/.

## Not claimed

- Not an optimal packing, only one with a lower coherence than the leaderboard row; the listed lower bound 0.40824829 is 0.0229 below mu.
- Only (6, 42). Other cells from the same searches are in packing-records and in pull request 20; each cell we claim here has its own package.
- Not new to the public record today: the same packing is in packing-records version 1.0.0 (https://github.com/TheBenMeadows/packing-records, https://doi.org/10.5281/zenodo.23906182, released 2026-11-02) and in pull request 20 to the leaderboard repository (https://github.com/gnikylime/GameofSloanes/pull/20, opened 2026-11-03, open and unmerged; the repository has had no commit since 2026-04-28).

## Credits

- John Jasper, Emily J. King and Dustin G. Mixon, the Game of Sloanes leaderboard, https://github.com/gnikylime/GameofSloanes (arXiv:1907.07848, https://arxiv.org/abs/1907.07848)
- Dustin G. Mixon (creator code `oai` on the leaderboard), the posted (6, 42) packing the leaderboard lists (https://raw.githubusercontent.com/gnikylime/GameofSloanes/main/CurrentBestPackings/6x42_oai.txt, sha256 0b655cdb78764d666a1585fe9e217d6b312f3fef80152a3013874f20432fb1a2), which we compared against; it was not a starting point
- dustinmixon, pull request 14 to the leaderboard repository (https://github.com/gnikylime/GameofSloanes/pull/14), file 6x42_sol.txt, which we compared against
- Benjamin Meadows (search, checking and packaging).
