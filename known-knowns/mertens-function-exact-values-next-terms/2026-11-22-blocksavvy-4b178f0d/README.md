# A084235(18) = 330055906058: least k with |M(k)| = 2^18

This is a **new OEIS term** (the next term of an existing sequence, computed by a known method: a segmented
Möbius sieve). It is not a new mathematical discovery, and it says nothing about the Riemann hypothesis.
Submission id: `2026-11-22-blocksavvy-4b178f0d`. Bank target: `mertens-function-exact-values-next-terms`,
partial win p1, a(18) only.

## What

Two separately written full segmented Mobius sieves from k = 1 (to 3.4e11 and 3.30125e11) agree that the least k with |M(k)| = 2^18 is 330055906058, where M(k) = -262144, and A084235 on OEIS ended at a(17) when re-fetched on 2026-11-22. This meets bank partial win p1 for a(18) only (not 2^19 or 2^20, and not the full criterion), with novelty against A051402 and outside sources left to the NOVELTY skeptic.

In short: with M(x) = sum over n <= x of mu(n) (the Mertens function, OEIS A002321), the least k >= 1 with
|M(k)| = 2^18 = 262144 is **k = 330055906058**, where M(k) = -262144 (object/a18.txt). The previous term is
a(17) = 108500046711. Three separately written sieves ran in full from k = 1 (two by the contributor, one by the
REPRODUCE skeptic) and agree.

## Check it yourself

From this folder (Python 3 standard library plus any C compiler):

```
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS`. Rough time: about 40 seconds on a laptop (quick tier). It brute-forces mu from the
definition against the C sieve, reproduces a(0..9) in pure Python, chains the run-1 block certificate to the
published M(10^8..10^11), recomputes 22 blocks of 10^8 from the definition (anchors, the first-hit blocks for
2^14..2^18, the block before the hit and 12 random blocks) and rescans the first-hit blocks exactly: it gets the
published a(14..17) and the object's k and M(k). The quick tier trusts the certificate for blocks it does not
recompute. For the complete check from k = 1 (no trust in the certificate), run
`FULL=1 sh verify-it-yourself/run_checks.sh` (about 2 CPU-hours; about 20 minutes on 6 cores). Receipts
for the original quick and full tiers, and for a later single-threaded FULL=1 re-run on a separate
Apple M1 iMac, are in verify-it-yourself/RECEIPTS.md (iMac logs also under
verify-it-yourself/independent_hardware/).

## Compared to

| sequence | cell | our value | table value | source | fetched (UTC) | HTTP | sha256 of fetched file |
|---|---|---|---|---|---|---|---|
| OEIS A084235 | a(18) | 330055906058 | absent (b-file ends at a(17) = 108500046711) | https://oeis.org/A084235/b084235.txt | 2026-11-22T17:17:09Z | 200 | e40ebda76ec5f993ea987206d65b8b630c2c94a4a90e9aad6939d8a10ead363f |

Also checked by the NOVELTY skeptic: the OEIS search for 330055906058 finds nothing; A051402 (a(n) = A051402(2^n))
and A051400/A051401 b-files stop at n = 10000; A304241/A304242 (Dobbelaere and Hurst) only bracket a(18) between
the extrema M(297193839495) = 207478 and M(330508686218) = -294816. See the-record-we-beat/ and panel/novelty.md.
The b-file must be re-fetched immediately before this is submitted anywhere (bank criterion).

## Not claimed

- Not the bank's full criterion (new terms of A084237 or A084236 with the M(10^22), M(10^23), M(2^74), M(2^75)
  consistency checks); only partial win p1, and only a(18). Nothing about 2^19 or 2^20.
- Not a new mathematical discovery and not progress on the Riemann hypothesis: a(18) is implicit in earlier
  complete sieves well past 3.3e11 (for example Hurst's sieve to 1e16, which recorded extrema but did not publish
  this first hit). The contribution is computing, verifying and publishing the term.
- The three independently written full sieves (two by the contributor, one by the REPRODUCE skeptic)
  all ran on the same machine, and the two contributor codes share an author and a sieve skeleton (different mu
  tests, segment and block sizes). A later full-tier re-run of this package's own checker (`FULL=1`,
  single-threaded) was done on separate hardware, an Apple M1 iMac running macOS; receipt in
  verify-it-yourself/independent_hardware/ and RECEIPTS.md.
- The quick tier of run_checks.sh is a spot check of the certificate, not a proof of "least"; the full tier is.

## Credits

- **Contributor:** [BlockSavvy](https://github.com/BlockSavvy). Found with a V3R1T4S agent run (extender and
  contrarian lenses), checked by a three-skeptic panel of fresh subagent contexts.
- **Robert G. Wilson v**: author of OEIS A084235 (May 2003). https://oeis.org/A084235
- **Ashley Jordan and Luke March**: a(14)-a(17) (Jul 2014); **L. Edson Jeffery** (definition, 2013) and
  **Sean A. Irvine** (offset, Mar 2026), editors of A084235. https://oeis.org/A084235
- **Amiram Eldar**: the formula a(n) = A051402(2^n). https://oeis.org/A051402
- **Greg Hurst**: Mertens function computations to 1e16 and the extrema list that brackets a(18)
  (arXiv:1610.08551, Math. Comp. 87 (2018) 1013-1028, https://arxiv.org/abs/1610.08551; and arXiv:2607.07566,
  https://arxiv.org/abs/2607.07566). **Dobbelaere and Hurst** (as credited on the OEIS entries): A304241/A304242,
  https://oeis.org/A304241 and https://oeis.org/A304242.
- **The OEIS Foundation** and the editors of A002321, A084237 (the M(10^n) values used as anchors) and A051402.
  https://oeis.org/A002321 , https://oeis.org/A084237
