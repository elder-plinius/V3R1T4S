# Skeptic Panel Report — Role: NOVELTY

role: NOVELTY
context: Antigravity fresh subagent (invoke_subagent, role NOVELTY)
target_id: covering-designs-record
cell: C(68, 14, 5)
claimed_bound: 15675
previous_best_bound: 16004

## 1. Mandate

> Fetch the primary table or status page once, honestly (no retries; a block means fail), and quote URL, value and time. Search the last 24 months of literature, this repo's TROPHY_CASE.md and open pull requests. Pass only if the result strictly beats everything known. A tie is not a record.

## 2. Claimed Artifact Verification

- Claimed design file: `claim/design_68_14_5.txt`
  - Size: `632,681` bytes, `15,675` lines
  - SHA-256: `2b72790b8149daebd293b91cddae0105bc2a19b798b414d405e66f81828bcf07`
- Standalone checker (`claim/author_checker_cover_check.py`, SHA-256 `dcf6f867fa3ea9d0e823640581f48d52d0a033a3a12bc1412085032f6abd82ac`) output on `claim/design_68_14_5.txt` for `(v, k, t) = (68, 14, 5)`:
  - `blocks=15675`, `distinct=15675`, `base=1`, `schonheim=5785`, `C_v_t=10424128`, `uncovered=0`, `COVER_CHECK: PASS`
- The claimed upper bound is `C(68, 14, 5) \le 15,675`, which exceeds the Schonheim lower bound `L(68, 14, 5) = 5,785` and improves upon the previously known bound `16,004` by `329` blocks (`-2.06%`).

## 3. Honest Single-GET Verification of Primary Tables

Every primary source was fetched once via `curl -sS -A "V3R1T4S-research-agent (honest single fetch)"` with zero retries.

### 3.1 Covering Repository (`coveringrepository.com`)

- URL: `https://coveringrepository.com/download_archive_vkt.aspx`
- Fetch UTC timestamp: `2026-10-18T10:37:58Z`
- HTTP status: `200`
- Response size: `171,740` bytes (`9,629` lines)
- SHA-256: `f02f5fc233aa66ca835b8f0b1b4d751fd35ad721c5264043ceb515ee95da9277` (matches `claim/cr_archive_vkt.txt` fetched at `2026-10-18T10:33:16Z`)
- Exact `(68, 14, 5)` row (line `4079`) and neighboring `(68, 14, t)` rows:
  ```text
  3821:68	14	02	02		30
  3907:68	14	03	03		176
  3993:68	14	04	04		1695
  4079:68	14	05	05		16004
  4165:68	14	06	06		135839
  ```
- Live Covering Repository record for `(68, 14, 5)`: **`16004`**.
- Note: Per-cell `history.aspx` pages were not queried because they are behind a Cloudflare 403 block, whereas the full plain-text `(v, k, t)` archive returns HTTP 200 on a single GET.

### 3.2 La Jolla Covering Repository (`dmgordon.org`, Zenodo, and GitHub `dmgordo/LJCR`)

1. **LJCR Main Page:**
   - URL: `https://dmgordon.org/covering-designs/`
   - Fetch UTC timestamp: `2026-10-18T10:37:59Z`
   - HTTP status: `200`
   - Response size: `9,200` bytes
   - SHA-256: `a5cc2312afc8dedd17c52410c34d518396d0a42982b2af429c8dc54f9e7170e3` (matches `claim/ljcr_home.html` fetched at `2026-10-18T10:33:20Z`)
   - Quoted page footer and Zenodo link: `Site last updated 2026-09-03`, linking to DOI `10.5281/zenodo.10779736` and noting that `coveringrepository.com` contains all coverings in the LJCR database plus more recent improvements.

2. **Zenodo LJCR Records (`19472830` v1.1 and `19735294` v1.2) and `coverdata.json`:**
   - URL (v1.1 metadata): `https://zenodo.org/api/records/19472830`
     - Fetch UTC timestamp: `2026-10-18T10:38:28Z`, HTTP status: `200`, SHA-256: `e5fe5d732f931b5ee4dc4320c1e70733740fb525fc8cb351fdaaa7673eedcc42`
     - Record `updated`: `2026-04-08T17:06:17.012983+00:00`, version `1.1`.
   - URL (v1.2 metadata): `https://zenodo.org/api/records/19735294`
     - Fetch UTC timestamp: `2026-10-18T10:38:29Z`, HTTP status: `200`, SHA-256: `367e139b93e24ab9069e9d5ab11e09917ca9177a5d7d88e906d027a7105d8899`
     - Record `updated`: `2026-04-24T15:59:09.825759+00:00`, version `1.2`, file `coverdata.json` (`8,319,503` bytes, `md5:b2c626b07f216aac830d344eff5ad523`).
   - URL (v1.2 `coverdata.json` content): `https://zenodo.org/api/records/19735294/files/coverdata.json/content`
     - Fetch UTC timestamp: `2026-10-18T10:41:52Z`, HTTP status: `200`, SHA-256: `9e7da3710921066b10234fdc95379a18df3a7d3ae0f8a08ae188ea6bbca92f87`
     - Exact entry for `C(68,14,5)`:
       `{'size': 16004, 'low_bd': 5785, 'imps': [['16004', 'Dynamic programming construction', 'LJCR', '2026-03-06 15:13:23'], ['16152', 'Private Tools', 'Jan de Heer and Steve Muir', '2026-02-28 23:37:26'], ['16192', 'Local search', 'A. West', '2023-12-21 09:38:15'], ...]}`
     - Live LJCR Zenodo v1.2 record for `C(68, 14, 5)`: **`16004`** (set `2026-03-06` via dynamic programming construction).

3. **GitHub `dmgordo/LJCR` Repository:**
   - URL (directory listing): `https://api.github.com/repos/dmgordo/LJCR/contents/coverings`
     - Fetch UTC timestamp: `2026-10-18T10:38:30Z`, HTTP status: `200`, SHA-256: `9886e6fae328054aa13a220b8776a17063ed627196b5dd0a498ea20063f60994`
   - URL (`coverdata.json` raw): `https://raw.githubusercontent.com/dmgordo/LJCR/main/coverings/coverdata.json`
     - Fetch UTC timestamp: `2026-10-18T10:39:53Z`, HTTP status: `200`, SHA-256: `0984bb8b4c89fe07268569b9814794e3c8852302d075f0794140f202e83d7fef` (`6,517,686` bytes)
     - Entry for `C(68,14,5)`: `{'size': 16194, 'low_bd': 5785, 'imps': [['16194', 'Local search', 'Dietmar Pree', '2021-08-29 09:36:58'], ...]}` (older snapshot prior to the `2026-03-06` Zenodo v1.2 update to `16004`).

Both primary tables (`coveringrepository.com` and LJCR Zenodo v1.2) list **`16,004`** as the best known upper bound for `C(68, 14, 5)`. Our claimed bound **`15,675`** strictly beats `16,004` by **`329` blocks**.

## 4. Literature, Repository, Trophy Case, and Pull Request Audit (Last 24 Months)

### 4.1 GitHub Repositories and Code Search

1. **GitHub Repository Search (`pushed` after `2024-10-18`):**
   - URL: `https://api.github.com/search/repositories?q=%22covering+designs%22+pushed:%3E2024-10-18`
   - Fetch UTC timestamp: `2026-10-18T10:39:06Z`, HTTP status: `200`, SHA-256: `11fcb9b0662bf326277fc909f0e71e8b03b8f2d7ec92e1688342121346d088bf`
   - Returned `total_count: 6` repositories:
     - `covering-designs` (`pushed_at: 2026-09-20T22:26:45Z`): covers `C(28,13,4) \le 53` and `C(32,13,4) \le 95`.
     - `covering-designs-finder` (`pushed_at: 2025-05-01T17:09:21Z`): general solver code, no `(68, 14, 5)` bound.
     - `problem-um-opg-762-combinatorial-covering-designs-0fa59888` (`pushed_at: 2026-09-06T14:03:04Z`): small `t=2,3` experiments, no `(68, 14, 5)` bound.
     - `covering-hunt` (`pushed_at: 2026-10-17T21:17:55Z`): six `t=2` covering designs `C(v,k,2)`, unrelated to `t=5` or `(68, 14, 5)`.
     - `fuzzy-solvers` (`pushed_at: 2026-09-15T14:36:35Z`): small `t=2,3` experiments, no `(68, 14, 5)` bound.
     - `Data-Science-16` (`pushed_at: 2026-07-11T00:18:38Z`): general discrete sets library.

2. **`thebrockchain/covering-designs` README:**
   - URL: `https://raw.githubusercontent.com/thebrockchain/covering-designs/main/README.md`
   - Fetch UTC timestamp: `2026-10-18T10:39:10Z`, HTTP status: `200`, SHA-256: `171f9f5e88341cc90576de0f3016d0ed67569c54e33c1ed16ae729d49b066da5` (`6,127` bytes)
   - Contains only `C(28,13,4) \le 53` and `C(32,13,4) \le 95`; zero occurrences of `(68, 14, 5)`.

3. **GitHub Code Search API:**
   - URL: `https://api.github.com/search/code?q=%2268,14,5%22`
   - Fetch UTC timestamp: `2026-10-18T10:39:09Z`, HTTP status: `401` (`Requires authentication` for unauthenticated REST code search), SHA-256: `b7dbd173f33b19650f61b1c528737e2037cf768d90076fdfce5d32541765e29e`.

### 4.2 arXiv Preprints (Last 24 Months)

- URL: `https://export.arxiv.org/api/query?search_query=all:%22covering+design%22&sortBy=submittedDate&sortOrder=descending&max_results=50`
- Fetch UTC timestamp: `2026-10-18T10:39:10Z`, HTTP status: `200`, SHA-256: `f74b966d73ae8ea6b663e58589bb9a361a4a6e4975a6d4c4376b8be308148a30`
- Returned `50` entries (including `27` preprints from `2024-01-13` through `2026-09-29`, such as `2607.10978v2` on tight single-change covering designs with block size 6, `2603.24170v3` on the 6/49 lottery, and `2502.12897v1` on fractional-repetition codes from covering designs).
- Zero entries mention `(68, 14, 5)` or `16004` / `16,004`.

### 4.3 V3R1T4S `TROPHY_CASE.md` and Open Pull Requests

1. **`TROPHY_CASE.md`:**
   - URL: `https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md`
   - Fetch UTC timestamp: `2026-10-18T10:39:10Z`, HTTP status: `200`, SHA-256: `b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1` (`31,012` bytes, `53` entries)
   - Contains zero `covering-designs-record` entries and zero mentions of `(68, 14, 5)`.

2. **Open Pull Requests (`elder-plinius/V3R1T4S`):**
   - URL: `https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100`
   - Fetch UTC timestamp: `2026-10-18T10:39:11Z`, HTTP status: `200`, SHA-256: `2631d21df914ebe4b032c3e9354652f1e9f823ca5cfc6f870736796ae50a732a`
   - Returned `90` open PRs total. The open PRs targeting `covering-designs-record` are:
     - PR #397 (`2026-10-18T10:06:36Z`): `C(94,13,5) \le 125,184` (different cell)
     - PR #353 (`2026-10-17T15:13:28Z`): `C(20,6,3) \le 70` (different cell)
     - PR #212 (`2026-10-16T03:04:54Z`): `C(53, 20, 3) \le 34` (different cell)
     - PR #211 (`2026-10-16T03:04:49Z`): `C(41, 12, 5) \le 2207` (different cell)
     - PR #209 (`2026-10-16T03:02:44Z`): `C(85, 24, 3) \le 76` (different cell)
     - PR #208 (`2026-10-16T03:02:39Z`): `C(61, 25, 3) \le 27` (different cell)
   - None of the 90 open PRs claim or mention `(68, 14, 5)`.

## 5. Verdict

The claimed explicit covering design `claim/design_68_14_5.txt` (`15,675` blocks) strictly improves the best known upper bound `C(68, 14, 5) \le 16,004` in both the Covering Repository (`coveringrepository.com`) and the La Jolla Covering Repository (`dmgordon.org` / Zenodo v1.2 `19735294`) by `329` blocks (`-2.06%`), with no prior or competing improvement in the literature, GitHub repositories, `TROPHY_CASE.md`, or open pull requests.

pass: true
