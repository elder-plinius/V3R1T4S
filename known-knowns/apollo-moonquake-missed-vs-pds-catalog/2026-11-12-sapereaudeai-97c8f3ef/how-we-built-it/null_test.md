# null_test (p2, PREREG.v6): shifted-catalogue controls

controls: 400
best_control: 0.0484
real: 0.9403
real_beats_all_controls: yes
command: python -I attempts/evaluator-first/code/p2_null.py attempts/evaluator-first/frozen/A1_s12_dev1972_templates.npz attempts/evaluator-first/out/scan_1971/scan_s12_A1_1971.jsonl data/catalog/levent.1008weber.csv 71 null_test.md

real recall over 67 scanned catalogued 1971 A1 times; control recall mean 0.0088, median 0.0000, max 0.0484.
theta (frozen) = 0.108978
