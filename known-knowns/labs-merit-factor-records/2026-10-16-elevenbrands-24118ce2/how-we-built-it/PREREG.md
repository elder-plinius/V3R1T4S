# PREREG: labs-merit-factor-records, run 2026-10-16-1741
frozen_at: Fri Oct 16 17:43:15 UTC 2026 (from date -u, before any attack program was run)

## Criterion (bank/targets.json, verbatim)
Success means an explicit +-1 sequence of length L with 67 <= L <= 600 whose exactly computed integer energy E = sum_{k>=1} C_k^2 is STRICTLY SMALLER (direction: min) than the best published energy for that L at verification time, taken as the minimum over the tables in arXiv:2607.09688, arXiv:2504.00987, the Boskovic et al. LABS records repository cited there, and any newer arXiv result. Compare integer energies, never rounded merit factors. For L <= 66 the optimum is proven; lower energy there means a bug.

## Judge (statistic)
baseline/labs_energy.py (copy of the dry-run checker, exact Python-int O(L^2) energy, alphabet and length check).
The search code (C) is never the judge: every candidate is re-scored by labs_energy.py.
Calibration done before this file (baseline/calibration_output.txt): all 35 sequences of Table 3 of arXiv:2607.09688v1
decode (hex -> last L bits, 0 -> -1) and reproduce the paper's 4-decimal merit factor exactly (all_match True).

## Scope of this run and thresholds
Attacked lengths: only the 35 lengths of Table 3 of arXiv:2607.09688v1, because only there the run holds an exact
published baseline E (the paper states each beats the previous best of refs [42] Psenicnik-Mlinaric-Brest-Boskovic 2025
and [19] Dimitrov 2022). Threshold per L: candidate E <= baseline_E(L) - 4 is a candidate record
(LABS energies of a fixed L share residue mod 4, so strictly smaller means at least 4 lower); E == baseline is a tie,
reported as a tie and never as a record.
Before any claim leaves this run: re-read the status source, read 2511.04553 and 2511.05778 tables and the Boskovic
repository for that L (the criterion's "any newer arXiv result"); until then a candidate is at most PROMISING.
Partial win p1 (skew record): no published per-L skew-symmetric table is in hand for L >= 121, so a skew candidate
that does not also beat the unrestricted baseline is reported as PENDING TABLE CHECK, never as p1.

Baseline table (E recomputed from the published sequence; F as printed in the paper):

| L | baseline E | paper F | skew-symmetric |
|---|---|---|---|
| 450 | 13009 | 7.7831 | no |
| 451 | 12625 | 8.0555 | yes |
| 452 | 13074 | 7.8134 | no |
| 455 | 13043 | 7.9362 | yes |
| 456 | 13288 | 7.8242 | no |
| 457 | 13532 | 7.7169 | yes |
| 458 | 13837 | 7.5798 | no |
| 459 | 14101 | 7.4704 | no |
| 460 | 13870 | 7.6280 | no |
| 461 | 13574 | 7.8282 | yes |
| 462 | 13811 | 7.7273 | no |
| 463 | 14439 | 7.4233 | yes |
| 464 | 14436 | 7.4569 | no |
| 465 | 14336 | 7.5413 | yes |
| 475 | 15197 | 7.4233 | yes |
| 476 | 15110 | 7.4976 | no |
| 477 | 15022 | 7.5732 | yes |
| 478 | 15115 | 7.5582 | no |
| 479 | 15007 | 7.6445 | no |
| 480 | 15160 | 7.5989 | no |
| 481 | 15016 | 7.7038 | yes |
| 482 | 15169 | 7.6579 | no |
| 483 | 15321 | 7.6134 | yes |
| 484 | 15646 | 7.4861 | no |
| 490 | 16005 | 7.5008 | no |
| 491 | 15957 | 7.5541 | no |
| 494 | 15955 | 7.6476 | no |
| 495 | 16155 | 7.5836 | no |
| 496 | 16308 | 7.5428 | no |
| 497 | 16568 | 7.4544 | no |
| 498 | 16825 | 7.3701 | no |
| 516 | 18278 | 7.2835 | no |
| 517 | 18150 | 7.3633 | no |
| 518 | 18463 | 7.2665 | no |
| 573 | 22558 | 7.2774 | yes |

## Null design
null_test: not needed because every claim is an explicit sequence checked by a deterministic integer checker against a table value (no search statistic, no "beats chance" claim).
