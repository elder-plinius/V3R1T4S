# The record we beat: A3(15,10)

Fetched by us with one plain curl request; the page itself is not included here. Times are UTC.

| item | value |
|---|---|
| URL | https://aeb.win.tue.nl/codes/ternary-1.html |
| fetched (UTC) | 2026-11-20T14:01:14Z |
| HTTP status | 200 |
| Date header | Fri, 20 Nov 2026 14:01:15 GMT |
| Last-Modified header | Sat, 17 Oct 2026 19:57:34 GMT |
| ETag header | "2727-65e0eb1272e91" |
| Content-Type header | text/html |
| Content-Length header | 10023 |
| sha256 of the fetched page | 72a5f8906bbfdd9046dec9413901c0c44deb3124ac40530b0eb41214d5c91642 |

## Extracted cell

The table gives d horizontally (columns d = 3, 4, ...) and n vertically, with an `ub` row of upper bounds and an `lb` row of lower bounds; an `=` in the `lb` row means the value is exact. The two rows for n = 15, as they appear in the page source:

```
15ub </TD><TD></TD><TD> 434815 </TD><TD> 149585 </TD><TD> 29213 </TD><TD> 9904 </TD><TD> 2204 </TD><TD> 685 </TD><TD> 165 </TD><TD> 39 </TD><TD> 10 </TD><TD> 6 </TD><TD> 3 </TD><TD> 3 </TD></TR><TR><TD>
15lb </TD><TD></TD><TD> 354294 </TD><TD> 83106 </TD><TD> 7929 </TD><TD> 3321 </TD><TD> 729 </TD><TD> 243 </TD><TD> 81 </TD><TD> 27 </TD><TD> = </TD><TD> = </TD><TD> = </TD><TD> = </TD></TR><TR><TD>
```

Column d = 10: lower bound **27**, upper bound **39**. The lower bound is a number, not `=`, so the cell is open.

Lines of the notes under the table that name A3(15,10):

- `A3(15,10) ≤ 39, A3(16,10) ≤ 117.`

None of them gives a lower bound above 27.

The value 27 is attributed in the literature to Bitan and Etzion 1995 (via Brouwer, Hamalainen, Ostergard and Sloane 1998).
