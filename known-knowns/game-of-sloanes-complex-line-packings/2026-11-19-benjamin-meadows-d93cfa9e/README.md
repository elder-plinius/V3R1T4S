# game-of-sloanes-complex-line-packings, (6, 44): coherence 0.4454997364686413

## What

The 2dn = 528 numbers in 6x44_bmea.txt (sha256 d93cfa9e4a52fe04...), read vector by vector in the repository layout and normalised, give 44 unit vectors in C^6 with coherence 0.4454997364686 at 40-digit precision, which is 9.3046e-04 below the Best Coherence 0.44643020 of the unmarked (6, 44) row of the GameofSloanes README fetched 2026-11-19T05:11:01Z and above that row's lower bound 0.41585133.

In numbers: 44 unit vectors in C^6 with coherence mu = 0.44549973646864132149, 0.00093 below the leaderboard Best Coherence 0.44643020 (row not marked provably optimal, lower bound 0.41585133); mu is 0.000397 below the lowest coherence among the packings for this cell in the open pull requests to the leaderboard repository (0.44589711067290 in pull request 17, JosiahPark). This package contains one object only: object/6x44_bmea.txt, in the leaderboard's file format (2dn numbers, one per line: the real parts of all 44 vectors, vector by vector, then the imaginary parts).

## Check it yourself

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. Python 3 standard library; under a second on a laptop. It checks the object's sha256, the count of numbers and the digits per coordinate, recomputes the coherence from the definition with exact integers, and compares it with the claimed value, the leaderboard value and the lower bound, and with the lowest coherence among the open pull requests for this cell. Details: RUN_IT_YOURSELF.md.

## Compared to

| source | cell | coherence | URL | fetched (UTC) |
|---|---|---|---|---|
| Game of Sloanes leaderboard | (d, n) = (6, 44) | 0.44643020 | https://raw.githubusercontent.com/gnikylime/GameofSloanes/main/README.md | 2026-11-19T05:00:43Z |
| posted packing for the row (oai) | (6, 44) | 0.4464301986 (recomputed) | https://raw.githubusercontent.com/gnikylime/GameofSloanes/main/CurrentBestPackings/6x44_oai.txt | 2026-11-19T05:02:12Z |
| open pull request 17 (JosiahPark) | (6, 44) | 0.4458971106 (recomputed) | https://github.com/gnikylime/GameofSloanes/raw/134bb4bd8ef2d433f5a24a0bf8227fc98855607d/CurrentBestPackings%2F6x44_grai.txt | 2026-11-19T05:01:34Z |
| open pull request 15 (djma) | (6, 44) | 0.4458993772 (recomputed) | https://github.com/gnikylime/GameofSloanes/raw/6f4a1bd2b3c14f0dee6d4cb52eafca77eb794b9c/SubmittedPackings%2F6x44_djma.txt | 2026-11-19T05:01:49Z |
| open pull request 20 (TheBenMeadows) | (6, 44) | 0.4460997588 (recomputed) | https://github.com/gnikylime/GameofSloanes/raw/cd4bf5ea596b70c1eb9c65e4cad5903018f3e1ca/SubmittedPackings%2F6x44_bmea.txt | 2026-11-19T05:00:52Z |
| open pull request 14 (dustinmixon) | (6, 44) | 0.4462476363 (recomputed) | https://github.com/gnikylime/GameofSloanes/raw/04831504e5e74f42ca6742315a2eb2366503a10a/SubmittedPackings%2F6x44_sol.txt | 2026-11-19T05:02:00Z |

Details in the-record-we-beat/.

## Not claimed

- Not an optimal packing, only one with a lower coherence than the leaderboard row; the listed lower bound 0.41585133 is 0.0296 below mu.
- Only (6, 44). Each cell we claim has its own package.
- Not built from scratch: the object was started from the published (6, 43) packing named above (one vector added), and is credited to its authors as a starting point.

## Credits

- John Jasper, Emily J. King and Dustin G. Mixon, the Game of Sloanes leaderboard, https://github.com/gnikylime/GameofSloanes (arXiv:1907.07848, https://arxiv.org/abs/1907.07848)
- djma, pull request 15 to the leaderboard repository (https://github.com/gnikylime/GameofSloanes/pull/15), file 6x43_djma.txt: the (6, 43) packing the object descends from; a starting point of this object (one vector added)
- JosiahPark, pull request 17 to the leaderboard repository (https://github.com/gnikylime/GameofSloanes/pull/17), file 6x43_grai.txt: the same (6, 43) packing, slightly polished, which the search was also given; a starting point of this object (one vector added)
- Dustin G. Mixon (creator code `oai` on the leaderboard), the posted (6, 44) packing the leaderboard lists (https://raw.githubusercontent.com/gnikylime/GameofSloanes/main/CurrentBestPackings/6x44_oai.txt, sha256 51cb29423b8ae4cdcb6f2884702974e874eb29b30f1254a609f3cadc4d41de10), which we compared against and which the search was given as a seed; the object does not descend from it
- JosiahPark, pull request 17 to the leaderboard repository (https://github.com/gnikylime/GameofSloanes/pull/17), file 6x44_grai.txt, which we compared against and which the search was given as a seed; the object does not descend from it
- djma, pull request 15 to the leaderboard repository (https://github.com/gnikylime/GameofSloanes/pull/15), file 6x44_djma.txt, which we compared against and which the search was given as a seed; the object does not descend from it
- dustinmixon, pull request 14 to the leaderboard repository (https://github.com/gnikylime/GameofSloanes/pull/14), file 6x44_sol.txt, which we compared against and which the search was given as a seed; the object does not descend from it
- Benjamin Meadows (search, checking and packaging; also the author of pull request 20 and of packing-records, https://github.com/TheBenMeadows/packing-records).
