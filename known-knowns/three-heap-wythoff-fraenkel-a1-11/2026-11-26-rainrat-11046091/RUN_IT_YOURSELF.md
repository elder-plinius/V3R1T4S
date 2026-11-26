# Run it yourself

## 1. Standalone verification (Python 3.8+ standard library only)

From this package folder in a fresh shell (~31 seconds, ~27 MB RAM):

```sh
sh verify-it-yourself/run_checks.sh
```

Expected final output line:

```text
PASS
```

This executes `python3 verify-it-yourself/verify_wythoff.py object/wythoff_a1_12_certificate.json`, which:
1. Cross-checks literal 3D game-tree DP ($0 \le p_1 \le 12, p_3 \le 55$) against direct rules-based P-position recomputation through $Y \le 5500$.
2. Recomputes $T^m, S^m, \alpha^m, N_1^m, N_2^m, N_3^m, B^m_{N_3^m}, B^m_{N_3^m+1}$ for all $0 \le m \le 12$ and checks exact agreement with Sun & Zeilberger's Table 1 ($m = 0..10$).
3. Verifies every hypothesis of Claims 3.3 (modulo-$p(m)$ ray witnesses across $[Y_{n_1}, Y_{n_1}+p(m)]$), 3.4, and 3.5 (half-sum $\alpha'$), as well as every finite hypothesis of the direct Lemma 2.6 continuation proof (`how-we-built-it/PROOF.md`).
4. Verifies every field of `object/wythoff_a1_12_certificate.json` against the recomputed values.

## 2. Rebuilding `object/wythoff_a1_12_certificate.json` from scratch

Requires `g++` with C++20 support and Python 3.8+ (~1.8 GiB RAM for `reverse.cpp`):

```sh
mkdir -p build
g++ -std=c++20 -O3 -Wall -Wextra how-we-built-it/reverse.cpp -o build/wythoff_reverse
g++ -std=c++20 -O3 -Wall -Wextra how-we-built-it/direct.cpp -o build/wythoff_direct
./build/wythoff_reverse 12000 > build/positions_reverse.txt
./build/wythoff_direct 12000 | awk '$3<=12000' | LC_ALL=C sort -n -k1,1 -k2,2 > build/positions_direct.txt
cmp build/positions_reverse.txt build/positions_direct.txt
python3 how-we-built-it/build_certificate.py build/positions_reverse.txt 12000 build/rebuilt_certificate.json
cmp object/wythoff_a1_12_certificate.json build/rebuilt_certificate.json
rm -rf build
```
