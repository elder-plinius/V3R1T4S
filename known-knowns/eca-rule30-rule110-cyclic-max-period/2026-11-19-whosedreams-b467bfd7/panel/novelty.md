# NOVELTY skeptic verdict: A204371(37)=4403 is not a published exhaustive term
context: subagent

## Live status fetches (one request each, no retries; all HTTP 200)

Times below are America/New_York. Fetch instants are 2026-11-18 evening ET (UTC-5, EST). HTTP `Last-Modified` headers that arrived in GMT were converted to this zone.

| Source | URL | Fetched | Value read |
|---|---|---|---|
| A204371 b-file | https://oeis.org/A204371/b204371.txt | 2026-11-18 20:39:25 ET | HTTP 200, 282 bytes, sha256 `9237e577a1b8e6c74b30a2c2ee7c95e67b20f061fc22e230230f59b12ce41091`. Header: `# A204371 (b-file synthesized from sequence entry)`. 36 index lines, last `36 1584`. Index 37 absent. The string `4403` does not appear. |
| A204371 entry | https://oeis.org/A204371 | 2026-11-18 20:39:26 ET | HTTP 200, 18765 bytes. HTTP last-modified 2025-11-10 21:50:40 ET. Name: "Maximum period of cellular automaton rule 110 in a cyclic universe of width n." DATA has 36 terms ending `..., 2759, 2368, 1100, 969, 3920, 1584`. Links: "Table of n, a(n) for n=1..36." Comments: "a(n) >= A180001(n), and this sequence agrees with A180001 up to n=11." Keywords: nonn, hard, more. Author: Ben Branman, Jan 14 2012. Extensions: a(19)-a(36) from Lars Blomberg, Dec 24 2015. Status: approved. No `a(37)` and no `4403`. |
| A180001 b-file | https://oeis.org/A180001/b180001.txt | 2026-11-18 20:39:26 ET | HTTP 200, 8734 bytes, last-modified 2022-10-17 12:22:30 ET (EDT, UTC-4). 1000 index lines. Line present: `37 4403`. |
| A180001 entry | https://oeis.org/A180001 | 2026-11-18 20:39:26 ET | HTTP 200, last-modified 2025-11-10 21:50:39 ET. Name: "Eventual period of a single cell in rule 110 cellular automaton in a cyclic universe of width n." DATA lists 61 terms; the 37th term is 4403. Links: "Table of n, a(n) for n = 1..1000." This is the single-cell floor, not the maximum over all starts. |
| A204371 drafts | https://oeis.org/draft/A204371 | 2026-11-18 20:39:26 ET | HTTP 200. Page title "Draft edits for A204371". Visible text: "(No pending changes for A204371.)" No `a(37)` and no `4403`. |
| A204371 history | https://oeis.org/history?seq=A204371 | 2026-11-18 20:39:26 ET | HTTP 200. First page, "Showing entries 1-10", revisions #21 down to #12. Latest: #21 by Sean A. Irvine at 2025-11-10 21:50:40 ET, an https fix to the cellular-automata index link (`https://oeis.org/edit/global/3069`). Earlier first-page edits are link or crossref changes (2025-02-16, 2020-06-10) and Lars Blomberg's #12 of 2015-12-24 01:50:39 ET, the a(19)-a(36) extension, approved the same day. No revision on this page adds a(37) or mentions 4403. |
| Status source A334497 | https://oeis.org/A334497 | 2026-11-18 20:39:26 ET | HTTP 200, 17365 bytes, last-modified 2026-06-12 18:55:01 ET (EDT, UTC-4). Rule 30 companion sequence. DATA has 36 terms ending `2237472`. Links: "Table of n, a(n) for n=1..36." Extensions still end at a(23)-a(36) from Paolo Xausa, Jun 29 2023, using Gage, Laub and McGarry (2005), Table 2. No a(37). This page is the bank `status_source`; the claimed cell is A204371(37), which was also fetched, as above. |

The claimed term is not in the live A204371 entry, its b-file, or its public draft queue. The last published A204371 term remains a(36)=1584.

## Repo search (upstream public, read-only, no login)

- `TROPHY_CASE.md` in the pinned kit copy: no mention of A204371, A334497, A180001, or `eca-rule30-rule110-cyclic-max-period`.
- `known-knowns/`: no family folder for this target.
- `known-unknowns/graphs-games-automata/eca-rule30-rule110-cyclic-max-period.md`: the unsolved-target page, still worded as open as of 2026-10-30, with floor `A204371(37) >= 4403` and the requirement that the term not already be in the live OEIS entry at claim time.
- Public GitHub issue/PR search against `repo:elder-plinius/V3R1T4S`, 2026-11-18 20:40:19 ET, unauthenticated API, one request each: `A204371`, `A334497`, and `eca-rule30-rule110-cyclic-max-period` each returned `total_count: 0`. A fourth query, `4403 rule 110`, returned one closed draft, PR #110, a packomania spheres-in-cube submission whose title contains the radius digits `0.11024...`; it is not an ECA-period claim.

## Literature and related tables

- Wolfram, "Random sequence generation by cellular automata," Adv. Appl. Math. 7 (1986) 123-169, PDF `https://content.wolfram.com/sw-publications/2020/07/random-sequence-generation-cellular-automata.pdf`, fetched 2026-11-18 20:41:05 ET, HTTP 200. Rule 110 appears only as sample space-time pictures in Figs. 2.1 and 2.2, among other elementary rules. The cycle-length tables (Table 9.2 and Fig. 9.2) are for CA30 (Rule 30) and CA60; N=37 there is the Rule 30 entry 49276415, a value "found" for that rule, not a Rule 110 census. The string 4403 does not occur. This paper does not publish an exhaustive A204371(37).
- Gage, Laub and McGarry, "Cellular Automata: Is Rule 30 Random?" (2005), `https://homes.luddy.indiana.edu/dgerman/2005midwestNKSconference/dgelbm.pdf`, fetched 2026-11-18 20:41:25 ET, HTTP 200, last-modified 2006-01-13 23:51:27 ET. The paper is about Rule 30. Table 1 is a cumulative census for window sizes 5 to 24 under Rule 30. Table 2 is "Maximum cycle lengths ΠN found for cellular automata under Rule 30 for window sizes 4 to 36." Further research item (2) is to examine Rule 30 windows larger than 24. No Rule 110 maximum, and no 4403.
- OEIS A332717, "Triangle read by rows in which row n lists the possible eventual periods of cellular automaton rule 110 in a cyclic universe of width n," `https://oeis.org/A332717`, fetched 2026-11-18 20:41:25 ET, HTTP 200, last-modified 2023-07-21 23:31:46 ET (EDT). DATA has 73 terms; the last row is `1, 14, 21, 189, 315, 630`, which is width 21 (final term = A204371(21)=630). Keywords include `hard, more`. No 4403 and no row 37. Companion A332718 (row lengths) is listed only through n=21. This inventory therefore stops far short of width 37.
- MathWorld, Rule 110, `https://mathworld.wolfram.com/Rule110.html`, fetched 2026-11-18 20:41:25 ET, HTTP 200. Linked from A204371. It discusses the elementary rule and other OEIS sequences for the evolution of a single black cell (for example A075437). It does not give A204371, A180001, or 4403, and it does not state an exhaustive width-37 maximum.
- Wikipedia, Rule 110, `https://en.wikipedia.org/wiki/Rule_110`, fetched 2026-11-18 20:41:25 ET, HTTP 200, last-modified 2026-11-17 14:24:59 ET. No A204371, A180001, or 4403.
- Web and arXiv searches in this check (including 2024-2026) for an exhaustive Rule 110 cyclic maximum at width 37, and for A204371(37), returned the OEIS entries above and papers on other questions: asynchronism and period bounds under non-standard update schemes (arXiv:2505.10645), and Rule 110 universality or emulation, not a 2^37 census under ordinary parallel update. No paper or code listing found that states an exhaustive A204371(37).

## Framing: the value equals a known floor

The packaged claim in `object/a204371_37.txt` is `n=37`, `rule=110`, `max_period=4403`, `witness=0x1c7dbbb23e`. The number 4403 is already published as A180001(37), the eventual period of a single live cell, and A204371 itself records the inequality a(n) >= A180001(n). So 4403 was already a lower bound for this cell. A lower bound is not an exact term: it does not by itself prove that no other start has a longer eventual period.

The package states this directly. README.md, under "Not claimed," says that 4403 is not larger than the single-cell period, that it is equal to it, and that "the new work is the exhaustive census showing that no start has a longer eventual period." That is the right comparison. This is not a tie with a published A204371(37) record, because no such exhaustive term is listed. It is a proposed exact term that meets the known floor with equality.

## Findings

No published source reached in this check already gives an exhaustive value of A204371(37). The live OEIS entry and b-file still stop at n=36; there is no pending OEIS draft; the history page shows no post-2015 data extension; the single-cell sequence A180001 supplies only the floor; Wolfram (1986) and Gage et al. (2005) do not census Rule 110 at width 37; A332717's period inventory stops at width 21; and the upstream V3R1T4S trophy case, known-knowns tree, and public pull requests contain no prior claim for this target.

Novelty therefore turns on the exhaustive upper bound, which is not already in the public record, not on a cycle longer than the known single-cell orbit.

## Caveats

A private note, an unindexed mailing-list post, or an OEIS draft submitted after 2026-11-18 20:39:26 ET would not be visible here. The history page was read only as first-page entries 1-10 (revisions #21 through #12, 2025 back to the 2015 data extension); older revisions are earlier still and cannot be a later a(37). This review did not re-run the 2^37 search; that is outside the novelty question.

pass: true
