# Novelty skeptic verdict: A384209(10) = 46 (target graph-automata-max-period)

context: subagent (executor, novelty)

## Status fetch (one plain curl GET per page, UA 'V3R1T4S-research-agent', no retries, no cookies)

| URL | UTC time | HTTP | sha256 | value |
|---|---|---|---|---|
| https://oeis.org/search?q=id:A384209&fmt=text | 2026-11-02T09:29:55Z | 200 | a2d2fe9c9ff2aab776502142000c0bd3bc4d5b2e120022d1679f0990a8c84247 | `%I A384209 #8 May 22 2025 09:53:28`; `%S A384209 1,1,1,1,2,4,8,14,27`; `%K nonn,more`; `%O 1,5`. No a(10). |
| https://oeis.org/draft/A384209 | 2026-11-02T09:29:55Z | 200 | 518047aa1ec41926179b58b6dda51d1404492476ce8411ae6b15061c38d88e82 | "(No pending changes for A384209.)" |
| https://oeis.org/A384209/b384209.txt | 2026-11-02T09:29:55Z | 200 | dbedf511d065d663017975cf76560c8d0384e44e6d301b61018b829091b19423 | "b-file synthesized from sequence entry", last line `9 27`. |

The text-format sha256 is the same as the scout's copy fetched 2026-11-02T09:21:21Z, so the entry has not changed since then (revision #8, May 22 2025).
The entry's own example table gives unique optimal graphs for n = 5..9 (D]{, E]yw, FE~vw, GEnvZ{, HCZJtzm), and there is no n = 10 graph.

## Search (last 24 months and beyond)

- Pinned repo copy (TROPHY_CASE.md, known-knowns/, bank/): A384209, A35795x and graph-automata appear only in the bank entry graph-automata-max-period (bank/targets.json), which states "known for n = 1..9". TROPHY_CASE.md has nothing on it. known-knowns/ only has unrelated "life-smaller-orphan" charter lines.
- GitHub PRs in elder-plinius/V3R1T4S (open and closed): I searched for A384209 / graph-automata / A357951-3 / "Game of Life" / "max period" / automata. There are 27 and 32 hits, all on other targets (subtraction games, Langton ant, etc.). None is a claim on graph-automata-max-period. A GitHub-wide PR search for "A384209" returned 0.
- GitHub code search "A384209": the only relevant hits are elder-plinius/V3R1T4S known-unknowns/graphs-games-automata/graph-automata-max-period.md (says "open as of 2026-10-30", n = 1..9 only) and loda-lang/loda-programs oeis/384/A384209.asm (lists only 1,...,27). Code search for the witness string "I?zUvYujw" returned 0.
- Web/arXiv/SeqFan/OEIS wiki: the OEIS entry, its internal format, the OEIS wiki page of Pontus von Brömssen (lists A357951-A357953 and does not give a 10-vertex Life term), arXiv 2111.01780 (Krechetov, a different rule measuring "complexity" and not the max period), arXiv 2312.02799 (omniperiodicity on the grid, which does not apply) and Wanless 1997 (graph games). None of these gives A384209(10) or a 10-vertex Life-on-graph period.
- Release assets: I found no repository dedicated to this sequence, so there were no assets to check.

## Comparison with published objects and neighbouring cells

- Published neighbour a(9) = 27 (HCZJtzm). Trivial edits cannot produce 46:
  - Adding an isolated vertex to HCZJtzm, or relabelling it, leaves 27.
  - Disjoint unions of published optima give lcm of the published maxima: at most 27 (9+1), 8 (7+3), 4 (6+4), 2 (5+5).
  - Deletion or restriction can only reach terms with n <= 9.
- The witness I?zUvYujw is a connected graph: 10 vertices, 27 edges, degrees [3,4,4,6,6,6,6,6,6,7]. My own independent decode and step of graph6 from start 62 under B3/S23 gives a cycle length of 46.
- The claim does not say it was seeded from a published object. It comes from exhaustive geng enumeration.

## Contradictions

I found no published 10-vertex graph with a longer Life period, and no published a(10) at all.
One thing to note: LODA's A384209.asm has a fitted formula, a(n) = floor((2^(n-1)+C(n-1,3))/12)+1, that matches n = 1..9 and would extrapolate to 50 at n = 10. It is a machine-mined fit to 9 terms, not a computed or published value. It has no witness, so it is not evidence against 46. It does mean the "and only 46" upper half rests entirely on the exhaustive enumeration, which is outside the novelty remit.

## Verdict

At 2026-11-02T09:29:55Z, a(10) is absent from the live OEIS entry and its draft, and I found it nowhere else (repo, PRs, GitHub code, literature). On novelty, 46 would be a new exact term that strictly beats everything known, with nothing tying it. This verdict covers novelty only. Correctness of the exhaustive enumeration is for the other skeptics.

pass: true
