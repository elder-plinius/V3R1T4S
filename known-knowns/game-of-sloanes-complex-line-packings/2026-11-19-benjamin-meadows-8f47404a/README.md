# game-of-sloanes-complex-line-packings, (5, 36): coherence 0.4992008036545907

## What

The 2dn = 360 numbers in 5x36_bmea.txt (sha256 8f47404a6ab8b0ba...), read vector by vector in the repository layout and normalised, give 36 unit vectors in C^5 with coherence 0.4992008036546 at 40-digit precision, which is 7.8810e-04 below the Best Coherence 0.49998890 of the unmarked (5, 36) row of the GameofSloanes README fetched 2026-11-19T05:11:01Z and above that row's lower bound 0.47519096.

In numbers: 36 unit vectors in C^5 with coherence mu = 0.49920080365459070361, 0.000788 below the leaderboard Best Coherence 0.49998890 (row not marked provably optimal, lower bound 0.47519096); mu is 0.000117 below the lowest coherence among the packings for this cell in the open pull requests to the leaderboard repository (0.49931760537131 in pull request 17, JosiahPark). This package contains one object only: object/5x36_bmea.txt, in the leaderboard's file format (2dn numbers, one per line: the real parts of all 36 vectors, vector by vector, then the imaginary parts).

## Check it yourself

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. Python 3 standard library; under a second on a laptop. It checks the object's sha256, the count of numbers and the digits per coordinate, recomputes the coherence from the definition with exact integers, and compares it with the claimed value, the leaderboard value and the lower bound, and with the lowest coherence among the open pull requests for this cell. Details: RUN_IT_YOURSELF.md.

## Compared to

| source | cell | coherence | URL | fetched (UTC) |
|---|---|---|---|---|
| Game of Sloanes leaderboard | (d, n) = (5, 36) | 0.49998890 | https://raw.githubusercontent.com/gnikylime/GameofSloanes/main/README.md | 2026-11-19T05:00:43Z |
| posted packing for the row (AUTO) | (5, 36) | 0.4999889033 (recomputed) | https://raw.githubusercontent.com/gnikylime/GameofSloanes/main/CurrentBestPackings/5x36_AUTO.txt | 2026-11-19T05:02:10Z |
| open pull request 17 (JosiahPark) | (5, 36) | 0.4993176053 (recomputed) | https://github.com/gnikylime/GameofSloanes/raw/134bb4bd8ef2d433f5a24a0bf8227fc98855607d/CurrentBestPackings%2F5x36_grai.txt | 2026-11-19T05:01:30Z |
| open pull request 15 (djma) | (5, 36) | 0.4993183835 (recomputed) | https://github.com/gnikylime/GameofSloanes/raw/6f4a1bd2b3c14f0dee6d4cb52eafca77eb794b9c/SubmittedPackings%2F5x36_djma.txt | 2026-11-19T05:01:44Z |
| open pull request 14 (dustinmixon) | (5, 36) | 0.4994381878 (recomputed) | https://github.com/gnikylime/GameofSloanes/raw/04831504e5e74f42ca6742315a2eb2366503a10a/SubmittedPackings%2F5x36_sol.txt | 2026-11-19T05:01:56Z |

Details in the-record-we-beat/.

## Not claimed

- Not an optimal packing, only one with a lower coherence than the leaderboard row; the listed lower bound 0.47519096 is 0.024 below mu.
- Only (5, 36). Each cell we claim has its own package.
- Not built from scratch: the object was started from the published (5, 37) packing named above (one vector removed), and is credited to its authors as a starting point.

## Credits

- John Jasper, Emily J. King and Dustin G. Mixon, the Game of Sloanes leaderboard, https://github.com/gnikylime/GameofSloanes (arXiv:1907.07848, https://arxiv.org/abs/1907.07848)
- djma, pull request 15 to the leaderboard repository (https://github.com/gnikylime/GameofSloanes/pull/15), file 5x37_djma.txt: the (5, 37) packing the object descends from; a starting point of this object (one vector removed)
- JosiahPark, pull request 17 to the leaderboard repository (https://github.com/gnikylime/GameofSloanes/pull/17), file 5x37_grai.txt: the same (5, 37) packing, slightly polished, which the search was also given; a starting point of this object (one vector removed)
- the leaderboard's own AUTO entry (creator code `AUTO`: a vector removed from the best known packing for n+1), the posted (5, 36) packing the leaderboard lists (https://raw.githubusercontent.com/gnikylime/GameofSloanes/main/CurrentBestPackings/5x36_AUTO.txt, sha256 0f7fdbda471fa4d6535c55fb0d909b356a7e2383f3c85dbd0f45560436a782c5), which we compared against and which the search was given as a seed; the object does not descend from it
- JosiahPark, pull request 17 to the leaderboard repository (https://github.com/gnikylime/GameofSloanes/pull/17), file 5x36_grai.txt, which we compared against and which the search was given as a seed; the object does not descend from it
- djma, pull request 15 to the leaderboard repository (https://github.com/gnikylime/GameofSloanes/pull/15), file 5x36_djma.txt, which we compared against and which the search was given as a seed; the object does not descend from it
- dustinmixon, pull request 14 to the leaderboard repository (https://github.com/gnikylime/GameofSloanes/pull/14), file 5x36_sol.txt, which we compared against and which the search was given as a seed; the object does not descend from it
- Benjamin Meadows (search, checking and packaging; also the author of pull request 20 and of packing-records, https://github.com/TheBenMeadows/packing-records).
