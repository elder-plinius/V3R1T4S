# Independent REPRODUCE report — immutable final claim

context: freshsubagent; onlyclaimpackage; own frozen checker and evidence; no supplied checker, proof, outside report, or other-agent verdict inspected.

The final explicit integer factor product passes an independent rigorous proof and complete replay at the exact threshold **0.422640947**. No object, threshold, degree, certificate, or checker mismatch was found. This is a mathematical upper-bound verdict; it does not assert optimality or literature priority.

## Final object and frozen source

- Final object: `claim/object/candidate.json`
- Object SHA256: `b68801eed7ca3043a7b817aa6567d92b6d73519c3be888936589519de71055ce`
- Exact threshold: `422640947/1000000000 = 0.422640947`
- Exact saved copy: `panel/reproduce_strict_evidence/candidate_final.json`
- Frozen mathematical checker: `panel/reproduce_strict_evidence/independent_checker.py`
- Checker SHA256: `ac927e7aff6c6f9c63aafe7404c171ba31e03e33b3da38eb88535d95091073fa`
- Certificate: `panel/reproduce_strict_evidence/certificate_final.jsonl`
- Certificate SHA256: `dc69d2a670472315264e82abaffd631e1f37aba7384de2bc2a765f48e3910819`

The checker was independently written from the mathematical definition, passed analytic positive/negative controls, and was source-hash frozen before its first complete proof. Only `CLAIM.md`, `TARGET.md`, object data, and mathematical-library API docstrings were consulted. No reference code, supplied proofs, or external checker was read before or after freezing. This final rerun continued that isolated context and read only the final claim and this agent's own evidence.

The original frozen source already had an explicit `--threshold` argument parsed as an exact rational. It was used for the new threshold. There were **no source, algorithm, or precision changes**. Arithmetic remained Python-FLINT 0.9.0 Arb at 256-bit midpoint precision, with one thread. The final live object and saved copy were rehashed after proof and replay and matched the declared final hash. The source was rehashed again and matched its original frozen hash.

## Exact polynomial checks

The loader rejects duplicate JSON keys. Coefficients must be integers, explicitly excluding booleans and floats. Exponents must be strictly positive integers. Declared degrees must be strictly positive integers, coefficient-list length must equal degree plus one, and the leading coefficient must be nonzero. All metadata totals are independently recomputed and checked as integers.

The final object has 213 factors, maximum w-degree 48, and unweighted degree sum 4,293. Its weighted w-degree is 1,000,000,000,026. The exact total degree is

`D = 2 sum_j e_j deg(R_j) = 2,000,000,000,052`.

A nonzero degree-d integer polynomial R yields a nonzero degree-2d integer polynomial R(x(1−x)): its leading coefficient is the leading coefficient of R times (−1)^d. Thus the factor product has integer coefficients and exactly the stated degree. The map x↦x(1−x) maps [0,1] onto [0,1/4], so the two supremum problems coincide exactly.

## Independent proof method

Define `F(w)=sum_j e_j log|R_j(w)|`, with log zero equal to minus infinity. Arb ball arithmetic encloses every operation, including logarithms. Ball endpoints used for acceptance are rounded outward. Exact integer data and exact dyadic cells enter these calculations without conversion to floating-point input data.

First bisect [0,1/4] eight times. Within each block, translate each polynomial algebraically about the exact block midpoint using Arb polynomial composition. This merely changes basis, enclosing every resulting coefficient. Then bisect adaptively. A cell at depth d is exactly

`I=[k/(4·2^d),(k+1)/(4·2^d)]`,

with exact midpoint m and radius h. On every cell, the direct enclosure gives

`F(w) <= sum_j e_j log U_j`, where `U_j=upper(|R_j(I)|)`.

This remains valid on cells containing zeros. If every factor interval excludes zero, the checker also encloses

`F'(m)=sum_j e_j R'_j(m)/R_j(m)` and

`F''(I)=sum_j e_j [R''_j(I)/R_j(I)−(R'_j(I)/R_j(I))²]`.

With rigorous upper endpoints `s>=|F'(m)|` and `M>=sup_I F''`, Taylor's theorem gives

`F(m+t) <= upper(F(m))+s|t|+Mt²/2`.

The increment is at most `s h+max(M,0)h²/2`. When M<0, it is also at most `s²/(−2M)` by completing the square. The checker takes the smallest available rigorous upper bound. This local argument handles complex roots and does not assume real-rootedness or global concavity.

A cell is accepted only when its outward-rounded upper endpoint is strictly less than the outward-rounded lower endpoint of

`D log(422640947/1000000000)`.

Sampling does not establish acceptance. Point evaluations serve only as rigorous counterexample witnesses for rejected thresholds.

## Complete cover and independent replay

The full proof produced **10,576 accepted dyadic cells**, after examining 20,896 nodes. Cell depths range from 8 through 22. The methods used were 3,362 direct bounds, 6,660 ordinary Taylor bounds, and 554 completed-square Taylor bounds. Every certificate row records a cell, its bound, and the method.

A separate invocation of the frozen checker verified coverage independently of the generator's subdivision stack: it converted all cell endpoints to exact rationals, sorted them, required the first left endpoint to be zero, required every subsequent left endpoint to equal the previous right endpoint, and required the final right endpoint to be exactly 1/4. These checks exclude omissions, overlaps, duplicate cells, and cells outside the domain.

The replay then recomputed every bound from the final object and exact cell endpoints, without trusting the recorded bound. All 10,576 recomputations passed at the exact final threshold. The generated and replayed upper enclosures were identical. Separate negative partition controls removed a cell and duplicated a cell; both were rejected by the exact coverage check.

## Controls

Fresh reruns of all analytic and type controls passed before the final proof:

| Polynomial product in w | Exact normalized maximum | Passing threshold | Rejected threshold |
|---|---:|---:|---:|
| w | 1/2 | 0.501 | 0.499 |
| −16w²+4w | 1/√2 | 0.708 | 0.707 |
| 64w²−16w+5, with complex roots | 5^(1/4) | 1.5 | 1.49 |
| w³(4w−1)³ | 1/2 | 0.501 | 0.499 |

Each negative analytic case returned a rigorous point violation. Eight malformed objects were rejected: boolean, zero, and floating-point exponents; floating-point and boolean coefficients; zero leading coefficient; inconsistent factor degree; and inconsistent total degree. Final missing-cell and duplicate-cell controls also passed. The actual control outputs are preserved in `controls_final.log` and `final_audit.log`.

## Own commands and actual output

These commands were executed from `panel/reproduce_strict_evidence/`. The interpreter path below is the actual relative path used. All substantive runs used nice priority 10 and explicit hard timeouts. Each checker log begins with its PID, source hash, precision, and mode. The complete proof logged progress at 20 and 40 seconds; it finished within the 1,800-second limit.

```sh
cp ../../claim/object/candidate.json candidate_final.json
timeout 180s nice -n 10 ../../../../.venv/bin/python independent_checker.py controls > controls_final.log 2>&1
timeout 180s nice -n 10 ../../../../.venv/bin/python independent_checker.py pilot --object candidate_final.json --threshold 0.422640947 --nodes 1000 --certificate pilot_final_cells.jsonl > pilot_final.log 2>&1
sha256sum independent_checker.py controls_final.log pilot_final.log candidate_final.json > FINAL_INPUT_SHA256SUMS
timeout 1800s nice -n 10 ../../../../.venv/bin/python independent_checker.py prove --object candidate_final.json --threshold 0.422640947 --certificate certificate_final.jsonl > proof_final.log 2> proof_final.stderr
timeout 1800s nice -n 10 ../../../../.venv/bin/python independent_checker.py replay --object candidate_final.json --threshold 0.422640947 --certificate certificate_final.jsonl > replay_final.log 2> replay_final.stderr
timeout 180s nice -n 10 ../../../../.venv/bin/python final_audit.py > final_audit.log 2> final_audit.stderr
```

Elapsed times are measured with `time.monotonic()` and peak RSS with `resource.getrusage` inside the frozen checker.

| Run | Actual outcome | Wall time | Peak RSS |
|---|---|---:|---:|
| Analytic/type controls | controls_pass; 8 analytic cases and 8 malformed objects | 0.024442 s | 26,996 KiB |
| Measured final-object pilot | pilot_limit; 1,000 nodes, 554 accepted leaves | 2.379409 s | 29,288 KiB |
| Complete final proof | proved; 20,896 nodes, 10,576 accepted leaves | 53.095197 s | 31,460 KiB |
| Complete final replay | replay_pass; exact coverage [0,1/4], all 10,576 bounds recomputed | 22.464584 s | 36,988 KiB |

The peak memory was below 400 MB throughout. Proof, replay, and final audit exited successfully with no stderr output. The additional `final_audit.py` checks version binding and negative partition controls; it does not modify or replace the frozen mathematical proof algorithm. Its actual output includes `"status": "final_audit_pass"` and `"no_mismatch": true`.

Both the full proof and the separate replay returned the following rigorous enclosure for the largest normalized cell upper bound:

`[0.4226409469990940637731819968039768493909436688505013923141767957217964 +/- 3.31e-71]`.

Their corresponding normalized logarithmic upper enclosure is

`[-0.8612322854530852105229441226168924044126734685882872135671515261222407 +/- 3.42e-71]`.

The exact threshold's logarithm was enclosed as

`[-0.8612322854509416978480613121283110391404622433808820318959093733706588 +/- 1.69e-71]`.

The displayed normalized enclosure is an enclosure of a rigorous upper bound, not an assertion that the true maximum equals that number. Its upper endpoint is strictly below the exact rational 0.422640947, which is strictly below the comparator 0.422684697505. The complete-cover proof and replay therefore independently reproduce the final mathematical upper-bound claim for SHA256 `b68801eed7ca3043a7b817aa6567d92b6d73519c3be888936589519de71055ce`.

pass:true
