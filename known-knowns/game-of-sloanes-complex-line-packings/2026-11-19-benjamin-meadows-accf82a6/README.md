# game-of-sloanes-complex-line-packings, (7, 31): coherence 0.3485093138521599

## What

The 2dn = 434 numbers in 7x31_bmea.txt (sha256 accf82a6ee2089b1...), read vector by vector in the repository layout and normalised, give 31 unit vectors in C^7 with coherence 0.3485093138522 at 40-digit precision, which is 9.0629e-04 below the Best Coherence 0.34941560 of the unmarked (7, 31) row of the GameofSloanes README fetched 2026-11-19T05:11:01Z and above that row's lower bound 0.33806170.

In numbers: 31 unit vectors in C^7 with coherence mu = 0.34850931385215991893, 0.000906 below the leaderboard Best Coherence 0.34941560 (row not marked provably optimal, lower bound 0.33806170); mu is 0.00085 below the lowest coherence among the packings for this cell in the open pull requests to the leaderboard repository (0.34935941870298 in pull request 18, owhs). This package contains one object only: object/7x31_bmea.txt, in the leaderboard's file format (2dn numbers, one per line: the real parts of all 31 vectors, vector by vector, then the imaginary parts).

## Check it yourself

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. Python 3 standard library; under a second on a laptop. It checks the object's sha256, the count of numbers and the digits per coordinate, recomputes the coherence from the definition with exact integers, and compares it with the claimed value, the leaderboard value and the lower bound, and with the lowest coherence among the open pull requests for this cell. Details: RUN_IT_YOURSELF.md.

## Compared to

| source | cell | coherence | URL | fetched (UTC) |
|---|---|---|---|---|
| Game of Sloanes leaderboard | (d, n) = (7, 31) | 0.34941560 | https://raw.githubusercontent.com/gnikylime/GameofSloanes/main/README.md | 2026-11-19T05:00:43Z |
| posted packing for the row (jrr) | (7, 31) | 0.3494156040 (recomputed) | https://raw.githubusercontent.com/gnikylime/GameofSloanes/main/CurrentBestPackings/7x31_jrr.txt | 2026-11-19T05:02:19Z |
| open pull request 18 (owhs) | (7, 31) | 0.3493594187 (recomputed) | https://github.com/gnikylime/GameofSloanes/raw/b0f64bccff9751542f9cb0803131542e37cb75e5/SubmittedPackings%2F7x31_owhs.txt | 2026-11-19T05:01:23Z |

Details in the-record-we-beat/.

## Not claimed

- Not an optimal packing, only one with a lower coherence than the leaderboard row; the listed lower bound 0.33806170 is 0.0104 below mu.
- Only (7, 31). Each cell we claim has its own package.
- Not built from scratch: the object was started from the published (7, 30) packing named above (one vector added), and is credited to its author as a starting point.

## Credits

- John Jasper, Emily J. King and Dustin G. Mixon, the Game of Sloanes leaderboard, https://github.com/gnikylime/GameofSloanes (arXiv:1907.07848, https://arxiv.org/abs/1907.07848)
- owhs, pull request 18 to the leaderboard repository (https://github.com/gnikylime/GameofSloanes/pull/18), file 7x30_owhs.txt: the (7, 30) packing the object descends from; a starting point of this object (one vector added)
- Juan Román-Roche and Sebastián Roca-Jerat (using FrameOpt, https://github.com/chuan97/frameopt), the posted (7, 31) packing the leaderboard lists (https://raw.githubusercontent.com/gnikylime/GameofSloanes/main/CurrentBestPackings/7x31_jrr.txt, sha256 7d0e57f131750209b9f9d41994093a37c9783f182b9e1eeda2d9c811272b8d84), which we compared against and which the search was given as a seed; the object does not descend from it
- owhs, pull request 18 to the leaderboard repository (https://github.com/gnikylime/GameofSloanes/pull/18), file 7x31_owhs.txt, which we compared against and which the search was given as a seed; the object does not descend from it
- Benjamin Meadows (search, checking and packaging; also the author of pull request 20 and of packing-records, https://github.com/TheBenMeadows/packing-records).
