# REPRODUCE verdict — peg-solitaire-9x9-central-game (31 moves)

context: subagent (executor REPRODUCE, scratch $TMPDIR/panel1321-reproduce)

## Definition used (quoted from claim.md, "Success criterion (bank, verbatim)")
> A legal central-game solution on the 9x9 board (centre vacancy to one peg in the centre, orthogonal jumps only) using at most 33 moves, where a move is a maximal run of consecutive jumps by the same peg, verified by a simulator that replays every jump and counts moves. It must be strictly shorter than the best solution on Bell's page at claim time (34 moves as of 2026-10-30).

Board: Bell's page (data/bell_index_claim.html) defines "The 9x9 Board (81 holes)", the full square, in "Standard 9x9 Notation": columns a-i, rows 1-9, centre e5. I used that. claim.md's one-sentence summary says "9x9 English", which is loose wording. The object uses the corner holes (a1, i1, a9, i9), so it is on the 81-hole square board, the board Bell's open question is about.

## Own checker (written before reading the author's code)
mine/mycheck.py (in scratch, not in the package). It does this:
- starts with all 81 holes full except e5
- parses every "-"-separated path into single jumps
- requires each jump to be orthogonal with a distance of 2, and requires from = peg, over = peg, to = empty and on the board
- removes the jumped peg each time
- counts moves as maximal runs, where a new move starts whenever a jump's start hole differs from the previous jump's end hole (so moves split across lines would also merge)
- requires exactly 1 peg left, at e5

## Results
- result/sol31.txt (31 lines, sha256 a49cfc85…093a): VALID, jumps=79, moves=31, pegs=1, peg at e5. The 79 jumps leave 1 of 80 pegs, as expected. The maximal-run count equals the line count, so no adjacent lines belong to the same peg.
- Fixtures under my checker:
  - neg_diag: ILLEGAL (geometry)
  - neg_occupied: ILLEGAL (occupancy)
  - neg_sol31_swapped: ILLEGAL (occupancy, jump 3 when counted from 0)
  - neg_sol31_truncated: INVALID (4 pegs left)
  - neg_unfinished: INVALID
  - pos_beam_34: VALID in 34 moves
- After my checker: code/check9.py and code/replay9.c (built with gcc -O2) both report jumps=79, moves=31, VALID/PASS. They agree with my checker on all 6 fixtures. Two runs of each gave identical output, so the results are deterministic.
- 31 ≤ 33 and 31 < 34, so the criterion is met.

## Status (best on Bell's page)
- data/bell_index.html and data/bell_index_claim.html: sha256 0cab8355…4e68, which matches table_record.md. Both show "Last Modified October 23rd, 2026", "what is the shortest solution to the central game? This is currently an open question. In 2004, Alain Maye found a solution by hand in 34 moves."
- I re-fetched https://www.gibell.net/pegsolitaire/ live during this review (2026-11-03, about 09:1x ET, HTTP 200). It is byte-identical (same sha256), so the record is still 34 and still open.
- The 9x9 subpage was not checked, by the author (HTTP 500 at scout) or by me. Status rests on the main page, as table_record.md says.

## Notes
- This was not an exhaustive-search claim. It is a single explicit object, and every jump was replayed in full.
- I did not re-run the beam search (code/beam9.c). The claim marks it optional, and it is not needed to verify the object.
- Minor issue: the summary's "English" wording is inaccurate. The board meant is the 81-hole 9x9 square. This does not change the verdict.

pass: true
