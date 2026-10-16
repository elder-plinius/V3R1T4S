# How the object was built (exact commands, from the run folder)
Requirements: python3 3.9 standard library; numpy and pypdf (any recent version) in a virtual environment.
1. Fetch arXiv:2607.09688v1 (https://arxiv.org/pdf/2607.09688v1) and extract its text with pypdf to arxiv_2607.09688v1.txt.
2. python3 parse_table3.py arxiv_2607.09688v1.txt   -> table3_records.json (35 rows; all reproduce the printed F).
3. python operators.py table3_records.json          -> operator scan over all 35 records (end extensions, interior
   insertions and deletions); its best L = 463 candidate is "-" + (Table 3 record for L = 461) + "+", E = 14047.
Rebuild by hand: take the L = 461 row of Table 3 of arXiv:2607.09688v1, decode it (last 461 bits, 0 -> -1), prepend "-"
and append "+".
