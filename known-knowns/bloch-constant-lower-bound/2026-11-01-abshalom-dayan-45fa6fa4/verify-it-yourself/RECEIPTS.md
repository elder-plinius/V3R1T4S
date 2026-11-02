# Receipts: real output of verify-it-yourself/run_checks.sh

Without FLINT_PY, 2026-11-01 about 02:49Z (last line PASS):
```
PASS T=0.0155 eta=0 rho0=0 leaves=14107 (cert=13501 excl=289 out=317) witnesses=10379 minorants=1 evals=1236298 min_margin=1.1720e-11 min_excl_margin=1.0923e-08 max|c|<=0
PASS cover: leaves=14107 kinds={0: 13501, 2: 317, 1: 289} residual_stack=1 volume=1
PASS T=0.0155 eta=0.2 rho0=0.19999980926513672 leaves=454 (cert=201 excl=21 out=232) witnesses=160 minorants=3 evals=14074 min_margin=5.0725e-10 min_excl_margin=2.7545e-0
PASS cover: leaves=454 kinds={0: 201, 2: 232, 1: 21} residual_stack=1 volume=1
PASS T=0.0155 eta=0.3 rho0=0.29999923706054688 leaves=356 (cert=107 excl=17 out=232) witnesses=97 minorants=3 evals=6697 min_margin=7.6735e-09 min_excl_margin=2.2171e-05 
PASS cover: leaves=356 kinds={0: 107, 2: 232, 1: 17} residual_stack=1 volume=1
PASS T=0.0155 eta=0.4 rho0=0.39999961853027344 leaves=344 (cert=94 excl=18 out=232) witnesses=84 minorants=3 evals=5714 min_margin=2.9010e-08 min_excl_margin=6.8099e-07 m
PASS cover: leaves=344 kinds={0: 94, 2: 232, 1: 18} residual_stack=1 volume=1
PASS T=0.0155 eta=0.5 rho0=0.5 leaves=310 (cert=65 excl=14 out=231) witnesses=63 minorants=3 evals=3445 min_margin=5.0899e-07 min_excl_margin=4.6988e-05 max|c|<=0.05772 c
PASS cover: leaves=310 kinds={0: 65, 2: 231, 1: 14} residual_stack=1 volume=1
PASS T=0.0155 eta=0.6 rho0=0.59999942779541016 leaves=311 (cert=69 excl=10 out=232) witnesses=67 minorants=3 evals=3959 min_margin=1.8830e-09 min_excl_margin=7.0390e-04 m
PASS cover: leaves=311 kinds={0: 69, 2: 232, 1: 10} residual_stack=1 volume=1
PASS T=0.0156 eta=0.7 rho0=0.69999980926513672 leaves=613 (cert=425 excl=120 out=68) witnesses=376 minorants=47 evals=40119 min_margin=7.7213e-11 min_excl_margin=6.4772e-
PASS cover: leaves=613 kinds={0: 425, 2: 68, 1: 120} residual_stack=1 volume=1
note: FLINT_PY not set: Arb replays and positivity skipped (see RUN_IT_YOURSELF.md)
PASS
```

With FLINT_PY, 128 bits. This run covers all seven pieces and positivity for eta 0.2, 0.3, 0.4, then was stopped by a time limit on the background job, so it has no final line:
```
PASS T=0.0155 eta=0 rho0=0 leaves=14107 (cert=13501 excl=289 out=317) witnesses=10379 minorants=1 evals=1236298 min_margin=1.1720e-11 min_excl_margin=1.0923e-08 max|c|<=0
PASS cover: leaves=14107 kinds={0: 13501, 2: 317, 1: 289} residual_stack=1 volume=1
ARB-PASS T=0.0155 eta=0 leaves=14107 cert=13501 excl=289 out=317 evals=1638431 min_margin_lower=1.1720e-11 wall=29.3s
PASS T=0.0155 eta=0.2 rho0=0.19999980926513672 leaves=454 (cert=201 excl=21 out=232) witnesses=160 minorants=3 evals=14074 min_margin=5.0725e-10 min_excl_margin=2.7545e-0
PASS cover: leaves=454 kinds={0: 201, 2: 232, 1: 21} residual_stack=1 volume=1
ARB-PASS T=0.0155 eta=0.2 leaves=454 cert=201 excl=21 out=232 evals=17031 min_margin_lower=5.0725e-10 wall=0.9s
PASS T=0.0155 eta=0.3 rho0=0.29999923706054688 leaves=356 (cert=107 excl=17 out=232) witnesses=97 minorants=3 evals=6697 min_margin=7.6735e-09 min_excl_margin=2.2171e-05 
PASS cover: leaves=356 kinds={0: 107, 2: 232, 1: 17} residual_stack=1 volume=1
ARB-PASS T=0.0155 eta=0.3 leaves=356 cert=107 excl=17 out=232 evals=7970 min_margin_lower=7.6735e-09 wall=0.2s
PASS T=0.0155 eta=0.4 rho0=0.39999961853027344 leaves=344 (cert=94 excl=18 out=232) witnesses=84 minorants=3 evals=5714 min_margin=2.9010e-08 min_excl_margin=6.8099e-07 m
PASS cover: leaves=344 kinds={0: 94, 2: 232, 1: 18} residual_stack=1 volume=1
ARB-PASS T=0.0155 eta=0.4 leaves=344 cert=94 excl=18 out=232 evals=6757 min_margin_lower=2.9010e-08 wall=0.2s
PASS T=0.0155 eta=0.5 rho0=0.5 leaves=310 (cert=65 excl=14 out=231) witnesses=63 minorants=3 evals=3445 min_margin=5.0899e-07 min_excl_margin=4.6988e-05 max|c|<=0.05772 c
PASS cover: leaves=310 kinds={0: 65, 2: 231, 1: 14} residual_stack=1 volume=1
ARB-PASS T=0.0155 eta=0.5 leaves=310 cert=65 excl=14 out=231 evals=3969 min_margin_lower=5.0899e-07 wall=0.2s
PASS T=0.0155 eta=0.6 rho0=0.59999942779541016 leaves=311 (cert=69 excl=10 out=232) witnesses=67 minorants=3 evals=3959 min_margin=1.8830e-09 min_excl_margin=7.0390e-04 m
PASS cover: leaves=311 kinds={0: 69, 2: 232, 1: 10} residual_stack=1 volume=1
ARB-PASS T=0.0155 eta=0.6 leaves=311 cert=69 excl=10 out=232 evals=4681 min_margin_lower=1.8830e-09 wall=0.1s
PASS T=0.0156 eta=0.7 rho0=0.69999980926513672 leaves=613 (cert=425 excl=120 out=68) witnesses=376 minorants=47 evals=40119 min_margin=7.7213e-11 min_excl_margin=6.4772e-
PASS cover: leaves=613 kinds={0: 425, 2: 68, 1: 120} residual_stack=1 volume=1
ARB-PASS T=0.0156 eta=0.7 leaves=613 cert=425 excl=120 out=68 evals=44236 min_margin_lower=7.7213e-11 wall=2.5s
PTS-PASS file=pts_eta0.2_r0.58732.json eta=0.2 r1=0.58732 nodes=18 subintervals=31 min_lower=2.9632900e-5 wall=53s
PTS-PASS file=pts_eta0.3_r0.58610.json eta=0.3 r1=0.58610 nodes=16 subintervals=29 min_lower=3.2313315e-5 wall=63s
PTS-PASS file=pts_eta0.4_r0.58498.json eta=0.4 r1=0.58498 nodes=17 subintervals=31 min_lower=2.1892112e-5 wall=56s
```

Eta 0.3 to 0.7 and the final line from a complete earlier run of the same script on the same certificates, 2026-11-01 02:44Z (before object/PROOF.md was pinned in run_checks.sh):
```
PTS-PASS file=pts_eta0.3_r0.58610.json eta=0.3 r1=0.58610 nodes=16 subintervals=29 min_lower=3.2313315e-5 wall=16s
PTS-PASS file=pts_eta0.4_r0.58498.json eta=0.4 r1=0.58498 nodes=17 subintervals=31 min_lower=2.1892112e-5 wall=15s
PTS-PASS file=pts_eta0.5_r0.58393.json eta=0.5 r1=0.58393 nodes=16 subintervals=29 min_lower=4.1821329e-5 wall=15s
PTS-PASS file=pts_eta0.6_r0.58297.json eta=0.6 r1=0.58297 nodes=15 subintervals=30 min_lower=6.8477015e-5 wall=16s
PTS-PASS file=pts_eta0.7_r0.58208.json eta=0.7 r1=0.58208 nodes=15 subintervals=27 min_lower=1.0885344e-5 wall=18s
PASS
```

check_arb.py with ctx.prec=256, on these shipped covers, 2026-11-01 about 02:50Z:
```
ARB-PASS T=0.0155 eta=0.2 leaves=454 cert=201 excl=21 out=232 evals=17031 min_margin_lower=5.0725e-10 wall=0.7s
ARB-PASS T=0.0155 eta=0.3 leaves=356 cert=107 excl=17 out=232 evals=7970 min_margin_lower=7.6735e-09 wall=0.2s
ARB-PASS T=0.0155 eta=0.4 leaves=344 cert=94 excl=18 out=232 evals=6757 min_margin_lower=2.9010e-08 wall=0.3s
ARB-PASS T=0.0155 eta=0.5 leaves=310 cert=65 excl=14 out=231 evals=3969 min_margin_lower=5.0899e-07 wall=0.2s
ARB-PASS T=0.0155 eta=0.6 leaves=311 cert=69 excl=10 out=232 evals=4681 min_margin_lower=1.8830e-09 wall=0.1s
ARB-PASS T=0.0155 eta=0 leaves=14107 cert=13501 excl=289 out=317 evals=1638431 min_margin_lower=1.1720e-11 wall=66.3s
ARB-PASS T=0.0156 eta=0.7 leaves=613 cert=425 excl=120 out=68 evals=44236 min_margin_lower=7.7213e-11 wall=7.1s
```

check_pts.py with ctx.prec=256, about 02:55Z:
```
PTS-PASS file=pts_eta0.7_r0.58208.json eta=0.7 r1=0.58208 nodes=15 subintervals=27 min_lower=1.0885340e-5 wall=52s
PTS-PASS file=pts_eta0.6_r0.58297.json eta=0.6 r1=0.58297 nodes=15 subintervals=30 min_lower=6.8477015e-5 wall=58s
PTS-PASS file=pts_eta0.5_r0.58393.json eta=0.5 r1=0.58393 nodes=16 subintervals=29 min_lower=4.1821329e-5 wall=87s
```

Altered copies, last lines of run_checks.sh: all witnesses of piece 2 shifted by 2e-3: FAIL. Last leaf of piece 7 dropped: FAIL. Top piece asked for T=0.0165: FAIL. One bit of a certificate part flipped: FAIL. One digit of object/PROOF.md changed: FAIL. One single witness shifted by 2e-3: PASS (that box has slack at this size).

Positivity at 256 bits for the three etas missing above (check_pts.py with ctx.prec = 256), run 2026-11-01:
```
PTS-PASS file=pts_eta0.2_r0.58732.json eta=0.2 r1=0.58732 nodes=18 subintervals=31 min_lower=2.9632900e-5 wall=19s
PTS-PASS file=pts_eta0.3_r0.58610.json eta=0.3 r1=0.58610 nodes=16 subintervals=29 min_lower=3.2313315e-5 wall=18s
PTS-PASS file=pts_eta0.4_r0.58498.json eta=0.4 r1=0.58498 nodes=17 subintervals=31 min_lower=2.1892112e-5 wall=23s
```
