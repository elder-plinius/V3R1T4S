# Criterion report: maxdet-109

context: Claude Code subagent, fresh context [claude-sonnet-5-5]

Method. I read the package folder, wrote my own exact checker (fraction-free Bareiss on Python integers, cross-checked modulo three primes; sympy was not used), and made two live fetches (not shipped in this package): Rokicki's newrec page (2026-10-19T05:26:44Z, HTTP 200, sha256 35007699196345c796ff298e9ae74d0252216e9c552e46e98aaf4a9ff070083a) and the arXiv abstract page for 2608.22518 (2026-10-19T05:27:13Z, HTTP 200, sha256 8aa955cef9b47849f450b118da542b8333a5e07c6ee70e93890b3d4575799a7a). I did not fetch the Orrick archive page myself; its value is taken from the saved excerpt in the-record-we-beat/.

Clauses of the success criterion, checked literally (explicit n x n +-1 matrix; exact |det| strictly greater than the maximum of the Orrick archive value, the Math-AI-Caltech CSV value, the EinsteinArena order-51 board and any newer arXiv value; must not exceed the residue-class bound; the previous record must be strictly below that bound):

1. Explicit +-1 matrix of order 109: MET. The object has 109 rows of 109 entries, all +1 or -1.
2. Exact determinant: MET. My Bareiss run gives |det| / 2^108 = 2162897555231082049798834993796033279114137960386362436200469570917630303164899. It is divisible by 2^108 and the three-prime cross-check agrees. This equals the claimed product.
3. Strictly greater than every comparison value: MET against every source I could read.
   - Orrick archive (saved excerpt, flagged 'not proved'): 1.877483842E78. The claimed value is larger.
   - Math-AI-Caltech records CSV: no row for order 109 (saved order list: 51, 103, 107, 111, 115, 119 and others).
   - Rokicki newrec page (the page the author's notes mention): its N = 108 row (type A) gives 1.87748e78, the same as Orrick for order 109.
   - arXiv:2608.22518 v3 abstract: 'new record determinants for orders n = 3 (mod 4) between 103 and 119, as well as n = 51'. Order 109 is 1 mod 4, so the paper does not cover it.
   - EinsteinArena: per the package folder only an order-51 board exists; I did not fetch it.
   - Merged V3R1T4S PR #155 holds 291 * 27^53 = 2119202655125403624550373680790052808829003860176536932438843923020304438454497 for this order; the object's 297 * 27^53 is larger (checked exactly: 2162897555231082049798834993796033279114137960386362436200469570917630303164899 > 2119202655125403624550373680790052808829003860176536932438843923020304438454497).
4. Not above the residue-class bound (Barba, n = 1 mod 4: det^2 <= (2n-1)(n-1)^(n-1)): MET. I tested this in exact integers; the ratio to the bound is 0.74673, which matches the folder. 2n-1 = 217 is not a perfect square, so the bound is not attainable.
5. Previous record strictly below the bound: MET. Orrick's ratio to the bound is about 0.65.
6. Direction and margin: strict max. The claimed value is above every readable comparator by far more than the rounding of the quoted decimal figures.

Hidden quantifiers and null models. None found. The cell is a plain record for one order. Rokicki's N is the 0/1 order, so his N = 108 row is the +-1 order 109; it repeats the Orrick value, as expected. Not decidable from the folder: whether a newer unreported source exists (novelty role).

Open questions in the claim record (not shipped) that concern this role.
- Does Rokicki's page or a newer source list a larger determinant for order 109? Answer: Rokicki's page lists the Orrick value for this order; I found nothing larger in what I fetched.
- Is the ceiling arithmetic in the author's notes (294 for n = 109) a sign of an error elsewhere? Answer: it does not enter the criterion, which is decided by the exact determinant; I did not see those notes and the object stands on my own recomputation.
- Should the merged package (PR #155) be the standing record? Answer: yes, it is a standing value from this project and the object beats it, so the answer does not change the outcome.

confirmed_scope: The object is a 109 x 109 matrix with all entries +1 or -1 whose exact |det| / 2^108 is 2162897555231082049798834993796033279114137960386362436200469570917630303164899, strictly above the Orrick archive value 1.877483842E78, the Rokicki page value, and the sources listed above (all that I could read), and below the Barba bound, for an order where the earlier record was far below the bound. It also exceeds the merged V3R1T4S value 291 * 27^53 for this order.

pass: true
