# LABS, L = 463: energy 14047

## What
The 463-symbol +-1 sequence in sequence_L463.txt (the Table 3 L = 461 record of arXiv:2607.09688v1 with -1 prepended and +1 appended) has exact energy E = 14047, strictly below E = 14439 of the L = 463 sequence in Table 3 of arXiv:2607.09688v1 and below the previous best it quotes (F = 7.3885); absence of a lower L = 463 value in arXiv:2504.00987, the Boskovic et al. repository and newer arXiv work rests on the claimant's record, not on this check.

## Check it yourself
`sh verify-it-yourself/run_checks.sh` from this folder (python3 standard library). Expected last line: `PASS`.
Rough time on a laptop: under 5 seconds.

## Compared to
| table | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| arXiv:2607.09688v1, Table 3 | L = 463 | E = 14439 (F = 7.4233) | https://arxiv.org/abs/2607.09688 | 2026-10-16 17:41:48 (re-read by the NOVELTY skeptic 17:50:00) |
| arXiv:2409.07222 (ref [42] there) | L = 463 | E = 14507 (F = 7.3885) | https://arxiv.org/abs/2409.07222 | 2026-10-16 17:52:08 |
| arXiv:2206.12070 (ref [19] there) | L = 463 | E = 14779 | https://arxiv.org/abs/2206.12070 | 2026-10-16 17:52:09 |

Our sequence: E = 14047, F = 463^2/(2*14047) = 7.6304.

## Not claimed
- Nothing about any other length. In the same scan, L = 464 gave E = 14396 below Table 3's 14436; that is a separate
  cell, not panelled, not claimed here.
- No new search method: the object is the published L = 461 record of arXiv:2607.09688v1 with -1 prepended and +1
  appended (a trivial end extension of a published sequence). No optimality claim.
- arXiv:2504.00987 covers sizes up to 120 and the Boskovic et al. repository has no entry at L >= 450, so neither has
  an L = 463 value; an arXiv API search on verification day returned HTTP 429 and was not retried (the arXiv web search
  returned 200).

## Credits
- Blaz Psenicnik, Borko Boskovic, Jan Popic, Janez Brest: arXiv:2607.09688 (https://arxiv.org/abs/2607.09688), the L = 461
  record this object extends and the L = 463 value it is compared with.
- Blaz Psenicnik, Rene Mlinaric, Janez Brest, Borko Boskovic: Dual-step optimization (arXiv:2409.07222, Digital Signal
  Processing 165:105316, 2025).
- Miroslav Dimitrov: arXiv:2206.12070. Zhiwei Zhang, Jiayu Shen, Niraj Kumar, Marco Pistoia: arXiv:2504.00987.
- Tom Packebusch and Stephan Mertens: arXiv:1512.02475 (the problem's modern record of exact optima).
- Borko Boskovic et al.: https://github.com/borkob/git_labs.
- Contributor credit: elevenbrands.
