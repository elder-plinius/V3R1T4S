context: Fresh REPRODUCE subagent (/root/skeptic_reproduce_256), fork_turns=none; reviewed only the isolated claim, independent primary definitions, and its own reproduction artifacts; no sibling reports or prior verdicts read.

# REPRODUCE — subagent

The submitted integer straight-line program reproduces the full `(2,5,6)` matrix product with 47 active bilinear products and exactly 179 binary additions/subtractions. This verdict judges reproduction only.

## Independent check and ordering

I read `claim/CLAIM.md`, `claim/REPRODUCE.md`, the candidate JSON, and the supplied scheme-format documentation. I wrote and ran the standard-library checker [reproduce-code/check.py](reproduce-code/check.py) and its controls before reading or running `claim/verify.py`. The timestamp and hashes of that completed work are saved in [reproduce-code/pre-author-checkpoint.json](reproduce-code/pre-author-checkpoint.json). I read no earlier runs, attempts, panel reports, charters, or reviewer verdicts.

Primary repository definitions were obtained by ordinary public GETs for the [README](https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md), [scheme implementation](https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/src/schemes/scheme.py), and [public 181-addition scheme](https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/results/addition_reduced_ZT/2x5x6_m47_cr181_fv63_cn332_ZT_reduced.json). The sandbox requests failed at DNS resolution; ordinary network escalation then produced one HTTP 200 response for each source. Payloads, response metadata, timestamps, and SHA-256 hashes are in [reproduce-code/sources/](reproduce-code/sources/). No HTTP denial or challenge was retried. I observed `claim/LITERATURE_ACCESS.md` and did not request its known HTTP 403 PDF.

The README defines original pools of `n1*n2`, `n2*n3`, and `rank`, followed by consecutive fresh variables. `Scheme.naive` and `Scheme.__validate_equation` independently establish row-major input indices `A[i,k] = i*5+k`, `B[k,j] = k*6+j` and transposed output indices `C[i,j] = j*2+i`. The checker uses those conventions explicitly.

## Exact results

| Property | Candidate | Public positive control |
|---|---:|---:|
| Format | `(2,5,6)` | `(2,5,6)` |
| Active, distinct rank-one terms | 47 | 47 |
| A-side binary additions | 38 | 40 |
| B-side binary additions | 65 | 65 |
| Output-side binary additions | 76 | 76 |
| Total binary additions | **179** | **181** |
| Expanded naive additions | 332 | 332 |
| Exact integer tensor coefficients checked | 3,600 | 3,600 |
| Coefficient mismatches | 0 | 0 |
| Direct basis input pairs executed | 300 | 300 |
| Individual binary gate executions audited | 53,700 | 54,300 |
| Individual product executions audited | 14,100 | 14,100 |

For each of the 12 outputs, all 10 A inputs and 30 B inputs were considered. The complete tensor contains the expected 60 coefficients equal to one and 3,540 equal to zero. This is exact integer arithmetic and exhaustive symbolic checking, with no sampling or finite-field substitution.

The checker independently expands every fresh and final form, assembles the tensor from all 47 outer products, and also executes the literal scalar schedule on all 300 basis input pairs. It audits every materialized binary prefix gate against its expanded form during every direct execution. The full expanded forms, every binary gate, every free assignment, and both complete tensors are saved in [reproduce-code/candidate/audit.json](reproduce-code/candidate/audit.json). A concrete schedule is in [reproduce-code/candidate/straight_line_program.txt](reproduce-code/candidate/straight_line_program.txt). Exact summary and console output are in [reproduce-code/candidate/summary.json](reproduce-code/candidate/summary.json) and [reproduce-code/candidate-output.txt](reproduce-code/candidate-output.txt).

The literal count is `38 + (28 + 37) + (20 + 56) = 179`: 38 fresh U gates and no final U gates, 28 fresh V gates and 37 final V gates, 20 fresh W gates and 56 final W gates. Every row of length `k` is compiled to `k-1` binary operations; singleton signs/copies are free. The 47 bilinear multiplications are distinct from the addition count. Metadata does not supply the measured count.

All 86 fresh variables are reachable from consumed final forms; all 10 A entries, 30 B entries, and 47 product inputs are live. Every product has a nonzero expanded U form, V form, and W column. Every sparse index is an exact nonnegative integer and references an earlier fresh variable or an existing base input. Every literal coefficient is an exact integer `+1` or `-1`; there are no hidden scalar operations. Every fully expanded fresh and final U/V/W coefficient lies in `{-1,0,1}`. The candidate has 47 positive singleton U aliases and, on V, 16 positive and 5 negative singleton aliases, all charged zero.

A supplementary exhaustive comparison of each product's complete 3,600-entry rank-one tensor also finds 47 nonzero, distinct contributions for both programs, including invariance to factor-sign gauges; results are in [reproduce-code/rank-one-distinctness.json](reproduce-code/rank-one-distinctness.json).

The candidate's expanded final U, V, and W arrays agree entry-for-entry with the freshly downloaded public scheme, as saved in [reproduce-code/expanded-comparison.json](reproduce-code/expanded-comparison.json). Its reduction is entirely the A-side schedule, from 40 additions to 38.

Candidate SHA-256: `6e554e0ee89a3fda23f7c59d261ca1f27bcb089e141db911246437ca50e931e9`.

Public control SHA-256: `3fa1d3759dbc1fec75c4330046151e028ef5cccaaebb70e7b936db4d0ecd5db9`.

## Controls and author comparison

The independent checker passes the public 181-addition scheme and three semantic equivalents of the candidate: paired factor negations, a live free negative alias, and reversed sum order. It rejects 15 saved corruptions covering integer-only correctness, output ordering, self/forward references, undeclared final references, scalar 2, float coefficients, Boolean indices, dishonest count metadata, a dead fresh gate, a zero product operand, expanded coefficient 2, Z2 mode, wrong dimensions, unknown hidden operations, and duplicate sparse indices. All 18 controls matched their expected outcome. A single product sign corruption produced 48 wrong integer coefficients; those errors are all even, so that corruption specifically defeats a modulo-two-only checker. Swapping the first two output forms produced 20 wrong coefficients.

The executable controls and their exact JSON inputs and outputs are saved in [reproduce-code/controls.py](reproduce-code/controls.py), [reproduce-code/controls/](reproduce-code/controls/), and [reproduce-code/controls-output.json](reproduce-code/controls-output.json).

Only after the independent work and checkpoint did I inspect and execute the author's verifier. It also reports candidate counts `(38,65,76)` totaling 179, public-control counts `(40,65,76)` totaling 181, and 3,600 verified identities for both. Its exact output is in [reproduce-code/author-candidate-output.txt](reproduce-code/author-candidate-output.txt), [reproduce-code/author-public181-output.txt](reproduce-code/author-public181-output.txt), and [reproduce-code/author-verifier-runs.json](reproduce-code/author-verifier-runs.json). The independent result covers additional liveness, active-product, expanded-ternary, metadata, and gate audits.

To rerun from the run directory:

```sh
python3 panel/reproduce-code/check.py claim/scheme.json --expect-additions 179 --artifacts panel/reproduce-code/candidate
python3 panel/reproduce-code/check.py panel/reproduce-code/sources/public181.json --expect-additions 181 --artifacts panel/reproduce-code/public181
python3 panel/reproduce-code/controls.py
```

No outward publication, submission, or write to a remote service was performed. Current global minima, novelty, priority, and any literature-access implications belong to their separate review roles.

pass: true
