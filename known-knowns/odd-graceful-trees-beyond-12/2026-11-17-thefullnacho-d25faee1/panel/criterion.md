# Criterion: the paneled object is a complete certificate for n = 23

context: subagent (fresh context; wrote its own tree generator and labeling checker; did not read the author's generator, checker, run notes, or other skeptics' output)

Definition used: injective f: V -> {0, ..., 2q-1} with q = 22, and {|f(u)-f(v)| : edges} = {1, 3, ..., 43}.

The certificate cert_n23.txt.gz (sha256 483c524995e2c184c1f5a7aeda65a69d44a97ac552c3c6177374bc4b13435520)
contains 14828074 lines. OEIS A000055(23) = 14828074, fetched this session (HTTP 200).

An independent C enumerator generated all unlabeled free trees on 23 vertices by composing canonical
rooted trees at the centroid (WROM-style). Rooted counts match A000081 for n = 1..12. Free-tree counts
match A000055 for n = 1..23. The same canonical form (lex-min preorder level sequence at the centroid(s))
was applied to the generated trees and to the certificate trees, then compared one-to-one. Every
certificate line was checked as a tree and as an odd-graceful labeling. A second, independent Python
checker also accepted every labeling.

Counts from the successful C generate-and-match run (one core, about 73 s process time,
2026-11-17T16:53:46Z to 2026-11-17T16:54:59Z):

- Generated trees at n=23: 14828074
- Certificate lines: 14828074
- Bad lines: 0
- Unique generated keys: 14828074 (0 duplicates)
- Unique certificate keys: 14828074 (0 duplicates)
- Set intersection: 14828074
- Only-generated / only-certificate: 0 / 0

A third fresh-context checker (Rust, WROM generator plus AHU membership, 2026-11-17T16:50:25Z to
2026-11-17T16:51:44Z) reported the same counts, with generated_leftover=0.

The fourth certificate field is leftover generator metadata (it is not q) and was ignored. It is not a
defect in the labeling.

Confirmed scope, no wider than this evidence: every unlabeled tree on 23 vertices is odd-graceful. This
is not, by itself, a literal satisfaction of bank target odd-graceful-trees-beyond-12 success criterion
(a), which asks for a certificate that every tree on at most 22 vertices is odd-graceful, with a file
for each n in 13..22. Partial wins p1 and p2 are the same claim cut at 16 and 20. The paneled object is
a complete certificate for the single order n = 23. That is a stronger single-order verification than
22, and it does extend the published bound past 12, but the 13..22 files named in (a) were not before
this panel.

nauty gentreeg was not used. A WROM generator is the same family of algorithm the bank's "how a win is
checked" line is aiming at: regenerate the trees, match counts to A000055, match by canonical form,
check every labeling.

pass: true
