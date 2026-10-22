# Panel Report — NOVELTY (`fmm-additive-complexity-records`)

context: Antigravity fresh subagent (invoke_subagent, role NOVELTY)
target_id: fmm-additive-complexity-records
date_utc: 2026-10-22T02:43:00Z

## 1. Mandate & Scope

Per the V3R1T4S NOVELTY panel mandate:
> "Fetch the primary table or status page once, honestly (no retries; a block means fail), and quote URL, value and time. Search the last 24 months of literature, this repo's TROPHY_CASE.md and open pull requests. Pass only if the result strictly beats everything known. A tie is not a record."

In isolated fresh context, I inspected `claim/CLAIM.md`, `claim/REPRODUCE.md`, and `claim/CERTIFICATE.json`, and executed one honest single HTTP GET (`curl -sS -D ... -A "V3R1T4S-research-agent (honest single fetch)"`, zero retries) against each live primary source, literature API, `TROPHY_CASE.md`, and all open pull requests.

---

## 2. Honest Single-Fetch Inventory of Primary Live Tables

| Source Description | URL | UTC Fetch Timestamp | HTTP Status | Size (bytes) | SHA-256 Digest |
| :--- | :--- | :---: | :---: | :---: | :--- |
| Sedoglavic `fmm_sota.json` | `https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json` | `2026-10-22T02:37:16Z` | `HTTP/2 200` | `343,774` | `2a6535154ac877aeb495f9294a5e97c3dbf1b1969aefe6ffc0a612f2cf01cbae` |
| Perminov `addition_reduced_ZT` API directory listing | `https://api.github.com/repos/dronperminov/FastMatrixMultiplication/contents/schemes/results/addition_reduced_ZT` | `2026-10-22T02:37:56Z` | `HTTP/2 200` | `431,121` | `a752b26b985b22db1c04e83299773458e3c3f1c8545b2ad07cb444dbdfe17ea6` |
| Perminov `schemes/reduced_known.json` | `https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/reduced_known.json` | `2026-10-22T02:38:44Z` | `HTTP/2 200` | `1,189` | `ef67c13792b0e770578de4ff01438178ce4e6ac4efd60a3580f3131e31907a5d` |
| Perminov `README.md` | `https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md` | `2026-10-22T02:37:57Z` | `HTTP/2 200` | `112,906` | `5f8eb46827fd667f0200990f0e91d2f439db13f6555f63eeecbb39bc7b9fc17e` |
| Perminov `CHANGELOG.md` | `https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/CHANGELOG.md` | `2026-10-22T02:37:57Z` | `HTTP/2 200` | `85,475` | `1ce6b0fa4aba0f86814dde157bee140014e894ac3956ed00efe022783d6224a8` |
| `matmulcatalog` `COVERAGE.md` | `https://raw.githubusercontent.com/solven-eu/matmulcatalog/master/generated/COVERAGE.md` | `2026-10-22T02:37:58Z` | `HTTP/2 200` | `94,842` | `c2a9bd929b477acb44d4f92aa8055a0c26eab3c33121c0734be650c5c86254b7` |

*(Note: an initial path check at `.../schemes/results/addition_reduced_ZT/reduced_known.json` at `2026-10-22T02:37:57Z` returned `HTTP/2 404` (`14` bytes, `sha256: d5558cd419c8d46bdc958064cb97f963d1ea793866414c025906ec15033512ed`) because `reduced_known.json` resides at `schemes/reduced_known.json` in Perminov's repository, fetched once at `2026-10-22T02:38:44Z` with `HTTP/2 200`.)*

---

## 3. Exact Line-by-Line Novelty Comparison Against All Primary Sources

### 3.1 Nine Exact-SOTA-Rank Formats ($\max(n, m, p) \le 8$)

For all 9 formats below, the claimed straight-line programs in `claim/schemes/` match the exact best rank in live `fmm_sota.json` and achieve a reduced addition count `cr` strictly below the minimum `cr` across all files for that format and rank in live `addition_reduced_ZT`, `reduced_known.json`, `README.md`, `CHANGELOG.md`, and `matmulcatalog` `COVERAGE.md`:

| Format | Live `fmm_sota.json` Rank | Live `addition_reduced_ZT` Files (All Variants) | Live Min `cr` | `reduced_known.json` | `matmulcatalog` `COVERAGE.md` `adds` | Claimed `cr` (`cu, cv, cw`) | Claimed `cn` | Strict Margin $\Delta\text{cr}$ | Claimed Artifact in `claim/schemes/` |
| :--- | :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **`2x4x7`** | `45` | `2x4x7_m45_cr168_cn308_ZT_reduced.json` (`168`), `2x4x7_m45_cr174_cn308_ZT_reduced.json` (`174`) | `168` | — | `+308` ($r=45$) | **`157`** (`26, 58, 73`) | `345` | **`-11`** (`-6.55%`) | `2x4x7_m45_cr157_cn345_ZT_reduced.json` |
| **`2x4x7`** (var. 2) | `45` | same (`168`, `174`) | `168` | — | `+308` ($r=45$) | **`164`** (`27, 64, 73`) | `285` | **`-4`** (`-2.38%`) | `2x4x7_m45_cr164_cn285_ZT_reduced.json` |
| **`2x5x5`** | `40` | `2x5x5_m40_cr147_cn283_ZT_reduced.json` (`147`), `2x5x5_m40_cr153_cn283_ZT_reduced.json` (`153`) | `147` | `Z: 313, Z2: 218` | `+256` ($r=40$) | **`145`** (`28, 58, 59`) | `273` | **`-2`** (`-1.36%`) | `2x5x5_m40_cr145_cn273_ZT_reduced.json` |
| **`4x5x8`** | `118` | `4x5x8_m118_cr466_cn1521_ZT_reduced.json` (`466`), `4x5x8_m118_cr513_fv249_cn1521_ZT_reduced.json` (`513`) | `466` | — | `+1521` ($r=118$) | **`447`** (`96, 141, 210`) | `1463` | **`-19`** (`-4.08%`) | `4x5x8_m118_cr447_cn1463_ZT_reduced.json` |
| **`4x6x7`** | `123` | `4x6x7_m123_cr468_cn1586_ZT_reduced.json` (`468`), `4x6x7_m123_cr517_cn1586_ZT_reduced.json` (`517`) | `468` | — | `+1586` ($r=123$) | **`464`** (`112, 138, 214`) | `1562` | **`-4`** (`-0.85%`) | `4x6x7_m123_cr464_cn1562_ZT_reduced.json` |
| **`5x5x6`** | `110` | `5x5x6_m110_cr411_cn1215_ZT_reduced.json` (`411`), `5x5x6_m110_cr460_fv204_cn1215_ZT_reduced.json` (`460`) | `411` | — | `+1215` ($r=110$) | **`406`** (`105, 110, 191`) | `1192` | **`-5`** (`-1.22%`) | `5x5x6_m110_cr406_cn1192_ZT_reduced.json` |
| **`5x5x8`** | `144` | `5x5x8_m144_cr555_cn1924_ZT_reduced.json` (`555`), `5x5x8_m144_cr620_fv281_cn1924_ZT_reduced.json` (`620`) | `555` | — | `+1908` ($r=144$) | **`548`** (`130, 156, 262`) | `1872` | **`-7`** (`-1.26%`) | `5x5x8_m144_cr548_cn1872_ZT_reduced.json` |
| **`5x6x6`** | `130` | `5x6x6_m130_cr499_cn1716_ZT_reduced.json` (`499`), `5x6x6_m130_cr562_fv250_cn1716_ZT_reduced.json` (`562`) | `499` | — | `+1716` ($r=130$) | **`492`** (`128, 139, 225`) | `1697` | **`-7`** (`-1.40%`) | `5x6x6_m130_cr492_cn1697_ZT_reduced.json` |
| **`5x6x7`** | `150` | `5x6x7_m150_cr577_cn2039_ZT_reduced.json` (`577`), `5x6x7_m150_cr664_fv310_cn2039_ZT_reduced.json` (`664`) | `577` | — | `+2039` ($r=150$) | **`573`** (`143, 165, 265`) | `1994` | **`-4`** (`-0.69%`) | `5x6x7_m150_cr573_cn1994_ZT_reduced.json` |
| **`5x6x7`** (var. 2) | `150` | same (`577`, `664`) | `577` | — | `+2039` ($r=150$) | **`576`** (`144, 168, 264`) | `2039` | **`-1`** (`-0.17%`) | `5x6x7_m150_cr576_cn2039_ZT_reduced.json` |
| **`5x7x7`** | `176` | `5x7x7_m176_cr694_cn2605_ZT_reduced.json` (`694`), `5x7x7_m176_cr788_fv371_cn2605_ZT_reduced.json` (`788`) | `694` | — | `+2745` ($r=176$) | **`680`** (`170, 197, 313`) | `2535` | **`-14`** (`-2.02%`) | `5x7x7_m176_cr680_cn2535_ZT_reduced.json` |

### 3.2 Two $\mathbb{Z}_T$-Best Formats (Where `fmm_sota.json` Rank Uses Non-Ternary $\mathbb{Q}$ Coefficients)

- **`4x4x8` ($r = 96$ in $\mathbb{Z}_T/\mathbb{Z}$, while `fmm_sota.json` rank `95` is over $\mathbb{Q}$ per Perminov's `README.md` and `CHANGELOG.md`):**
  - Live `addition_reduced_ZT` files: `4x4x8_m96_cr339_cn973_ZT_reduced.json` (`cr_len = 339`, true `cr_val = 340` due to a non-unit coefficient `2`) and `4x4x8_m96_cr377_fv171_cn973_ZT_reduced.json` (`377`); `matmulcatalog` `COVERAGE.md`: `+1027` adds ($r=96$).
  - Claimed: `claim/schemes/4x4x8_m96_cr338_cn962_ZT_reduced.json` with **`cr = 338`** (`cu = 73, cv = 101, cw = 164`, strictly unit coefficients) — strictly beating `339` by **`-1` (`cr_len`) / `-2` (`cr_val`) additions**.
- **`3x3x6` ($r = 43$ in `addition_reduced_ZT`, while `fmm_sota.json` rank `40` is over $\mathbb{Q}$):**
  - Live `addition_reduced_ZT` files: `3x3x6_m43_cr153_cn284_ZT_reduced.json` (`153`) and `3x3x6_m43_cr160_cn284_ZT_reduced.json` (`160`).
  - Claimed: `claim/schemes/3x3x6_m43_cr152_cn286_ZT_reduced.json` with **`cr = 152`** (`cu = 32, cv = 46, cw = 74`) — strictly beating `153` by **`-1` addition**.

### 3.3 Twenty-One Newly Addition-Reduced Exact-SOTA-Rank $\mathbb{Z}_T$ Formats

The live `addition_reduced_ZT` directory listing confirms that for all 21 formats below, Perminov's `addition_reduced_ZT` directory currently contains only older higher-rank schemes (`live_min_m > sota_rank`), whereas `claim/schemes/` provides the first addition-reduced ternary SLPs at the exact `fmm_sota.json` rank (and for 6 of them — `2x6x6` (`m=56, cr=221` vs live `m=57, cr=224` and `reduced_known.json` `Z=419, Z2=327`), `3x5x6` (`m=68, cr=245` vs live `m=70, cr=252`), `3x6x8` (`m=108, cr=381` vs live `m=113, cr=411`), `4x7x8` (`m=161, cr=625` vs live `m=164, cr=646`), `4x8x8` (`m=180, cr=734` vs live `m=182, cr=746`), and `5x7x8` (`m=204, cr=835` vs live `m=206, cr=837`) — simultaneously achieves both lower rank and strictly lower `cr` than the live `addition_reduced_ZT` file).

---

## 4. Literature Search (Last 24 Months)

1. **arXiv API (`ti:"matrix multiplication" AND all:additions`, sorted by `submittedDate` descending):**
   - **URL:** `https://export.arxiv.org/api/query?search_query=ti:%22matrix+multiplication%22+AND+all:additions&sortBy=submittedDate&sortOrder=descending&max_results=20`
   - **UTC Timestamp:** `2026-10-22T02:37:58Z` | **Status:** `HTTP/2 200` | **Bytes:** `41,671` | **SHA-256:** `52bc839700faa5514520e86d943eebfe6d9ffdcaec8003604ab1d2aeb087aebf`
   - **Targeted ID lookup (`2512.21980,2512.13365,2601.05272`):** `https://export.arxiv.org/api/query?id_list=2512.21980,2512.13365,2601.05272` (`2026-10-22T02:42:11Z`, `HTTP/2 200`, `5,772` bytes, `sha256: 4804badd1e0213c1f90cb4302238300d80ad7e8b8b54f0a7d399de7842b6e63c`).
   - **Findings:** Recent preprints on additive complexity focus either on `(3, 3, 3)` rank-23 (`arXiv:2512.21980` at 58 additions, `arXiv:2601.05272` at 59 total ops / 36 additions, `arXiv:2604.27645` at 56 additions, `arXiv:2607.28676` and `arXiv:2610.27451` at 55 additions, `arXiv:2609.06588` at 52 additions, `arXiv:2609.32388` at 51 additions in alternative basis) or on Perminov's general ternary heuristic exploration (`arXiv:2512.13365v2`, 2025-12-15), whose updated results are hosted directly in the live `dronperminov/FastMatrixMultiplication` repository audited in Section 3. None of these papers reports reduced addition counts below our claimed values on any of our 9 exact-SOTA formats (`2x4x7: 157`, `2x5x5: 145`, `4x5x8: 447`, `4x6x7: 464`, `5x5x6: 406`, `5x5x8: 548`, `5x6x6: 492`, `5x6x7: 573`, `5x7x7: 680`), 2 $\mathbb{Z}_T$-best formats (`3x3x6: 152`, `4x4x8: 338`), or 21 newly reduced SOTA-rank $\mathbb{Z}_T$ formats.

2. **OpenAlex API (`fast matrix multiplication addition reduction Perminov`):**
   - **URL:** `https://api.openalex.org/works?search=fast+matrix+multiplication+addition+reduction+Perminov&per-page=20`
   - **UTC Timestamp:** `2026-10-22T02:38:14Z` | **Status:** `HTTP/2 200` | **Bytes:** `432,120` | **SHA-256:** `7946684458d3961252efa46fa70b298f37a248b86a8c57342e3eb73e22f00945`
   - **Findings:** Top hits are `W4417457313` (`doi:10.48550/arxiv.2512.13365`, Perminov 2025), `W7133488919` (`doi:10.48550/arxiv.2603.02398`,Perminov 2026 on flip-graph rank search), and `(3, 3, 3)` rank-23 papers (`W7212002542`, `W7214731464`, `W7213699546`). No work in OpenAlex reports lower reduced addition counts for any of our claimed formats.

---

## 5. V3R1T4S `TROPHY_CASE.md` and Open Pull Requests Audit

1. **V3R1T4S `TROPHY_CASE.md`:**
   - **URL:** `https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md`
   - **UTC Timestamp:** `2026-10-22T02:38:16Z` | **Status:** `HTTP/2 200` | **Bytes:** `31,235` | **SHA-256:** `b946f68eb0a6473dd2224065a5390235a535d3282da24669f6724a1472171a1` (exact shell `shasum -a 256`: `b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1`)
   - **Findings:** `TROPHY_CASE.md` contains zero entries for `fmm-additive-complexity-records` (rows 44–48 are rational rank improvements over $\mathbb{Q}$ for large formats `(14, 15, 15)`, `(13, 14, 14)`, `(15, 16, 16)`, `(14, 14, 15)`, and `(13, 14, 15)`).

2. **V3R1T4S Open Pull Requests (all 297 open PRs across pages 1–4):**
   - **Page 1:** `https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100` (`2026-10-22T02:38:16Z`, `HTTP/2 200`, `2,122,190` bytes, `sha256: 87ea507187a372f78c226bb4fcc17830b51cd31cbc1dde01707973781248f188`, `100` PRs).
   - **Page 2:** `https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100&page=2` (`2026-10-22T02:42:10Z`, `HTTP/2 200`, `2,082,141` bytes, `sha256: 27f629bbc5fe53a0db36fd6d0c279e7bd36d2806a9b4908515b81fdd6274e415`, `100` PRs).
   - **Page 3:** `https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100&page=3` (`2026-10-22T02:42:50Z`, `HTTP/2 200`, `2,128,291` bytes, `sha256: 6b6a39fb287499e92406df763bdd3336a6d1589c34990f88411c7a2c7af54bd0`, `97` PRs).
   - **Page 4:** `https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100&page=4` (`2026-10-22T02:42:51Z`, `HTTP/2 200`, `2` bytes `[]`, `sha256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`, `0` PRs).
   - **Findings across all 297 open PRs:**
     - Rank-upgrade PRs (`#356`, `#402`, `#408`–`#415`, `#417`–`#424`, `#432`, `#615`) target `fmm-ternary-integer-ring-upgrade` on dimensions $\max(n, m, p) \ge 12$, completely disjoint from `fmm-additive-complexity-records`.
     - Existing open PRs on `fmm-additive-complexity-records` or fixed-rank circuits are:
       - `PR #357` (`4x5x5` rank 76 at `280` additions), `PR #330` (`2x5x6` rank 47 at `177` additions), `PR #218` (`4x5x6` rank 90 at `348` additions), `PR #205` (`5x5x5` rank 93 at `332` additions): none of these 4 formats is among our 9 claimed exact-SOTA-rank winners or 2 $\mathbb{Z}_T$-best winners.
       - `PR #465` (dated 2026-10-14 draft of 8 circuits): includes `4x5x8` ($r=118$) at `486` additions (already overtaken by Perminov live `466`, and strictly beaten by our **`447`** by **`-39` additions**) and `2x5x5` ($r=40$) at `148` additions (overtaken by Perminov live `147`, and strictly beaten by our **`145`** by **`-3` additions**).
       - `PR #313` (`2x4x7` rank 45 at `161` additions) and `PR #229` (`2x4x7` rank 45 at `164` additions): our primary `2x4x7` ($r=45$) scheme `claim/schemes/2x4x7_m45_cr157_cn345_ZT_reduced.json` achieves **`157` additions**, strictly beating `PR #313` (`161`) by **`-4` additions**, `PR #229` (`164`) by **`-7` additions**, and Perminov's live `168` by **`-11` additions**.
       - None of our other 6 exact-SOTA-rank winning formats (`4x6x7` at `464`, `5x5x6` at `406`, `5x5x8` at `548`, `5x6x6` at `492`, `5x6x7` at `573`, `5x7x7` at `680`), nor our 2 $\mathbb{Z}_T$-best formats (`3x3x6` at `152`, `4x4x8` at `338`), nor any of our 21 newly addition-reduced SOTA-rank $\mathbb{Z}_T$ formats has any open PR in the repository.

---

## 6. Verdict

All 9 exact-SOTA-rank formats (`2x4x7` at `cr = 157`, `2x5x5` at `cr = 145`, `4x5x8` at `cr = 447`, `4x6x7` at `cr = 464`, `5x5x6` at `cr = 406`, `5x5x8` at `cr = 548`, `5x6x6` at `cr = 492`, `5x6x7` at `cr = 573`, and `5x7x7` at `cr = 680`), both $\mathbb{Z}_T$-best formats (`3x3x6` at `cr = 152` and `4x4x8` at `cr = 338`), and all 21 newly addition-reduced SOTA-rank $\mathbb{Z}_T$ formats strictly beat every known value in the live primary tables, recent literature, `TROPHY_CASE.md`, and all 297 open pull requests.

pass: true
