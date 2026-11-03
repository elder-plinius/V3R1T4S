# NOVELTY skeptic verdict: (61,25,3) covering design with 27 blocks

role: NOVELTY
context: subagent (Claude Code Agent tool, fresh context that saw only claim/)

Claim tested: claim/CLAIM.md says claim/C61_25_3_27blocks.txt (sha256 097a9067d0628e1d3ba01f6230bafbcab3573b78f4d0c9913b8759676e00a18e, recomputed and matching) is a (61,25,3) covering with b = 27, against a best known 28.
Scope: novelty only, meaning whether 27 is strictly below every known value. Whether the object really covers all 3-subsets is not checked here.

Method: I fetched each URL once with `curl -s -A "V3R1T4S-research-agent (curl)" -o FILE -w '%{http_code}' URL` and took the time from `date -u` just before each request. I made no retries and sent no cookies. The one redirect was followed once. Saved files are named below relative to the novelty work folder (fetched/...).

## 1. coveringrepository.com (live table)

- URL: https://coveringrepository.com/download_archive_vkt.aspx
  - fetched 2026-10-15T23:15:56Z, HTTP 200, 171741 bytes, sha256 85d2521a14ebaabf6161ab002f4fa41b98c2a5d1892c7dff0dfa4fd8c68c9d17 (fetched/crep_download_archive_vkt.html). It is byte-identical to claim/table_record/coveringrepository_download_archive_vkt.html.
  - Row read: `61<TAB>25<TAB>03<TAB>03<TAB><TAB>28` (v=61, k=25, t=3, m=3, blocks=28). **Live value: 28.**
  - 9490 rows parsed, all with m = t, covering v 4..99, k 3..25 and t 2..8.
  - Neighbouring live cells: (60,24,3)=28, (60,25,3)=26, (61,24,3)=31, (62,25,3)=29, (59,23,3)=31.
- URL: https://coveringrepository.com/ (status source)
  - fetched 2026-10-15T23:15:57Z, HTTP 200, sha256 460945ed92ab57b72bef29741794cc7454ac23c60d6ff4b504cfae9784a327eb (fetched/crep_home.html).
  - It says: "(v,k,t)-covering designs Coverings online: 9.490 / 9.490" and "Allowed values: 4 ≤ v ≤ 99, 3 ≤ k ≤ 25, 2 ≤ t ≤ 8".
  - **(61,25,3) is inside the allowed range and the cell is listed.** The page also says historical data up to the end of March 2026 were imported from the Gordon repository.
- URL: https://coveringrepository.com/systems.aspx?li=2 (latest (v,k,t) improvements)
  - fetched 2026-10-15T23:15:58Z, HTTP 200, sha256 bb756993a86bfe8eac28c09b19284e9f0eef3259469164bbe366feb7ec1e32d5 (fetched/crep_systems_li2.html).
  - It lists 100 improvement entries dated 30/09/2026 to 14/10/2026. **None is for (61,25,3).**
  - The only k=25, t=3 entries are v=73 (39), 94 (82), 95 (83), 96 (83) and 97 (83).
  - Freshness check: the block count of every one of the 100 entries equals the download archive's value for that cell. So the archive includes improvements up to at least 14/10/2026.

## 2. LJCR, Zenodo, dmgordo/LJCR on GitHub

- URL: https://dmgordon.org/covering-designs/
  - fetched 2026-10-15T23:16:55Z, HTTP 200, sha256 a5cc2312afc8dedd17c52410c34d518396d0a42982b2af429c8dc54f9e7170e3 (fetched/ljcr_home.html).
  - The page has no per-cell values. It states the limits "v ≤ 100, k ≤ 25, and t≤8" and points to coveringrepository.com and to Zenodo DOI 10.5281/zenodo.10779736. Footer: "Site last updated 2026-09-03".
- URL: https://zenodo.org/api/records/19472830/versions/latest
  - fetched 2026-10-15T23:16:55Z, HTTP 301, location https://zenodo.org/api/records/19735294. The body was saved as fetched/zenodo_latest_body.txt, sha256 4ad78d1e7ce2ecd1971d2ee470c122f3dca21ef428e895e5fd64d5cc1142f701.
- URL: https://zenodo.org/api/records/19735294 (the redirect, followed once)
  - fetched 2026-10-15T23:17:05Z, HTTP 200, sha256 11d3aca9c015d33d977ccf2b6066fc6b7c1d697bdc9854e89c048450806d207e.
  - Record: "La Jolla Coverings Repository", version 1.2, publication_date 2026-04-24, conceptrecid 10779736. Its file list includes coverdata.json with size 8319503 and md5 b2c626b07f216aac830d344eff5ad523.
- URL: https://zenodo.org/api/records/19735294/files/coverdata.json/content
  - fetched 2026-10-15T23:17:41Z, HTTP 200, 8319503 bytes, sha256 9e7da3710921066b10234fdc95379a18df3a7d3ae0f8a08ae188ea6bbca92f87 (the same hash the claim cites). The md5 matches the Zenodo record.
  - Entry: `"C(61,25,3)": {"size": 28, "low_bd": 22, "imps": [["28", "Simple construction from (60,24,3)", "LJCR", "2009-01-21 20:48:47"], ["31", "Dynamic programming construction", "LJCR", "2009-01-11 18:16:45"]]}`.
  - **LJCR/Zenodo value: 28, lower bound 22.** The newest improvement timestamp anywhere in the dataset is 2026-04-20.
- URL: https://api.github.com/repos/dmgordo/LJCR/commits?per_page=3
  - fetched 2026-10-15T23:16:56Z, HTTP 200, sha256 3e8cc07a2a2497792b73ee0ef0b79a9d1dee5cc2183c47dd64f6f9f9b6b25167.
  - Last commit: 459bcaf247bd at 2022-12-19T18:10:24Z, "Add files via upload".
- URL: https://api.github.com/repos/dmgordo/LJCR/contents/coverings
  - fetched 2026-10-15T23:21:50Z, HTTP 200, sha256 84470afe20137cebd74b507ff55cfcf16717c88bd1ab8b7f706b094bd991e427.
- URL: https://raw.githubusercontent.com/dmgordo/LJCR/main/coverings/coverdata.json
  - fetched 2026-10-15T23:21:57Z, HTTP 200, 6517686 bytes, sha256 0984bb8b4c89fe07268569b9814794e3c8852302d075f0794140f202e83d7fef.
  - 8759 entries, all with k between 3 and 24. **There is no C(61,25,3) entry.**
  - It has C(60,24,3)=28, which gives C(61,25,3) ≤ 28 by adding one point to every block. It has C(61,24,3)=32.
- Extra source, not a binding one: https://ljcr.dmgordon.org/show_cover.php?v=61&k=25&t=3
  - fetched 2026-10-15T23:22:10Z, no HTTP response (curl http_code 000). Not retried.

## 3. Simple constructions from live table values

- Adding points to every block, deleting points, enlarging blocks, or using a higher-t covering: the best is 28, from (60,24,3)=28.
- Recursion C(60,25,3) + C(60,24,2) = 26 + 9 = 35.
- Direct-sum constructions over all splits: best 41.
- Lower bounds: Schonheim L(61,25,3) = 20, and the LJCR records low_bd = 22.

No simple construction gives 27 or fewer.

## 4. arXiv (export.arxiv.org API, sorted by submittedDate descending, max_results=100)

| Query | Fetched | HTTP | totalResults | since 2024-10-15 | since 2026-04-15 | sha256 |
|---|---|---|---|---|---|---|
| `search_query=all:"covering design"` | 2026-10-15T23:18:48Z | 200 | 54 | 21 | 10 | 10ae431e4e8f46c06e8ddc6b0f8c1a857a8737793911ccc5e62d6d9941294c5b |
| `search_query=all:"covering designs"` | 2026-10-15T23:18:49Z | 200 | 54 (same set) | 21 | 10 | 163bbb3da1a7ccb5aac33548ab0662455aaa61c5034b29626b70dd7d807aedab |
| `search_query=abs:"covering number" AND abs:"blocks"` | 2026-10-15T23:18:50Z | 200 | 26 | 14 | 7 | 0d49b529c4bb8618e8b28ccfe7ad8cb7288f0135070c49af65c304aeb3d52600 |

- No title or abstract matches 61,25,3.
- The covering-design papers among the results are about other parameters:
  - 2607.23766, "The covering number C(12, 6, 4) is 41"
  - 2607.10978, a single-change covering design with v=26, k=6
  - 2603.24170, the 6/49 lottery and a (49,6,5) covering
  - 2502.12897, fractional-repetition codes from covering designs
  - 2609.23094, nearest-neighbour Boolean functions

## 5. GitHub search (unauthenticated repository and issue search)

| Search | Fetched | HTTP | total_count | sha256 |
|---|---|---|---|---|
| repositories q="covering design" sort=updated | 2026-10-15T23:19:13Z | 200 | 117 | 36cd82bee134136b515fef5fb690396a35ea345371cf7d168c200f601b21709c |
| repositories q="covering designs" | 2026-10-15T23:19:18Z | 200 | 8 | 4068dcc05ae0fbe1814f0962eb9d545524ccbe15d360542035055c684ea1edde |
| repositories q="61,25,3" | 2026-10-15T23:19:19Z | 200 | 0 | 08c082fdf7ca87ba911a2aabb0f0cf2d3e482a6feeaac9713e4578c20b2600b2 |
| issues q="C(61,25,3)" | 2026-10-15T23:19:19Z | 200 | 0 | 840185ac69ff01c964c2bfead7f7b8a5a7764c3814155124f82ebe285189a90f |
| issues q="61,25,3" covering | 2026-10-15T23:19:20Z | 200 | 0 | 840185ac69ff01c964c2bfead7f7b8a5a7764c3814155124f82ebe285189a90f |
| issues q="covering design" created:>2024-10-15 | 2026-10-15T23:19:20Z | 200 | 64376 | a2b2f89fec1569a8343d9813b7e418a81b6450b97b43b7f563957c7caa438bd4 |

The last search did not enforce the phrase. Of the 100 newest results, only 2 contain "covering design" at all, and neither mentions (61,25,3).

I fetched the README of each combinatorial covering-design repository active in the last 24 months once, via https://api.github.com/repos/<repo>/readme:

| Repository | Fetched | HTTP | sha256 | Cells claimed |
|---|---|---|---|---|
| thebrockchain/covering-designs (the hobbyist repo named in the criterion) | 2026-10-15T23:19:52Z | 301 to https://api.github.com/repositories/1326363899/readme | | see next row |
| the redirect, followed once | 2026-10-15T23:20:20Z | 200 | 171f9f5e88341cc90576de0f3016d0ed67569c54e33c1ed16ae729d49b066da5 | identical to the TheEslabonGroup/covering-designs README (2026-10-15T23:19:53Z, HTTP 200, same hash); claims only C(28,13,4) ≤ 53 and C(32,13,4) ≤ 95 |
| nickroci/fuzzy-solvers | 2026-10-15T23:19:55Z | 200 | 12ab529e6fde9d6d28798aa9eb624c6d4e8e81334b71be2883eab70dca9a3103 | only t=2 cells: C(41,9,2), C(56,13,2), C(65,14,2), C(82,19,2), C(98,22,2) |
| vibemathing/problem-um-opg-762-combinatorial-covering-designs-0fa59888 | 2026-10-15T23:19:56Z | 200 | d16000bc3387e92529ec7eef2f36986f164213c83280b5767001d9a3030ef7eb | no cell values |
| Soulxlight/covering-design-c54-16-4 | 2026-10-15T23:19:58Z | 200 | 758e03b13ed72c1d0d686595b4608445bde55c120d5d482fa6ec32b7b7a1b258 | C(54,16,4) |
| edwares/horizonmath-c13-7-4 | 2026-10-15T23:20:00Z | 200 | 6b533f9ba0cbca61c1ef6591510e46f5b8a9442831be49573e51317092386560 | C(13,7,4) |
| ozgronurkoc/Twmq | 2026-10-15T23:20:02Z | 200 | 7f1d3c59b7fe55c34bea2bf1724dea17954ec4c92c6f6d80b7a23e4303d4a7cb | lottery (Spor Toto) code |
| jimmylai-921/lotto_covering_design | 2026-10-15T23:20:04Z | 404 | | no README |
| gimenezhiago/CoveringDesign | 2026-10-15T23:20:06Z | 404 | | no README |
| gooverdian/covering-designs-finder | 2026-10-15T23:20:08Z | 200 | 92707113fa5ab10d1c5b269468f9eff10c91882b497f9927e63faaaccce275ec | no cell values |
| forsing/Data-Science-16 | 2026-10-15T23:20:10Z | 200 | 7703c6cb529bd50471efe2cd6fb005d0a357c054705fe40d336ce5439ca49d79 | no cell values |

I searched every README for 61/25, "C(61" and "(61,". There were no matches.

## 6. General web search (search tool, 3 queries)

Queries:
- "C(61,25,3)" covering design
- "(61,25,3)" covering design blocks
- covering design v=61 k=25 t=3 27 blocks new upper bound 2026

Results: the classic Gordon-Kuperberg-Patashnik papers, Wikipedia, the LJCR pages, and arXiv 2601.06179 and 2601.04295 (which are about k=6 designs on [60], other parameters). No result gives a value for C(61,25,3).

## 7. This repo (elder-plinius/V3R1T4S)

- URL: https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md
  - fetched 2026-10-15T23:20:42Z, HTTP 200, sha256 738c07a33b810df76139ecbe71a1aa3e96c4e845a27d9f8887dff4f08a7afcc9, 100 lines.
  - There is no covering-design entry. "cover" appears only in line 14 (Lehmer totient: "Lean 4 covers the reduction") and line 34 ("recovered").
- URL: https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100
  - fetched 2026-10-15T23:20:43Z, HTTP 200, sha256 2ecd856e10100832a1d55c46bc09b4ebdc7025454d17c801fa620580b4275681.
  - 14 open PRs. **None concerns covering designs or (61,25,3).** "cover" appears only in #198 ("Tests cover"), #192 ("certificates covering one theorem") and #191 ("discovered").

## Injection check

I searched every fetched page for instruction-like text and found none. injection_suspected: none.

## Concerns

1. This verdict covers novelty only. It holds only if another panel member's exhaustive check confirms that the 27-block file covers all 35990 triples. The value 27 does not conflict with any known lower bound: the LJCR low_bd is 22 and Schonheim is 20. (claim/REPRODUCE.md quotes Schonheim 20; the LJCR bound of 22 is stronger, and 27 is above both.)
2. This is a snapshot taken between 2026-10-15T23:15:56Z and 23:22:10Z. coveringrepository.com is actively updated: 100 improvements in about two weeks, including k=25, t=3 cells on 30/09/2026. The cell should be re-checked when the claim is merged.
3. The searches have limits:
   - Unauthenticated GitHub code search is not available, so file contents inside repositories were not searched; only repository metadata, READMEs, issues and PRs were.
   - The arXiv API searches titles and abstracts only, so a table inside a paper's full text could be missed.
   - GitHub issue search did not enforce the quoted phrase.
4. The legacy LJCR per-cell host did not respond. The binding LJCR page has no per-cell values and points to Zenodo and coveringrepository.com, so the Zenodo v1.2 value (28) was used as the LJCR value.
5. Context, not an objection: this cell has stood at 28 since 2009, set by a simple construction, which suggests it is little explored rather than hard.

## Conclusion

27 is strictly less than every value found:
- 28, live coveringrepository.com (m = t row; the table was read with HTTP 200)
- 28, LJCR/Zenodo v1.2
- the dmgordo/LJCR GitHub snapshot has no k=25 entry, and its (60,24,3) value implies ≤ 28
- no value of 27 or less in arXiv (24 and 6 months), GitHub repositories, issues or hobbyist claims, the web search, TROPHY_CASE.md or the open PRs
- no simple construction from live cells gives 27 or less

The parameters are within the table's allowed range. This is a strict improvement of 1, not a tie.

pass: true
