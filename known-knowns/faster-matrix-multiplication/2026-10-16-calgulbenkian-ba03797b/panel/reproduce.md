The saved object passes the offline REPRODUCE checks: exact integer matrix multiplication with 45 products and 169 reduced additions. This verdict applies to the saved object and the scope assigned to this skeptic.

context: codex exec (gpt-6.1-sol, fresh session, workspace-write sandbox, no network)

I read CLAIM.md, the object, INDEX.csv, and table-record/README.md; wrote skeptic/definition.txt and my independent standard-library checker skeptic/check.py; ran it and saved skeptic/output.txt; only then opened REPRODUCE.md and verify-it-yourself/. I did not inspect any external package or use the network. The explicitly authorized preinstalled interpreter was used solely to run the author's optional SymPy cross-check.

The success criterion from CLAIM.md is quoted below. Only angle brackets have been changed to braces to satisfy the package formatting rule. The Lille URL template is https://fmm.univ-lille.fr/{n}x{m}x{p}.html; only its template brackets have been changed.

> Success means an explicit straight-line program (list of linear forms over the inputs, r products, and linear forms producing the outputs) for a format {n,m,p} with max(n,m,p) <= 8 and rank r equal to the best rank listed for that format in https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json (re-fetched live), that (1) is verified symbolically to compute the full product A*B exactly over Z, and (2) uses a number of additions/subtractions STRICTLY LESS (direction: min) than the smallest reduced addition count for that format and rank in Perminov's live repository (the addition_reduced_ZT scheme file for the format, reduced_known.json, README and CHANGELOG) re-fetched live immediately before claiming, counted under Perminov's 'reduced' convention (each binary +/- between already-computed quantities counts one; multiplication by -1 is free; multiplication by any other scalar is not allowed in a ternary SLP), AND below any lower count published for that format and rank on the live Lille per-format page's cited complexity variant and in matmulcatalog's live COVERAGE.md 'adds' column. If the Lille rank for the format is attained only with non-ternary coefficients, the comparison is against the best count in the same coefficient class as the candidate. The reference count is the MINIMUM cr value over all files for that format and rank in the live directory (formats have several files). Each scheme is claimed once: a scheme that also lowers the rank is a rank target, not this one.

The saved-object definition and counting convention from CLAIM.md are:

> the straight-line program in Perminov's reduced-scheme JSON layout: keys n, m, u_fresh, u, v_fresh, v, w_fresh, w. The inputs of the U map are the entries of A (row-major), of the V map the entries of B (row-major), of the W map the m products; fresh variable k of a map has index (number of inputs + k); every form is a list of index/value terms with value +1 or -1 and is a sum of already-computed quantities (inputs and earlier fresh variables); the u, v, w lists give the m product factors (u, v) and the outputs (w; output k*n+i is C[i][k], the transposed layout Perminov uses). The reduced addition count is the sum over all forms (fresh and final) of (number of terms - 1); negation is free.

The following properties were checked independently from the saved files:

| Property | Complete check |
|---|---|
| Format and product count | Strict JSON schema and integer types; dimensions exactly 2,4,7, maximum 7; exactly 45 U factors, 45 V factors, 14 outputs; z2 is false. All products have nonzero factors and contribute. This establishes 45 product terms, not minimality of tensor rank. |
| Straight-line order | Every reference is a nonnegative integer addressing an input or an earlier fresh variable in its map. Fresh variables become available only after their assignment. Final forms cannot reference other final forms. All forms are nonempty and all references within each form are distinct. |
| Ternary condition | Every literal scalar is exactly +1 or -1. Every one of the 208 fresh/final forms is expanded as an integer vector in its map's input basis (A entries, B entries, or formal products). All 377 ordered prefixes, including implicit binary intermediates inside multi-term forms, have coefficients in {-1,0,1}. No expanded form is zero. |
| Symbolic exactness | All 3,136 coefficients of A[a] B[b] in every output are computed and compared with the specified matrix multiplication tensor, including every required zero. Exactly 56 coefficients are nonzero and all are 1. The required output order is k*2+i, not row-major output order. |
| Direct execution | A separate scalar SLP interpreter evaluates all 8 times 28 = 224 input basis pairs, checking all 14 outputs in each case. This is exhaustive for a bilinear map, not a random sample. |
| Reduced count | Each form with L terms contributes L-1, with free negation and 45 products excluded. U contributes 15+20=35, V 67+0=67, W 26+41=67; total 169. Every fresh form is used. Independently, total terms minus total forms is 377-208=169. |
| Other saved numerical metadata | Expanded-factor naive count is 308. Object complexity fields and INDEX.csv agree. Saved reference metadata says 174, and 169 is smaller by 5; this is an arithmetic comparison with metadata, not a reference recount. |
| Hashes and stability | Object SHA-256 equals INDEX.csv. SHA-256 values of CLAIM.md, INDEX.csv, and table-record/README.md are recorded as fingerprints, without pretending they have external attestations. All four saved inputs remain byte-for-byte unchanged after the author checks. |
| Determinism | Three independent-checker processes produce byte-identical complete output, one with PYTHONHASHSEED=37. Each author cross-check also produces identical output on two runs. A digest covers the entire expanded forms, all prefixes, tensor, and counts. |

The algebraic proof was re-derived as follows. Give A and B their row-major unit-vector bases. Induction over the causal fresh assignments proves that adding the signed source vectors gives the exact integer linear form of each assignment. Write the resulting factor coefficients as U[t,a], V[t,b], and the output coefficients over formal products as W[c,t]. Substitution gives output coefficient T[c,a,b] = sum over t of W[c,t] U[t,a] V[t,b]. For c=k*2+i, this coefficient must equal 1 exactly when a=i*4+j and b=j*7+k for the same j, and 0 otherwise. My checker compares this equality for every c,a,b. Since all computed outputs are homogeneous bilinear polynomials, there are no other monomials to check. Equality of every coefficient over Z proves equality for all integer inputs. Direct execution on every input basis pair independently confirms the same complete coefficient family. The count follows by lowering each L-term ordered sum to L-1 binary additions/subtractions; signs are free, and the prefix checks establish that this lowering also preserves ternarity.

These are the exact successful commands, run from this folder. Every command exited 0:

```sh
python3 skeptic/check.py > skeptic/output.txt 2>&1
python3 skeptic/check.py > skeptic/output-repeat.txt 2>&1
sh verify-it-yourself/run_checks.sh > skeptic/author-output.txt 2>&1
../../../.venv/bin/python verify-it-yourself/sym_check.py object/2x4x7_m45_cr169_ZT_reduced.json > skeptic/author-symbolic-venv-output.txt 2>&1
sh verify-it-yourself/run_checks.sh > skeptic/author-output-repeat.txt 2>&1
PYTHONHASHSEED=37 python3 skeptic/check.py > skeptic/output-hashseed.txt 2>&1
../../../.venv/bin/python verify-it-yourself/sym_check.py object/2x4x7_m45_cr169_ZT_reduced.json > skeptic/author-symbolic-repeat.txt 2>&1
python3 skeptic/verify_runs.py > skeptic/verification.txt
```

The provided optional interpreter is addressed relatively in these commands. An earlier attempt with system python3 to run sym_check.py exited 1 because SymPy was absent (ModuleNotFoundError: No module named 'sympy'); its diagnostic is retained in skeptic/author-symbolic-output.txt. Re-running with the user-specified interpreter succeeded. This dependency failure is not a mathematical disagreement.

Full independent output, inserted directly from skeptic/output.txt:

```text
Independent exact integer SLP check
sha256 CLAIM.md: 921d763916466e051e2a447f4d2ebee88ad3cc0cdb80b5d1eaa69c295ab5472b
sha256 object/2x4x7_m45_cr169_ZT_reduced.json: ba03797bb02013423a43e98b27ac46c6897018e12f9e90f0761e874c402070d7
sha256 INDEX.csv: b959ed427dbdf4336c21d74e7fe52543fcb74eeb8f104f1ac5f2deee858154b1
sha256 table-record/README.md: 8edc05f2d66127f73b68c7ae81b7aca1732e6326a9507171663904d66a27f988
Schema/index/hash: OK; format=2x4x7, max dimension=7 <= 8; products=45; ring=Z
U: inputs=8, fresh=15, final=45, additions=fresh 15 + final 20 = 35, ternary prefixes=95; order/scalars/expanded forms OK
V: inputs=28, fresh=67, final=45, additions=fresh 67 + final 0 = 67, ternary prefixes=179; order/scalars/expanded forms OK
W: inputs=45, fresh=22, final=14, additions=fresh 26 + final 41 = 67, ternary prefixes=103; order/scalars/expanded forms OK
Full tensor: 3136 coefficients checked; nonzeros=56; mismatches=0
Direct SLP execution: all 224 input basis pairs, 3136 output checks; mismatches=0
Liveness: every fresh form and all 45 nonzero products contribute to outputs
Reduced additions=169; expanded naive additions=308; products=45 (excluded)
Saved numerical comparison: 169 < 174; improvement=5 (external baseline not recounted)
Complete expansion/tensor certificate sha256: 4636b4ce00003166b797b77183c8582d48b902affcfba20a951cd4fc96c76639
Input stability: all four checked saved files unchanged
PASS: all offline saved-object checks
```

Full author run output, inserted directly from skeptic/author-output.txt:

```text
sha256 matches INDEX.csv (ba03797bb02013423a43e98b27ac46c6897018e12f9e90f0761e874c402070d7)
== check_slp.py on object/2x4x7_m45_cr169_ZT_reduced.json (exact tensor identity, ternary coefficients, reduced addition count)
{"file": "2x4x7_m45_cr169_ZT_reduced.json", "format": "2x4x7", "rank": 45, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 35, "adds_V": 67, "adds_W": 67, "adds_total": 169, "naive_total": 308, "declared_reduced": 169, "VALID": true}
checker verdict: PASS (VALID=True, adds_total=169, tensor=C^T)
== negative control: a copy with one coefficient sign flipped in the first fresh U form must FAIL
negative control rejected as expected (VALID false)
ALL CHECKS PASS
```

Full successful author SymPy output, inserted directly from skeptic/author-symbolic-venv-output.txt:

```text
{"file": "2x4x7_m45_cr169_ZT_reduced.json", "format": "2x4x7", "rank": 45, "products": 45, "symbolic": {"C^T": true, "C=AB": false}, "reduced_additions": 169}
```

Repeat and stability verification output, inserted directly from skeptic/verification.txt:

```text
byte-identical independent output: skeptic/output-repeat.txt
byte-identical independent output: skeptic/output-hashseed.txt
byte-identical author output: skeptic/author-output.txt and skeptic/author-output-repeat.txt
byte-identical author output: skeptic/author-symbolic-venv-output.txt and skeptic/author-symbolic-repeat.txt
unchanged after author checks: CLAIM.md
unchanged after author checks: object/2x4x7_m45_cr169_ZT_reduced.json
unchanged after author checks: INDEX.csv
unchanged after author checks: table-record/README.md
sha256 skeptic/definition.txt: a29f8e19c9255e2e74f4219fa9e8171217ea43e2b0c92a8ce34aaf42b729b2c1
sha256 skeptic/check.py: bcf3cf3a13a02beabb1563b6c6d943fe2b08d4ef267d078f5703dbf68775977f
Verification: PASS
```

There is no disagreement on this object's exactness, output layout, product count, naive count, or reduced count. The author's checker has a verification gap: check_slp.py checks literal term signs but does not test ternarity of expanded coefficients, despite the broader description in REPRODUCE.md. sym_check.py also checks literal signs rather than expanded intermediate ternarity. My checker independently verifies the stronger expanded condition, including all binary prefixes, and it passes for this object. The author's C=AB false result in its alternative layout test is expected: the documented saved layout is C^T.

Offline scope: table-record/README.md deliberately supplies only metadata, including the external reference URL and its claimed SHA-256. Perminov's reference file is not shipped, so I cannot authenticate its hash, recount its 174 additions, or compare its individual U,V,W factors with this object's. The external source bodies behind the other table hashes are also absent; those hashes cannot be authenticated here. As directed, these disclosed third-party absences are outside this saved-object verdict. Live rank optimality, the minimum over all live reference files, same-coefficient-class comparisons, Lille and matmulcatalog counts, freshness of source fetches, and product identity with the reference belong to the other skeptics. I make no judgment about table currency, novelty, or prior duplicate claims. No exhaustive-search claim is being certified; the exact verification of the provided object is exhaustive.

No saved-object mismatch or non-determinism was found. All assigned properties that can be verified from these saved files have been confirmed.

pass: true
