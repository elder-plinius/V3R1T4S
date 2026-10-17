# A(34,10,8) <= 618 (Delsarte LP certificate), constant-weight-codes, partial win p2

## What
cert_A34_10_8.json, checked by verify.py in exact rational arithmetic and independently re-derived (Q via inverse eigenmatrix; primal LP optimum 114444/185), proves A(34,10,8) <= 618 from Delsarte's inequalities for J(34,8) plus the shell-counting constraint a_7 <= 8*A(26,10,7), conditional on the published upper bound A(26,10,7) <= 36 printed in Brouwer's table (still giving <= 630 if that input were only 37), which is strictly below the live tabulated upper bound 637 for this one cell.

## Check it yourself
```sh
sh verify-it-yourself/run_checks.sh
```
Expected last line: `PASS` (the line before it: `VERIFIED bound 618`). Python 3 standard library only; about a second on a laptop.

## Compared to
- Table: A. E. Brouwer, Bounds for binary constant weight codes, https://aeb.win.tue.nl/codes/Andw.html
- Cell: A(34,10,8) (mirror A(34,10,26) by complementation), printed `181-637`: upper bound 637 (unmarked; for n > 28 the page says unmarked upper bounds are Johnson bounds).
- Fetched 2026-10-17T08:02:33Z (scout) and again 2026-10-17T12:15:46Z (gate), HTTP 200, identical sha256 117899cff5af3fd00af17389595c5756050edb94cba876570cf9b76e451107f8. Details in the-record-we-beat/.
- Certified value 114444/185, so A(34,10,8) <= 618 < 637.

## Not claimed
- No new code and no new lower bound: the cell stays open (181..618).
- Not a new method. Delsarte's LP (1973) plus a classical counting row; new only as a table entry.
- The bound rests on one published input, A(26,10,7) <= 36 (A(26,10,7) printed "30-36" in the same table). The input A(26,10,7) <= 36 is the printed upper bound of "30-36" (Agrell-Vardy-Zeger 2000); with 37 the certificate would give 630, still below 637. Pure Delsarte alone gives 662.5; the win depends on the shell-counting row a_7 <= 8*A(26,10,7).
- Not optimal; a Schrijver-type SDP or more constraints may do better.
- No claim beyond this one cell.

## Credits
- P. Delsarte, An algebraic approach to the association schemes of coding theory, Philips Res. Rep. Suppl. 10 (1973): the LP method.
- E. Agrell, A. Vardy, K. Zeger, Upper bounds for constant weight codes, IEEE Trans. Inform. Theory 46 (2000) 2373-2395: the input bound and the a_x <= C(w,x)A(n-w,d,x)-style constraints.
- S. M. Johnson (Johnson bound) for the printed value compared against.
- A. E. Brouwer, table of bounds for constant weight codes, https://aeb.win.tue.nl/codes/Andw.html.
- Found and packaged by ada95ftw with the V3R1T4S kit (https://github.com/elder-plinius/V3R1T4S).
