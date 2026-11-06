# Run it yourself (fresh shell, from this folder)
1. Check: `sh verify-it-yourself/run_checks.sh` -> `size=42 distinct=True alphabet_length_gc_ok=True min_hamming=11 table=34` then `PASS`.
2. Rebuild (deterministic; Linux, gcc, Python 3 stdlib):
   cd how-we-built-it
   python3 gf4slice.py 15 2 3000 s40.txt        # 40 words, same set as intermediate_slice40.txt
   gcc -O2 -o gcmc gcmc.c
   ./gcmc 15 11 41 401 60 ck41.txt intermediate_slice40.txt | grep '^WORD' | sed 's/WORD //' > c41.txt   # = intermediate_code41_s401.txt
   ./gcmc 15 11 42 5042 600 ck42.txt c41.txt | grep '^WORD' | sed 's/WORD //' > c42.txt                 # = ../object/A4GC_15_11_7_M42.txt
   sha256sum c42.txt   # 7164f7dd9a56e376779fb30fc4d61a3dc7b6c9508cce1b4c1247f89d484b5089
3. Null: gcc -O2 -o nullgreedy nullgreedy.c; ./nullgreedy 15 11 1 400 -> maximum size 26 over 400 random greedy codes.
