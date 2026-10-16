#!/bin/sh
cd "$(dirname "$0")/.." || { echo FAIL; exit 1; }
EXPECT=5718dbe13ad14876665fd9a66ad86848ddc43fc5ef9aff96aa6a228f755a2c61
GOT=$(python3 -c "import hashlib;print(hashlib.sha256(open('object/scu507_refined.txt','rb').read()).hexdigest())")
echo "object sha256 $GOT"
if [ "$GOT" != "$EXPECT" ]; then echo "object sha256 differs from the published one"; echo FAIL; exit 1; fi
if python3 verify-it-yourself/check_scu_p3.py; then echo PASS; else echo FAIL; exit 1; fi
