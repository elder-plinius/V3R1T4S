# REPRODUCE skeptic report

context: codex exec (gpt-6.1-sol, fresh session, workspace-write sandbox, no network)

Verdict: the saved straight-line program passes the independent checks below. This verdict concerns the saved object, as instructed; it does not establish a current record, novelty, optimal rank, or identity with an absent reference scheme.

## Definition and success criterion

Source: `CLAIM.md`. For the quoted format notation I changed only the brackets, from angle brackets to braces, to avoid the package checker's placeholder rejection. The same brackets-only rendering of the Lille URL template is https://fmm.univ-lille.fr/{n}x{m}x{p}.html; the supplied criterion refers to the Lille page in words rather than spelling out that template.

> Success means an explicit straight-line program (list of linear forms over the inputs, r products, and linear forms producing the outputs) for a format {n,m,p} with max(n,m,p) {= 8 and rank r equal to the best rank listed for that format in https://raw.githubusercontent.com/sedoglavic/fmm_digest/master/fmm_sota.json (re-fetched live), that (1) is verified symbolically to compute the full product A*B exactly over Z, and (2) uses a number of additions/subtractions STRICTLY LESS (direction: min) than the smallest reduced addition count for that format and rank in Perminov's live repository (the addition_reduced_ZT scheme file for the format, reduced_known.json, README and CHANGELOG) re-fetched live immediately before claiming, counted under Perminov's 'reduced' convention (each binary +/- between already-computed quantities counts one; multiplication by -1 is free; multiplication by any other scalar is not allowed in a ternary SLP), AND below any lower count published for that format and rank on the live Lille per-format page's cited complexity variant and in matmulcatalog's live COVERAGE.md 'adds' column. If the Lille rank for the format is attained only with non-ternary coefficients, the comparison is against the best count in the same coefficient class as the candidate. The reference count is the MINIMUM cr value over all files for that format and rank in the live directory (formats have several files). Each scheme is claimed once: a scheme that also lowers the rank is a rank target, not this one.

The saved-object layout and counting definition are:

> - `object/`: the straight-line program in Perminov's reduced-scheme JSON layout: keys n, m, u_fresh, u, v_fresh, v, w_fresh, w. The inputs of the U map are the entries of A (row-major), of the V map the entries of B (row-major), of the W map the m products; fresh variable k of a map has index (number of inputs + k); every form is a list of index/value terms with value +1 or -1 and is a sum of already-computed quantities (inputs and earlier fresh variables); the u, v, w lists give the m product factors (u, v) and the outputs (w; output k*n+i is C[i][k], the transposed layout Perminov uses). The reduced addition count is the sum over all forms (fresh and final) of (number of terms - 1); negation is free.

In particular, the two operative requirements are:

> is verified symbolically to compute the full product A*B exactly over Z

> each binary +/- between already-computed quantities counts one; multiplication by -1 is free; multiplication by any other scalar is not allowed in a ternary SLP

## Scope and independence

I read `CLAIM.md`, `INDEX.csv`, `table-record/README.md`, and the object before inspecting any author code. I saved the verbatim definition excerpts in `skeptic/definition.md`, then wrote `skeptic/check.py` using only Python's standard library. I ran it successfully and saved its full output in `skeptic/output.txt` before reading `REPRODUCE.md` or anything in `verify-it-yourself/`. The independent checker imports no author code and uses no random trials.

The reference scheme is explicitly third-party data that is not shipped. `table-record/README.md` names its URL and recorded SHA256, but neither can establish its contents offline. I cannot recount the reference's claimed 383 additions, validate its recorded hash, or compare its expanded products with this object's. The source pages behind the other recorded table hashes are also absent; their hashes and extracted claims cannot be authenticated here. These intentional omissions do not fail this saved-object verdict under the assigned scope.

The live best-rank condition, live minimum over reference files, README/CHANGELOG comparisons, Lille and COVERAGE comparisons, coefficient-class comparison, and once-only/rank-target classification belong to the other skeptics. I made no network requests and did not inspect files outside this folder. No exhaustive search is claimed or certified here; the algebraic verification exhausts every tensor coefficient rather than sampling matrices.

## Properties checked and proof reconstruction

| Property | Independent check and result |
|---|---|
| Object and metadata | Required the exact JSON schema; rejected duplicate keys; required integer dimensions `[5,5,5]`, product count 93, and `z2: false`. Checked the target, cell, relative object path, counts, and SHA256 against the sole `INDEX.csv` row. The filename agrees with format, product count, and 332 additions. |
| Dimension bound and products | Each dimension is 5, hence at most 8. U and V have exactly 93 factor forms and W has exactly 25 outputs. Every product has nonzero U and V factors and occurs in some expanded output. This verifies a 93-term scheme, without proving the format's minimum tensor rank. |
| Straight-line order | For every term, required an integer, nonnegative index into the inputs or already-expanded fresh variables of its own map. Final forms may refer only to inputs and completed fresh forms. Required nonempty forms and distinct dependency indices. |
| Allowed scalars | Every stored coefficient is the integer +1 or -1; there are no other scalar multiplications. The 93 U-by-V bilinear products are excluded from the addition count. |
| Expanded ternarity | Expanded inputs as standard basis vectors over Z; expanded every fresh and final form by signed vector addition in dependency order. All 230 fresh forms and 211 final forms have only coefficients -1, 0, or 1. Also checked every prefix in the binary left-fold lowering of each multi-term form, including all 332 charged binary operations. All are ternary. |
| Exactness over Z and layout | Constructed each coefficient of the bilinear output tensor by summing W[out,t] times U[t,a] times V[t,b] for all 93 products. Compared all 25 times 25 times 25 = 15,625 integer coefficients with the defining matrix-product tensor, using output index k*5+i for C[i,k]. All 125 required ones and 15,500 required zeros match. |
| Reduced addition count | Independently summed length minus one over every fresh and final form. U: 87; V: 88; W: 157; total 332. Single-term copies and signs cost zero. The final factors and output forms are included. Metadata, filename, and INDEX agree. |
| Expanded naive count | Independently counted nonzero coefficients in the expanded U, V, W rows and subtracted 2*93+25. The result is 843, matching object metadata and the author's checker. |
| Recorded comparison | The saved numbers satisfy 332 less than 383, an improvement of 51. This is arithmetic against recorded metadata, not verification that 383 is the actual reference or live minimum. |
| Hash and determinism | Object SHA256 matches INDEX. Two complete independent parses, expansions, and tensor reconstructions within the checker agree; a separate process rerun produces byte-identical full output. Two direct author-checker processes also produce byte-identical full output. |

The proof is inductive. Each input vector represents its corresponding input coordinate. Since each fresh form uses only already-established vectors, signed vector addition derives its exact linear polynomial over Z; the same argument derives the final U and V factors and W weights. Multiplying each derived U factor by its V factor, then distributing the W map, gives coefficient sum_t W[out,t] U[t,a] V[t,b] for monomial A[a]B[b]. The expected coefficient is one exactly when the row of A equals the output row, the column of B equals the output column, and A's column equals B's row; it is zero otherwise. Exhaustive agreement therefore proves the polynomial identity for every integer input matrix. This simultaneously justifies the stated transposed output indexing. Each length-L form has a permitted binary left-fold evaluation with L-1 additions, and the checked prefixes show that this lowering also preserves expanded ternarity. Thus the reconstructed computation realizes the counted total without hidden scalar operations.

## Exact commands and real output

All commands were run from this folder. The independent run used:

```sh
python3 skeptic/check.py > skeptic/output.txt 2>&1
```

Exit status: 0. Complete captured output, inserted directly from `skeptic/output.txt`:

```text
Independent saved-object verification (Python standard library, exact integers)
object: object/5x5x5_m93_cr332_ZT_reduced.json
object_sha256: 9e16d07a126b9ef0421ed870f464c1f7927b34aa019c8f5a7d7589c15cd37af2
INDEX: target, cell, file, value, table_value, SHA256 agree
format: 5x5x5; dimensions <= 8; products: 93; z2: false
u: inputs=25, fresh=87, final=93, forms=180, terms=267, additions=87, binary_prefixes=87
v: inputs=25, fresh=88, final=93, forms=181, terms=269, additions=88, binary_prefixes=88
w: inputs=93, fresh=55, final=25, forms=80, terms=237, additions=157, binary_prefixes=157
Every term: integer index, available dependency, coefficient +1 or -1
Every named form and binary left-fold prefix: expanded coefficients in {-1,0,1}
Every product: nonzero U and V factors; used by at least one output
Tensor identity: 15625 / 15625 coefficients match over Z
Expected tensor: 125 ones; 15500 zeros
Output layout checked: output k*5+i equals C[i,k]
reduced additions: 332
expanded naive additions: 843
Metadata and filename count: 332; recorded comparison: 332 < 383 (difference 51)
expanded_uvw_sha256: 391cdd4d2a39c5317f82d7b38151a1bd79bc8d4800fef07a7dc26e5e604e7531
Determinism: two full parses, expansions, and exhaustive tensor checks agree
Scope: live tables and absent reference scheme not checked or recounted
PASS: all saved-object checks
```

Independent process determinism check:

```sh
python3 skeptic/check.py > skeptic/repeat-output.txt 2>&1
cmp skeptic/output.txt skeptic/repeat-output.txt
```

Both commands exited 0. `cmp` produced no output. The files are byte-identical.

Only after that first independent run did I inspect and run the author's implementation:

```sh
mkdir -p skeptic/tmp
TMPDIR="$(pwd)/skeptic/tmp" sh verify-it-yourself/run_checks.sh > skeptic/author-output.txt 2>&1
```

Exit status: 0. Complete captured output, inserted directly from `skeptic/author-output.txt`:

```text
sha256 matches INDEX.csv (9e16d07a126b9ef0421ed870f464c1f7927b34aa019c8f5a7d7589c15cd37af2)
== check_slp.py on object/5x5x5_m93_cr332_ZT_reduced.json (exact tensor identity, ternary coefficients, reduced addition count)
2026-10-15 16:29:16.584 xcodebuild[10083:76353805]  DVTFilePathFSEvents: Failed to start fs event stream.
2026-10-15 16:29:16.802 xcodebuild[10083:76353798] [MT] DVTDeveloperPaths: Failed to get length of DARWIN_USER_CACHE_DIR from confstr(3), error = Error Domain=NSPOSIXErrorDomain Code=5 "Input/output error". Using NSCachesDirectory instead.
{"file": "5x5x5_m93_cr332_ZT_reduced.json", "format": "5x5x5", "rank": 93, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 87, "adds_V": 88, "adds_W": 157, "adds_total": 332, "naive_total": 843, "declared_reduced": 332, "VALID": true}
checker verdict: PASS (VALID=True, adds_total=332, tensor=C^T)
== negative control: a copy with one coefficient sign flipped in the first fresh U form must FAIL
negative control rejected as expected (VALID false)
ALL CHECKS PASS
```

The Xcode diagnostics above are environment messages captured on stderr; the verification completed successfully. For a direct comparison and repeatability check I also ran:

```sh
python3 verify-it-yourself/check_slp.py object/5x5x5_m93_cr332_ZT_reduced.json > skeptic/author-direct-output.txt 2>&1
python3 verify-it-yourself/check_slp.py object/5x5x5_m93_cr332_ZT_reduced.json > skeptic/author-repeat-output.txt 2>&1
cmp skeptic/author-direct-output.txt skeptic/author-repeat-output.txt
```

All commands exited 0; `cmp` produced no output. Complete direct checker output, inserted from `skeptic/author-direct-output.txt`:

```text
{"file": "5x5x5_m93_cr332_ZT_reduced.json", "format": "5x5x5", "rank": 93, "tensor_exact": "C^T", "eval_ok": true, "adds_U": 87, "adds_V": 88, "adds_W": 157, "adds_total": 332, "naive_total": 843, "declared_reduced": 332, "VALID": true}
```

## Comparison and limitations

There is no result mismatch: the author and independent checker agree on exact tensor identity, transposed output layout, 93 products, U/V/W counts of 87/88/157, total 332, and naive count 843. The author's run script also rejects its sign-flipped negative control. I did not run the optional SymPy script; the independent exhaustive integer tensor reconstruction supplies the symbolic proof.

There is one author-checker coverage gap: `REPRODUCE.md` says it checks expanded intermediates for ternarity, but `verify-it-yourself/check_slp.py` checks only stored term signs and does not test its expanded vectors for membership in {-1,0,1}. The optional `verify-it-yourself/sym_check.py` likewise tests stored signs, not all expanded intermediate coefficients. This does not undermine this object's verdict: the independent checker explicitly checks every expanded named form and binary prefix and confirms the required condition.

Independent checker SHA256: `70656c7e3134ca0d4bf1b95a64e18fc493cd4468b855606ae803dc171f16f121`. The saved-object SHA256 and expanded U/V/W digest are in the real output above. No required saved object was missing; the unshipped reference and source pages remain explicitly outside this offline scope.

pass: true
