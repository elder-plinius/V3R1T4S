context: subagent (fork_turns none; isolated capsule)

PROVED-HERE: `scheme.json` is an exact integer program for the ordinary product of a 3×4 matrix and a 4×5 matrix, with 47 active distinct bilinear products and 156 literal binary additions/subtractions. Reproduction succeeds.

I read only the isolated `claim/` capsule and applicable `repo/AGENTS.md`, `repo/kit/RULES.md`, and `repo/kit/RUN.md` steps 6–7, plus the two fresh public sources recorded below. I did not read sibling panels, another run/attempt, prior findings/verdicts/reasoning, or the charter. No criterion or candidate-object file was edited. The candidate SHA256 is `e227d795fa1418070e30f21b18eac6a55d7426e51cfc8f8ef99c57b831d021f2`.

Definition quoted from `CLAIM.md`: “each binary +/- between already-computed quantities counts one; multiplication by -1 is free; multiplication by any other scalar is not allowed in a ternary SLP”. I used Python standard-library code and exact integers, with no floating-point or finite-field substitute.

**Independent derivation and chronology.** Before opening `verify.py`, I wrote `panel/reproduce-code/checker.py`. It expands append-ordered sparse variables over integer coordinate vectors. For each product r, let U[r,a] and V[r,b] be its expanded input factors, and let W[c,r] be its expanded output coefficient. Then the coefficient of A[i,k]B[k',j] in output C[i',j'] is

`sum_r W[c,r] * U[r,a] * V[r,b]`,

which must equal `int(i == i' and k == k' and j == j')`. The input coordinates are `a = i*4+k`, `b = k'*5+j`; the explicitly stated output coordinate is `c = j'*3+i'`. Every one of the 3600 coefficients is tested, including zero coefficients. A separate literal interpreter evaluates every one of the 240 input basis pairs and compares all output entries with ordinary matrix multiplication.

My first checker version guessed column-major inputs, resulting in 116 coefficient mismatches and 102 basis-pair mismatches. I retained this diagnostic error and corrected the checker assumption. The input convention is independently fixed by the fresh primary schema implementation, `Scheme.naive`, whose lines 45–47 assign `u[index][i*n2+k] = 1`, `v[index][k*n3+j] = 1`, and `w[index][j*n1+i] = 1`. `convention-audit.py` parses those assignments as data without importing or running the downloaded source. The four input-order diagnostics were A row/B row: 0, A row/B column: 108, A column/B row: 100, and A column/B column: 116; these diagnostics do not define the accepted product. The primary definition and ordinary elementary matrix checks define it.

The independent checker and complete controls were recorded before author-code inspection at `2026-10-14T13:46:44.000830+00:00` in `independent-before-author.json`; it explicitly records `author_verifier_read: false`. The checker hash at that point was `e34a706e20f0eb4554c94cd870273cd819afcbb401afc285a3c155e7484dc848` and the controls hash was `87017e0975b29861d0c7ca818691d46cbd4e9fcb88173ba860d667bbdab6f0d4`. The original pre-author controls output is preserved as `controls-results-before-author.json` with SHA256 `c0f28ad9e70cb2278b9a7fa39d33daf111e0d09733865b6399d39ce48d34e9cd`. Only afterwards did I read and execute `verify.py`; it agrees with the independent result.

**Exact candidate results.**

| Check | Executed result |
|---|---:|
| Integer tensor coefficients checked | 3600 |
| Coefficient mismatches | 0 |
| Literal basis pairs checked | 240 |
| Basis-pair mismatches | 0 |
| Tensor nonzero coefficients | 60 |
| Active products with nonzero U, V, and W support | 47 |
| Distinct products after normalizing independent U/V signs | 47 |
| Expanded U shape | 47×12 |
| Expanded V shape | 47×20 |
| Expanded W shape | 15×47 |
| All expanded terminal U/V/W entries in {−1,0,1} | true |
| Expanded naive addition count | 277 |

The tensor test is exhaustive and proves the bilinear identity over Z for all inputs, rather than merely demonstrating sample products. The support and distinction tests establish 47 active products in this program; they do not assert a separate lower-bound proof of minimum tensor rank.

**Literal operation count and reachability.** Every sparse form with k terms lowers to k−1 binary gates in a sequential accumulation. A single signed reference is an alias and costs zero. Signs are free edges; every term coefficient is exactly the integer +1 or −1. The checker rejects unavailable/forward/self references, nonunit scalars, extra instruction keys, or an unsupported top-level operation. U and V only compute linear forms over their own input bases, W only computes linear forms over the 47 explicit product bases; there is no place to hide an additional multiplication or scalar operation.

| Stage | Fresh-form gates | Terminal-form gates | Total gates | Variables declared/reached | Gates declared/reached |
|---|---:|---:|---:|---|---|
| U | 38 | 0 | 38 | 50/50 | 38/38 |
| V | 44 | 0 | 44 | 64/64 | 44/44 |
| W | 23 | 51 | 74 | 70/70 | 74/74 |

Total: `38 + 44 + 74 = 156`. A separately lowered binary dependency graph matches the expression-length count exactly and reaches every declared gate from the outputs. Every base variable and every fresh variable is reached. All 47 product variables are reached and also have nonzero expanded output support. Both U and V terminal lists contain only single-term aliases, contributing zero additions; the candidate has no fresh one-term alias. The recorded `complexity.reduced` and `complexity.naive` values match the independent 156 and 277 counts.

Expanded intermediate vectors are allowed to have arbitrary integer coefficients produced by charged ± gates. There is no intermediate ternary restriction. This candidate's fresh vectors and lowered partial sums happen to have maximum absolute coefficient one. The charged-intermediate-two control below demonstrates acceptance of a valid magnitude-two intermediate at its full charge.

**Fresh public-source calibration.** KNOWN: Dron Perminov's public 161-addition reduced program was fetched once after the initial sandbox DNS failure; no HTTP-denial response was retried. The fresh public program passes the same 3600 exact coefficients and 240 literal basis pairs with zero mismatches, 47 active distinct products, ternary expanded U/V/W, and complete variable/gate reachability. Its independently derived cost is `39 + 48 + 74 = 161`. Candidate and fresh public U/V/W expansions are exactly equal entry for entry in all three stages; the reproduced improvement is in the evaluation schedule. The candidate saves `161 − 156 = 5` additions against this calibration.

| Purpose | Exact source URL | UTC start / finish | HTTP | Response SHA256 | Bytes |
|---|---|---|---:|---|---:|
| Public 161 circuit | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/results/addition_reduced_ZT/3x4x5_m47_cr161_cn277_ZT_reduced.json | 2026-10-14T13:41:27.588020+00:00 / 2026-10-14T13:41:27.717439+00:00 | 200 | `d1248a3a32dd03bf5d9216edfdaf6b01be95987d7cefee03f5f9f9645271319a` | 10825 |
| Independent coordinate definition | https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/src/schemes/scheme.py | 2026-10-14T13:43:17.532058+00:00 / 2026-10-14T13:43:18.372975+00:00 | 200 | `3684c5f6d762fff39db1ebee60ab6465469d627443c875d7fa1a9f6be35337fe` | 52974 |

Each GET used `User-Agent: V3R1T4S reproduction skeptic`. Raw responses and complete fetch records are saved. `public161.network-error.json` records the earlier sandbox-only DNS failure with no HTTP status; ordinary `require_escalated` execution then performed the public GET. No denied IACR/SIAM URL, mirror, cookie, proxy, challenge bypass, or alternate copy was requested. The historical denied PDFs remain the stated literature-access gaps in `LITERATURE_ACCESS.md`; no contents of them are asserted here.

**Meaningful controls.** `controls.py` saves every control object, its object hash, complete checker output, expected result, and whether the expectation was met. All expectations succeeded.

| Control | Accepted? | Evidence |
|---|---|---|
| candidate | true | 156 additions; zero tensor/basis mismatches |
| public161 | true | 161 additions; zero tensor/basis mismatches |
| uncorrected-product-sign | false | 5 integer coefficient and 5 basis-pair mismatches, while every error is even and the tensor still matches modulo two |
| output-swap | false | 16 coefficient mismatches and 8 basis-pair mismatches, despite ternary factors and unchanged cost |
| product-permutation | true | Coherently swaps two product factors and their W references; exact identity and cost 156 preserved |
| compensated-product-sign | true | Flips one U factor and every corresponding W reference; exact identity and cost 156 preserved |
| free-negative-alias | true | Adds a reachable negative alias and rewires equivalent uses; exact identity and cost 156 preserved, alias charged zero |
| charged-intermediate-two | true | Computes a0+a0 then subtracts a0; a reachable coefficient 2 is accepted, terminal factors stay ternary, and both extra binary gates are charged for cost 158 |
| nonunit-scalar | false | Rejected: explicit coefficient 2 |
| hidden-operation-key | false | Rejected: extra scalar/operation key |
| self-forward-reference | false | Rejected: first fresh U form references unavailable index 12 |
| understated-cost | false | Rejected: metadata 155 disagrees with literal 156 |
| unreachable-gate | false | Identity remains correct, but appended fresh U variable 50 and its gate are unreachable; rejected with literal cost 157 |

Elementary checks independently compute the ordinary matrix product by triple loops for both candidate and public calibration. The single-entry case is A[1,2]=1 and B[2,3]=1, giving C[1,3]=1 at output index 10 and zero elsewhere. A=[1,…,12] and B=[1,…,20] in row-major order give rows `[110,120,130,140,150]`, `[246,272,298,324,350]`, and `[382,424,466,508,550]`. Both circuits also pass the saved dense signed-matrix case. These checks corroborate the independently sourced indexing; the proof still rests on all integer tensor coefficients.

**Executed commands and outputs.** The locally reproducible suite, executed from the run directory, is:

```sh
python3 panel/reproduce-code/run.py
```

That executed these exact subprocess commands:

```sh
python3 panel/reproduce-code/convention-audit.py
python3 panel/reproduce-code/checker.py claim/scheme.json
python3 panel/reproduce-code/checker.py panel/reproduce-code/public161.json
python3 panel/reproduce-code/controls.py
python3 claim/verify.py claim/scheme.json
python3 claim/verify.py panel/reproduce-code/public161.json
python3 panel/reproduce-code/checker.py claim/scheme.json
```

Every subprocess exited zero. `execution-log.json` and `execution-log.txt` contain the full command strings, UTC start/finish, exit code, unabridged stdout/stderr, and stdout hashes. The candidate checker was executed twice and produced byte-identical stdout and stderr. The author verifier output was:

```json
{"valid": true, "format": [3, 4, 5], "rank": 47, "addition_counts": {"u": 38, "v": 44, "w": 74}, "additions": 156, "identities_verified": 3600}
{"valid": true, "format": [3, 4, 5], "rank": 47, "addition_counts": {"u": 39, "v": 48, "w": 74}, "additions": 161, "identities_verified": 3600}
```

Network commands were executed from the research workspace:

```sh
python3 runs/2026-10-14-1335/panel/reproduce-code/fetch.py
python3 runs/2026-10-14-1335/panel/reproduce-code/fetch.py
python3 runs/2026-10-14-1335/panel/reproduce-code/fetch.py https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/src/schemes/scheme.py public-scheme-source
```

The first returned the saved DNS error with exit one; the second was ordinary sandbox escalation and returned HTTP200 with exit zero; the source-definition GET also used ordinary escalation and returned HTTP200 with exit zero. Fetch records above contain their full outputs. Initial direct checks and the input-order diagnostic preceded the final suite; the initial convention error, correction, counts, and before-author checkpoint are retained above. `sha256-manifest.json` records the saved code, responses, control objects, logs, and unchanged capsule-object hashes.

**Stated provenance scope.** The exact immutable mathematical object and its instruction cost reproduce from the capsule. I preserve the capsule's explicit limitation: “the search did not capture entire original dictionaries or runtime code hashes. No exact replay of the whole discovery history is claimed.” This object verification does not substitute a claim of replaying its entire discovery search. The REPRODUCE verdict establishes the saved object's correctness and cost; live global comparison and the full success criterion are the separate NOVELTY and CRITERION panel responsibilities.

pass: true
