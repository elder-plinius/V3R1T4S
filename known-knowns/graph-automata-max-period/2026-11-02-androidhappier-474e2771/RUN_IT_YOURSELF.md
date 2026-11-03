# Run it yourself (fresh shell, from this folder)

## 1. Quick checks (a few seconds)
    sh verify-it-yourself/run_checks.sh          # last line: PASS

## 2. Recompute a(9) with both programs (needs gcc and nauty 2.8.8's geng on PATH; about 6 minutes in total on 8 cores)
    FULL=1 sh verify-it-yourself/run_checks.sh   # step 6: fresh A and B outputs identical to object/evidence/, last line PASS

or by hand:

    cd how-we-built-it
    gcc -O2 -o totA totA.c && gcc -O2 -o totB totB.c
    for k in 1 2 3 4 5 6 7 8; do geng -cq $k | ./totA | head -1; done      # maxperiod 1 2 2 6 7 18 38 96
    for k in 1 2 3 4 5 6 7 8; do geng -cq $k | ./totB | head -1; done      # max_cycle 1 2 2 6 7 18 38 96
    sh run_A_n9.sh && sh run_B_n9.sh                                       # out/A_n9_part*.txt, out/B_n9_part*.txt
    grep -h '^n=' out/A_n9_part*.txt; grep -h '^order' out/B_n9_part*.txt   # counts sum to 261080, max 180
    python3 merge_parts.py out                                             # out/*_merged.txt
    for f in out/*.txt; do cmp "$f" ../object/evidence/$(basename "$f"); done   # no output: identical

Expected: the saved outputs in object/evidence/ (geng's residue split `r/8` is deterministic for a given nauty
version; with another version the per-part files may differ, but the totals and the maximum may not).

## 3. The witness alone
    python3 how-we-built-it/tstepper.py 'H?`DBbS' 0,2 175                 # preperiod=0 cycle_length=180
    python3 verify-it-yourself/check_tot.py graph 'H?`DBbS' 180            # no rule or start on this graph beats 180

## Rebuilding the object
object/VALUE.txt is a hand-written summary of the outputs above; its pins are `sha256sum` values of the files in
object/code/ and object/evidence/ (and of the geng binary used, which is not shipped).
