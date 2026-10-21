# `cryptocellar-truppenschluessel-1941` — Blind Garble-Tolerance Benchmark (`p1`) for the 1941 German Army Two-Square *Truppenschlüssel* Cipher (`2026-10-21-mizopl-307b2885`)

## What

Named partial win p1 (blind garble-tolerance benchmark) on cryptocellar-truppenschluessel-1941: using the Truppenschluessel Two-Square procedure of Ostwald and Weierud (2021, Cryptologia 45(3):235-249, Section 2 pp. 236-238, validated 100% across all 9 worked examples / 410 characters in Section 9 Appendix pp. 247-248), the blind C solver claim/p1_blind_garble_solver.c (sha256 68340440b31f162135863c90915e1de0d3725f6fc591bd9079a4de9a765d60d0) given 3 period-style 1941 German military ciphertexts of lengths 80, 76, and 76 letters (232 letters total) enciphered with random 5x5 squares and 19/232 (8.19%) injected Morse-Levenshtein-1 garbles (18/232 = 7.76% outside the opening crib) recovers 50/50 (100.0%) of both 5x5 key squares up to exact S5_row x C5_col_K1 x C5_col_K2 gauge equivalence (claim/p1_benchmark_certificate.json, sha256 307b2885211621dbc21f5d46bc3ef1cee905576be48e3371a868905529e43945) and recovers 96.25% (77/80), 97.37% (74/76), and 100.00% (76/76) of the plaintext letters under greedy Morse-Levenshtein-1 error correction (227/232 = 97.84% overall, all three >= 95%) and 98.75% (79/80), 97.37% (74/76), and 100.00% (76/76) under bottleneck-Viterbi Morse-Levenshtein-1 error correction (229/232 = 98.71% overall, all three >= 95%), with 200 shuffled-ciphertext null controls scoring +9.27 SD below the claim mean and +6.42 SD (>= 5.0 SD) below the claim from the best shuffle.

## Check It Yourself

From this package directory, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Expected last line**: `PASS`
- **Rough laptop time**: `< 1` second on CPU (`python3`).

## Compared To

- **Target ID**: `cryptocellar-truppenschluessel-1941` (`category: unbroken-ciphers`, Named Partial Win `p1`)
- **Primary Source & Reference**:
  - `https://www.cryptocellar.org/bgac/g-army-ts-messages.html` (fetched `2026-10-21T09:42:56Z`, `31,268` bytes, `sha256: 58a057ab7c535edb3517e7d2159afd149b435879aa49bf8372ccaed21a1675af`)
  - Christof Ostwald and Frode Weierud (2021), *"Modern cryptanalysis of the Truppenschlüssel"*, *Cryptologia* 45(3):235–249 (Section 2 pp. 236–238, Section 9 Appendix pp. 247–248)
- **Quantitative Benchmark Results (`object/p1_benchmark_certificate.json`)**:

| Metric / Message | Requirement (`p1`) | Raw Decryption (No EC) | Greedy Morse-Lev1 EC | Bottleneck-Viterbi Morse-Lev1 EC | Status |
|---|---:|---:|---:|---:|:---:|
| **Key Squares $(K_1, K_2)$** | Blind recovery | `50 / 50` (`100.00%` gauge) | **`50 / 50` (`100.00%`)** | **`50 / 50` (`100.00%`)** | **PASS** |
| **Message 1 (`80` chars, `7` garbles)** | `>= 95.0%` | `71 / 80` (`88.75%`) | **`77 / 80` (`96.25%`)** | **`79 / 80` (`98.75%`)** | **PASS** |
| **Message 2 (`76` chars, `6` garbles)** | `>= 95.0%` | `66 / 76` (`86.84%`) | **`74 / 76` (`97.37%`)** | **`74 / 76` (`97.37%`)** | **PASS** |
| **Message 3 (`76` chars, `6` garbles)** | `>= 95.0%` | `66 / 76` (`86.84%`) | **`76 / 76` (`100.00%`)** | **`76 / 76` (`100.00%`)** | **PASS** |
| **All 3 Messages (`232` chars, `19` garbles)** | `>= 95.0%` on each | `203 / 232` (`87.50%`) | **`227 / 232` (`97.84%`)** | **`229 / 232` (`98.71%`)** | **PASS** |
| **200-Shuffle Null Control (`T4_COND`)** | `>= 5.0 SD` below claim | `null_max = 54,395` | `claim = 417,578` | **`z_mean = +9.27 SD`, `z_max = +6.42 SD`** | **PASS** |
| **400-Shuffle Null Control (`null_test.md`)** | `real > best_control` | `best_control = 54,395` | `real = 417,578` | **`z_mean = +9.42 SD`, `z_max = +6.57 SD`** | **PASS** |

## Not Claimed

- We claim only Named Partial Win **`p1`** (the blind garble-tolerance benchmark on 3 period-style 1941 German military texts of `60–100` letters with random $5 \times 5$ squares and `8.19%` injected Morse-plausible garbles, accompanied by a structural 4-for-4 Morse-Levenshtein-1 differential audit across the unbroken `04.07.1941` repeats).
- We do not claim a full historical decryption (`CONFIRMED_SOLUTION`, `p2`, or `p3`) of an unbroken message on `https://www.cryptocellar.org/bgac/g-army-ts-messages.html`.

## Credits

- **Primary Corpus & Cryptanalysis Reference**: Frode Weierud's CryptoCellar (`https://www.cryptocellar.org/bgac/g-army-ts-messages.html`) and Christof Ostwald & Frode Weierud (2021, *Cryptologia* 45(3):235–249).
- **Contributor**: `mizopl`.
