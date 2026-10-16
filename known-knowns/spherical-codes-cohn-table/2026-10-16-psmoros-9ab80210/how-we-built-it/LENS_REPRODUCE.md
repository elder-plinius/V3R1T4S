# REPRODUCE (brute-scale lens, run 2026-10-16-0024)

Status of every claim here: NUMERICAL, single-context, unpanelled (no skeptic has seen it). The table comparison
uses the run's snapshot of https://spherical-codes.org/plain (data/sc/plain.csv, fetched 2026-10-16T00:28Z) and of
the HTML index (data/sc/index_parsed.tsv); the main session must re-fetch both at the gate (rows change fast).

## 1. Verify every claimed code (fresh shell)

Needs python3 with mpmath (the run's venv has it: WORKDIR/venv/bin/python). From the lens folder:

    cd <RUN>/attempts/brute-scale
    python3 -I code/verify_all.py                      # snapshot plain.csv
    python3 -I code/verify_all.py /path/to/fresh/plain.csv   # after re-fetching /plain

verify_all.py reads result/claims.csv and, for each row, checks the sha256 of result/d<d>_N<N>.txt, the shape,
>= 20 significant digits per coordinate, computes c* over ALL N(N-1)/2 pairs in mpmath at 50 digits (no float
screen), and checks gain = c_table - c* >= 1e-10 and the kissing exclusion. Expected last line: ALL_OK
(captured: out/verify_all_*.txt).

Independent second and third checks (numpy + mpmath, float screen 1e-7 then mpmath):

    python3 -I code/bs_check.py result/d28_N59.txt 28 59 --plain ../../data/sc/plain.csv --bar ../../data/sc/bar_table.tsv
    python3 -I ../../code/sc_check.py result/d28_N59.txt 28 59 --table ../../data/sc/plain.csv \
        --index ../../data/sc/index_parsed.tsv --require-digits 20

(captured for every claim in out/bs_check_d*_N*.json and out/sc_check_d*_N*.json; bs_check also prints the gain
below Vahteristo's archive cosine and the star / NMO flags.)

## 2. How each code was found (record; not needed to verify)

All starts are posted codes of neighbouring rows, fetched once each through code/sccache.py (shared cache).
"minus k" = delete k points of the posted (d, N+k) code, then polish.

| row | table holder (snapshot) | start | search | file |
|---|---|---|---|---|
| (28,59) | Vahteristo | Cohn's (28,61) [poly] minus 2 | mbh.py worker 2b (485 s MBH) + polish_final.py (90 s) | result/d28_N59.txt |
| (30,73) | Vahteristo | Ozgen's (30,74) minus 1 | mbh.py 2b (512 s) + 2c continuation (723 s, start=file) | result/d30_N73.txt |
| (30,64) | Vahteristo | Cohn's (30,65) minus 1 | mbh.py 2c (start already below; MBH hops 2-9) | result/d30_N64.txt |
| (32,108) | Vahteristo | Ozgen's (32,109) minus 1 | mbh.py 2d (615 s MBH) | result/d32_N108.txt |
| (6,551) | A. Jay | Cohn's NMO (6,552) minus 1 | h3sweep.py s1 | result/d6_N551.txt |
| (6,571) | A. Jay | Cohn's NMO (6,572) minus 1 | h3sweep.py s3 | result/d6_N571.txt |
| (8,152) | A. Jay | Vahteristo's (8,153) minus 1 | h3sweep.py s3 | result/d8_N152.txt |
| (8,511) | A. Jay | Cohn's NMO (8,512) minus 1 | h3sweep.py s5 | result/d8_N511.txt |
| (6,116) | H. Cohn | Cohn's NMO (6,117) minus 1 | h3sweep.py s5 | result/d6_N116.txt |
| (8,440) | A. Jay | Cohn's NMO (8,441) minus 1 | h3sweep.py s5 | result/d8_N440.txt |
| (7,748) | A. Jay | Cohn's NMO (7,749) minus 1 | h3sweep.py s7 (1 start, FINE 800 its) | result/d7_N748.txt |
| (6,526) | Vahteristo | Cohn's NMO (6,527) minus 1 | h3sweep.py s8 | result/d6_N526.txt |
| (6,525) | Vahteristo | our (6,526) code minus point 181 (no optimisation) | deletion only | result/d6_N525.txt |
| (5,433) | A. Jay | Cohn's NMO (5,434) minus 1 | h3sweep.py s8 | result/d5_N433.txt |
| (8,447) | A. Jay | Cohn's NMO (8,448) minus 1 | h3sweep.py s9 | result/d8_N447.txt |
| (27,130) | Vahteristo | Ozgen's (27,131) minus 1 | mbh.py worker 5 (380 s MBH) | result/d27_N130.txt |

Build and rerun (stochastic; CPU-share dependent):

    cd <RUN>/attempts/brute-scale/code
    clang -O3 -mcpu=native -shared -fPIC -o liblse2.so lse2.c -framework Accelerate
    clang -O3 -mcpu=native -shared -fPIC -o liblse3.so lse3.c -framework Accelerate
    # h3sweep rows, e.g. (8,152):
    echo "8 152 1" > ../out/cands_repro.txt
    OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -I h3sweep.py repro ../out/cands_repro.txt $(( $(date +%s) + 900 )) --cap 60 --tries 6
    # mbh rows, e.g. (28,59):
    echo "28 59 480 h3 minus2" > ../out/rows_repro.txt
    OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -I mbh.py repro ../out/rows_repro.txt $(( $(date +%s) + 600 )) \
        --seed 2002 --kinds gauss:0.6,reseed:0.15,cap:0.1,evict:0.15
    python3 -I polish_final.py ../out/best/d28_N59_wrepro.txt 28 59 ../out/best/d28_N59_repro_polished.txt 90

## 3. Optimizer sanity control (PREREG)

- h3sweep configuration: out/wctrl_results.jsonl (18 starred-row candidates, identical settings): no starred row
  beaten by >= 1e-10 (largest 3.3e-13 = rounding of the table's 0.166666666667 for (4,10)).
- mbh.py configuration (posted start): out/w1/w2/w3_results.jsonl starred rows (10 rows, 180 s): gain 0 on all.
- mbh.py configuration (minus2 start, kinds incl. evict, as used for the four mbh.py claims): out/w2d_results.jsonl
  (10 starred rows, gain 0 on all; on (8,240), (21,162), (22,100) no hop finished inside the cap).
- precise polish (polish_final.py) on 8 starred posted codes: out/ctrl_precise_polish_starred.txt (max change 5.6e-17).
