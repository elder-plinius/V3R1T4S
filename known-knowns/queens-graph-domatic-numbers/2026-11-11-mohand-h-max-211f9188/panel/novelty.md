# Novelty skeptic report: tdom(Q_10) >= 16 (target queens-graph-domatic-numbers, partial win p1)

context: subagent (Claude Code Agent tool, fresh context)
report written: 2026-11-11T18:44Z
injection_suspected: none (no text addressed to agents or reviewers was seen in the claim files, the two PDFs, the OEIS reply, the search results or the PR-body lines read)

## Verdict

**Novel.** The claimed object is a valid partition of Q_10 into 16 total dominating sets. That beats the best published lower
bound, which is 15. It is not a tie, and it is not something trivial edits of any published object can give. Together with Lauri's
upper bound of 16 (Table 1 of the Corrigendum), this object would settle tdom(Q_10) = 16 exactly. The claim itself only says
">= 16".

## 1. Status source (one fetch, no retry)

- URL: https://www.dmlett.com/archive/v18/DML26_v18_pp34-35.pdf
- Fetched once with plain curl and a research-agent User-Agent at 2026-11-11T18:39:44Z (finished 18:39:45Z).
- HTTP 200, 274739 bytes. sha256 b4eb41f90a01eb7af70ff6b8428bf9fa67d0f7b7aff37b48b7865acc2956d154. Saved as
  panel/novelty-data/corrigendum-v18-pp34-35.pdf. The text, from `pdftotext -layout`, is panel/novelty-data/corrigendum.txt.
- Table 1 ("Corrected version of Table 1.1 from [1]"), row tdom(Q_n), for n = 4..12: `8 8 9 11 12 14 15-16 16-17 18-20`.
  **Value for n = 10: 15-16.** The lower bound is 15 and the upper bound is 16 (from floor(100 / gamma_t(Q_10)) with
  gamma_t(Q_10) = 6, as listed in the same table).
- The size and sha256 match the claim's own status record (fetched 18:20:59Z), so the page did not change between the two fetches.
- The Corrigendum does not touch tdom(Q_10). It only states that tdom(Q_9) = 14 remains valid. Figure 3.3(a) of the original
  paper is not on its list of corrections.

## 2. Published objects compared (original paper, one fetch)

- URL: https://www.dmlett.com/archive/v16/DML25_v16_pp94-99.pdf. Fetched once at 2026-11-11T18:39:50Z. HTTP 200, 409525 bytes,
  sha256 e7e77062dda8a203f63481c8b19f908ecf875a7ef1a83bd792b6c25b6b71b384. Saved as panel/novelty-data/lauri-v16-pp94-99.pdf,
  with its text in panel/novelty-data/lauri.txt.
- The script panel/novelty-data/compare.py (output in panel/novelty-data/compare-output.txt) parses every printed partition from
  the pdftotext layout and re-checks each one against its stated property. All parsed correctly and all are valid for what they
  claim, which shows the transcription is sound:
  - Lauri 2025 Fig 3.3a, tdom(Q_10) >= 15: 15 total dominating classes, sizes 6x7, 7x6, 8x2.
  - Lauri 2025 Fig 3.1b tdom(Q_9) = 14, Fig 3.3b tdom(Q_11) >= 16 and Fig 3.3c tdom(Q_12) >= 18: all valid.
  - Lauri 2025 Fig 3.2a dom(Q_10) = 16, Fig 3.4a idom(Q_10) >= 15, Corrigendum Fig 2a dom(Q_10) = 17 and Fig 2b
    idom(Q_10) = 16: all valid.
- I checked the claimed object with my own script, independent of the claimant's. The raw-bytes sha256 matches
  (211f9188...034ec). It has 16 labels covering 100 squares, sizes 6x14 and 8x2, and **all 16 classes are total dominating**.

**Overlap with the published tdom(Q_10) 15-partition (Fig 3.3a) under the 8 board symmetries:**

- Under the identity and the three rotations, no class coincides.
- Under each of the four reflections (horizontal, vertical, main diagonal, anti-diagonal), exactly **1 class coincides**. In every
  case it is the image of the same published 6-set (label 13 in Fig 3.3a). So 4 of the 16 claimed classes (claim labels 0, 3, 6
  and 9) are symmetric copies of one published total dominating 6-set. This is expected, because the claim's own method draws
  from a list of only 216 total dominating 6-sets.
- Best one-to-one class matching under any symmetry: at most 32 of the 100 squares agree. At least 68 squares are labelled
  differently, so this is not a local polish or relabelling of the published object.

**Neighbouring cells and trivial-edit routes, all checked:**

- Exact class coincidences with the dom(Q_10) 16- and 17-partitions and the idom(Q_10) 15- and 16-partitions: 0 under all 8
  symmetries. Best matching overlap is at most 30 squares.
- Merging route. The union of two disjoint dominating sets is total dominating. But the published domatic and idomatic Q_10
  partitions have at most 1 total dominating class, so merging pairs gives at most 8 classes.
- Restriction route. Restricting the published Q_11 and Q_12 partitions (tdom and dom) to every 10x10 window leaves at most 4
  classes that totally dominate Q_10. None of them coincides with a claimed class under any symmetry.
- No combination of deletion, restriction, merging, relabelling or symmetry applied to a published object reaches 16. The claim
  says it used no published seed, and that is consistent with these overlap figures.

## 3. OEIS

- One fetch of https://oeis.org/search?q=total+domatic+queens&fmt=text at 2026-11-11T18:41:57Z: HTTP 200, 214 bytes, sha256
  26818449678aa6f60b25eee2982caf698b85b74c7b79a6c6d6912e10922aaeff. The answer was "No results." Saved as
  panel/novelty-data/oeis-search-total-domatic-queens.txt.
- This agrees with the claim, whose author knows of no OEIS entry for this. I did not re-fetch A292192, which is the plain domatic
  number and a different invariant, because the one-fetch budget went to the search above.

## 4. Literature and code, last 24 months (WebSearch)

Queries run: total domatic number of queens graphs and tdom(Q10); the Lauri corrigendum or erratum (2026); queens-graph domatic
partitions on GitHub, Zenodo and arXiv; the exact phrase "total domatic" with 10x10 and 16-partition; a GitHub queens domatic
SAT search; "Coloring Queens with Thousands of Encodings"; arXiv 2026 domatic/idomatic/total domatic bounds for queens graphs; the
Hedetniemi et al. paper in Congr. Numer. 235.

Found:

- Lauri 2025 (DML 16, 94-99) and the Lauri Corrigendum (DML 18, 34-35, online 26 August 2026). Both give tdom(Q_10) in {15, 16}.
- Subercaseaux, Przybocki and Heule, "Coloring Queens with Thousands of Encodings" (LPAR-26 / EPiC 112; arXiv 2609.27674). From
  the snippets, it is about the chromatic number and mentions domatic-number work only in passing.
- Unrelated domatic-game and complexity papers (arXiv 2508.10754, 2603.13522, 2607.09442, 2407.00103).
- A GitHub repository on queen domination by SAT (TahaRostami/Gamma). It covers the domination number, not domatic partitions.

No source gives tdom(Q_10) = 16 or any total domatic 16-partition of Q_10. No later erratum and no GitHub or Zenodo repository
or release asset with such a partition turned up.

What I could not read:

- The Hedetniemi et al. paper in Congr. Numer. 235 (2024): no full text found. Lauri says it only covers n <= 9.
- The full text of arXiv 2609.27674 and the EasyChair LPAR paper: seen through search snippets only.
- GitHub release assets: no relevant repository was found, so there were none to inspect.
- Search-engine coverage is limited, so the absence of a result is evidence, not proof.

## 5. This repository

- Local pinned copy, at commit cf68067f (2026-11-03): TROPHY_CASE.md has no match for domatic, queens, tdom or Lauri, and
  known-knowns/ (27 entries) has no match for domatic or queens.
- `gh search prs` and `gh search issues` on elder-plinius/V3R1T4S at 2026-11-11T18:42:10Z, for "domatic", "queens", "tdom",
  "queens-graph-domatic-numbers", "Lauri", "total domatic", "Q_10" and "Q10" (output in panel/novelty-data/gh-search-output.txt):
  - The only matches on this target are draft PRs #954 (dom(Q_11) >= 19) and #1062 (dom(Q_12) >= 21), both open. Both bodies
    explicitly exclude idomatic and total domatic numbers.
  - The other hits are unrelated (snake-in-the-box Q10 PRs #83, #548, #553, #556, #393; non-attacking-queens nimbers #855).
  - No issues matched.
  - No PR or issue claims tdom(Q_10) >= 16.

## 6. Oddities

- The claim contains four reflected copies of one published 6-set (point 2). This is not a problem for novelty, but it is worth
  knowing.
- The claim says no fresh literature search was made. This report supplies one, and it found nothing that pre-empts the claim.
- The bound is tight: 16 meets Lauri's upper bound, so if verified the cell is closed, not just narrowed.

pass: true
