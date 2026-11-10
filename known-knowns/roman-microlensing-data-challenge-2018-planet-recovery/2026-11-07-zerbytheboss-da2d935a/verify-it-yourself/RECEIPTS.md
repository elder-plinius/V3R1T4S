# Verification Receipts

- Object file: `object/roman_dc18_predictions.tsv`
- Object SHA-256: `4ca4afd4b2432bce2ecb6bbbbbf54cb75c501bd2207c6a79379cb44dcc5259ee`
- Command executed: `sh verify-it-yourself/run_checks.sh`
- Output:
  - `Verified 293 Roman DC18 events (WIN + p1 + p2 + p3 + p4): low-q=46/51 (90.20% > 41/51), false_lowq=5 <= 9 [20, 33, 52, 63, 171], 3-class=280/293 (95.56% > 268/293; CV=90/93, PSPL=71/74, USBL=119/126), p3 (log10 q < -5)=3/3 [47, 131, 152], p4 (s > 2)=10/10 [4, 53, 66, 78, 107, 152, 223, 226, 269, 281]`
  - `PASS`
- Exit status: `0`
