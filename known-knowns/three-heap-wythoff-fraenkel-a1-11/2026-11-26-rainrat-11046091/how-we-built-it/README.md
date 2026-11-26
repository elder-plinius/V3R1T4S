# How we built it

- `PREREG.md`: pre-registered verification specification frozen before generating the claim artifacts.
- `PROOF.md`: complete mathematical proof for $0 \le m \le 12$, uniting the Lemma 2.6 gap-indexed continuation, modulo-$p(m)$ ray witnesses, and Beatty-floor lower-layer separation (independent of the p. 235 midpoint printing typo).
- `reverse.cpp`: C++20 dense predecessor-marking solver for $0 \le m \le Y \le Z \le 12000$ (`g++ -std=c++20 -O3 -Wall -Wextra reverse.cpp -o reverse && ./reverse 12000 > positions.txt`).
- `direct.cpp`: C++20 sparse row-by-row gap-indexed solver (`g++ -std=c++20 -O3 -Wall -Wextra direct.cpp -o direct && ./direct 12000 | awk '$3<=12000' | LC_ALL=C sort -n -k1,1 -k2,2 > positions.txt`).
- `build_certificate.py`: Python 3.8+ script that extracts `object/wythoff_a1_12_certificate.json` from the dual-verified 59,483-row `positions.txt` (`python3 build_certificate.py positions.txt 12000 wythoff_a1_12_certificate.json`).
