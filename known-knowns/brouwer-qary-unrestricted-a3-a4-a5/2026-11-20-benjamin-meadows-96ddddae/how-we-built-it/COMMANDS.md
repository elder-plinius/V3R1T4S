# Commands

The search programs are standard C and Python 3 (standard library). Build the clique search with `cc -O2 -o orbsearch src/orbsearch.c` or `cc -O2 -o osg src/osg.c`.

Sampled groups (logs/sampled_*.tsv): `python3 src/runu.py plan.tsv <jobs> <deadline epoch>` for round 1 and `python3 src/runu2.py plan.tsv <jobs> <deadline epoch>` for round 2, with plan.tsv holding the rows of logs/plan_rows.tsv for this cell (without the first column). The runners call src/mkgroups.py or src/mkgroups2.py with the row's seed, so the same rows give the same group samples; they write one line per group, as in the logs.

Maximality: `cc -O2 -o maximal how-we-built-it/maximal.c && ./maximal object/A4-11-7-145words.txt 4 11 7` (output in MAXIMALITY.txt).
