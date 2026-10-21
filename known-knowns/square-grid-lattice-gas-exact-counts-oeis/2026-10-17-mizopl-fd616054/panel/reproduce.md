# REPRODUCE skeptic verdict — A054759(15)

context: subagent (general-purpose)

Claimed value (`object/a054759_15.txt`):
`4310182149988584261406143524214457416387448` (43 digits, 142 bits).

Definition verified (from `README.md` / `RUN_IT_YOURSELF.md`): A054759(n) = number of ways to
orient all 2n^2 edges of the n×n torus grid so every vertex has in-degree 2 and
out-degree 2 (square ice / six-vertex model at the ice point), offset 1.

## Check 1 — independent brute force from the definition (BEFORE reading author code)

I wrote my own enumerator over all 2^(2n^2) orientations of the n×n torus (horizontal
edge to the right + vertical edge down per vertex, mod n), counting those with in-degree 2
at every vertex. Output:

```
1 4
2 18
3 148
```

Matches https://oeis.org/A054759/b054759.txt (sha256 `26a837111876762bf9d1c5892c21ec1a15c36e00b0ee9e45bd2c389741cbfada`,
recorded in `the-record-we-beat/snapshot.md`) for n=1..3 (4, 18, 148) exactly.

## Check 2 — reproduction gate (n=1..14)

I ran a harness importing the author's transfer-matrix code (`how-we-built-it/sixvertex.py`,
as driven by `how-we-built-it/reproduce.py`) and compared against the published OEIS terms
from https://oeis.org/A054759/b054759.txt (sha256 `26a837111876762bf9d1c5892c21ec1a15c36e00b0ee9e45bd2c389741cbfada`). Output:

```
n= 1 computed=4 ... OK
n= 2 computed=18 ... OK
...
n=14 computed=15844635835975276495290739119895808472 published=15844635835975276495290739119895808472 OK
RESULT: ALL MATCH
```

All 14 published terms reproduced exactly. Combined with Check 1, the transfer matrix
matches the definition (n=1,2,3) and matches OEIS through n=14.

## Check 3 — independent CRT of saved residues (`object/residues.txt`)

With my own gcd-based CRT routine, primality check on every modulus, and residue check:

```
RUN_A: CRT value = 4310182149988584261406143524214457416387448   (220 bits)   matches object/a054759_15.txt? True
RUN_A: all value%prime==residue? True   modulus > value*2^64? True
RUN_B: CRT value = 4310182149988584261406143524214457416387448   (228 bits)   matches object/a054759_15.txt? True
RUN_B: all value%prime==residue? True   modulus > value*2^64? True
RUN_A prime count: 11   RUN_B prime count: 12
prime sets disjoint? True
value bit length: 142   value*2^64 bit length: 206
```

Both runs CRT to the value in `object/a054759_15.txt`; every row's value%prime==residue; prime sets
disjoint; both moduli (220, 228 bits) exceed value·2^64 (206 bits).

## Check 4 — gold standard: independent recomputation of the n=15 residues (~12 min)

I re-ran the transfer matrix myself for N=15 for BOTH decompositions (RUN_A: forward
encoding + closed-form entry, 11 primes near 2^20; RUN_B: reversed encoding + explicit
two-walk entry, 12 disjoint primes near 2^19) and compared each recomputed residue to the
saved `object/residues.txt`:

```
RUN_A p=1048573 r=597868 saved=597868 match=True
... (all 11 RUN_A rows match=True) ...
RUN_A CRT=4310182149988584261406143524214457416387448 bits=220 ==value? True
RUN_B p=524287 r=301866 saved=301866 match=True
... (all 12 RUN_B rows match=True) ...
RUN_B CRT=4310182149988584261406143524214457416387448 bits=228 ==value? True
AGREE: True ==object/a054759_15.txt: True
```

Every one of the 23 residues was reproduced from scratch and matched the saved file. The
two runs use different state encodings AND different entry code paths AND disjoint primes,
and both independently reconstruct the identical 43-digit integer. This is a full, not
spot-checked, reproduction.

## Check 5 — determinism / mismatches

No mismatches found. The transfer-matrix computation is deterministic (float64 BLAS matmul
with exact int64 reduction, entries < p < 2^20 and contracted dim ≤ C(15,7)=6435, so
products sum < 2^53 — exact), and my independent rerun produced byte-identical residues.
No missing objects; all referenced files are present in this package.

## Note on the growth clause (not a reproduction matter)

The claim openly reports a(15)^(1/225)=1.5469869 vs the Lieb ice constant W=1.5396007,
gap 0.0074 > 1e-3, and notes a(14) also fails it (gap 0.0085). Whether the p1 partial-win
criterion requires the growth clause is an ORACLE-scope interpretation, not reproduction.
From a pure reproducibility standpoint, the value and every stated property (two agreeing
runs, disjoint primes, different decompositions, CRT bound, reproduction of n=1..14, and
the definition for n=1..3) reproduce exactly.

pass: true
