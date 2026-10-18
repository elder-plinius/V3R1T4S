# Run It Yourself (`2026-10-18-mizopl-dd85465d`)

## 1. Quick Verification (~0.4 seconds, Python 3 + NumPy)

From the root of this package directory:

```bash
sh verify-it-yourself/run_checks.sh
```

## 2. Verification with `OrensteinLab/GreedyMini`'s Verbatim C++ `prob_gc_dna` Code

```bash
clang++ -O3 -std=c++17 verify-it-yourself/verify_greedymini_dna.cpp -o verify_greedymini_dna
./verify_greedymini_dna 12 3 the-record-we-beat/published_w12_k3.gm object/w12_k3_improved.gm
```
