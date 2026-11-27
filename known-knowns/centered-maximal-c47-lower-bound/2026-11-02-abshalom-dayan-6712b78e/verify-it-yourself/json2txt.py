#!/usr/bin/env python3
import sys, json
c = json.load(open(sys.argv[1])); print(c['bits'], c['Lx'], c['Ly'], len(c['atoms']))
for a in c['atoms']: print(*a)
