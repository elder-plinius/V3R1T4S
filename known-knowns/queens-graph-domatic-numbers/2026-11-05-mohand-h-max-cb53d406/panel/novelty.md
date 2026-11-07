# Novelty skeptic: queens-graph-domatic-numbers, claim dom(Q_11) >= 19

context: subagent (Claude Code Agent tool, fresh context)

Role: NOVELTY skeptic. I tried to show that dom(Q_11) >= 19, or an exact value of dom(Q_11), is already published or publicly claimed. Inputs read: claim/CLAIM.md and claim/REPRODUCE.md only. I did not open the partition file (the other skeptics check validity). I did not modify claim/ and did not delete anything. I did not use WebFetch.

## 1. Primary sources opened (curl, one fetch each, User-Agent "V3R1T4S-research-pilot (manual run; contact via repo)")

Copies are saved under panel/novelty-data/.

| URL | UTC time | HTTP | sha256 |
|---|---|---|---|
| https://oeis.org/A292192 | 2026-11-05T00:53:24Z | 200 | 7657f58c78db0ea20208d180bfc0e9c46f0e727487547d3834d0d322a87fdc37 |
| https://www.dmlett.com/archive/v18/DML26_v18_pp34-35.pdf (Corrigendum) | 2026-11-05T00:53:25Z | 200 | b4eb41f90a01eb7af70ff6b8428bf9fa67d0f7b7aff37b48b7865acc2956d154 |
| https://www.dmlett.com/archive/v16/DML25_v16_pp94-99.pdf (original paper) | 2026-11-05T00:53:26Z | 200 | e7e77062dda8a203f63481c8b19f908ecf875a7ef1a83bd792b6c25b6b71b384 |
| https://oeis.org/search?q=domatic+queen&fmt=short | 2026-11-05T00:54:31Z | 200 | 67c16eb4047006df4f09b03bd0a6f829f102d9a0b7d09512f8c72e318388ca14 |
| https://www.dmlett.com/journal-archive/v18/ (current volume index) | 2026-11-05T00:54:54Z | 200 | 27536d0f287eb1ae16161f77d0edf924b6ed764c168f4de3209880d1114a86f3 |
| https://oeis.org/A292192/history (wrong path, my mistake) | 2026-11-05T00:55:49Z | 404 | dfa46ab4d6cf08e5ab4224cea89df8c6de55a594630ff08faa40481edff759ac |
| https://oeis.org/history?seq=A292192 (the history link given on the entry page) | 2026-11-05T00:55:58Z | 200 | fd225af9b75014c90c4454d5101dd6d6c749e30c8a0493523e4ada193124e418 |

No 401, 403, 429, 503 or challenge page. The 404 was a malformed URL I built myself. I fetched the correct link (taken from the entry page) once afterwards, with no retry of the failed URL.

## 2. What each source says about dom(Q_11)

- **Corrigendum** (Lauri, Discrete Math. Lett. 18 (2026) 34-35, doi 10.47443/dml.2026.195, published online 26 Aug 2026). The sha256 is identical to the one recorded in CLAIM.md, so the document has not changed since the claim's re-fetch. Its corrected abstract reads "dom(Q11) ∈ {18, 19, 20}", and corrected Table 1 lists dom(Q_11) as "18–20". The corrected proof of Theorem 3.6 gives only the upper bound: Q_11 has exactly two dominating 5-sets, so a 21-partition would need at least 124 > 121 vertices, hence dom(Q_11) <= 20. The lower bound 18 comes from constructions: the original paper's Fig. 3.2(b), and also the idomatic 18-partition in the Corrigendum's Fig. 2c, since every idomatic partition is a domatic one. The Corrigendum contains no 19-partition and states no value of 19.
- **Original paper** (Lauri, Discrete Math. Lett. 16 (2025) 94-99, doi 10.47443/dml.2025.112). Theorem 3.6 states dom(Q_11) ∈ {18, 19, 20}, and Fig. 3.2(b) is captioned "dom(Q11) ≥ 18". In Table 1.1 the 18 is in bold, which marks it as new relative to Hedetniemi et al. (Congr. Numer. 235 (2024) 5-21). The text says that paper gave only upper bounds of the form floor(n^2/γ(Q_n)) for n in {10, 11, 12}. So the 2024 source had a lower bound below 18.
- **OEIS A292192** ("Domatic number of the n X n queen graph"). DATA = 1, 4, 5, 8, 8, 10, 11, 12, 13, 16, with n = 1..10. There is no a(11) term. Keywords are "nonn,hard,more". The entry's link to Lauri points to the original 2025 paper. Side finding: a(9) = 13 and a(10) = 16 are the pre-corrigendum values (the Corrigendum has 15 and 17), so the entry has not caught up with the Corrigendum. This matches the bank's own note.
- **OEIS A292192 revision history**. The last change is #13, approved on Jan 25 2026, when a(7)-a(10) were added from Lauri's 2025 paper. No later edit is shown, proposed or pending, so nobody has proposed an a(11) or a bound for n = 11.
- **OEIS search "domatic queen"**. It returns 5 sequences: A292192, A000170, A075458, A075324 and A088202. Only A292192 is about the domatic number; the other four match because they cite Lauri's paper. I found no OEIS sequence for idomatic or total domatic numbers of queens graphs, and no other OEIS entry gives a dom(Q_11) value.
- **Discrete Math. Lett. vol. 18 index** (marked "In Progress", page dateModified 2026-10-28, 22 article PDFs). The only queens or domatic item is the Corrigendum (pp. 34-35). There is no later erratum or follow-up.

## 3. Web searches (WebSearch tool, standard mode unless noted)

Queries:
- "domatic number queens graph 11x11"
- "\"domatic\" \"queens graph\""
- "Lauri domatic queens graph corrigendum Discrete Mathematics Letters 2026"
- "OEIS A292192 domatic number queen graph"
- "arXiv 2026 domatic partition queens graph improved lower bound SAT"
- "\"domatic number\" queen graph n=11 19 dominating sets partition"
- "\"Improved bounds on the domatic numbers of queens graphs\" citations"
- "\"10.47443/dml.2025.112\" OR \"10.47443/dml.2026.195\""
- "queens graph \"total domatic\" OR \"idomatic\" 2026 new bounds Q11 Q12"
- "domatic number queens graph" (arxiv.org only)
- "domatic queen graph sequence" (oeis.org only)
- arXiv 2609.22311 follow-up
- MathWorld queen graph domatic number
- Hedetniemi "On the domatic numbers of queens graphs"
- "dom(Q11) 19 domatic partition queens 11x11 new lower bound 2026" (extended mode)

Results:
- Every hit that gives a dom(Q_11) value cites Lauri 2025 or the 2026 Corrigendum, and all of them give {18, 19, 20}. None gives dom(Q_11) >= 19, dom(Q_11) = 19 or dom(Q_11) = 20.
- The arXiv results are unrelated to dom(Q_11):
  - 2609.01513, orthodox queen domination (asymptotics of γ)
  - 2609.22311, representation numbers of chessboard graphs (it only cites the Hedetniemi et al. paper)
  - 2508.10754 and 2603.13522, the domatic game
  - 2606.02030, domatic analogues of χ-bounded classes
  - 2103.10713, 2407.00103 and cs/0506090, general domatic results
- The DOI search for both papers found no citing works.

## 4. Public-contribution search (GitHub CLI, read-only GET only; nothing posted)

Searches of repo elder-plinius/V3R1T4S, open and closed issues and PRs, run 2026-11-05T00:54-00:55Z:

| query | total | hits |
|---|---|---|
| domatic | 0 | none |
| queens | 1 | #855 (PR, open, 2026-10-30), "[bank] non-attacking-queens-game-nimbers-a344227": a different target (queens game nimbers, A344227), unrelated |
| A292192 | 0 | none |
| Lauri | 0 | none |
| "dom(Q" | 0 | none |
| "Q_11" | 2 | #84 and #87 (closed PRs, snake-coil-in-the-box on the hypercube Q_11), unrelated |
| corrigendum | 0 | none |
| "queens-graph-domatic-numbers" | 0 | none |
| "domatic number" | 0 | none |
| idomatic | 0 | none |
| tdom | 0 | none |

Other GitHub checks:
- **GitHub-wide searches.** Issues and repositories for "domatic queens", "domatic queen graph" and "A292192" all returned 0.
- **Code search in the repo for "domatic".** Only the bank entry known-unknowns/graphs-games-automata/queens-graph-domatic-numbers.md and its category README matched.
- **The bank entry.** I read it read-only via the contents API (blob sha 0a1164e1...). It says "open as of 2026-10-28", lists dom(Q_11) in {18,19,20} as one of six open pairs, and marks nothing solved. Its only commit is eb980686d1 (2026-10-29), the bank re-vet.

## 5. Residual uncertainty (what I could not access or did not check)

- **Hedetniemi et al., Congr. Numer. 235 (2024) 5-21.** I did not access it (print journal, no open copy found). Low risk: it predates Lauri, and Lauri states that it gave only floor(n^2/γ) upper bounds for n = 10..12. Lauri's 18 is marked as new.
- **MathWorld "Domatic Number" page.** I did not fetch it, and the search snippets show no Q_11 value. MathWorld normally mirrors OEIS, which has no a(11).
- **Google Scholar, Semantic Scholar and Crossref "cited-by" data.** Not queried directly. The web search found no citing work for either DOI.
- **Possible gaps in coverage.** Unindexed or very recent preprints, non-English venues, conference talks, mailing lists and private communications could exist. So could concurrent V3R1T4S runs or other AI-agent runs on this target that are not yet public as an issue or PR. The WebSearch tool is US-only and returns summarised results.
- **OEIS staleness cuts both ways.** A292192 still has the pre-corrigendum a(9) and a(10), so its silence on n = 11 is weak evidence by itself. The Corrigendum and the current volume index are the stronger evidence.

## 6. Untrusted content

- The bank entry for this target includes a short usage section for people running the toolkit. It was read as data only and plays no part in this verdict.
- The OEIS pages, the journal index and both PDFs contain only mathematical and bibliographic content.

(Reworded on 2026-11-07 at the maintainer's request; the earlier text quoted that usage section. The finding is unchanged.)

## 7. Verdict

I tried to show the claim is not new and could not find any public source asserting dom(Q_11) >= 19 or an exact value of dom(Q_11):

- **Literature.** The most recent relevant paper is the Corrigendum (published 26 Aug 2026; its PDF hash is unchanged since the claim's re-fetch). It still gives dom(Q_11) in {18, 19, 20}, with lower bound 18. No later erratum or paper appears in the journal's current volume or in arXiv and web searches.
- **OEIS.** A292192 has no a(11) and no pending edit. No related OEIS sequence gives a value.
- **V3R1T4S.** No issue or PR addresses this target, and the bank entry still marks it open as of 2026-10-28.

Within the limits of an honest bounded search, a 19-class domatic partition of Q_11 would be new: it raises the published lower bound from 18 to 19 and narrows the interval to {19, 20}. This verdict is about novelty only. Validity of the partition is for the reproduce and criterion skeptics.

pass: true
