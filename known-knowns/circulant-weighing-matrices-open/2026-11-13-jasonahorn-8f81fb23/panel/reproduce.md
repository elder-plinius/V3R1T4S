context: hermes delegation

Own periodic autocorrelation of a length-208 sequence with entries in {-1,0,1}, written and tested before reading the search code in liftjoin.c:

- all-zero: 0 at every nonzero shift (C(0)=0)
- single +1: 0 at every nonzero shift (C(0)=1)
- two adjacent +1: C(1)=1, nonzero at shift 1 (also C(207)=1)

`cc -O3 -o liftjoin liftjoin.c && ./liftjoin all 180` finished, exit 0, not a sample. Last line:

END nodes=43196762 hits=0 capped=0 elapsed=30 targets=25 matches=5519232

That line contains hits=0 and capped=0.

`python3 indep_join.py` finished, exit 0. It printed `targets 25` and its last line was:

MATCHES 0

All three required checks agree.

pass: true
