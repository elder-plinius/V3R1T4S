# Skeptic Panel Report: NOVELTY

role: NOVELTY
context: Antigravity fresh subagent (invoke_subagent, role NOVELTY)
target id: covering-designs-record
claim: `claim/design_94_13_5.txt` is a `(94,13,5)` covering design with `125184` blocks, strictly fewer than the `coveringrepository.com` `(v,k,t)` archive value `129203` and the LJCR value `129337` for `C(94,13,5)`.

## 1. Claimed Artifact Verification

- File: `claim/design_94_13_5.txt`
  - sha256: `e1080beca9b83194c0ebe19400b30ebc7bdc3dab17230e7bf153eddc625bc908`
  - Line count: `125184` blocks (`v = 94`, `k = 13`, `t = 5`, 0-based points `0..93`)
- Independent execution of `claim/author_checker_cover_check.py 94 13 5 claim/design_94_13_5.txt`:
  - `blocks=125184`, `distinct=125184`, `base=0`, `schonheim=42705`, `C_v_t=54891018`, `uncovered=0`, `COVER_CHECK: PASS`
- Bundled table snapshot `claim/cr_archive_vkt.txt`:
  - sha256: `78bf5453858b476b90eeebd8ee8a35454e5f31866dd5f629934083ca0cd9bee3` (`9629` lines, `171740` bytes)
  - Row `3648` for `(94,13,5)` (`m = t = 5`): `94	13	05	05		129203` (`94 13 05 05  129203`)

## 2. Honest Single-Fetch Live Primary Table Checks

Each primary source was fetched once with a single plain HTTP GET (`User-Agent: V3R1T4S-research-agent (honest single fetch)`), with no retries and no requests to `history.aspx` per-cell pages:

1. **Covering Repository plain `(v,k,t)` archive**
   - URL: `https://coveringrepository.com/download_archive_vkt.aspx`
   - Fetch timestamp (UTC): `2026-10-18T09:40:05Z`
   - HTTP status: `200`
   - Size: `171740` bytes (`9629` lines)
   - sha256: `78bf5453858b476b90eeebd8ee8a35454e5f31866dd5f629934083ca0cd9bee3` (matches `claim/cr_archive_vkt.txt` byte-for-byte)
   - Exact `(94,13,5)` row (line `3648`): `94	13	05	05		129203` (`94 13 05 05  129203`)
   - Live value: `b = 129203`

2. **La Jolla Covering Repository (LJCR) status page**
   - URL: `https://dmgordon.org/covering-designs/`
   - Fetch timestamp (UTC): `2026-10-18T09:40:05Z`
   - HTTP status: `200`
   - Size: `9200` bytes
   - sha256: `a5cc2312afc8dedd17c52410c34d518396d0a42982b2af429c8dc54f9e7170e3`
   - Page footer timestamp: `Site last updated 2026-09-03`

3. **Zenodo LJCR datasets (v1.1 and v1.2)**
   - Record `19472830` metadata (`https://zenodo.org/api/records/19472830`):
     - Fetch timestamp (UTC): `2026-10-18T09:40:05Z`, HTTP `200`, `5610` bytes, sha256 `b0d4317c730eb108f70322f00f2f8e64719786f39b5b6bd27b277a7b8eaa68a2`
     - Version `1.1`, publication date `2026-04-08`, updated `2026-04-08T17:06:17.012983+00:00`
   - Record `19472830` `coverdata.json` (`https://zenodo.org/api/records/19472830/files/coverdata.json/content`):
     - Fetch timestamp (UTC): `2026-10-18T09:41:20Z`, HTTP `200`, `8319264` bytes, sha256 `c5f7f3bc210e20c52f3b0c6f28ea48f908baf0364b296d7dee936448c1ee3330`
     - Entry `C(94,13,5)` (among `9482` entries): `size: 129337`, `low_bd: 42705`, improvements `[['129337', 'Dynamic programming construction', 'LJCR', '2026-03-02 16:50:18'], ['133359', 'Simple construction: combined (93,13,5) and  (93,12,4)', 'LJCR', '2026-03-02 07:59:27']]`
   - Record `19735294` metadata (`https://zenodo.org/api/records/19735294`, latest Zenodo version):
     - Fetch timestamp (UTC): `2026-10-18T09:40:05Z`, HTTP `200`, `5642` bytes, sha256 `8efe67191805175d3033e089594bfb50cd4935094dbf89374a404395e5afa31a`
     - Version `1.2`, publication date `2026-04-24`, updated `2026-04-24T15:59:09.825759+00:00`
   - Record `19735294` `coverdata.json` (`https://zenodo.org/api/records/19735294/files/coverdata.json/content`):
     - Fetch timestamp (UTC): `2026-10-18T09:40:54Z`, HTTP `200`, `8319503` bytes, sha256 `9e7da3710921066b10234fdc95379a18df3a7d3ae0f8a08ae188ea6bbca92f87`
     - Entry `C(94,13,5)` (among `9482` entries): `size: 129337`, `low_bd: 42705`, improvements `[['129337', 'Dynamic programming construction', 'LJCR', '2026-03-02 16:50:18'], ['133359', 'Simple construction: combined (93,13,5) and  (93,12,4)', 'LJCR', '2026-03-02 07:59:27']]`

4. **GitHub `dmgordo/LJCR` repository**
   - Directory listing (`https://api.github.com/repos/dmgordo/LJCR/contents/coverings`):
     - Fetch timestamp (UTC): `2026-10-18T09:40:06Z`, HTTP `200`, `3186` bytes, sha256 `9886e6fae328054aa13a220b8776a17063ed627196b5dd0a498ea20063f60994`
   - Raw `coverdata.json` (`https://raw.githubusercontent.com/dmgordo/LJCR/main/coverings/coverdata.json`):
     - Fetch timestamp (UTC): `2026-10-18T09:41:00Z`, HTTP `200`, `6517686` bytes, sha256 `0984bb8b4c89fe07268569b9814794e3c8852302d075f0794140f202e83d7fef`
     - Contains `8759` entries (older snapshot prior to the `2026-03-02` additions; includes `C(94,13,2)=64`, `C(94,13,3)=655`, `C(94,13,4)=8984`, and no entry for `C(94,13,5)`).

## 3. Literature, Hobbyist Repositories, Trophy Case, and Open Pull Requests (Last 24 Months)

1. **GitHub searches and hobbyist covering-design repositories**
   - Repository search (`https://api.github.com/search/repositories?q=%22covering+designs%22+pushed:%3E2024-10-18`):
     - Fetch timestamp (UTC): `2026-10-18T09:41:01Z`, HTTP `200`, sha256 `11fcb9b0662bf326277fc909f0e71e8b03b8f2d7ec92e1688342121346d088bf`
     - Returned `total_count: 6`: `TheEslabonGroup/covering-designs` (pushed `2026-09-20T22:26:45Z`, `C(28,13,4)` in `53` blocks), `gooverdian/covering-designs-finder` (`2025-05-01T17:09:21Z`), `vibemathing/problem-um-opg-762-combinatorial-covering-designs-0fa59888` (`2026-09-06T14:03:04Z`), `Meliwat/covering-hunt` (`2026-10-17T21:17:55Z`, `t=2` designs), `nickroci/fuzzy-solvers` (`2026-09-15T14:36:35Z`, `t=2` designs), and `forsing/Data-Science-16` (`2026-07-11T00:18:38Z`).
   - Direct check of `thebrockchain/covering-designs` (`https://raw.githubusercontent.com/thebrockchain/covering-designs/main/README.md`):
     - Fetch timestamp (UTC): `2026-10-18T09:41:02Z`, HTTP `200`, sha256 `171f9f5e88341cc90576de0f3016d0ed67569c54e33c1ed16ae729d49b066da5`
     - Reports only `C(28,13,4)` (`53` blocks) and `C(32,13,4)` (`95` blocks); no `v = 94` designs.
   - Direct check of `nickroci/fuzzy-solvers` (`https://raw.githubusercontent.com/nickroci/fuzzy-solvers/main/README.md`):
     - Fetch timestamp (UTC): `2026-10-18T09:43:11Z`, HTTP `200`, sha256 `12ab529e6fde9d6d28798aa9eb624c6d4e8e81334b71be2883eab70dca9a3103`
     - Reports only `t = 2` cells: `C(41,9,2)=27`, `C(56,13,2)=24`, `C(65,14,2)=28`, `C(82,19,2)=24`, `C(98,22,2)=26`.
   - Direct check of `Meliwat/covering-hunt` (`https://raw.githubusercontent.com/Meliwat/covering-hunt/master/README.md`):
     - Fetch timestamp (UTC): `2026-10-18T09:43:39Z`, HTTP `200`, sha256 `48dd81af53a60282a0ca608c19f223ffea426461b4c884ec0ff4f488e4728922`
     - Reports only `t = 2` cells: `C(41,9,2)=27`, `C(61,11,2)=39`, `C(65,14,2)=28`, `C(70,21,2)=15`, `C(75,17,2)=26`, `C(98,22,2)=26`, plus `C(56,13,2)`, `C(82,19,2)`, `C(86,20,2)`.
   - Targeted GitHub searches for `"94,13,5"`:
     - `https://api.github.com/search/repositories?q=%2294,13,5%22` (`2026-10-18T09:41:24Z`, HTTP `200`, sha256 `4af480b8ee5b87b369a76c49bd22c9a783908272ebffbe97898f8ab0f0772a5f`): `total_count: 0`
     - `https://api.github.com/search/issues?q=%2294,13,5%22` (`2026-10-18T09:41:24Z`, HTTP `200`, sha256 `c9938edecb99d754b2d039ac9eec320a94c769b6a6417921e2dcbef9e2fe01a0`): `total_count: 0`
     - `https://api.github.com/search/code?q=%2294,13,5%22` (`2026-10-18T09:41:02Z`, HTTP `401`, sha256 `b7dbd173f33b19650f61b1c528737e2037cf768d90076fdfce5d32541765e29e`; unauthenticated GitHub code search endpoint requires login).

2. **arXiv literature search (last 24 months)**
   - Query `https://export.arxiv.org/api/query?search_query=all:%22covering+design%22&sortBy=submittedDate&sortOrder=descending&max_results=50`:
     - Fetch timestamp (UTC): `2026-10-18T09:41:02Z`, HTTP `200`, sha256 `f74b966d73ae8ea6b663e58589bb9a361a4a6e4975a6d4c4376b8be308148a30`
     - Returned `50` entries (newest `2026-09-29T20:36:07Z`, spanning `2024-10` through `2026-09`, including `arXiv:2607.10978v2`, `arXiv:2603.24170v3`, `arXiv:2502.12897v1`); `0` entries mention `(94,13,5)`, `129203`, or `129337`.
   - Query `https://export.arxiv.org/api/query?search_query=all:%2294,13,5%22+OR+all:%2294,+13,+5%22&max_results=20`:
     - Fetch timestamp (UTC): `2026-10-18T09:43:40Z`, HTTP `200`, sha256 `dc0a21b0e8e3007a74d0f0c8d15c791d031cbfd59edb96af574b7acc3fb9dfd8`
     - Returned `0` entries.

3. **Repository `TROPHY_CASE.md` and open pull requests**
   - `https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md`:
     - Fetch timestamp (UTC): `2026-10-18T09:41:03Z`, HTTP `200`, sha256 `b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1`
     - Contains `0` entries for `covering-designs-record` or `C(94,13,5)`.
   - `https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100`:
     - Fetch timestamp (UTC): `2026-10-18T09:41:03Z`, HTTP `200`, sha256 `dfe003e8fd09282f2945c4e673fbfdb7db6444b9d41d3d08e2bd81239dcf33db`
     - Returned `87` open pull requests. Five open pull requests target `covering-designs-record`, all for other `(v,k,t)` cells: PR `#353` (`C(20,6,3)` at `70`), PR `#212` (`C(53,20,3)` at `34`), PR `#211` (`C(41,12,5)` at `2207`), PR `#209` (`C(85,24,3)` at `76`), and PR `#208` (`C(61,25,3)` at `27`). None involve `(94,13,5)`.

## 4. Verdict

The claimed `(94,13,5)` covering design in `claim/design_94_13_5.txt` has `b = 125184` blocks, which is above the Schonheim lower bound `L(94,13,5) = 42705` and strictly smaller than every known upper bound:
- `125184 < 129203` (live `coveringrepository.com` archive row `94 13 05 05  129203`, improvement of `4019` blocks)
- `125184 < 129337` (Zenodo LJCR v1.1 and v1.2 `coverdata.json` entry `C(94,13,5)`, improvement of `4153` blocks)
- Unclaimed in `TROPHY_CASE.md`, open pull requests, arXiv, and GitHub repositories over the last 24 months.

pass: true
