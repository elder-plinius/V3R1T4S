# How the object was built (commands, relative to this folder)

cc -O2 -o smclimb smclimb.c && ./smclimb climb 15 PUBLISHED_27059.prefs 12 900 book 1000 1   # seed 12, 900 s, kick after 1000 evaluations, single forced move; the published instance is the order-15 table in a357271_1.txt converted to list form. Exact counts: ./smclimb count FILE 1 ; python3 -I count_stable.py --prefs FILE --brute
