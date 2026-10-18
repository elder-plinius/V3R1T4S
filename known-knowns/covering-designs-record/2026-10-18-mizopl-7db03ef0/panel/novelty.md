# Panelist Report: NOVELTY — $C(40, 16, 7) \le 7,251$

role: NOVELTY
context: Antigravity fresh subagent (invoke_subagent, role NOVELTY)
target_id: covering-designs-record
cell: (v, k, t) = (40, 16, 7)
claimed_value: 7251
table_value: 7470

## Mandate

"Fetch the primary table or status page once, honestly (no retries; a block means fail), and quote URL, value and time. Search the last 24 months of literature, this repo's TROPHY_CASE.md and open pull requests. Pass only if the result strictly beats everything known. A tie is not a record."

## 1. Local Claim Artifact & Standalone Verification

Inspected `claim/CLAIM.md`, `claim/REPRODUCE.md`, and `claim/design_40_16_7.txt`:
- `claim/design_40_16_7.txt`: `sha256: 7db03ef01cd698f6764f590955f51732a64cd8a41dbe97efce69a6738d479985`, `7,251` lines (`319,951` bytes).
- `claim/author_checker_cover_check.py`: `sha256: dcf6f867fa3ea9d0e823640581f48d52d0a033a3a12bc1412085032f6abd82ac`.
- Running `python3 claim/author_checker_cover_check.py 40 16 7 claim/design_40_16_7.txt` output:
  ```
  blocks=7251
  distinct=7251
  base=1
  schonheim=1965
  C_v_t=18643560
  uncovered=0
  COVER_CHECK: PASS
  ```

## 2. Single Honest Fetch of Primary Tables

### 2.1 Covering Repository (`coveringrepository.com`)

- **URL fetched (single GET, no retries):** `https://coveringrepository.com/download_archive_vkt.aspx`
- **User-Agent:** `V3R1T4S-research-agent (honest single fetch)`
- **UTC timestamp:** `2026-10-18T17:27:33Z`
- **HTTP status:** `200`
- **Response size / lines:** `171,740` bytes, `9,629` lines
- **SHA-256 of live response:** `6d317b207c4f582d7e913c4c7d6ebd0305407fdcd2dbb6de1901adf4f13a2704` (compared against `claim/cr_archive_vkt.txt` `sha256: f02f5fc233aa66ca835b8f0b1b4d751fd35ad721c5264043ceb515ee95da9277`; three unrelated $t=3, k=9$ rows changed between the claim snapshot and this fetch, while the $(40,16,7)$ row is unchanged)
- **Exact row for $(v, k, t) = (40, 16, 7)$ (line 5135):**
  ```
  40	16	07	07		7470
  ```
- **Comparison:** Claimed upper bound $b = 7,251$ is strictly smaller than the live Covering Repository record $7,470$ by **$219$ blocks** ($-2.932\%$).

### 2.2 La Jolla Covering Repository (`dmgordon.org` & Zenodo & GitHub)

1. **LJCR status page (single GET, no retries):**
   - **URL:** `https://dmgordon.org/covering-designs/`
   - **UTC timestamp:** `2026-10-18T17:27:34Z`
   - **HTTP status:** `200`
   - **Response size:** `9,200` bytes
   - **SHA-256:** `a5cc2312afc8dedd17c52410c34d518396d0a42982b2af429c8dc54f9e7170e3` (matches `claim/ljcr_home.html` byte-for-byte)
   - **Quoted footer timestamp:** `Site last updated 2026-09-03`

2. **Zenodo LJCR database records (single GET each, no retries):**
   - **URL 1 (v1.1):** `https://zenodo.org/api/records/19472830`
     - **UTC timestamp:** `2026-10-18T17:27:48Z`
     - **HTTP status:** `200`
     - **SHA-256:** `d5305a18894dbeeffd2848032ceef4cc96d93673e74f66b521e1cb8d27756294`
     - **Metadata:** `version: 1.1`, `publication_date: 2026-04-08`, `updated: 2026-04-08T17:06:17.012983+00:00`
   - **URL 2 (v1.2, latest):** `https://zenodo.org/api/records/19735294`
     - **UTC timestamp:** `2026-10-18T17:27:48Z`
     - **HTTP status:** `200`
     - **SHA-256:** `04cc239cc221e650299123df59b34297b49eb4268de0898821ed9a4e4ade2d0e`
     - **Metadata:** `version: 1.2`, `publication_date: 2026-04-24`, `updated: 2026-04-24T15:59:09.825759+00:00`
   - **URL 3 (`coverdata.json` from Zenodo v1.2 `19735294`):** `https://zenodo.org/records/19735294/files/coverdata.json?download=1`
     - **UTC timestamp:** `2026-10-18T17:28:18Z`
     - **HTTP status:** `200`
     - **SHA-256:** `9e7da3710921066b10234fdc95379a18df3a7d3ae0f8a08ae188ea6bbca92f87` (`8,319,503` bytes, `9,482` entries)
     - **Exact entry for `C(40,16,7)`:**
       - `size`: `7470`
       - `low_bd`: `1965`
       - Most recent recorded improvements: `['7470', 'Local search', 'A. West', '2023-12-28 07:55:38']`, `['7471', 'Local search', 'Dietmar Pree', '2023-02-12 05:54:35']`.

3. **GitHub LJCR repository metadata (single GET, no retries):**
   - **URL:** `https://api.github.com/repos/dmgordo/LJCR`
   - **UTC timestamp:** `2026-10-18T17:28:17Z`
   - **HTTP status:** `200`
   - **SHA-256:** `137d7a8c7a518842822a757c662bf79bc36c2ea2ce2fb4ffe02f3b4565a2f135`
   - **Quoted timestamps:** `pushed_at: 2022-12-19T18:10:24Z`, `updated_at: 2026-04-16T03:29:20Z`

- **Comparison:** Claimed upper bound $b = 7,251$ is strictly smaller than the LJCR value $7,470$ by **$219$ blocks** ($-2.932\%$).

## 3. Literature and Repository Search (Last 24 Months: 2024-10-18 to 2026-10-18)

### 3.1 GitHub Repositories and Code Search

1. **GitHub repository search (`"covering designs"` pushed after `2024-10-18`):**
   - **URL:** `https://api.github.com/search/repositories?q=%22covering+designs%22+pushed:%3E2024-10-18`
   - **UTC timestamp:** `2026-10-18T17:28:40Z`
   - **HTTP status:** `200`
   - **SHA-256:** `11fcb9b0662bf326277fc909f0e71e8b03b8f2d7ec92e1688342121346d088bf`
   - **Results (`total_count: 6`):**
     - `covering-designs` (`pushed_at: 2026-09-20T22:26:45Z`): covers $(28,13,4) \le 53$ and $(32,13,4) \le 95$ only.
     - `covering-designs-finder` (`pushed_at: 2025-05-01T17:09:21Z`): general solver utility, no $(40,16,7)$ bound.
     - `problem-um-opg-762-combinatorial-covering-designs-0fa59888` (`pushed_at: 2026-09-06T14:03:04Z`): small $t$-covering exploration, no $(40,16,7)$ bound.
     - `covering-hunt` (`pushed_at: 2026-10-17T21:17:55Z`): six $t=2$ coverings $C(v,k,2)$ only.
     - `fuzzy-solvers` (`pushed_at: 2026-09-15T14:36:35Z`): small $t=2,3$ experiments, no $(40,16,7)$ bound.
     - `Data-Science-16` (`pushed_at: 2026-07-11T00:18:38Z`): generic data-science scripts, no $(40,16,7)$ bound.

2. **Direct inspection of `covering-designs` README:**
   - **URL:** `https://raw.githubusercontent.com/thebrockchain/covering-designs/main/README.md`
   - **UTC timestamp:** `2026-10-18T17:28:41Z`
   - **HTTP status:** `200`
   - **SHA-256:** `171f9f5e88341cc90576de0f3016d0ed67569c54e33c1ed16ae729d49b066da5` (`3,790` bytes)
   - **Findings:** Contains only $C(28,13,4) \le 53$ and $C(32,13,4) \le 95$ (Zenodo `10.5281/zenodo.21834602`). Does not mention $(40,16,7)$.

3. **GitHub code search endpoint (`"40,16,7"`):**
   - **URL:** `https://api.github.com/search/code?q=%2240,16,7%22`
   - **UTC timestamp:** `2026-10-18T17:28:41Z`
   - **HTTP status:** `401` (`Requires authentication` on unauthenticated REST `/search/code`; `sha256: b7dbd173f33b19650f61b1c528737e2037cf768d90076fdfce5d32541765e29e`). All recently pushed covering-design repositories from `/search/repositories` were inspected directly above.

### 3.2 arXiv Preprints (Last 24 Months)

- **URL:** `https://export.arxiv.org/api/query?search_query=all:%22covering+design%22&sortBy=submittedDate&sortOrder=descending&max_results=50`
- **UTC timestamp:** `2026-10-18T17:28:41Z`
- **HTTP status:** `200`
- **SHA-256:** `fe81e00882c30275d002921f5835434353199eff8eb97980b2250e596881f2b8`
- **Findings:** `50` entries returned (`21` submitted in the last 24 months since `2024-10-18`, most recently `2609.38514v1` on `2026-09-29T20:36:07Z`, `2607.10978v2` on `2026-07-13T00:56:00Z` on single-change covering designs with block size $6$, `2603.24170v3` on `2026-03-25T10:37:37Z` on $6/49$ lottery designs, and `2502.12897v1` on `2025-02-18T14:34:02Z` on fractional-repetition codes from covering designs). Zero papers mention $(40, 16, 7)$ or improve $C(40, 16, 7)$.

### 3.3 Repository `TROPHY_CASE.md` and Open Pull Requests

1. **`TROPHY_CASE.md` (single GET, no retries):**
   - **URL:** `https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md`
   - **UTC timestamp:** `2026-10-18T17:28:42Z`
   - **HTTP status:** `200`
   - **SHA-256:** `b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1`
   - **Findings:** Zero entries for `covering-designs-record` or $(40, 16, 7)$.

2. **Open Pull Requests (single GET, no retries):**
   - **URL:** `https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100`
   - **UTC timestamp:** `2026-10-18T17:28:42Z`
   - **HTTP status:** `200`
   - **SHA-256:** `dddcd21e1f0d20d39662e71e8c8f4ba01af722697b9d95ffc75a9c67abb7d543`
   - **Findings:** Among the `100` open PRs returned, four target `covering-designs-record`:
     - PR #353: $C(20, 6, 3) \le 70$ (beats $71$)
     - PR #397: $C(94, 13, 5) \le 125,184$ (beats CR $129,203$, LJCR $129,337$)
     - PR #398: $C(68, 14, 5) \le 15,675$ (beats CR $16,004$, LJCR $16,004$)
     - PR #407: $C(57, 14, 3) \le 108$ (beats $109$)
     - In addition, PR #393 updates bank live values as of `2026-10-18`.
     - **None** of the open pull requests touch cell $(40, 16, 7)$.

## 4. Verdict

The claimed $(40, 16, 7)$ covering design with $b = 7,251$ blocks strictly beats the best known bound of $7,470$ across the live Covering Repository (`7470`), the La Jolla Covering Repository (`7470`), the last 24 months of GitHub and arXiv literature, `TROPHY_CASE.md`, and all open pull requests by **$219$ blocks** ($-2.932\%$).

pass: true
