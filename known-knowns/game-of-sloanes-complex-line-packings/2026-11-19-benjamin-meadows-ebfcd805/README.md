# game-of-sloanes-complex-line-packings, (7, 29): coherence 0.3400004550336341

## What

The 2dn = 406 numbers in 7x29_bmea.txt (sha256 ebfcd805697bcd8c...), read vector by vector in the repository layout and normalised, give 29 unit vectors in C^7 with coherence 0.3400004550336 at 40-digit precision, which is 6.4505e-04 below the Best Coherence 0.34064551 of the unmarked (7, 29) row of the GameofSloanes README fetched 2026-11-19T05:11:01Z and above that row's lower bound 0.33502970.

In numbers: 29 unit vectors in C^7 with coherence mu = 0.34000045503363412448, 0.000645 below the leaderboard Best Coherence 0.34064551 (row not marked provably optimal, lower bound 0.33502970); mu is 0.000542 below the lowest coherence among the packings for this cell in the open pull requests to the leaderboard repository (0.34054289311848 in pull request 18, owhs). This package contains one object only: object/7x29_bmea.txt, in the leaderboard's file format (2dn numbers, one per line: the real parts of all 29 vectors, vector by vector, then the imaginary parts).

## Check it yourself

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. Python 3 standard library; under a second on a laptop. It checks the object's sha256, the count of numbers and the digits per coordinate, recomputes the coherence from the definition with exact integers, and compares it with the claimed value, the leaderboard value and the lower bound, and with the lowest coherence among the open pull requests for this cell. Details: RUN_IT_YOURSELF.md.

## Compared to

| source | cell | coherence | URL | fetched (UTC) |
|---|---|---|---|---|
| Game of Sloanes leaderboard | (d, n) = (7, 29) | 0.34064551 | https://raw.githubusercontent.com/gnikylime/GameofSloanes/main/README.md | 2026-11-19T05:00:43Z |
| posted packing for the row (oai) | (7, 29) | 0.3406455123 (recomputed) | https://raw.githubusercontent.com/gnikylime/GameofSloanes/main/CurrentBestPackings/7x29_oai.txt | 2026-11-19T05:02:17Z |
| open pull request 18 (owhs) | (7, 29) | 0.3405428931 (recomputed) | https://github.com/gnikylime/GameofSloanes/raw/b0f64bccff9751542f9cb0803131542e37cb75e5/SubmittedPackings%2F7x29_owhs.txt | 2026-11-19T05:01:20Z |
| open pull request 20 (TheBenMeadows) | (7, 29) | 0.3405428934 (recomputed) | https://github.com/gnikylime/GameofSloanes/raw/cd4bf5ea596b70c1eb9c65e4cad5903018f3e1ca/SubmittedPackings%2F7x29_bmea.txt | 2026-11-19T05:01:04Z |
| open pull request 14 (dustinmixon) | (7, 29) | 0.3405452935 (recomputed) | https://github.com/gnikylime/GameofSloanes/raw/04831504e5e74f42ca6742315a2eb2366503a10a/SubmittedPackings%2F7x29_sol.txt | 2026-11-19T05:02:04Z |

Details in the-record-we-beat/.

## Not claimed

- Not an optimal packing, only one with a lower coherence than the leaderboard row; the listed lower bound 0.33502970 is 0.00497 below mu.
- Only (7, 29). Each cell we claim has its own package.
- Not built from scratch: the object was started from the published (7, 30) packing named above (one vector removed), and is credited to its author as a starting point.

## Credits

- John Jasper, Emily J. King and Dustin G. Mixon, the Game of Sloanes leaderboard, https://github.com/gnikylime/GameofSloanes (arXiv:1907.07848, https://arxiv.org/abs/1907.07848)
- owhs, pull request 18 to the leaderboard repository (https://github.com/gnikylime/GameofSloanes/pull/18), file 7x30_owhs.txt: the (7, 30) packing the object descends from; a starting point of this object (one vector removed)
- Dustin G. Mixon (creator code `oai` on the leaderboard), the posted (7, 29) packing the leaderboard lists (https://raw.githubusercontent.com/gnikylime/GameofSloanes/main/CurrentBestPackings/7x29_oai.txt, sha256 6b9163c2dc1a94ba2ae561aec135a730d7bf26d8ea575aa00a9319d9a1b24a7f), which we compared against and which the search was given as a seed; the object does not descend from it
- owhs, pull request 18 to the leaderboard repository (https://github.com/gnikylime/GameofSloanes/pull/18), file 7x29_owhs.txt, which we compared against and which the search was given as a seed; the object does not descend from it
- dustinmixon, pull request 14 to the leaderboard repository (https://github.com/gnikylime/GameofSloanes/pull/14), file 7x29_sol.txt, which we compared against and which the search was given as a seed; the object does not descend from it
- Benjamin Meadows (search, checking and packaging; also the author of pull request 20 and of packing-records, https://github.com/TheBenMeadows/packing-records).
