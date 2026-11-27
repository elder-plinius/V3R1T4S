# Panel Review — NOVELTY

panelist: NOVELTY skeptic (fresh context, isolated to `claim/`)
context: Antigravity fresh subagent (invoke_subagent, role NOVELTY)
target_id: `square-grid-lattice-gas-exact-counts-oeis` (partial win `p2`: OEIS `A089980` antidiagonal $d = 79$, b-file indices `n = 3160..3239`)
mandate: "Fetch the primary table or status page once, honestly (no retries; a block means fail), and quote URL, value and time. Search the last 24 months of literature, this repo's TROPHY_CASE.md and open pull requests. Pass only if the result strictly beats everything known. A tie is not a record."

---

## 1. Honest Single Fetch of Primary OEIS Table and Metadata

### 1.1 Primary B-File (`https://oeis.org/A089980/b089980.txt`)

One single `curl` GET request was executed with no retries:

- **URL**: `https://oeis.org/A089980/b089980.txt`
- **UTC Timestamp**: `2026-10-18T19:52:41Z`
- **HTTP Status**: `HTTP/2 200`
- **Byte Size**: `304,116` bytes (`3,160` non-comment data lines)
- **SHA-256**: `a28e1a8df3a08cf6881981e6288a61b0bad260be40cbd4ca58d08d53fbef2e32` (matches `claim/b089980.txt` byte-for-byte)
- **First Entry**: `0 1` (antidiagonal $d = 0$, $w = 0, m = 0$)
- **Last Published Entry**: `3159 1` (antidiagonal $d = 78$, $w = 78, m = 0$)
- **Last Published Central Peak Entry ($d = 78, w = 39, m = 39$, index `3120`, `272` decimal digits)**:
  `3120 29855612447544274159031389813027239335497014990491494036487199167155042005286230480609472592158583920411213748368073011775053878033685239323444700725664632236525923258394737964155747730125966370906864022395459136352378231301643917282836792261715266731741625623207330411607`
- **Absence of Antidiagonal $d = 79$**: Index `3160` (and all indices `3160..3239`) is absent from `b089980.txt`.

### 1.2 Primary Sequence JSON (`https://oeis.org/search?q=id:A089980&fmt=json`)

One single `curl` GET request was executed with no retries:

- **URL**: `https://oeis.org/search?q=id:A089980&fmt=json`
- **UTC Timestamp**: `2026-10-18T19:52:41Z`
- **HTTP Status**: `HTTP/2 200`
- **Byte Size**: `1,716` bytes
- **SHA-256**: `062f44191c1ec136653abe98566ebaf44b69cc8ed79882eebb0e91a983daed3b`
- **Sequence Metadata**:
  - `number`: `89980`
  - `revision`: `26`
  - `time`: `2025-07-18T09:33:37-04:00`
  - `created`: `2004-02-19T03:00:00-05:00`
  - `link`: references `/A089980/b089980.txt` (`Antidiagonals n = 0..78, flattened`), `arXiv:2505.12776`, and `arXiv:2507.04007`.
- **Verification**: No revision or link extends `A089980` beyond antidiagonal $d = 78$ (`n = 3159`).

---

## 2. Literature and Repository Search (Last 24 Months)

### 2.1 arXiv API Search

- **URL**: `https://export.arxiv.org/api/query?search_query=all:A089980+OR+all:%22hard+squares%22&sortBy=submittedDate&sortOrder=descending&max_results=25`
- **UTC Timestamp**: `2026-10-18T19:53:20Z`
- **HTTP Status**: `HTTP/2 200`
- **Byte Size**: `53,143` bytes (`25` entries returned, submission dates from `2017-04-26` to `2026-09-09`)
- **SHA-256**: `dae07951e7df302c876906e70385b3fddb89b587429b6ce0e34726c8151d4cac`
- **Findings**:
  - Exactly two preprints in the results mention `A089980`:
    1. `http://arxiv.org/abs/2507.04007v2` (*Independent Set Enumeration and Estimation of Related Constants of Grid Graphs and Their Variants*, published `2025-07-05T11:22:37Z`, updated `2025-08-08T14:55:01Z`, by Kai Liang).
    2. `http://arxiv.org/abs/2505.12776v2` (*Independent Set Enumeration in King Graphs by Tensor Network Contractions*, published `2025-05-19T07:04:14Z`, updated `2025-06-23T07:02:10Z`, by Kai Liang).
  - These two papers are the exact source of the current OEIS revision `26` (`2025-07-18T09:33:37-04:00`) and its b-file `b089980.txt` (`n = 0..3159`, antidiagonals $d = 0..78$, i.e., `79` antidiagonals in 0-based `A089980`).
  - None of the seven newer preprints from September 2025 through September 2026 (`2509.24885v1`, `2511.11905v1`, `2603.25492v2`, `2603.28609v1`, `2605.20160v1`, `2608.28332v2`, `2609.09936v1`) compute or report exact grid-graph counts for `A089980`.

### 2.2 GitHub Search API

- **Repositories Search**:
  - **URL**: `https://api.github.com/search/repositories?q=A089980`
  - **UTC Timestamp**: `2026-10-18T19:53:21Z`
  - **HTTP Status**: `HTTP/2 200`
  - **Byte Size**: `55` bytes
  - **SHA-256**: `4af480b8ee5b87b369a76c49bd22c9a783908272ebffbe97898f8ab0f0772a5f`
  - **Result**: `total_count: 0` repositories matching `A089980`.
- **Code Search**:
  - **URL**: `https://api.github.com/search/code?q=b089980+OR+A089980`
  - **UTC Timestamp**: `2026-10-18T19:53:21Z`
  - **HTTP Status**: `HTTP/2 401` (`Requires authentication` for unauthenticated code search API)
  - **Byte Size**: `120` bytes
  - **SHA-256**: `b7dbd173f33b19650f61b1c528737e2037cf768d90076fdfce5d32541765e29e`

---

## 3. V3R1T4S `TROPHY_CASE.md` and Open Pull Requests

### 3.1 `TROPHY_CASE.md`

- **URL**: `https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md`
- **UTC Timestamp**: `2026-10-18T19:53:21Z`
- **HTTP Status**: `HTTP/2 200`
- **Byte Size**: `31,235` bytes
- **SHA-256**: `b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1`
- **Findings**: `0` occurrences of `A089980`, `b089980`, or `square-grid-lattice-gas-exact-counts-oeis`.

### 3.2 Open Pull Requests (`elder-plinius/V3R1T4S`)

- **Page 1 URL**: `https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100`
  - **UTC Timestamp**: `2026-10-18T19:53:21Z`
  - **HTTP Status**: `HTTP/2 200`
  - **Byte Size**: `2,173,102` bytes (`100` open PRs, numbers `360..461`)
  - **SHA-256**: `0e93eb1f64255dc45577e4556539542e225f2f5a96dc6788a4653f2c87f06f02`
- **Page 2 URL**: `https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100&page=2`
  - **UTC Timestamp**: `2026-10-18T19:54:25Z`
  - **HTTP Status**: `HTTP/2 200`
  - **Byte Size**: `1,041,775` bytes (`54` open PRs, numbers `9..359`)
  - **SHA-256**: `7ba93e1c0dbc3b9890e34801ebc47d3f456b16d0eede02bc5b42eebbbfa5611b`
- **Findings across all `154` open PRs**:
  - PR `#366` claims `A054759(15) = 4310182149988584261406143524214457416387448` (partial `p1` of `square-grid-lattice-gas-exact-counts-oeis`, noting `A028420`, `A006506`, `A063443` as the main sequences).
  - PR `#459` claims `A054759(16)` (marked `gate PROMISING` on `A054759`).
  - PR `#383` and PR `#363` were also inspected directly in the page-1 response (`#383` is on `condorcet-domains` and `#363` is on `eaqecc-qutrit-codetables-gaps`; in addition, any prior or cross-referenced mentions of `A054759(15)` / `A006506` / `A063443` do not touch `A089980`).
  - **Zero (`0`) open pull requests** mention `A089980`, `b089980`, or antidiagonal $d = 79$ (`p2`).

---

## 4. Comparison of Claimed Result vs Published Record

- **Published Record (`b089980.txt`)**: Complete antidiagonals $d = 0..78$ (`3,160` entries `n = 0..3159`), ending at $T(78, 0) = 1$ (`n = 3159`) with central entry $T(39, 39)$ at `n = 3120` (`272` digits).
- **Claimed Extension (`claim/a089980_antidiag79.txt`, `sha256: 918a1787709ce8d30985fe62d7cf067072f66d3edf34e5c99718541f3b7f0ed6`; `claim/a089980_antidiag79.tsv`, `sha256: 8f76c40e12a0b32548660ca69e1ae2eadd060a2b04fb39737363205e740a6c8e`)**: Complete antidiagonal $d = 79$ (`80` entries `n = 3160..3239`, $T(w, 79 - w)$ for $w = 0..79$, determined by the `40` canonical widths $w = 0..39$), peaking at `n = 3199` ($w = 39, m = 40$, `279` decimal digits):
  `T(39, 40) = 254735682081189541344081503360736788844774937958504869716096214590338245178492823863429255507628678700444558564935870046594368781174025731139175661159108554557238150761113808065611962133371021250718485742976243397588856426972383225337965855119190243350002187880478598136326595377`
- **Verdict**: The claimed complete antidiagonal $d = 79$ (`n = 3160..3239`) strictly beats the live OEIS record ($d = 78$, `n = 0..3159`) and is not present in recent literature, `TROPHY_CASE.md`, or any open pull request.

pass: true
