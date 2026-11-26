# REPRODUCE verdict: constant-weight-codes, cell A(30,12,9)
context: fresh reviewer (new subagent context started for the REPRODUCE role only; saw only CLAIM.md, RECORD.md, object/, search/ and public pages; no access to the claimant's checker)
verdict_utc: 2026-11-26T20:22:12Z

## Definition used

A(n,d,w) is the largest number of distinct binary vectors of length n, each of Hamming weight exactly w, with all pairwise Hamming distances >= d. The success criterion in CLAIM.md asks for "an explicit list of M distinct binary vectors of length n, each with Hamming weight exactly w, with all pairwise distances >= d (d even), where M is STRICTLY GREATER ... than the lower bound shown at verification time in the (n,d,w) cell" and "M must not exceed the tabulated upper bound".

## Own checker, run before reading search/

Written from the definition above (Python standard library, words as ints, all 990 pairs computed, no sampling) and run on `object/A-30-12-9-45words.txt`:

- sha256 of the object file: 806649f74bcb4ec5746f248ef5f087f88d56120661f95e0d7a464d9965f9060d (matches CLAIM.md)
- 1 header line starting with `#`, 45 word lines, each exactly 30 characters from {0,1}
- every word has weight 9; all 45 words distinct
- 990 pairs; minimum distance 12
- distance histogram {12: 756, 14: 141, 16: 36, 18: 57}, i.e. intersection counts {3: 756, 2: 141, 1: 36, 0: 57} (matches CLAIM.md)
- coordinate degrees histogram {8: 3, 13: 3, 14: 18, 15: 6} (matches CLAIM.md)
- size 45: valid A(30,12,9) code

## Live table (fetched once with curl)

- https://aeb.win.tue.nl/codes/Andw.html fetched 2026-11-26T20:17:46Z (Date header), HTTP 200, Last-Modified Thu, 26 Nov 2026 15:24:18 GMT, Content-Length 129601, sha256 7429c8d2567123d043a5881bf67a3f1344b268b94a63af794eceefde2c165604 (identical to the sha256 in RECORD.md).
- Section "Bounds on A(n,12,w)", header columns w = 7..16; row n = 30, third data cell (w = 9): `44` (link `cwc/d12/a30.12.9.44`) `-74` (label Po). So lower bound 44, upper bound 74. 44 < 45 <= 74. The mirror cell A(30,12,21) is not a separate entry (the table lists w <= n/2).
- The Echols and Lysenstoen arXiv papers named in the criterion were not checked in this role; this verdict covers the object, the table cell and the reproduction.

## Seed file

- https://aeb.win.tue.nl/codes/cwc/d12/a30.12.9.44 fetched once, 2026-11-26T20:17:45Z (Date header), HTTP 200, Last-Modified Fri, 06 Mar 2026 14:40:17 GMT, Content-Length 1364.
- sha256 56d5cb3304998a0322d495e97dbb128b8c3710a8201bcdd080d75c0d72d2f4cd (matches CLAIM.md). My checker: 44 distinct weight-9 words of length 30, minimum distance 12, intersection counts {3: 760, 2: 98, 1: 31, 0: 57}.
- The object shares 0 words with the seed (minimum distance from each object word to the seed code: 2 for 6 words, 4 for 16, 6 for 13, 8 for 10).
- No 44-word subset of the object can have the seed's intersection counts: the seed has 760 pairs meeting in 3 positions and the whole object has only 756.

## Reproduction of the construction

- `search/bststate.cpp` read after the checks above. It reads the seed file, pads with the unique minimum-shortfall word, then runs the swap tabu search with an mt19937 generator seeded from the command line; timing only decides whether the run stops before solving.
- Compiler: the machine's `g++` is Apple clang 21.0.0, which has no `<bits/stdc++.h>`. I compiled an unmodified copy of the source with `clang++ -O2 -std=c++17 -Iinc`, where `inc/bits/stdc++.h` is my own shim that includes only standard headers (algorithm, chrono, climits, cstdint, cstdlib, fstream, iostream, random, string, unordered_set, vector). No change to the program's logic.
- Command, run under `nice`, single process: `./bststate 30 9 12 45 1008 300 out.txt a30.12.9.44 1 5 1000000000`
- Output on stderr: `padlib size 1 minpen 6 base 44` (44 seed words read, unique padding word with shortfall 6, as CLAIM.md states), then `SOLVED iter 19272004 restarts 0 steps 19272004 time 10.4266`. Exit code 0. Iteration count matches CLAIM.md.
- `out.txt` (45 lines) compared with the object file without its first `#` line: byte-identical (`cmp` silent; both sha256 1dc3534789a4f23293a3f665459a37e9d2730e92f586fc181f3ae647b3489b28) and equal as sets.

## Problems found

- Reviewer-side setup error, disclosed: my first launch of the program started before I had copied the seed file into the run folder, so it read 0 seed words (`base 0`) and searched from random padding. I stopped it after about 3 minutes without a result and discarded it. The single valid run above, with the seed file present and its sha256 checked just before launch, is the reproduction.
- `search/bststate.cpp` includes `<bits/stdc++.h>`, which is not available with Apple clang; the CLAIM.md build command (`g++ ...`) does not compile as written on macOS without a shim or a GNU toolchain. This is a portability note and does not affect the result.
- The claimed run time (53 to 74 seconds) differed from mine (10.4 seconds); CLAIM.md states the result depends only on seed and iteration count, and the matching iteration count and byte-identical output bear that out.

## Reasoning

Every property in the definition holds for the saved object on all 990 pairs: 45 distinct words, length 30, alphabet {0,1}, weight 9, minimum distance 12. 45 is strictly greater than the live lower bound 44 and does not exceed the upper bound 74. The stated intersection counts and coordinate degrees match my own computation. The seed file's sha256 matches, the object shares no word with it, and one deterministic run of the provided program on that seed reproduces the object byte for byte at the stated iteration count.

pass: true
