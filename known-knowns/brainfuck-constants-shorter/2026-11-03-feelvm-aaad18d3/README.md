# Brainfuck constant 114514 in 41 instructions

## What

The 41-instruction program object/program.bf, started from all zeros, halts after 305379 steps with the pointer on cell 1 holding exactly 114514, never moves left of cell 0, never holds a negative cell, and 41 is strictly less than every instruction count listed for 114514 on the live esolangs Brainfuck constants page (58, 78, 92 numbered, plus unnumbered BF-RLE and CESU-8 blocks), literally satisfying the over-255 partial win for this one constant.

(The sentence above is the claim panel's confirmed scope, quoted word for word from panel/gate.md.)

## Check it yourself

From this folder, in a fresh shell with Python 3 (standard library only):

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. Rough time: a few seconds on a laptop (the interpreter runs the 305,379-step
program plus a corruption self-test).

Or just the object check:

```sh
python3 verify-it-yourself/checker.py object/program.bf 114514
# PASS len=41 value=114514 steps=305379 mincell=0
```

## Compared to

- Table: https://esolangs.org/wiki/Brainfuck_constants (esolangs wiki, CC0), section `114514`.
- Fetched 2026-11-03T19:45:41Z, HTTP 200, page sha256
  d78c05da7dbb20b80f70cceea943fdd429372ae6abfbb3fe810cc29471db0dd4 (page last edited 25 June 2025, oldid
  160357); re-fetched byte-identically by all three panel skeptics the same day (see the-record-we-beat/).
- The cell lists (92, 2) — the shortest listed sequence that leaves 114514 in a cell — plus (78, 4) and
  (58, 2), which print UTF-8 bytes rather than leave a value, and two unnumbered blocks (a BF-RLE form
  expanding to 1916 instructions, and a 468-instruction CESU-8 printer). The object's 41 instructions is
  strictly below every listed count: 17 below the smallest listed (58) and 51 below the smallest listed
  value-in-cell program (92).
- Object: `>++>+++>+++>+++>+>++>++>+[>+[-<++++>]<<]>` (41 bytes, sha256
  aaad18d3b875c2161656c60a353a587def4b40a74f8646f650e67f37ce38cf38).

## Not claimed

- Not claimed: that 41 is the shortest possible program for 114514, or that the search was exhaustive. The
  search covered a parameterised one-loop fold family (see how-we-built-it/) and is not a completeness proof.
- Not claimed: a new construction method. The object is an instance of the page's own documented
  tape-hungry fold; the claim names that seed explicitly (see panel/novelty.md for the edit-closure test).
- Not claimed: anything about the neighbouring constants. Companion objects found in the same search
  (257 in 27 instructions, non-negative cells; 97104 in 49) are not part of this claim and were not panelled.

## Credits

- The esolangs wiki community — the Brainfuck constants table this claim is measured against (CC0), and the
  tape-hungry fold construction documented in the page's Algorithms section, which is the named seed of the
  object.
- User Primo (talk page, 2017) — the informal 2-cell/3-cell optimality crunches that frame what was already
  known.
- rdebath — the `crunchingbrains` brute-force logs used as a prior-art boundary (values 9..247 only).
- Three independent skeptic panels (REPRODUCE / NOVELTY / CRITERION) — fresh-context verification; their
  reports are in panel/.
