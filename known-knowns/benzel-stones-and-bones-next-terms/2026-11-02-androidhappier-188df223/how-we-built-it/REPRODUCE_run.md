# REPRODUCE (run inside a copy of claim/; needs gcc with OpenMP and python3 stdlib; 8 cores, ~4 GB free RAM for n=20)

```bash
mkdir -p $TMPDIR/bz
gcc -O3 -march=native -fopenmp -o $TMPDIR/bz/benzZQ   code/benzZQ.c
gcc -O3 -march=native -fopenmp -o $TMPDIR/bz/benzB64  code/benzB64.c
gcc -O3 -march=native -fopenmp -o $TMPDIR/bz/benzB128 code/benzB128.c

# 1. Saved outputs vs OEIS DATA (seconds): expect last line "RESULT PASS"
python3 code/repro_matrix.py

# 2. The new term, Program A (~40 min on 7 threads, peak ~3.5 GB):
BENZ_M=5 OMP_NUM_THREADS=7 $TMPDIR/bz/benzZQ 20 37 3            # stdout 225354012176304818, stderr ends "... overflow=0"
# 3. The new term, Program B (~40 min on 7 threads, peak ~3.5 GB; do not run 2 and 3 at the same time on 16 GB):
OMP_NUM_THREADS=7 $TMPDIR/bz/benzB64 20 37 3 5                   # stdout 225354012176304818, stderr ends "max states ... overflow 0"

# 4. Published terms (n = 3..16 take minutes; 17..20 take from 5 to ~60 min each):
for n in $(seq 3 16); do
  echo "A364416($n) A=$(BENZ_M=5 OMP_NUM_THREADS=4 $TMPDIR/bz/benzZQ $n $((2*n-4)) 3 2>/dev/null) B=$(OMP_NUM_THREADS=4 $TMPDIR/bz/benzB128 $n $((2*n-4)) 3 5 2>/dev/null)"
  echo "A364417($n) A=$(BENZ_M=5 OMP_NUM_THREADS=4 $TMPDIR/bz/benzZQ $n $((2*n-3)) 3 2>/dev/null) B=$(OMP_NUM_THREADS=4 $TMPDIR/bz/benzB128 $n $((2*n-3)) 3 5 2>/dev/null)"
done                                                          # compare with data/A364416.txt, data/A364417.txt

# 5. Definition-level checker (no transfer matrix), small n:
python3 code/indep_check.py 8 3                              # see result/out_indep_n3_8.txt
```

Checkpointing (optional, Program A): `BENZ_CKPT=$TMPDIR/ck.bin BENZ_CKPT_SEC=600` writes a checkpoint; rerunning the same
command with the same BENZ_CKPT resumes ("resumed t=..."). The saved A run on (20,37) used it once (result/A_final).
