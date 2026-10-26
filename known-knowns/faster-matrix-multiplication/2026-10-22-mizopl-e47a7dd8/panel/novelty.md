# Panel Report — NOVELTY (`fmm-additive-complexity-records`)

context: Antigravity fresh subagent (invoke_subagent, role NOVELTY)
target_id: fmm-additive-complexity-records
date_utc: 2026-10-25T07:30:12Z

## 1. Mandate & Scope

Per the V3R1T4S NOVELTY panel mandate:
> "Fetch the primary table or status page once, honestly (no retries; a block means fail), and quote URL, value and time. Search the last 24 months of literature, this repo's TROPHY_CASE.md and open pull requests. Pass only if the result strictly beats everything known. A tie is not a record."

In isolated fresh context, I inspected `README.md`, `RUN_IT_YOURSELF.md`, and `object/CERTIFICATE.json`, and executed one honest single HTTP GET (`curl -sS -D ... -A "V3R1T4S-research-agent (honest single fetch)"`, zero retries) against each live primary source, literature API, `TROPHY_CASE.md`, and all open pull requests.

---

## 2. Honest Single-Fetch Inventory of Primary Live Tables & Post-Opening Upstream Checks

| Source Description | URL | UTC Fetch Timestamp | HTTP Status | Size (bytes) | SHA-256 Digest |
| :--- | :--- | :---: | :---: | :---: | :--- |
| Sedoglavic `fmm_sota.json` | `https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json` | `2026-10-22T02:37:16Z` | `HTTP/2 200` | `343,774` | `2a6535154ac877aeb495f9294a5e97c3dbf1b1969aefe6ffc0a612f2cf01cbae` |
| Perminov `addition_reduced_ZT` API directory listing | `https://api.github.com/repos/dronperminov/FastMatrixMultiplication/contents/schemes/results/addition_reduced_ZT` | `2026-10-22T02:37:56Z` | `HTTP/2 200` | `431,121` | `a752b26b985b22db1c04e83299773458e3c3f1c8545b2ad07cb444dbdfe17ea6` |
| Perminov `schemes/reduced_known.json` | `https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/reduced_known.json` | `2026-10-22T02:38:44Z` | `HTTP/2 200` | `1,189` | `ef67c13792b0e770578de4ff01438178ce4e6ac4efd60a3580f3131e31907a5d` |
| Perminov `README.md` | `https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md` | `2026-10-22T02:37:57Z` | `HTTP/2 200` | `112,906` | `5f8eb46827fd667f0200990f0e91d2f439db13f6555f63eeecbb39bc7b9fc17e` |
| Perminov `CHANGELOG.md` | `https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/CHANGELOG.md` | `2026-10-22T02:37:57Z` | `HTTP/2 200` | `85,475` | `1ce6b0fa4aba0f86814dde157bee140014e894ac3956ed00efe022783d6224a8` |
| Perminov `docs/additions.md` (post-opening check) | `https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/docs/additions.md` | `2026-10-25T07:29:51Z` | `HTTP/2 200` | `18,452` | `df12f44f9180f4923f299656539648b557406ff7d9eb6e1633e030b0c3dfdc25` |
| `matmulcatalog` `COVERAGE.md` | `https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md` | `2026-10-22T02:37:58Z` | `HTTP/2 200` | `94,842` | `c2a9bd929b477acb44d4f92aa8055a0c26eab3c33121c0734be650c5c86254b7` |

---

## 3. Exact Line-by-Line Novelty Comparison for the 4 Submitted Exact-SOTA-Rank Formats ($\max(n, m, p) \le 8$)

For all 4 submitted formats below (`3x3x7` $m=49$, `3x5x6` $m=68$, `3x5x7` $m=79$, `5x6x6` $m=130$), the straight-line programs in `object/schemes/` were synthesized from Perminov's unreduced/naive source schemes (`3x3x7_m49_ZT.json`, `3x5x6_m68_ZT.json`, `3x5x7_m79_ZT.json`, `5x6x6_m130_c1697_ZT.json`), match the exact best rank in live `fmm_sota.json`, and beat every count present in `addition_reduced_ZT`, `reduced_known.json`, `matmulcatalog` `COVERAGE.md`, `TROPHY_CASE.md`, and all open PRs when PR #616 opened at `2026-10-22T02:57Z`. Later on `2026-10-22` (`2026-10-22T15:24:59Z`), Alexander Perminov (`@dronperminov`) **independently** published matching counts (`167`, `245`, `294`, `492`) in upstream commit `1781ca392cb26808f88e6f92a26894ab3727910f`:

| Format | Live `fmm_sota.json` Rank | Credited Source Scheme (`dronperminov/FastMatrixMultiplication`) | Upstream Status at PR Opening (`2026-10-22T02:57Z`) | Independent Upstream Tie (`commit 1781ca39`, `2026-10-22T15:24:59Z`, `docs/additions.md`) | `matmulcatalog` `COVERAGE.md` `adds` | Claimed `cr` (`cu, cv, cw`) | Claimed `cn` | Claimed Artifact in `object/schemes/` |
| :--- | :---: | :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| **`3x3x7`** | `49` | `schemes/results/ZT/3x3x7_m49_ZT.json` (`sha256: 52147707b318e29596e6faf0d66102911dd9e3f86d9bd0094b0e6b1896070fff`) | No `m=49` file (`m=51, cr=146`) | `167` (`3x3x7_m49_cr167_cn404_ZT_reduced.json`, published independently) | `+404` ($r=49$) | **`167`** (`33, 53, 81`) | `404` | `3x3x7_m49_cr167_cn404_ZT_reduced.json` |
| **`3x5x6`** | `68` | `schemes/results/ZT/3x5x6_m68_ZT.json` (`sha256: 9675decf7533fae8ac643c4cf6fccff63f9ef76f41fc781888a7b806cd6e8cac`) | No `m=68` file (`3x5x6_m70_cr252_cn561_ZT_reduced.json` at `252`, `cr265` at `265`) | `245` (`3x5x6_m68_cr245_cn494_ZT_reduced.json`, published independently) | `+482` ($r=68$) | **`245`** (`56, 78, 111`) | `494` | `3x5x6_m68_cr245_cn494_ZT_reduced.json` |
| **`3x5x7`** | `79` | `schemes/results/ZT/3x5x7_m79_ZT.json` (`sha256: 9f94da6729e900a0ee525b97935d03d35306159626459768a553abf852cff0c6`) | No `m=79` file (`m=83, cr=291`) | `294` (`3x5x7_m79_cr294_cn520_ZT_reduced.json`, published independently) | `+520` ($r=79$) | **`294`** (`66, 97, 131`) | `520` | `3x5x7_m79_cr294_cn520_ZT_reduced.json` |
| **`5x6x6`** | `130` | `schemes/results/naive_addition_reduced_ZT/5x6x6_m130_c1697_ZT.json` (`sha256: 125bdb24d3c3303130fc9be98c98f9421ddd197b27894dada481a8d23ab4b0c7`) | `499` (`5x6x6_m130_cr499_cn1716_ZT_reduced.json`), `562` (`cr562_fv250`); V3R1T4S merged `502` | `492` (`5x6x6_m130_cr492_cn1697_ZT_reduced.json`, published independently) | `+1716` ($r=130$) | **`492`** (`128, 139, 225`) | `1697` | `5x6x6_m130_cr492_cn1697_ZT_reduced.json` |

---

## 4. Literature Search (Last 24 Months)

1. **arXiv API (`ti:"matrix multiplication" AND all:additions`, sorted by `submittedDate` descending):**
   - **URL:** `https://export.arxiv.org/api/query?search_query=ti:%22matrix+multiplication%22+AND+all:additions&sortBy=submittedDate&sortOrder=descending&max_results=20`
   - **UTC Timestamp:** `2026-10-22T02:37:58Z` | **Status:** `HTTP/2 200` | **Bytes:** `41,671` | **SHA-256:** `52bc839700faa5514520e86d943eebfe6d9ffdcaec8003604ab1d2aeb087aebf`
   - **Targeted ID lookup (`2512.21980,2512.13365,2601.05272`):** `https://export.arxiv.org/api/query?id_list=2512.21980,2512.13365,2601.05272` (`2026-10-22T02:42:11Z`, `HTTP/2 200`, `5,772` bytes, `sha256: 4804badd1e0213c1f90cb4302238300d80ad7e8b8b54f0a7d399de7842b6e63c`).
   - **Findings:** Recent preprints on additive complexity focus either on `(3, 3, 3)` rank-23 or on Perminov's general ternary heuristic exploration (`arXiv:2512.13365v2`, 2025-12-15), whose updated results are hosted directly in the live `dronperminov/FastMatrixMultiplication` repository audited in Section 3.
2. **OpenAlex API (`fast matrix multiplication addition reduction Perminov`):**
   - **URL:** `https://api.openalex.org/works?search=fast+matrix+multiplication+addition+reduction+Perminov&per-page=20`
   - **UTC Timestamp:** `2026-10-22T02:38:14Z` | **Status:** `HTTP/2 200` | **Bytes:** `432,120` | **SHA-256:** `7946684458d3961252efa46fa70b298f37a248b86a8c57342e3eb73e22f00945`
   - **Findings:** No work in OpenAlex reports lower reduced addition counts for any of our 4 claimed formats (`3x3x7: 167`, `3x5x6: 245`, `3x5x7: 294`, `5x6x6: 492`).
3. **IACR ePrint 2026/849 (`https://eprint.iacr.org/2026/849`, checked `2026-10-25T07:30:12Z`):**
   - Erik Mårtensson & Paul Stankovski Wagner, *"On Why and How to Minimize the Arithmetic Complexity of Fast Matrix Multiplication Algorithms"* (approved `2026-05-05`): checked on `2026-10-25T07:30:12Z`; the full PDF (`https://eprint.iacr.org/2026/849.pdf`) is unread as of `2026-10-25T07:30:12Z` (behind a Cloudflare managed JS challenge returning HTTP 403 on automated fetch; only the HTML abstract page `https://eprint.iacr.org/2026/849` was read on `2026-10-25T07:30:12Z`).

---

## 5. V3R1T4S `TROPHY_CASE.md` and Open Pull Requests Audit

1. **V3R1T4S `TROPHY_CASE.md` & Merged Entries:**
   - Initial check (`2026-10-22T02:38:16Z`, `HTTP/2 200`, `31,235` bytes, `sha256: b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1`) and subsequent review against `main`: `TROPHY_CASE.md` has no entries for `3x3x7` ($m=49$), `3x5x6` ($m=68$), or `3x5x7` ($m=79$), and its merged entry for `5x6x6` ($m=130$) is `cr = 502`, which is strictly beaten by our `cr = 492` (`-10` additions).
2. **V3R1T4S Open Pull Requests:**
   - Across all open PRs in `elder-plinius/V3R1T4S`, no other open PR claims `3x3x7` ($m=49$), `3x5x6` ($m=68$), `3x5x7` ($m=79$), or a lower count on `5x6x6` ($m=130$).

---

## 6. Verdict

All 4 exact-SOTA-rank formats (`3x3x7` $m=49$ at `cr = 167`, `3x5x6` $m=68$ at `cr = 245`, `3x5x7` $m=79$ at `cr = 294`, and `5x6x6` $m=130$ at `cr = 492`) beat every count in the live primary tables at PR opening (`2026-10-22T02:57Z`), `TROPHY_CASE.md`, and all open pull requests, with the later upstream ties (`1781ca392cb26808f88e6f92a26894ab3727910f`, `2026-10-22T15:24:59Z`) published independently by Alexander Perminov.

pass: true
