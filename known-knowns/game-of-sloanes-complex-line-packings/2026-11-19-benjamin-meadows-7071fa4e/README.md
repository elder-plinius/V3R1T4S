# game-of-sloanes-complex-line-packings, (7, 24): coherence 0.3290360584555491

## What

The 2dn = 336 numbers in 7x24_bmea.txt (sha256 7071fa4e349c69da...), read vector by vector in the repository layout and normalised, give 24 unit vectors in C^7 with coherence 0.3290360584555 at 40-digit precision, which is 5.6365e-04 below the Best Coherence 0.32959971 of the unmarked (7, 24) row of the GameofSloanes README fetched 2026-11-19T05:11:01Z and above that row's lower bound 0.32494624.

In numbers: 24 unit vectors in C^7 with coherence mu = 0.32903605845554906315, 0.000564 below the leaderboard Best Coherence 0.32959971 (row not marked provably optimal, lower bound 0.32494624); mu is 0.000307 below the lowest coherence among the packings for this cell in the open pull requests to the leaderboard repository (0.32934295752156 in pull request 18, owhs). This package contains one object only: object/7x24_bmea.txt, in the leaderboard's file format (2dn numbers, one per line: the real parts of all 24 vectors, vector by vector, then the imaginary parts).

## Check it yourself

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. Python 3 standard library; under a second on a laptop. It checks the object's sha256, the count of numbers and the digits per coordinate, recomputes the coherence from the definition with exact integers, and compares it with the claimed value, the leaderboard value and the lower bound, and with the lowest coherence among the open pull requests for this cell. Details: RUN_IT_YOURSELF.md.

## Compared to

| source | cell | coherence | URL | fetched (UTC) |
|---|---|---|---|---|
| Game of Sloanes leaderboard | (d, n) = (7, 24) | 0.32959971 | https://raw.githubusercontent.com/gnikylime/GameofSloanes/main/README.md | 2026-11-19T05:00:43Z |
| posted packing for the row (hlc) | (7, 24) | 0.3295997130 (recomputed) | https://raw.githubusercontent.com/gnikylime/GameofSloanes/main/CurrentBestPackings/7x24_hlc.txt | 2026-11-19T05:02:15Z |
| open pull request 18 (owhs) | (7, 24) | 0.3293429575 (recomputed) | https://github.com/gnikylime/GameofSloanes/raw/b0f64bccff9751542f9cb0803131542e37cb75e5/SubmittedPackings%2F7x24_owhs.txt | 2026-11-19T05:01:17Z |
| open pull request 20 (TheBenMeadows) | (7, 24) | 0.3293574687 (recomputed) | https://github.com/gnikylime/GameofSloanes/raw/cd4bf5ea596b70c1eb9c65e4cad5903018f3e1ca/SubmittedPackings%2F7x24_bmea.txt | 2026-11-19T05:00:59Z |

Details in the-record-we-beat/.

## Not claimed

- Not an optimal packing, only one with a lower coherence than the leaderboard row; the listed lower bound 0.32494624 is 0.00409 below mu.
- Only (7, 24). Each cell we claim has its own package.

## Credits

- John Jasper, Emily J. King and Dustin G. Mixon, the Game of Sloanes leaderboard, https://github.com/gnikylime/GameofSloanes (arXiv:1907.07848, https://arxiv.org/abs/1907.07848)
- Henry Cohn, the posted (7, 24) packing the leaderboard lists (https://raw.githubusercontent.com/gnikylime/GameofSloanes/main/CurrentBestPackings/7x24_hlc.txt, sha256 2ca766817699f823c791df48578140ad5477f9a9c34dfd4a567be0d0620ffc02), which we compared against and which the search was given as a seed; the object does not descend from it
- owhs, pull request 18 to the leaderboard repository (https://github.com/gnikylime/GameofSloanes/pull/18), file 7x24_owhs.txt, which we compared against and which the search was given as a seed; the object does not descend from it
- Benjamin Meadows (search, checking and packaging; also the author of pull request 20 and of packing-records, https://github.com/TheBenMeadows/packing-records).
