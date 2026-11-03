# Exact commands used to build the result (from this folder, Linux x86-64, gcc, Go, nauty 2.8.8 geng)

    gcc -O3 -march=native -o totF totF.c                       # Program A (the run used -O3 -march=native)
    mkdir -p B && cp main.go go.mod B/ && (cd B && go build -o ../totBgo .)   # Program B
    for k in 1 2 3 4 5 6 7 8 9; do geng -cq $k | ./totF | grep '^n='; done      > A_n1_9.txt   # 1 2 2 6 7 18 38 96 180
    for k in 1 2 3 4 5 6 7 8 9; do geng -cq $k | ./totBgo nbr | grep '^n='; done > B_n1_9.txt   # same maxima
    mkdir -p out
    seq 0 31 | xargs -P 8 -I{} sh runA.sh 10 {} 32               # out/A10_r{0..31}of32.txt, ~2 core-hours
    seq 0 31 | xargs -P 8 -I{} sh runB.sh 10 {} 32               # out/B10_r{0..31}of32.txt, ~12+ core-hours
    mkdir -p A B && cp out/A10_* A/ && cp out/B10_* B/ && python3 compare_AB.py A B   # VERDICT AGREE M = 624
    python3 stepper.py 'I?AAD@oIg' 0,2 2                          # preperiod=0 cycle_length=624

Each output file is complete only if it contains a line `fnv <hex>` (FNV-1a hash of the per-graph maxima in geng
order); runA.sh/runB.sh skip a class whose output is already complete, so a stopped run can be resumed.

runA.sh and runB.sh here are the run's driver scripts with one change: the run called geng by its absolute path in
the workspace; here it is `${GENG:-geng}`. The run's originals had sha256
8c465b2293e05c1522432e81f37fb5ad3c4ec22de59ff383eb53167e7e347baa (runA.sh) and
27504d307c2851b117c3b7cc1b9dc850eb16668afc02a7027022d82a423ecafb (runB.sh); they are pinned in the run's claim
record, not in object/VALUE.txt. The geng binary itself (sha256 75d1bf01…f450) is pinned in object/VALUE.txt as
tools/geng but not shipped.

During the run the A and B workers were paused (SIGSTOP) for about 1 h 38 min to share the machine and then resumed
(SIGCONT); every class still finished with its `fnv` line, and the reproduce skeptic's own full recompute and a fresh
B rerun of class 7 match the saved outputs, so the pause did not affect them.

Supporting checks (object/code/): spot.py recomputes per-graph maxima in pure Python over all 1024 rules (no degree
pruning) for a 170-graph sample and A's top 20 graphs (object/evidence/spot.txt, spot_top20.txt: 0 mismatches);
small_exhaustive.py brute-forces n <= 8 (object/evidence/python_small_exhaustive.txt).
