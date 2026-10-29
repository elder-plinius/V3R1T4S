# Skeptic panel: novelty

target: schutte-multiple-tournament-dice-bounds (V3R1T4S bank), partial win p1
claim: f(2,5) = 14, i.e. no S_5 set of two tournaments on 13 vertices (README.md)
role: novelty (bank kit RUN.md step 6)
context: subagent (fresh context, Claude Science delegation)
reviewed: 2026-10-28, 21:00-21:16 UTC
inputs: the claim folder (README.md, REPRODUCE.md, INDEX.csv, the-record-we-beat/RECORD.md, object/cnf_spec.json, object/upper_bound_m2k5n14.json, how-we-built-it/SOUNDNESS.md) and the public sources listed below
path key: `TROPHY_CASE.md`, `bank/targets.json` and `known-unknowns/graphs-games-automata/schutte-multiple-tournament-dice-bounds.md` are files of github.com/elder-plinius/V3R1T4S at commit c027ca3e0c8d1fc475d8e39cccd4b146fd50ffb8; `problems/schutte-multiple-tournament-dice-bounds.md` is in github.com/r-nikhil/INVENTA (branch main); `reproducible_source_code/BigWIN2/BW2-B87-P01/source/manuscript/main.tex` is in github.com/ArtificialZeng/AI-Has-Taste (branch main). Every other path is inside the claim folder.

## Instruction (RUN.md step 6, verbatim as given to this panel)

> Fetch the primary table or status page once, honestly (no retries; a block means fail), and quote URL, value and time. Search the last 24 months of literature, this repo's TROPHY_CASE.md and open pull requests. Pass only if the result strictly beats everything known. A tie is not a record.

For this p1 claim the question is whether f(2,5) = 14, or any proof of f(2,5) >= 14 (no S_5 2-set of order 13), is already published or already claimed in the repository.

## 1. Status source (one request each)

- URL: https://arxiv.org/abs/2604.08790
- time: 2026-10-28T21:00:12Z; HTTP 200; 39949 bytes; sha256 0b2c17af0cb7342b68eecf9951a3f011cbf28e31fdb41b3c086f9b58cfd9e3c0
- page: J. Jeffries, "Schuttes property for sets of tournaments and an application to dice games" (math.CO); the submission history lists only [v1] Thu, 9 Apr 2026 21:58:15 UTC; no journal reference.
- table: https://arxiv.org/pdf/2604.08790, 2026-10-28T21:00:32Z, HTTP 200, no redirect, 393509 bytes, sha256 6aca2fdf8285dabf47dbc7b83fd6232e31fe0e11bb02cb163f9dba05be97a8e8, 12 pages.
- value: Figure 7 ("Known upper bounds of f(m,k) for small values of m and k. Starred values show confirmed equality."), row k = 5 reads `331 14 9* 8* 7*` for m = 1..5. The cell (m,k) = (2,5) is **14 without a star**: an upper bound, not an exact value. Row k = 4, m = 2 reads `10*`.
- The paper says the starred values were "confirmed to be exact values for f(m,k) using a SAT formulation" described in its reference [8]. Section 4 says: "This work also provides no non-trivial lower bound for f(m,k)."
- Both sha256 values equal those recorded in the-record-we-beat/RECORD.md (claimant fetches at 11:54:10Z and 11:54:11Z), so the status page and the PDF had not changed by the time of this review. The claim's record (the-record-we-beat/RECORD.md; INDEX.csv: "<= 14 (Figure 7, unstarred)") is accurate.

## 2. What is known about f(2,5)

- Upper bound 14: Proposition 2.3 applied to two order-7 Paley tournaments (Figure 7). The claim reuses this published construction (object/upper_bound_m2k5n14.json; README.md cites Figure 7 and Proposition 2.3) and does not present it as new.
- Lower bound: no non-trivial lower bound is published. The best bound I can derive from published values: deleting one vertex w from an S_k m-set of order n >= k+1 leaves an S_(k-1) m-set of order n-1 (for a (k-1)-set U avoiding w, the dominator of U + w lies outside U + w). Hence f(2,5) >= f(2,4) + 1 = 11, using the starred f(2,4) = 10. Nothing I found reaches 14. This one-line argument is mine, not a published result.

## 3. Literature, last 24 months (2024-10-28 to 2026-10-28)

| source | what it says about f(2,5) |
|---|---|
| Jeffries, arXiv:2604.08790 v1 (April 2026), the status source | 14 without a star; no lower bound (section 1) |
| Jeffries, PhD dissertation, Iowa State University, "Generalizations of Schütte's property with applications to dice games", DOI 10.31274/td-20250502-307 (approved 2024, citation date 2024-08, deposited 2025-05-02). This is reference [8] of the paper and the source of its SAT confirmations | Figure 4.5 (printed page 42) is the same table, with (2,5) = 14 unstarred. Section 4.3 gives the base SAT formulation without symmetry breaking. The text never mentions f(2,5), the pair (2,5), order 13 or 13 vertices, or UNSAT/unsatisfiable, and gives no lower bound for f(m,k). The approval date falls just before the window; I checked it anyway. |
| X. Zeng, "The (k-1)-Tournament Schütte Boundary: f(k-1,k)=k+3", GitHub ArtificialZeng/AI-Has-Taste, entry BW2-B87-P01 (repository last pushed 2026-09-16; not peer reviewed) | proves f(k-1,k) = k+3 for k >= 3 (for k = 5 that is f(4,5) = 8, already starred). It notes that "general nontrivial lower bounds for f(m,k) are absent" and says nothing about m = 2, k = 5 |
| arXiv API, 9 queries sorted by submission date (all:Schutte AND all:tournament; abs:"sets of tournaments"; all:tournament AND all:dice; abs:paradoxical AND abs:tournaments; all:Schütte; abs:k-paradoxical; all:Erdos AND all:Schutte; all:Schütte AND all:tournament; abs:tournaments AND abs:Erdos AND abs:dominated) | no other paper in the window on Jeffries' f(m,k) or on Schütte's property for sets of tournaments; arXiv:2604.08790 has no later version |
| Semantic Scholar, citations of arXiv:2604.08790 | 0 citing records |
| Crossref (bibliographic query, exact-title query, the dissertation's DOI record) | no journal version of arXiv:2604.08790; only the dissertation |
| OEIS (Schutte tournament; 2,4,6,10 tournament; 3,5,7,9 tournaments dominated; paradoxical tournament) | only A362137 (single Paley tournaments); no sequence for f(2,k) or f(3,k) |
| GitHub-wide search of issues and PRs for "2604.08790"; repository search (2604.08790 in readme or description; schutte tournaments) | only V3R1T4S #694 (section 4). The Erdős #902 projects concern the single-tournament f(k) only (jaredwilder/erdos902 judged by its README and file tree, jaredwilder/erdos902-tournament-f4 by its description); AI-Has-Taste is covered above |
| web search (several phrasings: f(2,5), Jeffries, sets of tournaments, Schütte, SAT) | nothing beyond the items above |

## 4. Repository (github.com/elder-plinius/V3R1T4S)

- main HEAD c027ca3e0c8d1fc475d8e39cccd4b146fd50ffb8 (2026-10-27T16:42:35Z) is 10 commits ahead of the claim's commit 8846324a8fe813bf89a9ef2a60eb9b13d0ba79fd and 0 behind. Neither the bank entry nor bank/targets.json is among the 121 files changed between them. The target record has status_checked 2026-10-25 and disclosure open, and the entry says "No optimality is claimed for 14 or 13".
- TROPHY_CASE.md at HEAD (31306 bytes, sha256 83af764f5a6551a5a27bbb135324931659bda04e60b66a2c0e711b991b356113) matches none of: schutte, Schütte, tournament, dice, Jeffries, 2604.08790, f(2,5), f(3,6).
- Repository tree at HEAD (5684 entries, not truncated): the only path containing "schutte" is the bank entry. No claim folder for this target exists.
- Open pull requests: all 352 (4 API pages fetched 21:03:27-21:03:32Z; created between 2026-10-14 and 2026-10-28T19:32:50Z). None mentions the target id, Schütte/Schutte, Jeffries, 2604.08790, f(2,5), f(3,6) or tournament in its title, body or head branch. The two regex hits on "dice" (#462, #333) are inside the word "indices".
- Closed PRs and issues (search API, all states): "schutte", "Schütte", "2604.08790" and "tournaments dice" return only #694, and "Jeffries" returns nothing. #694 (r-nikhil, 2026-10-24) proposed the target and was closed unmerged at 2026-10-25T19:31:10Z, when the maintainer added the target with p1 and wrote "Claims against the target are welcome now." The proposer's explainer (problems/schutte-multiple-tournament-dice-bounds.md in INVENTA) says "No smaller construction is claimed."

## 5. Verbatim check

The success criterion and the p1 statement quoted in README.md equal the `success_criterion` and `partial_wins[p1].statement` fields of bank/targets.json at HEAD (whitespace-normalised comparison: both equal).

## 6. Verdict on novelty

The published record gives f(2,5) <= 14 without a star and no non-trivial lower bound; this covers arXiv:2604.08790 v1 and the dissertation behind its SAT stars. Elementary consequences of the published values reach only f(2,5) >= 11. No source in the window, and no item in the repository (merged, open or closed), proves f(2,5) >= 14 or states f(2,5) = 14. The claimed exact value therefore goes strictly beyond what is known: a new lower bound of 14 that meets the published upper bound, not a tie with an exact value someone already established. The 14-vertex upper-bound object is the published composition, correctly attributed, and is not counted as new.

Scope: this panel judges novelty only. I did not check the encoder, the symmetry-breaking argument (how-we-built-it/SOUNDNESS.md) or the LRAT proof, and I ran no solver or checker. A pass here does not certify correctness; that rests with the other panel roles.

## 7. Limits and deviations

- OpenAlex was not used (no API key is configured in this environment). For citations I used Semantic Scholar, which can lag for recent preprints.
- zbMATH Open was not queried: api.zbmath.org is not on this sandbox's allowlist, and I did not ask for it because Crossref covers journal DOIs. Google Scholar, MathSciNet and ResearchGate were not queried either.
- dr.lib.iastate.edu: this sandbox's own proxy refused the first attempt (21:06:49Z) before it reached the server. After the domain was allowlisted I made one request to the landing page and one to the PDF; curl followed one 301 and one 302 redirect. No other page was requested twice.
- I searched the dissertation through text extraction (pypdf) of all 124 pages and read pages 48-51 in full. A statement made only inside a figure would have been missed.
- Pull-request coverage: titles, bodies and branch names of the 352 open PRs, plus the search API for closed ones. I did not list the changed files of each PR.
- I read Figure 7 from the PDF's extracted text. The k = 5 row has all five entries, so there is no column ambiguity, and it matches Figure 4.5 of the dissertation.

## 8. Context disclosure

Besides the claim folder and public sources, my context held two other things. One was the delegation message: role, the quoted RUN.md step 6, the status-source URL, and machine and network limits. The other was a set of memory notes recalled automatically from the requesting user's workspace: working rules, machine limits, the contributor's upstream account, and a note about an earlier panel on a different target. None of these concerned this claim or the literature on f(m,k), and none was used as evidence.

## Request log (UTC, 2026-10-28; plain curl, one request per page)

| time | URL | HTTP | bytes | sha256 (full or first 16 hex) |
|---|---|---|---|---|
| 21:00:12 | https://arxiv.org/abs/2604.08790 | 200 | 39949 | 0b2c17af0cb7342b68eecf9951a3f011cbf28e31fdb41b3c086f9b58cfd9e3c0 |
| 21:00:32 | https://arxiv.org/pdf/2604.08790 | 200 | 393509 | 6aca2fdf8285dabf47dbc7b83fd6232e31fe0e11bb02cb163f9dba05be97a8e8 |
| 21:01:38 | https://api.github.com/repos/jaredwilder/erdos902 | 200 | 5979 | 22537cf7113154f6 |
| 21:01:52 | https://raw.githubusercontent.com/jaredwilder/erdos902/main/README.md | 200 | 5637 | fc8e73ee7984f75d |
| 21:02:32 | https://api.github.com/repos/elder-plinius/V3R1T4S | 200 | 5892 | 7af01ac0f5a61685 |
| 21:02:33 | https://api.github.com/repos/elder-plinius/V3R1T4S/commits/main | 200 | 15225 | ee79f67dea4a96d9 |
| 21:02:49 | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/c027ca3e0c8d1fc475d8e39cccd4b146fd50ffb8/TROPHY_CASE.md | 200 | 31306 | 83af764f5a6551a5a27bbb135324931659bda04e60b66a2c0e711b991b356113 |
| 21:02:50 | https://api.github.com/repos/elder-plinius/V3R1T4S/git/trees/c027ca3e0c8d1fc475d8e39cccd4b146fd50ffb8?recursive=1 | 200 | 2049151 | f3df364663fb1de3 |
| 21:02:52 | https://api.github.com/repos/elder-plinius/V3R1T4S/compare/8846324a8fe813bf89a9ef2a60eb9b13d0ba79fd...c027ca3e0c8d1fc475d8e39cccd4b146fd50ffb8 | 200 | 650569 | 003734170fe2eb22 |
| 21:03:05 | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/c027ca3e0c8d1fc475d8e39cccd4b146fd50ffb8/known-unknowns/graphs-games-automata/schutte-multiple-tournament-dice-bounds.md | 200 | 5638 | ecf021110c60705fb72e488ad5d14cc823eab4604193f6e9d01f0e489a12cd13 |
| 21:03:27 | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100&page=1 | 200 | 2563018 | 4208dd4fda660ff9 |
| 21:03:29 | (same, page=2) | 200 | 2445450 | c0aa64a14ec5d175 |
| 21:03:31 | (same, page=3) | 200 | 2427633 | 5712c32c51e383d7 |
| 21:03:32 | (same, page=4) | 200 | 1211223 | 9f0113cfe2ce3143 |
| 21:04:07 | https://api.github.com/search/issues?q=repo:elder-plinius/V3R1T4S+schutte&per_page=100 | 200 | 4417 | 7d48c1c7b17310ab |
| 21:04:11 | https://api.github.com/search/issues?q=repo:elder-plinius/V3R1T4S+2604.08790&per_page=100 | 200 | 4417 | 7d48c1c7b17310ab |
| 21:04:15 | https://api.github.com/search/issues?q=repo:elder-plinius/V3R1T4S+tournaments+dice&per_page=100 | 200 | 4417 | 7d48c1c7b17310ab |
| 21:04:20 | https://raw.githubusercontent.com/elder-plinius/V3R1T4S/c027ca3e0c8d1fc475d8e39cccd4b146fd50ffb8/bank/targets.json | 200 | 2146913 | 7c10835a078dd0ed24154e89da3a0138a11fe4c52c89627f28989429b88fe38d |
| 21:04:32 | https://api.github.com/repos/elder-plinius/V3R1T4S/pulls/694 | 200 | 19758 | 89d8cf1e2644b4e8 |
| 21:04:33 | https://api.github.com/repos/elder-plinius/V3R1T4S/issues/694/comments?per_page=100 | 200 | 2644 | 203ee11fd365109f |
| 21:04:46 | https://raw.githubusercontent.com/r-nikhil/INVENTA/main/problems/schutte-multiple-tournament-dice-bounds.md | 200 | 2169 | b12fa49ccc9021d10980fad57b011e767d65059f1f5835e8c34d5a42d68ef67c |
| 21:05:13 | https://export.arxiv.org/api/query?search_query=all:Schutte+AND+all:tournament&sortBy=submittedDate&sortOrder=descending&max_results=50 | 200 | 2240 | e5addbde54677976 |
| 21:05:19 | (arXiv API) search_query=abs:%22sets+of+tournaments%22 (same parameters) | 200 | 69652 | 632b596fa1b5aa60 |
| 21:05:25 | (arXiv API) search_query=all:tournament+AND+all:dice | 200 | 19442 | 5fc0360ad26de39f |
| 21:05:30 | (arXiv API) search_query=abs:paradoxical+AND+abs:tournaments | 200 | 15735 | 3f8b69a1ad2b4f77 |
| 21:05:52 | (arXiv API) search_query=all:Sch%C3%BCtte | 200 | 211303 | 54d53eb01eca197f |
| 21:05:58 | (arXiv API) search_query=abs:k-paradoxical | 200 | 118309 | cc47d12c027d3070 |
| 21:06:03 | (arXiv API) search_query=all:Erdos+AND+all:Schutte | 200 | 2230 | 613540ce59da8422 |
| 21:06:09 | https://api.semanticscholar.org/graph/v1/paper/arXiv:2604.08790/citations?fields=title,year,externalIds,publicationDate&limit=100 | 200 | 26 | b890c0f15f5c03ba |
| 21:06:10 | https://api.crossref.org/works?query.bibliographic=Sch%C3%BCtte+property+sets+of+tournaments+dice&rows=20 | 200 | 7580 | 481d0efcaf6c2a27 |
| 21:06:39 | https://api.crossref.org/works/10.31274/td-20250502-307 | 200 | 1363 | 0df62ea93023df64 |
| 21:06:49 | https://dr.lib.iastate.edu/handle/20.500.12876/Ewpa01Ov | refused by this sandbox's proxy (never reached the server) | - | - |
| 21:07:58 | https://dr.lib.iastate.edu/handle/20.500.12876/Ewpa01Ov (301 to /entities/publication/33a1fdb3-3801-4087-ae1e-5b3dd4ac6c6c) | 200 | 735468 | 00566105c8b59b204fb71705288f2694bc71444b8bd11e7efb72e5af39bb63a3 |
| 21:08:30 | https://dr.lib.iastate.edu/bitstreams/6f2ce53a-ab52-4d94-bbc7-bab801e54fd3/download (one 302) | 200 | 790604 | 6b04b8ec2e3d975f7a27f25974136ac8bea2b46c7f69c9da15033fa48dbf1e1a |
| 21:09:37 | https://api.github.com/search/issues?q=%222604.08790%22&per_page=100 (all of GitHub) | 200 | 4417 | 7d48c1c7b17310ab |
| 21:09:42 | https://api.github.com/search/repositories?q=2604.08790+in:readme,description&per_page=50 | 200 | 54327 | ad8c5927d775c1b8 |
| 21:09:48 | https://api.github.com/search/repositories?q=schutte+tournaments+in:readme,description,name&per_page=50 | 200 | 53964 | 6ad87cd918cb3f3f |
| 21:10:11 | https://api.github.com/repos/ArtificialZeng/AI-Has-Taste | 200 | 6143 | c9cbb657aa00a41b |
| 21:10:12 | https://raw.githubusercontent.com/ArtificialZeng/AI-Has-Taste/HEAD/README.md | 200 | 343817 | 7ef8b71794f893cc |
| 21:10:14 | https://api.github.com/repos/jaredwilder/erdos902/git/trees/main?recursive=1 | 200 | 30677 | 93b521fdb53538e2 |
| 21:10:46 | https://raw.githubusercontent.com/ArtificialZeng/AI-Has-Taste/main/reproducible_source_code/BigWIN2/BW2-B87-P01/source/manuscript/main.tex | 200 | 8335 | 91ced0beec4f39bfdd0442ff4527fb1bb27778b97d284b2ea93d20d929b78721 |
| 21:11:01 | https://oeis.org/search?q=Schutte+tournament&fmt=json | 200 | 4157 | 1c931ade73ddb3a9 |
| 21:11:13 | https://oeis.org/search?q=2,4,6,10+tournament&fmt=json | 200 | 9021 | dd686bad4c3b47b5 |
| 21:11:17 | https://oeis.org/search?q=3,5,7,9+tournaments+dominated&fmt=json | 200 (null: no match) | 4 | 74234e98afe7498f |
| 21:11:20 | https://oeis.org/search?q=paradoxical+tournament&fmt=json | 200 | 4157 | 1c931ade73ddb3a9 |
| 21:12:37 | https://api.github.com/search/issues?q=repo:elder-plinius/V3R1T4S+Sch%C3%BCtte&per_page=100 | 200 | 4417 | 7d48c1c7b17310ab |
| 21:12:42 | https://api.github.com/search/issues?q=repo:elder-plinius/V3R1T4S+Jeffries&per_page=100 | 200 | 101 | 840185ac69ff01c9 |
| 21:12:45 | https://api.crossref.org/works?query.title=Sch%C3%BCtte%27s+property+for+sets+of+tournaments+and+an+application+to+dice+games&rows=10 | 200 | 3314 | 3fad9e304ef3cc06 |
| 21:13:41 | (arXiv API) search_query=all:Sch%C3%BCtte+AND+all:tournament | 200 | 2469 | eea8b80c480ba75b |
| 21:13:47 | (arXiv API) search_query=abs:tournaments+AND+abs:Erdos+AND+abs:dominated | 200 | 4349 | a257df1a42fcba9c |
| 21:15:29 | https://api.zbmath.org/v1/document/_search?search_string=Sch%C3%BCtte%20tournament%20py%3A2024-2026 | refused by this sandbox's proxy; not requested again | - | - |

Web searches (search engine, not page fetches): Jeffries dissertation title; "Schütte's property" sets of tournaments f(m,k); jaredwilder erdos902 Schütte; Jeffries dissertation Iowa State; exact dissertation title; "f(2,5)" tournaments Schütte SAT; Jeffries f(m,k) lower bound exact value 2026; "Joel Jeffries" tournaments dice Schütte 2026.

pass: true
