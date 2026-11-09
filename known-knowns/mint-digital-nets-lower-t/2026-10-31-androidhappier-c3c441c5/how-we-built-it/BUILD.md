# How the object was built (exact commands)

Run from the package folder in a fresh shell. Needs a C compiler and python3 (standard library only); no other
dependencies, nothing to pin. The construction is deterministic for a given seed.

    cc -O2 -o gvgreedy2 how-we-built-it/gvgreedy2.c
    ./gvgreedy2 24 17 11 101 > first13.txt          # about 15-20 s, about 16 MB of memory; progress goes to stderr
    python3 how-we-built-it/pad_full.py first13.txt full.txt 24 17
    cmp first13.txt object/net_F2_t11_m24_s17_first13rows.txt && echo first13 identical
    cmp full.txt object/net_F2_t11_m24_s17.txt && echo full identical

Expected sha256:
- first13.txt  a4b7187724050c0d657597b5d1b399fd78bd4b8bcb250143f2e9834bc646dbe6
- full.txt     c3c441c507605e64d545fb6c6ab57863c7306e8b29dc88bafca22577dfd54618

Arguments of gvgreedy2: m s t seed. Seed 101 is the first of the three seeds (101, 102, 103) fixed in PREREG.md
before the claim object was generated.

## Files
- gvgreedy2.c: depth-major randomized greedy over F_2. Row j of C_i is drawn uniformly from the vectors outside an
  exact forbidden set, kept as a bitmap over F_2^m: the span of the rows of C_i above it, plus every sum of
  already-placed rows of the other matrices whose NRT weight is at most k - j (k = m - t). Rows that avoid this set
  keep every composition independent, so the output is a digital (t,m,s)-net by construction. It is still checked
  independently (verify-it-yourself/). The source comments mention F_4 because the file was derived from a base-4
  version; this binary works over F_2.
- pad_full.py: completes the first k = 13 rows of each C_i to a nonsingular 24x24 matrix with unit vectors. Rows
  14..24 do not enter the t = 11 condition.
- PREREG.md: the run's preregistration, copied unchanged (frozen 2026-10-31 14:32:51 UTC, before the claim object
  was generated). It states null_test: not needed (the claim is an explicit object checked exhaustively).

Verified on the build machine, 2026-10-31: a rebuild from seed 101 is byte-identical to both object files.
