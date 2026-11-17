# Reproduce: every tree on 23 vertices is odd-graceful

context: subagent (fresh context; did not read the generator, the author's checker, VERIFY.md, run notes, or other skeptics' output)

I wrote an independent C checker from the definition of an odd-graceful labeling: an injective map
f: V -> {0, ..., 2q-1}, with q = 22, such that the edge labels |f(u)-f(v)| are exactly {1, 3, ..., 43}.

The certificate cert_n23.txt.gz (sha256 483c524995e2c184c1f5a7aeda65a69d44a97ac552c3c6177374bc4b13435520,
466729481 bytes gzip, 2679334720 bytes uncompressed) was read line by line. Line format, observed from
the file: n;u-v,u-v,...;label,label,...[;optional ignored field].

For each line the checker confirms: the graph uses vertex set {0, ..., n-1}, has exactly n-1 simple
undirected edges, is connected (hence a tree), the n labels are injective into {0, ..., 2q-1}, and the
n-1 edge differences are exactly the odd numbers {1, 3, ..., 2q-1}. Each tree is assigned the AHU
canonical form of an unrooted tree (one centre: rooted AHU string; two centres: sorted pair of the two
sides). The form is hashed with SHA-256, truncated to 128 bits, and inserted into an open-addressing
set. A duplicate hash is a failure. None occurred.

The SHA-256 implementation was checked against the FIPS 180-4 test vectors for the empty string and for
"abc". A self-test of handmade positives and negatives, isomorphism of two drawings of P4, inequality of
a path and a star, and an unlabeled-tree census for n = 1..9 against A000055, passed before the
certificate was read. OEIS A000055 was fetched once this session from
https://oeis.org/search?q=id:A000055&fmt=json at 2026-11-17T16:45:30Z (HTTP 200); a(23) = 14828074.

Full check, one core, started 2026-11-17T16:48:39Z, ended 2026-11-17T16:49:09Z, wall about 30 s,
runtime_seconds=29.917:

    lines_read=14828074
    n_expected=23
    count_expected_A000055=14828074
    labelings_valid_and_unique=14828074
    unique_canonical_forms=14828074
    parse_failures=0
    wrong_n=0
    odd_graceful_failures=0
    isomorphism_duplicates=0
    hash_collisions_recorded=0
    VERDICT=PASS

Every one of the 14828074 certificate lines is a tree on 23 vertices with a valid odd-graceful labeling;
the trees are pairwise non-isomorphic under an AHU canonical form; and the count equals OEIS A000055(23).
Therefore the certificate contains every unlabeled tree on 23 vertices exactly once, each with an
explicit odd-graceful labeling.

pass: true
