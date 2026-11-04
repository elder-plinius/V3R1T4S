# Criterion skeptic: run 2026-11-02-1802
context: subagent (criterion skeptic, isolated claim copy)

Scope read: only the isolated copy of claim/ (paths below are relative to claim/).

## Criterion clauses, checked literally
1. "A legal solution on Triangle(12) in at most 28 moves": result/T12_25moves.txt has 25 comma-separated moves and 76 jumps (= 78 - 2). I re-ran code/pegcheck.py 12 result/T12_25moves.txt and got `start_vacancy=a3 pegs_left=1 finish=j12 jumps=76 moves=25 VALID`. I compiled and ran code/pegsim2.c separately and got `moves=25 pegs_left=1 VALID`. sha256 is 7ec9d443…6c78b, which matches claim.md. 25 <= 28: met.
2. "starting from a single vacancy and ending with a single peg": the start is the full board minus a3, and the finish is one peg at j12. A127500 asks for "any problem beginning with one peg missing and ending with one peg", so the vacancy and finish holes can be anywhere: met.
3. "verified by a simulator": two simulators (Python and C) both say VALID. Calibration: Bell's published T9/16, T10/18, T11/28 and T12/29 solutions all give VALID with the expected move counts, and the two corrupted fixtures (fixtures/neg_T11_swapped.txt, fixtures/neg_T11_order.txt) both give ILLEGAL. I read the code of code/pegcheck.py. Its jump vectors (0,±2), (±2,0), (±2,±2) with matching signs are the correct triangular-lattice jumps. It checks the source, midpoint and target states on every jump. It counts maximal same-peg runs, which is the A127500 definition, so if any of the listed moves chained together the count could only go down. Met.
4. "strictly better than the bounds in the live OEIS A127500 entry and Bell's triangular page at claim time": data/A127500.txt (fetched 2026-11-02T17:31:50Z) says "19<=a(11)<=28, 21<=a(12)<=29". data/bell_large_triangular.html says 21<=S(12)<=29. table_record.md says no pending OEIS draft (data/A127500_draft.html). I found no T12 bound below 29 in data/bell_tindex.html. 25 < 29 is a strict improvement, and 25 >= 21 is consistent with the published lower bound. Met.

## Hidden quantifiers / subsumption
- The criterion says "or", so meeting the T12 alternative alone is enough. T11 is not claimed and not needed.
- This is the first improvement past the published upper bound for a(12), so it is the FULL criterion and not p1, which counts only improvements "beyond the first". Nothing published earlier already gives this result.
- The claim does not reach an exact a(12) value or any lower-bound certificate. Neither p2 nor the exact-value alternative is claimed.
- Limitation: the "live" status depends on fetches taken at 2026-11-02T17:31:50Z, and I did not re-fetch the pages (isolated context).

confirmed_scope: The 25-move sequence in result/T12_25moves.txt is a legal Triangle(12) peg solitaire solution from single vacancy a3 to single peg j12, verified by two simulators, giving a(12) <= 25, strictly below the upper bound 29 in OEIS A127500 and on Bell's page as fetched 2026-11-02T17:31:50Z.

pass: true
