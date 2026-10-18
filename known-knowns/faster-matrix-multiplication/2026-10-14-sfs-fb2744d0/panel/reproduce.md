# Reproduction judgment

Context: fresh REPRODUCE subagent; reproduction only. The candidate passes an exact independent check as an integer bilinear program for `(2,5,5)` with 40 active products and 148 binary additions/subtractions. This judgment does not establish the live record comparison or novelty.

The audited candidate is [scheme.json](../claim/scheme.json), SHA-256 `fb2744d037444d6e5f84f56628cf97a01ad2650e374421fbe4961bfafefd7ca2`.

## Independent definition and method

I requested Perminov's primary README independently. The sandbox attempt stopped at DNS before an HTTP response; the single authorized network request returned HTTP 200. The [saved definition](reproduce-code/primary-readme.md), [response headers](reproduce-code/primary-readme.headers), and [request manifest](reproduce-code/manifest.json) preserve this evidence. Its full-format example establishes row-major inputs and flattened `C^T` outputs; its reduced-format definition establishes fresh indices starting at 10, 25, and 40 respectively, with 40 U/V final forms and 10 W final forms. The binding convention in [CLAIM.md](../claim/CLAIM.md) supplies one cost per binary addition/subtraction and free sign/copy operations.

I wrote [check_independent.py](reproduce-code/check_independent.py) from that definition, using only the Python standard library, before reading or running the author's verifier. It expands every intermediate and final form over integers, validates every term and sequential reference, rejects duplicate sparse indices and forbidden scalars, checks intermediate liveness, and recomputes both reduced and expanded naive costs. Descriptive metadata has no execution semantics and was ignored.

The exact tensor contraction checks all `10 × 25 × 10 = 2,500` integer bilinear coefficients, including every zero coefficient, against `C[i,j] = sum_t A[i,t] B[t,j]`. A separate literal scalar evaluation executes all 250 input basis pairs and checks all 2,500 output values. Input order is `A[i,t] -> i*5+t`, `B[t,j] -> t*5+j`; output order is `C[i,j] -> j*2+i`. No sampling or modular arithmetic is used.

## Arithmetic and gate audit

| Stage | Fresh-form additions | Final-form additions | Total | Fresh variables | Free final aliases/signs |
|---|---:|---:|---:|---:|---:|
| U | 31 | 0 | 31 | 31 | 40 |
| V | 11 | 44 | 55 | 11 | 17 |
| W | 62 | 0 | 62 | 62 | 10 |
| Total | 104 | 44 | **148** | 104 | 67 |

All 194 supplied linear forms are audited in [candidate-audit.json](reproduce-code/candidate-audit.json), including complete expanded vectors and all references. Expanded U, V, and W coefficients belong to `{-1,0,1}`. All 40 products have nonzero left factors, right factors, and output columns; their complete rank-one tensors are nonzero, with no duplicate or opposite rank-one terms. The full product tensor has exactly 50 nonzero entries, all equal to 1. The independently recomputed naive expanded cost is 283.

For a fully explicit gate view, [emit_and_check_tape.py](reproduce-code/emit_and_check_tape.py) spells out [255 primitive instructions](reproduce-code/candidate-primitive-tape.json): 148 binary signed additions, 40 bilinear products, and 67 free aliases/signs. Every instruction references an existing value. Executing that tape on all 250 basis pairs performs 63,750 instruction evaluations and reproduces every output; see [tape-result.json](reproduce-code/tape-result.json). Rank 40 here means 40 active bilinear products, rather than a new lower-bound proof of minimal tensor rank.

## Controls and supplied verifier

[run_controls.py](reproduce-code/run_controls.py) accepts the saved [public 153-addition program](../claim/data/2x5x5_m40_cr153_cn283_ZT_reduced.json), independently counting U/V/W costs `34/55/64`. The public program and candidate have identical expanded U/V/W digests (`65a453e1db66f57aee3c7d9a2c2de6e62cc3b7b6601d92067e79215675314adb`). Thus the saved positive control confirms a five-addition schedule reduction for that same decomposition.

A second positive control inserts a fresh negative alias and a compensating negative final alias; it passes with unchanged 148 cost. All 15 corrupt negatives fail with the expected diagnostic: wrong product sign, wrong input order, wrong output order, a forward reference, a forbidden scalar, nonternary expanded coefficients despite locally ternary gates, an inactive product, wrong reduced cost, wrong naive cost, a duplicate sparse reference, a missing output, Z2 semantics, a boolean scalar, wrong rank, and wrong format. The [control report](reproduce-code/controls-result.json), individual saved programs, and actual stdout/stderr remain in `reproduce-code/`.

After completing the independent checker and controls, I read and ran the supplied verifier. It agrees: [candidate output](reproduce-code/author-candidate.stdout.json) reports rank 40, 148 additions, and 2,500 identities; [public-control output](reproduce-code/author-public153.stdout.json) reports 153 additions and the same 2,500 identities. The independent checker additionally supplies the coefficient-class, active-product, metadata-cost, liveness, and primitive-gate checks above.

Reproduce from the workspace root:

```sh
python3 research/runs/2026-10-14-1155/panel/reproduce-code/check_independent.py research/runs/2026-10-14-1155/claim/scheme.json --expected-additions 148 --audit research/runs/2026-10-14-1155/panel/reproduce-code/candidate-audit.json
python3 research/runs/2026-10-14-1155/panel/reproduce-code/run_controls.py
python3 research/runs/2026-10-14-1155/panel/reproduce-code/emit_and_check_tape.py
```

pass:true
