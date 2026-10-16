# How the object was built (exact commands, from the run folder of the run that found it)
Requirements: python3 3.9 standard library; numpy and pypdf (any recent version) in a virtual environment.
1. Fetch arXiv:2607.09688v1 (https://arxiv.org/pdf/2607.09688v1) and extract its text with pypdf to arxiv_2607.09688v1.txt.
2. python3 parse_table3.py arxiv_2607.09688v1.txt   -> table3_records.json (35 rows; all reproduce the printed F).
3. python operators.py table3_records.json          -> operator scan over all 35 records (end extensions of 0..2
   symbols, interior insertions and deletions); its best L = 464 candidate is "--" + (Table 3 record for L = 461) + "+",
   E = 14396 (12 operator paths reach the same energy).
PREREG.md here is the rule frozen before that scan (scope: the 35 Table 3 lengths, threshold E <= table E - 4).
Rebuild by hand: take the L = 461 row of Table 3 of arXiv:2607.09688v1, decode it (last 461 bits, 0 -> -1), prepend "--"
and append "+".
