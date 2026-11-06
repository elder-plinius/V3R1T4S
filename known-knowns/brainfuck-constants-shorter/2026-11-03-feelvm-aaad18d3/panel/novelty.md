# NOVELTY
context: subagent

## Primary fetch (one-shot, honest)

- URL: https://esolangs.org/wiki/Brainfuck_constants
- Fetched (UTC): 2026-11-03T20:29:11Z
- HTTP status: 200
- User-Agent: `V3R1T4S-novelty-panel/1.0 (one-shot fetch; no retries)`
- Page sha256: `d78c05da7dbb20b80f70cceea943fdd429372ae6abfbb3fe810cc29471db0dd4` — byte-identical to the
  sha256 recorded in the-record-we-beat/record.md (fetched 2026-11-03T19:45:41Z). Current revision confirmed as oldid
  160357, "last edited on 25 June 2025, at 15:33".

## The 114514 cell as fetched (quoted)

Numbered entries:

- `+++[>++++++++<-]>+++[<++++++++>-]<+++++++[>++++++++<-]>+++++[<++++++++>-]<++[>++++++++<-]>++` — (92, 2)
  non-wrapping ("Generate using power series." — leaves 114514 in a cell)
- `>++++++[<+++++>-]<+[>+++++>++++++>++++++++<<<-]>>>--------.<<.>+++.<---------.` — (78, 4) non-wrapping
  ("Printing the pistol emoji in UTF-8")
- `++++[->----<]>.-[+<------>]<+.-[+++>--<]>+.+[+++<----->]<.` — (58, 2) non-wrapping ("Printing the pistol
  emoji in UTF-8 using signed chars (no wrapping)")

Unnumbered "Other versions":

- `62+[>1847+<-]>.` — BF-RLE ("114514=62×1847 but its too long, so encoded in BF-RLE"); expands to 1916
  instructions under the page's RLE convention.
- a 468-instruction CESU-8 printer ("'Shorter', Uses non-standard 'CESU-8' encoding that is usually
  considered broken.").

Nothing listed for 114514 is ≤ 41. Smallest listed count: 58 (printer); smallest value-in-cell count: 92.

Over-255 sections on the page: 256, 333, 45306, 114514, 97104 — the neighbouring cells are 45306 and 97104
(97104 has one unannotated power-series program).

## Independent verification of the object

With my own reference interpreter (arbitrary-precision cells, no wrapping, unbounded right tape):

```
LEN=41 HALTED=1 STEPS=305379 PTR=1 VALUE=114514 MINCELL=0 MINPTR=0 MAXPTR=9
```

Matches object/expected.txt exactly. The object is a non-soft instance of the page's tape-hungry drift-fold
construction: digits 2,3,3,3,1,2,2,1 written to cells 1..8, one drifting propagation loop
`[>+[-<++++>]<<]` (base 4, +1 bias per fold), final `>`. Hand-checked arithmetic:
114514 − (4+16+…+4^8) = 114514 − 87380 = 27134 = (2,3,3,3,1,2,2,1) base 4 (LSB first) — the claimed digit
vector is the exact offset representation, no zeros (a zero written digit would stop the drift loop early).

## Named seed and what trivial edits of it give

The claim names its seed: the page's own "Algorithms" construction ("Using these tape-hungry methods…" /
Free-form Series; added to the page by Rdebath in December 2013 per the Talk page), with published working
instances at other constants. All three named seed instances were verified verbatim on the live page and
executed with my interpreter:

| seed | program | listed | my run |
|---|---|---|---|
| 256 | `>+>->->+[>++[-<+++>]<<]>` | (24, 6) soft | value 256, mincell −1 |
| 333 | `>+>->+>+>+[>[-<++++>]<<]>` | (25, 7) soft | value 333, mincell −1 |
| 45306 | `+>>->>>>+[+>++[-<+++++>]<<-]>+` | (30, 8) soft | value 45306, 101,973 steps (matches prior_art.md) |

Seed rule applied literally — do trivial edits (deletion, restriction, a valid propagation rule, relabelling,
symmetry, a local numerical polish, alone or combined) of these published objects alone give the claimed
object's cell (114514), or anything at ≤ 41 instructions for it?

- Structural barriers (hand analysis, verified arithmetically):
  - Deletion only removes units; the object needs 8 written digit cells (base 4, bias 1). Every published
    drift-fold instance on the page has at most 7 digit cells of total state (at most 5 written before the
    loop; measured over the 191 drift-fold programs in sections 200-255..Algorithms: histogram
    2:71, 3:91, 4:26, 5:3). No edit in the trivial set adds digit cells.
  - A propagation-rule edit (changing the loop multiplier/bias) leaves the digit vector fixed; with the
    seeds' fixed digit vectors the reachable value set under multiplier 1..15 is finite and small.
  - Re-choosing base, length and digits to retarget the construction is exactly the optimisation the page
    itself states has "no known efficient algorithm" — that is re-derivation, not a trivial edit. The claim
    discloses this openly and names the construction as its seed.
  - Symmetry/relabelling (mirroring, start-cell shifts) preserve the computed value; they give no new value.
- Computational enumeration (named seeds, wide box): each of the three named seed programs was put through
  a deliberately wide trivial-edit closure — polish any unit by ±3, set any in-loop run length to any value
  1..15 (valid propagation rule), delete any one unit, mirror (symmetry), and combinations of a
  propagation-rule change with up to TWO simultaneous digit polishes — and every resulting program was
  executed in an independent interpreter (arbitrary-precision cells, no wrapping, step cap 8M):

  | seed | edits tested | programs computing 114514 |
  |---|---|---|
  | S256 (24 → 256) | 5,101 | **0** |
  | S333 (25 → 333) | 5,516 | **0** |
  | S45306 (30 → 45306) | 8,237 | **0** |

  No trivial edit of any named seed computes 114514 at any length — the claimed object therefore beats
  what trivial edits of the named seed alone give (they give nothing for this cell).
- Whole-page enumeration: all published program strings on the page (whole table, 1440 strings from section
  0-99 through Algorithms — including the three named seeds, the neighbouring cells 256/333/45306/97104,
  and the 114514 cell's own 92/78/58 programs) were put through a bounded trivial-edit closure: delete one
  unit; polish one unit ±2; set any in-loop run to any length 1..15 (valid propagation rule); and
  combinations of a propagation-rule change with a digit polish. 402,176 distinct edited programs were
  executed (4 parallel workers, arbitrary-precision cells, no wrapping, pointer-left-of-start aborts, 6M
  step cap, per-general-loop budget 20k — see method notes below). RESULT: **21 unique programs computing
  114514, every one of length 93-107, and every one an edit of the 114514 cell's own listed 92-instruction
  power series** (no-op `.` prefixes, multiplier/digit re-balancing; some reach 114514 only through
  intermediate cells as negative as −11.5M). The shortest trivial-edit product is 93 instructions — longer
  than the page's listed 92, and 52 instructions longer than the claimed object. **No edit product comes
  from the named seeds, and nothing at or below 92 was produced by any edit of anything published.**
  Shortest hits (all verified by re-running in the slow reference interpreter):

  - len 93: `.+++[>++++++++<-]>+++[<++++++++>-]<+++++++[>++++++++<-]>+++++[<++++++++>-]<++[>++++++++<-]>++`
    (the listed 92 with a no-op `.` prepended; mincell 0, 196,305 steps)
  - len 95: `.+++[>++++++++<-]>+++[<++++++++>---]<+++++++[>++++++++<-]>+++++[<++++++++>-]<++[>++++++++<-]>++`
    (multiplier rebalance; mincell 0, 69,963 steps)
  - len 96: `.++[>++++++++++++<-]>+++[<++++++++>-]<+++++++[>++++++++<-]>+++++[<++++++++>-]<++[>++++++++<-]>++`
    (mincell 0) — and 17 more, all ≥ 94.

## Enumeration method notes (for reproducibility and audit)

- Candidates: maximal instruction-character strings from the page HTML (tags stripped before unescaping,
  hard-wrapped lines joined), bracket-balanced, ≤ 151 instructions as parents (longer parents — the
  468-instruction CESU-8 printer — cannot yield edits ≤ 135 and were not enumerated), edit products capped
  at 135 instructions; named-seed wide-box products capped at 60.
- Interpreter: run-length encoded with arithmetic fast paths for simple transfer loops (bodies of the form
  `[-<+M>]`, `[<+M>-]`, `[- >+M< ]`), which were A/B-verified value-exact (value, final pointer,
  min cell) against a slow per-instruction reference interpreter on 449 published programs plus the object;
  the object's own 305,379-step count matches object/expected.txt exactly under the slow interpreter. A
  sound infinite-loop early-out covers flat loops whose checked cell can never reach zero; a 20k-step
  budget per general (non-transfer) loop instance aborts pathological drift loops — no legitimate
  fold-family candidate for 114514 can exceed it (its general loops iterate at most once per digit; the
  object's general-loop usage is ~40 steps). Step counts reported for hits are from the slow reference.
- Known budget boundaries: edits are ≤ 3 simultaneous local changes (propagation-rule change × up to two
  digit polishes for the named seeds; × one digit polish page-wide); deeper chains are covered by the
  structural argument (no trivial edit adds the 8 digit cells the object's construction writes — measured:
  all 191 published drift folds in sections 200-255..Algorithms have ≤ 5 pre-loop written cells, ≤ 7 cells
  of fold state; deletion only shrinks; relabelling/symmetry preserve values — mirrors of the named seeds
  were included in their wide box and add no new values).
- Restriction edits of the 114514 cell's own printers: dropping the output instructions from the 58-instr
  printer yields a program that does NOT halt on no-wrap cells (infinite loop); from the 78-instr printer
  yields a 74-75 instruction program ending at 146/189, not 114514. Restriction of the BF-RLE or CESU-8
  forms leaves programs of 1915+/464+ instructions. Nothing at ≤ 41.

## Prior-art searches (all single-shot; blocks recorded, not retried)

- Live table (above): nothing ≤ 41 for 114514.
- Talk page https://esolangs.org/wiki/Talk:Brainfuck_constants (fetched 2026-11-03T20:50:22Z, HTTP 200):
  newest entry 29 April 2024 (Rdebath, on >255 conventions — no construction); before that 7 Aug 2023
  (None1, a question), 17 May 2017 (Primo: 2-cell solutions optimal in length for small constants), 2016
  (Rdebath: crunchfuck results, values ≤ 255), 2013 (Rdebath added the fold algorithm: "I don't really want
  to add 4 billion strings to this page"). Nothing in the last 24 months; no over-255 instance anywhere
  beyond the main-page table.
- Page history: `https://esolangs.org/w/index.php?...action=history` returned HTTP 403 (one attempt; not
  retried). Current-revision metadata from the fetched page itself confirms oldid 160357 (25 June 2025) —
  the same revision the claim compares against.
- github.com/rdebath/crunchingbrains: repo tree fetched via GitHub API (HTTP 200, 2026-11-03T20:52:41Z);
  the largest result log run1b/run.txt fetched raw (HTTP 200, 5,761,802 bytes): 79,008 `Result:` lines,
  values span 9..247, zero occurrences of `114514`. Confirms prior_art.md's characterization (8-bit
  wrapping brute force; no data for any constant above 247).
- GitHub code-search API: HTTP 401 (requires authentication) — recorded, not retried. The claim records an
  authenticated human-run search (2026-11-03) with no results for the object or `114514` in `.bf`.
- grep.app: HTTP 429 Vercel security checkpoint — recorded, not retried (matches the claim's own record).
- Sourcegraph public code search (HTTP 200, 2026-11-03T20:55:54Z): exact 41-byte object string → 0 matches;
  `114514` in `*.bf` files → 0 matches. Corroborates the claim's GitHub search.
- Web/literature searches (last 24 months): no paper, post, or repo constructing Brainfuck constants ≥ 255
  beyond the esolangs table; the anarchy golf problem "114514" ("make a 114514 number", fetched
  2026-11-03T20:54:39Z) has no Brainfuck entry at all (shortest 10 bytes is Nibbles, a different task —
  printing the numeral); esolangs wiki search for 114514 surfaces only the Brainfuck constants table
  itself (the `/w/index.php` search path returned HTTP 403; equivalent scoping done via web search).
- This claim ecosystem: TROPHY_CASE.md — no brainfuck/114514/esolang entries; known-knowns/ — none;
  open and closed PRs/issues of the repo (elder-plinius/V3R1T4S, GitHub search API HTTP 200) — zero
  matches for brainfuck/114514/esolangs.
- Blocked once each, not retried: esolangs `/w/index.php` (HTTP 403, history + search), grep.app (HTTP 429),
  GitHub code-search API (HTTP 401, auth required).

## Comparison with the claim

- The claim names the seed (the page's own construction and its published instances) and does not claim the
  method is new — as the novelty rule requires for a seeded object.
- The object (41, non-soft) strictly beats every listed sequence for its cell in every category: 58 (printer),
  92 (value-in-cell), 78 (printer), 1916 (BF-RLE expanded), 468 (CESU-8 printer). A tie would not pass; this
  is a strict win of 17 instructions over the smallest listed count.
- Trivial edits of the named seeds give no 114514 program at all (18,854 wide-box edits, zero hits). Trivial
  edits of everything else published on the page give 114514 programs only at lengths 93-107 (all edits of
  the cell's own listed 92). The object is not reachable from any published object by the listed edit
  classes, and it strictly beats every edit product (41 < 93) and every listed count (41 < 58 < 92).
- No prior art for a shorter 114514 program was found in code search (Sourcegraph global: exact object
  string 0 hits; `114514` in `*.bf` 0 hits), the talk page, the crunchingbrains logs, the repo's
  TROPHY_CASE/known-knowns/PRs, or the last 24 months of literature.

## Verdict

The claimed object is a genuine instance of the page's own published tape-hungry fold construction (the
claim names the construction and its published instances as the seed, exactly as the novelty rule requires).
The seed rule is satisfied: (a) no trivial edit of the named seeds produces any 114514 program at any
length (0 of 18,854); (b) no trivial edit of any other published object produces one shorter than 93 (the
best edit product is the listed 92 padded by one no-op), so the object strictly beats everything trivial
edits give; (c) the object strictly beats every listed count for its cell (41 vs 58/78/92/468/1916) — not a
tie; (d) no prior art for a shorter 114514 program exists in the last 24 months of literature, public code,
the wiki talk page, the crunchingbrains logs, or this claim ecosystem's own records. The page history
endpoint was blocked (HTTP 403, single attempt, not retried), so the possibility of a shorter program in an
older revision of the page cannot be fully excluded; however, the current revision is the one the target
definition designates (re-fetched live, byte-identical sha256 to the claim's fetch), and the wiki's stated
convention is to list the shortest known sequences, which makes a hidden shorter historical entry unlikely.

pass: true
