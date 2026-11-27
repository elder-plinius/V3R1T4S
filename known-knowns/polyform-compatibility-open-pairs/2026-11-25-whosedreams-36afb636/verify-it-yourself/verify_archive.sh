#!/bin/sh
# Full proof check, for anyone who has downloaded the archive (175028808 bytes) from
# https://doi.org/10.5281/zenodo.24518087 into this package folder, and has a drat-trim binary.
# Usage, from the package folder:   DRAT_TRIM=/path/to/drat-trim sh verify-it-yourself/verify_archive.sh
# Unpacked size is about 2.7 GB; drat-trim used up to about 1.4 GB of RAM (k = 20) on the packaging machine.
set -u
A=heptiamond-MX-k2-20-proofs.tar.xz
D=${DRAT_TRIM:-drat-trim}
grep " $A\$" object/SHA256SUMS-archive.txt | sha256sum -c - || { echo FAIL; exit 1; }
mkdir -p mx-proofs && xz -dc "$A" | tar -xf - -C mx-proofs || { echo FAIL; exit 1; }
(cd mx-proofs && sha256sum -c ../object/SHA256SUMS-files.txt) || { echo FAIL; exit 1; }
bad=0
for k in $(seq 2 20); do
  r=run_unrestricted; [ "$k" -gt 8 ] && r=run_k9_20
  d=mx-proofs/work/$r/M-X/k$k/prove
  if "$D" "$d/problem.cnf" "$d/proof.drat" -t 20000 | grep -q '^s VERIFIED'; then echo "k=$k s VERIFIED"; else echo "k=$k NOT VERIFIED"; bad=1; fi
done
[ $bad -eq 0 ] && echo PASS || { echo FAIL; exit 1; }
