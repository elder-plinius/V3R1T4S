# How the object was built (commands, relative to this folder)

python3 prodGen.py JO_N7_85.prefs K2.prefs n14.prefs && python3 prodGen.py n14.prefs K2.prefs instance_n28.prefs   # JO_N7_85.prefs = Table 1 of M. Jo, Zenodo 10.5281/zenodo.23329599 (order-7 instance with 85 stable matchings) in list form; K2.prefs is the order-2 instance: men '1 2' / '2 1', women '2 1' / '1 2'. Count: cc -O2 -o smcount3 smcount3.c -lm && MEMO_MAX_STATES=40000000 ./smcount3 count instance_n28.prefs 0 ; FULL=1 sh verify-it-yourself/run_checks.sh for the 45-minute verified enumeration
