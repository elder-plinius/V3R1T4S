#!/bin/sh
# Rebuild the large certificates (numpy needed; ~1-6 min each on one core). Run from how-we-built-it/:
#   sh regenerate.sh OUTDIR
# then compare with the hashes of the decompressed text in code/../LARGE_FILES.md  (zcat FILE | sha256sum).
set -e
O=${1:-regen}; mkdir -p "$O"
nice python3 code/mkcert.py 9/20 2000 67005787/100000000 max "$O/upper_a45_T2000_rho67005787.txt.gz" 0.98
nice python3 code/mkcert.py 9/20 2000 67005785/100000000 max "$O/NEG_dual_a45_T2000_rho67005785.txt.gz" 1.02
nice python3 code/mkcert.py 9/20 2000 67005785/100000000 corrected "$O/NEG_pol_a45_T2000_rho67005785.txt.gz" 0.98 "$O/NEG_pol_a45_T2000_rho67005785.pol.gz"
nice python3 code/mkcert.py 9/20 1500 67005786/100000000 under "$O/lower_a45_T1500_rho67005786.txt.gz" 0.98 "$O/lower_a45_T1500_rho67005786.pol.gz"
