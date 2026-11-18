# baseline/record.md — step 3c (empirical benchmarks), ebl-fragment-identification

## Baseline 1: eBL statistics endpoint vs the bank entry
- Reproduced: GET https://www.ebl.lmu.de/api/statistics → HTTP 200
  live = {"transliteratedFragments": 39105, "lines": 636187.0, "totalFragments": 328942}
- Expected (bank entry, 2026-10-20): {"transliteratedFragments": 38586, "lines": 627690, "totalFragments": 328409}
- Coordinator pre-flight (2026-11-17 21:40 UTC): {"transliteratedFragments": 39105, "lines": 636187, "totalFragments": 328942}
- **Reproduced == pre-flight: True** (corpus grew since the bank
  entry: 38,586→39,105 transliterated fragments, 627,690→636,187 lines, 328,409→328,942 total).
  Tolerance: exact match to the live value (a statistics snapshot, not a score).

## Baseline 2: calibration of the independent aligner + eBL TF-IDF matcher on KNOWN-identified fragments
(positives = fragments whose museum number appears in a corpus chapter's manuscript list, i.e.
already identified in eBL; 591 such fragments among the 39,017 transliterated, 12 checked here)
- 12/12 : the independent banded Smith-Waterman aligner
  (match +3 / mismatch -1 / gap -2 / wildcard +1, min_block 6) recovers the known chapter as the
  top-ranked alignment for the known chapter's fragment.
- 9/12 : eBL's public ngram-matcher TF-IDF strategy (re-implemented
  offline from the frozen dumps, n∈{1,2,3}, idf=log(N/(df+1))+1, N=229) ranks the known chapter
  inside its top-10 for 9 of 12; the 3 misses are cases where a DIFFERENT chapter of the same
  composition outranks it (top-10 is over chapters, and same-composition chapters dominate).
  This is exactly the behaviour condition (d) exploits: the TF-IDF top-10 is chapter-granular and
  composition-aware, so 'the correct composition in the top-10' is a meaningful gate.
- What was NOT reproduced within budget: the in-platform lineToVec matcher
  (/api/fragments/{id}/match, 403-public per the related target) — re-implemented only as the
  ngram TF-IDF baseline the bank names (eBL's own matcher for the public route). The lineToVec
  line-structure ranking was re-derived from ebl-api source (commit 545294b, rank_line_to_vec)
  but not run over all 39k fragments (budget); it is used qualitatively for condition (d).
- Could not reproduce: an independent external aligner's published numbers (none exist for eBL
  fragment identification — the task is open-ended; no published baseline score to beat).
