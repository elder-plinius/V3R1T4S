role: NOVELTY
context: subagent (fresh context that saw only claim/)

# Novelty Panelist Report: C(41,12,5) <= 2207

## 1. Scope and Fresh-Context Attestation
This evaluation was performed in a fresh subagent context that inspected only the files inside `claim/` (`claim/CLAIM.md`, `claim/REPRODUCE.md`, `claim/C41_12_5_2207blocks.txt`, and `claim/table_record/*`) plus live external fetches and searches saved under `panel/work/novelty/`.

## 2. Live Authority and Table Verification (Single Plain Requests)

All live table endpoints were queried once using plain `curl.exe -s -L -A "V3R1T4S-research-agent (curl)"`:

1. **Covering Repository plain `(v,k,t)` archive (`https://coveringrepository.com/download_archive_vkt.aspx`)**
   - Fetched at `2026-10-16T02:08:02Z`, HTTP `200`, `171741` bytes, sha256 `85d2521a14ebaabf6161ab002f4fa41b98c2a5d1892c7dff0dfa4fd8c68c9d17` (saved to `panel/work/novelty/live_download_archive_vkt.html`).
   - Identical byte-for-byte to `claim/table_record/coveringrepository_download_archive_vkt.html` (`171741` bytes, sha256 `85d2521a14ebaabf6161ab002f4fa41b98c2a5d1892c7dff0dfa4fd8c68c9d17`).
   - Line 3150 of the file reads `41[TAB]12[TAB]05[TAB]05[TAB][TAB]2244`, confirming the live `coveringrepository.com` upper bound for `C(41,12,5)` is **2244**.

2. **Covering Repository interactive systems page (`https://coveringrepository.com/systems.aspx?li=2`)**
   - Fetched at `2026-10-16T02:08:03Z`, HTTP `200`, `173838` bytes, sha256 `3903b928c5f86ff159da0dcd728972cda21e80aa5fa9940e43a6047d938a3f49` (saved to `panel/work/novelty/live_systems_li2.html`).
   - Returns the default first page of the ASP.NET WebForms table; full per-cell values without WebForms postbacks are served by `download_archive_vkt.aspx` above.

3. **Dan Gordon LJCR overview page (`https://dmgordon.org/covering-designs/`)**
   - Fetched at `2026-10-16T02:08:03Z`, HTTP `200`, `9200` bytes, sha256 `a5cc2312afc8dedd17c52410c34d518396d0a42982b2af429c8dc54f9e7170e3` (saved to `panel/work/novelty/live_dmgordon.html`).
   - Hosts no per-cell table directly; delegates live tables to `coveringrepository.com` and archival snapshots to Zenodo.

4. **LJCR Zenodo dataset (`https://zenodo.org/api/records/19472830/versions/latest` and `https://zenodo.org/api/records/19735294`)**
   - Fetched at `2026-10-16T02:08:27Z` and `2026-10-16T02:16:52Z`, HTTP `200`, `5642` bytes, sha256 `11d3aca9c015d33d977ccf2b6066fc6b7c1d697bdc9854e89c048450806d207e` (saved to `panel/work/novelty/zenodo_latest.json` and `panel/work/novelty/zenodo_19735294.json`).
   - Confirms record `19735294` is the latest release (Version `1.2`, published `2026-04-24`), containing `coverdata.json` (`8319503` bytes, md5 `b2c626b07f216aac830d344eff5ad523`).
   - As recorded in `claim/table_record/ljcr_zenodo_v1.2_C41_12_5.json`, the Zenodo v1.2 entry for `C(41,12,5)` has `size: 2245` and `low_bd: 1121` (submitted `2026-02-28 23:37:02` by Jan de Heer and Steve Muir).

5. **LJCR GitHub repository (`https://api.github.com/repos/dmgordo/LJCR/commits?path=coverings/coverdata.json&per_page=5`)**
   - Fetched at `2026-10-16T02:08:31Z`, HTTP `200`, `4575` bytes, sha256 `04a66d1b65ceb0b860a67c6cf79e094428cb6a7dbd0d9efcf102808b2055829f` (saved to `panel/work/novelty/ljcr_commits.json`).
   - Confirms the last commit to `coverings/coverdata.json` is `2022-12-19`, where `C(41,12,5)` has `size: 2429` and `low_bd: 1121` (`claim/table_record/ljcr_github_C41_12_5.json`).

### Comparison Summary Against All Authorities
| Source | Best Known Upper Bound for C(41,12,5) | Claimed Value | Improvement |
| :--- | :---: | :---: | :---: |
| Live `coveringrepository.com` (`download_archive_vkt.aspx`) | 2244 | **2207** | -37 blocks |
| LJCR Zenodo v1.2 (`record/19735294`, 2026-04-24) | 2245 | **2207** | -38 blocks |
| `dmgordo/LJCR` GitHub (`coverings/coverdata.json`, 2022-12-19) | 2429 | **2207** | -222 blocks |
| Schonheim / LJCR Lower Bound (`L(41,12,5)` / `low_bd`) | 1070 / 1121 | **2207** | Valid (`2207 >= 1121`) |

## 3. Literature, Preprint, and Repository Novelty Search (Last 24 Months and Last 6 Months)

1. **arXiv Search (`panel/work/novelty/arxiv_web_search.html`, `arxiv_covering_designs.html`, `arxiv_c41_12_5.html`, `arxiv_41_12_5.html`, `arxiv_math_co.html`)**
   - Note: `export.arxiv.org` returned HTTP `429` rate-limiting, so direct queries were executed against `https://arxiv.org/search/` and `https://arxiv.org/search/math` (`HTTP 200`, 50 newest submissions per query sorted by announcement date) as well as Google web search (`search_web`).
   - Searches for `"C(41,12,5)"` and `"41, 12, 5" covering` returned **0** matches.
   - Recent 2025-2026 covering design preprints inspected include `arXiv:2607.10978` (7 Oct 2026, *A tight single-change covering design with block size 6*), `arXiv:2603.24170` (31 May 2026, *Tackling the 6/49 Lottery and Debunking Common Myths with Probabilistic Methods and Combinatorial Designs*), and Charlie Krug's July 2026 proof of `C(12,6,4) = 41`. None study or report bounds on `C(41,12,5)`.

2. **GitHub Repositories, Issues, and Pull Requests (`panel/work/novelty/search_results.txt`, `inspect_results.txt`)**
   - Queries across GitHub repositories and issues/PRs for `"C(41,12,5)"` (`0` repositories, `0` issues), `"41,12,5"` (`1` unrelated 2013 JS repo, `1` unrelated ECharts issue), `"covering design"`, and `"covering designs"` found no prior claim for `(41,12,5)`.
   - Explicitly audited all recent covering-design repositories active in 2025-2026:
     - `thebrockchain/covering-designs` and `TheEslabonGroup/covering-designs` (Aug-Sep 2026): contain only `C(28,13,4) <= 53` and `C(32,13,4) <= 95`.
     - `nickroci/fuzzy-solvers` (Sep 2026): reports five `t=2` designs (`C(41,9,2) <= 27`, `C(56,13,2) <= 24`, `C(65,14,2) <= 28`, `C(82,19,2) <= 24`, `C(98,22,2) <= 26`); nothing for `(41,12,5)`.
     - `Soulxlight/covering-design-c54-16-4` (Oct 2026): studies `C(54,16,4)` only.
     - `jamesyc/covering` (Oct 2026): Lean lower-bound proofs for `C(24,14,4) >= 20` and `C(25,15,5) >= 34`.
     - `vibemathing/problem-um-opg-762-combinatorial-covering-designs-0fa59888` (Sep 2026): general problem notes, no `(41,12,5)` design.

3. **V3R1T4S Trophy Case and Open Pull Requests (`panel/work/novelty/trophy_case.md`, `v3r1t4s_pulls.json`)**
   - Fetched `https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md` (`2026-10-16T02:08:30Z`, HTTP `200`, `30936` bytes, sha256 `738c07a33b810df76139ecbe71a1aa3e96c4e845a27d9f8887dff4f08a7afcc9`) and `https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100` (`2026-10-16T02:08:31Z`, HTTP `200`, `379445` bytes, sha256 `18126123be31b993a60af93f810458c6eb8a06ac2246ecaaccd72ba81140f4cb`, 17 open PRs).
   - Zero occurrences of `covering-designs-record`, `41,12,5`, `2207`, or `2244` in either `TROPHY_CASE.md` or open pull requests.

4. **General Web Search (`search_web`)**
   - Web searches for `"C(41,12,5)"`, `"41, 12, 5"`, `"2244"`, and `"2245"` with covering design keywords surfaced only the standard LJCR / Covering Repository references and no bound below `2244`.

## 4. Independent Sanity Check of `claim/C41_12_5_2207blocks.txt`

Executed in `panel/work/novelty/inspect_fetches.py`:
- **File size and hash**: `74496` bytes, sha256 `ec985f89dd793006ccf15346b6937419e1ce4e922034d73b18e769fb958778aa` (matches `claim/CLAIM.md` and `claim/REPRODUCE.md`).
- **Block structure**: `2207` non-empty lines, `2207` distinct blocks, every block has `12` distinct integers in `1..41`.
- **Parameter constraints**: `v = 41 <= 99`, `k = 12 <= 25`, `t = 5 <= 8`, `C(41,5) = 749398 <= 5e9`, and `b = 2207 >= L(41,12,5) = 1070` (and `>= 1121`).
- **Exhaustive coverage check**: All `749,398` 5-subsets of `{1, ..., 41}` were tested by bitmask containment; **0** 5-subsets are uncovered.

## 5. Conclusion

The claimed `(41,12,5)` covering design in `claim/C41_12_5_2207blocks.txt` with `2207` blocks is valid and strictly improves upon the live `coveringrepository.com` bound (`2244`, by 37 blocks), the Zenodo v1.2 bound (`2245`, by 38 blocks), and the `dmgordo/LJCR` GitHub bound (`2429`, by 222 blocks), with no competing or better bound (`<= 2207`) found anywhere in the literature, arXiv, GitHub, or V3R1T4S.

pass: true
