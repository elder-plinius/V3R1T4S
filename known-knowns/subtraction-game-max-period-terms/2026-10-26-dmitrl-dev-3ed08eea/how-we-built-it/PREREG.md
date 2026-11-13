# PREREG: subtraction-game-max-period-terms, cell A389690(23) (run 2026-10-26-0708)

frozen: 2026-10-26T07:10:01Z (date -u), before any computation in this run.

Disclosure: an earlier run (2026-10-26-0459) already computed this term under its own pre-registration (not shipped;
frozen 2026-10-26T05:02:17Z, sha256
9ae4e15bf9656f093da80b904642db1d7a66fafb4b70462a56d03e7150a4d41a, before that run computed anything at n >= 19 for
Sprague-Grundy). This run repeats the computation from scratch with the same programs and the same rule, so that the
second cell has its own claim and package (one object per package).

## Criterion (verbatim from the bank, repo 8846324)
CONFIRMED: the exact value of the next unknown term (A389689 at n = 24, or A389690 at n = 23), or of any later term once those are filled, using the entries' own definitions (S ranges over all subsets of {1, ..., n} that contain n; the period is the minimal eventual period, found as the first repeat of the length-n window of outcomes or Sprague-Grundy values), with all of: (1) an explicit maximising set S whose period an independent program recomputes exactly; (2) two independently written exhaustive searches over all 2^(n-1) sets that agree on the maximum AND on the full histogram of periods (number of sets with each period); (3) the term is not yet in the OEIS entry, its b-file or its history at verification time. Submitting to OEIS is an action for the human only.

## Programs and statistic
- A: how-we-built-it/A/subper_a.c, sha256 caaea9ae9aed77381ff7f5d17ed1203039205659c10d22bd7142618f96700fe7 (unchanged from the earlier run).
- B: how-we-built-it/B/src/main.rs, sha256 21287066503f79117013fc65f177083bc6619039ce0d70cc3ff60f79e0d77ab8 (unchanged).
- Statistic: maximum period over all 2^22 sets S with max S = 23, first maximising set in mask order, full histogram.

## Decision rule (all must hold)
1. A and B finish the full range (A overflow 0; counts sum to 2^22).
2. A and B agree on the maximum, the first maximising set and every histogram line.
3. The OEIS program's own sg_eventual_period (https://oeis.org/A389690/a389690_2.txt, demo loop removed) and a
   standard-library reference implementation (not shipped) give the maximum for the reported set.
4. A and B reproduce A389690 n = 1..22 with equal histograms.
5. The term is absent from the entry, b-file and history at the first status fetch and again before any claim (the last
   fetch is in the-record-we-beat/RECORD.md).

null_test: not needed because the term is a deterministic exhaustive computation checked by two independent programs and the OEIS program, with no search statistic or "beats chance" component.

## Caps
At most 5 concurrent threads or processes; 60 minutes per program. Claims stay PROMISING unless the human approves a
fresh-context panel (approved for this claim at about 2026-10-26T05:37Z).

Paths updated 2026-10-28 at the maintainer's request (PR #781 review); the rule is unchanged. The frozen text
(sha256 2cae6c4dd30838e689e3b41093f7081c91ca7e32f7edce5979754ed9a04a374b) is in commit
0b431acbcd04ed0e52376c38de42348c8442973f of this pull request.
