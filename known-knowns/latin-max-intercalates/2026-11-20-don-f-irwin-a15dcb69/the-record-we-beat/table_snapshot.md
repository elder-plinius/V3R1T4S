# The record we beat

Table snapshot, selected headers only (the page itself is not copied in).

## A092237 (maximum number of intercalates in a Latin square of order n)

- URL: https://oeis.org/A092237/a092237_2.txt
- UTC fetch: 2026-11-20T12:20:40Z (scout); re-fetched by the novelty and criterion skeptics at 2026-11-20T13:04Z and 13:09Z
- HTTP status: 200
- sha256 of the page as fetched: 8ba511ee48a02234ce897aa943d57a69cf89be5f97e7d7d498ea9ccedec1818b
- Selected header: `n=28, a(28)>=2940`
- Extracted cell compared against: a(28) >= 2940
- Page footer date: "Aug 28 2025"

## A307164 (maximum number of intercalates in a diagonal Latin square of order n)

- URL: https://oeis.org/A307164/a307164_5.txt
- UTC fetch: 2026-11-20T12:20:40Z
- HTTP status: 200
- sha256 of the page as fetched: b21fbe9c534737beef61a8cc558699253f1f883221c9ea8c82f70807b51716ff
- Selected header: `n=28, a(28)>=2892`
- Extracted cell compared against: a(28) >= 2892
- Page footer date: "Aug 28 2025"

## The comment blocks

- https://oeis.org/A092237 and https://oeis.org/A307164 returned HTTP 403 (Cloudflare challenge page) at
  2026-11-20T12:20:40Z and again at 12:20:57Z from the run's own client. They were read successfully by the
  CRITERION skeptic at 2026-11-20T13:09Z with one honest request, and corroborate a(28) >= 2940 (A092237) and
  a(28) >= 2892 (A307164).

## Bar used

The maximum across both sequences for n = 28: **2940**. The object's value is 3324.
