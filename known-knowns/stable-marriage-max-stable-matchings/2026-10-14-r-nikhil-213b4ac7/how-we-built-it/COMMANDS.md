# How the object was built (commands, relative to this folder)

python3 prodGen.py OUTER.prefs K2.prefs instance_n22.prefs   # OUTER = the order-11 table in a357271_1.txt converted to list form (1690 stable matchings); K2.prefs is the order-2 instance: men '1 2' / '2 1', women '2 1' / '1 2'. Count: cc -O2 -o smcount3 smcount3.c -lm && ./smcount3 count instance_n22.prefs 1 && ./smcount3 enumerate instance_n22.prefs
