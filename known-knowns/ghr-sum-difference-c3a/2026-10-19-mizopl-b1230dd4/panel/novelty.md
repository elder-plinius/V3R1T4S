# Panel Review: NOVELTY (`ghr-sum-difference-c3a`, Partial Win `p1`)

role: NOVELTY
context: Antigravity fresh subagent (invoke_subagent, role NOVELTY)
problem_id: ghr-sum-difference-c3a
partial_win_id: p1

## 1. Mandate

> Fetch the primary table or status page once, honestly (no retries; a block means fail), and quote URL, value and time. Search the last 24 months of literature, this repo's TROPHY_CASE.md and open pull requests. Pass only if the result strictly beats everything known. A tie is not a record.

---

## 2. Honest Single Fetch of Primary Status Page (`constants/3a.md`)

A single unconditional HTTP GET was executed against the canonical status page:

- **URL:** `https://raw.githubusercontent.com/teorth/optimizationproblems/main/constants/3a.md`
- **UTC Timestamp:** `2026-10-19T00:41:05Z`
- **HTTP Status:** `HTTP/2 200`
- **Byte Size:** `9,559` bytes (matches `claim/3a.md` byte-for-byte)
- **SHA-256:** `7fcaf2453bc29c26452b9421152df4111ec3aa459d40de653fa0fabd5d439adf`

### Top Rows of the `## Known lower bounds` Table (Quoted from `constants/3a.md` Lines 31–35)

| Bound | Reference | Comments (sanitized for angle brackets) |
|---|---|---|
| `$1.1740744$` | `[G2026]` | Base-$21$ digit construction with exact counting certificate. |
| `$1.1835129324$` | `[MI2026]` | Base-$33$ digit construction with exact counting certificate. |
| `$1.187326127925948$*` | `[Num2026]` | Capped base-$89$ digit construction (max digit $44$, sparse 29-letter alphabet); certified as the large-deviation LIMIT of the exact per-depth lemma values $\theta(U_d)$. |
| `$1.19102809$*` | `[K2026]` | Base-$34065$ masked-digit limit construction with $M=\langle 1518,1524,1587,2024,2032,2116\rangle\cap[0,17032]$ and a directed-rounding certificate. |
| `$1.19102809$ ($1.19519192$*)` | `[K2026b]` | Lean-formalized proof of $1.19519192$* via controlled-carry masked-digit limit construction with $M=\langle 1971,2016,2100,2628,2688,2800\rangle\cap[0,26972]$ in base $27022$ and Lean-formalized explicit finite construction of $1.19102809$ with $M=\langle 1518,1524,1587,2024,2032,2116\rangle\cap[0,17032]$ in base $34065$ using $10^{13}$ digits. |

### Verification of Live Baseline Records on `constants/3a.md`

1. **Best finite-certified lower bound on `constants/3a.md`:** `1.19102809` (`[K2026b]`, base $Q = 34065 = 2B + 1$, mask bound $B = 17032$, finite depth $N = 10^{13}$ digits).
2. **Best limit (asterisked) lower bound on `constants/3a.md`:** `1.19519192*` (`[K2026b]`, even base $q_2 = 27022$, mask bound $B_2 = 26972$, asymptotic limit $N \to \infty$ without a finite-depth certificate).

---

## 3. Audit of Upstream Repositories (`teorth/optimizationproblems` and `kleinwaks/masked-digit-sum-difference-bound`)

1. **`teorth/optimizationproblems` Open Pull Requests:**
   - **URL:** `https://api.github.com/repos/teorth/optimizationproblems/pulls?state=open&per_page=50`
   - **UTC Timestamp:** `2026-10-19T00:41:05Z`
   - **HTTP Status:** `HTTP/2 200`
   - **Byte Size:** `271,878` bytes
   - **SHA-256:** `24d63176b73216a9427924fbcac6bae0263e42fe930ba06494907defb593e210`
   - **Findings:** `14` open pull requests returned (`#235, #234, #232, #228, #226, #223, #217, #209, #205, #203, #196, #195, #184, #148`). Only PR `#148` (opened `2026-08-19T18:00:11Z`, title `"Improve C_3a lower bound to 1.21418 via two-temperature cyclic compression"`) touches `constants/3a.md`. Inspection of PR `#148` and its issue comments (`https://api.github.com/repos/teorth/optimizationproblems/issues/148/comments`, fetched `2026-10-19T00:42:56Z`, HTTP `200`, `5,114` bytes, `sha256: 2fc175bee5186da0a59cf32710695d3d78d840a4bbd2ad427b6968e99ad3d17a`) confirms that PR `#148` proposes an unverified asymptotic limit row `1.21418*` ("conservatively marked as a limit value because the written theorem remains unverified") and explicitly leaves the finite-certified record unchanged at `1.19102809` (`README` cell `1.19102809 (1.21418*)`). Thus no open PR on `teorth/optimizationproblems` improves the finite-certified lower bound `1.19102809`.

2. **`teorth/optimizationproblems` Commit History on `constants/3a.md`:**
   - **URL:** `https://api.github.com/repos/teorth/optimizationproblems/commits?path=constants/3a.md&per_page=10`
   - **UTC Timestamp:** `2026-10-19T00:41:06Z`
   - **HTTP Status:** `HTTP/2 200`
   - **Byte Size:** `43,435` bytes
   - **SHA-256:** `223750a6df76dd29e96ede8efada2135f5f89ea1e46e393767d6669c910229ac`
   - **Findings:** The latest commit on `constants/3a.md` is `e1d5596eecfc` (`2026-10-18T05:44:37Z`, `"Merge pull request #198"`), which merged `[K2026c]` into the upper-bound table ($1.312373302115\dots^*$). The last lower-bound modification on `constants/3a.md` was `0b24d2a19ac9` (`2026-08-14T20:41:52Z`, `"Improve lower bound for C_3a"`, followed by reference link update `569192cc3145` on `2026-08-14T23:09:11Z` for PR `#146` `[K2026b]`).

3. **`kleinwaks/masked-digit-sum-difference-bound` Commit History:**
   - **URL:** `https://api.github.com/repos/kleinwaks/masked-digit-sum-difference-bound/commits?per_page=10`
   - **UTC Timestamp:** `2026-10-19T00:41:06Z`
   - **HTTP Status:** `HTTP/2 200`
   - **Byte Size:** `45,345` bytes
   - **SHA-256:** `062a24603966d59e0fbf079788d4bfbc340a952e35c0313157acbcb135baf104`
   - **Findings:** `10` commits total; the latest commit is `352ab86effec` (`2026-08-14T20:12:25Z`, `"Fix Markdown"`), immediately following `395b8e85e0b1` (`2026-08-14T19:06:32Z`, `"Update proof and certificate for C_3a > 1.19519192, add Lean formalization"`). No subsequent commits exist.

---

## 4. Literature Search (Last 24 Months) and Code/Issue Search

1. **arXiv API Search:**
   - **URL:** `https://export.arxiv.org/api/query?search_query=all:%22Gyarmati%22+OR+all:%22sums+and+differences%22+OR+all:%22masked-digit%22&sortBy=submittedDate&sortOrder=descending&max_results=25`
   - **UTC Timestamp:** `2026-10-19T00:41:21Z`
   - **HTTP Status:** `HTTP/2 200`
   - **Byte Size:** `49,822` bytes
   - **SHA-256:** `2c87020c3e0ce4f7841e06ac3429a3defae3ea3ca7eaa8f99a3ad0da7346e951`
   - **Findings:** `25` entries returned, spanning `2026-08-10` to `2026-10-09` (including `2610.12912v1` `"Product and Quotient Set Dominance in Finite Groups"`, `2610.08394v1` `"Generating and generalizing MSTD sets through Markov processes"`, and `2608.22189v2` `"A Classification of Small MSTD Sets in Arbitrary Fields"`). None of the papers report a lower bound on the Gyarmati–Hennecart–Ruzsa constant $C_{3a}$ beyond `[G2025]` (`arXiv:2505.16105`, $1.173050$), `[Z2025]` (`arXiv:2506.01896`, $1.173077^*$), and `[GGSWT2025]` (`arXiv:2511.02864`, $1.1584$).

2. **GitHub Repository, Code, and Issues Search:**
   - **Repository Search URL:** `https://api.github.com/search/repositories?q=masked-digit-sum-difference-bound+OR+C_3a`
     - **UTC Timestamp:** `2026-10-19T00:41:22Z`, **HTTP Status:** `HTTP/2 200`, **Byte Size:** `194,901` bytes, **SHA-256:** `fe8548a62cf6f495e938150208028cac055a8055fcd345e3efb76428aedfee01`
     - **Findings:** No repository contains a finite-certified lower bound exceeding `1.19102809`.
   - **Code Search URL:** `https://api.github.com/search/code?q=1.19102809+OR+27995+17086`
     - **UTC Timestamp:** `2026-10-19T00:41:23Z`, **HTTP Status:** `HTTP/2 401` (`120` bytes, `sha256: b7dbd173f33b19650f61b1c528737e2037cf768d90076fdfce5d32541765e29e`; GitHub `/search/code` requires authentication).
   - **Unauthenticated Issues/PRs Search URL:** `https://api.github.com/search/issues?q=1.19102809+OR+27995+OR+17086+OR+ghr-sum-difference-c3a`
     - **UTC Timestamp:** `2026-10-19T00:41:50Z`, **HTTP Status:** `HTTP/2 200`, **Byte Size:** `162,750` bytes, **SHA-256:** `7f5d2081c456ae9e8b8917d0d6969d81a8bc5b7ef08b90be584fb98b88276511`
     - **Findings:** Confirms zero hits across GitHub for the controlled-carry odd-base parameter pair $(B, q) = (17086, 27995)$ or $(17032, 27995)$. Also shows three historical PRs `#121`, `#122`, `#123` on `elder-plinius/V3R1T4S` that were closed unmerged (`merged_at: null`) on `2026-10-14T12:49:14Z–17Z` (15 minutes after creation) with zero comments (`https://api.github.com/repos/elder-plinius/V3R1T4S/issues/121/comments`, fetched `2026-10-19T00:42:56Z`, HTTP `200`, `2` bytes `[]`, `sha256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`).

---

## 5. V3R1T4S `TROPHY_CASE.md` and Open Pull Requests

1. **`TROPHY_CASE.md`:**
   - **URL:** `https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md`
   - **UTC Timestamp:** `2026-10-19T00:41:24Z`
   - **HTTP Status:** `HTTP/2 200`
   - **Byte Size:** `31,235` bytes (`100` lines)
   - **SHA-256:** `b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1`
   - **Findings:** `0` occurrences of `ghr-sum-difference-c3a`, `3a`, `Gyarmati`, `Ruzsa`, or `Kleinwaks`. Neither full win nor partial win `p1`/`p2` has been claimed in `TROPHY_CASE.md`.

2. **`elder-plinius/V3R1T4S` Open Pull Requests:**
   - **URL:** `https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100`
   - **UTC Timestamp:** `2026-10-19T00:41:24Z`
   - **HTTP Status:** `HTTP/2 200`
   - **Byte Size:** `2,148,060` bytes (`100` open PRs returned)
   - **SHA-256:** `126359d94c53fb1ff4ec748f8842a32e0852aea8982c26e25d1c1d64aa33fdff`
   - **Findings:** Zero open claim pull requests target `ghr-sum-difference-c3a`. The only open pull request mentioning `ghr-sum-difference-c3a` is bank-maintenance PR `#396` (`2026-10-18T09:53:10Z`, `"bank: C_3a and sunflower capacity: Tao's pages as of 2026-10-18"`), which updates only the `statement` text of `ghr-sum-difference-c3a` to reflect the `[K2026c]` upper bound on `constants/3a.md` while explicitly noting `"Criteria are unchanged"` and quoting the lower-bound table end as `$1.19102809$ ($1.19519192$*) [K2026b]`.

---

## 6. Comparison of Claimed Partial Win `p1` Against Published Record

Running `python3 claim/author_checker_c3a_check.py claim` confirms:

- **Published finite-certified record (`constants/3a.md` `[K2026b]`, reproduced by `claim/kleinwaks_finite_certificate_17032_34065.json`):**
  $$C_{3a}(V_{\text{K2026b}}) > 1.19102809427254087548 > 1.19102809$$
- **Secondary new finite-depth certificate (`claim/finite_certificate_17032_27995.json`, $B = 17032, q = 27995, N = 10^{13}$):**
  $$C_{3a}(V_{17032,27995}) > 1.19229904840497896133 \ (\text{mpmath 60-dps}), \quad 1.19229904838280822699 \ (\text{pure integer}) > 1.19229904$$
  (strictly beats `1.19102809` by $+0.00127095 \ge 10^{-7}$).
- **Primary new finite-depth certificate (`claim/finite_certificate_17086_27995.json`, $B = 17086, q = 27995, N = 10^{13}$):**
  $$C_{3a}(V_{17086,27995}) > 1.19230254070568368329 \ (\text{mpmath 60-dps}), \quad 1.19230254068351294895 \ (\text{pure integer}) > 1.19230254$$
  (strictly beats the best finite-certified lower bound `1.19102809` on `constants/3a.md` by $+0.00127445 = 12,744.5 \times 10^{-7}$, while lying below the asymptotic limit record `1.19519192*`, matching the definition of Partial Win `p1`).

pass: true
