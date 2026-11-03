# Panel: REPRODUCE

context: fresh-context subagent, saw package only
date: 2026-11-03 (UTC), work between 12:47Z and 13:03Z

## Procedure (written out before starting; kit/RUN.md step 6, REPRODUCE)

1. Use only this package folder and the archive named in object/CERTIFICATES.md (sem-trees-18-20-certificates.tar.xz),
   unpacked into a scratch folder outside the package. Read no run notes and no earlier panel work.
2. Before running or reading the package's checkers, write an own checker from the definition alone.
3. Calibrate it on known positives, a bad edge-sum set, a cycle, a repeated label and an isomorphic duplicate, and test
   its canonical form against brute-force enumeration of all labelled trees for small n.
4. Check every line of every certificate (no sampling); compare the number of distinct trees with A000055(n) computed
   by the checker itself (Otter's formula), not copied from the package.
5. Run the package's own `sh verify-it-yourself/run_checks.sh` and require last line `PASS`.
6. Fail on any mismatch, missing tree, malformed line or non-determinism.

## Definition used (quoted from the package README)

"a bijection onto {1..n} with n-1 consecutive edge sums" for each tree, i.e. a graph with p vertices and q edges is
super edge-magic iff there is a bijection f: V -> {1..p} whose q edge sums f(u)+f(v) are q consecutive integers.

## What was done

- Archive: 29618152 bytes, sha256 390d1698ff6e9563ed2e41a645cff865a05ab6b5427ece910e5bdda6ed82cc8b, matching
  object/CERTIFICATES.md. It lists exactly three files, no folder. Unpacked cert_n18.txt, cert_n19.txt, cert_n20.txt
  have the sha256, byte sizes and line counts in object/CERTIFICATES.md and object/certificates.sha256.
- Own checker: panel/reproduce-work/fresh/fresh_check.py (python3 standard library). Per line: n field equals n;
  exactly n-1 edges, endpoints in 0..n-1, no loops, no repeated edges, connected by BFS (so a tree); labels a
  permutation of 1..n; sorted edge sums equal s, s+1, ..., s+n-2. Isomorphism class: centre(s) by leaf peeling, then an
  AHU parenthesis code rooted at the centre (two centres: code of the central edge, both halves ordered), collected in
  a set; a repeat counts as dup. A000055(n) from A000081 by the rooted-tree recurrence and Otter's formula.
- Calibration (fresh_check.py calib, dup.txt): valid P4 and K1,3 -> PASS; P4 with sums 3,5,7 -> FAIL (bad_sums=1);
  triangle -> FAIL (not_tree=1); repeated label -> FAIL (bad_labels=1); relabelled isomorphic P4 duplicate -> FAIL (dup=1).
- Canonical-form test (panel/reproduce-work/fresh/canon_test.py): all n^(n-2) Pruefer trees for n=3..8 give
  1, 2, 3, 6, 11, 23 distinct forms = A000055; 3000 random trees on 10..20 vertices under random relabelling gave
  0 mismatches.
- Own Otter computation gives A000055(18..20) = 123867, 317955, 823065, the same as verify-it-yourself/A000055_18_20.txt.
- Full run, every line (panel/reproduce-work/fresh/fresh_out.txt):
  - n=18 lines=123867 bad_parse=0 wrong_n=0 not_tree=0 bad_labels=0 bad_sums=0 dup=0 distinct=123867 expected_A000055=123867 -> PASS
  - n=19 lines=317955 bad_parse=0 wrong_n=0 not_tree=0 bad_labels=0 bad_sums=0 dup=0 distinct=317955 expected_A000055=317955 -> PASS
  - n=20 lines=823065 bad_parse=0 wrong_n=0 not_tree=0 bad_labels=0 bad_sums=0 dup=0 distinct=823065 expected_A000055=823065 -> PASS
- Completeness: every line is a tree on n vertices with a valid labeling, the lines are pairwise non-isomorphic, and
  there are exactly A000055(n) of them, so every isomorphism class of trees on n vertices has a certificate.
- Package's own check, `CERT_DIR=<scratch> sh verify-it-yourself/run_checks.sh` (panel/reproduce-work/fresh/pkg_out.txt):
  all five sections `-> PASS`, `OVERALL: PASS`, last line `PASS`, exit 0. Section 5 regenerated 123867, 317955 and
  823065 trees with missing=0 extra=0.
- Determinism: both checks are deterministic over fixed files with fixed hashes; own checker and package checker agree.

## Limits of this review

- Custody: the archive was supplied locally as the file the placeholder archive_url will point to; the URL itself is
  not yet filled in and was not fetched. Once hosted, its sha256 must still equal the value above.
- Orders up to 17 are not re-checked (the package does not claim to); they rest on the cited Lee and Shan result.
- Wall times are not reported: the host paused during the run, so timings are unreliable.

verdict: SURVIVES
pass: true
