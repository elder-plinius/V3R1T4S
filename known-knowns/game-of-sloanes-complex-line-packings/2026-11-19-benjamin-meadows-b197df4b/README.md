# game-of-sloanes-complex-line-packings, (6, 45): coherence 0.4503506341028973

## What

The 2dn = 540 numbers in 6x45_bmea.txt (sha256 b197df4be95fd38c...), read vector by vector in the repository layout and normalised, give 45 unit vectors in C^6 with coherence 0.4503506341029 at 40-digit precision, which is 9.7367e-04 below the Best Coherence 0.45132430 of the unmarked (6, 45) row of the GameofSloanes README fetched 2026-11-19T05:11:01Z and above that row's lower bound 0.41931393.

In numbers: 45 unit vectors in C^6 with coherence mu = 0.45035063410289725825, 0.000974 below the leaderboard Best Coherence 0.45132430 (row not marked provably optimal, lower bound 0.41931393); mu is 0.000776 below the lowest coherence among the packings for this cell in the open pull requests to the leaderboard repository (0.45112660942111 in pull request 17, JosiahPark). This package contains one object only: object/6x45_bmea.txt, in the leaderboard's file format (2dn numbers, one per line: the real parts of all 45 vectors, vector by vector, then the imaginary parts).

## Check it yourself

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. Python 3 standard library; under a second on a laptop. It checks the object's sha256, the count of numbers and the digits per coordinate, recomputes the coherence from the definition with exact integers, and compares it with the claimed value, the leaderboard value and the lower bound, and with the lowest coherence among the open pull requests for this cell. Details: RUN_IT_YOURSELF.md.

## Compared to

| source | cell | coherence | URL | fetched (UTC) |
|---|---|---|---|---|
| Game of Sloanes leaderboard | (d, n) = (6, 45) | 0.45132430 | https://raw.githubusercontent.com/gnikylime/GameofSloanes/main/README.md | 2026-11-19T05:00:43Z |
| posted packing for the row (hlc) | (6, 45) | 0.4513242950 (recomputed) | https://raw.githubusercontent.com/gnikylime/GameofSloanes/main/CurrentBestPackings/6x45_hlc.txt | 2026-11-19T05:02:13Z |
| open pull request 17 (JosiahPark) | (6, 45) | 0.4511266094 (recomputed) | https://github.com/gnikylime/GameofSloanes/raw/134bb4bd8ef2d433f5a24a0bf8227fc98855607d/CurrentBestPackings%2F6x45_grai.txt | 2026-11-19T05:01:36Z |
| open pull request 15 (djma) | (6, 45) | 0.4511284072 (recomputed) | https://github.com/gnikylime/GameofSloanes/raw/6f4a1bd2b3c14f0dee6d4cb52eafca77eb794b9c/SubmittedPackings%2F6x45_djma.txt | 2026-11-19T05:01:51Z |
| open pull request 14 (dustinmixon) | (6, 45) | 0.4511572114 (recomputed) | https://github.com/gnikylime/GameofSloanes/raw/04831504e5e74f42ca6742315a2eb2366503a10a/SubmittedPackings%2F6x45_sol.txt | 2026-11-19T05:02:02Z |
| open pull request 20 (TheBenMeadows) | (6, 45) | 0.4512086459 (recomputed) | https://github.com/gnikylime/GameofSloanes/raw/cd4bf5ea596b70c1eb9c65e4cad5903018f3e1ca/SubmittedPackings%2F6x45_bmea.txt | 2026-11-19T05:00:54Z |

Details in the-record-we-beat/.

## Not claimed

- Not an optimal packing, only one with a lower coherence than the leaderboard row; the listed lower bound 0.41931393 is 0.031 below mu.
- Only (6, 45). Each cell we claim has its own package.
- Not built from scratch: the object was started from the published (6, 44) packing named above (one vector added), and is credited to its authors as a starting point.

## Credits

- John Jasper, Emily J. King and Dustin G. Mixon, the Game of Sloanes leaderboard, https://github.com/gnikylime/GameofSloanes (arXiv:1907.07848, https://arxiv.org/abs/1907.07848)
- djma, pull request 15 to the leaderboard repository (https://github.com/gnikylime/GameofSloanes/pull/15), file 6x44_djma.txt: the (6, 44) packing the object descends from; a starting point of this object (one vector added)
- JosiahPark, pull request 17 to the leaderboard repository (https://github.com/gnikylime/GameofSloanes/pull/17), file 6x44_grai.txt: the same (6, 44) packing, slightly polished, which the search was also given; a starting point of this object (one vector added)
- Henry Cohn, the posted (6, 45) packing the leaderboard lists (https://raw.githubusercontent.com/gnikylime/GameofSloanes/main/CurrentBestPackings/6x45_hlc.txt, sha256 d3f00db78a3c58caebdd4abbf680528041c0881ff13758dd437b2940e68124da), which we compared against and which the search was given as a seed; the object does not descend from it
- JosiahPark, pull request 17 to the leaderboard repository (https://github.com/gnikylime/GameofSloanes/pull/17), file 6x45_grai.txt, which we compared against and which the search was given as a seed; the object does not descend from it
- djma, pull request 15 to the leaderboard repository (https://github.com/gnikylime/GameofSloanes/pull/15), file 6x45_djma.txt, which we compared against and which the search was given as a seed; the object does not descend from it
- dustinmixon, pull request 14 to the leaderboard repository (https://github.com/gnikylime/GameofSloanes/pull/14), file 6x45_sol.txt, which we compared against and which the search was given as a seed; the object does not descend from it
- Benjamin Meadows (search, checking and packaging; also the author of pull request 20 and of packing-records, https://github.com/TheBenMeadows/packing-records).
