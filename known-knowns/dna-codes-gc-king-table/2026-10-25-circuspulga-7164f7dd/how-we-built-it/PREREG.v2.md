# PREREG v2 (written 2026-10-24T12:38:40Z, AFTER first results; PREREG.md stays unchanged)

Why a v2: (1) king_bounds.py was patched twice before its output was used (DP cross-check limited to small cells;
a 10^6 cap on Theorem 4 replaced by the Theorem 5 limit, because capped values produced false "table above bound"
lines); (2) two new programs were written after PREREG.md (far-import/code/simplex20.py, far-import/code/gf4slice.py);
(3) results seen before this file: m-sequence code 15 at (15,12) VALID; simplex code 16 at (20,16) VALID;
gf4slice seed 1 (300 restarts): (15,11) 39 VALID, (20,15) 36 VALID, (19,14) 41 VALID, (18,13) 40, (16,12) 54;
null controls at (15,12) finished (not yet summarised).

## Claim focus (one cell per claim)
- The single claim cell is (n,d,w) = (15,11,7), which PREREG.md already named as the secondary cell (table 34,
  unmarked 'v'). Thresholds unchanged from PREREG.md (size > 34 and checker VALID -> at most PROMISING).
- (20,15,10) and (19,14,9) were NOT pre-registered; they are reported as exploratory observations, each would need
  its own run/prereg and panel. (15,12) tie and (20,16) tie: reported under tie-unmarked-mid, with the note that both
  cells are already optimal by King 2003 Theorem 4 (unmarked on the page).

## Null for the claim cell (added now, before running it)
null_test: required
Controls: 400 random maximal codes at (15,11,7) from null-and-leak-auditor/code/nullgreedy.c (seeds 1..400,
unchanged code, sha256 18f05409...). The final claimed (15,11) code size must be strictly larger than every control.
The PREREG.md null at (15,12,7) is also reported.

## Further search allowed on (15,11) before the final freeze
More restarts/seeds of gf4slice.py; augmentation of the best slice by gcmc warm start (M = best+1). The final claimed
object is whatever checker-VALID code is largest at freeze; its file sha256 and the sha256 of the program that made it
go into claim/ and the report. A tie-break: smallest seed.

## Code sha256 at this point
9d58cf4df669bab74d4802d760f16021e57a6b43aa4ab75c9a678e3ce0487cfc  attempts/table-auditor/code/king_bounds.py
21f90ca3bca4e9e95597c6a97de0343657f693e7f9fdd78bf5abd2d691e0c3de  attempts/far-import/code/mseq.py
3724ff792ad2b014eaf6beed0c845584f9d678bc44248b5831ee41adeabc4b0c  attempts/far-import/code/simplex20.py
d37c340ed102534ba3c3d68f04a5335539ba9a6baddc9945216bbe887fb7549c  attempts/far-import/code/gf4slice.py
7d0e5e2415c1caec3f5a7cf1a576ba2cdb6f70513ee28eab2bacd7b8d2d872b7  attempts/evaluator-first/code/gcmc.c
18f05409983739c1467431785074233f0d44b24d45d140a47fabe4508174be33  attempts/null-and-leak-auditor/code/nullgreedy.c
