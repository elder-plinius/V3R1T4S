# Novelty skeptic: A357953(9) = 180

context: subagent (novelty skeptic, isolated claim copy)

Claim: A357953(9) = 180, witness graph6 `H?`DBbS`, rule {0,2}, start 175.
Inputs read: the isolated claim copy only (claim.md, table_record.md, REPRODUCE.md), plus the public web and GitHub.

## 1. Live status fetch (one fetch, no retries)
- URL: https://oeis.org/search?q=id:A357953&fmt=text
- Time: 2026-11-02T20:50:20Z (3:50 PM EST, UTC-5)
- HTTP 200
- Header: `%I A357953 #13 Oct 24 2022 14:14:10`; this is the same revision the scout fetched at 09:58:53Z.
- `%S A357953 1,2,2,6,7,18,38,96`: DATA still ends at a(8) = 96 (offset 1). Keywords nonn,more,hard.
- 180 does not appear anywhere in the entry. The only b-file is the auto "Table of n, a(n) for n=1..8". No a(9) is in the examples.
- Draft check: https://oeis.org/draft/A357953 returned HTTP 200 with "No pending changes" at about 20:50Z.

## 2. Repo, TROPHY_CASE, known-knowns, PRs
- Local repo HEAD f3b19b4 (2026-10-30): TROPHY_CASE.md and known-knowns/ have no mention of A357953, A357951, A357952, A384209, `DBbS` or "totalistic". The only hits are the bank entry (bank/targets.json, known-unknowns/graphs-games-automata/graph-automata-max-period.md), which lists A357953 as open for n <= 8, a(8) = 96.
- I searched GitHub issues and PRs in elder-plinius/V3R1T4S, open and closed. "A357953" gives 1 hit, "A384209" gives 1 hit, and "graph-automata" gives that same PR among its results. That PR is #904 (open), "[claim] graph-automata-max-period: A384209(10) = 46". Its object/VALUE.txt is A384209(10) = 46 only, using Life rule programs lifeA/lifeB. It does not cover A357953(9).
- "DBbS" gives 0 hits. "totalistic" gives 0 hits.
- The GitHub code search API needs auth, which is not available on the box. I used the unauthenticated issue/PR search and PR file listings instead.

## 3. Literature, last 24 months
- Web searches for A357953, "totalistic cellular automaton connected graph maximum period", and 9 nodes / 180 found only the OEIS entries A357951/2/3, von Brömssen's OEIS wiki page, and unrelated older papers (Marr–Hütt 2008, J. Phys. A 1997, an ICALP 2024 logic paper).
- None of them gives a value for A357953(9).

## 4. Comparison with this cell and neighbouring cells
- This cell, A357953(9): unpublished. Live data stops at a(8) = 96, and 180 is a new term rather than a tie or a re-derivation. The values grow 18, 38, 96, 180 (ratios about 2.1, 2.5, 1.9), which is plausible.
- Neighbouring cells:
  - A357952(9) (counts the node itself): unpublished. Live data ends at a(8) = 112.
  - A357951(8) (outer totalistic): unpublished. Live data ends at a(7) = 66.
  - A357951(9), the formula upper bound a(n) <= A357951(n): unknown, so it does not conflict.
  - A384209(10) = 46: a different sequence (Life rule on simple graphs), packaged in PR #904.
- No published object gives this term through a trivial edit. Adding a node to the n = 8 witness G?CidW cannot certify a maximum over all 9-node connected graphs. The exhaustive enumeration claim is what makes the term exact, and correctness is the other panelists' check.
- Novelty caveat: this verdict is on novelty only. It assumes the exhaustive-max claim is correct, which is the soundness and reproduction panelists' job.

Verdict: 180 at n = 9 is strictly beyond everything known. The live OEIS entry, its draft, the repo trophy case and known-knowns, open and closed PRs, and the recent literature all stop at a(8) = 96.

pass: true
