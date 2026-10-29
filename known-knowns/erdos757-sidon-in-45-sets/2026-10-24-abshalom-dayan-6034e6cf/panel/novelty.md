# Novelty skeptic report: erdos757-sidon-in-45-sets, partial win p2

context: subagent (fresh context, given only claim/, the web and the repo's TROPHY_CASE.md)

Files named below without a prefix are in panel_work/novelty/ (every fetched page, the fetch log fetch_log.txt, the search log websearch_log.txt, and two small checks I ran). Files with the prefix claim/ are the claim folder, which I read and did not modify.

## 1. What was claimed, as I read it

claim/CLAIM.md offers p2: an explicit abstract 3-uniform hypergraph H (claim/H.json, n = 101, m = 99) that is linear, F7-free, has pairwise distinct middles in label order (none at vertex 0 or 100, so m <= n - 2), with alpha(H) = 56, so 56/101 = 0.55446 < 5/9 = 0.55556 < 4/7 = 0.57143. H is the depth-8 chain of 9 copies of a 13-vertex block, each copy sharing two vertices with the next (claim/construction.json), asymptotic ratio 6/11 = 0.54545. The claim makes no statement that H is the A.P.-hypergraph of a real (4,5)-set; p2 does not require it.

## 2. Status source, read once, no retries

- URL: https://arxiv.org/html/2602.23282 (Ma and Tang, "Largest Sidon subsets in weak Sidon sets")
- Fetched 2026-10-24T12:31:38Z, HTTP 200, 462433 bytes, sha256 6b668ce63b00c5b81999adc934439b7feb2bc38daf0399f1777e37d451ac4608 (file status_arxiv_html_2602.23282.html; same hash as the run's scout copy, so the page is unchanged since 10:12Z).
- Value read: Theorem 1.6, 9/17 <= c_* <= 4/7. The 4/7 comes from the 14-point set A_base with h(A_base) = 8 (Lemma 5.1).
- Latest version: the abs page (arxiv_abs_2602.23282.html, fetched 12:31:39Z, HTTP 200) lists only v1 (26 Feb 2026) and v2 (6 Mar 2026). v2 is the version in claim/paper/.

Other live values read in the same minute (all HTTP 200):
- https://www.erdosproblems.com/757, 2026-10-24T12:31:39Z: "Ma and Tang [MaTa26] have improved these bounds to 9/17 <= c <= 4/7"; page last edited 10 April 2026; 7 comments, 0 proof claims (erdosproblems_757.html). The forum thread (erdos_forum_757.html, 12:35:00Z) has nothing after 27 Feb 2026 and posting is suspended. The history page (erdos_history_757.html, 12:35:02Z) shows no later edit.
- https://einsteinarena.com/problems/sidon-45-set, 2026-10-24T12:31:40Z: leaderboard top is "Ma-Tang Previous SOTA 0.571428571" (einsteinarena_sidon45.html). Verifier accepts at most 18 points. I also read threads 264, 268, 269, 270, 280, 282 (arena_thread_*.html).
- teorth/optimizationproblems constant 5b, raw file, 2026-10-24T12:35:02Z: upper bound 4/7 [MT26], lower 9/17 (teorth_5b.md).
- Community record (outside the three named sources): https://erdosproblemaday.com/day/757-reader-five-ninths-refereed, 2026-10-24T12:31:40Z: an anonymous reader's self-similar family with finite ratios (7+5K)/(11+9K), limit 5/9, first member below 4/7 at K = 6 (65 points, h = 37, 0.5692). The page itself says "5/9 is a limit, approached and never reached" (reader_five_ninths.html). Its problem page (aday_problem_757.html) lists that one attempt only.

So the live best ratio is 4/7 on the named sources and 5/9 as a limit (best finite real set known to me: 38/67 = 0.5672, hturcotte1 C005; every finite member of the reader family is above 5/9).

## 3. Question (a): does arXiv:2602.23282 exhibit or exclude such an H?

No. I read claim/paper/arxiv_2602.23282_v2.txt (and the live status page). The paper:
- proves the structural properties of A.P.-hypergraphs of (4,5)-sets (Lemma 2.4 distinct middles and m <= n - 2; Lemma 2.5 linear; Lemma 5.2 F7-free; Lemma 2.3 h = alpha) and applies Henning-Yeo (Theorem 5.3, 17 tau <= 5n + 3m) to get 9/17;
- exhibits exactly one hypergraph with small alpha/n, the one of A_base (n = 14, alpha = 8, ratio 4/7), and the Fibonacci hypergraph of Gyarfas-Lehel (3/5);
- states no tightness of 9/17, no class infimum, no abstract-class construction, and no obstruction that would rule out a hypergraph with these properties at ratio 56/101. Its only exclusion is alpha/n >= 9/17, and 56/101 = 0.5545 is above 9/17 = 0.5294, so H is not excluded.

For consistency I computed (not from the paper): H has Henning-Yeo slack 5n + 3m - 17 tau = 37 >= 0 (tau = 45), so H does not contradict the paper's theorem.

## 4. Question (b): has anyone posted an explicit H like this with alpha/n below the live best, or a statement that the class has infimum below 5/9?

Searched and found nothing. Details:

hturcotte1/Erdos-757 (an autonomous AI research repo, last push 2026-10-21; all 8 PRs closed; README, GOAL, LEDGER, FINAL_REPORT, STATE, kb/ notes, dead_ends, open_questions, ideas_backlog, known_results, experiments READMEs saved under h1/; full tree in h1_tree.json, 9770 entries, I did not read the roughly 9000 raw experiment files):
- It names the exact abstract class of the claim as an open question. kb/open_questions.md Q5: "c_hyp, the abstract-class constant (linear, F7-free, hereditary e(S) <= |S| - 2, injective midpoints): is it 9/17? ... Small-n part DONE, constant itself open ... The asymptotic constant is open." (h1/kb_open_questions.md, fetched 12:32:15Z). kb/literature/part2_supplement.md section 5 item 1 poses the same constant and says either answer is publishable.
- It states conjecture I11, 11 tau <= 3n + 2m, proved by computer for the abstract class C only for n <= 27 (L007-L011, L013, L016), "a [conjecture] in general", which would give c_* >= 6/11. No document says I11 is asymptotically tight, and no abstract chain is built. (h1/kb_notes_i11_conjecture.md.) The listed equality cases are (3,1,1), (10,7,4), (12,4,4), (13,8,5), (14,12,6) and disjoint unions; the claim's family is a different, connected, unbounded family with constant I11 slack 6.
- D27 (h1/kb_dead_ends.md, h1/exp_selfsim_README.md): self-similar two-point chains were scanned only over REALIZABLE seeds (54,243 twelve-point, 2,910 fourteen-point, 40,163 derived thirteen-point, 2,337 sampled fifteen-point). Result: nothing below 5/9. It derives that "n0 = 13 with g = 6" is one of the only improving cases (that is the claim's numerology: 6/11) but found no seed (the 13-point realizable minimum growth was 20/3), and says abstract seeds, trees, and sharing of three or more points were "Not run". So the target numbers were known, the abstract construction was not.
- Its abstract census table (h1/i11_abstract_table.md) has the cell (13, 11) with I11 slack 6 in the abstract ordered class (that is, a 13-vertex abstract block with 11 edges and tau 5 exists, as the claim's block). The gain in the claim comes from chaining; no chained abstract family appears.
- Henning-Yeo note (h1/kb_notes_henning_yeo_2021_affine.md): full text of Graphs and Combinatorics 37 (2021) not obtained; "whether the HY bound is tight in the range m <= n - 2 is unknown"; a random search found no example with 17 tau = 5n + 3m. No tight example with distinct middles is recorded.

Other posts:
- fortunto2/erdos-757-sidon45 (README, releases v1.0.0 to v1.1.2, tree): nauty enumeration of abstract linear 3-graphs with hereditary filters for n <= 23, only to rule out records below 4/7 for real sets. Nothing below 5/9, nothing at n = 101.
- EinsteinArena threads 264, 268, 269, 270, 280, 282: reformulation, the m <= n - 2 map, Henning-Yeo feasibility for n <= 18, the no-(16,9) result. No abstract construction.
- erdosproblems.com forum and history: nothing after Feb and Apr 2026.
- the-omega-institute/trureturing issue 9804 (Sept 2026): an inductive inequality conjectured to prove 4/7, refuted on real 12-point sets (ratio 7/12). No ratio below 4/7.
- vibemathing problem repo for #757: template harness; attempts.jsonl 785 bytes, results.jsonl empty.
- QuanyuTang/ep757-45set-base-block-verification: verification of A_base only (page fetched, nothing beyond it).
- arXiv: API queries (weak Sidon; (4,5)-set; Sidon plus arithmetic progression plus hypergraph plus transversal; Erdos Problem 757; Gyarfas Lehel Sidon; Sidon 3-uniform linear hypergraph; five distinct differences) return only arXiv:2602.23282 for the topic. Semantic Scholar lists no citing paper. General web search (seven queries, websearch_log.txt, covering the last 24 months) found no follow-up paper and no source for 6/11 or for the class infimum.
- TROPHY_CASE.md in the V3R1T4S repo (commit d14b0098, 2026-10-22): no entry for erdos757, Sidon, hypergraphs or this target (my grep hits were only the digits "757" inside unrelated numbers).
- Open pull requests of elder-plinius/V3R1T4S (GitHub API, 4 pages, 310 open PRs, v3_open_pulls*.json) and an issue search (v3_search_issues_757.json): the only PR on this target is #406 (p1 tie at 4/7 with a 21-element set, "not better"), plus closed #29 (same set). No PR claims p2 or any abstract hypergraph for this target. The code-search API returned 401 (anonymous code search is not allowed); I stopped there.

## 5. Question (c): is the specific construction (chains of a 13-vertex block, limit 6/11) already known?

Not found anywhere. The nearest items are the reader's 11-vertex chain (limit 5/9, realizable, a different block and a larger limit) and hturcotte1's D27 note that a 13-point seed with growth 6 "would improve" but none was found among realizable seeds. I also ran two independent checks on the claim (files novelty_check.py, chain_alpha_K0_8.txt):
- H from claim/H.json: n = 101, m = 99, linear, middles distinct and never an end vertex, alpha = 56 (OR-Tools CP-SAT, OPTIMAL, bound 56), ratio 56/101 < 5/9, I11 slack 3n + 2m - 11 tau = 6.
- Rebuilding the chain from claim/construction.json (labels ignored): K = 0..8 gives (n, alpha) = (13, 8), (24, 14), (35, 20), (46, 26), (57, 32), (68, 38), (79, 44), (90, 50), (101, 56): +11 vertices and +6 to alpha per copy, I11 slack 6 at every depth, so the limit is 6/11 and the ratio first drops below 5/9 at K = 8 (n = 101). Note that K = 7 gives 50/90 = 5/9 exactly, so the claim is at the smallest depth where it is strictly below.
I did not re-run F7-freeness or the label-order argument; those belong to the reproduction skeptic. My novelty finding assumes they hold as the claim's own checker reports.

## 6. Assessment

- Strictly beats the live best? Yes, as an abstract object: 56/101 = 0.55446 is below 4/7 (named sources), below 5/9 (the community limit, which no finite member of the reader family reaches), and below every finite ratio known for real (4,5)-sets (best 38/67 = 0.5672). It is not a tie: no source lists an equal or smaller ratio for any hypergraph of this class.
- The paper neither exhibits nor excludes it (section 3).
- What it does NOT do, so nobody overstates it: H is not shown to be the A.P.-hypergraph of a (4,5)-set, so it lowers no bound on c_*. Within the repo's own conjecture I11 (c_* >= 6/11 if true) the family would show that I11 cannot be improved on the abstract class; it also shows c_hyp <= 6/11 (c_hyp being the repo's Q5 constant), which is new relative to everything I could find.
- Residual risks (could not be closed): (1) the full text of Henning-Yeo 2021 is closed access and I could not read it, so a published tight example for 17 tau = 5n + 3m cannot be excluded outright; but any such example that also has distinct middles would have to beat I11, which is proved for n <= 27 on this class, and neither Ma-Tang nor any of the sources above cites one. (2) I read the documentation of hturcotte1/Erdos-757 and not its 9000 raw experiment files, and that repo is moving fast (it posted the reader verification on 2026-10-20 and 21); a later abstract-chain run there would not be visible. (3) Search-engine coverage of the last 24 months is limited; the arXiv API and Semantic Scholar showed only the single Ma-Tang paper on this topic.

## 7. Fetch compliance and injection notes

- Fetch log: fetch_log.txt (UTC time, HTTP status, URL, saved file, sha256, bytes; 91 lines). One GET per URL. Exception to disclose: my first three arXiv API calls used http:// and returned HTTP 301 with an empty body; I then issued the same queries once each over https:// (new URLs), not as repeats of a blocked fetch. No 403, 429 or 503 occurred. HTTP 401 only on the GitHub code-search API (stopped). HTTP 404 for one guessed GitHub path (aday_gh_verif_757.json), not retried. No browser user agent, cookies or challenge bypass.
- Nothing was posted, commented, registered, submitted or opened. I wrote only inside panel_work/novelty/ and this file.
- injection_suspected: low. The README.md and GOAL.md of hturcotte1/Erdos-757 are written for a Claude Code session (they tell an agent to paste a /goal command, to "send continue", to choose a model and effort). They are addressed to that repo's own operator, not to this run, and I ignored them. No page tried to redirect this task.
- Pages are data; I followed no instruction found in any page.

## 8. Verdict

Nothing found that exhibits, excludes, ties or beats this H. The result is novel as far as the status source, the three named sources, the community record, hturcotte1's repo documentation, the arXiv API, general web search, TROPHY_CASE.md and the open pull requests show, with the three residual risks in section 6. Novelty only; correctness and the value of an unrealized abstract target are for the other two skeptics.

pass: true
