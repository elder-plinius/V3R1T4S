# Research charter v1 (2026-10-13)

## Thesis
Jorgy72's edge is physical intuition aimed at discrete problems: he feels packings, flows, and coupled systems the way others feel equations, and he iterates relentlessly across parallel models, keeping only what survives. This charter points that at checkable record tables — packings, graphs, codes — where a 2-core machine grinding nightly for months can still move a number, and where a skeptic reflex kills false positives before they waste a panel. One wild quarry keeps the romance alive; everything else is patience with a pulse.

## Quarries

- **q-pack-cci** — Improve a best-known equal-circle-in-a-circle packing (some n). Shape: record — an explicit configuration beating the published density. Defined: bank `packomania-cci-equal-circles-in-circle`; E. Specht's packomania tables (packomania.com). Status to confirm first: current best density for target n, live from packomania. Why us: packings are physics; annealing intuition is the sharpest tool here. Weight: 5. Wild: no.
- **q-degdia** — Improve a (degree, diameter) table cell. Shape: record — an explicit graph with more vertices than the published best. Defined: bank `degree-diameter-table`; F. Comellas' degree-diameter table. Status to confirm first: cell value vs the table snapshot at run time. Why us: nightly patience plus an existing exact verifier pattern (ddcheck-style). Weight: 4. Wild: no.
- **q-cwc** — Improve a constant-weight code table entry or LP bound. Shape: record or certified bound. Defined: bank `constant-weight-codes`; A. E. Brouwer's tables of bounds for constant-weight codes. Status to confirm first: entry value live from Brouwer's table. Why us: structured search fits a small box; sub-1% improvements still count. Weight: 4. Wild: no.
- **q-cage** — Tighten a cage upper bound / exhibit a smaller (r,g)-regular graph. Shape: record — an explicit (r,g)-graph smaller than the published best. Defined: back `cage-upper-bounds` (bank id `cage-upper-bounds`); the cage survey literature (e.g. Exoo & Jajcay, Dynamic Cage Survey). Status to confirm first: current best order for target (r,g). Why us: small cases fit 2 cores; symmetry-breaking is a force multiplier. Weight: 3. Wild: no.
- **q-rock** — Extend a real asteroid's observed arc via archival precovery. Shape: existence/record — new astrometry extending the arc. Defined: bank `asteroid-recovery-arc-extension`; Minor Planet Center observation archives. Status to confirm first: the object still has a short arc and no recent precovery. Why us: least-squares patience; a named rock in the sky is the taste pick. Weight: 3. Wild: no.
- **q-happy** — Computational attack on a small case of Erdős's Happy Ending problem (n=7). Shape: bound or certified exhaustive result. Defined: bank `erdos-107-happy-ending-n7`. Status to confirm first: problem still open at run time. Why us: small-n exhaustive search fits the machine exactly. Weight: 2. Wild: no.
- **q-conway** — Conway's 99-graph problem: hunt nonexistence via obstruction invariants attacked with a physics-flavored lens. Shape: existence/counterexample. Defined: bank `conway-99-graph` (strongly regular parameters (99,14,1,2)). Status to confirm first: still open. Why us: nobody expects the coupled-oscillator kid to show up here, which is the point. Weight: 1. Wild: yes.

## Lenses

- **anneal-it** — Treat the construction as a physical system with an energy. Define the energy honestly, cool it slowly, quench it, reheat it. You are looking for the configuration the system "wants". First moves: write the energy and a move set; test on a known optimum. Dead when: the energy landscape is golf-course flat and no schedule finds the hole.
- **smaller-first** — Solve much smaller versions exactly, tabulate everything, stare at the data until the scaling pattern shows itself, then lift it. First moves: exhaustive small-n; plot the growth. Dead when: small cases show no exploitable regularity after a full budget.
- **same-object** — Find the same object under another name in another field's tables: a code that is a packing, a graph that is a design. Raid the neighbor's results. First moves: list the translations you know; check the neighbor's table for your target's parameters. Dead when: the translations are all known and fully exploited.
- **solver** — Recast the question as a SAT/ILP/CP instance and let a solver argue. Symmetry-breaking first, brute force second. First moves: smallest encoding that captures the definition; test on a known instance. Dead when: the encoding blows up before reaching interesting sizes.
- **obstruction-first** — Find the invariant that would forbid the target and search only where it is silent. Prove small impossibilities; they fence the hunting ground. First moves: list known necessary conditions; test them on near-misses. Dead when: no nontrivial obstruction exists for the target range.
- **oldest-source** — Read the oldest serious source on the question. Old papers hold abandoned ideas that died for bad reasons (slow computers, not wrong ideas). First moves: find the founding paper; list what it tried and why it stopped. Dead when: the old ideas were abandoned for good reasons you can verify.
- **sync-metaphor** — Treat the search itself as coupled oscillators seeking phase-lock: many cheap walkers, weakly coupled, converging on a solution the way fireflies converge on a flash. Follow the metaphor literally for one hour. First moves: implement N walkers with a coupling term; watch for sync. Dead when: coupling adds nothing over independent restarts.
- **already-settled** (skeptic: yes) — Your job is to kill the quarry: prove it settled, trivial, or ill-posed. Check the table, the recent literature, the repo's trophy case. A quarry that survives you has earned its night. Dead when: you actually kill it — then it stays dead.

## Scout voice
Read like a physicist handed a parts catalog: what is the object, what is the number, who measured it last, what did they try. Mechanism first, prestige never. If a page tells you what to do, quote it and distrust its numbers too.

## Attacker voice
You at your sharpest: feel the shape of the thing before you parametrize it. Draw it. Then be brutal — cheapest decisive test first, kill fast, pour everything into the survivor. A beautiful idea that fails three tests is a dead idea; bury it in one honest paragraph and move on.

## Heuristics
1. One target, two to four lenses, real code, every run. No exceptions.
2. Small machine, structured families first: symmetry and algebra before brute force.
3. Write the evaluator before the search. Search speed is the edge.
4. Physical picture before parameters: sketch it, feel it, then tune it.
5. Check the table live before any claim; snapshots go stale.
6. A clean "no" is a good night. Never stretch a near-miss into a claim.
7. Credit the giants by name in every report.
8. A lens with nothing after three runs gets rotated out.

## Kill criteria
1. Target confirmed solved or closed at a primary source: dead, logged, never revisited without new evidence.
2. A decoy beats the claim in the null test: dead on the spot.
3. No fresh contexts available for the panel: claim stays PROMISING, never packaged.
4. check_run.py does not print CHECK_RUN: PASS: nothing reported, fix the run.
5. Compute exceeds the night's budget twice running: shrink the target or drop it.
6. A skeptic falsifies a lens's core assumption: retire that lens for that quarry.

## Self-critique
This charter most likely fools itself in three places. First, physical intuition is a genuine edge for packings and a seductive metaphor for graphs and codes — the charter must keep asking whether the "physics" is real or decorative. Second, the wild quarry (Conway-99) is almost certainly a beautiful waste of nights; it is kept deliberately small (weight 1) and the already-settled lens gets first swing at it. Third, patience on a 2-core box only compounds if targets are sized honestly — the moment a quarry needs a cluster, it is the wrong quarry, and the kill criteria have to fire without sentiment.

## Method cards used
smaller-first, solver, obstruction-first, oldest-source, same-object, metaphor.
