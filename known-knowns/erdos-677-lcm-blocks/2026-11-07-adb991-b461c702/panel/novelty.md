# Novelty skeptic: Erdős 677 (JSP-000550), no counterexample for 26 ≤ k ≤ 28, n ≤ 10^494, any m

Question checked: is a verification of Erdős 677 for 26 ≤ k ≤ 28 with n ≤ 10^494 (m uncapped) already covered by published or posted work? Read: CLAIM.md, object/PROOF.md, source/ (fetch_log.txt, erdosproblems_677.html), REPRODUCE.md, object/search677b.c (header only, for provenance). Kit repo: TROPHY_CASE.md, known-knowns/, plus a grep of the rest of the checkout. Working files are in ../panel_work/novelty/ (paths relative to claim/).

## 1. Status sources (each fetched once, curl, User-Agent "V3R1T4S-research-bot", no retries)

| source | URL | fetched (UTC) | HTTP | sha256 of saved bytes | what it says |
|---|---|---|---|---|---|
| prize catalog | https://raw.githubusercontent.com/TheJustinSunPrize/awards/main/problems/catalog-0501-0600.md | 2026-11-07T09:20:31Z | 200 | 78ecc0e2a46520944d1b2f07196bd945433e82e4788a32585f22604c6b8b7834 | JSP-000550 "Must two disjoint equal-length intervals of consecutive integers have different least common multiples?": **Current status: Open**, **Lean proof: No**, Eligible to claim: No, Publication details empty. No verified ranges listed. |
| problem page | https://www.erdosproblems.com/677 | 2026-11-07T09:20:32Z | 200 | 837f45777da64c53a1cd319f3df5173968d686c0e3c7ae8f310b5def282bc6de | Open (no solved marker). "This page was last edited 30 September 2025." Proof claims (0), proof expositions (0), Comments (8). Only the Thue–Siegel finiteness remark for fixed k. No verified ranges. Apart from the "accessed" date, the e-mail obfuscation token and the Cloudflare ray id, this is the same as the run's copy source/erdosproblems_677.html. |
| forum thread | https://www.erdosproblems.com/forum/thread/677 | 2026-11-07T09:20:32Z | 200 | 27734c68eb1109f9f73a2a5243889d7852d47b0cb804079bbd888ffc05a73c9c | 8 posts dated 31 Mar to 2 Apr 2026. Topics: the qrdlgit/erdos677 Aristotle Lean repo (finiteness for fixed d and k only), the Farhi–Kane lcm paper, and extra examples of the *unequal-length* equation M(n,k)=M(m,l) (M(8,4)=M(43,2), M(153,3)=M(1363,2)). No verified range for equal k. "The ability to post new comments has been suspended." |

All three status sources could be read. Saved bytes and the log are in ../panel_work/novelty/fetch/ and ../panel_work/novelty/fetch_log.txt.

## 2. What I searched and what I found

**arXiv API** (export.arxiv.org, sorted by date; window from 2024-11-07). My first five queries went to the http:// endpoint, could not resolve the host, and returned nothing. I sent them again over https, plus four more, so there were nine https queries:
- `all:"least common multiple" AND all:consecutive AND all:Erdos`
- `all:"Erdos problem 677"`
- `abs:"least common multiple" AND abs:"consecutive integers"`
- `all:lcm AND all:"consecutive integers" AND all:equal`
- `abs:"Erdos problems" AND abs:computational`
- `ti:"least common multiple"`
- `abs:lcm AND abs:consecutive`
- `abs:Erdos AND abs:"least common multiple"`
- `abs:"Erdos problems" AND abs:verification`

Inside the window there are no hits on Erdős 677 or on equal lcms of disjoint equal-length blocks. The only hits were off-topic: lcm of polynomial values, Pascal rows, covering systems, random lcms, Garside monoids, divisor Nim, and Erdős #272. Phrase queries on abs: returned weak zeros, as another source (plasma-ai wiki) also noted.

**Code search** (GitHub REST search/code and search/repositories). Queries: `erdos_677`, `lcmInterval 677`, `Erdos677`, `admissible_r lcm`, `deep_rig`, `search677`, `lcmInterval convergent`, and the repository query `erdos 677`. Two further phrase queries failed with a connection reset and were not retried. I cloned the relevant repositories and read them:
- **laaielichter/erdos-677** (2026-10-27): for 3 ≤ k ≤ 100, no solution with m + k ≤ 10^8; plus a proof of k = 3 (via Chan, arXiv:2408.01306). It has no tags, so it has no releases. **This is the strongest published finite verification for k = 26–28.**
- **MaxwellLaw/erdos-677-research** (2026-10-27): a complete k = 6 noncollision theorem (elliptic curves, certificates). Its prior-work audit cites:
  - Danesh–Bianchetti 2026 (IJMTT 72(9)), with a reported search of k ≤ 150, 0 ≤ n < m ≤ 150000;
  - trureturing PR #8768: N = 40000, k ≤ 24;
  - lean-genius: k = 1 and 2, and small-n k = 3;
  - formal-conjectures PR #2946: statement for m, n < 100 left as sorry.

  The repository has no tags. I could not fetch the Danesh–Bianchetti PDF (proxy 403, one attempt), so its range is known here only second-hand, with sha256 99f3db58… recorded by MaxwellLaw.
- **Kuberwastaken/c5-k4**: HOLD_BOUNDED, n, m ≤ 2·10^5 for k ≤ 12, and n ≤ 40 complete-in-m for k ≤ 24.
- **przchojecki/agentic-erdos**: n ≤ 1600 for k ≤ 10.
- **kavanaghpatrick/aristotle-math-problems**: a small search, k ≤ 20 with start ≤ 20000.
- **qrdlgit/erdos677**: Lean lemmas only; no tags or releases (the releases web page gave 403 once, and `git ls-remote --tags` shows none).
- **KDDavis91**: k = 5 visualisation.
- **plasma-ai/erdos** wiki, **dust-tt/srchd**, **conjectures-io**, **vibemathing**, **rjwalters/lean-genius**, **teorth/erdosproblems** (data/problems.yaml: 677 "open", last update 2025-08-31), and **formal-conjectures** 677.lean (fetched 2026-11-07T09:22:41Z, sha256 cc682a41…): statement and examples only, main theorem sorry.

None of these reaches k ≥ 26 beyond m + k ≤ 10^8.

**Prize repository PRs and claims** (GitHub search/issues):
- JSP-000550 PRs: #4846 (open; two closed arithmetic examples), #4288 (closed; the wrong problem, Erdős 550), #3543 (closed; elementary facts).
- Erdos677 PRs: #3298, #2582, #2412, all for JSP-000677 (another problem).
- JSP-000550 issues or Lean claims: 0.

**Kit repo** (remote https://github.com/elder-plinius/V3R1T4S; local HEAD 6bb0dcf equals the remote HEAD by ls-remote):
- TROPHY_CASE.md, known-knowns/ and the rest of the checkout contain no Erdős 677, JSP-000550, lcmInterval or lcm-blocks entry. "677" occurs only in the unrelated etp-finite-magma-677-255 and in data files.
- **PRs:** the GitHub API (gh REST and the github MCP tool) was refused for this repository: "GitHub access to this repository is not enabled for this session". So I could **not** read PR titles, bodies or open/closed state. What I did check:
  - `git ls-remote` lists 933 `refs/pull/N/head` refs (PR numbers 1–972). These cover open and closed PRs alike.
  - I fetched all 933 heads tree-only and listed every path each PR changes against its merge base with main.
  - No PR touches an Erdős 677 or lcm path. The only "erdos" families are erdos-699, erdos757, and the known-unknowns notes for erdos-617 and sunflower. PR 677 is a lottery bank target and PR 910 is etp-finite-magma-677.
  - No commit message on any fetched ref mentions Erdős 677, lcm blocks or JSP-000550.

## 3. Comparison

The cell is "Erdős 677 verified for k ∈ {26, 27, 28}". The neighbouring cells are other k and other n ranges.

**Best published object for this cell:** laaielichter/erdos-677, which has no solution with m + k ≤ 10^8. Add the trivial propagation rule from Lemma A(b) of object/PROOF.md: m + k ≤ (n+k)·R(k)^{1/k}, with R(k)^{1/k} = 2.221, 2.243 and 2.177 for k = 26, 27 and 28. The m-cap then lifts to "any m" only for n ≲ 4.4·10^7. Danesh–Bianchetti (m ≤ 1.5·10^5) and the other scans are weaker.

**Neighbouring cells:**
- k = 3 is fully proved (Chan; laaielichter).
- k = 6 is fully proved (MaxwellLaw).
- k ≤ 25 to 10^494 is the workspace's own earlier claim. It is not published in the kit repo or anywhere I found, so it is not prior art. In any case it does not cover k ≥ 26: a statement for one k does not transfer to another k under deletion, restriction, relabelling or symmetry.

**Trivial edits:** none of the edits (deletion, restriction, propagation, relabelling, symmetry, numerical polish), alone or combined, takes any published object from about 10^7 or 10^8 to 10^494 for k = 26–28.

**What the claim covers:** every n ≤ 10^494 and every m. This strictly contains every published covered set for these k, by about 486 orders of magnitude in n. It is not a tie.

**Provenance:** object/search677b.c calls itself a chunked version of the workspace's own search677.c. It is not laaielichter's search677.c: line-level similarity is 0.13 and the method differs (window plus G_k hash, not a p > 100 hash with sorting). The claim is not seeded from any published object. Its step-2 small-X range (n + k ≤ 1.1·10^6) is itself inside laaielichter's published range, but it is only a component of the proof.

**Caveats:**
- Novelty is judged against what is findable. GitHub search and arXiv phrase search are not exhaustive.
- The Danesh–Bianchetti and Farhi–Kane PDFs were blocked.
- I could not read kit-repo PR titles or states, only their changed paths and commit messages.

This verdict is on novelty only. It does not judge correctness of the computation.

novelty: the claimed range (26 ≤ k ≤ 28, n ≤ 10^494, any m) strictly exceeds every published or posted verification found (best: m + k ≤ 10^8 for k ≤ 100, laaielichter/erdos-677, 2026-10-27). JSP-000550 and erdosproblems.com/677 both read Open on 2026-11-07.

context: subagent (fresh context, Claude Code Agent tool)

pass: true
