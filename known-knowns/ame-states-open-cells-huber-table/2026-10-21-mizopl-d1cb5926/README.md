# Single-Cell Huber–Wyderka Table Certificate: `AME(17, 8)` (`[[17, 0, 9]]_8`)

- **Target ID:** `ame-states-open-cells-huber-table` (`known-knowns`)
- **Run / Package ID:** `2026-10-21-mizopl-d1cb5926`
- **Claimed cell:** `AME(17, 8)` (`[[17, 0, 9]]_8`, $n = 17$ parties, local dimension $D = 8 = 2^3 \in \{2..10\}$)
- **Checked scope:** `24,310 / 24,310` eight-party cuts over $\mathbb{F}_8$ (`0` rank-deficient cuts) and `24,310 / 24,310` eight-qudit (`24`-qubit) cuts of the $51$-qubit binary trace-symplectic graph state over $\mathbb{F}_2$ (`0` rank-deficient cuts)
- **Certificate file:** `object/ame_17_8_pure_circulant_certificate.json` (`4,176` bytes, `sha256: 0bc632480b2bfb3a90117f0676e8894dc5972ea32cb315cd47e1d04077f20a28`)

## What

Single-cell certificate for the open Huber-Wyderka table entry AME(17, 8) (quantum MDS code [[17, 0, 9]]_8, n = 17 parties of local dimension D = 8 = 2^3, sitting in the table's D in {2..10} column range where cell (n = 17, D = 8) is Blank at https://tp.nt.uni-siegen.de/ame/table.html), constructed as a symmetric 17x17 circulant graph state over GF(8) = GF(2)[w]/(w^3 + w + 1) with palindromic chord vector a = (1, 2, 5, 1, 5, 2, 2, 2) = (1, w, w^2+1, 1, w^2+1, w, w, w) and verified exhaustively across all C(17, 8) = 24,310 eight-party cuts over GF(8) (24,310 / 24,310 full rank 8, 0 rank-deficient cuts) and across all 24,310 eight-qudit (24-qubit) cuts of the 51-qubit binary trace-symplectic graph state [I_51 | B_51] over GF(2) (24,310 / 24,310 full rank 24).

## Numbers

| Metric / Invariant | Value |
| :--- | :--- |
| **Claimed Huber–Wyderka cell** | `AME(17, 8)` ($n = 17$, $D = 8 \in \{2..10\}$; pure quantum MDS code `[[17, 0, 9]]_8`) |
| **Live Huber–Wyderka table status (`https://tp.nt.uni-siegen.de/ame/table.html`)** | **Blank** (`<td></td>` at row $n = 17$, column $D = 8$; `Yes` entries in $D = 8$ stop at $n = 14$; fetched `2026-10-20T01:10:09Z` & `2026-11-07T15:09:42Z`, `230,252` bytes, `sha256: e71dda90edc6f6664bc512aaa039beea2b986c5998ca16674a8aa7c896c77082`) |
| **Status in bank papers (`arXiv:2608.05781`, `arXiv:2609.11796`, `arXiv:2608.01011`, Ball 2020)** | **Open / not constructed** (Ball 2020 and `arXiv:2609.11796` require **odd** characteristic $\operatorname{char}(\mathbb{F}_q) \ne 2$, whereas $D = 8 = 2^3$ has even characteristic $2$) |
| **Status on `codetables.de` (`https://www.codetables.de/QECC/QECC.php?q=64&n=17&k=0`)** | Prior to `2026-10-21`: lower bound $8$ (`[[17, 0, 8..9]]_8`). Updated `2026-10-21` to lower bound $9$ (`[[17, 0, 9]]_8`) under **`Construction type: Gajewski`** (crediting the submitter of this PR, `@mizopl`) with the identical $\mathbb{F}_8 \subset \mathbb{F}_{64}$ 17-circulant polynomial (`9,098` bytes, `sha256: c1565d91540ffdd9c4819f30773ced9161d9158e71e6d6aa7c4d1ce3586ee981`) |
| **Finite field & primitive polynomial** | $\mathbb{F}_8 = \mathbb{F}_2[w]/(w^3 + w + 1)$ (`0xB = 11`, integer encoding $c_0 + 2 c_1 + 4 c_2$) |
| **Palindromic chord vector $a = (a_1, \dots, a_8)$** | `[1, 2, 5, 1, 5, 2, 2, 2]` $= (1, w, w^2+1, 1, w^2+1, w, w, w)$ |
| **First row of $17 \times 17$ circulant $\Gamma$** | `[0, 1, 2, 5, 1, 5, 2, 2, 2, 2, 2, 2, 5, 1, 5, 2, 1]` |
| **Exhaustive $\mathbb{F}_8$ 8-party cut check** | `24,310 / 24,310` cuts have full $\mathbb{F}_8$-rank `8` (`0` rank-deficient cuts; `0.40s`) |
| **Exhaustive $\mathbb{F}_2$ $51$-qubit trace-symplectic cut check** | `24,310 / 24,310` eight-qudit (`24`-qubit) cuts have full $\mathbb{F}_2$-rank `24` (`0` bad cuts; `0.66s`) |
| **Null control (`400` random $\mathbb{F}_8$ symmetric 17-circulants, `seed=42`)** | `0 / 400` achieve `AME(17, 8)`; best random control reaches `24,140 / 24,310` full-rank cuts (`170` bad cuts) |
| **Single-entry mutant controls** | Zeroing edge $(0,1)$ causes `184 / 24,310` bad cuts; zeroing chord $d=1$ causes `918 / 24,310` bad cuts |

## Compared To

1. **Huber–Wyderka Online Table (`https://tp.nt.uni-siegen.de/ame/table.html`):**
   Fetched `2026-10-20T01:10:09Z` and re-fetched `2026-11-07T15:09:42Z` (`HTTP 200`, `230,252` bytes, `sha256: e71dda90edc6f6664bc512aaa039beea2b986c5998ca16674a8aa7c896c77082`). In column $D = 8$, `Yes` entries stop at $n = 14$ (`#8_10..#8_14`), while row $n = 17$ (`AME(17, 8)`) is **Blank** (`<td></td>`).
2. **Papers Named by the Bank (`arXiv:2608.05781`, `arXiv:2609.11796`, `arXiv:2608.01011`, Ball 2020):**
   Bidav (`arXiv:2608.05781`) constructs `AME(12, 5)` and $D \in \{11, 13\}$ states; `arXiv:2609.11796` and Ball (`arXiv:1907.04391`, *J. Phys. A* 2020) construct $\operatorname{AME}(2q-1, q)$ and $\operatorname{AME}(2q, q)$ only for **odd** prime powers $q$ ($\operatorname{char}(\mathbb{F}_q) \ne 2$), which does not apply to $D = 8 = 2^3$ ($\operatorname{char}(\mathbb{F}_8) = 2$); `arXiv:2608.01011` covers $n = 7$ only.
3. **Grassl's `codetables.de` (`https://www.codetables.de/QECC/QECC.php?q=64&n=17&k=0`):**
   Prior to `2026-10-21` (when we found `AME(17, 8)` on `2026-10-20`), `codetables.de` listed only `lower bound: 8` (`[[17, 0, 8..9]]_8`, strictly below the quantum Singleton bound $d = 9$). After `@mizopl` communicated this $\mathbb{F}_8$ 17-circulant to Dr. Markus Grassl on `2026-10-21`, `https://www.codetables.de/QECC/QECC.php?q=64&n=17&k=0` (`last modified: 2026-10-21`, re-fetched `2026-11-07T15:09:42Z`, `HTTP 200`, `9,098` bytes, `sha256: c1565d91540ffdd9c4819f30773ced9161d9158e71e6d6aa7c4d1ce3586ee981`) was updated to `[[17, 0, 9]]_8` under **`Construction type: Gajewski`** (crediting the submitter of this PR) with the identical $\mathbb{F}_8 \subset \mathbb{F}_{64}$ 17-circulant generator polynomial (verified in Step 4 of `verify-it-yourself/verify.py`).

## Not Claimed

1. **Out-of-range dimensions $D \ge 11$ removed:** The Huber–Wyderka table covers $D \in \{2..10\}$ only (`485` filled cells). All $D \ge 11$ certificates from the earlier draft (`AME(20, 11)`, `AME(19, 11)`, `AME(16, 13)`, `AME(20, 121)`, `AME(19, 289)`, etc.) have been removed from this package.
2. **One cell per package (`kit/SUBMIT.md` §1):** All other $D \in \{2..10\}$ cells from the earlier multi-cell draft have been removed from `object/` so that this package claims exclusively `AME(17, 8)` (`[[17, 0, 9]]_8`). In particular, `AME(15, 7)` (`[[15, 0, 8]]_7`), `AME(13, 5)` (`[[13, 0, 7]]_5`), `AME(17, 7)` (`[[17, 0, 9]]_7`), `AME(18, 7)` (`[[18, 0, 10]]_7`), and `AME(15, 9)` (`[[15, 0, 8]]_9`) were already known on `codetables.de` or in `arXiv:2609.11796` and are not claimed here.
3. **Removed invalid and withdrawn items:** `AME(10, 10)` (which held a binary `[[10, 2, 4]]_2` code rather than a $D = 10$ state), the withdrawn `Q19/C20` items, and the $\mathbb{Z}_9$ reading of `AME(15, 9)` have been removed.
4. **Symmetry-restricted `D31` and `D33–D35` searches:** The earlier `D31` (`AME(8, 6)`) and `D33–D35` (`AME(7, 6)`, `AME(11, 10)`, `AME(12, 10)`) files were symmetry-restricted searches (cyclic / circulant / group-ring ansätze), not general non-existence results across the full Hilbert space; they have been removed and are not claimed here.

## How we built it

1. **Dihedral $D_{17}$ Orbit Filtration over $\mathbb{F}_8$ Circulants:**
   A symmetric hollow $17 \times 17$ circulant matrix $\Gamma_{i,j} = a_{\min((j-i)\bmod 17, (i-j)\bmod 17)}$ over $\mathbb{F}_8 = \mathbb{F}_2[w]/(w^3 + w + 1)$ is determined by $8$ chord weights $(a_1, \dots, a_8) \in \mathbb{F}_8^8$. Fixing $a_1 = 1$ under diagonal $\mathbb{F}_8^\times$ rescaling reduces the search space from $8^8 = 16,777,216$ to $8^7 = 2,097,152$ normalized chord vectors, and the dihedral group $D_{17}$ partitions the $\binom{17}{8} = 24,310$ eight-party cuts into $750$ orbits whose exact orbit multiplicities sum to $24,310$.
2. **Exact Certificate & Dual Exhaustive Verification:**
   Filtering candidates across the $750$ $D_{17}$ orbits and then testing all $\binom{17}{8} = 24,310$ cuts directly (without symmetry quotienting) isolated the palindromic chord vector $a = (1, 2, 5, 1, 5, 2, 2, 2) = (1, w, w^2+1, 1, w^2+1, w, w, w)$, stored in `object/ame_17_8_pure_circulant_certificate.json`. See `HOW_WE_FOUND_IT.md` and `how-we-built-it/search_and_verify_ame_17_8_circulant.py`.

## Check It Yourself

From the package root (`known-knowns/ame-states-open-cells-huber-table/2026-10-21-mizopl-d1cb5926`), run:

```sh
sh verify-it-yourself/run_checks.sh
```

Using only the Python 3 standard library (`~2.2s` runtime on Apple M1), `verify-it-yourself/verify.py` verifies the certificate schema and circulant structure, checks all $24,310$ eight-party cuts over $\mathbb{F}_8$ (`bad = 0`), checks all $24,310$ eight-qudit (`24`-qubit) cuts of the $51$-qubit binary trace-symplectic graph state over $\mathbb{F}_2$ (`bad = 0`), verifies the exact $\mathbb{F}_8 \subset \mathbb{F}_{64}$ subfield isomorphism with the `codetables.de` `[[17, 0, 9]]_8` entry (`Construction type: Gajewski`, `2026-10-21`), runs positive/negative/mutant controls, and prints `PASS`.

## Verify it yourself

See `RUN_IT_YOURSELF.md` and `verify-it-yourself/RECEIPTS.md` for step-by-step instructions and recorded output logs.

## Credits

- **Discovery, certificate & verification code:** `@mizopl` (`we*`, Gemini-CLSS `PROOFER v19`).
- **Independent review & audit feedback:** `@DmitrL-dev` (independent verification of `object/ame_17_8_pure_circulant_certificate.json` across all $24,310$ cuts) and `@elder-plinius` (single-cell scoping, table range, and provenance audit).
- **Online tables & references:** Felix Huber and Nikolai Wyderka (*Table of AME States*, `https://tp.nt.uni-siegen.de/ame/table.html`); Markus Grassl (*Code Tables: Bounds on the parameters of various types of codes*, `https://www.codetables.de/QECC/`).
