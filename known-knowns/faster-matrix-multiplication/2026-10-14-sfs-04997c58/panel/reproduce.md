context: subagent (fork_turns none; isolated capsule)

PROVED-HERE: The immutable `claim/scheme.json` is a ternary integer rank-58 decomposition for ordered format (3,5,5), implemented by an explicit straight-line program with 214 binary additions/subtractions: U=50, V=70, W=94.

I saw only the isolated claim capsule and the allowed repository instructions (AGENTS.md, kit/RULES.md, RUN.md steps 6–7), plus the fresh public definitions and calibration circuit recorded below. I did not read sibling panel files, other runs, attempts, prior findings, charters, verdicts, or reasoning. I wrote and ran my independent checker before opening `claim/verify.py`. This is a reproduction verdict for the immutable object; the novelty comparison and full binding success criterion belong to the other panel roles and the main honesty gate.

Definition checked: “C[i,j] = sum_k A[i,k] B[k,j] over Z.” A[i,k] has coordinate i*5+k, B[k,j] has coordinate k*5+j, and C[i,j] has coordinate j*3+i. This ordinary definition was independently fixed by fresh public `Scheme.naive` lines 35–49: its one-product entries are U[i*5+k]=1, V[k*5+j]=1, W[j*3+i]=1. The fresh README reduced schema and `Scheme.from_reduced` confirmed consecutive fresh indices starting at 15, 25, and 58 respectively, and the transpose from output-form W rows to product-factor W columns. No coordinate permutation was fitted to the candidate.

The checker uses Python arbitrary-precision integer arithmetic, imports no author or public implementation, and does not reduce modulo a field. It expands each linear form recursively in append order, constructs every rank-one contribution, and compares every tensor coefficient, including every expected zero, against the ordinary coordinate definition. Separately, it executes the literal circuit on every input basis pair and computes the expected output by the defining matrix-product sum.

Actual primary result, retained in `panel/reproduce-code/commands.jsonl`:

```text
argv: python3 independent_check.py ../../claim/scheme.json
returncode: 0
dimensions: [3, 5, 5]
rank: 58
active_distinct_products: 58
reduced_cost: 214
naive_cost: 357
tensor_coefficients_checked: 5625
tensor_failures: 0
basis_pairs_checked: 375
basis_failures: 0
exact_integer_identity: true
literal_scalars: [-1, 1]
expanded_factor_scalars: [-1, 0, 1]
sha256: 04997c5844e0968c43b347b7e911059ac1464c5da653b29bd3838a489723df7c
```

The symbolic equality of all coefficients proves the bilinear polynomial identity over Z for every input, rather than merely testing selected numeric inputs. All 58 U, V, and W factors are nonzero. Every product is used, and all 58 U/V pairs are distinct even after canonicalizing their independent free signs. Both metadata costs agree with independent literal and expanded-factor counts. The expanded candidate U, V, and W arrays equal those of the independently fetched public 221 circuit exactly; this is an independently verified re-expression of that decomposition.

The circuit audit counts every written gate, including any possible unused gate before rejecting dead gates. There are 214 fresh rows, all binary, and 131 final rows, all unit aliases. Their stage costs are U=50, V=70, W=94. There are no forward references, duplicate references within a row, dead fresh gates, fresh aliases, zero factors, extra operational fields, noninteger literals, or nonunit literal scalars. `research_method` is an inert string and is not interpreted as an operation or executed. No product or additional arithmetic is inferred from metadata.

The maximum absolute expanded intermediate coefficients are U=1, V=1, W=2. Specifically, W variable 136 is the literal gate W100+W135 and has coefficient 2 on product 0 in its expansion. This is one charged binary addition between previously computed quantities, with unit literal signs. It is not a free scalar multiplication by 2. All final expanded U/V/W factors have coefficients in {-1,0,1}. A separate exact toy control accepts (x+x)-x, charges both binary operations, and verifies coefficient-2 intermediates; another control rejects a literal free scalar 2.

Before-author evidence: `panel/reproduce-code/independent_check.py.before-author.json` records UTC 2026-10-14T14:07:10.934905+00:00 and SHA256 444e8e1fb2ecbf2749a1efb6286f11327361c11ab6a6ba45d559d666d4caa980 with `author_verifier_read: false`. The first independent candidate run began at 2026-10-14T14:07:29.640859+00:00. The author verifier was first opened by the logged command at 2026-10-14T14:09:09.811046+00:00; its subsequent run returned:

```json
{"valid": true, "format": [3, 5, 5], "rank": 58, "addition_counts": {"u": 50, "v": 70, "w": 94}, "additions": 214, "identities_verified": 5625}
```

The independent checker’s current SHA256 remains the same. Two subsequent independent executions returned code 0, empty stderr, and identical stdout with SHA256 a3fffe36c007318de39386d5f46b0bc41f82e3050ed67c0aaf2dd1876ea04925. The candidate hash remained unchanged. The author verifier agrees on this object, but the independent checker additionally audits expanded ternarity, product activity/distinctness, dead gates, and metadata.

All 15 controls succeeded, with saved mutated objects and full results in `panel/reproduce-code/controls/` and `controls-result.json`:

- Accepted equivalent term reordering, an internal gate sign with all references compensated, a product sign with W references compensated, and a free fresh alias without changing the charged cost.
- Rejected a sign-corrupted U output: 20 integer tensor coefficient failures and 2 basis-pair failures, while all 5625 mod-2 coefficients still pass. Its first witness is A-coordinate 6, B-coordinate 6, C-coordinate 0, expected 0, actual -2.
- Rejected cost metadata reduced by one, a literal scalar 2, a forward reference, a dead gate whose cost metadata was also updated, an extra hidden-operation field, a Boolean literal, an output-coordinate swap, duplicate active products, and a duplicate JSON key.
- Accepted the charged coefficient-2 toy circuit described above.

Fresh public calibration: the live public source circuit passes the same full 5625-coefficient/375-basis-pair checks with 58 active distinct products, expanded ternary factors, naive count 357, and independently counted cost 221 (U=53,V=72,W=96). Credit: Andrew I. Perminov’s FastMatrixMultiplication repository supplied the public scheme schema, ordinary coordinate convention, and comparison object. I inspected source text but did not execute its code.

Each URL below received one ordinary GET with User-Agent `V3R1T4S independent reproduction checker`; all returned HTTP 200. There were no real-denial retries, mirrors, browser impersonation, or access-control bypasses. Source bodies and per-source fetch records are retained in `panel/reproduce-code/`; `fetch.py` is the actual retrieval command implementation, and `source_records.py` logs the saved retrieval outputs.

| Source URL | GET UTC | HTTP | SHA256 |
| --- | --- | --- | --- |
| https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/src/schemes/scheme.py | 2026-10-14T14:04:50.746879+00:00 | 200 | 3684c5f6d762fff39db1ebee60ab6465469d627443c875d7fa1a9f6be35337fe |
| https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/README.md | 2026-10-14T14:04:51.165830+00:00 | 200 | 7b0761ecc0fa1988cb2ef0efeca503af974eeb6ade76d30629308ebba7e78341 |
| https://raw.githubusercontent.com/dronperminov/FastMatrixMultiplication/master/schemes/results/addition_reduced_ZT/3x5x5_m58_cr221_cn357_ZT_reduced.json | 2026-10-14T14:04:51.335448+00:00 | 200 | 17cdcab30fdacdaf92464bbfd7ff135a1d39fada357114d400586e8cad1dcd9e |

KNOWN from the isolated capsule’s `LITERATURE_ACCESS.md`: the optional IACR PDF https://eprint.iacr.org/2024/2063.pdf returned HTTP 403 at 2026-10-14T12:01:02Z; the optional SIAM PDF https://epubs.siam.org/doi/pdf/10.1137/1.9781611979084.24?download=true returned HTTP 403 with a challenge at 2026-10-14T13:18:23.764660+00:00, response SHA256 52c588c2e38265841bea3da3665a256aa7b70ca1ec48dd4339a2e2c06502a9c4. I did not request either denied URL, seek another copy, or assert either PDF’s contents. These remain explicitly recorded literature-access gaps for the comparison roles; they do not affect exact verification of the saved circuit.

Reproduction commands from the run folder (no network needed after the saved source retrieval):

```sh
python3 panel/reproduce-code/independent_check.py claim/scheme.json
python3 panel/reproduce-code/independent_check.py panel/reproduce-code/public-221.json
python3 panel/reproduce-code/controls.py
python3 panel/reproduce-code/details.py
python3 claim/verify.py claim/scheme.json
```

Limit: no exact replay of the whole discovery history is claimed or confirmed. The capsule itself states that the original complete dictionaries and runtime code hashes were not saved. Exact, deterministic verification of the immutable circuit is complete; the search-provenance statement is kept at its explicit limited scope. I did not edit the object or criterion, publish anything, or take outward action.

Attribution metadata repair: an earlier version of this report incorrectly gave Perminov’s first name as Dmitry. I checked my retained primary README’s “License and Citation” BibTeX entries, which identify the author as `Perminov, Andrew I`, and corrected the credit to Andrew I. Perminov. The saved primary text is logged in `panel/reproduce-code/commands.jsonl`. This correction changes attribution only; the mathematical findings, object, and checking code are unchanged.

pass: true
