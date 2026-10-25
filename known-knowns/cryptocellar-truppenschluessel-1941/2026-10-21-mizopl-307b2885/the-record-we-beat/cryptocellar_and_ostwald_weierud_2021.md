# Primary Source & Literature Audit — `cryptocellar-truppenschluessel-1941` (`p1`)

## 1. Primary CryptoCellar Status Page (`https://www.cryptocellar.org/bgac/g-army-ts-messages.html`)

- **URL:** `https://www.cryptocellar.org/bgac/g-army-ts-messages.html`
- **Fetched UTC:** `2026-10-21T09:42:56Z` (`HTTP/2 200`, `Last-Modified: Mon, 27 Jul 2026 14:50:30 GMT`)
- **Size:** `31,268` bytes (`object/g-army-ts-messages.html`)
- **SHA-256:** `58a057ab7c535edb3517e7d2159afd149b435879aa49bf8372ccaed21a1675af`
- **Status at fetch time:** `41` `h4` message entries (`53` message/part blocks), with `11` literal `Broken` marker strings (`13` broken message blocks) and `30` unbroken `h4` entries (`40` unbroken message blocks), including all `04.07.1941` messages (`Nr. 88, 90, 91, 92, 94, 95, 96, 97`).

## 2. Primary Cryptanalysis Reference (Ostwald & Weierud 2021)

- **Reference:** Christof Ostwald and Frode Weierud (2021), *"Modern cryptanalysis of the Truppenschlüssel"*, *Cryptologia* 45(3):235–249 (DOI: `https://doi.org/10.1080/01611194.2020.1755746` / `https://doi.org/10.1080/01611194.2021.1998810`, Section 2 pp. 236–238 and Section 9 Appendix pp. 247–248 [preprint pp. 14–15]).
- **OpenAlex / GitHub / V3R1T4S Audit (`2026-10-21T09:42:59Z`):**
  - `TROPHY_CASE.md` (`https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md`, `sha256: b946f68eb0a6473dd2224065a52390235a535d3282da24669f6724a1472171a1`): `0` entries for `cryptocellar-truppenschluessel-1941` or `unbroken-ciphers`.
  - Open PRs (`https://api.github.com/repos/elder-plinius/V3R1T4S/pulls?state=open&per_page=100`, `sha256: e6b410e62a7fb3b2c319da0063ffce19abed176ccce3ed3cb7ff7588c6d47f42`): `0` open pull requests touch `cryptocellar-truppenschluessel-1941`.
  - Prior to this package, no public repository or paper provided a self-contained solver passing the `p1` blind garble-tolerance benchmark (`50 / 50 = 100.00%` key cell recovery up to $S_5^{\text{row}} \times C_5^{\text{col}, K_1} \times C_5^{\text{col}, K_2}$ gauge equivalence and `97.84%` greedy / `98.71%` Viterbi plaintext recovery across three `60–100` letter messages with `8.19%` injected Morse-Levenshtein-1 garbles, `z_mean = +9.27 SD`, `z_above_max = +6.42 SD` over 200 shuffled-ciphertext controls and `z_mean = +9.42 SD`, `z_above_max = +6.57 SD` over 400 shuffled-ciphertext controls).
