# A(31,10,7) <= 106 (Delsarte LP certificate), constant-weight-codes, partial win p2

## What
An exact rational Delsarte-LP dual certificate (Delsarte inequalities k=1,2 for J(31,7) plus the elementary constraint a_7 <= A(24,10,7) <= 24, using the published bound A(24,10,7) <= 24 (Agrell–Vardy–Zeger 2000, printed as 24 in Brouwer's table)) proves A(31,10,7) <= 106, strictly below the upper bound 109 printed for this cell in Brouwer's Andw.html as fetched 2026-10-17 08:44 UTC.

## Check it yourself
```sh
sh verify-it-yourself/run_checks.sh
```
Expected last line: `PASS` (the line before it: `VERIFIED bound 106`). Python 3 standard library only; about a second on a laptop.

## Compared to
- Table: A. E. Brouwer, Bounds for binary constant weight codes, https://aeb.win.tue.nl/codes/Andw.html
- Cell: A(31,10,7) (mirror A(31,10,24) by complementation), printed `62-109`: upper bound 109 (unmarked; for n > 28 the page says unmarked upper bounds are Johnson bounds).
- Fetched 2026-10-17T08:02:33Z (scout) and again 2026-10-17T12:15:46Z (gate), HTTP 200, identical sha256 117899cff5af3fd00af17389595c5756050edb94cba876570cf9b76e451107f8. Details in the-record-we-beat/.
- Certified value 2015/19, so A(31,10,7) <= 106 < 109.

## Not claimed
- No new code and no new lower bound: the cell stays open (62..106).
- Not a new method. Delsarte's LP (1973) plus a classical counting row; new only as a table entry.
- The bound rests on one published input, A(24,10,7) <= 24 (A(24,10,7) printed "24" in the same table). The input A(24,10,7) <= 24 is printed as the single value "24"; Agrell-Vardy-Zeger 2000, Example 2, proves A(24,10,7) <= 24. The panel could not re-derive it from first principles (it reached 27). With 25 the certificate would still give 108 < 109; with 26 or more the claim fails.
- Not optimal; a Schrijver-type SDP or more constraints may do better.
- No claim beyond this one cell.

## Credits
- P. Delsarte, An algebraic approach to the association schemes of coding theory, Philips Res. Rep. Suppl. 10 (1973): the LP method.
- E. Agrell, A. Vardy, K. Zeger, Upper bounds for constant weight codes, IEEE Trans. Inform. Theory 46 (2000) 2373-2395: the input bound and the a_x <= C(w,x)A(n-w,d,x)-style constraints.
- S. M. Johnson (Johnson bound) for the printed value compared against.
- A. E. Brouwer, table of bounds for constant weight codes, https://aeb.win.tue.nl/codes/Andw.html.
- Found and packaged by ada95ftw with the V3R1T4S kit (https://github.com/elder-plinius/V3R1T4S).
