# A linear [157,10,102] code over GF(4), one above the live lower bound

## What

The object is a valid [157,10,102] code over GF(4) (rank 10, exact minimum distance 102 by full enumeration of all 4^10 - 1 messages, 5304 minimum-weight words) whose distance strictly exceeds the live lower bound 101 (upper 110) and is not implied by the live neighbours.

The sentence above is quoted word for word from `panel/gate.md` (status `CONFIRMED_SOLUTION`). The object is `object/new_win_q4_n157_k10_d102.json` (sha256 40b6f0180e9248f1b86c69053b8c5e200f01156b917179cc619c63f659469d81); its programs are in `how-we-built-it/`.

## Check it yourself

From this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Requirements**: `python3` 3.8 or later, standard library only; a C compiler is optional (it runs a second implementation).
- **Rough laptop time**: about 4 seconds on the packager's machine; allow a minute or two on a slow laptop.
- **Expected last line**: `PASS`

The quick check verifies the object's hash against INDEX.csv, computes the rank and the exact minimum distance by full enumeration of all 4^k - 1 messages (standard-library Python, meet in the middle), compares both with the live bounds in `the-record-we-beat/`, repeats the distance in C if a C compiler is present, and confirms that a rank-deficient copy is rejected. The checker alone: `python3 -I verify-it-yourself/mindist_gf4.py object/new_win_q4_n157_k10_d102.json`, whose last output line begins: `{"n": 157, "k": 10, "messages_nonzero": 1048575, "expected": 1048575, "rank_k": true, "min_distance": 102, "A_d": 5304, "claimed_d": 102}`. Its real output is in `verify-it-yourself/RECEIPTS.md`. The checker differs from the one the panel ran only in file locations and the last output line (see RECEIPTS.md).

## Compared to

| Source | Cell | Listed value | URL | UTC fetch time |
|---|---|---|---|---|
| BKLC cell page | [157,10] over GF(4) | lower 101, upper 110 | http://www.codetables.de/BKLC/BKLC.php?q=4&n=157&k=10 | 2026-10-19T04:35:39Z (package); 2026-10-19T05:15:56Z (novelty skeptic) |
| V3R1T4S TROPHY_CASE.md and known-knowns folders | this cell | no competing value (see `panel/novelty.md`) | https://github.com/elder-plinius/V3R1T4S | 2026-10-19T05:15:21Z (novelty skeptic) |
| arXiv, four generic queries plus the named work 2609.37056 | this cell | no newer claim found (queries were generic, not exhaustive; see `panel/novelty.md`) | https://arxiv.org/abs/2609.37056 | 2026-10-19 (novelty skeptic) |

Ours: [157,10,102]_4 linear code over GF(4), value 102; the table value in `INDEX.csv` is "lower 101 upper 110". Each page was fetched once, with a plain GET and no retry; snapshot metadata (HTTP status, sha256 of the page, the extracted cell) is in `the-record-we-beat/README.md`. The panel's reports are in `panel/`.

## Not claimed

- The minimum distance is one above the live lower bound (and below the live upper bound); nothing is claimed about the upper bound, about any other cell of the table, or about the code being optimal.
- The exact distance was computed by full enumeration of all 4^k - 1 messages. The package checker and the panel's own programs are all the same enumeration idea (some in Python, some in C); no structurally different method (for example a Brouwer-Zimmermann style bound, or the weight enumerator through the dual code and the MacWilliams identities) was run.
- The construction field says the code is a one-column extension of a [156,10,101] code over GF(4) from the same search; that code is not in the live table (the live lower bound for [156,10] is 100) and is not claimed here. The gate found this code not obtainable from the live table or its live neighbours (padding, puncturing, shortening or taking a subcode).
- The comparison with the arXiv record is limited to four generic queries plus the named work 2609.37056 (seven binary codes of length 172 to 200, which cannot concern GF(4)); a paper listing a code of this size that those queries missed is not excluded.
- Unresolved from the panel: the Magma-generated Brouwer and Grassl tables carry no later data than the page fetched; whether an unpublished or non-arXiv code exists for this cell cannot be settled from public sources.
- Not peer reviewed. The package was checked by three fresh Claude Code subagents (reproduce, novelty, criterion) and by the standalone checker shipped here. The object was built by a different model family (Gemini, the contributor's search agent); the skeptics and the packager are Claude.

## Filing history

New submission for this cell; no merged result and no open pull request by another contributor concerns it.

## Credits

- **codetables.de** (http://www.codetables.de/), the table compared against, maintained by Markus Grassl as the bank statement for this target names it.
- **LinCodeEvolve**, arXiv:2609.37056 (https://arxiv.org/abs/2609.37056), the work the success criterion names; compared against, not built on.
- The object and the search code are by Gemini ("Argon"), an AI search agent working for the contributor. Contributor credit: `calgulbenkian`.
- The three panel reports are by fresh Claude Code subagents (`panel/`).
