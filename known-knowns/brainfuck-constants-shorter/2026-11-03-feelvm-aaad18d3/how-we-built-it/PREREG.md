# PREREG — brainfuck-constants-shorter (run 2, repair round 1)

Frozen 2026-11-03T19:46Z (from `date -u`) before this run's search output exists. This is a new PREREG for a
new run; it does not edit run 2026-11-03-0621's PREREG. The acceptance rule is unchanged from run 1 — same
criterion, same statistic — because the repair addresses the claim package (seed naming, prior-art record),
not the acceptance rule. No threshold depends on this run's results.

## Criterion (verbatim from bank/targets.json)

A Brainfuck string for some n listed on https://esolangs.org/wiki/Brainfuck_constants (re-fetched live
immediately before claiming) such that a reference interpreter with unbounded right tape, 8-bit cells (wrapping
only if claimed in the wrapping category), starting at all zeros, halts with the pointer on a cell holding n (mod
256 rules exactly as the page defines), never moves left of the start cell, and whose instruction count is
strictly less than the smallest listed count for n in that category (and for numbers > 255, the page's stated
cell-size conventions).

Partial win claimed: **over-255** — "A shorter program for one of the listed constants above 255."

## Table snapshot

Fetched 2026-11-03T19:45:41Z, HTTP 200, sha256
d78c05da7dbb20b80f70cceea943fdd429372ae6abfbb3fe810cc29471db0dd4 — byte-identical to run 1's snapshot. The
panel re-fetches once more at claim time; the cell must be unchanged.

## Statistic and acceptance test (fixed, same as run 1)

For the candidate program P and target n = 114514:

1. Instruction count = `len(P)` (all eight BF characters count).
2. Reference interpreter: unbounded right tape, zero-initialised, arbitrary-precision cells, pointer starts at
   0 and may never go below it, step limit 10^7.
3. PASS requires: halts; final pointer cell == 114514 exactly; pointer never < 0; `len(P) < 92` (the smallest
   listed value-in-cell count; also < 58, the smallest listed count of any kind).
4. Non-wrapping only; non-negative cells (MINCELL >= 0) for the category-exact claim.
5. One object per claim.

## Null design

`null_test: not needed because the claim is an explicit Brainfuck string checked by a deterministic interpreter
against a fixed table value — no search statistic, randomness or "beats chance" element is involved.`

The q-drift search that may produce a better object is a deterministic enumeration over a parameterised
family; its completeness is not claimed. If it finds nothing, the run-1 object (41 instructions) is the claim
object and nothing about the acceptance rule changes.
