# Commands

The search programs are standard C and Python 3 (standard library). Build the clique search with `cc -O2 -o orbsearch src/orbsearch.c` or `cc -O2 -o osg src/osg.c`.

Class-by-class search (logs/classes_target257.tsv):

```sh
python3 src/gen_groups.py 12 4 groups 8   # one element file per conjugacy class of subgroups of AGL(1, Z_12) x S_4, plus groups/manifest.tsv
cc -O2 -o orbsearch src/orbsearch.c
python3 src/run.py groups 4 12 7 257 <time limit s> <max vertices> <jobs> out 8
```

The time limit and vertex cap of the original run were not recorded; the status column of logs/classes_target257.tsv shows which groups finished. Each COMPLETE line is exact for its group.

Sampled groups (logs/sampled_*.tsv): `python3 src/runu.py plan.tsv <jobs> <deadline epoch>` for round 1 and `python3 src/runu2.py plan.tsv <jobs> <deadline epoch>` for round 2, with plan.tsv holding the rows of logs/plan_rows.tsv for this cell (without the first column). The runners call src/mkgroups.py or src/mkgroups2.py with the row's seed, so the same rows give the same group samples; they write one line per group, as in the logs.

Maximality: `cc -O2 -o maximal how-we-built-it/maximal.c && ./maximal object/A4-12-7-320words.txt 4 12 7` (output in MAXIMALITY.txt).
