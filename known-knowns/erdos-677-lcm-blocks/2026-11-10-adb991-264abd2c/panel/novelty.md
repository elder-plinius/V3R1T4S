# Novelty skeptic: erdos-677-lcm-blocks, k = 29, 0 ≤ n ≤ 10^494, every m ≥ n + k

Question: is the cell (k = 29, 0 ≤ n ≤ 10^494, all m ≥ n + 29) already covered by published or posted work, or
trivially derivable from it?

Working files: `panel_work/novelty/` (fetched bytes in `fetched/`, request log `fetch_log.tsv`, helper `fetch.sh`).
Every request used User-Agent "V3R1T4S-research-bot", with at most one retry per URL. Work window 09:20 to 09:25 UTC,
2026-11-10.

## Status sources (fetched once each)

| source | URL | fetched (UTC) | HTTP | sha256 | what it says |
|---|---|---|---|---|---|
| prize catalog, JSP-000550 | https://raw.githubusercontent.com/TheJustinSunPrize/awards/main/problems/catalog-0501-0600.md | 2026-11-10T09:20:41Z | 200 | 78ecc0e2a46520944d1b2f07196bd945433e82e4788a32585f22604c6b8b7834 | "Current status: Open", "Lean proof: No". Bytes identical to the scout's fetch of 2026-11-09. |
| problem page | https://www.erdosproblems.com/677 | 2026-11-10T09:20:41Z | 200 | bcafdf8fd4deee80f97ec3cf82d6c70d8a768c64d0bf062c7426882f53990e4c | Open. "Last edited 30 September 2025"; Comments (8), Proof claims (0), Proof expositions (0). Only finiteness for fixed k (Thue–Siegel, ineffective) is stated. The hash differs from the scout's only in a Cloudflare email-obfuscation token, the challenge script and the "accessed" date; the problem text is unchanged. |
| forum thread | https://www.erdosproblems.com/forum/thread/677 | 2026-11-10T09:20:42Z | 200 | 4ba1f110375f8c29700dade626280c065f0149b60e33aa0a563084a2c750a512 | 8 comments, 31 Mar to 2 Apr 2026, posting suspended. Content: unequal-length examples (M(8,4)=M(43,2), M(153,3)=M(1363,2)), padded forms of 420, a Lean repository (qrdlgit/erdos677), and the Farhi–Kane lcm paper. No computational verification of the same-k statement, and nothing about k = 29. |

## Searches and findings

**arXiv API** (export.arxiv.org over HTTPS, sorted by submission date, newest first; plain-HTTP attempts failed with a
DNS error and are logged):

- `all:"least common multiple" AND all:consecutive` gives 12 results. The relevant ones are 2410.09138 (a different Erdős
  lcm question: lcm ratios of a block versus a larger later block) and 0808.1507 (Farhi–Kane, periodicity of
  product/lcm). Neither verifies M(n,k) ≠ M(m,k).
- `all:Erdos AND all:677` gives 0 results. `abs:"consecutive integers" AND abs:"same set of prime factors"` gives 0.
- `abs:"least common multiple" AND abs:intervals` gives 3 results, all on other problems. `abs:"least common multiple"
  AND abs:Erdos` gives 1 unrelated result.
- `ti:lcm OR ti:"least common multiple"`: of the newest 40 (through 2026-11-08), none is about Erdős 677.
- Known related paper (cited by laaielichter): Chan, arXiv:2408.01306, settles only the curve behind k = 3.

**GitHub REST API** (public; per-repository endpoints return 403 in this session, so files were read through
raw.githubusercontent.com):

- Repository search `erdos 677`, `erdos677`, `lcm consecutive erdos` finds 5 repositories: laaielichter/erdos-677,
  MaxwellLaw/erdos-677-research, KDDavis91/erdos677-curve-visualisation, vibemathing/problem-um-ep-677-…,
  qrdlgit/erdos677.
- Code search `erdos_677 lcmInterval` (55 hits) and `"Erdos 677" lcm search` (1 hit). The hits are restatements,
  benchmark copies, Lean lemma packages and small scans. `"erdos-677-lcm-blocks"` has 0 hits.
- PR search `JSP-000550 is:pull-request` finds only awards #4288 (wrong problem), #4846 (two closed numeric examples)
  and #3543 (unrelated). The `"erdos 677"` issue/PR search is swamped by unrelated #677 items.

**What each source covers:**

| work | scope | reaches k = 29 with every m? |
|---|---|---|
| laaielichter/erdos-677 (README, WRITEUP.md, run_1e8.txt; sha256 6347ce81…, b02537fa…, 60ac91ab…) | exhaustive hash-and-exact search, 3 ≤ k ≤ 100, all 0 ≤ n < m, m ≥ n+k, **m + k ≤ 10^8**. Its k = 29 line reads `k=29 windows=99999972 … solutions=0`. It also proves k = 3 completely. | Only with m capped. Its own size bound gives m + 1 ≤ (n+k)·(28!)^{1/29} ≈ 10.39(n+k), so every m is covered for n ≤ about 9.6·10^6. With the elementary Lemma A window m + k ≤ (n+k)·R(29)^{1/29}, where R(29)^{1/29} ≈ 2.377, every m is covered for n ≤ about 4.2·10^7. |
| MaxwellLaw/erdos-677-research (README, docs/PRIOR_WORK.md, docs/RESEARCH_STATUS.md) | k = 6 only (curves, heights, Lean parts); a prior-work audit of the field up to 2026-10-27 | no |
| HuanHuanHuanFFF/lean-math-lab, RegionConsumer.lean @37e42ac (sha256 5b587c96…) | every k: no collision if m − n ≤ 8k or n ≤ 369k, **conditional** on an assumed `DusartPrimeInterval` hypothesis | conditionally, n ≤ 10701 only |
| the-omega-institute/trureturing #8768 / erdos677.py | scan N = 40000, k ≤ 24 (per the MaxwellLaw audit; the script's defaults agree) | no (k ≤ 24, small n) |
| Kuberwastaken/c5-k4 erdos-hunt.md | n, m ≤ 2·10^5 for k ≤ 12; complete in m for n ≤ 40, k ≤ 24 | no |
| KDDavis91 (k = 5 visualisation), qrdlgit (Lean lemmas, k-generic, no range), vibemathing (harness stub), conjectures-io (lcmInterval API lemmas), plasma-ai wiki and dust-tt/srchd (status pages: open), formal-conjectures 677.lean (sha256 cc682a41…, statement `sorry`, category research open), teorth/erdosproblems problems.yaml (677: open, last update 2025-08-31) | no verification ranges | no |

**V3R1T4S checkout.** TROPHY_CASE.md, known-knowns/, known-unknowns/ and the rest of the checkout (head fb51644) contain
no entry for Erdős 677. A grep for erdos-677, Erdős 677, erdos_677, lcmInterval, JSP-000550 and lcm-blocks finds
nothing. The "677" hits in TROPHY_CASE.md are a matrix-multiplication rank. The workspace's own draft PRs #994
(n ≤ 5871k, every k), #995 (k ≤ 25, n ≤ 10^494) and #996 (26 ≤ k ≤ 28, n ≤ 10^494) are listed as open drafts by the
GitHub search API. They are the same contributor's work, not prior art. For k = 29 they reach only n ≤ 5871·29 = 170259.
Nothing in the checkout covers k = 29.

## Best published object for this cell

laaielichter/erdos-677 `run_1e8.txt`: no collision for k = 29 with m + k ≤ 10^8. Turning it into an "every m" statement
needs a window bound:

- With its own published size bound, it covers n ≤ about 9.6·10^6.
- With the elementary Lemma A window, it covers n ≤ about 4.2·10^7.

The next best results are conditional (n ≤ 369·29 = 10701, assuming Dusart) or smaller scans. The claim's range,
n ≤ 10^494, goes about 486 orders of magnitude beyond the best published coverage.

## Trivially derivable?

No. The only published general statement is Thue–Siegel finiteness for fixed k, which is ineffective and gives no bound
on n. To get from n ≈ 10^7 to n ≈ 10^494, the claim needs:

- the 114817-ratio Lemma-A curve set for k = 29;
- a rigorous asymptotic margin on each curve;
- a continued-fraction enumeration to q ≤ 10^495.

None of these is in any source found. The method is the same one the workspace used for k ≤ 28, which is still
unpublished draft PRs, so it is not prior art. Correctness is for the other skeptics. This verdict is only about
coverage.

## Verdict

The cell (k = 29, 0 ≤ n ≤ 10^494, every m ≥ n + 29) is not covered by published or posted work and is not trivially
derivable from it. The published coverage for k = 29 with every m ends near n ≈ 10^7 (from laaielichter's
m + k ≤ 10^8 search). The problem stays open at all three status sources (catalog Open, problem page Open with 0 proof
claims, forum with nothing new since April 2026), so no published solution makes the partial result moot. The claim is
novel in scope.

context: subagent (fresh context, Claude Code Agent tool)
pass: true
