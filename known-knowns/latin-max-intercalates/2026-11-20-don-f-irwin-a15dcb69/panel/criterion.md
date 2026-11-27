context: headless hermes CLI

# CRITERION verdict — latin-max-intercalates, n = 28

## 1. Order in range
n = 28. In range 10..28, and 28 is neither 15 nor 16. Satisfied.

## 2. Explicit Latin square (verified independently)
`claim/square_n28_3324.txt`, sha256 a15dcb69db4d57903112555c0389b10b87dbf49be6b0ebdd660d7f6a867cf99b,
28 lines x 28 space-separated integers 0..27 (no ragged rows; symbol set exactly {0..27}).
I verified it myself, not via the author's helpers: every row is a permutation of 0..27 and every column is a
permutation of 0..27. It is a genuine Latin square of order 28.

## 3. Two independent programs agree
- countA.py (row-pair / position scan, literal definition):  latin = true, intercalates = 3324
- countB.py (per-row-pair permutation, counts transpositions):  latin = true, intercalates = 3324

Both print 3324. I did not stop there: a third, separate brute-force enumeration over all
C(28,2) x C(28,2) = 378 x 378 row-pair/column-pair intersections also returns 3324. Three independent
methods agree, so the number is solid.

## 4. Strictly greater than the bar (re-fetched immediately before claiming)
All four sources were fetched live at claim time (2026-11-20), and all four were readable this time:
- A092237 comment page: a(28) >= 2940
- A092237 proving list a092237_2.txt header: "n=28, a(28)>=2940"
- A307164 comment page: a(28) >= 2892
- A307164 proving list a307164_5.txt header: "n=28, a(28)>=2892"

Largest bound for n = 28 across both sequences = max(2940, 2892) = 2940. Is 3324 > 2940? Yes, strictly,
by 384.

Note on the numbers in the criterion text: the comment pages now display some values that differ from the
"2026-10-30 values" quoted in the criterion (A092237 a(23) is 983, not 985; a(27) is 648, not 1372;
a(21) is 1026, not 884). None of these discrepancies touch n = 28: both the comments and both proving-list
headers agree on 2940 as the A092237 n=28 bound, and 2892 as the A307164 n=28 bound. The bar used is 2940.

## 5. Proven bound respected
Even-order bound n^2(n-1)/4 = 28*28*27/4 = 5292. Count 3324 <= 5292, so no contradiction with
Heinrich–Wallis. (3324/5292 ≈ 0.63.)

## 6. Caveat: were the comment pages readable?
Yes — at this fetch both A092237 and A307164 comment pages returned content (no 403), and they corroborate
the proving-list headers. The claim folder's own CLAIM.md said the comment pages had been 403/Cloudflare at
an earlier time and recorded them as "PENDING TABLE CHECK"; that caveat is now resolved in favor of the
claim, since the comment values independently confirm 2940 and 2892 for n = 28.

Because the criterion names BOTH "comments and the ... proving-list headers", the literal reading requires
the bound to be checked in both. It was, and both agree for n = 28. Had the comments been unreadable, the
literal criterion would be only partially evidenced (proving-list headers alone), but here that is moot.

## 7. One more point about the object (not a defect)
The square is the direct product of the order-2 square (source_n2.txt) with the published order-14 square
(source_n14.txt); I confirmed it equals that product under (i1,i2) -> i1*14 + i2. Being a composite
construction does not affect any clause of the criterion: the criterion asks only for an explicit Latin
square of order n with the stated count. The order-14 factor has 391 intercalates (itself the A092237
a(14) value); the product amplifies to 3324, consistent with the "composite squares" method already used
in the proving lists.

## Verdict
All clauses are satisfied:
- n = 28 in range, not 15/16
- explicit Latin square, rows and columns independently verified
- count 3324 agrees across two independent programs (and a third brute-force check)
- 3324 strictly greater than the re-fetched bar 2940 (max over comments and proving-list headers of both sequences)
- 3324 <= proven bound 5292

confirmed_scope: An explicit order-28 Latin square with 3324 intercalates, strictly exceeding the 2940 bar read from the comments and proving-list headers of A092237 and A307164, and below the proven bound 5292.

pass: true
