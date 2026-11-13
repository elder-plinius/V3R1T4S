# NOVELTY review: A389690(23) = 3570 (target subtraction-game-max-period-terms), round 2

context: subagent (fresh context, Claude Science delegation)

Path key (added by the claimant on 2026-10-28 at the maintainer's request, PR #781 review): this review was run on the panel zip, whose layout differs from this package. Its code/A/ and code/B/ are how-we-built-it/A/ and how-we-built-it/B/ here (byte-identical). These panel inputs are not shipped: CLAIM.md and REPRODUCE.md (the claim summary and its commands; see README.md, RUN_IT_YOURSELF.md and how-we-built-it/BUILD.md), histogram_sg_23_A.txt, histogram_sg_23_B.txt and maximising_set.txt (objects/; object/A389690_23.txt holds the same maximising set and, as lines 10-682, the same 673 histogram lines, sha256 760aabce6a540d00660f1e4ab4a243b83a5d6e3640773d6497d67ea630bc00ac), the check helpers verify_oeis.py and sg_ref.py (code/check/), and a389690_2.txt (inputs/), the OEIS program https://oeis.org/A389690/a389690_2.txt (sha256 9fe51a4caa7f2d3f381c44fcb39b43c270c7bab12204e9cbf7e6e2c59999b61f). File references in the text were changed only to name these package paths, URLs or bare file names; no finding, number or verdict changed. Verbatim logs keep the zip's paths.

role: NOVELTY skeptic. I worked only from the claim package (the panel zip) and the network.
package: claim zip sha256 `d8fbe05071f18e492f951b4ea4d5cd172cc76c0e1c8ed66c4bcb5209a30d0161`; its `CLAIM.md` sha256 `26629684c4d87f59f194e3519917cfa80de80f2cd202d2c22e81c48307a127e3`; its `maximising_set.txt` sha256 `5eb9b6efe05eabd3a01db9d9c9e8e89f13160b32996699446c3141cbf6e5900c` (matches the hash listed in `CLAIM.md`).

novelty: NEW. No source gives A389690(23). The OEIS entry, its b-file and its history list n = 1..22 only, and no prior work found here determines the term for max S = 23.

## 1. Primary status pages (kit/RUN.md step 6)

Each page got exactly one plain request with `curl -sS -L`, curl 8.22.0 and its default User-Agent. There were no retries, mirrors or caches, and no redirects occurred.

| UTC | URL | HTTP | bytes | sha256 | read |
|---|---|---|---|---|---|
| 2026-10-26T08:52:36Z | https://oeis.org/A389690 | 200 | 16800 | `8b8475cedae0960445a55fd373872e9d91694ffbca238fcf3aca3f42f17964f8` | DATA `2, 4, 6, 8, 10, 12, 22, 25, 28, 58, 54, 87, 114, 144, 189, 336, 306, 456, 728, 1178, 1180, 4464` (n = 1..22), link 'Table of n, a(n) for n=1..22', keyword `nonn,more`, STATUS approved, AUTHOR Rui Yao, Oct 10 2025; no a(23), no '3570' |
| 2026-10-26T08:52:38Z | https://oeis.org/A389690/b389690.txt | 200 | 183 | `a0fc3d77b3ef73421b37232cc8d9071031a7eddaf9f5d6f3ce5b0c6fa418a2b8` | 'b-file synthesized from sequence entry', 22 lines, last line `22 4464`; no n = 23; no '3570' |
| 2026-10-26T08:52:39Z | https://oeis.org/history?seq=A389690 | 200 | 20156 | `a913d547e257e4be7734a5cc6fe8cd0e8aad5ce73cbdf9d323b5599e24d0b043` | revisions #36..#27; latest #36 (Sean A. Irvine, Oct 26 2025) proposed -> approved |
| 2026-10-26T08:52:40Z | https://oeis.org/history?seq=A389690&start=10 | 200 | 24022 | `efce250817ac5b41c09187ee351718f661cc47dc95676589ce4877650c8402ef` | revisions #26..#17 (NAME wording, links) |
| 2026-10-26T08:52:42Z | https://oeis.org/history?seq=A389690&start=20 | 200 | 31973 | `dba645925f40e71d65d1427e6db210b024c45e904107b243d90205b12b45011b` | revisions #16..#7 (NAME wording, PROG moved to a link) |
| 2026-10-26T08:52:43Z | https://oeis.org/history?seq=A389690&start=30 | 200 | 32021 | `c07143e2d2691cf55fd65f068dc5f08e7a6967c4c03bac35f83e73a46de4d4ab` | revisions #6..#1; DATA set once in #2 (Rui Yao, Oct 10 2025) to n = 1..22 and never changed afterwards |
| 2026-10-26T09:06:01Z | https://oeis.org/A389690/a389690.txt | 200 | 2517 | `e75eb9f55ff688588facba97830fc36f8456878d55a936f610233f669f246c14` | program file linked in earlier revisions (#8 to #29): code only, no data |
| 2026-10-26T09:06:06Z | https://oeis.org/A389690/a389690_1.txt | 200 | 2795 | `9fe51a4caa7f2d3f381c44fcb39b43c270c7bab12204e9cbf7e6e2c59999b61f` | program file linked in #31..#32: byte-identical to the claim's copy `a389690_2.txt` (same sha256), code only |

All 36 revisions (#36 down to #1) were read. None mentions a(23) or 3570, and none is pending after #36. The entry-page and history-page hashes differ from those recorded in `CLAIM.md`, because the pages carry a live footer ('Last modified October 26 04:45 EDT 2026. Contains 400709 sequences.'). The terms and the revision list are identical to what `CLAIM.md` records. The b-file hash is identical (`a0fc3d77...a2b8`). The term is therefore absent from the entry, the b-file and the history at verification time (2026-10-26T08:52:36Z to 08:52:43Z), which is criterion (3).

## 2. Prior art named in the task: A. Flammenkamp, *Lange Perioden in Subtraktions-Spielen* (Bielefeld, 1997)

| UTC | URL | HTTP | bytes | sha256 | read |
|---|---|---|---|---|---|
| 2026-10-26T08:53:36Z | https://wwwhomes.uni-bielefeld.de/~achim/diss.ps.gz | 200 | 1314054 | `68b513ae3bdb9ba1ddee941d7a8b97a04663a2950865bb7d721f8ccb946f2c86` | gzip of `diss.ps` (gzip header date 29 Jan 1997); converted with Ghostscript 10.08.0 `txtwrite` to 156 pages of text |

Findings (page numbers are the printed book pages; PDF page = book page + 5):

1. The only exhaustive table over all move sets is on pp. 40-41: 'Periodenlängen aller Zugmengen mit maxL < 30', a running list of 44 record holders with `p` (period) and `q` (preperiod). This is the win/lose (P-N) table, not a Sprague-Grundy table. I checked this with my own exhaustive recomputation for maxL <= 14 (stdlib Python, both sequences). The P-N maxima at maxL = 10..14 are 45, 54, 61, 76, 94, exactly the table's last entries for those maxL. The SG maxima are 58, 54, 87, 114, 144, equal to A389690(10..14) and different from the table at maxL = 10, 12, 13, 14. The table has no row with maxL = 23: it goes from `{2,7,10,12,15,20,22} p=516` to the maxL = 24 rows. A389689(22) = 516 and A389689(23) = 446 are consistent with that.
2. I read every occurrence of 'Nim', 'Grundy' and 'SGW' in the extracted text in context (PDF pp. 4, 5, 20-27, 66-71, 82, 84, 87, 93, 101, 155). I also read in full the record pages (PDF pp. 39-46), the Nim section (PDF pp. 66-71) and 'Offene Fragen' (PDF pp. 95-100), plus the passage on PDF p. 50 around `{4,10,13,19,23}`. I did not read the whole thesis line by line. The Sprague-Grundy material is limited to Definition 7, the structure proof of Satz 8 for the family (2n, 5n, 6n+1, 8n+1), and the section 'Gewinn/Verlust-Folge versus Nim-Folge' (pp. 61-66). That section gives examples whose Nim period is twice the P-N period ((4,6,11,14), (5,7,14,17), (2,3,6,9,10,12), (2,5,10,13,15)), the families (n,n+3,3n-1,3n+3), {2,4n-1,4n+1,4n+5,8n-2}, {2,4n+1,4n+3,4n+7,8n+2} and (n,2n+1,4n+2,5n+3,6n+3), and Satz 22 (the ratio of the two periods is unbounded). None of these is a maximum over all sets, and none has max element 23.
3. The values 3570, 4464, 1180, 1178, 728, 336 and 2232 do not occur anywhere in the extracted text. 306 and 456 occur only as polynomial coefficients in 4-move family formulas.
4. The extracted text contains two explicit sets with max element 23 (I searched for brace, parenthesis and TeX-brace notation). The first is `{1,8,22,23}`, a 4-move preperiod record holder on p. 37 with `p=118 q=349` (P-N). The second is `{4,10,13,19,23}` on p. 45, the family (n, 2n+2, 3n+1, 4n+3, 5n+3) at n = 4, with `p=422`. My recomputation gives SG period 118 (P-N 118) and SG period 422 (P-N 422). Both are below 3570, so nothing contradicts the claim.

Conclusion: the dissertation does not give, or imply, the maximum Sprague-Grundy period for max S = 23. Its table cannot stand in for A389690, because the SG and P-N maxima already differ at maxL = 10 and at maxL = 22 (4464 against 516).

## 3. Literature of the last 24 months (2024-10-26 to 2026-10-26) and other sources

| UTC | URL | HTTP | bytes | sha256 | read |
|---|---|---|---|---|---|
| 2026-10-26T09:02:07Z | http://export.arxiv.org/api/query?search_query=all:%22subtraction%20game%22%20OR%20all:%22subtraction%20games%22&sortBy=submittedDate&sortOrder=descending&max_results=60 | 200 | 69132 | `e3466e1c8cff1d4f98cccb145820acb170be8dc8600603ada985170a2ccabc3c` | 42 results in total, 9 since 2024-10-26: 2610.25829 (two-element games with a pass), 2609.05358 (purely periodic three-move), 2609.00871 (Grundy DFA for grammar games), 2608.17654 (infinite sets), 2607.27989 (partizan), 2606.29015, 2603.10414 (additive), 2601.18715 (additive sink), 2510.24280 (cumulative). None computes a maximum period over all S with max S = n |
| 2026-10-26T09:01:31Z | https://arxiv.org/pdf/2405.20054 | 200 | 1639113 | `767613f57212bb940d707d05486ddcd93f2f07d7485658ff238f2667eb851865` | Larsson & Saha, 'A brief conversation about subtraction games' (also Games of No Chance 6, MSRI Publ. 71, 2025): a survey centred on the 1997 thesis. In the passages read (every 'record' context), it describes the max S <= 30 table as outcome record holders. A keyword search of the extracted text finds no '3570', '4464', '1180' or '1178' |
| 2026-10-26T09:02:04Z | https://arxiv.org/pdf/2312.02426 | 200 | 939161 | `d39e31b831bf1c9b847a494deceb3fa3e6be90546554a6f9f154222e6c8694fc` | Miklós & Post (IJGT 53(4), 2024, doi 10.1007/s00182-024-00911-5): outcome sequences with seeds (title and abstract). A keyword search of the extracted text finds no 'nim-sequence', 'record', '3570' or '4464'; the paper was not read in full |
| 2026-10-26T09:05:01Z | https://arxiv.org/pdf/2606.01175 | 200 | 688599 | `14fb838101680761d066fa3719463dfd9318c81f571acb4535bef46bf953401d` | Parfenov & Vyalyi, 'On the Complexity of Recurrence Evaluation' (2026): complexity results according to the abstract and the 'subtraction' contexts. A keyword search finds no '3570', 'Grundy' or 'A389690' |
| 2026-10-26T09:09:28Z | https://api.crossref.org/works?query.bibliographic=subtraction+game+period+nim-sequence&filter=from-pub-date:2024-10-01&rows=60&select=DOI,title,published,container-title | 200 | 13749 | `9ca468d86fdccfb4f3f9119688fd3d40e739514301819a5dfb418c755f9ae906` | Crossref (from 2024-10-01): game-theory hits are Miklós-Post and Nim variants (divisor Nim, MuM, Kotzig's Nim); nothing on maximum SG periods |
| 2026-10-26T09:03:44Z | https://oeis.org/search?q=1178%2C1180%2C4464&fmt=text | 200 | 1823 | `2658fab562dbf8458307412b0ea8a07e990858ed8eb71424b91aa1c9cae3c17c` | OEIS search `1178,1180,4464`: only A389690 |
| 2026-10-26T09:03:48Z | https://oeis.org/search?q=1180%2C4464%2C3570&fmt=text | 200 | 212 | `fb19dc876168964545d7a68e6c9c4e1131d4a21346bc8d1992e840a62051056c` | OEIS search `1180,4464,3570`: 'No results.' |
| 2026-10-26T09:03:49Z | https://oeis.org/search?q=%22subtraction+game%22+period&fmt=text | 200 | 34894 | `cfd31ad2793c5127484dd23b41263437099646a4c1e1bcf3ff08108cc4e38b69` | OEIS search '"subtraction game" period': 11 entries (A389689, A389690, A242080, A242079, A014587, A396951, A266756, ...); none has SG maxima beyond n = 22 |
| 2026-10-26T09:06:51Z | https://wwwhomes.uni-bielefeld.de/achim/ | 200 | 1365 | `0af13fb837d27c8b948722fe56bc9a4a101c1dde9b52f893b8744040f7aa69c2` | Flammenkamp's site index, pointing to `welcome.html` |
| 2026-10-26T09:07:15Z | https://wwwhomes.uni-bielefeld.de/achim/welcome.html | 200 | 302 | `aea33b620fbe1b3ac601aca9d3e6c080e686d57479f0e5bcf1d602fcb59da26a` | meta refresh to the CGI index below |
| 2026-10-26T09:07:33Z | http://wwwhomes.uni-bielefeld.de/cgi-bin/cgiwrap/achim/index.cgi | 200 | 1837 | `9bd526e9c47b0a536cc3aa8347e2e940441fddf6fa97423f5ebf35ce997b9395` | HTTP 200, but the body is a CGIWrap 'Script Execution Failed' page, so the live site cannot be browsed (not retried) |

Web searches (7 queries, run by the search tool itself): the longest or maximum SG period of subtraction games; 'A389690'; subtraction-game periodicity papers 2025; the OEIS author together with subtraction games; Flammenkamp record tables; '4464' or '3570' with subtraction sets; Althöfer-Bültermann 1995. The only page besides OEIS that names A389690 is V3R1T4S PR #699 (the bank PR). According to its abstract, Althöfer & Bültermann, TCS 148 (1995) 111-119, studies Win/Loss periods of specific families. The full text was not read.

## 4. This repository

| UTC | URL | HTTP | bytes | sha256 | read |
|---|---|---|---|---|---|
| 2026-10-26T08:58:32Z | https://api.github.com/repos/elder-plinius/V3R1T4S/commits/main | 200 | 528857 | `903136757d5d549d5aae480b63d738e3891fbc3eb00fe93c2621b88c5f3ee5e7` | main = `8846324a8fe813bf89a9ef2a60eb9b13d0ba79fd` (2026-10-25T19:26:25Z), the commit quoted in `CLAIM.md` |
| 2026-10-26T08:59:29Z | https://api.github.com/repos/elder-plinius/V3R1T4S/contents/TROPHY_CASE.md?ref=main | 200 | 43934 | `8361a4e1e7c0b5ecc89b6c947320a58de7afd36e253eb9ed40ee1e6e64f057f4` | TROPHY_CASE.md at main: blob `571f24117c6b128ffe751a39f22fcab68c498e66`, decoded 31235 bytes, sha256 `b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1`. No 'subtraction', 'A389690', 'A389689', 'Sprague', 'Grundy', '3570' or 'OEIS' |
| 2026-10-26T08:58:34Z | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100&page=1 | 200 | 2577149 | `fea859a5edea2e6d833e0a359620d45e6894184099bbf5a935ef626fc51da39d` | open PRs page 1: 100 |
| 2026-10-26T08:58:59Z | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100&page=2 | 200 | 2492855 | `a03de93c09d8b9494a2c8f92b723d5c4959eda2f3f97bfa7e971cb51da985b55` | open PRs page 2: 100 |
| 2026-10-26T09:00:06Z | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100&page=3 | 200 | 2364283 | `674409194d5f33fd8eeb676962c68f9ebdf4489866d3f1d7733a1ef80ac9c794` | open PRs page 3: 100 |
| 2026-10-26T09:00:09Z | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100&page=4 | 200 | 673049 | `6bdb4097d25fe4a5c5a36a64571713157ad5e5b0f805eb31e297af130fcda5b4` | open PRs page 4: 29 |
| 2026-10-26T08:59:34Z | https://api.github.com/search/issues?q=repo:elder-plinius/V3R1T4S+A389690&per_page=100 | 200 | 4320 | `91ba3ff2641d84b051a76d00903c184829394d51067bc02d31bfd3b7371e0ae5` | issues+PRs, all states, 'A389690': 1 hit, the closed bank PR #699 |
| 2026-10-26T08:59:35Z | https://api.github.com/search/issues?q=repo:elder-plinius/V3R1T4S+subtraction&per_page=100 | 200 | 210493 | `eba4c2867720474de644ad9db3d991040be9a786d45b19d0c05690dd08d9508e` | 'subtraction': 29 hits; only #699 concerns this target (the rest mention arithmetic 'subtractions') |
| 2026-10-26T08:59:38Z | https://api.github.com/search/issues?q=repo:elder-plinius/V3R1T4S+3570&per_page=100 | 200 | 101 | `840185ac69ff01c964c2bfead7f7b8a5a7764c3814155124f82ebe285189a90f` | '3570': 0 hits |
| 2026-10-26T09:08:40Z | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/8846324a8fe813bf89a9ef2a60eb9b13d0ba79fd/bank/targets.json | 200 | 2146913 | `7c10835a078dd0ed24154e89da3a0138a11fe4c52c89627f28989429b88fe38d` | bank entry `subtraction-game-max-period-terms`: A389690 'n = 1..22 known', disclosure 'open', status_checked 2026-10-25. The success criterion is identical (after whitespace normalisation, 777 characters) to the quote in `CLAIM.md` |
| 2026-10-26T09:03:51Z | https://api.github.com/search/issues?q=A389690&per_page=100 | 200 | 13927 | `d337578447620cc38faeb38bc6a02c9a92f56984287102c393f850856628d6e6` | GitHub-wide issues/PRs 'A389690': #699 plus one unrelated hit |
| 2026-10-26T09:03:53Z | https://api.github.com/search/repositories?q=subtraction+game+period&per_page=50 | 200 | 28053 | `848f15d023b058246e1284bd53c23abddc125b9204a7c4774d9976ac86b25cc0` | GitHub repositories 'subtraction game period': 1 unrelated result |

Open PRs: 329 in total (numbers 9..778). I scanned their titles, bodies and branch names for `subtraction|A38968x|A38969x|Sprague|Grundy|3570|max period|mex`. There were two hits, both unrelated: #465 (matrix-multiplication circuits, 'additions/subtractions') and #200 (card guessing, '3570' inside a fraction). No open PR, and no PR or issue of any state found by search, reports A389690(23).

## 5. Sanity check of the claimed object (not a reproduction of the exhaustive search)

I wrote my own stdlib implementation of the entry's definition: the first repeat of the length-23 window, counted from n >= 22. For S = {2, 3, 5, 7, 9, 10, 13, 14, 16, 18, 20, 21, 22, 23} (mask 3846998, as in `maximising_set.txt`) it gives SG period 3570, preperiod start 1012 and largest SG value 13. The outcome (P-N) period is 119, and 3570 = 30 x 119. This agrees with the expected output in `REPRODUCE.md`. The exhaustive maximum and the histogram (criteria 1-2) are for the other skeptics.

Note: 3570 < a(22) = 4464 does not bear on novelty. The entry is not monotone (a(11) = 54 < a(10) = 58, a(17) = 306 < a(16) = 336), and the target asks for the exact next term, not a larger value. Nothing has been published for n = 23 that this value could tie or must beat.

## 6. Limitations

- Not obtainable online, so not read: J. Bültermann, *Periodenlängen in Nim-Spielen* (Diplomarbeit, Bielefeld 1993), cited by the thesis. The 1997 thesis, whose preface calls its topic a continuation of a diploma thesis supervised by Althöfer, reports no SG-maximum table. The 1995 Althöfer & Bültermann paper concerns Win/Loss periods according to its abstract.
- Read only from secondary descriptions: the full text of Althöfer & Bültermann (1995), Austin's M.Sc. thesis (1976; all sets with max S <= 8) and Winning Ways (max S <= 7). The last two cover only small max S.
- Flammenkamp's live web pages: the CGI index returns an error page (see section 3).
- Search coverage: web search, the arXiv API (exact phrase), Crossref, OEIS search and GitHub search. No MathSciNet or zbMATH; OpenAlex was not used.
- Independence: before the work began, the delegation harness displayed recalled notes about the sibling claim A389689(24). They were not used as evidence. Every statement above comes from the sources fetched in this review or from my own computation.

## Verdict

No source gives A389690(23). At 2026-10-26T08:52Z the term was absent from the OEIS entry, its b-file and all 36 history revisions. The 1997 Flammenkamp thesis tabulates win/lose (P-N) periods, not Sprague-Grundy periods, and has no row for max S = 23. No publication of the last 24 months and no TROPHY_CASE.md entry reports the term. No open pull request reports it either, and neither does any pull request or issue of any state found by search. The claim would be the first determination of A389690(23). This passes NOVELTY only: correctness of the maximum and of the histogram is outside this review.

pass: true
