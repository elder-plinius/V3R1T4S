# Replay of all 800 controls

context: fresh Claude Code subagent started by the run's lead agent with only this brief; read only claim/ and ran its frozen code in a copy

## What was run
- `sha256sum -c SHA256SUMS` inside claim/: every listed file reported OK (all entries, including both control logs).
- Copied claim/ to a work copy; moved output/dialogues-payload-controls.jsonl and output/dialogues-first_order-controls.jsonl out of the copy's output/ (kept as saved/ for comparison), so that all seeds were recomputed.
- Commands in the copy (OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1, NumPy venv python), two processes in parallel (code has no parallel option; one process per mode):
  - `python code/controls.py dialogues payload` (default --n 400, seeds 310000..310399)
  - `python code/controls.py dialogues first_order` (default --n 400)
- Start 2026-11-18 09:07:56 UTC (payload; first_order started about a minute later). End: payload 09:13:43 UTC, first_order 09:14:39 UTC. Runtime about 311 s (payload) and 298 s (first_order) of compute. Both ran to 400/400 checkpoints.
- Problem noted: my first launch of first_order raced the copy step and failed immediately (no directory); it was simply restarted. No effect on results.

## Comparison (recomputed vs saved logs, seed by seed)
- Payload: 400 seeds recomputed, same seed set 310000..310399 as saved log; all numeric fields (including changed_fields, targets, groups, bits, gains for all 5 model families) identical. Largest absolute difference: 0 (exact equality).
- First_order: 400 seeds, same seed set; all fields identical. Largest absolute difference: 0.
- Seeds reproduced: 800 of 800. Seeds that differ: none.

## Maxima and counts (recomputed; identical to saved)
Observed gains for reference: 0.230409564 over baseline, 0.286580809 over twin.

| control set | max selected gain over baseline | max selected gain over twin | seeds >= observed over baseline | seeds >= observed over twin |
|---|---|---|---|---|
| payload | 0.200664285 | 0.256013480 | 0 of 400 | 0 of 400 |
| first_order | 0.095298456 | 0.160037978 | 0 of 400 | 0 of 400 |

## Any-family sensitivity (largest twin gain over selected, order2, order3, repetition, timing per seed)
- Payload: 5 of 400 seeds reach or exceed 0.286580809; maximum 0.318323143. Agrees with the authors' 5 of 400 and 0.318323143.
- First_order: 0 of 400 seeds reach 0.286580809; maximum 0.199329911.

## Result
All 800 stored control results are reproduced exactly. The frozen selector's gains stay below the observed gains in every seed in both sets. The any-family sensitivity matches the authors' reported figures. Limit: this replays the author code for the controls (as REPRODUCE.md describes); it is not an independent re-derivation of the evaluation.

pass: true
