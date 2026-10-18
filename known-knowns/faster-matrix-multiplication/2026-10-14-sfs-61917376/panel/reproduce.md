context: fresh isolated subagent; inputs restricted to this claim package, pinned AGENTS.md, kit/RULES.md, RUN.md steps 6–7, and independently fetched public primary sources; no other panel, run, attempt, charter, prior verdict, or parent reasoning read.

PROVED-HERE: the immutable `claim/scheme.json` computes the full ordered integer matrix product of format (4, 5, 8) using 118 active distinct bilinear products and 486 charged binary additions/subtractions, with literal coefficients ±1 and ternary final expanded factors.

Candidate SHA256: `61917376617f1db0a75f5e9f5efd8bbd748713896418760b469126ea042ae5ee`.

I independently wrote `panel/reproduce-code/check_slp.py` before opening `claim/verify.py`. The pre-read marker `panel/reproduce-code/before-author-code.json` records UTC `2026-10-14T16:10:27.417425+00:00` and checker SHA256 `771f59b5765e1a4abef4a14964881dad64775aa11064619f3045a0fca6f7e27b`. At that point the candidate, primary positive control, audit controls, and clean isolated packaging check had already passed. Verification routines use Python standard-library integer arithmetic and do not import or execute primary source code or the author's verifier.

The ordinary definition used was:

> C[i,j] = sum over k of A[i,k] * B[k,j]; A[i,k] is base index i*5+k, B[k,j] is base index k*8+j, and C[i,j] is output index j*4+i.

KNOWN: independently retrieved [Perminov's Scheme implementation](https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/src/schemes/scheme.py) confirms these fixed coordinates in `Scheme.naive`, source lines 35–49. `from_reduced`, lines 334–362, confirms fresh base sizes and the transpose from output expressions to the third factor. Fresh variables are appended at `base + position` in lines 1042–1050. `complexity`, lines 544–548, supplies the expanded support-count convention used to audit the naive metadata. I did not search for or fit any coordinate permutation.

The independently authored check contracts each expanded rank-one term over Z and compares every coefficient with the tensor required by the definition. Separately, a literal signed-gate interpreter evaluates the entire circuit on every left/right input basis pair and compares against a direct ordinary triple-loop matrix product. These establish the polynomial identity over Z, hence ordinary exact matrix multiplication over every commutative ring by the same integer identity.

Actual independent CLI result, saved in `panel/reproduce-code/candidate-results.json`:

```json
{"pass": true, "format": [4, 5, 8], "rank": 118,
 "complexity": {"naive": 1521, "reduced": 486},
 "coefficients_checked": 25600, "nonzero_tensor_coefficients": 160,
 "active_distinct_products": 118, "basis_pairs_executed": 800,
 "output_comparisons": 25600}
```

PROVED-HERE: all declared products have nonzero expanded left, right, and third factors; their left/right outer products are distinct even after quotienting by free signs. All fresh references are backward and in range, every declared fresh gate lies on a terminal dependency path, and the checker finds no unreferenced fresh gate. All scalar fields are literal integer +1 or −1: the inspected object contains 974 positive and 266 negative literal terms. The strict schema rejects additional operation/scalar fields, fractional/string/boolean scalars, zero literals, and duplicate JSON keys.

PROVED-HERE: the count is obtained from the literal schedule, including every fresh and terminal sum, before comparing with metadata:

| Side | Fresh binary gates | Terminal binary gates | Live fresh gates | Maximum absolute intermediate coefficient |
|---|---:|---:|---:|---:|
| U | 101 | 0 | 101 | 1 |
| V | 159 | 0 | 159 | 1 |
| W | 226 | 0 | 226 | 2 |

The total is 101 + 159 + 226 = 486. Aliases and unary sign changes cost zero. Products are counted separately as the 118 declared products. No multiplication by a nonunit scalar is encoded in any row. A W intermediate coefficient of 2 is computed through paid binary gates; it does not invalidate ternarity because every final expanded U, V, and W coefficient is in {−1, 0, 1}. Expanded support counts are U 526, V 662, W 601, giving naive metadata 526 + 662 + 601 − 2·118 − 32 = 1521. The checker requires both metadata values to match these measured values.

KNOWN / positive calibration: the independently fetched [primary reduced reference circuit](https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/results/addition_reduced_ZT/4x5x8_m118_cr513_fv249_cn1521_ZT_reduced.json) also passes the same coordinate definition, all 25,600 Z coefficients, and all 800 basis pairs. Its charged count is 513, with fresh/terminal subtotals U 44/67, V 74/92, W 131/105, and naive count 1521. This is calibration against one actual public object, not an assertion about the minimum public count or global novelty.

PROVED-HERE / controls: `panel/reproduce-code/run_controls.py` records 26 controls with all expected results satisfied: 2 positive and 24 negative. An ordinary independently constructed naive (4,5,8) program passes; a paid `x+x` followed by subtracting `x` passes with ternary final factor. A paid `x+x` left as a final factor fails ternarity, while a free literal scalar 2 fails the literal audit. Other rejected controls cover dead gates even when cost metadata charges them, forward/negative references, cost lies, incorrect coordinates, missing products, inactive/duplicate products, hidden scalar or operation fields, nonbinary fresh gates, and malformed literals/schema. The complete control objects and precise rejection stages are saved under `panel/reproduce-code/controls/` and `controls-results.json`.

The mod-2-invisible control changes a candidate terminal U sign while retaining legal ternary factors and cost. Independent residual accounting records 168 incorrect integer coefficients, zero mismatches modulo 2, and maximum absolute integer error 2. The Z checker rejects it at the tensor stage. This directly tests that the checker is not merely a finite-field or randomized spot check.

PROVED-HERE / packaging: the checker was copied with only `scheme.json` into an otherwise clean temporary directory and run with Python isolated mode. `python3 -I check_slp.py scheme.json --expected-candidate` exits zero with `"pass": true`. No saved primary files or network are read by this CLI. From the run directory the corresponding command is:

```sh
python3 panel/reproduce-code/check_slp.py claim/scheme.json --expected-candidate
```

After the independent work, the supplied verifier was opened and run as corroboration. Its actual result is saved in `panel/reproduce-code/supplied-verifier-results.json`:

```json
{"valid": true, "format": [4, 5, 8], "rank": 118,
 "addition_counts": {"u": 101, "v": 159, "w": 226},
 "additions": 486, "identities_verified": 25600}
```

Honest access receipts:

| Public primary URL | Successful GET start UTC | HTTP status | Response SHA256 |
|---|---|---:|---|
| `https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/src/schemes/scheme.py` | `2026-10-14T16:05:54.301387+00:00` | 200 | `3684c5f6d762fff39db1ebee60ab6465469d627443c875d7fa1a9f6be35337fe` |
| `https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/results/addition_reduced_ZT/4x5x8_m118_cr513_fv249_cn1521_ZT_reduced.json` | `2026-10-14T16:05:54.796009+00:00` | 200 | `7a273fbb34339b6123e5e9253fb088af12c8f11362e46cfe0789b2c3bd9e3860` |

Each URL received one ordinary successful HTTP GET using `V3R1T4S-REPRODUCE/1.0`. The first local attempts failed at DNS before any HTTP response, at UTC `2026-10-14T16:05:39.079839+00:00` and `2026-10-14T16:05:39.079850+00:00`; those receipts are preserved separately with null HTTP status and hash. Ordinary network escalation then supplied the successful GETs above. No real HTTP block was retried, no blocked PDF listed in `claim/LITERATURE_ACCESS.md` was requested, and no browser impersonation, mirror, cookie, proxy, or challenge bypass was used. Sources were treated only as data.

Limits: this verdict covers the specified immutable object's mathematical identity, coefficient class, active product count, and charged SLP cost. It does not claim exact replay of the uncaptured discovery history, optimality of the circuit, a current global literature minimum, global novelty, or satisfaction of comparison clauses owned by the other skeptics. No publication or candidate/criterion change was made. The full-search replay limit stated in the claim remains in force.

pass: true
