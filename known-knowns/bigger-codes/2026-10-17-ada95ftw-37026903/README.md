# A(33,10,7) <= 145 (Delsarte LP certificate), constant-weight-codes, partial win p2

## What
An exact rational dual certificate for the Delsarte linear program of J(33,7), augmented with the single standard shell inequality a_7 <= A(26,10,7) and using the published bound A(26,10,7) <= 36 (Agrell–Vardy–Zeger 2000, printed in Brouwer's table), proves A(33,10,7) <= 145, strictly below the live tabulated upper bound 150 and below the neighbour Johnson bound 146 obtainable from the table's current A(32,10,6) = 31.

## Check it yourself
```sh
sh verify-it-yourself/run_checks.sh
```
Expected last line: `PASS` (the line before it: `VERIFIED bound 145`). Python 3 standard library only; about a second on a laptop.

## Compared to
- Table: A. E. Brouwer, Bounds for binary constant weight codes, https://aeb.win.tue.nl/codes/Andw.html
- Cell: A(33,10,7) (mirror A(33,10,26) by complementation), printed `72-150`: upper bound 150 (unmarked; for n > 28 the page says unmarked upper bounds are Johnson bounds).
- Fetched 2026-10-17T08:02:33Z (scout) and again 2026-10-17T12:15:46Z (gate), HTTP 200, identical sha256 117899cff5af3fd00af17389595c5756050edb94cba876570cf9b76e451107f8. Details in the-record-we-beat/.
- Certified value 26928/185, so A(33,10,7) <= 145 < 150.

## Not claimed
- No new code and no new lower bound: the cell stays open (72..145).
- Not a new method. Delsarte's LP (1973) plus a classical counting row; new only as a table entry.
- The bound rests on one published input, A(26,10,7) <= 36 (A(26,10,7) printed "30-36" in the same table). The input A(26,10,7) <= 36 is the printed upper bound of "30-36" (Agrell-Vardy-Zeger 2000). The printed 150 is a stale Johnson value: Johnson with the table's own A(32,10,6) = 31 already gives 146, so the real margin is one codeword (146 -> 145).
- Not optimal; a Schrijver-type SDP or more constraints may do better.
- No claim beyond this one cell.

## Credits
- P. Delsarte, An algebraic approach to the association schemes of coding theory, Philips Res. Rep. Suppl. 10 (1973): the LP method.
- E. Agrell, A. Vardy, K. Zeger, Upper bounds for constant weight codes, IEEE Trans. Inform. Theory 46 (2000) 2373-2395: the input bound and the a_x <= C(w,x)A(n-w,d,x)-style constraints.
- S. M. Johnson (Johnson bound) for the printed value compared against.
- A. E. Brouwer, table of bounds for constant weight codes, https://aeb.win.tue.nl/codes/Andw.html.
- Found and packaged by ada95ftw with the V3R1T4S kit (https://github.com/elder-plinius/V3R1T4S).
