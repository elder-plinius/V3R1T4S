# PREREG: brouwer-qary-unrestricted-a3-a4-a5, cell A4(12,8)

written_utc: 2026-11-20T14:06Z

## Timing, stated plainly

The code was found by computer searches that ran on 2026-11-18 and 2026-11-19 (UTC). This file was written after the search, after the table was re-fetched on 2026-11-20 and after the three reviewers were started, but before any of their verdicts was read. It freezes the judging, not the search; it is not a pre-registration of the search. The criterion is quoted from the public bank, `bank/targets.json` on the main branch of https://github.com/elder-plinius/V3R1T4S (read 2026-11-20). No threshold below was chosen by us.

## Criterion: brouwer-qary-unrestricted-a3-a4-a5

> Success means an explicit list of M distinct words over {0..q-1}^n (q in {3,4,5}) such that an independent script confirms all pairwise Hamming distances >= d, and M is STRICTLY GREATER (direction: max) than the lower bound for A_q(n,d) in the corresponding live table (https://aeb.win.tue.nl/codes/ternary-1.html, https://aeb.win.tue.nl/codes/quaternary-1.html or https://aeb.win.tue.nl/codes/5ary-1.html), re-fetched live immediately before claiming; '=' entries are exact and cannot be beaten; the improvement must not appear in the notes under the table or in an arXiv/journal search done on the day.

Cell: A4(12,8), table https://aeb.win.tue.nl/codes/quaternary-1.html.

## Statistic and thresholds

Exactly as in the criterion: every word has length 12 over {0, ..., 3}; the words are distinct; the Hamming distance of every pair (all M(M-1)/2 pairs, no sampling) is >= 8; M is strictly greater than the lower bound in the live table (128 when re-fetched on 2026-11-20) and the cell is not an `=` entry; M is not above the table's upper bound (240; a larger M would mean a bug); the notes under the table and a literature search on the day show no value >= M. null_test: not needed because the claim is an explicit object checked by a deterministic checker against a table value.

## Panel

Three fresh reviewers (REPRODUCE, NOVELTY, CRITERION), each started in a new context for its role, each seeing only the claim folder (CLAIM.md, RECORD.md and object/) and public pages, and each writing its own code; none sees the search code or our checker. The cell is dropped unless all three write `pass: true`.
