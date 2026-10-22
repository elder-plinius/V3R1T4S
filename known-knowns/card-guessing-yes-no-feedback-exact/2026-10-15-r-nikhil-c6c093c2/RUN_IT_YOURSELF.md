# Run it yourself (fresh shell, from this folder)

## Verify (standard-library Python 3)
    sh verify-it-yourself/run_checks.sh
Expected output ends with `PASS` (about 3 minutes): the shipped certificates n = 2..9 and the claimed n = 11
certificate (reassembled from object/cert/n11.txt.gz.part-*) verified on every state against values.json.
    FULL=1 sh verify-it-yourself/run_checks.sh     # also n = 10, 12, 13 (shipped in parts)
    FULL=2 sh verify-it-yourself/run_checks.sh     # also recompute P+_{2,11} from scratch
To reassemble a shipped certificate by hand: `cat object/cert/n13.txt.gz.part-* > n13.txt.gz`. The reassembled files are
byte-identical to the originals; sha256 of the gzip files: n10 692351f7c01e7a5dec72944c71cceb4f69cfa8fcf6baa72cd2d1584f18fa6b90; n11 a76e7b21d9077161148ab470fcb87ee54be74bab3cee9c0a3b4ca54200da052a; n12 a34b63f5023bdfe691d6e132ed8edcbc2d5f6868de6da5c43cbc1c2c624a7748; n13 6763774ff4ee481f9bd1c2883d0c93a9f43eba0c36ad520451a6367e0072a996.

## Verify the large certificates (n = 10..16)
They are not in git (50 MB to 224 MB each; n = 10..13 are shipped in parts). Download them from the archive URL below, check their sha256 against
README.md, put them into object/cert/, and rerun the script; each certificate present is verified on every state
(n = 16: about 30 minutes, 1.5 GB). Archive URL: ARCHIVE_URL_TO_BE_ADDED_BY_THE_SUBMITTER.
Single file: `python3 -I verify-it-yourself/verify_cert.py object/cert/n16.txt.gz --claimed 287519620950287971428538054033/95596617538340806567680000000`
(`--literal` evaluates the rational recursion with fractions as well; `--persistence` also tests the 1981 persistence
conjecture on every state).

## Fast verification of the large certificates (C++17, GMP, zlib; optional)
    c++ -O2 -std=c++17 verify-it-yourself/cg_verify.cpp -o cg_verify -lgmp -lz     # add -I/-L for your GMP location
    ./cg_verify object/cert/n16.txt.gz --claimed 287519620950287971428538054033/95596617538340806567680000000 --persistence
Same checks as verify_cert.py (C recomputed from (A.1) for every state, two layers in memory); n = 16 in a few minutes
and under 1 GB; n = 17 in about 6 minutes.

## Recompute from scratch (no certificate needed)
    python3 -I verify-it-yourself/recompute_value.py 12 2 --expect 228254911260131056513/75738330289702080000
(about 6 minutes; n = 13 about 15 minutes; larger n needs the C++ solver below).

## Rebuild the certificates (C++17, GMP, zlib)
    c++ -O2 -std=c++17 how-we-built-it/cg_solver.cpp -o cg_solver -lgmp -lz     # add -I/-L for your GMP location
    ./cg_solver 16 2 n16.txt.gz          # about 13 minutes, 1.1 GB; prints the value as a JSON line
The decompressed text is byte-identical to the archived certificate (deterministic layer order and sorted states).

## Raw-definition brute force on tiny decks (no sufficient statistic assumed)
    python3 -I how-we-built-it/bruteforce_raw_definition.py 4 2     # P+ = 1279/420 (about 80 s)
