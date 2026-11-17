# REPRODUCE (fresh shell, inside a copy of this claim/ folder; needs gcc, python3, gzip)

```
gcc -O2 -o acclist source/acclist.c
gcc -O2 -o count source/count.c
gcc -O2 -o count2 source/count2.c

# 1. the SM list: regenerate, compare, check (seconds)
./acclist 11 0 | gzip -1 > SM_q11.txt.gz
zcat SM_q11.txt.gz | sha256sum          # expect 723e21fb...0667d68 (object/counts.txt)
zcat object/SM_q11.txt.gz | sha256sum   # same
python3 checker/check_list.py 11 0 SM_q11.txt.gz      # expect "valid solutions: 37005" then PASS

# 2. the SMnuR list: regenerate (about 1 min, about 2.5 GB RAM), hash, check (about 15 min)
./acclist 11 1 | gzip -1 > SMnuR_q11.txt.gz
zcat SMnuR_q11.txt.gz | sha256sum       # expect f4e16ec8...96dbdaf4
python3 checker/check_list.py 11 1 SMnuR_q11.txt.gz   # expect "valid solutions: 45378377" then PASS

# 3. independent counts (different algorithm: raw count of all sorted-triple solutions, then Burnside for the
#    sign and Moebius for common factors); conventions.py prints several conventions; the published one is prim_incl0
for q in $(seq 1 11); do ./count $q 0; done > N_sm.txt;  (cd source && python3 conventions.py ../N_sm.txt 0)
for q in $(seq 1 11); do ./count $q 1; done > N_nu.txt;  (cd source && python3 conventions.py ../N_nu.txt 1)
./count2 11 1; ./count2 11 0                            # same raw N as ./count
# expect prim_incl0 = 37006 at SM Q_max 11 and 45378378 at SMnuR Q_max 11, and the published values at
# SM Q_max 1,3,5,7,10 and SMnuR Q_max 6..10 (status.md)
```

Every published value in status.md is reproduced by the same programs under the same convention (calibration).
