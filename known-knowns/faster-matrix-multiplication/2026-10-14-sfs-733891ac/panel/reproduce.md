context: fresh isolated subagent, started as the REPRODUCE skeptic and shown only this run's claim package, pinned AGENTS.md, kit/RULES.md, RUN.md steps 6–7, and independently requested public primary sources.

PROVED-HERE: `claim/scheme.json` computes the full ordinary integer product of a 4×4 matrix and a 4×6 matrix using 73 active, distinct bilinear products and exactly 264 binary additions/subtractions, with ternary expanded final factors and only literal unit signs.

Object SHA256: `733891ac541bd4c85da049a68dfcafd680d7fa5f006718668d1e8d38f7478900`. The object was unchanged before and after verification. This is the immutable ordered format (4,4,6); no axis permutation was searched or fitted.

The definition used before reading `claim/verify.py` was:

> For every i,j, C[i,j] = sum over k of A[i,k] B[k,j]. A[i,k] has input index i*4+k; B[k,j] has input index k*6+j; C[i,j] has output index j*4+i. Every sparse row is a signed linear form over already available quantities. A row containing t terms requires t−1 binary +/- operations; aliases and negations are free. Only the 73 declared products multiply nonconstant quantities.

I wrote `panel/reproduce-code/check_integer_slp.py` before inspecting the supplied verifier. Its SHA256 is `8c3c3dafc211510456d14702dc472a3f3372bde4cf54ff88d245d040539400f3`. Its complete results and controls are saved in `panel/reproduce-code/results.json`; the read order and repeated execution are recorded in `panel/reproduce-code/execution_receipt.json`.

PROVED-HERE: I expanded every fresh register over Z, constructed every coefficient of the bilinear tensor, and compared all 9,216 coefficients with the ordinary-coordinate definition. Separately, I executed the literal SLP on all 384 input basis pairs and compared all 9,216 output values with direct matrix multiplication. Both checks pass. The code uses exact Python integers, with no modular arithmetic in the candidate proof. Exhaustiveness plus the explicitly checked linear/bilinear structure proves equality for arbitrary integer inputs.

The following independent audits also pass:

| Property | Observed result |
| --- | --- |
| Product counts | 73 declared, 73 nonzero and output-active, 73 distinct bilinear forms up to free sign |
| Literal scalars | Every arithmetic term has exact integer value +1 or −1; no nonunit scalar or unexpected arithmetic field |
| References | Every fresh register references earlier registers in its own stage; final references are in range |
| Dead gates | None in U, V, or W |
| Final factor expansions | Every U, V, and W coefficient belongs to {−1,0,+1} |
| U paid operations | 67 binary fresh sums; 0 paid final operations |
| V paid operations | 76 binary fresh sums; 0 paid final operations |
| W paid operations | 121 binary fresh sums; 0 paid final operations |
| Total and metadata | 264 paid operations; expanded naive cost 540; both metadata fields match |
| Intermediate expansion maxima | U: 1; V: 1; W: 2 in absolute value |
| Determinism | Two separate candidate checker executions have identical output, SHA256 `84b451bea58c601ed7f167f2397cc3304b98ae9684aef77069af6707b8f8118e` |

PROVED-HERE: W's intermediate coefficient 2 is built entirely by counted binary additions/subtractions with literal ±1 coefficients. It is not an uncharged scalar multiplication. All expanded final factors are ternary. A separate positive control, x → x+x → (x+x)−x, verifies that the checker admits paid intermediate 2 while requiring the final factor to be ternary.

KNOWN, independently obtained primary-source calibration: the live [Perminov Scheme implementation](https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/src/schemes/scheme.py) explicitly assigns the same ordinary indices in `Scheme.naive`; the live [README schema](https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md) specifies the fresh-register blocks and final-form dimensions. I executed unchanged primary-source bodies for `Scheme.naive`, its initializer, and its reduced-format parser, excluding unrelated imports and validation methods. `primaryScheme.naive(4,4,6)` passes the complete coefficient/basis checks at 96 products and 72 additions; the nonsquare calibration `primaryScheme.naive(2,3,4)` passes at 24 products and 16 additions. The source parser's independent recursive expansion agrees coefficient-for-coefficient with my candidate and source-control expansions, including transposed W layout. No indices were fitted to the candidate.

PROVED-HERE: the independently fetched public [4×4×6, 73-product reduced source circuit](https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/results/addition_reduced_ZT/4x4x6_m73_cr280_cn540_ZT_reduced.json) passes the same full checker at 280 paid operations and naive cost 540. Its independently counted stage costs are U 73, V 81, W 126. This is a positive control for the schema and cost accounting, not a minimum-of-literature determination.

PROVED-HERE: all 12 targeted corruption controls are rejected: an output sign flip invisible modulo 2, an otherwise exact circuit with an uncharged scalar 2, a dead paid gate with correctly updated metadata, a self/forward reference, understated reduced cost, false naive cost, an inactive product, duplicate products, wrong output coordinates, a hidden arithmetic field, a boolean index, and a nonternary final expansion. The modulo-2 corruption still passes all 9,216 modular coefficient checks, but both my integer tensor checker and separate literal basis executor reject it. All controls are explicit in `panel/reproduce-code/run_checks.py`.

Only after these independent checks did I inspect and run `claim/verify.py`. It independently reports `valid: true`, format [4,4,6], rank 73, stage additions U 67/V 76/W 121, total 264, and 9,216 verified identities. Its saved output is `panel/reproduce-code/supplied_verifier.stdout.json`. My verdict does not rely on its result.

The public access receipts are saved beside each source. Each successful source had one ordinary public GET with User-Agent naming V3R1T4S; no credentials, proxy, browser imitation, challenge bypass, mirror, or blocked-source retry was used.

| URL | UTC request start | HTTP | Response SHA256 |
| --- | --- | --- | --- |
| https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/src/schemes/scheme.py | 2026-10-14T15:12:37.549750+00:00 | 200 | `3684c5f6d762fff39db1ebee60ab6465469d627443c875d7fa1a9f6be35337fe` |
| https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md | 2026-10-14T15:12:55.313537+00:00 | 200 | `7b0761ecc0fa1988cb2ef0efeca503af974eeb6ade76d30629308ebba7e78341` |
| https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/results/addition_reduced_ZT/4x4x6_m73_cr280_cn540_ZT_reduced.json | 2026-10-14T15:12:57.403762+00:00 | 200 | `cbc252aaf1694aa0cb565cf4a4c3e9d418697afad253af77e25611dc66852222` |

The initial sandbox attempt for the Scheme URL at `2026-10-14T15:12:21.752235+00:00` failed at DNS before HTTP; its receipt records null HTTP status, zero response bytes, and null SHA256. The one successful HTTP request used ordinary allowed network escalation. The denied optional URLs recorded in `claim/LITERATURE_ACCESS.md` were not requested.

Reproduction commands, from the run directory:

```sh
python3 panel/reproduce-code/check_integer_slp.py claim/scheme.json --candidate
python3 panel/reproduce-code/run_checks.py
```

Scope: this is complete mathematical reproduction of the immutable circuit and its literal operation count. It does not assert novelty, a rank lower bound, the full binding record criterion, or exact replay of the whole discovery/search history. No criterion, object, source package, publication, or schedule was changed.

pass: true
