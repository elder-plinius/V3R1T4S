# NOVELTY panel: runs/2026-11-03-2146-drawings

context: subagent (novelty) -- fresh executor subagent; read only claim/ and the NOVELTY instruction (kit RUN.md step 6, panel_requests/2026-11-03-2146-drawings.md)

Claim under review: A155520 row 6, first missing term A(6,1) = 6 (flattened index 22); full row 6 = 6,2,6,9,11,4,4,4,2,15,8,2,0,6,12,0,0,1,4,6,0,4,4,0,8,4,0,0,0,4,0,0,0,1,2,0,0,2,0,0,0,1 (see claim/CLAIM.md, claim/object/).

## 1. Status source -- fetched once each, no retries (2026-11-03 16:50 EST)
- https://oeis.org/A155520 -> HTTP 200. Name "Triangle read by rows: A(n,k) is the number of ordered trees with n edges having k drawings."
  DATA: 1, 2, 3, 2, 4, 2, 6, 1, 1, 5, 2, 6, 9, 1, 4, 4, 4, 2, 1, 2, 2 (21 terms = rows 1..5). OFFSET 1,2. KEYWORD nonn,tabf,more.
  STATUS approved. %e "Triangle starts" shows rows 1..5 then "...". COMMENTS/FORMULA/LINKS contain no row-6 value
  (only row sums = Catalan, Sum k*A(n,k) = A014307(n), Klazar link). EXTENSIONS: only "Keyword tabf added by Michel Marcus, Apr 09 2013".
- https://oeis.org/A155520/b155520.txt -> HTTP 200, "# A155520 (b-file synthesized from sequence entry)", indices 1..21, last line "21 2". Index 22 absent.
- https://oeis.org/history?seq=A155520 -> HTTP 200, entries #1..#12 (newest #12 by Andrei Zabolotskii, Sep 24 2025, status approved;
  older page "start=10" read once for #1-#2: original DATA by N. J. A. Sloane/Emeric Deutsch, same 21 terms). No pending/proposed
  draft above #12; no revision ever added a row-6 term. All edits are formatting, link, keyword (tabf) and %e typo fixes.

## 2. Literature: Klazar 1997
- Author PDF https://kam.mff.cuni.cz/~klazar/twelve2.pdf (preprint of Eur. J. Combin. 18 (1997) 195-210; author notes the PDF may differ slightly from print) and
  Addendum https://kam.mff.cuni.cz/~klazar/add.pdf (Eur. J. Combin. 18 (1997) 739-740), read in full (text extraction).
- Section 5 treats w12 (drawings) only in aggregate: recurrence (39) and totals w12(n) = 1, 1, 2, 7, 35, 226, 1787, 16717, ... (= A014307).
  Sec. 6 gives only extremal values m12(n) = 1 (path) and bounds on M12(n), and poses "how to calculate efficiently for any given T the number w12(T)"
  as an open question. No per-tree w12 list or by-k distribution for n = 6 (or any n) is printed. The Addendum corrects other tables/values only.
- Consistency note: Klazar's Lemma 5.3 counts drawings as sequences of distinct trees; claim's sum k*A(6,k) = 1787 = w12(6) matches.
- ScienceDirect (publisher) copy returned 403 to the fetcher; the author's preprint was used instead.

## 3. Value searches (OEIS, 2026-11-03 16:51 EST)
- seq:6,2,6,9,11,4,4,4,2,15,8,2 -> "Sorry, but the terms do not match anything in the table."
- seq:1,2,2,6,2,6,9,11 (DATA tail + row-6 head) -> no match.
- seq:6,2,6,9,11,4 -> no match.
(No results x3, matching the disclosure in claim/CLAIM.md.)

## 4. Web / literature, last 24 months (2026 searches)
- Searches for "A155520", "ordered trees ... k drawings", and plane-tree drawing / leaf-deletion distribution (2025-2026 arXiv) found only the OEIS
  entry itself and older work (arXiv 1301.6327, "Ordered Partitions and Drawings of Rooted Plane Trees", aggregate count A014307 only;
  Callan bijections). Nothing prints A(6,k) or extends A155520.

## 5. Repo checks
- repo/TROPHY_CASE.md, repo/known-knowns/, repo/news/, repo/sealed-envelopes/: no mention of A155520 (only digit-substring coincidences in unrelated numeric files).
- repo/bank/targets.json and bank/proposed/: A155520 not named ("drawing" appears only in unrelated crossing-number/epigraphy targets).
- GitHub elder-plinius/V3R1T4S issues+PRs (open and closed), public search API for "A155520", "155520", "drawings": 0 hits; last 100 PRs: none mention it.

## 6. Neighbouring-cell / trivial-derivation comparison
- The cell is a single new OEIS term at the first absent index (22). Not obtainable from published objects by deletion/restriction/relabelling:
  the only published row-6 information is aggregate (row sum C_6 = 132, weighted sum 1787), which does not determine A(6,1).
- Caveat (not disqualifying): the first column 1,2,3,4,5 of DATA suggests A(n,1) = n, so the value 6 is pattern-predictable; but it is not stated or
  proved in the entry, history, Klazar 1997 or the Addendum, and an OEIS term counts by being computed, not guessed. The full row-6 list is likewise unpublished.
- Zero convention (row 6 has interior zeros) is a CRITERION question; it does not affect novelty of A(6,1) = 6.

## Verdict
A(6,1) = 6 at flattened index 22 is absent from the live A155520 DATA, b-file, comments/links/extensions and full edit history (no pending drafts);
Klazar 1997 + Addendum give only aggregate drawing counts; OEIS value searches and web/repo/PR searches are clean. The term is new.

pass: true
