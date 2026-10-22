# How the certificate vectors were produced

`make_cert.py` is the producer, with the local paths replaced by `{WORKDIR}`. It is not needed to check the certificate.

For each width m = 22 and m = 24 it does the following, using two programs built from `mdtm.c`:

1. `mdtm_dbl pow m 1 80 FILE`: 80 steps of floating point power iteration of the cylinder transfer matrix, written to a vector file.
2. `mdtm_ex cw m 1 FILE 8` with environment `NTH=12` (threads), `SC=72` (scale 2^72) and `VECOUT` set: converts the vector to exact integers with 8 exact refinement steps and writes the integer vector.
3. `make_cert.py` keeps the entries at the representatives of the dihedral orbits of subsets of the m-cycle (rotations and the reflection; 96,909 orbits for m = 22 and 352,698 for m = 24), in ascending order, as 10-byte big-endian integers, concatenates the two widths, and cuts the stream into parts of at most 900,000 bytes. It writes `cert_part00.bin` to `cert_part04.bin` and `MANIFEST.txt` (sha256 of each part and of the whole).

Build commands for the programs (from the contributor's report; Apple clang on arm64 used `-mcpu=native`, use `-march=native` elsewhere):

```
cc -O3 -mcpu=native -DEXACT mdtm.c -o mdtm_ex
cc -O3 -mcpu=native mdtm.c -o mdtm_dbl
```

`mdtm.c` here is the sanitised copy (the six standard header includes use double quotes instead of angle brackets); the original has sha256 44c92bdda412d9a929dfae23b913abe7970fb1f37020d8e0c2e44cfff8ad37e6. `make_cert.py` also imports the orbit routine from the checker (`verify-it-yourself/check_p1.py`) and expects to sit next to it. The exact command lines and the run logs of the original run are not recorded in this package. Width 24 needs a large amount of memory (tens of gigabytes); the machine used was a Mac Studio with 12 threads.

This cell had no pre-registration file of its own; the proofs are in `object/PROOF.md`.
