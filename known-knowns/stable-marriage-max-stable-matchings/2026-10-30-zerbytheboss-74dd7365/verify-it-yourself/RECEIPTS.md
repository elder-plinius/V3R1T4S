# Verification Receipts

- Order: n = 19
- Men preference lists: 19 rows, each a strict permutation of 1..19
- Women preference lists: 19 rows, each a strict permutation of 1..19
- Method 1 (Irving-Leather rotation poset downset DP): 128 rotations, 95,449 memo states, count = 642,696
- Method 2 (Gusfield breakmarriage lattice traversal): 642,696 matchings visited, verified zero blocking pairs
- Dual counter agreement: agree = yes
- Comparison: OEIS A357271 record is 637,336 (+5,360, +0.84%)
