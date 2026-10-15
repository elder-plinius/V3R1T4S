# How the object was built (commands, relative to this folder)

cc -O2 -o smcount3 smcount3.c -lm && ./smcount3 climb 13 PUBLISHED_7123.prefs 11 900 book 1500 1   # the published instance is the order-13 table in a357271_1.txt converted to list form; seed 11, 900 s, kick after 1500 evaluations, single forced move (smclimb.c v2 was the binary used; smcount3.c has the same climb mode on a faster evaluator). Exact counts: python3 -I count_stable.py --prefs FILE --brute ; ./smcount3 count FILE 1
