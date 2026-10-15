# How the object was built (commands, relative to this folder)

python3 prodGen.py JO_N7_85.prefs K2.prefs instance_n14.prefs   # JO_N7_85.prefs = Table 1 of M. Jo, Zenodo 10.5281/zenodo.23329599 (order-7 instance with 85 stable matchings), in list form; K2.prefs is the order-2 instance: men '1 2' / '2 1', women '2 1' / '1 2'. Count: python3 -I count_stable.py --prefs instance_n14.prefs --brute ; cc -O2 -o smcount3 smcount3.c -lm && ./smcount3 count instance_n14.prefs 1
