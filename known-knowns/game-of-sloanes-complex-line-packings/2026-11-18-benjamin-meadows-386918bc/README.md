# game-of-sloanes-complex-line-packings, (5, 38): coherence 0.4999809988399789

## What

38 unit vectors in C^5 (object/5x38_bmea.txt) with coherence mu = 0.49998099883997889999 (exact integer arithmetic with a 60-digit square root; mpmath at 40 or more digits), lower than the Game of Sloanes leaderboard Best Coherence 0.49998890 for (d, n) = (5, 38) by 7.9e-06; the row is not marked provably optimal, mu is above the listed lower bound 0.48199920, every coordinate is written with at least 16 significant digits, and mu is also at least 1e-7 below every packing for this cell in the open pull requests to the leaderboard repository other than our own pull request 20 (lowest: 0.4999857906170948 in pull request 17, 0.4999864756948050 in pull request 15).

This package contains one object only: object/5x38_bmea.txt, in the leaderboard's file format (2dn numbers, one per line: the real parts of all 38 vectors, vector by vector, then the imaginary parts).

## Check it yourself

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. Python 3 standard library; under a second on a laptop. It checks the object's sha256, the count of numbers and the digits per coordinate, recomputes the coherence from the definition with exact integers, and compares it with the claimed value, the leaderboard value and the lower bound, and with the lowest coherence among the other open pull requests for this cell. Details: RUN_IT_YOURSELF.md.

## Compared to

| source | cell | coherence | URL | fetched (UTC) |
|---|---|---|---|---|
| Game of Sloanes leaderboard | (d, n) = (5, 38) | 0.49998890 | https://raw.githubusercontent.com/gnikylime/GameofSloanes/main/README.md | 2026-11-18T00:23:25Z |
| posted packing for the row (jrr) | (5, 38) | 0.4999889033 (recomputed) | https://raw.githubusercontent.com/gnikylime/GameofSloanes/main/CurrentBestPackings/5x38_jrr.txt | 2026-11-18T00:23:35Z |
| open pull request 17 (JosiahPark) | (5, 38) | 0.4999857906 (recomputed) | https://github.com/gnikylime/GameofSloanes/raw/134bb4bd8ef2d433f5a24a0bf8227fc98855607d/CurrentBestPackings%2F5x38_grai.txt | 2026-11-18T00:24:19Z |
| open pull request 15 (djma) | (5, 38) | 0.4999864756 (recomputed) | https://github.com/gnikylime/GameofSloanes/raw/6f4a1bd2b3c14f0dee6d4cb52eafca77eb794b9c/SubmittedPackings%2F5x38_djma.txt | 2026-11-18T00:24:13Z |

Details in the-record-we-beat/.

## Not claimed

- Not an optimal packing, only one with a lower coherence than the leaderboard row; the listed lower bound 0.48199920 is 0.018 below mu.
- Only (5, 38). Other cells from the same searches are in packing-records and in pull request 20; each cell we claim here has its own package.
- Not new to the public record today: the same packing is in packing-records version 1.0.0 (https://github.com/TheBenMeadows/packing-records, https://doi.org/10.5281/zenodo.23906182, released 2026-11-02) and in pull request 20 to the leaderboard repository (https://github.com/gnikylime/GameofSloanes/pull/20, opened 2026-11-03, open and unmerged; the repository has had no commit since 2026-04-28).

## Credits

- John Jasper, Emily J. King and Dustin G. Mixon, the Game of Sloanes leaderboard, https://github.com/gnikylime/GameofSloanes (arXiv:1907.07848, https://arxiv.org/abs/1907.07848)
- Juan Román-Roche and Sebastián Roca-Jerat (using FrameOpt, https://github.com/chuan97/frameopt), the posted (5, 38) packing the leaderboard lists (https://raw.githubusercontent.com/gnikylime/GameofSloanes/main/CurrentBestPackings/5x38_jrr.txt, sha256 f65b0a2aa852c5d3f10fa85d7a78e6784f1e344cbea57f96a4cd356cdd423e09), which we compared against; it was not a starting point
- JosiahPark, pull request 17 to the leaderboard repository (https://github.com/gnikylime/GameofSloanes/pull/17), file 5x38_grai.txt, which we compared against
- djma, pull request 15 to the leaderboard repository (https://github.com/gnikylime/GameofSloanes/pull/15), file 5x38_djma.txt, which we compared against
- Benjamin Meadows (search, checking and packaging).
