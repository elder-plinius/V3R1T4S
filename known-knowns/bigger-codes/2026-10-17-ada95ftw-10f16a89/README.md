# A(32,10,7) <= 131 (Delsarte LP certificate), constant-weight-codes, partial win p2

## What
An exact rational LP dual certificate in cert_A32_10_7.json combines the Delsarte inequalities D1 and D2 for J(32,7) with the standard distance-distribution constraint a_7 <= A(25,10,7) <= 32, whose input follows from A(24,10,6) <= 9 by Johnson; verify.py and an independent recomputation check it, and it proves A(32,10,7) <= 131, strictly below the upper bound 139 printed for that single cell in Brouwer's live Andw.html table as fetched on 2026-10-17.

## Check it yourself
```sh
sh verify-it-yourself/run_checks.sh
```
Expected last line: `PASS` (the line before it: `VERIFIED bound 131`). Python 3 standard library only; about a second on a laptop.

## Compared to
- Table: A. E. Brouwer, Bounds for binary constant weight codes, https://aeb.win.tue.nl/codes/Andw.html
- Cell: A(32,10,7) (mirror A(32,10,25) by complementation), printed `64-139`: upper bound 139 (unmarked; for n > 28 the page says unmarked upper bounds are Johnson bounds).
- Fetched 2026-10-17T08:02:33Z (scout) and again 2026-10-17T12:15:46Z (gate), HTTP 200, identical sha256 117899cff5af3fd00af17389595c5756050edb94cba876570cf9b76e451107f8. Details in the-record-we-beat/.
- Certified value 46624/355, so A(32,10,7) <= 131 < 139.

## Not claimed
- No new code and no new lower bound: the cell stays open (64..131).
- Not a new method. Delsarte's LP (1973) plus a classical counting row; new only as a table entry.
- The bound rests on one published input, A(25,10,7) <= 32 (A(25,10,7) printed "28-32" in the same table). The input A(25,10,7) <= 32 is the printed upper bound of the range "28-32" (unmarked for n <= 28, so from Agrell-Vardy-Zeger 2000). The REPRODUCE skeptic also re-proved it from A(24,10,6) <= 9 (counting) and Johnson.
- Not optimal; a Schrijver-type SDP or more constraints may do better.
- No claim beyond this one cell.

## Credits
- P. Delsarte, An algebraic approach to the association schemes of coding theory, Philips Res. Rep. Suppl. 10 (1973): the LP method.
- E. Agrell, A. Vardy, K. Zeger, Upper bounds for constant weight codes, IEEE Trans. Inform. Theory 46 (2000) 2373-2395: the input bound and the a_x <= C(w,x)A(n-w,d,x)-style constraints.
- S. M. Johnson (Johnson bound) for the printed value compared against.
- A. E. Brouwer, table of bounds for constant weight codes, https://aeb.win.tue.nl/codes/Andw.html.
- Found and packaged by ada95ftw with the V3R1T4S kit (https://github.com/elder-plinius/V3R1T4S).
