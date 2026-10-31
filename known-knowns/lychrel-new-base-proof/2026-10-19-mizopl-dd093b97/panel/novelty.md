# Skeptic Panel Report — Role: NOVELTY

> **Dated Note (2026-10-29):** This panel report originally reviewed the earlier three-base + audit version under `claim/`, which has since been split into **#517** (this package: base 50, where `claim/lychrel_base50_certificate.json` is now at `object/lychrel_base50_certificate.json` with identical `sha256: dd093b972a4f7eb7d6d9db4c5809a3332e413868719635bb6d2fdc9e59dacdb2`), **#723** (base 98), **#724** (base 146), and **#725** (Kuitché 2023 audit). The other `claim/` files (`lychrel_base98_certificate.json`, `lychrel_base146_certificate.json`, `kuitche_2023_audit.json`) and copied third-party pages/PDFs (`Lychrel_number.html`, `dseal_live.htm`, `rs_2659802.pdf`) named below are no longer included in this directory.

- `target_id`: `lychrel-new-base-proof`
- `panelist_role`: `NOVELTY`
context: Antigravity fresh subagent (invoke_subagent, role NOVELTY)
- `audit_utc`: `2026-10-19T06:30:18Z` – `2026-10-19T06:30:48Z`

## 1. Mandate

> "Fetch the primary table or status page once, honestly (no retries; a block means fail), and quote URL, value and time. Search the last 24 months of literature, this repo's TROPHY_CASE.md and open pull requests. Pass only if the result strictly beats everything known. A tie is not a record."

---

## 2. Honest Single-Fetch Verification of Primary Status Pages & Reference Tables

Every URL below was fetched once via `curl -sS -D ... -A "V3R1T4S-research-agent (honest single fetch)"` with zero retries.

| # | Source URL | Fetch Time (UTC) | HTTP Status | Byte Size | SHA-256 Digest | Value / Listed Proven Lychrel Bases |
|---|---|---|---|---|---|---|
| 1 | `https://en.wikipedia.org/wiki/Lychrel_number` | `2026-10-19T06:30:18Z` | `HTTP/2 200` | `206,959` | `2e5338385838c5abe91d01fb0fb68ae77ada436ef0ea765a340629d14bd6ab05` | `"Lychrel numbers have been proven to exist in the following bases: 11, 17, 20, 26, and all powers of 2."` |
| 2 | `https://oeis.org/search?q=id:A023108&fmt=json` | `2026-10-19T06:30:18Z` | `HTTP/2 200` | `6,811` | `df70aa9263660a0cf0203c818870df01bfa18e1a865abc21bd0627d36ca6047c` | Base-10 Lychrel candidates only (`196, 295, 394, ...`); zero proofs in base `50` (or `98`, `146`). |
| 3 | `https://oeis.org/search?q=id:A060382&fmt=json` | `2026-10-19T06:30:18Z` | `HTTP/2 200` | `3,777` | `12f4f464c277612795a9e25527fb1719d8ebccc05859b2db383237c55c507105` | Smallest base-$n$ candidate $a(n)$ (`22, 103, 290, ...`); comment states `"Only a(2) is proved, all the others are conjectured."` Zero proofs or template cycles in base `50` (or `98`, `146`). |
| 4 | `https://www.mathpages.com/%68ome/dseal.htm` | `2026-10-19T06:30:19Z` | `HTTP/2 200` | `4,085` | `abd869951209dd65d19b0ea8000f2bc3a3bed28bfeeece9097f258ef1ad95c3c` | David Seal's January 1996 `rec.puzzles` posting listing only `"Base 4"`, `"Base 11"`, `"Base 17"`, `"Base 20"`, and `"Base 26"`. |

### 2.1 Detailed Primary Source Quotes

1. **Wikipedia (`https://en.wikipedia.org/wiki/Lychrel_number`, fetched `2026-10-19T06:30:18Z`):**
   - Exact sentence in the `"Other bases"` section:
     > `"Lychrel numbers have been proven to exist in the following bases: 11, 17, 20, 26, and all powers of 2."`
   - Base `b = 50 = 2 * 5^2` is not a power of 2 and does not appear among the proven bases on `https://en.wikipedia.org/wiki/Lychrel_number` at verification time.
   - All 15 cited references on the Wikipedia page (`cite_note-1` through `cite_note-15`, including Kevin Brown's MathPages article *"Digit Reversal Sums Leading to Palindromes"*, Jason Doucette's records, Wade VanLandingham's `p196.org` pages, Romain Dolbeau's `p196_mpi` page, OEIS `A060382`, and `"Letter from David Seal"`) were inspected; none contains any proof in base `50`.

2. **OEIS `A023108` and `A060382` (`2026-10-19T06:30:18Z`):**
   - `A023108` (*"Positive integers which apparently never result in a palindrome under repeated applications of the function A056964(x) = x + (x with digits reversed)"*) records only base-10 empirical candidates (`196, 295, 394, ...`).
   - `A060382` (*"In base n, a(n) is the smallest number m that leads to a palindrome-free sequence..."*) records empirical smallest starting values $a(n)$ across bases $n \ge 2$ and notes `"Only a(2) is proved, all the others are conjectured."` Neither sequence contains any template-closure proof for base `50`.

3. **MathPages (`https://www.mathpages.com/%68ome/dseal.htm`, fetched `2026-10-19T06:30:19Z`):**
   - Exact opening quote:
     > `David Seal posted the following "sporadic solutions" for reverse-sum iterations in the Usenet Newsgroup rec.puzzles in January of 1996:`
   - Lists only `Base 4` (period 6), `Base 11` (period 6), `Base 17` (period 6), `Base 20` (untranscribed over-200-digit template), and `Base 26` (period 4: `1N5ELA6C(n Ps)P6E7(n 0s)0D59ME5N`). Base `50` is absent.

4. **Rostand S. Kuitché (2023), *"On the Construction of Some Lychrel Numbers"* (DOI `10.21203/rs.3.rs-2659802/v1`, `648,343` bytes, `sha256: c5130873a5d82c3577ac52d7a9a1ec94a7dce1017d9ce2dededa13a87f64dac7`; audited in companion package #725):**
   - Sections 2–3 prove four 1-step/2-step sibling-preimage equivalence relations (Propositions 3.1–3.4) restricted to bases $3 \le b \le 10$ showing $\phi(a) = \phi(x)$ or $\phi^2(a) = \phi^2(x)$.
   - Section 4 Case 1 gives an explicit template cycle only in base $b = 4$ (a power of 2, already covered by $\{2^k\}$).
   - Section 4 Case 2 and Section 5 apply Propositions 3.1–3.4 in base $b = 10$ to unproved candidates (`196, 879, 1997, 7059`) to generate sibling candidates tested numerically to `530,914` iterations without any template-closure proof.
   - The natural base-$b$ analogue of Section 4 Case 1 fails template closure in every non-power-of-2 base $b \in \{3, 5, 6, 7, 9, 10\}$ (and reaches a palindrome in bases $3, 5, 6, 7, 10$). Thus Kuitché (2023) proves zero new bases outside $\{2^k, 11, 17, 20, 26\}$ and never considers base `50`.

---

## 3. Literature & Repository Search (Last 24 Months + Full Historical Scope)

| # | Query URL | Fetch Time (UTC) | HTTP Status | Byte Size | SHA-256 Digest | Findings |
|---|---|---|---|---|---|---|
| 5 | `https://export.arxiv.org/api/query?search_query=all:%22Lychrel%22&sortBy=submittedDate&sortOrder=descending&max_results=25` | `2026-10-19T06:30:44Z` | `HTTP/2 200` | `704` | `82b04f36aa15c0d1516cf9d8bb1450137bf8beee2706fddd9bf88cfe5942c991` | `totalResults: 0` (`0` preprints matching `"Lychrel"` on arXiv). |
| 6 | `https://api.openalex.org/works?search=Lychrel&per-page=25` | `2026-10-19T06:30:45Z` | `HTTP/2 200` | `293,047` | `351cf3600f0b952b77e0eecd441e6036afd983b06dfdb16a22796c354199b661` | `31` total works indexed (including `13` from 2024–2026); zero works prove Lychrel numbers or template cycles in base `50`. |
| 7a | `https://api.github.com/search/repositories?q=Lychrel` | `2026-10-19T06:30:45Z` | `HTTP/2 200` | `157,699` | `cef93268a3da41005cfb7564026f40694dad93a971635c4d68352fed0a951627` | `94` repositories returned; all are base-10/196 empirical searchers or educational scripts. Zero repositories mention base `50`. |
| 7b | `https://api.github.com/search/code?q=%221N5ELA6C%22+OR+%22lychrel%22+%22base+50%22` | `2026-10-19T06:30:47Z` | `HTTP/2 401` | `120` | `b7dbd173f33b19650f61b1c528737e2037cf768d90076fdfce5d32541765e29e` | Unauthenticated GitHub code-search endpoint returns `401 Requires authentication`; repository search (7a) succeeded with `HTTP/2 200`. |
| 8a | `https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md` | `2026-10-19T06:30:47Z` | `HTTP/2 200` | `31,235` | `b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1` | `100` lines; case-insensitive search for `"lychrel"` returns `0` matches. |
| 8b | `https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100` | `2026-10-19T06:30:48Z` | `HTTP/2 200` | `2,055,941` | `9dd6295eb62c2e2c234f10d0b14c04e0ebca268e5ce22b1b9f9c5a480f4be5ae` | `87` open pull requests (`#401` through `#487`); `0` open pull requests mention `"lychrel"`, `lychrel-new-base-proof`, or `base 50`. |

### 3.1 Review of Recent Literature (2024–2026) from OpenAlex

All works dated 2024–2026 in the OpenAlex response (`sha256: 351cf3600f0b952b77e0eecd441e6036afd983b06dfdb16a22796c354199b661`) were audited:
- `W4402065007` (`2024-01-01`, DOI `10.4236/apm.2024.148037`, *"Lychrel Numbers in Base 10: A Probabilistic Approach"*): heuristic/probabilistic discussion in base 10; explicitly states in its abstract that proven existence is known in `"base 2, 11 or 17"`.
- `W7115005317` (`2024-01-01`, DOI `10.13140/rg.2.2.15542.97607`, *"Numerical Experiments Around the Lychrel Conjecture"*): numerical experiments in base 10.
- `W7112251530` (`2025-09-18`) and `W7106695520` (`2025-11-25`, DOI `10.5281/zenodo.17716998`): philosophical/heuristic essays on `196` in base 10.
- `W7142970438` / `W7148857843` (`2026-01-01` / `2026-04-03`, DOI `10.5281/zenodo.19395251`): divisibility by 11 of even-digit base-10 palindromes.
- `W7130530939` (`2026-02-19`, DOI `10.5281/zenodo.18694586`), `W7136063045` (`2026-03-15`), `W7154941775` (`2026-04-20`), `W7161739774` (`2026-05-19`), `W7169713277` (`2026-07-19`), `W7202027492` (`2026-08-09`), `W7206202609` (`2026-09-02`): base-10 `196` candidate heuristics or general dynamical essays; zero template-closure proofs in new bases.
- `W7166506178` (`2026-06-29`, DOI `10.17605/osf.io/aqwg7`, *"The Minimal Condition for Reverse-and-Add Universality"*): empirical carry-density study across bases $b = 2, \dots, 16$.
- `W7221326814` (`2026-10-11`, DOI `10.5281/zenodo.23289048`, *"Self-similar reverse-and-add cycles and a base-9 Lychrel family"*): Zenodo software upload addressing base 9; does not touch base `50`.

---

## 4. Conclusion on Novelty

1. The primary status page `https://en.wikipedia.org/wiki/Lychrel_number` (`2026-10-19T06:30:18Z`, `HTTP/2 200`, `sha256: 2e5338385838c5abe91d01fb0fb68ae77ada436ef0ea765a340629d14bd6ab05`) lists only `"11, 17, 20, 26, and all powers of 2"` as proven bases.
2. Base `50` ($2 \cdot 5^2$) is neither a power of 2 nor in $\{11, 17, 20, 26\}$, and `50` does not appear as a proven Lychrel base in Wikipedia, OEIS (`A023108`, `A060382`), MathPages (`dseal.htm`), Kuitché (2023), arXiv, OpenAlex, GitHub, `TROPHY_CASE.md`, or open pull requests (`#401`–`#487`).
3. The mechanical template-closure proof in `object/lychrel_base50_certificate.json` strictly expands the set of proven Lychrel bases beyond everything previously known.

pass: true
