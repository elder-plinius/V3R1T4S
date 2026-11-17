# The record we beat: Erdős Problem 677 = Justin Sun Prize JSP-000550

There is no recorded range to beat. Neither the status source (the Justin Sun Prize catalog) nor the problem's own page
(erdosproblems.com/677, with its history, proof-claims page and forum thread) records any verification of the
statement for a range of (n, k), any explicit range with m uncapped, or a solution. The only result the problem page
records is qualitative: for each fixed k, the Thue–Siegel theorem gives finitely many exceptions. So the "record" this
package is compared against is the absence of any recorded range, as read on 2026-10-24 by the round-2 NOVELTY
skeptic (`panel/novelty.md`).

Everything below is copied from the round-2 NOVELTY skeptic's fetch log (`panel_work/novelty_round2/fetch_log.txt` in
the run folder 2026-10-15-0724; one plain request per URL, User-Agent "V3R1T4S-research-bot (novelty skeptic)",
UTC time from `date -u`, HTTP status from curl's `%{http_code}`, sha256 from `sha256sum`) and from the files it saved.
The sha256 values were recomputed from the saved files when this package was built (2026-10-24) and agree with the
log. The pages themselves are not copied into this package. No HTTP response headers were saved by the skeptic, so
none are listed.

## 1. Status source: the Justin Sun Prize catalog, entry JSP-000550

| field | value |
|---|---|
| url | https://raw.githubusercontent.com/TheJustinSunPrize/awards/main/problems/catalog-0501-0600.md |
| fetched_utc | 2026-10-24T08:26:00Z |
| http_status | 200 |
| bytes | 127396 |
| sha256 | 78ecc0e2a46520944d1b2f07196bd945433e82e4788a32585f22604c6b8b7834 |
| selected headers | not saved |

The same URL fetched by the run's scout on 2026-10-15T07:24:59Z (HTTP 200) had the same sha256
(`how-we-built-it/claim/CLAIM.md`, "Status record"), so the catalog volume did not change between the claim and the
round-2 check. The awards repository's main branch HEAD at the skeptic's clone was
5b7126acf3d3d31c71e5964525807d1532cba892.

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
`Scholarly recognition` empty).

## 2. The problem page: erdosproblems.com/677 (T. F. Bloom)

| page | url | fetched_utc | http_status | sha256 |
|---|---|---|---|---|
| problem page (32435 bytes) | https://www.erdosproblems.com/677 | 2026-10-24T08:26:00Z | 200 | c2ed64f6d85f1b970b18641c50d69fb9c4c70b917d2cd3b44dd098a317b0ef19 |
| forum thread | https://www.erdosproblems.com/forum/thread/677 | 2026-10-24T08:26:00Z | 200 | b6a1ecc91bc1ab0ca18d63bcbad4d3822c0d03b9c3f1b1e7d7a6b4fdee247e9f |
| proof claims | https://www.erdosproblems.com/forum/thread/677/proof-claims | 2026-10-24T08:26:36Z | 200 | dfe536c5d6c692ae039c61b6ca8bbbfeff07126a1998ce5e0df6460cf17c7c92 |
| page history | https://www.erdosproblems.com/history/677 | 2026-10-24T08:26:37Z | 200 | 5210ecf22974f091fce7a26c83838095cea6c2235c2ded431f4877bd50801b88 |
| the site's data file | https://raw.githubusercontent.com/teorth/erdosproblems/main/data/problems.yaml | 2026-10-24T08:26:37Z | 200 | 3fe99c8c0bd87e90a9d6db053471a90aaef5762e024e27069783d071a1e9c6be |

On 2026-10-15 the problem page could not be read from the contributor's machine (proxy: `CONNECT tunnel failed,
response 403`, `how-we-built-it/claim/CLAIM.md`); that is why the first gate stopped at PROMISING.

The statement, line 401 of the saved problem page, verbatim:

```
Let $M(n,k)=[n+1,\ldots,n+k]$ be the least common multiple of $\{n+1,\ldots,n+k\}$.<br><br>Is it true that for all $m\geq n+k$\[M(n,k) \neq M(m,k)?\]
```

The only result the page records for this (equal-length) question, the first sentence of line 419, verbatim:

```
The Thue-Siegel theorem implies that, for fixed $k$, there are only finitely many $m,n$ such that $m\geq n+k$ and $M(n,k)=M(m,k)$.
```

The rest of that paragraph is about the different-length equation M(n,k) = M(m,l) (Erdős knew only M(4,3) = M(13,2)
and M(3,4) = M(19,2)) and refers to problem B35 of Guy's collection. The page also shows, verbatim,
`Proof expositions (0)` (line 435), `No proof expositions yet.` (line 444), `Proof claims (0)` (line 457) and
`This page was last edited 30 September 2025.` (line 470). The site's data file has, for `number: "677"`
(lines 11180-11189), `status:` / `state: "open"` / `last_update: "2025-08-31"`.

The forum thread (8 comments, 31 Mar to 2 Apr 2026, per `panel/novelty.md`) gives further different-length examples
and links a Lean repository with finiteness lemmas for fixed gap and fixed k; it gives no range verification, no bound
on n in terms of k and no solution. The proof-claims page says no proof claims have been submitted.

## 3. Other places searched (from `panel/novelty.md`, section 3)

The formal statement (google-deepmind/formal-conjectures `FormalConjectures/ErdosProblems/677.lean`, 2026-10-24T08:33:12Z,
HTTP 200, sha256 cc682a41950449c693578cdfc83060505bcd482abc12ab33233eaea483681bd0, still `research open` with
`sorry`); the forum-linked Lean repository; the AI-contributions wiki (through its git repository); the V3R1T4S
TROPHY_CASE.md and all 615 V3R1T4S pull-request heads; all 4580 prize-repository pull-request heads; ten arXiv API
queries covering 2024-10 to 2026-10; web searches. None records a range verification for this problem. Limits stated
by the skeptic: Guy's B35 was not read; the forum-linked Farhi–Kane PDF and the GitHub web pull-request listings were
blocked by the contributor's proxy (403) and were reached through other routes (the paper's arXiv abstract, git refs).

## 4. The cell compared in this package

| source | cell | recorded value | this package |
|---|---|---|---|
| Justin Sun Prize catalog, JSP-000550 (2026-10-24T08:26:00Z) | Current status | Open; no partial result recorded | partial win only, not a solution |
| erdosproblems.com/677 (2026-10-24T08:26:00Z) | recorded results for M(n,k) ≠ M(m,k), m ≥ n + k | Thue–Siegel finiteness for each fixed k; no range verification | no counterexample with 0 ≤ n ≤ 5871·k, every k ≥ 1, every m ≥ n + k (computer-assisted; relies on Rosser–Schoenfeld 1962 and Schoenfeld 1976) |
