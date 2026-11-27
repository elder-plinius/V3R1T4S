"""Offer assignment files to the shared BEST/ dir (vcycle.Best rule).  Usage: python offer.py BEST SUMMARY n FILE [FILE...]"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vcycle import Best  # noqa: E402
b = Best(sys.argv[1], open(sys.argv[2], "a"))
n = int(sys.argv[3])
for f in sys.argv[4:]:
    print(n, f.split("/")[-1], b.offer(n, f, "offer.py"))
