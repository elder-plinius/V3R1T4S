# LABS, L = 464: energy 14396

## What
The explicit +-1 sequence in claim/sequence_L464.txt (length 464) has exact aperiodic autocorrelation energy 14396, strictly below the L = 464 energies 14436 (arXiv:2607.09688v1 Table 3) and 14824 (arXiv:2409.07222 Table 2) that I decoded and recomputed, with the other named sources and any newer arXiv results covered only by the claimant's 2026-10-16 search record.

## Check it yourself
`sh verify-it-yourself/run_checks.sh` from this folder (python3 standard library). Expected last line: `PASS`.
Rough time on a laptop: under 5 seconds.

## Compared to
| table | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| arXiv:2607.09688v1, Table 3 | L = 464 | E = 14436 (F = 7.4569) | https://arxiv.org/abs/2607.09688 | 2026-10-16 20:13:13 (re-read by the NOVELTY skeptic 20:16:47) |
| arXiv:2409.07222 (ref [42] there), Table 2 | L = 464 | E = 14824 (F = 7.2617) | https://arxiv.org/abs/2409.07222 | 2026-10-16 20:13:13 (NOVELTY 20:17:20) |
| arXiv:2206.12070 (ref [19] there) | L = 464 | E = 15088 | https://arxiv.org/abs/2206.12070 | 2026-10-16 20:17:20 (NOVELTY) |

Our sequence: E = 14396, F = 464^2/(2*14396) = 7.4776.

## Not claimed
- Nothing about any other length. This is a separate cell from the contributor's L = 463 submission
  (2026-10-16-elevenbrands-24118ce2, draft PR #255); the L = 464 object is "-" prepended to that L = 463 sequence.
- No new search method: the object is the published L = 461 record of arXiv:2607.09688v1 with "--" prepended and "+"
  appended (a trivial end extension of a published sequence). No optimality claim.
- arXiv:2504.00987 covers sizes up to 120 and the Boskovic et al. repository has no entry at L >= 450, so neither has
  an L = 464 value; arXiv API searches on verification day returned HTTP 429/503 and were not retried (the arXiv web
  search returned 200). Newer LABS papers read by the NOVELTY skeptic (2610.14361, 2511.05778, 2511.04553, 2506.17391,
  2609.05771) report no L = 464 value.

## Credits
- Blaz Psenicnik, Borko Boskovic, Jan Popic, Janez Brest: arXiv:2607.09688 (https://arxiv.org/abs/2607.09688), the L = 461
  record this object extends and the L = 464 value it is compared with.
- Blaz Psenicnik, Rene Mlinaric, Janez Brest, Borko Boskovic: Dual-step optimization (arXiv:2409.07222, Digital Signal
  Processing 165:105316, 2025).
- Miroslav Dimitrov: arXiv:2206.12070. Zhiwei Zhang, Jiayu Shen, Niraj Kumar, Marco Pistoia: arXiv:2504.00987.
- Tom Packebusch and Stephan Mertens: arXiv:1512.02475 (the problem's modern record of exact optima).
- Borko Boskovic et al.: https://github.com/borkob/git_labs.
- Contributor credit: elevenbrands.
