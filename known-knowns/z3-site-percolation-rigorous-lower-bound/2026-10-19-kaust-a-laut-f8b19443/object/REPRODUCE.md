# Reproduce

Requirements: Go (any recent version; built here with go 1.26) and Python 3 (standard library only).
Reference machine: Intel i5-8500T, 6 cores, 16 GB RAM. The enumerator uses little memory.

1. Build the enumerator:
       cd code/par && go build -o par .        (par.exe on Windows)
2. Quick runs (exact tables; compare with outputs/):
       ./par 16 6 > p16.txt     (about 30 s)      diff p16.txt ../../outputs/p16.txt
       ./par 18 6 > p18.txt     (about 9 min)     diff p18.txt ../../outputs/p18.txt
3. The certificate run (about 140 min on 6 cores):
       ./par 20 6 > p20.txt                       diff p20.txt ../../outputs/p20.txt
   Output: "TOTAL 20 <number of 20-step NAWs>" and "EXT 20 f:c_f ...".
4. Exact check of the bound (from the repository root of claim/):
       python code/verify_cert.py outputs/p20.txt 263376
   Expected: K_N(263376/10^6) = 0.999971526024 -> PASS; K_N(263377/10^6) = 1.000041779030 -> fails; sanity
   1/5 passes; 0.3116 fails; f_max = 23, K_N increasing on [0, 21/44]. Saved as outputs/verify_N20.txt.
5. Threshold search used during the run (same exact arithmetic): python code/kcheck.py outputs/p20.txt
   (saved as outputs/k20.txt).
Arguments of par: N (walk length) and the number of worker goroutines.
