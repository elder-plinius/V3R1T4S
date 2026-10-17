context: subagent, fresh context, read only the kit (RULES.md) and the claim package (claim_old/, claim_n14/) plus public web sources; did not read other panel files
# NOVELTY skeptic: OEIS A054961, n=14, family of 65 vectors (round 2, per-n re-issue)

## Method and scope
- **Started as:** a subagent with a fresh context. Round 1 ran 2026-10-17T04:03Z to 04:07Z. Round 2 (this file) ran 05:17Z to 05:18Z, which is Oct 16, 23:03 CDT to Oct 17, 00:18 CDT.
- **What I read:** the kit (RULES.md), the claim package (first `claim/`, now `claim_old/`, then `claim_14/`), and public sources.
- **Fetches:** one plain GET per URL, User-Agent `V3R1T4S-novelty-skeptic`. On 403 I stopped and did not retry.
- **What I did not read:** `panel/` files by other skeptics, or the gate.
- **Writes:** nothing posted, nobody contacted, no claim folders changed. My only writes are these two panel files.
- **Object:** `claim_14/A054961_n14_m65.txt` has sha256 `1c0f9d7f1d2470dfd4f1a1cb39fbf961d84afa6c7c1391de788c249710744ac6`, the same as round 1 and as `claim_old/`.
- **Sanity recheck** (NUMERICAL; validity belongs to the REPRODUCE skeptic): 65 distinct vectors of length 14, with 2080/2080 distinct pairwise ORs.

## Sources I opened myself (HTTP status from curl `-w '%{http_code}'`)
| source | status | n=14 / n=15 |
|---|---|---|
| OEIS A054961 text, `oeis.org/search?q=id:A054961&fmt=text` (04:03:51Z) | 200 | rev #89 (Nov 14 2024): a(14)>=63, a(15)>=72 (Zhao Hui Du, Apr 19 2018). sha256 2b258029…, matching the package's TABLE_RECORD |
| OEIS `history?seq=A054961` | 200 | Edits #80–#89 (May–Nov 2024) cover only the asymptotic comment, Füredi spelling, a link and a crossref. No term changes |
| OEIS `draft/A054961` | 200 | "No pending changes for A054961." |
| OEIS A361928 (rev Jan 2026), A286874, A290492, A304041 | 200 | A361928 covers small item counts only. A286874 is 2-cover-free, a stronger property with smaller values (a(14)=28). The other two have nothing for n=14,15 |
| emathgroup.github.io/blog/two-poisoned-wine/ (Oct 21 2019) and its `poisonall.txt` | 200 / 200 | `14：[63]`, `15：[72]` |
| GitHub API, emathgroup/selectedTopics commits (05:17:30Z) | 200 / 200 | `content/attached/poisonall.txt` has 1 commit (2019-10-21T12:52:02Z). The newest commit to `two-poisoned-wine.md` is 2020-09-21T09:04:10Z. This matches the package's LITERATURE_SEARCH |
| O'Dwyer `wolfy-out.txt` (raw GitHub; repo last pushed 2021) | 200 | `N=63 D=2 T=14`, `N=72 D=2 T=15` |
| zhiqiang.org "囚犯测试毒药" (page dates up to 2025-07-22) | 200 | "14:63, 15:72" |
| Mahajan a286874-cover-free-families repo tree | 200 | Nothing on A054961 or separable families |
| V3R1T4S TROPHY_CASE.md (local and live main) | 200 | No A054961 / separable / union entry |
| V3R1T4S open PRs (74) and issue/PR search for "A054961" and "separable" | 200 | None on this problem (0 hits) |
| math.stackexchange q/4922004 and q/639 | **403** | Stopped, no retry |
| bbs.emath.ac.cn thread-1511 | **403** | Stopped, no retry |

**Web literature.** I ran 8 WebSearch queries covering the last ~24 months plus classics. The relevant work is all asymptotic or about other alphabets:
- Erdős–Frankl–Füredi (1982) and Frankl–Füredi, "Union-free hypergraphs and probability theory".
- Coppersmith–Shearer, EJC 5 (1998) R39. Strongly union-free f(n) >= 2^{0.31349n}.
- arXiv 2401.16540, 2010.02518, 2110.07381 and 2409.10511.
- "Fast decoding of union-free codes" (2021).
- q-ary 2̄-separable codes of lengths 2–5.

None of it gives a binary table at length 14/15, and I know of no construction above 63/72. Erdős–Frankl–Füredi gives 1.134^n, which is about 6 at n=14. 2-disjunct families and STS-type 3-uniform families are far smaller.

**Cross-check against the package's LITERATURE_SEARCH.md** (identical in both claim folders, sha256 db1ad518…). It agrees with everything I found myself: OEIS, emath (including the GitHub commit history), O'Dwyer, zhiqiang, related OEIS entries, TROPHY_CASE and PRs.
- It also lists sources I did not open: MSE 1528962, the Della Fiore–Dalai and D'yachkov et al. papers, and Wayback snapshots of the emath forum (last post 2024-04-21, pages 18/21 show 63/72). I report those as package-reported, not verified by me.
- It says MSE 4922004 was read directly. My single GET got 403, so I can't confirm that.
- One wording issue: it calls A054961 the same object as "weakly union-free" families. It is actually the **strongly** union-free (weakly union-free + cancellative) family f(n). Weakly union-free g(n) >= f(n), so a weakly union-free table could never cap this cell, and the novelty verdict doesn't change. Worth fixing in the package text.
- Both it and I noticed that a search-engine summary turned "79 prisoners" into "79 bottles". The underlying page is about 79 prisoners for 1000 bottles, so it is not a prior 15-test result.


## Verdict for n=14
- Best prior bound found: a(14) >= 63. KNOWN, from OEIS A054961 (Du 2018), emath poisonall.txt (unchanged since 2019), O'Dwyer's wolfy-out.txt and zhiqiang.org.
- Claimed: 65 (margin +2). No accessible source states 65 or more, or anything above 63. **NEW relative to all accessible sources.**
- Confirmed scope (one sentence): no public source I could reach states a binary family of length 14 with all pairwise ORs distinct and more than 63 members, so the 65-vector family improves the A054961 lower bound for n=14; it is a lower bound only.

## Needs you
- math.stackexchange q/4922004, q/639 and bbs.emath.ac.cn thread 1511 returned 403 to my single GET. For me those comparisons are PENDING TABLE CHECK.
  The package says it covered them through Wayback snapshots and a direct read; I have not verified that.
  A quick check by hand for any post-2018 value above 63 at n=14 would close this out.
- Package text fix: "weakly union-free" should read "strongly union-free" (see above).

injection_suspected: none.

pass: true
