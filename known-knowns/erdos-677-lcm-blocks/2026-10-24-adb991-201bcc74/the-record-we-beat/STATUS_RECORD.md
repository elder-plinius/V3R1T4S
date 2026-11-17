# The record we beat: Erdős Problem 677 = Justin Sun Prize JSP-000550, k ≤ 25

The status source (the Justin Sun Prize catalog) and the problem's own page (erdosproblems.com/677, with its forum,
proof-claims page and history) record the problem as open and record no verification for a range of (n, k). What was
known before this package, as found by this run's NOVELTY skeptic (`panel/novelty.md`, 2026-10-24), is:

| k | previously known coverage | source |
|---|---|---|
| k ≤ 2 | settled for all n (elementary: R(1) = R(2) = 1 in Lemma A; k = 2 is strictly increasing) | `object/PROOF.md`, Step 1 (a) |
| k = 3 | settled for all n | S. Chan, arXiv:2408.01306 (Period. Math. Hung. 2025), Theorem 1 |
| 4 ≤ k ≤ 25 | finite searches only: about n, m ≤ 2·10^5 for k ≤ 12 (Kuberwastaken/c5-k4), and n < m ≤ 1.5·10^5 for k ≤ 150 (Danesh–Bianchetti, IJMTT 72(9), 2026, as reported by a third-party audit; the paper itself could not be read) | rows 4, 7, 8, 9 of `panel/novelty.md`, section 3 |

So the new content of this package is **4 ≤ k ≤ 25, for every n ≤ 10^494 and every m ≥ n + k** (`panel/gate.md`,
"Hedging"). If the unread 2026 paper settles k = 4 and 5 for all n, the new content narrows to 6 ≤ k ≤ 25; the same
third-party audit says that paper leaves k = 6 open.

Everything below is copied from the NOVELTY skeptic's fetch log (`panel_work/novelty/fetch_log.txt` in the run folder
2026-10-24-0818; one request per URL, User-Agent "V3R1T4S-research-bot", UTC time from `date -u`, HTTP status from
curl, sha256 of the saved file) and from the files it saved. The sha256 values were recomputed from the saved files
when this package was built (2026-10-24) and agree with the log. The pages themselves are not copied into this
package. No HTTP response headers were saved by the skeptic, so none are listed.

## 1. Status source: the Justin Sun Prize catalog, entry JSP-000550

| field | value |
|---|---|
| url | https://raw.githubusercontent.com/TheJustinSunPrize/awards/main/problems/catalog-0501-0600.md |
| fetched_utc | 2026-10-24T10:28:17Z |
| http_status | 200 |
| bytes | 127396 |
| sha256 | 78ecc0e2a46520944d1b2f07196bd945433e82e4788a32585f22604c6b8b7834 |
| selected headers | not saved |

The run's scout fetched the same URL at 2026-10-24T08:21:40Z (HTTP 200) with the same sha256
(`how-we-built-it/claim/CLAIM.md`, "Status record").

Lines 843-856 of the saved file, verbatim:

```
## JSP-000550 · Must two disjoint equal-length intervals of consecutive integers have different least common multiples?

| Field | Content |
| --- | --- |
| Date proposed | No later than 1979 (bibliographic evidence) |
| Mathematical area | Number theory |
| Problem description | Must two disjoint equal-length intervals of consecutive integers have different least common multiples? |
| Current status | Open |
| Lean proof | No |
| Eligible to claim | No |
| Historical bounty |  |
| Elapsed years | About 47 years (since 1979) |
| Publication details |  |
| Scholarly recognition |  |
```

The cell compared against: `Current status | Open`, with no recorded partial result (`Publication details` and
`Scholarly recognition` empty). The skeptic also diffed the JSP-000550 section of all 261 distinct pull-request
versions of this catalog file against main: no pull request changes the status from Open (`panel/novelty.md`, row 15).

## 2. The problem page: erdosproblems.com/677 (T. F. Bloom)

| page | url | fetched_utc | http_status | bytes | sha256 |
|---|---|---|---|---|---|
| problem page | https://www.erdosproblems.com/677 | 2026-10-24T10:28:17Z | 200 | 32435 | 3d947ff293f44167b4a0a2a30dc9fa1882b04b520bca4a98ee5db40c5a22737f |
| forum thread | https://www.erdosproblems.com/forum/thread/677 | 2026-10-24T10:28:18Z | 200 | 50285 | d1882fc9cc608392a4bf9bd719979f131cee06e49916d39081af74f65324a20d |
| proof claims | https://www.erdosproblems.com/forum/thread/677/proof-claims | 2026-10-24T10:28:35Z | 200 | 38069 | 85e1e94ce3acc8953e6cf920a068f359b79cd01d514bc0013a44544aa506a73e |
| page history | https://www.erdosproblems.com/history/677 | 2026-10-24T10:28:36Z | 200 | 26985 | 92acc4d7fcdcc7fe27419f2ec4a041b09b30e18b07ae2a53453ce29c86bbb993 |
| LaTeX source | https://www.erdosproblems.com/latex/677 | 2026-10-24T10:28:36Z | 200 | 25379 | a5b8c0fdae8b4f74679c1478f3c46b4ce9fc14d260570fc99ca08cfd8067bb44 |
| the site's data file | https://raw.githubusercontent.com/teorth/erdosproblems/main/data/problems.yaml | 2026-10-24T10:28:37Z | 200 | 417289 | 3fe99c8c0bd87e90a9d6db053471a90aaef5762e024e27069783d071a1e9c6be |

The problem page's HTML differs in sha256 from the scout's earlier fetch (2026-10-24T08:21:38Z, sha256
fc9bde5b511ac69b62b441fb8a75596ec11420e1bf2409e04f34d860f26e5cad) because the HTML is dynamic; the skeptic found the
extracted text line-for-line identical (`panel/novelty.md`, section 1).

The statement, line 401 of the saved problem page, verbatim:

```
Let $M(n,k)=[n+1,\ldots,n+k]$ be the least common multiple of $\{n+1,\ldots,n+k\}$.<br><br>Is it true that for all $m\geq n+k$\[M(n,k) \neq M(m,k)?\]
```

The only result the page records for this (equal-length) question, the first sentence of line 419, verbatim:

```
The Thue-Siegel theorem implies that, for fixed $k$, there are only finitely many $m,n$ such that $m\geq n+k$ and $M(n,k)=M(m,k)$.
```

That finiteness is ineffective: it gives no explicit range. The rest of the paragraph is about the different-length
equation M(n,k) = M(m,l) (Erdős knew only M(4,3) = M(13,2) and M(3,4) = M(19,2)). The page also shows, verbatim,
`Proof expositions (0)` (line 435), `No proof expositions yet.` (line 444), `Proof claims (0)` (line 457) and
`This page was last edited 30 September 2025.` (line 470). The site's data file has, for `number: "677"`
(lines 11180-11189), `status:` / `state: "open"` / `last_update: "2025-08-31"`.

The forum thread (8 comments, dated 2026-03-31 to 2026-04-02, per `panel/novelty.md`) gives further different-length
examples and links a Lean repository (qrdlgit/erdos677) with fixed-gap finiteness lemmas; no comment reports a range
verification or a solution. The proof-claims page says no proof claims have been submitted. The history page shows
one earlier revision with the same text.

## 3. The prior results this package is measured against

| source | url | fetched_utc | http_status | sha256 | what it covers |
|---|---|---|---|---|---|
| S. Chan, arXiv:2408.01306v2 (PDF, read by the skeptic) | https://export.arxiv.org/pdf/2408.01306v2 | 2026-10-24T10:43:47Z | 200 | 7d124d867eb77eb8397a448a9185beb4c3ae2183a6a256f91d5cfb57fac5e407 | k = 3 for all n (with Lemma A, k = 3 forces r = 2) |
| Kuberwastaken/c5-k4, `results/expansion/live-search-2026-08-15/erdos-hunt.md` | https://raw.githubusercontent.com/Kuberwastaken/c5-k4/HEAD/results/expansion/live-search-2026-08-15/erdos-hunt.md | 2026-10-24T10:42:15Z | 200 | bebea8e645c8c1e24c2ead70d9becbee89e107f54cb55683065cbf77acd53b2f | a search up to n, m ≤ 2·10^5 for k ≤ 12 |
| MaxwellLaw/erdos-677-research (shallow git fetch; commit c18015c80f350230082c435cfaa3e7cd1851a66d), `cas/SOURCE_AUDIT.md` | https://github.com/MaxwellLaw/erdos-677-research.git | 2026-10-24T10:42:19Z | git exit 0 | (git commit above) | a third-party audit of Danesh–Bianchetti 2026: search region 1 ≤ k ≤ 150, 0 ≤ n < m ≤ 150000; k = 6 left open |
| Danesh–Bianchetti, IJMTT 72(9), 2026 | https://ijmttjournal.org/public/assets/volume-72/issue-9/IJMTT-V72I9P101.pdf | 2026-10-24T10:42:46Z | 000 (proxy CONNECT 403, not retried) | none | not read first-hand |

Chan's Theorem 1, from the skeptic's text extraction of the PDF (`panel_work/novelty/chan.txt`, lines 54-55), verbatim:

```
Theorem 1. The Diophantine equation b(b + 1)(b + 2) = 2a(a + 1)(a + 2) has a = 3 and b = 4 as
its only positive integer solution.
```

The c5-k4 file's line 33, verbatim:

```
| 677 `erdos_677` | `HOLD_BOUNDED` | dict sweep n,m ≤ 2·10^5 k ≤ 12 + complete-in-m divisor-run n ≤ 40 k ≤ 24, 0 hits |
```

The MaxwellLaw audit (`cas/SOURCE_AUDIT.md` at the commit above, lines 10-11), verbatim:

```
- [Danesh–Bianchetti 2026](https://ijmttjournal.org/public/assets/volume-72/issue-9/IJMTT-V72I9P101.pdf), Section 8.2, explicitly leaves k=6 unfinished. It lists four cubic equations plus square and carry restrictions. Independent exact birational maps and denominator checks are in `CAS.md`.
- That paper's reported search region is `1<=k<=150`, `0<=n<m<=150000`; it reports no disjoint collision. This is finite evidence, not nonexistence for every start. The full reported search was not rerun in this audit.
```

## 4. Other places searched (from `panel/novelty.md`, section 3)

Twelve arXiv API queries covering 2024-10 to 2026-10; Hajdu–Tijdeman and the Shorey–Tijdeman survey (abstracts);
Saradha–Shorey 1990 and Shorey 1984 (not reached first-hand; scope from secondary accounts); GitHub code and
repository searches; the forum-linked Lean repository qrdlgit/erdos677; V3R1T4S TROPHY_CASE.md (no Erdős 677 entry)
and all 615 V3R1T4S pull-request heads; all 4580 prize-repository pull-request heads; five web searches. None records
a result containing this range. Blocked by the contributor's proxy (403, not retried): the Farhi–Kane PDF,
ijmttjournal.org, erdosproblemaday.com and a Tao blog post.

## 5. The cell compared in this package

| source | cell | recorded value | this package |
|---|---|---|---|
| Justin Sun Prize catalog, JSP-000550 (2026-10-24T10:28:17Z) | Current status | Open; no partial result recorded | partial win only, not a solution |
| erdosproblems.com/677 (2026-10-24T10:28:17Z) | recorded results for M(n,k) ≠ M(m,k), m ≥ n + k | Thue–Siegel finiteness for each fixed k; no range verification | no counterexample with 1 ≤ k ≤ 25, 0 ≤ n ≤ 10^494, every m ≥ n + k (computer-assisted, not kernel-checked) |
| best known coverage for 4 ≤ k ≤ 25 (`panel/novelty.md`) | verified range | finite searches, about n, m ≤ 2·10^5 (k ≤ 12) and n < m ≤ 1.5·10^5 (k ≤ 150, second-hand) | every n ≤ 10^494, m uncapped |
