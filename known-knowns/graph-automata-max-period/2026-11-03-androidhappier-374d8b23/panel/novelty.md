# NOVELTY skeptic — A357951(8) = 150
context: subagent (novelty skeptic, isolated claim copy)
claim copy: [scratch]/panel0236-novelty (cp -a of runs/2026-11-03-0236/claim); only claim.md, table_record.md, REPRODUCE.md read. No attempts/, NOTES, REPORT, other panel files or packaging scripts read.
cell: A357951(8) (outer-totalistic, connected graphs). NOT the bank sibling A384209 (Life on simple graphs).

## Primary table fetch (single attempt, no retries)
- URL: https://oeis.org/search?q=id:A357951&fmt=text  (status_source https://oeis.org/A357951)
- UTC time: 2026-11-03T04:15:37Z (Nov 2, 2026, 11:15 PM EST)
- HTTP status: 200
- sha256: e8e8bfa7c8a4953334164e23d561e02541c275663e8a984b7640e62d5578b302 (byte-identical to the claim-time fetches at 02:36:55Z and 02:50:41Z)
- %I A357951 #11 Oct 23 2022 13:42:18
- %S A357951 2,2,4,6,16,26,66   -> ends a(7)=66, no a(8)
- %K A357951 nonn,more,hard
- Draft: https://oeis.org/draft/A357951, 2026-11-03T04:15:37Z, HTTP 200, "No pending changes for A357951."
- Saved: [scratch]/panel0236-novelty/oeis_novelty.txt, [scratch]/panel0236-novelty/draft_novelty.html

## GitHub PR / code search
- elder-plinius/V3R1T4S PRs (open+closed) for "A357951": 1 hit, #904 (open draft, CharanRayudu, created 2026-11-02T18:47:50Z): "[claim] graph-automata-max-period: A384209(10) = 46". That is the SIBLING cell. Its body and README say: "A384209(11) and the related sequences A357951, A357952 and A357953 are not claimed." Its 56 changed files only mention A357951 in credits/criterion quotes and contain no A357951(8) value.
- PRs for "graph-automata": 28 hits. Only #904 is on this target. The rest are other bank targets (subtraction games, Langton ant, etc.).
- PRs for "outer-totalistic", or for GCQfBg / A357952 / A357953: no claim on A357951 (only #904 again).
- GitHub-wide code search "A357951": 373 hits. The only real ones are V3R1T4S bank files (known-unknowns/graphs-games-automata/graph-automata-max-period.md, README.md). The rest are substring noise (password lists, pbxproj, etc.). No repo states a(8).
- GitHub-wide code search for the witness "GCQfBg": 262 hits. All are generic lists of every 8-vertex graph (graph8c.g6 etc.), and none is tied to automata or periods.
- Local repo origin/main (9a0d19a, 2026-11-02T13:14:05Z): no A357951 term in known-knowns/, news/ or sealed-envelopes/.

## TROPHY_CASE / known-knowns
- TROPHY_CASE.md (origin/main): no line for graph-automata / A357951 / A3579xx / A384209.
- known-knowns/: there is no graph-automata-max-period directory on origin/main. (PR #904 would add one for A384209(10) only.)

## Literature, last 24 months (Nov 2024 – Nov 2026)
- OEIS A357951 (Pontus von Brömssen, 2022) is still the only source of the terms, and it gives a(1..7) only. The OEIS wiki page of P. von Brömssen lists A357951 with no further terms.
- Web/arXiv: nothing gives a(8). Marr–Hütt arXiv:0812.2408 (2008) is about a different question. arXiv:2406.01710 (Koller–Behrens–Zdeborová) covers fixed points on random regular graphs, not max periods. arXiv:2607.10453 (Pulse Graphs, Jul 2026) uses a different rule class on directed graphs. None of them reports the maximum outer-totalistic period on connected 8-vertex graphs.
- Sanity check: the claimed 150 is at least the sibling a(8) values A357952(8)=112 and A357953(8)=96. This fits the OEIS formula a(n) <= A357951(n), so it does not conflict with known data.

## Verdict
No known source (live OEIS DATA/draft, V3R1T4S PRs open or closed, TROPHY_CASE, known-knowns, GitHub code, or literature from the last 24 months) gives any value for A357951(8). The claimed term is new. It is not a tie with a known value.
novelty: NEW (a(8) absent from live OEIS at 2026-11-03T04:15:37Z)
pass: true
