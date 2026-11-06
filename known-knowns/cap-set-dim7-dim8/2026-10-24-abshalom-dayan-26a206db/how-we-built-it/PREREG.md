<!-- Package copy of the run's PREREG.md (original sha256 9a2e114fc4dcbae5a7ede35beb2e6baf2ac2f6c026ef6763486e1791149c665a). One change: the usage notation "angle-bracket file, angle-bracket n" is written FILE N here so the package checker does not read it as an unfilled placeholder. Nothing else differs. -->

# PREREG: cap-set-dim7-dim8, run 2026-10-24-1738

frozen: 2026-10-24T17:46:24Z (date -u), before any lens of this run has run. (The 236-cap rebuild in checker/ is an input, a tie
with the record, and scores nothing.)

## Criterion (verbatim, bank)
Success means a set S of distinct vectors in {0,1,2}^n (n = 7 or 8) such that for every pair of distinct x,y in S, the third point -(x+y) mod 3 is not in S, verified exhaustively, with |S| STRICTLY GREATER (direction: max) than the best known cap size for that n at verification time (OEIS A090245, Wikipedia 'Cap set', fresh arXiv search; context on 2026-10-03: 236 for n=7, 512 for n=8). For n=7, |S| must be <= 288 (Thackeray's bound); larger means a bug.

Partial win p1 (verbatim, bank): A cap in F_3^9 or F_3^10, verified exhaustively, strictly larger than the best published cap for that dimension at verification time (Edel's tables, FunSearch, X-evolve, OEIS, fresh arXiv search).

## Statistic and checker
The object is a text file, one vector per line. Judge: `python3 checker/capcheck.py FILE N` (this run folder),
two independent exact routes (all pairs on base-3 codes; all lines through two members); both must print CAP and
the script must exit 0, and |S| is taken from the same output. A second, independently written checker (the
REPRODUCE skeptic's own) must agree before any status above PROMISING.

## Thresholds
- n=7: 237 <= |S| <= 288. |S| > 288 is a bug, never a claim.
- n=8: |S| >= 513.
- p1, n=9: |S| >= 1083 (FunSearch's notebook states 1082 is the largest known); n=10: strictly above the best
  published value re-read at claim time. Edel's tables are currently unreadable, so a p1 object can reach at most
  PROMISING with "PENDING TABLE CHECK" for Edel's tables unless a skeptic reads them honestly.
- Anything equal to or below the live record (236, 512, 1082) is "nothing" (a rebuilt record is a tool, not a result).

## Null design
null_test: not needed because every claim here is an explicit object judged by a deterministic exhaustive checker against a table value; no search statistic, period or chance level is scored.

## Re-check before any claim
Re-read https://arxiv.org/html/2508.07932 (one honest GET) and run a fresh arXiv search right before a claim.
