# A316471(21) = 482706: locally disjoint rooted identity trees with 21 nodes

## What

Confirmed scope, quoted word for word from panel/gate.md:

> A316471 (bank-eligible, keyword more, live 2026-11-03T21:17Z) has DATA/b-file ending at a(20)=214490, and two independent programs matching the entry's definition (C and Go, rebuilt by me) both reproduce a(1..20) and give a(21)=482706, a value absent from OEIS search, the entry and its history; by-products a(22..26) are not covered.

OEIS A316471 (Gus Wiseman, July 2018) is the "Number of locally disjoint rooted identity trees with n nodes, meaning
no branch overlaps any other branch of the same root". A rooted identity tree has pairwise distinct branches at
every node; locally disjoint means that, at every node, no two distinct branches share a branch (per the entry's
Mathematica code). The entry gives a(1..20) = 1, 1, 1, 2, 3, 6, 11, 21, 43, 89, 185, 391, 840, 1822, 3975, 8727,
19280, 42841, 95661, 214490 (offset 1,4) and carries keyword more. This folder adds the next term:

    A316471(21) = 482706

The object is object/VALUE.txt, the single line `A316471(21) = 482706` (sha256
7eb8fe00ca9ad3d0cd9e416451bb86b10febf6b4551078a0034854cc7191ecd9).

How the number was obtained (sources in how-we-built-it/):
- Program A (how-we-built-it/pA_progA.c, C): canonical-id backtracking; a tree is a strictly increasing set of
  branch ids (identity), and a mark array forbids any grandchild id shared by two chosen branches (locally disjoint).
- Program B (how-we-built-it/pB_go/main.go, Go, no shared code): a literal transcription of the entry's Mathematica
  algorithm: integer partitions of n-1, sorted tuples of smaller trees, kept iff branches are pairwise distinct and
  pairwise have empty intersection of their own branch lists.
- Program C (how-we-built-it/pC_progC.py, Python with sympy): a Matula-Goebel oracle using the A316494 rule, n <= 11.
- A and B print a(1..20) = DATA and a(21) = 482706; C agrees for n <= 11. With the disjointness test removed, A and B
  both give A004111 (rooted identity trees) instead, as they should (how-we-built-it/outputs/).

## Check it yourself

From this folder:

    sh verify-it-yourself/run_checks.sh

Expected last line: `PASS`. Rough laptop time: a few seconds (about 1.4 s on the build machine). Requirements:
Python 3 (standard library only); a C compiler is optional (step 4). The script checks the sha256 of
object/VALUE.txt, then runs verify-it-yourself/verify_a316471.py, a checker written for this package from the
definition (canonical nested-string trees, strictly increasing branch choice, a literal pairwise test that the
branches' own branch sets are disjoint): it must give a(1..20) = DATA and a(21) equal to the value in
object/VALUE.txt. A negative control without the disjointness test must not reproduce DATA (it gives A004111). With
a C compiler it also builds Program A and requires its output to match for n = 1..21. Real output:
verify-it-yourself/RECEIPTS.md.

## Compared to

| source | cell | value | this package | fetched (UTC) |
|---|---|---|---|---|
| OEIS A316471 (revision #6, Jul 05 2018), DATA, b-file, history, drafts, value search | a(21) | absent (DATA and b-file end at a(20) = 214490; keyword nonn,more; no pending draft; value searches 482706 and 214490,482706: no results) | 482706 | 2026-11-03T20:00:13Z-20:03:09Z (claim time); about 2026-11-03T21:17Z (panel); 2026-11-03T21:29:31Z-21:29:35Z (gate) |

URL: https://oeis.org/A316471 (b-file https://oeis.org/A316471/b316471.txt, history
https://oeis.org/history?seq=A316471). The fetch record is in the-record-we-beat/TABLE_SNAPSHOT.md.

## Not claimed

- Only one cell, A316471(21). Program A also prints a(22..26) = 1090033, 2469229, 5609557, 12777215, 29173674
  (how-we-built-it/outputs/pA_26.txt); those are by-products, were not judged by the panel and are not claimed here.
- Programs A, B and C were written by the same contributor in the same run. Their independence is in language,
  generator and test algorithm (C id/mark-array backtracking vs Go literal partition x tuple filter).
  verify_a316471.py was written for this package after the gate.
- Program C needs sympy (not in the Python standard library; the reproduce skeptic used sympy 1.14.0 in a virtual
  environment). It is a small-n oracle only, not one of the two programs the criterion relies on.
- The table check is as of the fetch times above. Nothing was submitted to the OEIS, and no pull request was opened.
- The OEIS pages fetched are not shipped (third-party content); their URLs, times and sha256 are in the-record-we-beat/.
- panel/ holds the four panel files plus the reproduce skeptic's own checker, copied as written (panel/REDACTIONS.md:
  nothing redacted).

## Credits

- Gus Wiseman: the sequence A316471, its definition, Mathematica code and terms a(1..20), https://oeis.org/A316471;
  also A316494 (Matula-Goebel numbers of these trees, used by Program C), https://oeis.org/A316494; Susanna Cuyler,
  editor who approved revision #6.
- Robert P. P. McKone: the Feb 2026 extension of the sibling A316473 (locally disjoint rooted trees), checked by the
  novelty skeptic, https://oeis.org/A316473.
- The OEIS Foundation, https://oeis.org; A004111 (rooted identity trees, the negative control),
  https://oeis.org/A004111; A000081 (rooted trees, Program C's column), https://oeis.org/A000081.
- SymPy (Program C), https://www.sympy.org.
- V3R1T4S kit (target bank, panel protocol, checker gate): https://github.com/elder-plinius/V3R1T4S
- Contributor: GitHub CharanRayudu (https://github.com/CharanRayudu).
