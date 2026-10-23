context: subagent (fork_turns none; isolated capsule)
role: REPRODUCE
id: fmm-additive-complexity-records
UTC: 2026-10-14T13:22:37.141543+00:00

PROVED-HERE: `claim/scheme.json` computes the complete integer product of a 2x4 matrix and a 4x8 matrix, with 51 active, distinct bilinear products and exactly 182 binary additions/subtractions, split U 37, V 68, W 77. Expanded product factors are ternary. Output entry C[i,j] has index j*2+i.

I read only this run's isolated claim capsule and the applicable repo instructions. I did not read sibling panel files, attempts, other runs, charters, prior verdicts or prior reasoning. I wrote and ran `panel/reproduce-code/check.py` before opening `claim/verify.py`. The independent checker's SHA256 was already 3a95eb30b089964bbbb2e26f95256be00e8f3646f5a65bd7b85a396d99258f79 when its first candidate result was printed at 2026-10-14T13:15:47.774606+00:00. That checker is unchanged. The Python version is 3.9.6.

The saved source definition is "Each file describes a bilinear algorithm for multiplying an `n₁×n₂` by `n₂×n₃` using `m`multiplications." The checked matrix definition is A[i,h] at offset i*4+h, B[h,j] at offset h*8+j, and C[i,j] = sum over h of A[i,h]*B[h,j]. The claim specifies that output C[i,j] is entry j*2+i. The reduced JSON schema appends each fresh variable after its existing stage values. It then forms each explicit product from the corresponding U and V terminal rows and forms the W outputs from those products. This agrees with the schema in `claim/data/README.md`, whose SHA256 is 7b0761ecc0fa1988cb2ef0efeca503af974eeb6ade76d30629308ebba7e78341.

The binding arithmetic convention says "each binary +/- between already-computed quantities counts one; multiplication by -1 is free; multiplication by any other scalar is not allowed in a ternary SLP". I apply that convention literally. A k-term literal sum costs k-1 operations. Single-term aliases and signs cost zero. I do not require ternary intermediate expanded forms.

## Independent result

The checker expands all linear forms with Python integers and compares every coefficient of the resulting bilinear tensor with the matrix definition. It also executes the literal instructions independently for every pair of input basis matrices. This checks all 4,096 tensor coefficients and all 4,096 output values from 256 input basis pairs, with zero mismatches in both methods. A repeated run produced byte-identical output at 2026-10-14T13:20:38.305634+00:00.

| Quantity | Independent result |
|---|---:|
| Format | 2x4x8 |
| Explicit products | 51 |
| Active, distinct products up to free factor signs | 51 |
| U additions | 37 |
| V additions | 68 |
| W additions | 77 |
| Total additions | 182 |
| Expanded naive additions | 354 |
| Integer tensor mismatches | 0 |
| Direct basis output mismatches | 0 |

Every fresh row is binary. U has 37 fresh rows, V has 68, and W has 77. All terminal rows are positive, single-term aliases, so they add no operations. `binary_operations.json` records every one of the 182 charged operations. Every present instruction coefficient is an integer +1 or -1, every reference is backward or to an existing base quantity, and there are no repeated references within candidate rows. All expanded U, V and W factor coefficients belong to {-1,0,1}.

The W stage contains intermediate expanded coefficients -2 and +2. They arise from charged unit-coefficient additions. They are allowed by the criterion, and the final W factor matrix is ternary. U and V intermediates remain ternary. There are no scalar multiplications concealed by a coefficient 2, no extra products, and no division or other arithmetic operations in the interpreted language. The sole extra JSON key is string metadata `research_method`.

The gate audit checks both ordinary dependency reachability and net linear influence on every terminal. It finds no dead or net-unconsumed fresh gates, no zero fresh forms, and no duplicate fresh forms up to sign. Every explicit product has nonzero U and V factors, a nonzero expanded W column, and a unique U tensor V factor up to free signs. The cost metadata agrees exactly with both the literal count and the expanded naive count.

## Positive public calibration

KNOWN: I fetched the public [Perminov 2x4x8 rank-51 reduced circuit](https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/results/addition_reduced_ZT/2x4x8_m51_cr188_cn354_ZT_reduced.json) with one ordinary V3R1T4S GET that reached the server. The initial sandbox attempt failed at local DNS and received no server response; its record is `public-188.dns-failure.json`. An ordinary request outside that DNS restriction received HTTP 200 at 2026-10-14T13:16:29.468182+00:00, finished at 2026-10-14T13:16:29.595588+00:00, and returned 11951 bytes. No denial, mirror or access-control bypass was involved. The raw source SHA256 is b68445935df00311217280a30d628395594619584691d8264723045b2b62131a.

The same independent checker verifies this public circuit over the integers on all 4,096 coefficients and all 256 basis pairs. It counts U 38, V 72, W 78, totaling 188 additions, matching the public cost metadata. This calibrates the schema, indexing, ternary-factor check and counting convention against a current public object. The complete current-table minimum and novelty comparisons belong to the other panel roles; this reproduction verdict establishes the mathematical object and its arithmetic count.

## Controls

All 22 controls returned their expected result. `controls.json` and `extra_controls.json` contain the full results.

- Exact elementary multiplication passes. A two-operation 2a-a intermediate passes with ternary final factors.
- Negating the sole alias for output zero creates four incorrect integer tensor coefficients and four incorrect directly executed output values, while creating zero modulo-two mismatches. This confirms that the checker detects a sign error that binary-field testing misses.
- Invalid references, a forward self-reference, a coefficient 2, a floating coefficient, a boolean index, and a binary-field flag are rejected.
- Duplicate products, a zero product factor, an unused product and an expanded coefficient-2 product factor are rejected. An understated addition count is rejected.
- An appended dead gate is detected and still charged, increasing the literal count to 183.
- A consistent internal sign change, a pair of free negative aliases, a consistent permutation of products, and reversal of every signed-sum operand list preserve the integer identity and the 182 count.
- Replacing the specified output order with row-major output order creates 112 mismatches.
- Separate terminal binary and three-term sums are charged one and two operations respectively.

## Supplied checker comparison

Only after the independent checker and the initial controls had run did I read and execute `claim/verify.py`. Its SHA256 is 52cfb7166cc61de245463fabfa8f314dfe4f5de9a13943e91f9ba5757eae94f6. Its actual output is:

```json
{"valid": true, "format": [2, 4, 8], "rank": 51, "addition_counts": {"u": 37, "v": 68, "w": 77}, "additions": 182, "identities_verified": 4096}
```

The supplied verifier agrees with the independent identity and count. It does not itself prove expanded ternary factors, active distinct products, cost metadata or gate consumption; the independent checks cover those properties.

## Exact rerun commands

Run these from this run's directory, with the already-saved public source file:

```sh
python3 panel/reproduce-code/check.py claim/scheme.json --trace panel/reproduce-code/binary_operations.json > panel/reproduce-code/candidate.json
python3 panel/reproduce-code/check.py panel/reproduce-code/public-188.json --trace panel/reproduce-code/public-188-binary_operations.json > panel/reproduce-code/public-188-check.json
python3 panel/reproduce-code/controls.py
python3 panel/reproduce-code/gate_audit.py
python3 panel/reproduce-code/extra_controls.py
python3 claim/verify.py claim/scheme.json
python3 panel/reproduce-code/check.py claim/scheme.json > panel/reproduce-code/candidate-repeat.json
cmp panel/reproduce-code/candidate.json panel/reproduce-code/candidate-repeat.json
python3 panel/reproduce-code/summary.py
```

The one successful ordinary public fetch command was:

```sh
python3 panel/reproduce-code/fetch.py https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/results/addition_reduced_ZT/2x4x8_m51_cr188_cn354_ZT_reduced.json panel/reproduce-code/public-188.json
```

The result and code hashes are in `panel/reproduce-code/manifest.json`; the actual consolidated output is `panel/reproduce-code/summary.out`. The candidate SHA256 is 289432a72c0f86a04925e6475d31d4ff86d92a65fb8d57f4b57f918c3866d654. The independent checker SHA256 is 3a95eb30b089964bbbb2e26f95256be00e8f3646f5a65bd7b85a396d99258f79. The operation-trace SHA256 is 87bb259ed8b1a8d7df40138e13fec4f5542c51d1c30866c4ad2706ae66a911ad.

I read the provenance limit. This verdict reproduces the immutable mathematical circuit in full. It does not claim an exact replay of the whole discovery history, and such replay is not required to establish this identity and cost. I did not request the optional IACR PDF recorded as blocked in `claim/LITERATURE_ACCESS.md`. I did not modify the circuit or criterion and took no outward action.

pass: true
