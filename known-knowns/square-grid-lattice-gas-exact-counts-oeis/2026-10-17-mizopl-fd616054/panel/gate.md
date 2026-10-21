# Honesty gate (step 7)

The run's main session read all three panel files (`panel/reproduce.md`, `panel/novelty.md`,
`panel/criterion.md`) and the self-break (`how-we-built-it/break.py`).

Downgrade triggers checked (RUN.md step 7): no hedging panelist; no reproduction mismatch
(REPRODUCE and CRITERION each independently recomputed all 23 n=15 residues from scratch and
both CRT to the claimed value); the value strictly extends the live table (NOVELTY: A054759
b-file HTTP 200 at 2026-10-17T13:01:03Z, largest index 14, index 15 absent, no prior
publication); no stretched criterion or hidden quantifier (the growth clause is reported
literally and openly, and p1 names only the two-run and reproduction rules); scope not wider
than reproduced; no sample-as-complete (full recomputation, not spot checks); no probable
prime as proof; no table value obtained by evasion (one honest curl, HTTP 200); one object,
one cell (a(15)). Panel table fetch is < 6 h old (minutes), no re-fetch needed.

The three panel verdicts are pass: true, pass: true, pass: true.

status: CONFIRMED_PARTIAL
confirmed_scope: A054759(15) = 4310182149988584261406143524214457416387448 is confirmed under p1's two-run rule (two agreeing runs with disjoint prime sets and different decompositions: forward+closed-form vs reversed-encoding+explicit-walk, both independently recomputed) and reproduction rule (method reproduces all published terms n=1..14 exactly, and the Eulerian-orientation definition is confirmed by brute force for n=1..3); the main criterion's 1e-3 growth clause is not met at n=15 (gap 0.0074, and the published a(14) also fails it) and is not part of p1.
