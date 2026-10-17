# REPRODUCE skeptic report

context: codex exec (gpt-6.1-sol, fresh session, workspace-write sandbox, no network)

Verdict: the saved straight-line program passes every property within the assigned offline scope. It computes 4x5x6 matrix multiplication over the integers with 90 explicit products and 348 reduced additions/subtractions. No mathematical mismatch or nondeterminism was found.

## Scope and independence

Evidence was restricted to this folder; no network was used. I read CLAIM.md, INDEX.csv, the object, and table-record/README.md first. I wrote skeptic/definition.md and skeptic/check.py, ran the independent checker successfully, and completed its determinism checks before opening verify-it-yourself/ or REPRODUCE.md. The independent checker uses Python's standard library and imports no author code.

The reference scheme is deliberately absent third-party data. table-record/README.md identifies its URL and SHA256, but a digest without the corresponding bytes cannot verify the reference, its addition count, or its product identity with this object. I did not recount that reference, verify hashes of unsaved fetched responses, determine the live minimum or best rank, compare live Lille or matmulcatalog records, or judge uniqueness/newness. Those comparisons and the identity with Perminov's reference belong to the other skeptics. The inequality 348 < 380 below compares saved numbers only. This pass applies to the saved object's exactness, ternarity, order, counts, hash, and determinism, as requested.

## Quoted definition and criterion

CLAIM.md. In quoted passages below, angle brackets delimiting matrix formats have been replaced by braces; only those brackets changed. The Lille URL template, with the same bracket substitution, is https://fmm.univ-lille.fr/{n}x{m}x{p}.html.

## Success criterion (entire paragraph, including clauses outside offline scope)

> Success means an explicit straight-line program (list of linear forms over the inputs, r products, and linear forms producing the outputs) for a format {n,m,p} with max(n,m,p) <= 8 and rank r equal to the best rank listed for that format in https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json (re-fetched live), that (1) is verified symbolically to compute the full product A*B exactly over Z, and (2) uses a number of additions/subtractions STRICTLY LESS (direction: min) than the smallest reduced addition count for that format and rank in Perminov's live repository (the addition_reduced_ZT scheme file for the format, reduced_known.json, README and CHANGELOG) re-fetched live immediately before claiming, counted under Perminov's 'reduced' convention (each binary +/- between already-computed quantities counts one; multiplication by -1 is free; multiplication by any other scalar is not allowed in a ternary SLP), AND below any lower count published for that format and rank on the live Lille per-format page's cited complexity variant and in matmulcatalog's live COVERAGE.md 'adds' column. If the Lille rank for the format is attained only with non-ternary coefficients, the comparison is against the best count in the same coefficient class as the candidate. The reference count is the MINIMUM cr value over all files for that format and rank in the live directory (formats have several files). Each scheme is claimed once: a scheme that also lowers the rank is a rank target, not this one.

## Object definition (entire object description)

> `object/`: the straight-line program in Perminov's reduced-scheme JSON layout: keys n, m, u_fresh, u, v_fresh, v, w_fresh, w. The inputs of the U map are the entries of A (row-major), of the V map the entries of B (row-major), of the W map the m products; fresh variable k of a map has index (number of inputs + k); every form is a list of index/value terms with value +1 or -1 and is a sum of already-computed quantities (inputs and earlier fresh variables); the u, v, w lists give the m product factors (u, v) and the outputs (w; output k*n+i is C[i][k], the transposed layout Perminov uses). The reduced addition count is the sum over all forms (fresh and final) of (number of terms - 1); negation is free.

## Properties and derivation

- **Schema and dimensions:** unique JSON keys, the expected map arrays and metadata, integer dimensions [4,5,6], maximum dimension 6, z2=false, 90 U factors, 90 V factors, and 24 outputs. All 90 products have nonzero factors and are used. This establishes a decomposition using 90 products; it does not prove minimal rank.
- **Straight-line order and permitted scalars:** every form is nonempty; every index and coefficient has exact integer type; every coefficient is +1 or -1. A fresh assignment can reference only its inputs and preceding fresh assignments. Final forms can reference only inputs and completed fresh assignments. Products take one U factor and one V factor; W is linear in these products. There are no other scalar or nonlinear operations.
- **Expansion and ternarity:** start with unit coordinate vectors for each map's inputs, and replace each referenced variable by its exact integer vector. Check all coordinates of all 448 fresh and final expanded forms, including all 796 listed left-to-right partial sums, lie in {-1,0,1}. For W, coordinates are the 90 independent products, as specified by the object layout. Checking partial sums additionally supplies a valid binary implementation of each multi-term form.
- **Exact full tensor identity:** let a=4, b=5, c=6, and s index the 90 products. The coefficient of A[x,y]*B[z,t] in output C[i,k] is sum_s W[k*a+i,s]*U[s,x*b+y]*V[s,z*c+t]. Ordinary multiplication requires that coefficient to equal 1 precisely when x=i, t=k, and y=z, and 0 otherwise. The checker forms every coefficient by exact integer additions and multiplications and compares all 24*20*30=14,400 coefficients, including zeros: 120 ones and 14,280 zeros match. Each output is bilinear by construction, so matching this full monomial basis proves equality over Z for every input, without probabilistic assumptions.
- **Direct execution:** independently execute the assignment lists on all 20*30=600 pairs of input unit vectors and compare all outputs to the matrix product. This exhausts the bilinear basis rather than sampling it. Six fixed dense signed-integer cases supplement that complete check. No exhaustive-search claim is being accepted from a sample.
- **Reduced addition count:** a form with L terms is implemented by L-1 binary additions/subtractions; signed inputs and unary negation are free. Count every fresh and final form: U=81+0=81, V=104+0=104, W=107+56=163. Total 81+104+163=348, excluding the 90 products. This agrees with the filename, CLAIM.md, complexity.reduced, and INDEX.csv. Expanded naive support counts independently give 1023, agreeing with complexity.naive. The saved comparison is 348 < 380, by 32.
- **Object and hash:** exactly the indexed object file is present in object/, its bytes are readable, and its SHA256 matches INDEX.csv. It remains unchanged through independent and author checks. Remote response hashes listed in table-record/README.md cannot be verified without those responses.
- **Determinism:** three fresh independent processes with distinct PYTHONHASHSEED values reproduce the entire original output byte for byte and leave object and checker bytes unchanged. Two fresh author-checker processes also agree byte for byte. Both checkers use exact integer arithmetic for the tensor proof; the author's seeded random evaluations are supplementary.

## Exact independent commands and real output

Commands were run from this folder, in this order, before reading author code:

```sh
python3 skeptic/check.py > skeptic/output.txt 2>&1
cat skeptic/output.txt
python3 skeptic/check_determinism.py > skeptic/determinism.txt 2>&1
cat skeptic/determinism.txt
```

Both commands exited 0. The following blocks are inserted directly from the saved output files.

skeptic/output.txt:

```text
Independent verifier: exact integer arithmetic; no network; no author code
Object: object/4x5x6_m90_cr348_ZT_reduced.json (26496 bytes)
SHA256: aee2afd0dd35ce54d64786b5439fc37101e55a8a758cfd2a8e572e4431396c8c; matches INDEX.csv
Format: 4x5x6; max dimension=6 <= 8; products=90; integer arithmetic
U: inputs=20 fresh=81 finals=90 additions_fresh=81 additions_final=0 total=81
U: all 171 expanded forms and 252 listed partial sums ternary; all references precede use
V: inputs=30 fresh=104 finals=90 additions_fresh=104 additions_final=0 total=104
V: all 194 expanded forms and 298 listed partial sums ternary; all references precede use
W: inputs=90 fresh=59 finals=24 additions_fresh=107 additions_final=56 total=163
W: all 83 expanded forms and 246 listed partial sums ternary; all references precede use
Products: exactly 90 nonzero U-factor times V-factor multiplications; every product used
Reduced additions: 81+104+163=348; matches object metadata, filename, CLAIM.md and INDEX.csv
Expanded naive additions: 1023; matches object metadata
Saved-number comparison: 348 < 380; difference=32 (reference not independently recounted)
Tensor identity: all 14400 integer coefficients checked; 120 ones and 14280 zeros match A*B exactly
Tensor SHA256 (canonical compact JSON): fad8487842ebc1fab1172b80d9410e8115d0c7a35d79928b4b9c5d100b904003
Expanded U,V,W SHA256 (canonical compact JSON): 5b9c676fb88632cb007ad787afd415fda81eae741938b20d1ef480274ae7c6ef
Direct SLP execution: all 600 input basis pairs plus 6 fixed dense signed-integer cases match every output
Execution SHA256 (canonical compact JSON): 86f41e36517ddadaf2029e0e22c614b40b8113f5d7716062e6258ec6a625952b
Object bytes unchanged during verification
OFFLINE SCOPE: no best-rank/live-table check, reference recount/product-identity check, external response-hash verification, or novelty judgment
PASS: all saved-object properties checked
```

skeptic/determinism.txt:

```text
PYTHONHASHSEED=0: exit=0; stdout byte-identical; stderr empty; object/checker unchanged
PYTHONHASHSEED=1: exit=0; stdout byte-identical; stderr empty; object/checker unchanged
PYTHONHASHSEED=8675309: exit=0; stdout byte-identical; stderr empty; object/checker unchanged
Output SHA256: b34888c58432973875e7a653bcaf19a6c7f7c7dee7f06fbc04153c15bc5ba968
PASS: three fresh processes reproduce the full initial output
```

## Author comparison and real output

After the independent checks passed, I read the author files and ran:

```sh
sh verify-it-yourself/run_checks.sh > skeptic/author_output.txt 2>&1
author_check_exit=$?
cat skeptic/author_output.txt
exit "$author_check_exit"
```

This completed with exit 0. An earlier shell capture attempt used zsh's read-only variable status and emitted `zsh:2: read-only variable: status` after the wrapper had run; the command above reran the wrapper and correctly captured its successful exit.

skeptic/author_output.txt:

```text
sha256 matches INDEX.csv (aee2afd0dd35ce54d64786b5439fc37101e55a8a758cfd2a8e572e4431396c8c)
== check_slp.py on object/4x5x6_m90_cr348_ZT_reduced.json (exact tensor identity, ternary coefficients, reduced addition count)
{"file": "4x5x6_m90_cr348_ZT_reduced.json", "format": "4x5x6", "rank": 90, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 81, "adds_V": 104, "adds_W": 163, "adds_total": 348, "naive_total": 1023, "declared_reduced": 348, "VALID": true}
checker verdict: PASS (VALID=True, adds_total=348, tensor=C^T)
== negative control: a copy with one coefficient sign flipped in the first fresh U form must FAIL
negative control rejected as expected (VALID false)
ALL CHECKS PASS
```

I also ran the comparison harness, which invokes the author checker twice, parses its JSON, compares each result with independently derived values, and checks object immutability:

```sh
python3 skeptic/compare_author.py > skeptic/author_comparison.txt 2>&1
cat skeptic/author_comparison.txt
```

This completed with exit 0. skeptic/author_comparison.txt:

```text
Author command: python3 verify-it-yourself/check_slp.py object/4x5x6_m90_cr348_ZT_reduced.json
{"file": "4x5x6_m90_cr348_ZT_reduced.json", "format": "4x5x6", "rank": 90, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 81, "adds_V": 104, "adds_W": 163, "adds_total": 348, "naive_total": 1023, "declared_reduced": 348, "VALID": true}
Comparison: format, products, transposed output layout, exact tensor, evaluation, all map counts, naive count, declared count and VALID agree
Determinism: two author-checker processes returned byte-identical stdout, exit=0, empty stderr; object unchanged
Limitation: author check_slp.py does not test expanded intermediate ternarity; independent checker checks every form and binary partial sum
PASS: no result disagreement
```

The author agrees on the tensor identity, transposed output layout, 90 products, 348 reduced additions, map subtotals, and 1023 naive additions. Its negative control rejects a sign-flipped object. Its claimed expanded-intermediate ternary test is absent from check_slp.py: expand computes vectors but never checks their coefficients against {-1,0,1}. This is a limitation of that checker, not a mismatch in the saved object; the independent checker exhaustively verifies the missing property, including binary partial sums. No result disagreement remains. The optional author sympy cross-check was not needed or run; the independent full integer tensor proof establishes exactness.

pass: true
