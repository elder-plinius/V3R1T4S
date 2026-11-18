# game-of-sloanes-complex-line-packings, (7, 30): coherence 0.3452270454186594

## What

30 unit vectors in C^7 (object/7x30_bmea.txt) with coherence mu = 0.34522704541865939507 (exact integer arithmetic with a 60-digit square root; mpmath at 40 or more digits), lower than the Game of Sloanes leaderboard Best Coherence 0.34639121 for (d, n) = (7, 30) by 0.00116; the row is not marked provably optimal, mu is above the listed lower bound 0.33660139, every coordinate is written with at least 16 significant digits, and mu is also at least 1e-7 below every packing for this cell in the open pull requests to the leaderboard repository other than our own pull request 20 (lowest: 0.3459604160433147 in pull request 18, 0.3459901687816934 in pull request 14).

This package contains one object only: object/7x30_bmea.txt, in the leaderboard's file format (2dn numbers, one per line: the real parts of all 30 vectors, vector by vector, then the imaginary parts).

## Check it yourself

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. Python 3 standard library; under a second on a laptop. It checks the object's sha256, the count of numbers and the digits per coordinate, recomputes the coherence from the definition with exact integers, and compares it with the claimed value, the leaderboard value and the lower bound, and with the lowest coherence among the other open pull requests for this cell. Details: RUN_IT_YOURSELF.md.

## Compared to

| source | cell | coherence | URL | fetched (UTC) |
|---|---|---|---|---|
| Game of Sloanes leaderboard | (d, n) = (7, 30) | 0.34639121 | https://raw.githubusercontent.com/gnikylime/GameofSloanes/main/README.md | 2026-11-18T00:23:25Z |
| posted packing for the row (hlc) | (7, 30) | 0.3463912141 (recomputed) | https://raw.githubusercontent.com/gnikylime/GameofSloanes/main/CurrentBestPackings/7x30_hlc.txt | 2026-11-18T00:23:46Z |
| open pull request 18 (owhs) | (7, 30) | 0.3459604160 (recomputed) | https://github.com/gnikylime/GameofSloanes/raw/b0f64bccff9751542f9cb0803131542e37cb75e5/SubmittedPackings%2F7x30_owhs.txt | 2026-11-18T00:24:35Z |
| open pull request 14 (dustinmixon) | (7, 30) | 0.3459901687 (recomputed) | https://github.com/gnikylime/GameofSloanes/raw/04831504e5e74f42ca6742315a2eb2366503a10a/SubmittedPackings%2F7x30_sol.txt | 2026-11-18T00:24:10Z |

Details in the-record-we-beat/.

## Not claimed

- Not an optimal packing, only one with a lower coherence than the leaderboard row; the listed lower bound 0.33660139 is 0.00863 below mu.
- Only (7, 30). Other cells from the same searches are in packing-records and in pull request 20; each cell we claim here has its own package.
- Not new to the public record today: the same packing is in packing-records version 1.0.0 (https://github.com/TheBenMeadows/packing-records, https://doi.org/10.5281/zenodo.23906182, released 2026-11-02) and in pull request 20 to the leaderboard repository (https://github.com/gnikylime/GameofSloanes/pull/20, opened 2026-11-03, open and unmerged; the repository has had no commit since 2026-04-28).

## Credits

- John Jasper, Emily J. King and Dustin G. Mixon, the Game of Sloanes leaderboard, https://github.com/gnikylime/GameofSloanes (arXiv:1907.07848, https://arxiv.org/abs/1907.07848)
- Henry Cohn, the posted (7, 30) packing the leaderboard lists (https://raw.githubusercontent.com/gnikylime/GameofSloanes/main/CurrentBestPackings/7x30_hlc.txt, sha256 b0b34d8f2ac654a2496728439a28e4291cb4d6c739e2f84d28cdd6aa137dd15b), which we compared against; it was not a starting point
- owhs, pull request 18 to the leaderboard repository (https://github.com/gnikylime/GameofSloanes/pull/18), file 7x30_owhs.txt, which we compared against
- dustinmixon, pull request 14 to the leaderboard repository (https://github.com/gnikylime/GameofSloanes/pull/14), file 7x30_sol.txt, which we compared against
- Benjamin Meadows (search, checking and packaging).
