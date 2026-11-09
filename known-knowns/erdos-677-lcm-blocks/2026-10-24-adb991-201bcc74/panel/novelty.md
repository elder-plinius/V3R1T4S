# NOVELTY skeptic: Erdős 677 / JSP-000550, no counterexample with k ≤ 25 and n ≤ 10^494

context: subagent (fresh context, Claude Code Agent tool)

Inputs read: claim/ only (CLAIM.md, object/PROOF.md, source/). Work files are in panel_work/novelty/. Every request is
listed in panel_work/novelty/fetch_log.txt, with UTC time from `date -u`, HTTP status, sha256 and byte count. Each URL
was requested once with User-Agent "V3R1T4S-research-bot". No URL was retried after 401/403/429/503. Nothing was posted
and nobody was contacted.

## 1. Status fetch (primary)

| item | value |
|---|---|
| URL | https://raw.githubusercontent.com/TheJustinSunPrize/awards/main/problems/catalog-0501-0600.md |
| time (UTC) | 2026-10-24T10:28:17Z |
| HTTP | 200 |
| sha256 | 78ecc0e2a46520944d1b2f07196bd945433e82e4788a32585f22604c6b8b7834 (identical to the scout's hash in claim/CLAIM.md) |
| file | panel_work/novelty/catalog-0501-0600.md |
| status quoted | `## JSP-000550 · Must two disjoint equal-length intervals of consecutive integers have different least common multiples?` / `\| Current status \| Open \|` / `\| Lean proof \| No \|` / `\| Eligible to claim \| No \|` |

The problem page was fetched in the same pass. https://www.erdosproblems.com/677 returned HTTP 200 at 2026-10-24T10:28:17Z,
sha256 3d947ff293f44167b4a0a2a30dc9fa1882b04b520bca4a98ee5db40c5a22737f. Its sha differs from the scout's because the
HTML is dynamic, but the extracted text (panel_work/novelty/erdos_677.txt) is line-for-line identical to
claim/source/erdosproblems_677.txt.

## 2. What the problem page and forum record

- **Problem page /677:** The problem is open. The page has the statement M(n,k) ≠ M(m,k) for m ≥ n+k and this note:
  "The Thue-Siegel theorem implies that, for fixed k, there are only finitely many m,n …". That finiteness is
  ineffective, so it gives no explicit range. The only examples are of the different-length kind:
  M(4,3)=M(13,2) and M(3,4)=M(19,2). The page also shows "Proof expositions (0)", "Comments (8)" and
  "Proof claims (0)", and "This page was last edited 30 September 2025."
- **History /history/677:** There is one earlier revision (2025-10-20) with the same text. No partial result was ever
  recorded.
- **LaTeX /latex/677:** The same text, with references [Er79d] and [Gu04].
- **Forum /forum/thread/677:** 8 comments, dated 2026-03-31 to 2026-04-02.
  - They give more different-length examples: M(8,4)=M(43,2), M(153,3)=M(1363,2), and the M(·,·)=420 chain.
  - They link qrdlgit/erdos677, a Lean package. It proves fixed-gap finiteness, and SylvesterSchur.lean contains a
    `sorry`.
  - They link the Farhi–Kane lcm paper and a ChatGPT share.
  - One moderator-level reply calls the qrdl repo "likely too basic".
  - No comment reports a range verification or a solution. New comments are suspended.
- **Proof claims page:** "No proof claims have been submitted yet."
- **teorth/erdosproblems problems.yaml:** Problem 677 has status `open`, last_update 2025-08-31.

## 3. What was searched and found

Statuses are HTTP codes from the single request. "blocked" means a proxy CONNECT 403, which was not retried.

| # | source | HTTP / result | what it holds about Erdős 677 (k ≤ 25) | covers the claim? |
|---|---|---|---|---|
| 1 | prize catalog (above) | 200 | JSP-000550 Open, Lean proof No | no |
| 2 | erdosproblems.com /677, forum, proof-claims, history, latex | 200 ×5 | open; nothing beyond Thue–Siegel finiteness | no |
| 3 | arXiv API, last 24 months, 12 queries: Erdős 677, lcm + consecutive, lcm + interval, products/product of consecutive integers, blocks of consecutive, Thue + consecutive, lcm + Erdős, "Erdos problems", plus an undated lcm+consecutive sanity query | 200 ×12 | 0 hits on 677. Hits that are related but different: Cambie 2410.09138 (Erdős 678: the lcm ratio can be arbitrarily large), Tao 2603.27990 (bad intervals / factorial equation), Farhi–Kane 0808.1507 (the period of the product/lcm ratio) | no |
| 4 | Chan, arXiv 2408.01306v2 (updated 2025-03-27; Period. Math. Hung. 2025). PDF read | 200 | **Theorem 1:** b(b+1)(b+2) = 2a(a+1)(a+2) has only (a,b) = (3,4), which are overlapping blocks. By Lemma A (claim/object/PROOF.md), k = 3 forces r = 2, so **k = 3 is already settled for all n**. The paper also lists Cohn 1971, which covers only the k = 4 case with ratio 2. | covers only the k = 3 slice |
| 5 | Hajdu–Tijdeman 2204.12345; Shorey–Tijdeman survey 1612.05438 (abstracts) | 200 | General f(x)=g(y) / Erdős–Woods under abc; no explicit resolution of f(m) = r f(n) for k ≥ 4 | no |
| 6 | Saradha–Shorey 1990 "On the ratio of two blocks…"; Shorey 1984 "On the ratio of values of a polynomial" | not read first-hand (publisher/IAS full text not reached); scope from web search and a third-party audit (row 9) | Finiteness under extra hypotheses (x,y composed of fixed primes) and a gap bound. The special case solved is k vs 2k (unequal lengths). No effective classification for equal lengths. | no theorem found that settles any k ≥ 4 for all n |
| 7 | Danesh–Bianchetti, "Prime-Power Transport and a Three-Site Reduction", IJMTT 72(9) 2026 | **blocked** (403) | Known only second-hand (row 9). Reported search region: 1 ≤ k ≤ 150, 0 ≤ n < m ≤ 150000, no collision. Section 8.2 leaves **k = 6 unresolved** (four cubic branches). | no: the n bound 1.5·10^5 is far below 10^494, and k = 6 is open there |
| 8 | GitHub code/repo search (MCP): "erdos_677 lcmInterval", "erdos 677", "JSP-000550", "Erdos 677 counterexample verified" | ok | Hits checked, all partial: Kuberwastaken/c5-k4 (dict sweep n,m ≤ 2·10^5, k ≤ 12; complete-in-m n ≤ 40, k ≤ 24); kavanaghpatrick sketch; conjectures-io (lemma API only); dust-tt/srchd and plasma-ai wiki (open); vibemathing (template only); KDDavis91 (k = 5, ratio 4/3 curve visualisation, not exhaustive) | no |
| 9 | MaxwellLaw/erdos-677-research (shallow fetch, HEAD 2026-10-24) | ok | Lean-checked k = 6 reductions to four curves, with k = 6 explicitly unsolved. Its PRIOR_WORK.md is a same-day prior-work audit listing: rjwalters/lean-genius (k = 1,2 for all n; k = 3 for n ≤ 3); the-omega-institute/trureturing PR #8768 (scan N = 40000, k ≤ 24); grandchallenge MATH-PROGRAMME #1948 (small scan); formal-conjectures PR #2946 (m,n < 100, `sorry`). The repo's own conclusion: no complete k = 6 proof, no counterexample. | no |
| 10 | qrdlgit/erdos677 (API 403; then raw README 200 + shallow git fetch) | 403 / 200 | Window-lcm lemmas and fixed-gap finiteness; `sorry` in Sylvester–Schur; no range | no |
| 11 | Farhi–Kane PDF (cseweb.ucsd.edu) | **blocked** | The arXiv abstract (row 3) shows it is about the period of g_k, not equal lcms | no |
| 12 | erdosproblemaday.com/day/677-lcm-bridge; Tao blog post | **blocked** ×2 | Not read. Per the row 9 audit, the July 2026 page "does not claim to close k=6". The Tao paper abstract (row 3) is off-topic. | not known to |
| 13 | V3R1T4S TROPHY_CASE.md (raw) | 200 | No Erdős 677, JSP-000550 or lcm entry. The only "677" match is a matrix-multiplication rank 1677. | no |
| 14 | V3R1T4S pull requests: API **403**; `git ls-remote` 615 PR heads (308 open by /merge ref) + shallow blobless fetch of all heads + 1290 Erdős/README blobs grepped | ls-remote ok | No PR path or title mentions 677 / JSP-000550 / lcm blocks. The 4 blob "677" matches are hex substrings of sha256 values. | no |
| 15 | Prize repo TheJustinSunPrize/awards pull requests: API **403**; `git ls-remote` 4580 PR heads (1609 open) + shallow blobless fetch; titles and paths grepped, and the JSP-000550 section of all 261 distinct PR versions of catalog-0501-0600.md diffed against main | ls-remote ok | **#3543** (closed): "Lean proof Yes" pointing to a file proving only primality of 2…11 and 550 % 3 = 1. **#4288** (open): points to plby Erdos550.lean, which is Erdős #550 (Ramsey), the wrong problem. **#4846** (open): jsp550.lean, one closed `decide` conjunction checking lcm(1..3) ≠ lcm(4..6) and lcm(2..5) ≠ lcm(6..9). PRs #1–#5 used an older numbering in which JSP-000550 was a different problem. #2412 and #3298 are JSP-000677, a different entry, with `True := trivial` content. No PR changes the status from Open. | no |
| 16 | Web search (5 queries: Saradha–Shorey; Erdős 677 computation; the f(m) = r f(n) equation; equal-lcm disjoint intervals; Danesh–Bianchetti) | ok | Nothing beyond rows 4–12 | no |

Files: panel_work/novelty/fetch_log.txt lists every request. The other evidence files are:
- panel_work/novelty/jsp_pr_hits.txt
- panel_work/novelty/jsp_catalog550_differs.txt
- panel_work/novelty/jsp_files/
- panel_work/novelty/v3_pr_hits.txt (empty)
- panel_work/novelty/v3_blob_hits.txt
- panel_work/novelty/chan.txt
- panel_work/novelty/repos/

## 4. The workspace's other claim (n ≤ 5871·k)

CLAIM.md says that neither claim contains the other. Checked: this is **correct**.
- (k, n) = (26, 0) is in the earlier claim but not this one, since this claim needs k ≤ 25.
- (k, n) = (6, 10^6) is in this claim but not the earlier one, since 10^6 > 5871·6 = 35226.

For k ≤ 25 the earlier claim's range, n ≤ 5871·k ≤ 146775, lies entirely inside this claim's range. So the only extra
coverage the earlier claim adds is k ≥ 26. Neither claim appears in V3R1T4S (rows 13–14), so neither is "already
known" from the repo.

## 5. Call

The best known coverage for 1 ≤ k ≤ 25 is:
- **k ≤ 2:** settled for all n. This is elementary, and also Lean-checked in rjwalters/lean-genius.
- **k = 3:** settled for all n by Chan 2025, Theorem 1 (read first-hand).
- **4 ≤ k ≤ 25:** only finite searches.
  - The largest reported is Danesh–Bianchetti 2026, with n < m ≤ 1.5·10^5 for k ≤ 150. Its m cap makes it weaker
    still.
  - Others: c5-k4 (n,m ≤ 2·10^5 for k ≤ 12), trureturing (N = 40000, k ≤ 24), and the workspace's own unpublished
    n ≤ 5871·k.
  - k = 6 is explicitly open in Danesh–Bianchetti and in MaxwellLaw (2026-10-23/24).
  - No theorem in the literature I could check settles any k ≥ 4 for all n, or gives an explicit bound anywhere near
    10^494. Thue–Siegel gives only ineffective finiteness.
- **Prize side:** the catalog, the problem page and every PR record the problem as open. None records a range result.

The claim covers k ≤ 25 for n ≤ 10^494 with m uncapped. No known result (published, preprint, problem page or forum,
proof claims, either repository's PRs, or the GitHub hits) contains this range. For every k from 4 to 25 it pushes
the verified n-range from about 10^5 to 10^494, so it strictly beats the known finite results and is not a tie.

Caveats the panel should weigh:
1. **The k ≤ 3 part is not new.** k ≤ 2 is trivial, and k = 3 for all n is Chan 2025. The record should say that
   k = 1..3 are already settled for all n, and that the new content is 4 ≤ k ≤ 25 for n ≤ 10^494.
2. **Danesh–Bianchetti 2026 could not be read first-hand** (proxy 403). Its scope comes from the third-party audit in
   MaxwellLaw/erdos-677-research (docs/PRIOR_WORK.md, cas/SOURCE_AUDIT.md). That audit says Section 8.2 leaves k = 6
   open and reports a finite search to 1.5·10^5. Even if the paper settles k = 4 and 5 for all n, it cannot contain the
   claim, because k = 6 is open there. That would only shrink the new content to 6 ≤ k ≤ 25.
3. **Full texts of Saradha–Shorey 1990 and Shorey 1984 were not reached.** The available abstracts and secondary
   accounts show only finiteness, gap bounds, or the k-versus-2k case. A theorem settling equal-length ratios for
   k ≥ 4 would contradict the open status recorded on erdosproblems.com and in the 2026 papers.
4. Novelty only. Whether the computation is correct (patched pre-filter, non-interval window bounds, not
   kernel-checked) is for the other skeptics.

Verdict: the claim's range is not covered by anything known and strictly extends the known verified range for
4 ≤ k ≤ 25. Pass, conditional on the record noting the k ≤ 3 prior coverage (caveat 1).

pass: true
