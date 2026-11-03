# CRITERION skeptic — panel 1321

context: subagent (executor CRITERION, scratch $TMPDIR/panel1321-criterion)
inputs: only the claim package copy (claim.md, table_record.md, REPRODUCE.md, result/, code/, fixtures/, data/)

## Criterion (bank) clauses checked literally
1. Board: 9x9 square board, 81 holes (Bell: "The 9x9 Board (81 holes)"). Solution uses all 81 holes a1..i9 — consistent. OK.
2. Central game: start vacancy e5, finish single peg at e5. My own from-scratch simulator (written without reading code/check9.py; on-board check, orthogonal distance-2 only, from/over occupied, to empty): left=1, e5=1. OK.
3. Orthogonal jumps only: every jump has (|dx|,|dy|) in {(2,0),(0,2)}. OK.
4. Move = maximal run of consecutive jumps by the same peg: I counted moves by merging consecutive jumps where jump k+1 starts at jump k's landing hole, regardless of line breaks (so line-splitting cannot inflate or deflate the count). Result: jumps=79, moves=31. Matches code/check9.py (VALID, 31) and code/replay9.c (PASS, 31).
5. At most 33 moves: 31 <= 33. OK.
6. Strictly shorter than best on Bell's page at claim time: data/bell_index_claim.html (sha256 0cab8355..., identical to scout copy) says the 9x9 central-game shortest solution "is currently an open question. In 2004, Alain Maye found a solution by hand in 34 moves." 31 < 34. OK.

## Null models / calibration
- Fixtures: my simulator rejects neg_diag, neg_occupied, neg_sol31_swapped (illegal jump), and neg_sol31_truncated (4 pegs left) / neg_unfinished (79 left) as non-solutions; pos_beam_34 is a valid 34-move solution. So the checker discriminates, and the 34 calibration equals (does not beat) the record.
- Trivial null: a merely legal solution is not the bar; the bar is <=33 and <34 — 31 clears it by 3, not by a counting-convention artifact (my merge-by-landing count is the most favourable-to-skeptic convention and still gives 31).

## Hidden quantifiers / stretched definitions
- claim.md calls it the "9x9 English" board. That is a misnomer: English = 33-hole cross; this is the 81-hole 9x9 square board. Not part of the criterion; excluded from confirmed_scope.
- "Bell's page": status taken from Bell's main index only; the dedicated 9x9 subpage returned HTTP 500 at scout and was not retried. Residual risk that the subpage lists something shorter than 34 that the main page does not. Mitigation: the main page (Last Modified 2026-10-23) explicitly calls it open with 34 as best, and the bank itself fixes the reference at 34 as of 2026-10-30. Recommend a subpage re-fetch before submission; not disqualifying under the literal criterion.
- No claim of optimality is made or needed; confirmed_scope does not assert 31 is minimal.
- Full criterion is met (not a partial win), and the result is not subsumed by the 34-move record.

confirmed_scope: result/sol31.txt is a legal 9x9 (81-hole) square-board central-game solution from e5 vacancy to a single peg at e5 using orthogonal jumps only, of 79 jumps and 31 moves (maximal same-peg runs), independently replayed, which is shorter than the 34-move Maye solution listed as best on Bell's main index page as fetched at 2026-11-03T14:09:43Z.

pass: true
