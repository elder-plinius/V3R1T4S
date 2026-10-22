# Commands

Scan all 9482 published designs in LJCR Zenodo v1.2 `covers.json` for single-point (`R7`) and pair (`R8`) derived
covering bounds against the live table:

    python -I derived.py covers.json covers_index.tsv scout_merged_table.csv derived_beats.csv

Extract the minimum-degree derived design of `C(42,13,6)` (at point `p = 16`, degree `2207`):

    python -I derive_at_point.py zenodo_C42_13_6.txt 42 C41_12_5_derived.txt
