# Pre-registration v3 — pass 2: odd lengths whose only public competitor is a GitHub continuation value

Sealed 2026-10-24T16:31:03Z (from `date -u`), **before any pass-2 output exists**. `PREREG.v2.md` continues to bind pass 1. Nothing
here changes it.

## 0. Known at sealing

Pass 1 is running. Only its first length has finished: L = 587, E = 25285 (F 6.8137) against B(587) = 27477. Calibration
at L = 579 (before PREREG.v2) gave F 6.687 in 180 s. That run is not part of any claim.

## 1. Criterion

Verbatim as in `target.md` and `PREREG.v2.md` section 1. Bar B(L) is computed exactly as in PREREG.v2: the minimum of the
best rotated/periodically-extended Legendre sequence, every public sequence of length L, and every end-derivation
(0..2 removed / 0..2 added per end, all signs) of public sequences of lengths L-4..L+4
(`code/legendre_bar.py` -> `data/bar_pass2_odd.json`, sha256 18a934c5be77947e562b217482af4ba50d1a6d79f4282bb732627b7fca255730). For these lengths the public
values are the GitHub mdayan8/labs-continuation sequences (not on arXiv), so here a record means beating someone's
actual sequence, not only a construction. A record at L requires E < B(L).

## 2. Target set, bars and budgets (frozen; easiest bars first)

| L | B(L) | F at bar | source | budget |
|---|---|---|---|---|
| 535 | 22139 | 6.4643 | mdayan8 all_best_this_work.tsv | 300 s |
| 567 | 24827 | 6.4746 | mdayan8 all_best_this_work.tsv | 300 s |
| 583 | 25991 | 6.5386 | mdayan8 all_best_this_work.tsv L=579 remove 0/0 add 2/2 | 300 s |
| 585 | 26700 | 6.4087 | mdayan8 all_best_this_work.tsv | 300 s |
| 531 | 20933 | 6.7348 | mdayan8 all_best_this_work.tsv | 450 s |
| 533 | 21446 | 6.6234 | mdayan8 all_best_this_work.tsv | 450 s |
| 569 | 24224 | 6.6826 | mdayan8 all_best_this_work.tsv | 450 s |
| 581 | 25122 | 6.7184 | mdayan8 all_best_this_work.tsv | 450 s |
| 529 | 20280 | 6.8994 | mdayan8 all_best_this_work.tsv | 600 s |
| 571 | 23453 | 6.9509 | mdayan8 all_best_this_work.tsv | 600 s |
| 575 | 22999 | 7.1878 | mdayan8 all_best_this_work.tsv | 600 s |
| 577 | 23740 | 7.012 | mdayan8 all_best_this_work.tsv | 600 s |
| 579 | 24481 | 6.847 | mdayan8 all_best_this_work.tsv | 600 s |

## 3. Method

Identical to PREREG.v2 section 3 (same `search.py` flags, same head-arm scaling rule, random starts only, never seeded
from a published or constructed sequence), except: budget per length as in the table, seed = 2000 + L, Python from
the workspace venv `venvs/labs-gpu`. Code unchanged since PREREG.v2: `code/gpu/skew_kernels.cu` c366e248c1a87f54b8e988e5b9a2e9974979f25c642a21a1df22c6cfef16898a,
`code/gpu/search.py` 89923c635120db49c025e4f31f1e3f147fe393e551a2af88011627e7c656077b, `code/gpu/labsgpu.py` 84d54ed2acd7b38f4512956dd1d5380bb1a4e832a8a14b987c35ce7c7022ecfc.
Starts automatically when pass 1's process exits; runs in the order of the table.

## 4. Verification

As PREREG.v2 section 4 (independent stdlib checker against B(L), numpy recheck, skew check, symmetry-minimised distance to
the bar-defining sequence and to the public sequence at length L).

## 5. Forecast

Beats the bar at 535, 567, 583 and 585 (bars F <= 6.54): likely, 3-4 of 4. At 531, 533, 569 and 581 (6.62-6.73):
2 of 4. At 529, 571, 575, 577 and 579 (6.85-7.19): at most 1 of 5, because these continuation values come from the
arXiv:2607.09688 L = 573 record and are strong.

## 6. Reporting and stopping

All 13 lengths reported, failures included. No new search starts after 20:40 UTC.

null_test: not needed because each claim is an explicit sequence whose exact integer energy is checked by a deterministic checker against a fixed numeric bar
