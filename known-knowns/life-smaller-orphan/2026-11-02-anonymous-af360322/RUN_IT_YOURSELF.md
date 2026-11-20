# Run it yourself
From this package folder, in a fresh shell:
```
sh verify-it-yourself/run_checks.sh
```
Last line must be PASS (about 2-5 s). Receipts: verify-it-yourself/RECEIPTS.md.

## Regenerate and check one cube (needs a C compiler, CaDiCaL and lrat-check)
Build CaDiCaL (https://github.com/arminbiere/cadical) and lrat-check from https://github.com/marijnheule/drat-trim .
```
cc -O2 -o mcnf object/encoders/mcnf.c
cc -O2 -o tcnfc object/encoders/tcnfc.c
cc -O2 -o subseq object/encoders/subseq.c
# mcnf, 5 x 8, cube on target column 4, value V (0..31); args: h w m Bmask Smask col val (Life: 8 12)
./mcnf 5 8 4 8 12 4 V > c.cnf
cadical --lrat=true --binary=false c.cnf c.lrat ; echo $?   # 20 = UNSAT
lrat-check c.cnf c.lrat                                      # expect "c VERIFIED"
# tcnf, 5 x 8, same cube; args: h w Bmask Smask col val
./tcnfc 5 8 8 12 4 V > t.cnf ; cadical --lrat=true --binary=false t.cnf t.lrat ; lrat-check t.cnf t.lrat
```
Compare the clause count and result with the matching row of object/certificate.tsv. A 5 x 8 cube takes about 5-20
CPU-minutes and up to about 3 GB RAM. All 64 cubes are about 10 CPU-hours.

The drivers used during the run are in how-we-built-it/code/ (paths were replaced by the TOOLS and WORK variables;
set TOOLS to a folder with cadical-zig/cadical-cli and drat-trim/lrat-check). Coverage check: `./mcnf 5 8 4 8 12 > full.cnf`
then `./subseq full.cnf c.cnf 40` (see how-we-built-it/data/mcnf_NOTES.md and tcnf_NOTES.md for argument details and
how-we-built-it/data/subset_day6_seg3.txt for the recorded output).
