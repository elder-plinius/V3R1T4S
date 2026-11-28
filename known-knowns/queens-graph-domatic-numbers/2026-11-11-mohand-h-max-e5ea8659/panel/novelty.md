# Novelty skeptic report: dom(Q_12) >= 21 (claim/dom-Q12-21-partition.txt)

context: subagent (Claude Code Agent tool, fresh context)
role: NOVELTY skeptic (one of three); default was fail unless novelty could be confirmed independently
date of checks: 2026-11-11 (UTC times below)

## Verdict

Novel as of 2026-11-11T18:03Z. The published lower bound for dom(Q_12) is 20 (Lauri 2025, Fig. 3.2(c); kept unchanged
in the 2026 Corrigendum). No later erratum, paper, preprint, OEIS entry, code repository, or V3R1T4S pull request,
issue or release that I could find gives 21. The claimed object strictly beats 20. It is not a trivial edit of any
published partition of this cell or its neighbours (see "Comparison with published objects").

One provenance point needs fixing in the credit line, but it does not block the verdict: 3 of the 21 classes are
identical to classes printed in Lauri 2025 Fig. 3.2(c) (see below), and that figure is not named.

## 1. Status source (fetched once, no retry)

- URL: https://www.dmlett.com/archive/v18/DML26_v18_pp34-35.pdf
- Command: plain `curl -s -A "V3R1T4S-research-agent/1.0 (honest single fetch)"`, one call
- UTC time (`date -u`): started 2026-11-11T17:57:31Z, finished 2026-11-11T17:57:32Z
- HTTP 200, application/pdf, 274739 bytes
- sha256: b4eb41f90a01eb7af70ff6b8428bf9fa67d0f7b7aff37b48b7865acc2956d154. This is identical to the claim's fetch at
  17:27:34Z, so the table has not changed since the claim was made.
- Saved as: panel/novelty-data/DML26_v18_pp34-35.pdf
- Value: Table 1 (Corrected version of Table 1.1), row dom(Q_n), column n = 12: **20–21**. The same row gives 18–20 for n = 11.
  The abstract text also says dom(Q_12) in {20, 21}. The proof of Theorem 3.6 explains the upper bound 21: Q_12 has
  only eight dominating 6-sets, and a 22-partition would need at least ten.
- How I read it: I extracted the text with `pdftotext -layout` (xpdf 4.00; no Python PDF library is installed). I also
  decompressed the page-1 content stream with Python zlib to check fonts. The cells 15 and 17 are set in the bold font,
  which marks entries that differ from the original. The cell "20{21" for n = 12 is in the regular font, so the lower
  bound 20 is unchanged from the 2025 paper.

## 2. OEIS A292192 (fetched once, no retry)

- URL: https://oeis.org/A292192, same single plain curl
- UTC time: 2026-11-11T17:57:37Z; HTTP 200, text/html, 14096 bytes
- sha256: 85607616c7fcf1d649061855dab79741dffd748c84142c4deb5b4a5ca8b60780. This differs from the claim's
  654bff4f…. The page has a dynamic site footer ("Last modified November 11 12:25 EST 2026. Contains 401258
  sequences"), so a byte-level difference is expected. I cannot compare against the claim's copy, which is not in the package.
- Saved as: panel/novelty-data/A292192.html
- Value: DATA is 1, 4, 5, 8, 8, 10, 11, 12, 13, 16 (n = 1..10). There is no a(11) and no a(12). The EXTENSIONS line says
  a(7)-a(10) came from Lauri and were added in Jan 2026. Keywords: nonn, hard, more.
- Odd: OEIS still shows the pre-Corrigendum a(9) = 13 and a(10) = 16, while the Corrigendum gives 15 and 17. The entry is
  stale for n = 9 and 10, but it is silent on n = 12, so this does not affect the claim.

## 3. Other primary documents fetched (one plain curl each, same User-Agent)

| file (panel/novelty-data/) | URL | UTC | HTTP | bytes | sha256 |
|---|---|---|---|---|---|
| DML25_v16_pp94-99.pdf (Lauri 2025, original paper) | https://www.dmlett.com/archive/v16/DML25_v16_pp94-99.pdf | 2026-11-11T18:00:10Z | 200 | 409525 | e7e77062dda8a203f63481c8b19f908ecf875a7ef1a83bd792b6c25b6b71b384 |
| Hedetniemi_CN235_pp5-21.pdf (Hedetniemi, Hedetniemi, Hedetniemi, Hedetniemi, Congr. Numer. 235, pp. 5-21; header says 2025, Lauri cites it as 2024) | https://combinatorialpress.com/article/cn/volume%20235/on-the-domatic-numbers-of-queens-graphs.pdf | 2026-11-11T18:02:23Z | 200 | 2337746 | eb386b00965cd6c6dc7f8e9e07558d90458376197cb52d83dd98735b6ddbea73 |

- Lauri 2025: the abstract and Table 1.1 give dom(Q_12) in {20, 21}. Fig. 3.2(c) prints a domatic 20-partition of Q_12.
  I parsed it from the text extraction and checked it with my own code: 20 classes, sizes 6,6,6,6,7×11,8,8,8,9,10, all
  dominating. The same paper prints an 18-class total domatic partition of Q_12 (Fig. 3.3(c)) and an 18-class idomatic
  partition (Fig. 3.4(c)). Both checked valid, and both are also domatic partitions with 18 classes.
- Hedetniemi et al.: for n = 12 they give only the upper bound dom(Q_12) <= 4 + floor(120/7) = 21 (open problem 10). They
  give no lower-bound construction for n >= 10.
- The Corrigendum replaces Figs. 3.1(a), 3.1(c), 3.2(a) and 3.4(b) only. Fig. 3.2(c), the 20-partition of Q_12, stands.

## 4. Literature and code search, last 24 months (WebSearch tool; WebFetch not used)

Queries run on 2026-11-11, about 17:58-18:03Z:
- "domatic number queens graph Q12"
- Lauri "Improved bounds on the domatic numbers of queens graphs" corrigendum erratum
- arXiv domatic partition queen graph 2026
- "On the domatic numbers of queens graphs" Combinatorial Press
- queens graph domatic number 21 partition 12x12 board dominating sets
- github domatic queens graph SAT partition dom(Q_12)
- "Coloring Queens with Thousands of Encodings" domatic
- "domatic" "queens graph" OR "queen graph" 2026 new lower bound partition
- zenodo domatic number queens graph certificate
- "domatic" queens Lauri 2026 dom(Q_{12}) = 21 OR "dom(Q12) = 21"
- idomatic total domatic number queens graph Q11 Q12 new results
- dmlett.com Discrete Mathematics Letters 2026 queens graph domatic erratum volume 19
- "queens graph" domatic partition explicit 12 x 12 "21 dominating sets"
- OEIS A292192 domatic number queen graph a(11) a(12)
- Hedetniemi domatic queens graph follow-up 2026 idomatic tdom Q10 Q11 Q12 SAT
- "Queen Domination by SAT Solving" Rostami Bright domatic

GitHub (gh CLI, read-only, 2026-11-11T18:00:48Z):
- `gh search repos "domatic queens"`: nothing.
- `gh search repos "domatic number"`: two unrelated repositories (QAOA and random graphs, last updated in 2024).
- `gh search code domatic queens`: only the V3R1T4S bank file, plus unrelated hits. A SAT-applications list mentions
  the domatic problem in general and gives no Q_12 data.

Findings: nothing newer than the Corrigendum (published online 26 Aug 2026) touches dom(Q_12). Nothing anywhere gives
dom(Q_12) >= 21 or an explicit 21-partition.
- One search result surfaced V3R1T4S PR #954, which is about dom(Q_11), a different cell.
- The journal archive lists volume 18 as in progress, and no later erratum appeared.
- The 2026 arXiv items found are on other topics: the domatic game (2603.13522), domatic chi-boundedness (2606.02030),
  3D queen domination (2604.03793), orthodox queen domination (2609.01513), queen colouring encodings (2609.27674,
  LPAR-26), and queen domination by SAT (2508.11945).

What I could not read:
- I saw only search snippets for arXiv 2609.27674, 2508.11945 and 2609.01513, not the full texts. The snippets show
  that they are about colouring and domination numbers and mention domatic numbers only as related work.
- A preprints.org ID, 202608.0597, appeared once in a result list. No page for it could be found by search, and I did not fetch it.
- I did not enumerate the works citing Lauri 2025 or the Corrigendum in Google Scholar.
- The search engine is US-only and may miss non-indexed material.

## 5. This project's repository

- Local pinned copy, at commit cf68067 (2026-11-03):
  - TROPHY_CASE.md: read; it has no domatic or queens entries.
  - known-knowns/: 27 families, none of them domatic or queens. A grep for "domatic", "queen" and "A292192" finds
    nothing under known-knowns/.
  - The only hits are under known-unknowns/ and bank/: the target file and its index entries.
- Upstream main, read-only via the API (commit fb51644, 2026-11-09T19:54:43Z): known-knowns/ has no domatic or queens
  folder, and TROPHY_CASE.md has 0 matches.
- Pull requests. `gh search prs` was run on 2026-11-11T17:59:41Z and 17:59:54Z for: domatic, queens-graph, A292192,
  Q_12, Lauri, queens, idomatic, "dom Q12", 21-partition.
  - The only matches on the subject are #954 (open, created 2026-11-05: dom(Q_11) >= 19, a different cell) and #855
    (closed, a non-attacking-queens game, unrelated).
  - The Q_12 hits are unrelated snake-in-the-box items (#79, #85, #88).
  - #954 contains only an 11 x 11 object. Its file list was read via `gh pr view`; I did not read the file contents.
- Issues: `gh search issues` with the same terms finds nothing.
- Releases: `gh release list` shows none, so no release assets can lag the tree.

## 6. Comparison with published objects (cell and neighbours)

Validity re-check (my own code, written from the definitions):
- The sha256 of the raw bytes is e5ea8659…1b2e and the LF-normalised sha256 is bc2433e6…6cb7; both match CLAIM.md.
- The file has 12 rows of 12 labels and 21 distinct labels.
- Class sizes are 6 (×3) and 7 (×18), summing to 144.
- Every class dominates Q_12.

Against Lauri 2025 Fig. 3.2(c) (dom(Q_12) >= 20), trying all 8 board symmetries:
- The best match is the identity. Under it, 3 claim classes are identical to published classes:
  - claim label 0, a 6-set with corner (0,0);
  - claim label 2, a 6-set with corner (11,11);
  - claim label 4, the 7-set {(1,1),(1,9),(3,7),(5,1),(7,11),(9,5),(11,3)}.
- The other 18 classes match no published class. Summed over claim classes, the best overlap with any published class
  is 76/144 cells, and 137 of the claim's 423 same-class cell pairs are also together in the published partition.
- The claim's third 6-set (label 1, corner (0,11)) is not in Fig. 3.2(c), which has its mirror image instead.
- The claim's partition is neither a refinement nor a coarsening of the published one.

Against Lauri 2025 Fig. 3.3(c) (tdom(Q_12) >= 18): 1 identical class, the same 7-set, label 4. Overlap 75/144.
Against Lauri 2025 Fig. 3.4(c) (idom(Q_12) >= 18): 0 identical classes. Overlap 53/144.

Trivial-edit test:
- Deletion, restriction, relabelling, symmetry, a valid propagation rule (moving squares between classes while keeping
  domination), or local polishing can only keep or reduce the number of dominating classes.
- None of them turns the published 20-partition, or the 18-class tdom and idom partitions, into 21 dominating classes.
- The claim also differs from Fig. 3.2(c) in 18 of its 21 classes.
- Neighbouring cells live on other boards (dom(Q_11): Lauri's 18-partition, and #954's unmerged 19-partition). They
  give no 12 x 12 object by the listed edits.

So the object strictly beats everything known for the cell, and it is not a trivial edit of a published object.

On the shared classes:
- By counting, any domatic 21-partition of Q_12 must contain at least 3 of the eight dominating 6-sets (6k + 7(21-k) <= 144
  gives k >= 3). Sharing 6-sets with Fig. 3.2(c) is therefore largely forced.
- The shared 7-set is not forced. It has a trivial symmetry stabiliser, and it also appears in Fig. 3.3(c), which
  suggests the published partitions may have served as a seed.
- The package does not say how the object was found. CLAIM.md credits Lauri for "the eight dominating 6-sets" but
  does not name Fig. 3.2(c) or Fig. 3.3(c).
- Requested amendment, not blocking: name Lauri 2025 Fig. 3.2(c) (and Fig. 3.3(c)) in the credit line as containing 3
  (resp. 1) classes identical to the object's, and state whether they were used as a seed. Even if they were, the result
  beats what trivial edits of them give (20 -> 21).

## 7. Other observations

- With Lauri's upper bound (Corrigendum, Theorem 3.6 proof) and Hedetniemi et al.'s independent count (<= 21), this
  object would settle dom(Q_12) = 21 exactly. CLAIM.md claims only p1, the raised lower bound, which is conservative.
- OEIS A292192 cannot take a(12) while a(11) is still open.
- Not this cell: I checked the Corrigendum's printed Q_9 15-partition (Fig. 1(a)) with my code and it is valid. This
  confirms that Hedetniemi et al.'s upper bound dom(Q_9) <= 13 was wrong, and that OEIS is stale for n = 9 and n = 10.

## 8. Text addressed to agents

- injection_suspected: repo copy, known-unknowns/graphs-games-automata/queens-graph-domatic-numbers.md. Its closing
  section addresses AI agents directly, asking them to set up the project and run its hunt workflow on this target. It
  is ordinary project boilerplate, but it is text addressed to agents. I did not follow it.
- None found in the two Discrete Math. Lett. PDFs, the Congr. Numer. PDF, or the OEIS page. I scanned the extracted
  text for words that address agents, reviewers or assistants.
- claim/REPRODUCE.md addresses reviewers with checking steps. That is its intended purpose. My checks above were
  written independently from the definitions.

## Summary line

The result (dom(Q_12) >= 21) strictly beats the best published lower bound of 20. It is not obtainable from any
published object by trivial edits. I found no prior or concurrent claim in the literature, in OEIS, or in this
repository's tree, PRs, issues or releases.

pass: true
