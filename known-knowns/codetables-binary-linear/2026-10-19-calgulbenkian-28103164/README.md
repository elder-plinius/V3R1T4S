# A linear [163,11,104] code over GF(4), one above the live lower bound

## What

The object is a valid [163,11,104] code over GF(4) (rank 11, exact minimum distance 104 by full enumeration of all 4^11 - 1 messages, 7956 minimum-weight words) whose distance strictly exceeds the live lower bound 103 (upper 113); it is a refile of closed PR #101.

Path note: the sentence above is quoted word for word from `panel/gate.md` (status `CONFIRMED_SOLUTION`). The object is `object/win_q4_n163_k11_d104.json` (sha256 28103164e334b8d35cdcb6e2d2dac8be21a26b82a9acaad2b53d835d25456b8f); its programs are in `how-we-built-it/`.

## Check it yourself

From this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Requirements**: `python3` 3.8 or later, standard library only; a C compiler is optional (it runs a second implementation).
- **Rough laptop time**: about 8 seconds on the packager's machine; allow a minute or two on a slow laptop.
- **Expected last line**: `PASS`

The quick check verifies the object's hash against INDEX.csv, computes the rank and the exact minimum distance by full enumeration of all 4^k - 1 messages (standard-library Python, meet in the middle), compares both with the live bounds in `the-record-we-beat/`, repeats the distance in C if a C compiler is present, and confirms that a rank-deficient copy is rejected. The checker alone: `python3 -I verify-it-yourself/mindist_gf4.py object/win_q4_n163_k11_d104.json`, whose last output line begins: `{"n": 163, "k": 11, "messages_nonzero": 4194303, "expected": 4194303, "rank_k": true, "min_distance": 104, "A_d": 7956, "claimed_d": 104}`. Its real output is in `verify-it-yourself/RECEIPTS.md`. The checker differs from the one the panel ran only in file locations and the last output line (see RECEIPTS.md).

## Compared to

| Source | Cell | Listed value | URL | UTC fetch time |
|---|---|---|---|---|
| BKLC cell page | [163,11] over GF(4) | lower 103, upper 113 | http://www.codetables.de/BKLC/BKLC.php?q=4&n=163&k=11 | 2026-10-19T04:35:36Z (first fetch); 2026-10-19T05:15:59Z (novelty skeptic) |
| V3R1T4S TROPHY_CASE.md and known-knowns folders | this cell | no competing value (see `panel/novelty.md`) | https://github.com/elder-plinius/V3R1T4S | 2026-10-19T05:15:21Z (novelty skeptic) |
| arXiv, four generic queries plus the named work 2609.37056 | this cell | no newer claim found (queries were generic, not exhaustive; see `panel/novelty.md`) | https://arxiv.org/abs/2609.37056 | 2026-10-19 (novelty skeptic) |

Ours: [163,11,104]_4 linear code over GF(4), value 104; the table value in `INDEX.csv` is "lower 103 upper 113". Each page was fetched once, with a plain GET and no retry; snapshot metadata (HTTP status, sha256 of the page, the extracted cell) is in `the-record-we-beat/README.md`. The panel's reports are in `panel/`.

## Not claimed

- The minimum distance is one above the live lower bound (and below the live upper bound); nothing is claimed about the upper bound, about any other cell of the table, or about the code being optimal.
- The exact distance was computed by full enumeration of all 4^k - 1 messages. The package checker and the panel's own programs are all the same enumeration idea (some in Python, some in C); no structurally different method (for example a Brouwer-Zimmermann style bound, or the weight enumerator through the dual code and the MacWilliams identities) was run.
- This is a refile of an earlier filing of the same code (see Filing history).
- The comparison with the arXiv record is limited to four generic queries plus the named work 2609.37056 (seven binary codes of length 172 to 200, which cannot concern GF(4)); a paper listing a code of this size that those queries missed is not excluded.
- Unresolved from the panel: the Magma-generated Brouwer and Grassl tables carry no later data than the page fetched; whether an unpublished or non-arXiv code exists for this cell cannot be settled from public sources.
- Not peer reviewed. The package was checked by three fresh Claude Code subagents (reproduce, novelty, criterion) and by the standalone checker shipped here. The object was built by a different model family (Gemini, the contributor's search agent); the skeptics and the packager are Claude.

## Filing history

This package refiles closed pull request #101 ("[163, 11, 104]_4 vs d_lower=103"), which filed the same code (its sha256 begins 28103164, the fragment in that title).

## Credits

- **codetables.de** (http://www.codetables.de/), the table compared against, maintained by Markus Grassl as the bank statement for this target names it.
- **LinCodeEvolve**, arXiv:2609.37056 (https://arxiv.org/abs/2609.37056), the work the success criterion names; compared against, not built on.
- The object and the search code are by Gemini ("Argon"), an AI search agent working for the contributor. Contributor credit: `calgulbenkian`.
- The three panel reports are by fresh Claude Code subagents (`panel/`).
