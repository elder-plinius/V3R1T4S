#!/bin/bash
O=../../claim/object
get(){ if [ -f $O/cert_n$1.txt ]; then cat $O/cert_n$1.txt; else xz -dc $O/cert_n$1.txt.xz; fi; }
for n in 18 19 20 21 22 23 24 25; do get $n | nice -n 19 ./semcheck $n k$n.bin > /dev/null; done
for n in 18 19 20 21 22 23 24; do m=$((n+1)); get $n | /usr/bin/time -f "%e s %M KB" nice -n 19 ./extcheck $n - k$m.bin; rm -f k$n.bin; done
rm -f k25.bin; echo DONE
