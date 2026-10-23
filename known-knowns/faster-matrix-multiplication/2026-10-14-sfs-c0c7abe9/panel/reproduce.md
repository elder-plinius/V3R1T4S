# REPRODUCE

context: subagent (fork_turns none; isolated capsule)

PROVED-HERE: The immutable `claim/scheme.json` computes the ordered 5×5×5 matrix product exactly over Z using 93 active, distinct bilinear products and 354 binary additions/subtractions, with ternary final expanded factors and only literal ±1 scalars.

The candidate SHA256 is `c0c7abe9136e5f773d01c5c276cb1f6c3f565afab183499fdda63ac67947e02e`. I inspected only the isolated claim, the permitted kit instructions, and independently fetched public primary sources. I did not inspect sibling panels, prior runs, attempts, charters, parent reasoning, or earlier verdicts. I did not edit the candidate or criterion.

## Independent definition and checker

I wrote and executed `panel/reproduce-code/independent.py` before reading `claim/verify.py`. Its SHA256 is `3a86286c8adf1603978aab4bdbddb06687cfb223a662e5729a3d5f10cda3d4b2`; the recorded initial execution UTC is `2026-10-14T14:56:08.806975+00:00`. The definition is:

> A[i,k] has index i*5+k; B[k,j] has index k*5+j; C[i,j] has index j*5+i.

Therefore the coefficient of A[a]B[b] in C[c] is one exactly when the ordinary row, shared dimension, and column match, and zero otherwise. Equivalently, it is the sum over products of U[r,a]V[r,b]W[c,r]. I constructed this target directly; I fitted no permutation to the candidate.

KNOWN: Dron Perminov's public [`Scheme.naive`](https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/src/schemes/scheme.py), lines 35–49 in the saved response, independently uses `i*n2+k`, `k*n3+j`, and `j*n1+i`. Its reduced parser appends fresh variables after the corresponding base namespace and transposes final output rows into W columns. I audited and executed only the small `naive` method extracted by AST, with a local constructor that captures its dense arrays, rather than importing the remote module. Positive controls for asymmetric 2×3×4 and 5×5×5 passed; the asymmetric control exposes accidental coordinate symmetries.

PROVED-HERE: The independent checker expands the complete integer circuit, checks all 15,625 tensor coefficients including the zeros, and separately executes the literal SLP on every one of the 625 input basis pairs, checking all 25 outputs per pair. There are zero mismatches in either route. Python integers supply exact arithmetic; this is exhaustive verification of this bilinear object, not a sample or a floating-point test. Two subsequent independent verifications returned identical diagnostics.

## Structure, coefficient class, and cost

PROVED-HERE: All fresh references are backward within their own namespaces; all final references exist. Every term has exactly an integer `index` and a literal integer `value` in {−1,+1}; unexpected expression fields, nonunit literals, and duplicate JSON keys are rejected. The U and V namespaces contain only their respective inputs and signed sums. W contains only products and signed sums. Thus the only nonunit multiplications performed by the represented object are its 93 explicit U×V products.

All 93 U factors, 93 V factors, and 93 W product columns are nonzero. All 93 rank-one summands are distinct, including after normalization up to sign. This verifies the decomposition's multiplication count; it does not independently prove a lower bound on tensor rank. The live rank table separately lists rank 93 for this ordered format.

All final U, V, and W coefficients belong to {−1,0,+1}. Intermediate maximum absolute coefficients are U=1, V=1, W=2. The W value 2 comes from charged binary sums and is allowed: final W factors remain ternary. I neither reject paid intermediate 2 nor permit a free literal scalar 2.

Each literal row of k terms is charged k−1 binary additions/subtractions; aliases and unit negation are free. Every listed fresh row is charged, even if it were unused. The candidate has 93 U, 96 V, and 165 W fresh rows, each binary, and only single-term final aliases. The independently derived total is **93+96+165=354**. Literal execution charges 354 operations per basis pair, or 221,250 across all pairs. Expanded naive cost is 843. Both saved cost metadata fields match the independent counts.

## Controls and supplied verifier

PROVED-HERE: All 11 negative controls were rejected: a changed output sign; a tripled output formed with two paid additions; self/forward reference; free literal scalar 2; underreported cost; mod-2 flag; extra expression field; wrong declared rank; nonternary expanded final factor; inactive product; and duplicate tensor summands. The changed-sign control remains structurally valid and ternary, yet has five wrong integer coefficients and zero mod-2 mismatches. The tripled-output control likewise has five integer mismatches and zero mod-2 mismatches. This demonstrates rejection of corruptions invisible over F2. A separate valid one-product control accepts a paid intermediate 2 followed by subtraction, charging both operations and retaining a ternary final factor.

The independently fetched public [rank-93 reduced source control](https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/results/addition_reduced_ZT/5x5x5_m93_cr383_fv160_cn843_ZT_reduced.json) passes all 15,625 integer identities and 625 literal basis pairs. Its count is independently recovered as 103+105+175=383 and naive 843. The candidate's 354 is below that particular source control; this panel does not assert that this one file exhausts current published comparisons.

Only after my own checker passed did I read and run `claim/verify.py` (SHA256 `52cfb7166cc61de245463fabfa8f314dfe4f5de9a13943e91f9ba5757eae94f6`). Its real output agrees:

```json
{"valid": true, "format": [5, 5, 5], "rank": 93, "addition_counts": {"u": 93, "v": 96, "w": 165}, "additions": 354, "identities_verified": 15625}
```

The supplied checker does not itself certify final factor ternarity, activity/distinctness, or agreement with cost metadata. It accepts controls with altered metadata or an extra expression field. The independent checks supply these missing validations; the candidate itself contains neither defect.

## Honest access receipts

KNOWN: Each source below received one ordinary public GET using a V3R1T4S-named User-Agent. Requested and actual URLs agree. Bodies and full receipts are preserved under `panel/reproduce-code/sources/`.

| Actual URL | UTC | HTTP status | Body SHA256 |
| --- | --- | --- | --- |
| https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/src/schemes/scheme.py | 2026-10-14T14:52:48.080395+00:00 | 200 | `3684c5f6d762fff39db1ebee60ab6465469d627443c875d7fa1a9f6be35337fe` |
| https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/results/addition_reduced_ZT/5x5x5_m93_cr383_fv160_cn843_ZT_reduced.json | 2026-10-14T14:57:00.148971+00:00 | 200 | `808285b8fb393d2e950ecff4ffe9881a209b6d3eff0d787e34d801a3f22293da` |
| https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json | 2026-10-14T14:56:59.154128+00:00 | 200 | `d0da2c364dcf4d13c0721ea8b7c3dcd7fae4f6f3c843d22a714a1ccb9bd244c1` |

The initial sandbox source attempt at `2026-10-14T14:52:37.434720+00:00` failed local DNS resolution and made no HTTP exchange. Ordinary `require_escalated` access then produced the single actual source GET; the no-HTTP attempt has a separate receipt. There was no HTTP denial retry, mirror, or bypass. I made no request to any denied URL listed in `claim/LITERATURE_ACCESS.md`.

## Reproduction and limits

From the run directory, execute:

```sh
python3 panel/reproduce-code/independent.py
python3 panel/reproduce-code/audit_after.py
```

These use saved primary responses and need no network. Detailed results are in `independent-results.json` and `secondary-results.json` within `panel/reproduce-code/`.

The pass covers exact reproduction, coefficient class, multiplication structure, and the 354-operation value for this immutable object. It does not certify the whole discovery search, reconstruct unrecorded dictionaries or runtime hashes, establish uniqueness/global optimality, or complete the separate current-literature and minimum-across-all-records novelty comparison. The claim's stated whole-search replay limit remains in force. No publication or outward communication occurred.

## Portability supplement

PROVED-HERE: Added `panel/reproduce-code/portable.py`, a self-contained standard-library CLI that accepts exactly one JSON path, fixes the expected ordered format to 5×5×5 and multiplication count to 93, prints the exact verification diagnostics, and exits nonzero for invalid input. It requires no public response files, sibling Python modules, network access, or source-directory writes. Its verification class/functions are verbatim copies of my independently authored definitions; AST source-segment equality confirmed this. The initial `independent.py` and its before-author evidence remain unchanged. No mathematical check, candidate, or criterion was changed.

Portable checker SHA256: `b182637d54e75757c6204525a8e987a482eee5475351a9d2585fb0921181044a`. Original independent checker SHA256 remains `3a86286c8adf1603978aab4bdbddb06687cfb223a662e5729a3d5f10cda3d4b2`. Candidate SHA256 remains `c0c7abe9136e5f773d01c5c276cb1f6c3f565afab183499fdda63ac67947e02e`. Initial `independent-results.json` SHA256: `79dd0775040df2b1faba25f8f375b410d2de3ecbda97ab9c5fda9080611df037`.

At UTC `2026-10-14T15:26:08.738653+00:00`, `python3 panel/reproduce-code/test_portable.py` copied only the CLI and the three JSON inputs into a fresh temporary directory. It executed the following actual commands there; the table extracts fields from their literal JSON stdout. Every full output equals the diagnostics returned by the unchanged independent functions, and every stderr is empty.

| Actual command | Exit | Additions | Integer coefficients checked | Integer mismatches | Literal basis pairs | Literal output mismatches | pass |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `python3 portable.py candidate.json` | 0 | 354 | 15625 | 0 | 625 | 0 | true |
| `python3 portable.py public383.json` | 0 | 383 | 15625 | 0 | 625 | 0 | true |
| `python3 portable.py corrupt-sign.json` | 1 | 354 | 15625 | 5 | 625 | 5 | false |

The corrupt-sign object is saved as `panel/reproduce-code/corrupt-sign.json`; its JSON stdout reports `"failures": ["integer tensor mismatch", "literal execution mismatch"]`, while `"mod2_tensor_mismatches": 0`. The clean directory contained only `portable.py`, `candidate.json`, `public383.json`, and `corrupt-sign.json`; its file names and hashes were identical before and after all CLI executions.

Full commands, exit codes, literal stdout/stderr, diagnostics, and hashes are saved in `panel/reproduce-code/portable-results.json` (SHA256 `4682543a5e7f47efc1bcc073a10def1c300e3db3becc1d512613cf5b9f78bc3a`). To verify any standalone package object, run `python3 portable.py scheme.json` with only those two files present.

pass: true
