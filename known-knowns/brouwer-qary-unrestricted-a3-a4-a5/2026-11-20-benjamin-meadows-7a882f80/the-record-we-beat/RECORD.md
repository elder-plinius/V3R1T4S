# The record we beat: A4(12,7)

Fetched by us with one plain curl request; the page itself is not included here. Times are UTC.

| item | value |
|---|---|
| URL | https://aeb.win.tue.nl/codes/quaternary-1.html |
| fetched (UTC) | 2026-11-20T14:01:15Z |
| HTTP status | 200 |
| Date header | Fri, 20 Nov 2026 14:01:16 GMT |
| Last-Modified header | Thu, 07 Sep 2017 11:17:33 GMT |
| ETag header | "1673-558979b568d40" |
| Content-Type header | text/html |
| Content-Length header | 5747 |
| sha256 of the fetched page | 85cdd35bfe053946d1ebea9eb051e026e9462a2a63c24647992151008cf60aa4 |

## Extracted cell

The table gives d horizontally (columns d = 3, 4, ...) and n vertically, with an `ub` row of upper bounds and an `lb` row of lower bounds; an `=` in the `lb` row means the value is exact. The two rows for n = 12, as they appear in the page source:

```
12ub </TD><TD></TD><TD> 419430 </TD><TD> 109226 </TD><TD> 20852 </TD><TD> 5864 </TD><TD> 1167 </TD><TD> 240 </TD><TD> 48 </TD><TD> 9 </TD><TD> 4 </TD></TR><TR><TD>
12lb </TD><TD></TD><TD> 262144 </TD><TD> 65536 </TD><TD> 8192 </TD><TD> 4096 </TD><TD> 256 </TD><TD> 128 </TD><TD> = </TD><TD> = </TD><TD> = </TD></TR><TR><TD>
```

Column d = 7: lower bound **256**, upper bound **1167**. The lower bound is a number, not `=`, so the cell is open.

Lines of the notes under the table that name A4(12,7):

- `A4(12,7) ≤ 1167.`

None of them gives a lower bound above 256.

The value 256 is attributed in the literature to Bogdanova, Brouwer, Kapralov and Ostergard 2001 (the linear [12,4,7] code over GF(4)).
