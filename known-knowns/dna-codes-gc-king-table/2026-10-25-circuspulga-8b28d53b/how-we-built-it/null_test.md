# null_test for A_4^GC(19,14,9) per PREREG.md
controls: 400
best_control: 25
real: 44
real_beats_all_controls: yes
command: cd attempts/null-and-leak-auditor && code/nullsample 19 14 1 200 20000000; code/nullsample 19 14 201 400 20000000   (the first launch was cut off at seeds 98/297 and resumed at seeds 99-200 and 298-400; see PIDs.txt; the outputs are null_*.out, 400 distinct seeds)
