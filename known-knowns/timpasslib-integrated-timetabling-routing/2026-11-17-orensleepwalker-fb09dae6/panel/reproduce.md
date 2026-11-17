# Reproduce panel report

context: fresh Claude Code subagent started by the run's lead agent with only this brief; read only claim/ and public pages (workspace notes auto-inserted into context, if any, were ignored).

## Method
Wrote my own evaluator (work-reproduce/lib/ev.py, Python 3 stdlib) from claim/REPRODUCE.md before opening claim/provenance/. Provenance was opened only afterwards, for comparison.

## Definition implemented (quoted from claim/REPRODUCE.md)
- "Feasibility: for every activity (i -> j, bounds L and U) the periodic duration d = ((time_j - time_i - L) mod T) + L must satisfy d <= U. Every event must appear exactly once." Times in {0..T-1}.
- "Objective: for every OD pair, the cheapest path from ANY departure event at the origin stop to ANY arrival event at the destination stop, using only drive, wait and change activities as arcs; an arc costs its periodic duration d, and a change arc costs d plus ean_change_penalty. Sync and headway activities carry no passengers. Total = the sum over OD pairs of customers times that cheapest path cost."
Implementation: multi-source Dijkstra from all departure events of each origin, minimum over arrival events of the destination. Config: T=10, ean_change_penalty=5.

## Results (real output)
```
Hamburg-140850920-Timetable.csv (140850920, 9694166, 0) []                      <- reproduces posted best exactly
Timetable.csv (140833625, 9694166, 0) []                                         <- object/Timetable.csv
141610697_Timetable_Loebel_Lindner_2025.csv (141610697, 9694166, 0) []
LBRTimetable_Schiewe_Goerigk_Lindner_2023_141629305.csv (141629305, 9694166, 0) []
```
(tuple = total, passengers routed, passengers unreachable.) All four feasible, all 508 events present once, times in 0..9. Object total 140833625 = claimed; 17295 below 140850920. Two repeated runs of the object gave identical output (deterministic).

Live page (curl of solutions.html, one fetch): the Hamburg row lists 140850920 first (B. Ramos, 31.08.2026), then 141610697, then 141629305; the only 14[01]xxxxxx totals on the page are those three. So object 140833625 < 140850920.

Instance files: Hamburg.zip downloaded from the live site (namelist: Activities.csv, Events.csv, OD.csv, Config.csv; extracted only these into work-reproduce/zipdl/x/). Byte comparison with claim/references/instance/:
```
Config.csv True / Events.csv True / Activities.csv True / OD.csv True
sha file (instance_files.sha256) Config/Events/Activities/OD: all True
```

## Negative tests (copies in work-reproduce/neg_*.csv)
```
orig         (140833625, 9694166, 0) 0 errors
outofrange   rejected: time out of range 1=10
negtime      rejected: time out of range 1=-1
missing      rejected: missing event 7
dup          rejected: dup 7
lineshift    rejected: 487 violations (act 1 d=10 U=4, ...)
fixedbreak   rejected: act 1 (drive 4..4) d=5 U=4, act 2 d=9 U=0
random single-event moves (50, seed 1): rejected 50/50
```
Global cyclic shift by c=1..9 (mod 10): all feasible, total 140833625 unchanged every time.

## Comparison with provenance (after the above)
provenance/logs/batch_independent_scores.txt reports 140833625 for H01,H02,H04,H05,H06 and 140850920 for others; consistent with my numbers. No mismatch found. Not examined: search code correctness (irrelevant to the checked properties); optimality is not claimed.

## Mismatches
None.

pass: true
