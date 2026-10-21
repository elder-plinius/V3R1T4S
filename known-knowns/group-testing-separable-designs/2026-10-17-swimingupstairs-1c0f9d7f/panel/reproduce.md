# REPRODUCE skeptic: OEIS A054961, n=14 (m=65) and n=15 (m=79)

context: subagent (fresh context, knowledgeWork subagent; saw only claim/ and kit/)
date: 2026-10-17T04:04:23Z (from `date -u`)

## Definition used (fetched, quoted)
Single GET of https://oeis.org/A054961 with User-Agent "V3R1T4S-panel-reproduce", one request with no retries:
HTTP 200 at 2026-10-17T04:03:31Z, sha256 of body 49b556b744a5ba44bbed7c7d77569055898544a274c7940f6351030d1e2ae5d1.
- %N: "Maximal number of binary vectors of length n such that the unions (or bitwise ORs) of any 2 distinct vectors are all distinct."
- %C: "The concatenation of these vectors produces a 2-separable matrix."
- %C: "a(13) to a(27) are >= 55,63,72,91,... - Zhao Hui Du, Apr 19 2018". So for n=14 and n=15 OEIS gives only
  **lower bounds**, a(14) >= 63 and a(15) >= 72. Known terms are a(0..9) = 1,2,3,4,5,6,8,10,13,17.

## Interpretation (PROVED-HERE for small cases; reading of %N is KNOWN)
Property P2: for distinct indices {i,j}, the map {i,j} -> v_i OR v_j is injective, and the vectors are distinct.
The property covers unions of exactly 2 vectors ("2-separable" in the exact sense). It is NOT the stronger
"unions of <= 2 vectors distinct" (2-bar-separable), and NOT 2-disjunct / cover-free ("no set covered by the union of two
others", the Erdős-Frankl-Füredi notion, which OEIS cites only for asymptotics). Evidence:
- All 9 OEIS example families (n=4..12) satisfy P2. All 9 fail <=2-separability and all 9 fail 2-disjunctness, e.g. the n=4
  example contains 0000 and 0001, with 0000|0001 = 0001.
- My own branch-and-bound brute force under P2 gives a(0..6) = 1,2,3,4,5,6,8, matching the OEIS data exactly.

## Independent verifier
I wrote my own checker from the %N definition before using check_union.py. It is stdlib Python, exhaustive over every
unordered pair, and it parses with whitespace split plus strict length/alphabet checks.
NUMERICAL / PROVED-HERE (exhaustive, deterministic) output:
```
n=14 file_sha256=1c0f9d7f1d2470dfd4f1a1cb39fbf961d84afa6c7c1391de788c249710744ac6 m=65 bad_tokens=0 duplicates=0 pairs=2080 distinct_ORs=2080 A054961_property=True clash=None bound_m(m-1)/2<=2^n:True le2_separable=False 2-disjunct=False zero_vector_present=False
n=15 file_sha256=5323b7e4a596e3f8d9e33f3d8feddc4ef0a3c05e933494bb873a93e221e41118 m=79 bad_tokens=0 duplicates=0 pairs=3081 distinct_ORs=3081 A054961_property=True clash=None bound_m(m-1)/2<=2^n:True le2_separable=False 2-disjunct=False zero_vector_present=False
```
The file hashes match CLAIM.md. Both families satisfy the OEIS A054961 property. As expected for this sequence, they do
not satisfy the stronger notions, and neither do OEIS's own examples. This means the claim must not be described as
"union-free", "2-disjunct" or "<=2-separable". "Pairwise ORs all distinct" (CLAIM.md's wording) is correct.

## Does the folder's checker test the same property?
Yes. By reading check_union.py: with k=2 it requires every token to have length n, all vectors distinct, and the ORs of all
unordered 2-subsets of distinct indices to be pairwise distinct. That is exactly P2 (singletons are not included, which is
correct for A054961). One small note: its regex `[01]+` would silently skip non-binary characters rather than reject them,
but the files hold only clean 0/1 tokens (bad_tokens=0 above). Differential test: 124 adversarial inputs (120 single-bit
flips of the claimed files, 2 duplicate injections, 2 truncated vectors). check_union.py and my verifier agreed on 124/124,
and all 124 were rejected. Its check_output.txt agrees with my results.

## Verdict per n
- n=14: PASS. There are 65 distinct length-14 vectors, and all 2080 pairwise ORs are distinct. 65 > 63 (the OEIS lower bound).
  This reproduces a(14) >= 65 as a lower bound only, not an exact value.
- n=15: PASS. There are 79 distinct length-15 vectors, and all 3081 pairwise ORs are distinct. 79 > 72 (the OEIS lower bound).
  This reproduces a(15) >= 79 as a lower bound only, not an exact value.
Scope: this file covers reproduction of the objects and the property only. Novelty against non-OEIS sources and
the success criterion belong to the other panelists.

pass: true
