# CRITERION
context: subagent

## 1. The criterion and the named partial win (quoted from how-we-built-it/PREREG.md)

Success criterion (how-we-built-it/PREREG.md, "Criterion (verbatim from bank/targets.json)"):

"A Brainfuck string for some n listed on https://esolangs.org/wiki/Brainfuck_constants (re-fetched live immediately before claiming) such that a reference interpreter with unbounded right tape, 8-bit cells (wrapping only if claimed in the wrapping category), starting at all zeros, halts with the pointer on a cell holding n (mod 256 rules exactly as the page defines), never moves left of the start cell, and whose instruction count is strictly less than the smallest listed count for n in that category (and for numbers > 255, the page's stated cell-size conventions)."

Enumerated partial win (how-we-built-it/PREREG.md, line 17): `over-255` — "A shorter program for one of the listed constants above 255."

## 2. The object

object/program.bf = `>++>+++>+++>+++>+>++>++>+[>+[-<++++>]<<]>`, exactly 41 bytes (wc -c = 41, no trailing newline), every byte a BF instruction (no comments, no I/O), so the instruction count is 41. Claimed n = 114514.

## 3. Literal behaviour check

Hand-trace of the full run: the preamble seeds cells 1..8 with 2,3,3,3,1,2,2,1; the drift loop `[>+[-<++++>]<<]` folds right-to-left, each outer pass adding 1 to the right neighbour and multiplying that neighbour by 4 back into the current cell, giving v8=5, v7=26, v6=110, v5=445, v4=1787, v3=7155, v2=28627, v1=114514; the fold's last `<<` lands on cell 0 (value 0) so the loop exits, and the final `>` halts on cell 1 holding 114514. Minimum pointer = 0, minimum cell value = 0 (no negative cells), maximum pointer = 9. Counting executed instructions by hand: preamble 25 + outer-loop entry `[` 1 + eight outer passes of (6 + 8k) for k = 1, 6, 27, 111, 446, 1788, 7156, 28628 (sum k = 38163, so 8 x 38163 = 305304, plus 48) + final `>` 1 = 305379. This exactly matches object/expected.txt ("STEPS=305379 PTR=1 VALUE=114514 MINPTR=0 MAXPTR=9 MINCELL=0 LEN=41 HALTED=1 OK=1") — derived before running any code, an independent confirmation a gamed checker cannot produce. checker.py run now: `PASS len=41 value=114514 steps=305379 mincell=0` (exit 0). The checker implements the definition directly: unbounded right tape, arbitrary-precision non-wrapping cells, pointer below 0 rejected, final pointer cell must equal 114514 exactly, non-BF characters rejected.

## 4. The comparison — every reading of "smallest listed count for n in that category"

I fetched https://esolangs.org/wiki/Brainfuck_constants once (HTTP 200). Its sha256 d78c05da7dbb20b80f70cceea943fdd429372ae6abfbb3fe810cc29471db0dd4 is byte-identical to the snapshot recorded in the-record-we-beat/record.md (fetched 2026-11-03T19:45:41Z), so the recorded table is authentic and unmodified. The page contains exactly one 114514 section (3 text occurrences of "114514", all inside it). It lists, in the page's "(instructions, cells)" notation:

- "Generate using power series." `+++[>++++++++<-]>+++[<++++++++>-]<+++++++[>++++++++<-]>+++++[<++++++++>-]<++[>++++++++<-]>++` — (92, 2) non-wrapping; leaves 114514 in a cell (hand-verified: accumulate 3x8=24, +3, x8 -> 216+7*8... fold reaches intermediate 14314, then 114512 + 2 = 114514 in cell 1).
- "Printing the pistol emoji in UTF-8" `>++++++[<+++++>-]<+[>+++++>++++++>++++++++<<<-]>>>--------.<<.>+++.<---------.` — (78, 4) non-wrapping; printer (ends in `.`).
- "Printing the pistol emoji in UTF-8 using signed chars (no wrapping)" `++++[->----<]>.-[+<------>]<+.-[+++>--<]>+.+[+++<----->]<.` — (58, 2) non-wrapping; printer; its first loop drives a cell to -16 (later cells reach -102), so under the page's rule "for numbers greater than 255 'soft' means that it uses negative cells" it is soft, even though the page tags it "signed chars" rather than "(soft)".
- Unnumbered "Other versions": `62+[>1847+<-]>.` (BF-RLE notation; the page lists no instruction count for it, and it is not a valid BF string since digits are not BF instructions) and a CESU-8 printer (no count listed on the page itself; the-record-we-beat/record.md measures 468 expanded).

Readings of "smallest listed count for n in that category":

- All numbered listings: min = 58; 41 < 58 (by 17).
- Value-in-cell listings only (92; BF-RLE expansion 1916 per the-record-we-beat/record.md): min = 92; 41 < 92 (by 51).
- Non-soft listings only: min = 78 (92 among value-in-cell); 41 < 78.
- Including the unnumbered blocks under the-record-we-beat/record.md's counts (468, 1916): min still 58; 41 < 58.
- Adversarial reading of the RLE form as ~15 characters: rejected — the page lists no count for it, it is explicitly a compression encoding ("encoded in BF-RLE"), and the criterion compares against a "listed count" under the page's "number of program instructions" convention.

Under every reading, 41 is strictly less than the smallest listed count for 114514; the verdict does not depend on resolving the category question.

## 5. Category / conventions check (n > 255)

The page's conventions, verified verbatim on the live fetch: "The shortest known Brainfuck code sequences are listed for each constant, along with number of program instructions and cells taken. Cells for values 0..255 are assumed to be unsigned 8 bits and initialized to zero. Wrapping indicates that any cell over/underflows are allowed and wrap using normal modular arithmetic. The non-wrapping solutions do not require this though the ones marked with '(soft)' do require cell values outside the 0-255 range (For numbers greater than 255 'soft' means that it uses negative cells)." and "none of the sequences here modify or rely on the contents of any cell to the left of the data pointer's initial location."

The object is non-wrapping, non-soft (MINCELL=0), leaves the value in a cell, and never touches a cell left of its start — the same category as the page's own listed 92, which itself holds values above 255 in cells (intermediate 14314, final 114514). Holding >255 cell values is therefore the category's own requirement under the criterion's "(and for numbers > 255, the page's stated cell-size conventions)" clause, not a claimant stretch; the criterion's "8-bit cells" default governs the 0..255 categories and explicitly defers to the page for >255.

## 6. Hidden quantifiers and null models

- "re-fetched live immediately before claiming": the-record-we-beat/record.md documents the claim-time fetch (2026-11-03T19:45:41Z, HTTP 200, sha256 recorded); my independent fetch returned byte-identical content, so the comparison target is real and current.
- "instruction count": 41 is the count of actual BF instructions (41 bytes, no comment padding; the checker rejects non-BF characters and passed).
- "halts": the fold provably terminates (drains to cell 0 = 0); 305379 steps, finite.
- Null model "a shorter listing exists somewhere on the page": none — the only 114514 section lists nothing at or below 41 (shortest 58).
- Null model "the win is an artifact of a gamed checker": ruled out — my hand-derived step count (305379) matched object/expected.txt exactly before I ran anything.
- Subsumption: how-we-built-it/PREREG.md names exactly one partial win for this target (`over-255`); the object meets it literally (114514 is a listed constant above 255, and 41 is shorter than every count listed for it) and also satisfies the full criterion's literal wording for n = 114514. Nothing wider is claimed: README.md's "Not claimed" section disclaims optimality, exhaustive search, and novelty of the construction, and the claim is scoped to this one constant and its listed sequences.

## 7. Scope

This verdict covers n = 114514 only, the comparison against the sequences listed on the live page for that constant only, and the measured behaviour of this one 41-instruction string. It does not assert that 41 is optimal, that no shorter program exists, or anything about other constants.

confirmed_scope: The 41-instruction program object/program.bf, started from all zeros, halts after 305379 steps with the pointer on cell 1 holding exactly 114514, never moves left of cell 0, never holds a negative cell, and 41 is strictly less than every instruction count listed for 114514 on the live esolangs Brainfuck constants page (58, 78, 92 numbered, plus unnumbered BF-RLE and CESU-8 blocks), literally satisfying the over-255 partial win for this one constant.

pass: true
