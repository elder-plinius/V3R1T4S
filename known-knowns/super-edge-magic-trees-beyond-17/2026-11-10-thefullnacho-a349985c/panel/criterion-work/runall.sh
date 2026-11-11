#!/bin/bash
O=../../claim/object
for n in 18 19 20; do /usr/bin/time -f "%e s %M KB" nice -n 19 ./semcheck $n < $O/cert_n$n.txt; done
for n in 21 22 23 24 25; do nice -n 19 xz -dc $O/cert_n$n.txt.xz | /usr/bin/time -f "%e s %M KB" nice -n 19 ./semcheck $n; done
echo "--- sha256"
(cd $O && nice -n 19 sha256sum -c certificates.sha256)
echo DONE
