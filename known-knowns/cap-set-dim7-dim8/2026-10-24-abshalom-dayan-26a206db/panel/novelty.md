# NOVELTY skeptic verdict: cap_1104_n9.txt (target cap-set-dim7-dim8, partial win p1)

context: subagent (Agent tool, fresh context, claude-opus-5-5)
novelty: 1104 strictly beats every F_3^9 value I could find: the best published is 1082 (Edel's PG(8,3) 541-cap doubled; FunSearch says 1082 is the best known), and the best posted is an unrefereed 1084 (GitHub Noirsys/capset, created 2026-10-23). I found no affine cap of 1104 or more in AG(9,3), and no projective cap of 552 or more in PG(8,3).

## Bottom line

| quantity | best value found | source | 1104 vs it |
|---|---|---|---|
| affine cap, AG(9,3), published | 1082 | Edel/Bierbrauer table (PG(8,3) at 541) + doubling theorem; FunSearch notebook ("largest known cap set for `n = 9` has size `1082`") | +22, strict |
| affine cap, AG(9,3), any public claim | 1084 (unrefereed, witness posted) | github.com/Noirsys/capset, README and PUBLIC-WRITEUP.md, repo created 2026-10-23 | +20, strict |
| projective cap, PG(8,3) | 541 | Edel's cap page (last changed 2010-04-28); Bierbrauer & Edel 2012 survey, Table 1 | doubling 541 gives 1082 < 1104 |
| status source (X-evolve, arXiv 2508.07932) | no n = 9 value (Table 2 covers n = 3..8) | read OK | n/a |

Action for the claim package (not a novelty failure): CLAIM.md says 1104 is "strictly larger than 1082, the largest cap in F_3^9 that the sources below report". That is true of its listed sources, but the strongest prior value now public is Noirsys's 1084 (2026-10-23). The claim text and credit should cite it, and the margin is +20 over the best known, not +22.

Side note, not checked: the slice sizes 80/512/512 in REPRODUCE.md fit the doubling pattern 2 x (512 + 40). If the object really is a doubling, it would also imply a 552-cap in PG(8,3), above Edel's 541. I did not verify that.

Sanity check: `shasum` of cap_1104_n9.txt gave 26a206db2dafae4a7f2c6f7478738acf5550af13998da2d4d0dff610ba83f82e (matches CLAIM.md). An inline Python pair scan, using no files from the package's checker, found 1104 distinct 9-digit ternary vectors and 0 pairs whose third point -(x+y) mod 3 lies in the set (2026-10-24T20:04:15Z).

## Sources checked (one plain GET each, User-Agent "V3R1T4S-research-run (honest client)", times from `date -u`)

Saved copies are in novelty-fetch/ (relative to the claim folder).

1. Status source: https://arxiv.org/html/2508.07932 (X-evolve, Zhai et al.)
   2026-10-24T20:04:23Z, HTTP 200, 760823 bytes, sha256 526607c13d086051e05b70ac698ed24409917f75bf05e7b5a217f77e7165721c (same as the scout's two fetches). File: novelty-fetch/xevolve-2508.07932.html.
   Quote (Table 2): "n 3 4 5 6 7 8 / Best known 9 20 45 112 236 496 / FunSearch 9 20 45 112 236 512 / X-evolve 9 20 45 112 236 512". The text says "It also matches state-of-the-art results in constructing maximal cap sets for dimensions 3 through 8". No n = 9 value. The page was readable, so the PENDING STATUS CHECK rule does not apply.

2. Edel's pages on the Heidelberg host (the honest try the brief asked for):
   - https://www.mathi.uni-heidelberg.de/~yves/index.html: 2026-10-24T20:05:00Z, HTTP 404 (Apache "Not Found").
   - https://www.mathi.uni-heidelberg.de/~yves/Matritzen/CAPs/CAPMatIndex.html: 2026-10-24T20:05:09Z, HTTP 404.
   I did not try the bare host mathi.uni-heidelberg.de (the scout reported a TLS name mismatch there) and used no TLS-skip.

3. Edel's cap table at his own current domain, taken from the link on OEIS A090245 ("Yves Edel, Caps, 2010"). The page calls itself "the website formerly known as www.mathi.uni-heidelberg.de/~yves/". The Heidelberg host answered 404 (moved). It did not block me, so this is the author's canonical page, not a mirror used to dodge a block. The panel may weigh this. Without it, the 1082 bar still stands on the FunSearch notebook (item 5).
   - http://www.yvesedel.de/Matritzen/CAPs/CAPMatIndex.html: 2026-10-24T20:07:59Z, HTTP 200, 15275 bytes, sha256 8aa5a2837a51d261c7b030e500c2c99e396d9ce7a653ecce8bc9badf6c1e2817. File: novelty-fetch/edel-yvesedel-CAPMatIndex.html.
     Quote: "Lower bounds on m 2 (k,q) ... 8 534 --> 541 ..." (row k = 8, column q = 3, meaning PG(8,3) at 541), "A 541 Cap in PG(8,3)", "Last changed: April 28, 2010." The page gives no separate affine AG(9,3) entry.
   - http://www.yvesedel.de/Matritzen/CAPs/Is/Iindex.html: 2026-10-24T20:08:24Z, HTTP 200. Admissible sets and capsets for "Extensions of generalized product caps". No n = 9 cap listed.
   - http://www.yvesedel.de/Papers/CapSurvey.html: 2026-10-24T20:08:24Z, HTTP 200. Bierbrauer & Edel, "Large caps in projective Galois spaces" (2012): "a construction of an 541-cap in PG(8,3)".
   - http://www.yvesedel.de/Papers/CapSurvey.pdf: 2026-10-24T20:08:31Z, HTTP 200, 244851 bytes, sha256 66ebda0dda4c6e3f7c37bceece4baab8df233be6db82ac6283f628ad493380da. Files: novelty-fetch/edel-CapSurvey.pdf and .txt.
     Quote: "Theorem 1. An n-cap in PG(d, q) allows the construction of a 2n-cap in AG(d + 1, q)." Table 1 (Lower bounds), row d = 8, q = 3: "541 c". So AG(9,3) is at least 2 x 541 = 1082.

4. OEIS A090245: https://oeis.org/A090245
   2026-10-24T20:07:27Z, HTTP 200, sha256 0cf521b9c40ae1e3459da3fc977f4c5d3353acc1c392bc7d9b25e14dc351f8b2. Terms "1, 2, 4, 9, 20, 45, 112" (exact maxima through n = 6 only). Gives no n = 9 value.

5. FunSearch notebook: https://raw.githubusercontent.com/google-deepmind/funsearch/main/cap_set/cap_set.ipynb
   2026-10-24T20:18:29Z, HTTP 200, 17080 bytes, sha256 f97f6f6ec331e5809ca4d40205224d2c5c613687d4f65316ecc2dd04a1724203 (identical to sources/funsearch-cap_set.ipynb). File: novelty-fetch/funsearch-cap_set.ipynb.
   Quotes: "recall that largest known cap set for `n = 9` has size `1082`"; "Discovered function that builds a $1082$-cap in $n = 9$ dimensions ... This matches the previously known best construction"; code `assert cap_set_n9.shape == (1082, 9)`.

6. Wikipedia "Cap set": https://en.wikipedia.org/wiki/Cap_set
   2026-10-24T20:07:27Z, HTTP 200, sha256 1b9e2940444caae31fa3779ba4c385653682821210aaabc1da249babe20a5166. No n = 9 value. Asymptotic bounds only: "improved to 2.2203^n with another large language model and to (2.2203+ε)^n by Hametner & Tyrrell (2026)".

7. Target repo, TROPHY_CASE.md: https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md
   2026-10-24T20:06:43Z, HTTP 200, 31235 bytes, sha256 b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1. It lists six result families (degree-diameter graphs, constant-weight codes, matrix multiplication, Lehmer bound, VNN-COMP counterexamples, RobustBench attack) plus two cipher-challenge commitments. No cap-set entry: grep for "cap", "F_3", "1082", "1104" and "FunSearch" found nothing.

8. Target repo, open pull requests: https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100, pages 1 to 4 (page 1 via /repos/..., pages 2 to 4 via the Link header's /repositories/1011751194/...).
   Page 1 at 2026-10-24T20:06:44Z, page 2 at 20:06:51Z, page 3 at 20:06:52Z, page 4 at 20:06:53Z. All HTTP 200. sha256 per page: ac55b186..., b90550cf..., 8801bdcb..., 848f09c4...
   337 open PRs. A strict scan of titles, bodies and branch names for "cap set", "capset", "cap-set" and "cap_set" found 0 hits. A loose scan matched only unrelated claims, where "1082" or "1104" appear as other quantities (for example #540 Hadamard, #523 Feigenbaum, #599 JARVIS). No pending cap-set claim.

9. qed.bot register: https://qed.bot/t/capset-dimension-8 (2026-10-24T20:07:26Z, HTTP 200, sha256 178174a977c966d8a68a75374e3e7dcb9c0a73fbd94b6a5d595165b0ad1bfede) and https://qed.bot/data/targets.json (2026-10-24T20:07:59Z, HTTP 200, 283665 bytes, sha256 1c56d8e6e715e9c5fa1490910e4dad9b334d75b3bcfe3bbe0592d10e2542884c).
   Only one cap-set target: "capset:dimension-8", record "512 points, FunSearch, 2023-12-14", earlier "496 points, Yves Edel, 2004". No dimension-9 target. The page footer has a "For agents" link, which I did not follow.

10. whataifound.org: https://whataifound.org/finding/2023-12-funsearch-capset
    2026-10-24T20:15:23Z, HTTP 200, sha256 75e4bbc01a9b910aafc0960dd34a5d949720dfb89245c1e2dac5668ebb5e42df. FunSearch 2023 entry only. No n = 9 value.

11. GitHub repository search: https://api.github.com/search/repositories?q=%22cap+set%22+OR+capset+pushed:%3E2024-10-01&sort=updated&per_page=100
    2026-10-24T20:16:37Z, HTTP 200, total_count 81, sha256 f1dc02e6165ef8f4d926ab0244f1c85c54f13dcca1189a8686bb383cb8245c72. File: novelty-fetch/gh-search-capset.json.
    Relevant hit: Noirsys/capset (created and pushed 2026-10-23), description "Lower bounds c(9,3) >= 1084 and c(11,3) >= 5529, with both witnesses and two independent checkers."

12. READMEs via https://api.github.com/repos/<repo>/readme, 2026-10-24T20:17:02Z to 20:17:05Z, HTTP 200 each:
    - Noirsys/capset (sha256 dd4a6b46...): "| $c(9,3)$ | **1084** | 1082 | two independent checkers |". Also: "The $n=9$ clearance is **absence of evidence**: no paper in this niche states a $d=9$ result". So 1084 is their prior-art bar and their claim. 1104 > 1084.
    - JonFermin/auto-erdos (sha256 d5ca3c97...): "| `capset_n9` | 9 | 1082 | 2592* | open | Big gap |" and "Cap-set problems remain open above their literature LBs." No improvement.
    - keremt-dev/discovery-harness (e00d83c8...): FunSearch-style harness. No n = 9 value.
    - IdeaSearch/IdeaSearch-capset (1c2a6cb7...): README is only a title.
    - Sapphire-Brand/CapsetSearch (a1f42bf8...): "Randomized searcher for large capsets". No values.
    - vibemathing/problem-um-comb-010-... and problem-um-game-007-... (both d16000bc...): harness boilerplate. It addresses AI agents ("Start with: 1. `AGENTS.md` ..."). injection_suspected (benign; not followed). No values.
    - https://raw.githubusercontent.com/Noirsys/capset/master/PUBLIC-WRITEUP.md: 2026-10-24T20:17:25Z, HTTP 200, sha256 4c3c6fe39a668755fb0d0183d87249f18e0120dcf0d51f6015eae281c93addc5. "1084 points in 9 dimensions — up from 1082". No larger n = 9 claim. No instructions aimed at the reader-agent.
    - https://api.github.com/repos/Noirsys/capset/git/trees/master?recursive=1: 2026-10-24T20:17:42Z, HTTP 200, not truncated, 49 entries. The n = 9 files are engine/edel/affine_n9_1082.json, engine/edel/affine_n9_1084.json and evidence/cap_n9_1084_12d746361afb9eec.txt. Nothing above 1084. I did not check their 1084 witness. Either way, 1104 > 1084.

13. arXiv API searches (export.arxiv.org):
    - all:"cap set" OR all:"cap sets" OR all:capset OR all:capsets OR all:"cap-set", newest first, max 200: 2026-10-24T20:10:52Z, HTTP 200, total 45, sha256 edfdcc98188746d5e9d062c348bf6f03b50281954a7d01fd2a4b0bd35cf919b8.
    - abs:"cap set" OR abs:"cap sets" OR abs:capsets OR ti:"cap set" OR ti:capsets, newest first, max 60: 2026-10-24T20:18:03Z, HTTP 200, total 44, sha256 0e985ea087d8325ddc42c7eeb6ce5a774f49a005f6ebe93624dd9f072ae62999. Same recent set as the first query.
    - (abs:caps OR ti:caps OR ti:cap) AND (abs:projective OR abs:affine OR abs:ternary OR abs:F_3), newest first, max 150: 2026-10-24T20:11:25Z, HTTP 200, total 821. Noise. No paper on caps in PG(8,3) or AG(9,3).
    - id_list=2609.13972,2608.23875,2603.15617,2408.02328,2409.07216: 2026-10-24T20:14:56Z, HTTP 200.
    Since 2024-10, the cap-set papers are 2610.19960, 2606.12194, 2605.13628, 2604.26989, 2602.05254, 2601.16917, 2508.07932, 2502.06005, plus off-topic hits. None gives an AG(9,3) value above 1082.

14. Full texts checked for n = 9, 1082, PG(8,3) and AG(9,3):
    - arXiv 2601.16917 (Karapetyan & Karapetyan, "New Method for Constructing Complete Cap Sets", Jan 2026): https://arxiv.org/pdf/2601.16917, 2026-10-24T20:11:35Z, HTTP 200, sha256 48ab07c9... Its list of known bounds: "c7,3 >= 236 ... c8,3 >= 512 ... In [15] we proved that c11,3 >= 5504, and in [16] c16,3 >= 274432, c21,3 >= 13991936". Upper bound "c9,3 <= 2070". No c9,3 lower-bound improvement. Their 2024 and 2025 Pattern Recognition and Image Analysis papers, cited there as [15] and [16], were not read directly; this intro summarizes their bounds.
    - arXiv 2602.05254v2 (Grace & Voloch, "Algebraic capsets"): https://arxiv.org/pdf/2602.05254v2, 20:11:35Z, HTTP 200, sha256 2c866634... Quote: "The exact value of a(n) is known for n <= 6 ... It is also known that a(8) >= 512". No n = 9 value.
    - arXiv 2606.12194v2 (Hametner & Tyrrell, June 2026): https://arxiv.org/pdf/2606.12194v2, 20:11:35Z, HTTP 200, sha256 8801b003... Asymptotic results only ("The current record is r3(F_3^n) >= (2.2203...)^n"). No n = 9 value.
    - arXiv 2511.02864v3 (Georgiev, Gómez-Serrano, Tao, Wagner, AlphaEvolve "Mathematical exploration and discovery at scale"): https://arxiv.org/html/2511.02864, 20:13:51Z, HTTP 200, sha256 8933f1ef... Cap sets mentioned once, as FunSearch background. No cap-set result.
    - arXiv 2503.11061v2 (Ellenberg et al., "Generative modelling for mathematical discovery"): https://arxiv.org/html/2503.11061, 20:13:51Z, HTTP 200, sha256 51edec06... Benchmarks cap sets at n = 8 only ("The best known score is 512"). No n = 9 value.
    - arXiv 2603.15617v2 (HorizonMath benchmark): https://arxiv.org/html/2603.15617, 20:15:10Z, HTTP 200, sha256 0d6e5cc4... Cap sets appear only as FunSearch background. None of its new results is a cap set.
    - arXiv 2608.23875v2 ("AI Finds A Way"): https://arxiv.org/html/2608.23875, 20:15:10Z, HTTP 200, sha256 8b0d81e7... FunSearch anecdote only. No n = 9 value.
    - From abstracts only (item 13): 2604.26989 (multiplicative subgroups as caps, fields of order 81/243/729, no record sizes), 2609.13972 (integer solution-free sets, not caps), 2408.02328 (survey).

## Web searches run (WebSearch tool, 2026-10-24, about 20:04Z to 20:16Z)

- cap set F_3^9 dimension 9 largest known cap 1082 new record (extended)
- "cap set" "dimension 9" larger than 1082
- AG(9,3) cap size lower bound Edel table affine caps
- FunSearch 512 cap set dimension 8 extended product construction new caps dimension 9 10 (extended)
- "PG(8,3)" cap 552 OR "552-cap"
- FunSearch 512-cap AG(8,3) projective extension points at infinity PG(8,3) larger cap doubling AG(9,3) (extended)
- AlphaEvolve cap set dimension 9 new lower bound
- "cap set" 1104 F_3^9
- Karapetyan "Complete caps in affine geometry AG(n,3)" Pattern Recognition and Image Analysis 2024
- Karapetyan "On Some Large Cap Sets" 2025 Pattern Recognition and Image Analysis AG(n,3)
- Qiao honors thesis Brown 2026 cap set (result: an expository thesis on upper bounds; not opened)
- TU Delft thesis "Constructions for the cap set problem" dimension 9 lower bound (result: Pelupessy 2024 BSc thesis on asymptotics; snippets show no n = 9 value; not opened)
- LLM evolutionary search cap set n=9 1082 OpenEvolve OR ShinkaEvolve OR CodeEvolve OR ThetaEvolve OR AlphaResearch (extended)
- "Mathematical exploration and discovery at scale" AlphaEvolve Tao cap set
- Ellenberg "Generative modelling for mathematical discovery" funsearch cap set dimension 9
- github cap set n=9 F3^9 larger than 1082 cap new record 2025 2026 (extended)
- new large cap PG(8,3) 2024 OR 2025 OR 2026 improves 541
- "cap set" "nine dimensions" OR "9 dimensions" largest known size 2025

No search result reported an AG(9,3) cap above 1082 except Noirsys's 1084 (found through the GitHub API, item 11). None reported a PG(8,3) cap above 541. Older secondary tables give lower n = 9 figures: arXiv 1809.05117 lists 1064 (= 2 x 532-cap, pre-541), and a projective-caps thesis lists 1008/1064. These are below 1082 and do not matter.

## What I could not read, and why

- Edel's pages on www.mathi.uni-heidelberg.de: HTTP 404 (pages moved). Read instead at his own domain yvesedel.de, the link OEIS gives (item 3).
- MinT database, http://mint.sbg.ac.at/ (Edel's page names it for current bounds, as linear codes with d = 4 / OA strength 3): 2026-10-24T20:15:48Z, HTTP 000, connection timed out after 30 s. Not retried. So I could not check whether MinT lists a ternary [n, n-9, 4] code with n of 552 or more (a PG(8,3) cap of 552 or more).
- Karapetyan & Karapetyan's 2024 and 2025 Pattern Recognition and Image Analysis papers, and their CSIT 2023 paper: not opened (journal pages; likely paywalled). Their Jan 2026 arXiv paper (item 14) lists their own bounds and gives none for n = 9. Noirsys also says this group "publishes corollaries for four dimensions and skips" d = 9.
- The Brown (Qiao 2026) and TU Delft (Pelupessy 2024) theses were not opened. Search snippets show they cover upper bounds and asymptotics.
- Local tool hiccup, for the record: at 2026-10-24T20:07:18Z a shell loop failed locally (zsh word splitting; curl rejected the URL before any request was sent). No network request went out. The three affected pages (qed.bot, Wikipedia, OEIS) were then fetched once each at 20:07:26Z and 20:07:27Z.
- No source answered 401, 403, 429 or 503, or showed a challenge page. No TLS failure.

## Limits of this verdict

The novelty bar rests on positive citations: 1082 (Edel 541 x 2; FunSearch's own "largest known" statement) and 1084 (Noirsys repo). Beyond those, "nothing at 1104 or above exists" is absence of evidence from the searches listed above. MinT, the main table that could hide a larger PG(8,3) cap, was unreachable. Within those limits, 1104 is strictly above every known value, and it is not a tie.

pass: true
