# Novelty review (Hamburg, TimPassLib, 140,833,625)

context: fresh Claude Code subagent started by the run's lead agent with only this brief; read only claim/ and the public web (gh, curl); no workspace notes were used.

## Fetched
- https://timpasslib.aalto.fi/solutions.html, fetched once, 2026-11-17 08:33:03 UTC (date -u), HTTP 200. Hamburg rows: 140850920 (31.08.2026, B. Ramos), 141610697 (01.09.2025, F. Loebel, N. Lindner), 141629305 (31.01.2023, Schiewe/Goerigk/Lindner), lower bound 139892927. Best listed = 140,850,920, matching the claim. No note or other bound on the page.
- Link check, one request each (08:33:11 UTC): data/Hamburg/12239162_Timetable.zip -> 404; data/Hamburg/141610697_Timetable.zip -> 200. Authors' statement confirmed (the page's link is a typo).

## Searched
- OpenAlex (TimPassLib, integrated periodic timetabling + passenger routing, since 2024-11): only the 2023 TimPassLib paper, the tropical Dijkstra paper (2025), compact cycle formulation MESP, column generation for periodic timetabling (2025), and unrelated integrated-timetabling papers. None reports a Hamburg total in the abstract metadata. Full texts not read.
- Semantic Scholar: HTTP 429, no result. arXiv API query returned nothing relevant in the lines I viewed.
- Loebel/Lindner ATMOS 2025 PDF: downloaded (HTTP 200) but I had no PDF text tool, so I could NOT read it. Its Hamburg value is represented on the status page as 141,610697 (2025 row), which I take as its reported total.
- GitHub: gh code/repo search for TimPassLib / "TimPassLib Hamburg": no hits. V3R1T4S PR and issue searches (timpasslib, PESP, passenger routing, Hamburg, timetabling; open and closed): nothing relevant (only unrelated issue #1092, an exam-timetabling item). TROPHY_CASE.md: no match for timpass/pesp/hamburg/timetabl. known-knowns/: no matching entries. V3R1T4S releases: only one, unrelated. Zenodo search "timpasslib": no relevant record shown (output empty).
- Result: I found no public value or timetable for Hamburg at or below 140,833,625. Not exhaustive (no 2026 full-text search, ATMOS PDF unread, Semantic Scholar blocked).

## Own distance computation (stdlib python, T=10, best global shift, compared per event id)
```
posted 508 events shift 2 differ 285 (56.1%) lines [1,2,3,5,6]
2025   508 events shift 5 differ 284 (55.9%) lines [1,2,3,4,6,7]
2023   508 events shift 7 differ 280 (55.1%) lines [1,2,3,4,5,7]
```
Matches claim/provenance/distance_to_published.txt exactly. All three exceed half of events.

## Trivial-edit analysis
- Not a global cyclic shift image of any published timetable (about 55% of events differ after the best shift). Not a restriction, deletion, or relabelling (same 508 events, ids as in the instance). No evidence of a propagation rule or local numerical polish: a polish would change few events, not 280+.
- Weak point: a time reflection or per-line shift symmetry image was not tested by me beyond the global shift; a per-line shift is not a general symmetry (it changes transfer durations), a reflection changes activity bounds, so I do not consider these likely.
- The roughly equal distance (~55%) to all three published objects suggests the object sits in a region sharing structure with the known solutions yet is far from each; consistent with LNS from the 2023 start, not with an edit of one.
- Gain over published best: 17,295 (0.0123%), tiny but strictly below the best; no tie.
- Seeding disclosure (provenance/README.md): names the 2023 timetable as the seed, the intermediate 140,833,937 run, batch H04, and states that jobs started from the posted best found nothing. Disclosure is adequate and honest; it also says the evaluator is withheld, so the total itself is for the other skeptics to verify (I did not recompute the total).

## Verdict
Novelty-wise, as far as I could check, the object is not matched by any public value or timetable, is not a trivial edit of the three published timetables, and its seed is named. Residual risk: unread ATMOS 2025 PDF and no full 2026 literature sweep. I confirm novelty relative to the status page and the sources searched, with these limits.

pass: true
