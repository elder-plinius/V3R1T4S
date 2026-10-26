# REPRODUCE — A_4^GC(19,14,9)
context: fresh subagent (knowledgeWork) for the REPRODUCE role, given only claim/ and the step-6 instruction, working in its own temporary folder

## definition used (own checker written before reading code/check_gc_code.py)
"all words have length n over {A,C,G,T}, exactly the table's GC-content w (w = floor(n/2)), pairwise Hamming distance >= d, are distinct" (bank criterion, quoted in CLAIM.md). Here n=19, d=14, w=9.

## own checker on objects/A4GC_19_14_9_M44.txt
- sha256 8b28d53b3639dc0cc9d1a1afd37dfca139f5c3852c66003db5ee118b476c1a1a (matches CLAIM.md and PREREG.md)
- 44 lines, 44 distinct words, all length 19, alphabet subset of ACGT, GC count = 9 for every word
- all 946 pairs checked exhaustively: minimum Hamming distance 14 (>= 14)
- result: OK

## table cell (read directly from data/dnacodes.html)
- data/dnacodes.html sha256 25d6e9f88262fbb07c95841225cb3202aa29eb31f7f72d24b43e9c595bdb18c5 (matches CLAIM.md)
- first table "Lower bounds for A4GC(n,d,w)", row 19, column d=14: `38<sup>v </sup>` — no '.' or ':' after it (unmarked; v = VNS, [MS]/[MS2])
- 44 > 38

## regeneration (PREREG command, claim copy code/gf4slice.py)
- code/gf4slice.py sha256 d37c340e...7549c, code/check_gc_code.py ba053c3e...f5bb70, null/nullsample.c 7c5e3d1a...b3ee: all equal to the frozen hashes in PREREG.md
- `python3 code/gf4slice.py 19 1 3000 rebuilt.txt` run twice: best_count=44, sha256 8b28d53b...1c1a1a both times, byte-identical to the object (deterministic; ~38 s each)
- the generator opens only its output file (no read of the object)

## freeze
- `sha256sum -c PREREG.sha256` in claim/: PREREG.md: OK

## author's checker (run after own check)
- `python3 code/check_gc_code.py objects/A4GC_19_14_9_M44.txt 19 14 data/dnacodes.html`: "VERDICT: VALID, beats_table=True", cell 38 marker ''
- `--selftest`: PASS (corrupted copy rejected)

## not checked here
- the post-2010 literature clause and the live re-fetch of the table (NOVELTY's job); w = floor(n/2) taken from the criterion text, the saved page does not restate it.
- null/ outputs were not re-run (not a reproduction requirement).

pass: true
