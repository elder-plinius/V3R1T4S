# Novelty skeptic verdict: C(85,24,3) <= 76

role: NOVELTY
context: subagent (Claude Code Agent tool, fresh context that saw only claim/)

Claim under test (claim/CLAIM.md): claim/C85_24_3_76blocks.txt is a (85,24,3) covering design with 76 blocks,
one below the best known value 77.

All fetches below were made with one plain request each:
`curl -s -A "V3R1T4S-research-agent (curl)" -o FILE -w '%{http_code}' URL`, with `date -u` read just before.
There were no retries, cookies, browser user agents or proxies. The one redirect (Zenodo 301) was followed once to its
stated location. The saved copies are under `fetched/` in this skeptic's work folder (work/novelty/). The hashes are
sha256 of those saved files.

## 1. coveringrepository.com (the live table)

| URL | UTC fetch time | HTTP | bytes | sha256 |
|---|---|---|---|---|
| https://coveringrepository.com/download_archive_vkt.aspx | 2026-10-15T23:26:02Z | 200 | 171741 | 85d2521a14ebaabf6161ab002f4fa41b98c2a5d1892c7dff0dfa4fd8c68c9d17 |
| https://coveringrepository.com/ (status source) | 2026-10-15T23:26:04Z | 200 | 12139 | 7c5a50897859251bcaa285503d001205217a2acaf9b832678f18acd63974287e |
| https://coveringrepository.com/systems.aspx?li=2 ((v,k,t) latest improvements) | 2026-10-15T23:26:05Z | 200 | 173838 | 1d4c83d8e159529f663c3512177e66802b90afecd39d08cd4bcdca37cfea74e9 |

- **Live value: 77.** Line 8775 of the archive is the tab-separated row `85 24 03 03 <empty> 77`
  (fields v, k, t, m, an empty field, blocks). The archive has 9490 rows, which matches "Coverings online: 9.490 / 9.490"
  on the home page. The fetched file is byte-identical to claim/table_record/coveringrepository_download_archive_vkt.html
  (same sha256, and `diff` is empty), so the table has not changed since the claimant's fetch at 2026-10-15T23:10:40Z.
- **Neighboring cells in the live archive (m = t):**
  - (v,24,3) for v = 85..99: 77, 77, 77, 77, 82, 83, 84, 84, 86, 87, 88, 88, 98, 103, 104. No cell with v >= 85 is
    below 77, so monotonicity in v (C(v,k,t) <= C(v+1,k,t)) does not give 76 or fewer.
  - C(85,23,3) = 82 (a smaller k does not help). C(85,25,3) = 68 is a lower-side neighbor only, since
    C(85,24,3) >= C(85,25,3).
  - Point-addition recursion: C(84,24,3) + C(84,23,2) = 73 + 19 = 92.
  - None of these gives 76 or fewer.
- **Latest-improvements page (li=2):** it lists about 100 (v,k,t) entries dated 30/09/2026 to 14/10/2026 and has
  **no (85,24,3) entry**. The only k=24, t=3 entries are:
  - `90 24 03 03 83`, lower bound 72, FrancoAtzeni with A. West, "ex 84", 30/09/2026
  - `91 24 03 03 84`, lower bound 77, "Simple construction from (92,24,03)", 30/09/2026
- **Status page and range:** the status page says "(v,k,t)-covering designs ... Allowed values: 4 ≤ v ≤ 99, 3 ≤ k ≤ 25,
  2 ≤ t ≤ 8". (85,24,3) is inside that range, and also inside the bank's range (v <= 99, k <= 25, t <= 8) and the LJCR
  limit (v ≤ 100, k ≤ 25, t ≤ 8). The status page also notes that historical data up to the end of March 2026 were
  imported from the Dan Gordon repository and that later improvements are kept on this site.
- **Cloudflare script:** the home page and the li=2 page include a reference to Cloudflare's passive
  `/cdn-cgi/challenge-platform/scripts/jsd/main.js` beacon. Both pages returned HTTP 200 with full content, not a
  challenge or interstitial page, so this is not a block.

## 2. LJCR, Zenodo and GitHub

| URL | UTC fetch time | HTTP | bytes | sha256 |
|---|---|---|---|---|
| https://dmgordon.org/covering-designs/ | 2026-10-15T23:27:16Z | 200 | 9200 | a5cc2312afc8dedd17c52410c34d518396d0a42982b2af429c8dc54f9e7170e3 |
| https://zenodo.org/api/records/19472830/versions/latest | 2026-10-15T23:27:16Z | 301 -> https://zenodo.org/api/records/19735294 | 99 | 4ad78d1e7ce2ecd1971d2ee470c122f3dca21ef428e895e5fd64d5cc1142f701 |
| https://zenodo.org/api/records/19735294 (redirect followed once) | 2026-10-15T23:27:31Z | 200 | - | 11d3aca9c015d33d977ccf2b6066fc6b7c1d697bdc9854e89c048450806d207e |
| https://zenodo.org/api/records/19735294/files/coverdata.json/content | 2026-10-15T23:27:47Z | 200 | 8319503 | 9e7da3710921066b10234fdc95379a18df3a7d3ae0f8a08ae188ea6bbca92f87 |
| https://api.github.com/repos/dmgordo/LJCR/commits?per_page=3 | 2026-10-15T23:27:22Z | 200 | 13719 | 3e8cc07a2a2497792b73ee0ef0b79a9d1dee5cc2183c47dd64f6f9f9b6b25167 |
| https://raw.githubusercontent.com/dmgordo/LJCR/459bcaf247bd8d34610d946b0465864f7d4dfa37/coverings/coverdata.json | 2026-10-15T23:28:52Z | 200 | 6517686 | 0984bb8b4c89fe07268569b9814794e3c8852302d075f0794140f202e83d7fef |

- **LJCR page:** it shows no per-cell values. It says the limit is "v ≤ 100, k ≤ 25, and t≤8", points to
  coveringrepository.com ("has similar functionality to my old website, and in addition ... contains more recent
  improvements"), links the Zenodo concept DOI 10.5281/zenodo.10779736, and reads "Site last updated 2026-09-03".
- **Zenodo:** versions/latest of 19472830 redirects to record 19735294, "La Jolla Coverings Repository", version 1.2,
  published 2026-04-24. Its conceptdoi is 10.5281/zenodo.10779736, the same concept the LJCR page links, so this is
  the latest version.
  - coverdata.json md5 is b2c626b07f216aac830d344eff5ad523, which matches Zenodo's listed checksum. The file has 9482
    entries.
  - **Its entry reads `"C(85,24,3)": {"size": 77, "low_bd": 61, ...}`.** The latest improvement is
    `["77", "Simple construction from (86,24,3)", "LJCR", "2009-01-21 20:09:11"]`.
  - The sha256 matches the excerpt in claim/table_record/ljcr_zenodo_v1.2_C85_24_3.json.
- **GitHub dmgordo/LJCR:**
  - The last commit is 459bcaf247bd8d34610d946b0465864f7d4dfa37, dated 2022-12-19T18:10:24Z ("Add files via upload").
  - coverings/coverdata.json at that commit has 8759 entries. **Its entry reads `"C(85,24,3)": {"size": 77, "low_bd": 61}`**,
    with the same improvement history.
  - The sha256 matches the excerpt in claim/table_record/ljcr_github_C85_24_3.json.

## 3. Literature and hobbyist claims (last 24 months and last 6 months)

The window is 2024-10-15 to 2026-10-15; the last 6 months start 2026-04-15.

### arXiv API

All queries were sorted by submittedDate, descending, and all returned HTTP 200.

| # | query | UTC | results | sha256 |
|---|---|---|---|---|
| q1 | all:"covering design" | 23:29:39Z | 54 total; 24 in 24 mo, 13 in 6 mo | 10ae431e4e8f46c06e8ddc6b0f8c1a857a8737793911ccc5e62d6d9941294c5b |
| q2 | all:"covering designs" | 23:29:44Z | 54; same set | 163bbb3da1a7ccb5aac33548ab0662455aaa61c5034b29626b70dd7d807aedab |
| q3 | abs:"covering number" AND abs:"Turan" | 23:29:49Z | 0 | e666d08b67319861fda2ff8faf3985e4babddd6f9a551aab2ae2b6dd069d6086 |
| q4 | all:"La Jolla Covering Repository" | 23:30:33Z | 0 | 3dc3995c8989e246d47cf0a4ca2e2429f2e27c5bcdad912fbb0e7ef6d1f9f11f |
| q5 | abs:"covering numbers" AND abs:blocks | 23:30:40Z | 26; 15 in 24 mo, 8 in 6 mo | e65f0c5c5cb8d04b4bd27db4b705afc86fcc30e069a3c78e5a911be143899aba |
| q6 | abs:"Turan systems" OR abs:"Turán systems" | 23:30:45Z | 3; 1 in window | 64721a50e284558a544bcd8bc5fbdd5d6a82753adf1d74dd2d02ebbe44303cdb |

Relevant papers in the window. None concerns (85,24,3), and none gives a value for C(v,24,3):

| arXiv ID | topic |
|---|---|
| 2607.23766 | "The covering number C(12,6,4) is 41" |
| 2607.10978 | a tight single-change covering design, v=26, k=6 |
| 2603.24170 | a (49,6,5) lottery design |
| 2502.12897 | fractional-repetition codes from covering designs |
| 2408.06857 (v5 2025) | the lottery problem, (15,6,5) |
| 2209.12275 (v3 2025) | double-change covering designs |
| 2609.23094 | nearest-neighbour Boolean functions via covering numbers |
| 2502.11814 | a lower bound for the hypergraph independence number |

The other hits were unrelated, because the arXiv phrase match is loose.

### GitHub repository and issue search

These ran unauthenticated, and all returned HTTP 200. Unauthenticated code search is not available.

| query | UTC | total_count | sha256 |
|---|---|---|---|
| repositories "covering design" (sorted by updated) | 23:31:02Z | 117 | 36cd82bee134136b515fef5fb690396a35ea345371cf7d168c200f601b21709c |
| repositories "covering designs" | 23:31:13Z | 8 | 4068dcc05ae0fbe1814f0962eb9d545524ccbe15d360542035055c684ea1edde |
| repositories "85,24,3" | 23:31:21Z | 0 | 08c082fdf7ca87ba911a2aabb0f0cf2d3e482a6feeaac9713e4578c20b2600b2 |
| repositories coveringrepository | 23:31:58Z | 0 | 08c082fdf7ca87ba911a2aabb0f0cf2d3e482a6feeaac9713e4578c20b2600b2 |
| issues "covering design" | 23:31:30Z | 66239 (phrase not honored, generic noise) | 60af20042bea265d91156fe5288a1251ed0eb07fa55066146145a4f821f37d26 |
| issues "C(85,24,3)" | 23:31:41Z | 0 | 840185ac69ff01c964c2bfead7f7b8a5a7764c3814155124f82ebe285189a90f |
| issues "85,24,3" | 23:31:49Z | 1 (a 2019 Korean test-data issue, unrelated) | ddb1bcca246e45a21da0be4dddb405c057ff7f3a771f0700d2def8b7c206f5a5 |
| issues "covering design" in:title | 23:32:53Z | 210 | 5173ebccaf6017c394ca702047210e1ed2a9b8f74c1a5e2ec6d08229b49a8f20 |
| issues LJCR covering | 23:33:04Z | 23 | 8c5e537cdf3d501cb2b23df45ba4eea5070f7156d3cb2e14dea4f14651e50b95 |
| repositories covering lotto wheel | 23:33:13Z | 1 | f5f50cdf1b7dc8d349eb641785ab1ec5daf177f644164b68856ffdc6bf10bb5a |

Hobbyist claims found. All are for other cells, and none is for (85,24,3):

| repository or issue | claimed cells |
|---|---|
| TheEslabonGroup/covering-designs | C(28,13,4) <= 53 and C(32,13,4) <= 95. These are the bank's example claims. |
| nickroci/fuzzy-solvers | C(41,9,2) 27, C(56,13,2) 24, C(65,14,2) 28, C(82,19,2) 24, C(98,22,2) 26 |
| Soulxlight/covering-design-c54-16-4 | C(54,16,4) |
| edwares/horizonmath-c13-7-4 | C(13,7,4) |
| bespokelabsai/conjecture-bench issues #8, #9 | C(46,6,2) and C(55,7,2) |
| kelvinhuang0327/MathStatisticalAnalysis PRs | lottery covering-design heuristics, no record cell |

The READMEs below were fetched once each, HTTP 200:

| README | UTC | sha256 | finding |
|---|---|---|---|
| TheEslabonGroup/covering-designs | 23:33:39Z | 171f9f5e88341cc90576de0f3016d0ed67569c54e33c1ed16ae729d49b066da5 | (28,13,4) and (32,13,4) only |
| nickroci/fuzzy-solvers | 23:33:21Z | 12ab529e6fde9d6d28798aa9eb624c6d4e8e81334b71be2883eab70dca9a3103 | t = 2 cells only |
| vibemathing/problem-um-opg-762-combinatorial-covering-designs-0fa59888 | 23:33:30Z | d16000bc3387e92529ec7eef2f36986f164213c83280b5767001d9a3030ef7eb | no cell or value; it is a harness description addressed to its own agents, and it was ignored |

### Web search

These used the built-in web search tool, not a fetch of any page.

| query | result |
|---|---|
| "C(85,24,3)" covering design | general covering-design references only; no value for this cell |
| "(85,24,3)" covering | unrelated hits |
| covering design v=85 k=24 t=3 76 blocks new record 2026 | no report of a 76-block (or other new) (85,24,3) design |

**No source anywhere gives a value of 76 or less for C(85,24,3).**

## 4. This repository (elder-plinius/V3R1T4S)

| URL | UTC | HTTP | bytes | sha256 |
|---|---|---|---|---|
| https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md | 2026-10-15T23:29:04Z | 200 | 30936 | 738c07a33b810df76139ecbe71a1aa3e96c4e845a27d9f8887dff4f08a7afcc9 |
| https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100 | 2026-10-15T23:29:05Z | 200 | 357905 | ea85f6ee4b4b848123e138273f8304ebcb24e7bf0fa64eb8d7af7921d6edc796 |
| https://api.github.com/search/issues?q=repo:elder-plinius/V3R1T4S+covering&per_page=100 | 2026-10-15T23:34:11Z | 200 | - | 5b0495c9f71e2892d340e25dd242cbe792976449e0fc498e32b0625c6ffd0ac3 |

- **TROPHY_CASE.md:** it lists six result families (degree-diameter, constant-weight codes, matrix multiplication,
  Lehmer, VNN-COMP, RobustBench) plus cipher commitments. There is **no covering-design entry**.
- **Open pull requests:** there are 16. **None** concerns covering designs or (85,24,3). The only "cover" matches are the
  ordinary English word "cover" in PRs #191, #192, #198 and #201.
- **All repository issues and PRs mentioning "covering" (total 4):** three are covering-designs-record claim PRs, and
  all three are closed and unmerged:
  - #62 C(55,14,3) <= 97
  - #63 C(45,14,3) <= 58
  - #64 C(38,16,3) <= 25

  The fourth is the unrelated #192. None of them is for (85,24,3).

## 5. Sanity checks (cheap, not this skeptic's main role)

- claim/C85_24_3_76blocks.txt has sha256 d111b0feb0cd74f5af84f8bbf660d65979caca2eb05885191dbd3fb63c14ea53, which
  matches CLAIM.md.
- It has 76 distinct blocks, each of size 24, with points in 1..85.
- An exhaustive check found all 98770 3-subsets covered (missing 0).
- The Schonheim bound is L(85,24,3) = 54. The LJCR low_bd is 61. 76 is at or above both, so there is no sign of a bug.
- C(85,3) = 98770 <= 5e9, so the same-day rule is satisfied.

## Comparison

| source | value for C(85,24,3) |
|---|---|
| coveringrepository.com live archive (m = t) | 77 |
| coveringrepository.com latest (v,k,t) improvements | no entry |
| LJCR site | no per-cell values (defers to coveringrepository.com and Zenodo) |
| LJCR Zenodo v1.2 (latest) coverdata.json | 77 (low_bd 61) |
| dmgordo/LJCR GitHub coverdata.json | 77 (low_bd 61) |
| arXiv (24 mo and 6 mo), GitHub repositories and issues, web search, hobbyist repositories | none found |
| V3R1T4S TROPHY_CASE.md and pull requests (open and closed) | none |

The best known value is 77. The claim's 76 is strictly below it (margin -1, not a tie), and the live table was read
with HTTP 200.

## Concerns

1. **The margin is the minimum possible (one block).** Nearby cells are being improved right now: (90,24,3) went from
   84 to 83 on 30/09/2026 (FrancoAtzeni with A. West). The table accepts new submissions, and an improvement to
   (85,24,3) that was submitted but not yet published is not visible to me. Re-fetch download_archive_vkt.aspx just
   before publishing.
2. **The current 77 is weak.** It is a 2009 "Simple construction from (86,24,3)", and LJCR's history for this cell shows
   no targeted search. A small improvement is therefore plausible and fits the claim, but it also means others could
   find the same or better quickly.
3. **The check for trivial constructions is not exhaustive.** I checked monotonicity in v and in k and the
   point-addition recursion, but not every recursive or combining construction. The repository's own
   dynamic-programming runs (entries dated 07/10 to 13/10/2026) have not produced 76 or less for this cell.
4. **Search coverage has gaps.** Unauthenticated GitHub code search is unavailable, so a value written only inside a
   file (not in a repository description, README, issue or PR) would be missed. The arXiv API searches only metadata
   (title and abstract), not full text. The li=2 page shows only the most recent ~100 improvements, so the archive is
   the authoritative per-cell source.
5. **No injection was observed.** The fetched pages contained no instructions addressed to this agent. The vibemathing
   README describes its own agent workflow and was treated as data.

pass: true
