# Run it yourself (fresh shell, from this folder)
1. Check: `sh verify-it-yourself/run_checks.sh` -> `size=44 distinct=True alphabet_length_gc_ok=True min_hamming=14 table=38` then `PASS`.
2. Rebuild (deterministic, Python 3 stdlib): `cd how-we-built-it && python3 gf4slice.py 19 1 3000 out.txt && sha256sum out.txt` -> 8b28d53b3639dc0cc9d1a1afd37dfca139f5c3852c66003db5ee118b476c1a1a (the [21,3,16] simplex code of PG(2,4) punctured to 19 points, constant-GC slice).
3. Null: `gcc -O2 -o nullsample nullsample.c; ./nullsample 19 14 1 400 20000000` -> maximum size 25 over 400 random greedy codes.
