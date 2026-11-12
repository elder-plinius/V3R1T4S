# Novelty skeptic report: dom(Q_11) <= 19

context: subagent (Claude Code Agent tool, fresh context)

Claim judged: claim/CLAIM.md, an UPPER bound dom(Q_11) <= 19 (no partition of the 121 squares of the 11 x 11 queens
graph into 20 dominating sets), against the table value 18-20. This report judges novelty only (is the bound already
known, published, or a trivial consequence of something published). Whether the 681-step certificate is correct, and
whether a chain of refutations meets the bank's wording, are for the other two panel members.

All fetched material, with one line per request (UTC time, URL, HTTP status, size, sha256), is in
panel/novelty-data/ (index: panel/novelty-data/FETCHES.txt). One request per URL, no retries, a User-Agent naming the
project only.

## 1. Status source (fetched once)

- URL: https://www.dmlett.com/archive/v18/DML26_v18_pp34-35.pdf (J. Lauri, Corrigendum, Discrete Math. Lett. 18 (2026)
  34-35, doi 10.47443/dml.2026.195)
- Time: 2026-11-12T00:50:25Z. HTTP status: 200. Size: 274739 bytes.
- sha256: b4eb41f90a01eb7af70ff6b8428bf9fa67d0f7b7aff37b48b7865acc2956d154 (identical to the hash recorded in
  claim/table/scout.md and claim/CLAIM.md for the author's fetch of 2026-11-11T21:42:14Z).
- Saved as panel/novelty-data/lauri-corrigendum.pdf.
- Table 1, row dom(Q_n), n = 4..12: 8, 8, 10, 11, 12, 15, 17, 18-20, 20-21. Cell for n = 11: **18-20**.
- The replacement abstract text agrees: "dom(Q11) ∈ {18, 19, 20}".
- The corrigendum's own upper-bound argument for n = 11 (proof of Theorem 3.6 as corrected): exactly two dominating
  5-sets and none smaller, so a 21-partition needs at least 2*5 + 19*6 = 124 > 121 squares. That rules out 21 only.
  Nothing in the corrigendum rules out 20.

## 2. OEIS state

- https://oeis.org/A292192, fetched 2026-11-12T00:50:41Z, HTTP 200, sha256
  16408d711d9d45732b39c0798f3b933a9ed055c919bea2ac429d08c4a8796e20. Name: "Domatic number of the n X n queen graph."
  Data: 1, 4, 5, 8, 8, 10, 11, 12, 13, 16 (n = 1..10). Keywords nonn, hard, more. **No term for n = 11**, and no comment
  giving a bound for n = 11. (Side note: a(9) = 13 and a(10) = 16 are the values of the 2025 paper, not the corrected
  15 and 17 of the corrigendum; the entry has not been updated since Jan 25 2026.)
- Revision history https://oeis.org/history?seq=A292192, fetched 2026-11-12T00:54:56Z, HTTP 200, sha256
  9d8003dafce235a65a84f7a0938c5500dfe77209779912866d8d3b94ef714026: last revision #13, approved Jan 25 2026; no
  pending or later edit.
- Cross-references of A292192: A075458 (domination number of the queens graph, not a domatic number) and A157887
  (fetched 2026-11-12T00:50:53Z, HTTP 200, sha256 58a8546924c34a7df0cc8b02acac56de1da9553c4ab893146f3943fa44087930: the
  domatic number of the n-cube, unrelated to queens).
- OEIS search "domatic queen" (fmt=text), fetched 2026-11-12T00:50:54Z, HTTP 200, sha256
  5b9ca29f3166ba4e345a6a19e6bbdb1e74beb8d194f0ff7f6d67fc286f5b85aa: 5 hits (A292192, A000170, A075458, A075324,
  A088202). A292192 is the only domatic-number entry for queens graphs; no idomatic or total domatic queens entry.
- Conclusion: OEIS gives nothing for dom(Q_11); the interval is open there.

## 3. Literature and code search (last 24 months and earlier)

Web searches (WebSearch tool), each returned nothing that proves dom(Q_11) <= 19, determines dom(Q_11), or states
any upper bound below 20:
1. domatic number queens graph Q11
2. "domatic number" "queens graph" 2026
3. Lauri "Improved bounds on the domatic numbers of queens graphs"
4. "domatic" queens graph SAT DRAT upper bound 11x11
5. "dom(Q_11)" OR "dom(Q11)" queens domatic
6. arxiv domatic partition queen graph 11 x 11 board disjoint dominating sets
7. "dml.2026.195" OR "Corrigendum to Improved Bounds on the Domatic Numbers of Queens Graphs"
8. github domatic number queens graph SAT encoding
9. "Coloring Queens with Thousands of Encodings" domatic
10. Hedetniemi domatic idomatic total domatic numbers queens graphs
11. "queens graph" domatic number upper bound 19 OR "at most 19" 11
12. dmlett.com 2026 queens graph domatic total domatic idomatic
13. "domatic 20-partition" OR "domatic 19-partition" queens
14. queens graph domatic number thesis 2025 2026 SAT certificate unsatisfiable partition dominating sets 11x11
15. queens graph domatic Lauri (restricted to dmlett.com; the filter was not honoured, results generic)

Every result on the topic points back to Lauri 2025 (18-20 for n = 11) or the corrigendum (18-20). Other hits were on
queen domination numbers, 3D queens, the chromatic number, the domatic game, or complexity of domatic problems.

Direct sources:
- arXiv API, all:domatic AND all:queens (2026-11-12T00:51:50Z, HTTP 200): 0 results.
- arXiv API, all:domatic, newest first, 50 results back to 2001 (2026-11-12T00:51:57Z, HTTP 200): no entry mentions
  queens anywhere in title or abstract. 2025-2026 entries are on the domatic game, criticality, complexity, total
  domatic numbers of cubic graphs, and similar.
- Semantic Scholar citations of Lauri 2025 (doi 10.47443/dml.2025.112), 2026-11-12T00:53:53Z, HTTP 200: one citing
  paper, Subercaseaux, Przybocki, Heule, "Coloring Queens with Thousands of Encodings" (arXiv 2609.27674, LPAR-26).
  I fetched it once (2026-11-12T00:54:01Z, HTTP 200, sha256
  9168c86a53306cbb2a6a8797d5537722b04236ffbe32d1e10854a899076d18ae) and searched its text: the one domatic passage is
  a passing remark that such problems "have been attacked via SAT", citing Lauri. No bound for Q_11.
- Semantic Scholar citations of the corrigendum (doi 10.47443/dml.2026.195): 0. Citation indexes lag, so this is
  weak evidence, but it agrees with the web searches.
- Lauri 2025 original (https://www.dmlett.com/archive/v16/DML25_v16_pp94-99.pdf, 2026-11-12T00:54:32Z, HTTP 200,
  sha256 e7e77062dda8a203f63481c8b19f908ecf875a7ef1a83bd792b6c25b6b71b384): Table 1.1 lists dom(Q_11) as 18-20 and
  the upper bound came from floor(n^2/gamma). It says Hedetniemi et al. (Congr. Numer. 235 (2024) 5-21) gave "only
  upper bounds of the form n2/γ(Qn)" for n = 10..12, which for n = 11 gives 24. The paper links no code repository.
- GitHub (gh search repos: "domatic", "domatic queens", "queens graph domination", "queen graph SAT"; gh search code:
  "domatic queen", "domatic" "queens"): no repository or file on domatic numbers of queens graphs other than the
  challenge bank itself. The only 2026 domatic repository found (a general maximum-domatic-partition project) has no
  queen in its README and no releases. No release assets found anywhere on this topic.
- Journal site: no later erratum or paper on queens domatic numbers turned up in searches. The corrigendum (published
  26 August 2026) is the latest item.

Limits: no Google Scholar or MathSciNet/zbMATH query (none available without an account); a paper not indexed by the
search engine, arXiv or Semantic Scholar would have been missed.

## 4. Challenge repository elder-plinius/V3R1T4S

- Local copy (commit cf68067, 2026-11-03): TROPHY_CASE.md and every file under known-knowns/ contain no occurrence of
  "domatic", "queen" or "Lauri".
- Live main (gh api, head fb51644 of 2026-11-09T19:54:43Z): TROPHY_CASE.md (saved as
  panel/novelty-data/trophy-case-live.md, sha256 83af764f5a6551a5a27bbb135324931659bda04e60b66a2c0e711b991b356113) has
  no such occurrence either; no known-knowns folder name mentions queens or domatic.
- Pull requests, all states, searched with "domatic", "queens", "queen", "queens-graph-domatic-numbers", "Lauri",
  "dom(Q", "idomatic", "total domatic", "Q_11" (gh pr list): on this target only three, all open drafts by the claimant:
  #954 (dom(Q_11) >= 19), #1062 (dom(Q_12) >= 21), #1063 (tdom(Q_10) >= 16). All three are LOWER bounds. #1062 and
  #1063 state that they prove no upper bound. The only other queens hit is a closed PR #855 on queens-game nimbers
  (unrelated); #84 and #87 are snake-in-the-box. Issues searched with "domatic": none.
- PR #954 body, section "Not claimed", contains a parenthetical by the same contributors: "The contributors also
  computed an exact certificate that Q_11 has no domatic 20-partition". It says that certificate (lists of minimal
  dominating 5- and 6-sets and a rational LP dual) is not in DRAT/LRAT form and is not part of that package; the PR's
  file list confirms no such certificate is included. So the same bound was announced, without proof, by the same
  claimant on 2026-11-05. This is the claimant's own earlier statement, not a result of anyone else and not a
  published proof. It does not make the bound known in the sense of prior art. CLAIM.md does not mention it, though;
  I recommend one line there saying so, for transparency.
- The one comment on #954 (2026-11-06) is procedural (a file flagged by the repository's screening) and says nothing
  about any bound. #1062 and #1063 have no comments.

## 5. Is the bound subsumed by something published?

- floor(121 / gamma(Q_11)) = floor(121/5) = 24 (Hedetniemi et al.; Lauri 2025). Weaker.
- Lauri's corrected count: two dominating 5-sets, none smaller. For 21 parts: 2*5 + 19*6 = 124 > 121, excluded. For
  20 parts: 2*5 + 18*6 = 118 <= 121, not excluded (and if the two 5-sets intersect, 5 + 19*6 = 119 <= 121, not excluded
  either). So the published counting stops at 20.
- dom(G) <= delta(G) + 1: the corner square has degree 3*10 = 30, giving 31. Weaker.
- The uniform-weight LP (fractional) bound is 121/5 = 24.2. Weaker.
- Ruling out 20 needs information on how many disjoint dominating 6-sets (and 7-sets) can coexist, which no published
  source gives for Q_11. I found no general theorem that yields dom(Q_11) <= 19.

## 6. Could the object be a trivial edit of a published object?

The object is a non-existence certificate (two CNF encodings, a lemma chain, and DRAT proofs), not a construction.
Deletion, restriction, relabelling, symmetry, propagation or numerical polish of a published object cannot produce an
upper bound, and there is no published non-existence proof for 20 parts to edit. The only published objects used are
Lauri's 18-partition of Q_11, used (and named, claim/CLAIM.md, partitions/lauri-idom-Q11-18.txt) only as a
satisfiable cross-check of the encoding, and the corrigendum's counting idea, which the claim extends with new
lemmas (sizes 5, 6, 7 and 434 listed sets) to go one step further than the corrigendum's own argument. Not a trivial
edit; method novelty is not required anyway.

## Conclusion

- The best published upper bound for dom(Q_11) is 20 (Lauri, Corrigendum, Table 1, fetched today, unchanged hash).
  OEIS A292192 has no term for n = 11. No paper, preprint, thesis, code repository, release, citation, trophy-case
  entry, known-knowns folder, or pull request of anyone else gives dom(Q_11) <= 19 or determines dom(Q_11).
- The claimed bound 19 is strictly below 20: a strict improvement of the upper end of the open interval, not a tie.
- The only prior mention of the same bound is the claimant's own unproved parenthetical in draft PR #954; it is not a
  competing prior result.
- Not subsumed by floor(n^2/gamma), the corrigendum's count, delta + 1, or the uniform LP bound.
- Out of scope here but noted: claim/CLAIM.md says the final drat-trim check for the second encoding had not ended when
  the folder was built. Novelty does not depend on it; the result does.

On novelty alone, the claimed bound would be new if correct.

pass: true
