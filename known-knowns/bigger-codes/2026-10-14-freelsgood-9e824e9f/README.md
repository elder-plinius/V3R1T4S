# A(27,6,10) >= 13026

## What

The supplied explicit list of 13026 distinct binary words of length 27 and Hamming weight 10 has pairwise Hamming distance at least 6, proving A(27,6,10) >= 13026.

PROVED-HERE: independent exhaustive checks establish the explicit lower bound. This improves the fetched lower bound by 39; it does not settle the exact maximum.

## Check it yourself

Python 3.10+ and a POSIX shell; no third-party packages:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. The full pair check took about 13 seconds in the review environment; allow roughly a minute on a typical laptop. Actual receipts are included. RUN_IT_YOURSELF.md gives exact rebuild and checksum commands.

## Compared to

KNOWN: Brouwer's table at https://aeb.win.tue.nl/codes/Andw.html fetched 2026-10-14T02:50:22.728485+00:00 lists `12987g–43529` for A(27,6,10). The equivalent complement cell is A(27,6,17). The candidate has 13026 words, a strict increase of 39. The fresh NOVELTY report records checks of the required papers, newer literature, upstream trophy entries and open pull requests. No equal or stronger value was found in the checked sources. Table metadata and hashes are under the-record-we-beat/.

## Not claimed

No optimality, exhaustive literature omniscience, unpublished-result exclusion, new upper bound, proof of the construction narrative, or historical discovery/preregistration provenance is claimed. No mathematical claims about the auxiliary shortening certificates from the supplied archive are included. Reviewers were distinct fresh contexts of the same model family, not humans or different models. Maintainer acceptance remains separate.

## Credits

The witness and reconstruction constants came from the user-supplied Gemini candidate archive; this package does not claim that the reviewing assistant discovered them. Submission credit: Freelsgood. Andries E. Brouwer maintains the comparison table (https://aeb.win.tue.nl/codes/Andw.html). Compared publications include William Echols (https://arxiv.org/abs/2608.13906), Christian Lysenstoeen (https://arxiv.org/abs/2607.19550), and the additional works listed in the novelty report. The comparison cell links its published group-code construction at https://aeb.win.tue.nl/codes/cwc/d6/i27.10; provenance of the candidate's constants is not independently authenticated. Independent review and packaging used the V3R1T4S protocol at https://github.com/elder-plinius/V3R1T4S, pinned to commit 7aca3835635e5323b48cdf3b5b59fcde502cab28.
