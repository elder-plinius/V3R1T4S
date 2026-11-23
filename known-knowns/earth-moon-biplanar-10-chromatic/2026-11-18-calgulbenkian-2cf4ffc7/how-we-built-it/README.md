# How We Built It

1. Compile the C99 Wagner diagonal-flip sphere-triangulation search engine:
   ```sh
   cc -O3 -Wall -Wextra wagner_n18_20.c -lm -o wagner_n18_20
   ```
2. Run with seed `42` on `n = 19` vertices:
   ```sh
   ./wagner_n18_20 19 42 5.0 candidates.jsonl 1
   ```
3. Peel the first spanning vertex-9-critical union candidate (`SPAN_CRIT9`) to an exact 9-edge-critical biplanar graph (`n = 19, e = 92`) and emit its planar embeddings, 8-coloring UNSAT DRAT proof (`PySAT>=1.8.dev13`, `networkx>=3.2`), and all 92 edge-deletion 8-colorings:
   ```sh
   python3 peel_to_9critical.py candidates.jsonl
   ```
