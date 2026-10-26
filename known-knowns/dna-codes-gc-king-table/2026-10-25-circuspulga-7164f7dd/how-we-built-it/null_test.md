# null_test for the claim cell (15,11,7) (PREREG.v2.md): 400 random-order greedy maximal codes, nullgreedy.c seeds 1..400
controls: 400
best_control: 26
real: 42
real_beats_all_controls: yes
command: cd attempts/null-and-leak-auditor/code && ./nullgreedy 15 11 1 100; ./nullgreedy 15 11 101 200; ./nullgreedy 15 11 201 300; ./nullgreedy 15 11 301 400   (argv: N D seed_from seed_to; saved as null_15_11_*.out; max size 26, seed 81)
note: the PREREG.md primary-cell null (15,12,7) also ran: 400 controls, best_control 11, real 15 (a tie with the table, not a record).
