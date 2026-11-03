# A214570(17) = 3360: the largest number of ordered trees sharing one rooted-tree shape on 17 vertices

## What

Confirmed scope, quoted word for word from panel/gate.md:

> A214570(17) = 3360 -- one new term at the first missing index (n=17) of an OEIS keyword-more sequence, computed by two independently written programs (different algorithms) that agree and both reproduce DATA a(1..16), not present in the entry, its edit history (incl. pending drafts), or an OEIS value search as this count, and A214570 not named in the V3R1T4S bank.

OEIS A214570 (Emeric Deutsch, July 2012): a(n) = Max(c(t)), where c(t) is the number of ordered (plane) trees
isomorphic, as rooted trees, to the rooted tree t, and the maximum is over all rooted trees with n vertices. The entry
gives a(1..16) (offset 1, keyword nonn,hard,more; a(12..16) by Alois P. Heinz, 2012), ending a(16) = 1680. This folder
adds the next term:

    a(17) = 3360        (attained by exactly one rooted tree on 17 vertices)

The object is object/VALUE.txt (the single number 3360; sha256 ea6ddd47e1fce10db26cc83619ee6f58bbaac89d49bc9fc9c559aa68d54c4456).
Built-in checks used by every method: 634847 = A000081(17) rooted trees, and the c(t) sum to Catalan(16) = 35357670
(every ordered tree counted once).

How it was obtained (sources in how-we-built-it/):
- Program A (how-we-built-it/pA_c/progA.c, C, no formula): enumerates all Catalan(16) = 35357670 ordered trees as Dyck
  words, interns each node's sorted multiset of child classes in a hash table, counts ordered trees per rooted-tree
  class, and prints the largest count.
- Program B (how-we-built-it/pB_c/progB.c, C, different algorithm): enumerates all 634847 rooted trees by
  Beyer-Hedetniemi canonical level sequences and computes c(t) = prod deg! / prod (multiplicity of identical sibling
  subtrees)!.
- Both reproduce all 16 DATA terms and agree at n = 17 (same per-n maximizer counts); outputs in how-we-built-it/outputs/.
  A third small-n method (nested tuples) and a negative fixture (no multiplicity division, which fails DATA at n = 4)
  are in how-we-built-it/self-break/.
- The reproduce skeptic's own Python checker (panel/reproduce_work/mycheck.py), the criterion skeptic's re-run and the
  gate's re-run give the same a(17).

## Check it yourself

From this folder:

    sh verify-it-yourself/run_checks.sh

Expected last line: `PASS`. Rough laptop time: a few seconds. Requirements: Python 3 (standard library only); a C
compiler is optional (step 4). The script checks the sha256 of the object, then runs
verify-it-yourself/verify_a214570.py, a checker written for this package from the definition: (a) every ordered tree
with n <= 10 vertices as nested tuples, grouped by rooted-tree class; (b) every rooted tree with n <= 17 vertices
built once as a multiset of smaller trees, c(t) = deg!/prod(mult!) * prod c(child), with the A000081 and Catalan
self-checks. a(1..16) must equal DATA and a(17) must equal object/VALUE.txt. A negative control (no multiplicity
division) must not reproduce DATA. With a C compiler it also builds Program B and compares a(17) and its full output.
Real output: verify-it-yourself/RECEIPTS.md.

## Compared to

| source | cell | value | this package | fetched (UTC) |
|---|---|---|---|---|
| OEIS A214570 (revision #29, May 28 2015), DATA, b-file, history, drafts, value searches | a(17), first missing index | absent (DATA and synthesized b-file end at a(16) = 1680; keyword nonn,hard,more; no pending draft; full-prefix value search: no results; context searches 1680,3360 and 420,840,1680,3360: only unrelated sequences) | 3360 | 2026-11-03T21:36:24Z-21:38:03Z (claim time); 2026-11-03T22:15:56Z-22:16:08Z (panel); 2026-11-03T22:23:33Z-22:23:34Z (gate) |

URL: https://oeis.org/A214570 (b-file https://oeis.org/A214570/b214570.txt, history
https://oeis.org/history?seq=A214570). The fetch record is in the-record-we-beat/TABLE_SNAPSHOT.md.

## Not claimed

- Only a(17). Program B also printed a(18..21) = 6720, 15120, 30240, 55440 during the run; those by-products were
  checked by one program only, were not judged by the panel, and are not claimed here.
- The rooted tree attaining the maximum at n = 17 is counted (exactly one) but not published as an object.
- Programs A and B were written in the same run by the same contributor and are both in C; their independence is in
  algorithm (brute-force class counting over ordered trees vs level-sequence enumeration with the embedding formula).
  verify_a214570.py was written for this package after the gate.
- 3360 = 2 * 1680 continues a visible doubling pattern, so the value is guessable; it is computed here, not inferred.
  A search for 3360 alone returns 1069 unrelated hits (a small value); the context searches are the meaningful ones.
- The table check is as of the fetch times above. Nothing was submitted to the OEIS, and no pull request was opened.
- The OEIS pages are not shipped (third-party content); their URLs, times and sha256 are in the-record-we-beat/.
- panel/ holds the four panel files plus the reproduce skeptic's checker and logs, copied as written.

## Credits

- Emeric Deutsch: the sequence A214570, its definition and a(1..11), and the companion triangle A214569,
  https://oeis.org/A214570; Alois P. Heinz: a(12..16), the Maple program and the x^x^...^x comment; Jean-François
  Alcover: the Mathematica program; N. J. A. Sloane and other OEIS editors (edits/approvals).
- The OEIS Foundation, https://oeis.org; related entries A214569, A214571, A206487, A215703, A000081, A000108.
- T. Beyer and S. M. Hedetniemi, "Constant time generation of rooted trees", SIAM J. Comput. 9 (1980) (level-sequence
  enumeration used by Program B).
- V3R1T4S kit (target bank, panel protocol, checker gate): https://github.com/elder-plinius/V3R1T4S
- Contributor: GitHub CharanRayudu (https://github.com/CharanRayudu).
