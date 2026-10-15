# How the object was built (commands, relative to this folder)

cc -O2 -o smcount3 smcount3.c -lm && ./smcount3 climb 15 START.prefs SEED SECONDS book KICK KMAX   # e.g. the published 27059 instance as START (the order-15 table in a357271_1.txt converted to list form), then the best file of each book as the next START; seeds 12, 34, 52 and kicks 1000-3000 with KMAX 1-2 were used. Exact counts: ./smcount3 count FILE 1 ; ./smcount3 enumerate FILE ; python3 -I count_stable.py --prefs FILE --brute
