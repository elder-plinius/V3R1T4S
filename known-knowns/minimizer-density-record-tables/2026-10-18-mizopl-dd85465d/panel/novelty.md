# NOVELTY Panelist Report — `minimizer-density-record-tables` `(w = 12, k = 3)`

context: Antigravity fresh subagent (invoke_subagent, role NOVELTY)

## 1. Claim Summary & Witness Verification

Per `claim/CLAIM.md` and `claim/REPRODUCE.md`, the claim submits an explicit binary-projected DNA minimizer order for `(w = 12, k = 3)` over the $2^3 = 8$ binary 3-mers `000..111` (`0..7`):

- **Rank vector:** `[4, 7, 1, 0, 6, 5, 2, 3]`
- **Witness files in `claim/`:**
  - `claim/w12_k3_improved.gm` (`72` bytes, `sha256: dd85465d87f23d688778ff35175ed19e4c9f00e71cad28b535d7a9d73294f302`, binary `.gm` format with `uint64_t` length prefix `8` followed by `[4, 7, 1, 0, 6, 5, 2, 3]`)
  - `claim/w12_k3_improved.csv` (`59` bytes, `sha256: 24790fb381b985fe053ea4d82ae225412815e1a2df754a55fe5a53448ab7b55a`)
- **Claimed exact expected DNA density (`prob_gc_dna` and 4-ary transfer-matrix DP over all $4^{15} = 1,073,741,824$ DNA windows of length $w + k = 15$):**
  $$\frac{146,639,789}{2^{30}} \approx 0.1365689458 \quad (\text{density factor } (w+1) \cdot d = 1.7753962951)$$
- **Independent execution of `claim/author_checker_minimizer_check.py`:**
  - `Published w12_k3.gm (prob_gc_dna)        : 149082035 / 2^30 = 0.1388434647`
  - `Improved  w12_k3_improved.gm (prob_gc_dna): 146639789 / 2^30 = 0.1365689458`
  - `Improved  w12_k3_improved.gm (4-ary DP)   : 146639789 / 2^30 = 0.1365689458`
  - `Smallest published value: 0.1383894480 (angle-based)`
  - `Relative reduction vs best: -1.315492% (required at least 0.500000%)`
  - `Empirical Check (N=1,000,000, seed=0): Published 0.138838 vs Improved 0.136709 (-1.5334%)`

---

## 2. Live Single-Fetch Audit of Primary Tables & Precomputed Minimizers

Each upstream resource was fetched **once** via `curl -sS -A "V3R1T4S-research-agent (honest single fetch)"` with zero retries.

### 2.1 Primary Expected-Density Table (`k_extension_k16_w12.csv`)
- **URL:** `https://raw.githubusercontent.com/OrensteinLab/10-minimizers/main/density-measurement-and-plots/GM%20paper%20densities/k_extension_k16_w12.csv`
- **UTC Timestamp:** `2026-10-18T17:27:39Z`
- **HTTP Status:** `200`
- **Size & SHA256:** `1644` bytes, `sha256: 88c4f8fcd0ea6d4308f4e1fc716bb901ea78d3c6112b7e70d4af42bb631bf2fa` (identical to `claim/k_extension_k16_w12.csv`)
- **All Values in Column `3` (`w = 12, k = 3`):**

| Method (`k_extension_k16_w12.csv`) | Column `3` Value | Claimed Density (`0.1365689458`) | Relative Change |
| :--- | :--- | :--- | :--- |
| `angle-based` | `0.138389448` | `0.1365689458` | **`-1.315492%`** |
| `GreedyMini` | `0.138843` | `0.1365689458` | **`-1.637860%`** |
| `decycling` | `0.150863` | `0.1365689458` | **`-9.474857%`** |
| `double decycling` | `0.150863` | `0.1365689458` | **`-9.474857%`** |
| `miniception` | *(empty)* | `0.1365689458` | N/A |
| `mod-minimizer` | `0.222468` | `0.1365689458` | **`-38.611869%`** |
| `open-close-syncmer` | *(empty)* | `0.1365689458` | N/A |

### 2.2 Precomputed Minimizer (`w12_k3.gm`)
- **URL:** `https://raw.githubusercontent.com/OrensteinLab/10-minimizers/main/density-measurement-and-plots/GM/w12_k3.gm`
- **UTC Timestamp:** `2026-10-18T17:27:39Z`
- **HTTP Status:** `200`
- **Size & SHA256:** `72` bytes, `sha256: c592519b57ad8104860b7e1559b28c2d37ef329db82298b151a65e056ce27f1d` (identical to `claim/published_w12_k3.gm`)
- **Decoded Rank Vector:** length prefix `8`, ranks `[8, 2, 8, 8, 0, 4, 1, 3]`
- **Exact Expected DNA Density (`prob_gc_dna`):** `149,082,035 / 2^30 = 0.1388434647` (relative reduction of `claim/w12_k3_improved.gm` vs `w12_k3.gm`: **`-1.638189%`**, or `-2,442,246` gamechanger windows out of $4^{15}$).

### 2.3 Upstream Repository Commit Histories
- **`OrensteinLab/10-minimizers` Commits:**
  - **URL:** `https://api.github.com/repos/OrensteinLab/10-minimizers/commits?per_page=5`
  - **UTC Timestamp:** `2026-10-18T17:27:40Z` | **HTTP Status:** `200`
  - Latest 5 commits:
    1. `916daebd399d15d061e2fd437326aee5cf0e7292` (`2026-06-29T16:57:18Z`): `"updated files"`
    2. `e6b3058ae9c19b9bc21f7b75b3cdca3a56cc1348` (`2026-05-08T21:05:51Z`): `"update for WABI"`
    3. `441bc52b6dcfb00a3b07f14ed8b14214cb9f6f9f` (`2026-03-23T02:32:23Z`): `"Create random10order.ipynb"`
    4. `af5c57021be7b49e011a4c4dde48bd4a3387b3b9` (`2026-03-23T02:26:10Z`): `"Add description for random10order.ipynb"`
    5. `7178085da0ddb75a8e69ec23dc0458970bb47ac0` (`2026-03-23T02:25:18Z`): `"Update README.md"`
- **`OrensteinLab/GreedyMini` Commits:**
  - **URL:** `https://api.github.com/repos/OrensteinLab/GreedyMini/commits?per_page=5`
  - **UTC Timestamp:** `2026-10-18T17:27:40Z` | **HTTP Status:** `200`
  - Latest 5 commits:
    1. `a67eb90dc278ea78111a76d5813cf2ac7662b0ae` (`2026-03-12T19:04:25Z`): `"added 2 more orders to examples"`
    2. `08c9b8713e1242195045ef7ddd9e24abefb0de2b` (`2025-03-28T13:46:58Z`): `"Merge branch 'main' of https://github.com/OrensteinLab/GreedyMini"`
    3. `7a1d5c867668fe79dec0e2cae189ee43196e5f8f` (`2025-03-28T13:46:55Z`): `"updated plots for ISMB"`
    4. `ee5a963a2697603cc11eced1d71827fa493e987c` (`2025-01-28T00:18:12Z`): `"Update README.md"`
    5. `e96766ec5b79a41d935c83afc6f2b6f2168b590b` (`2025-01-27T16:51:05Z`): `"Update README.md"`

---

## 3. Literature, Code, `TROPHY_CASE.md`, and Open PR Audit (Last 24 Months)

### 3.1 arXiv Literature Search
- **URL:** `https://export.arxiv.org/api/query?search_query=all:%22GreedyMini%22+OR+all:%2210-minimizers%22+OR+all:%22minimizer+density%22&sortBy=submittedDate&sortOrder=descending&max_results=25`
- **UTC Timestamp:** `2026-10-18T17:27:53Z` | **HTTP Status:** `200`
- **Findings:** 25 preprints returned. The only computational-biology minimizer density paper in the 24-month window is `2506.05277v1` (`2025-06-05T17:33:00Z`, *"On Minimizers of Minimum Density"*), which computes minimum-density minimizers on pure $\sigma$-ary alphabets for $(\sigma, k) \in \{(2,2), (2,3), (2,4), (2,5), (4,2)\}$ and does not give a DNA ($\sigma = 4$) minimizer order for $k = 3$ or a binary-projected DNA order under `prob_gc_dna` for `(w = 12, k = 3)`. No preprint reports a DNA density for `(w = 12, k = 3)` below `0.138389448`.

### 3.2 GitHub Repository & Code Search
- **Repository Search URL:** `https://api.github.com/search/repositories?q=GreedyMini+OR+10-minimizers`
  - **UTC Timestamp:** `2026-10-18T17:27:54Z` | **HTTP Status:** `200`
  - **Findings:** `total_count: 193`. The only relevant repositories are `OrensteinLab/10-minimizers` (`pushed_at: 2026-06-29T16:57:20Z`) and `OrensteinLab/GreedyMini` (`pushed_at: 2026-03-12T19:04:27Z`); no forks or third-party repositories contain improved `(w = 12, k = 3)` tables or `.gm` files.
- **Code Search URL:** `https://api.github.com/search/code?q=w12_k3.gm`
  - **UTC Timestamp:** `2026-10-18T17:27:55Z` | **HTTP Status:** `401` (`Requires authentication` on unauthenticated GitHub REST code search endpoint; recorded honestly without retry).

### 3.3 `TROPHY_CASE.md` & Open Pull Requests
- **`TROPHY_CASE.md` URL:** `https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md`
  - **UTC Timestamp:** `2026-10-18T17:27:55Z` | **HTTP Status:** `200`
  - **SHA256:** `b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1` (`100` lines)
  - **Findings:** Zero entries for `minimizer-density-record-tables`, `GreedyMini`, `10-minimizers`, or `(w = 12, k = 3)`.
- **Open Pull Requests URL:** `https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100`
  - **UTC Timestamp:** `2026-10-18T17:27:55Z` | **HTTP Status:** `200`
  - **SHA256:** `dddcd21e1f0d20d39662e71e8c8f4ba01af722697b9d95ffc75a9c67abb7d543` (`100` open PRs)
  - **Findings:** Only one open pull request references `minimizer-density-record-tables`: PR #425 (created `2026-10-18T16:33:52Z`, titled `[claim] minimizer-density-record-tables: (w=12, k=4) DNA density 0.1336292920 vs 0.1360458389 (-1.7763% rel)`), which targets `(w = 12, k = 4)` (`16` binary 4-mers), distinct from `(w = 12, k = 3)` (`8` binary 3-mers). Zero open pull requests claim `(w = 12, k = 3)`.

---

## 4. Verdict

The claimed binary-projected DNA minimizer order `[4, 7, 1, 0, 6, 5, 2, 3]` (`claim/w12_k3_improved.gm`) achieves an exact expected DNA density of `146,639,789 / 2^30 = 0.1365689458` at `(w = 12, k = 3)`, strictly beating the smallest published value `0.138389448` (`angle-based` in `k_extension_k16_w12.csv`) by **`-1.315492%` relative** (`2.63x` the required `0.5%` relative threshold) and beating the precomputed `w12_k3.gm` (`0.1388434647`) by **`-1.638189%` relative**, with identical storage cost (`72` bytes on disk / `24` bits of rank table storage) and zero prior claims in the literature, `TROPHY_CASE.md`, or open pull requests.

pass: true
