# REPRODUCE skeptic verdict

context: subagent (Claude Code Agent tool, opus, fresh context, saw only claim/)
verdict time (date -u): 2026-11-09T14:40:29Z
injection_suspected: none

Claim checked: Meunier's conjecture for (k,s) = (3,5): chi(KG(17,3)_{5-stab}) = 7 and chi(KG(22,3)_{5-stab}) = 12
(claimed), with n = 18..21 as confirmations. For each n = 17..22 this needs: the CNF "KG(n,3)_{5-stab} is
(n-11)-colourable" is UNSAT (DRAT proof checked by drat-trim on a CNF I regenerated), and a proper (n-10)-colouring.

My own files (generator, colouring checker, lzma decompressor, built binaries, logs) live in my scratch folder and
are named below by bare filename. Paths starting with object/ or tools/ are inside claim/.
This file contains no angle-bracket characters: where my scripts printed a two-character arrow (minus sign, then
greater-than sign) it is written as the word "gives", and the inequality signs in the quoted definition are
spelled out in square brackets. Everything else in the output blocks is verbatim.

## Definition used (quoted from REPRODUCE.md, which cites arXiv 2607.12912)

"[n] = {1..n}; S is s-stable if min{j - i, n + i - j} [at least] s for all i [less than] j in S; KG(n,k)_{s-stab} has the s-stable
k-subsets of [n] as vertices, adjacent iff disjoint. Here k = 3, s = 5."

Encoding (REPRODUCE.md, paraphrased with the bracket placeholders rewritten): vertices are the 5-stable 3-subsets
as sorted tuples in lexicographic order, v = 0, 1, ...; x(v,c) = v*C + c + 1 with C = n - 11; clauses in order:
one at-least-one-colour clause per vertex, then for each edge u lt v (by u, then v) and each c the clause
(-x(u,c) | -x(v,c)), then units x(Q_j, j-1) for j = 1..min(t, C), t = floor(n/3), Q_j = {j, j+t, j+2t}; header
'p cnf V*C clauses', one clause per line ending ' 0', no comments.

Soundness of the symmetry breaking (my own argument): the Q_j are pairwise disjoint, hence pairwise adjacent, so in
any proper C-colouring they receive min(t,C) distinct colours; permuting colours maps any proper colouring to one
with Q_j coloured j-1. So the CNF with units is satisfiable iff the graph is C-colourable. This is exactly the
"fixing colours on a clique of pairwise disjoint s-stable sets" the criterion allows.

## Check 1: my own CNF generator (written before opening tools/)

I wrote mygen.py (stdlib Python) from the text above only. It also asserts that every Q_j is a vertex, is 5-stable,
and that the Q_j are pairwise disjoint.

Command: `for n in 17 18 19 20 21 22; do C=$((n-11)); python3 -I mygen.py $n 3 5 $C n${n}_k3_s5_c${C}.cnf; done`

```
n=17 C=6 vertices=34 edges=374 clauses=2283 vars=204 Q=[(1, 6, 11), (2, 7, 12), (3, 8, 13), (4, 9, 14), (5, 10, 15)]
n=18 C=7 vertices=60 edges=1140 clauses=8046 vars=420 Q=[(1, 7, 13), (2, 8, 14), (3, 9, 15), (4, 10, 16), (5, 11, 17), (6, 12, 18)]
n=19 C=8 vertices=95 edges=2850 clauses=22901 vars=760 Q=[(1, 7, 13), (2, 8, 14), (3, 9, 15), (4, 10, 16), (5, 11, 17), (6, 12, 18)]
n=20 C=9 vertices=140 edges=6240 clauses=56306 vars=1260 Q=[(1, 7, 13), (2, 8, 14), (3, 9, 15), (4, 10, 16), (5, 11, 17), (6, 12, 18)]
n=21 C=10 vertices=196 edges=12390 clauses=124103 vars=1960 Q=[(1, 8, 15), (2, 9, 16), (3, 10, 17), (4, 11, 18), (5, 12, 19), (6, 13, 20), (7, 14, 21)]
n=22 C=11 vertices=264 edges=22814 clauses=251225 vars=2904 Q=[(1, 8, 15), (2, 9, 16), (3, 10, 17), (4, 11, 18), (5, 12, 19), (6, 13, 20), (7, 14, 21)]
```

Vertex counts agree with the closed form n/(n-12) * binom(n-12, 3): 34, 60, 95, 140, 196, 264.
Clause counts check by hand, e.g. n = 17: 34 + 374*6 + 5 = 2283; n = 22: 264 + 22814*11 + 7 = 251225.

Hash comparison against object/cnf_sha256.txt (`sha256sum -c` on its hash/filename columns):

```
a995b6a42f1457c779bbfa910f6d5a4c06246f7b193e85737d025d21ff2fcfa9  n17_k3_s5_c6.cnf
0fdf3fd23554b77dbaece3c91dd020ebac901b01283160942e69acf6cbb851ad  n18_k3_s5_c7.cnf
7dd4c309760e4d50953cc58f428026e0e7d98ad3c83f2e030c6ca410b0c21c55  n19_k3_s5_c8.cnf
9f571b3e4deddd5813d40c045f86847de73125a650416138077610160205eba0  n20_k3_s5_c9.cnf
3d3d48ff23b7d10754c7ae5e991ab3bdb2409ef365af954f99d622c2f1a7ed1b  n21_k3_s5_c10.cnf
b5caefbad0996e1d8836998e01b134b50edb1a66c14dc3b589d91c87cd544adb  n22_k3_s5_c11.cnf
----
n17_k3_s5_c6.cnf: OK
n18_k3_s5_c7.cnf: OK
n19_k3_s5_c8.cnf: OK
n20_k3_s5_c9.cnf: OK
n21_k3_s5_c10.cnf: OK
n22_k3_s5_c11.cnf: OK
```

All six hashes match, and the vertex/edge/clause counts match the ones in object/cnf_sha256.txt.

Clique Q_j, checked separately for every n (REPRODUCE.md states it only for n = 17..21; I checked n = 22 too):

```
n=17 C=6 t=5 units=5 min cyclic distance inside Q_j=5 pairwise disjoint=True union=True
n=18 C=7 t=6 units=6 min cyclic distance inside Q_j=6 pairwise disjoint=True union=True
n=19 C=8 t=6 units=6 min cyclic distance inside Q_j=6 pairwise disjoint=True union=True
n=20 C=9 t=6 units=6 min cyclic distance inside Q_j=6 pairwise disjoint=True union=True
n=21 C=10 t=7 units=7 min cyclic distance inside Q_j=7 pairwise disjoint=True union=True
n=22 C=11 t=7 units=7 min cyclic distance inside Q_j=7 pairwise disjoint=True union=True
```

Every Q_j is 5-stable (smallest cyclic distance 5 at n = 17, larger elsewhere), the Q_j are pairwise disjoint (they
partition {1..3t}), and the number of units is min(t, C) in every case.

After my generator existed I read tools/gen_cnf.py (not executed). It implements the same encoding. Its docstring
refers to PREREG.md, which is not in claim/; that does not affect anything checked here.

## Check 2: tools built independently

drat-trim: `curl -sSL -o drat-trim.c https://raw.githubusercontent.com/marijnheule/drat-trim/master/drat-trim.c`
(exit 0), sha256 `d834b649f437e091597f5347f259b9f681087f89ca0844d0cee250a1a1a0c2ee`, header "Last edit: April 21,
2024". The GitHub API's latest commit touching drat-trim.c is `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`
(2024-11-25), the same commit REPRODUCE.md names (2e3b2dc0ecf9). Built with
`systemd-run --user --scope -q -p CPUQuota=100% nice -n 10 gcc -O2 -o drat-trim drat-trim.c` gives exit 0
(gcc 16.2.1 20260810).

CaDiCaL: `curl -sSL -o cadical-rel-3.0.1.tar.gz https://github.com/arminbiere/cadical/archive/refs/tags/rel-3.0.1.tar.gz`
(exit 0), 889912 bytes, sha256
`0a8ea563b5a25f5aa064634814edab45cc0e45111ea0f5d412a565f806fd7e11`, equal to the tarball hash in
object/proof_n22_c11_not_shipped.txt. VERSION file: 3.0.1. Built with
`systemd-run --user --scope -q -p CPUQuota=100% nice -n 10 bash -c './configure && make -j2'` gives exit 0;
`./build/cadical --version` gives `3.0.1`. (Only build warnings: no git id available from a tarball, and one
unused-variable warning in kitten.c.)

## Check 3: shipped proofs n = 17..21 against my regenerated CNFs

Decompressed with Python lzma (my unxz.py; `xz -t` on all five archives also reported no error):

```
object/proof_n17_c6.drat.xz gives proof_n17_c6.drat bytes=525 sha256=65fe24a4b8ef43f23303f5278b20479ab747e1321dfd3f778cfc809605b2f80f
object/proof_n18_c7.drat.xz gives proof_n18_c7.drat bytes=5285 sha256=24e5f07406be700ed086a0936ee8102c5be41150d99c8a003d521e50b62920d1
object/proof_n19_c8.drat.xz gives proof_n19_c8.drat bytes=37037 sha256=c84568048050defdd5972fda04d905ec5d660a924e2e9f47d61d0728e581fc6d
object/proof_n20_c9.drat.xz gives proof_n20_c9.drat bytes=375564 sha256=3a0c8aa39e0b6fbd0a322057cea418af111100d66a838c00e2be8af804a1c172
object/proof_n21_c10.drat.xz gives proof_n21_c10.drat bytes=2989068 sha256=194fb8a89c7b2f382ca22153913028d3a52ee1127a17c66f4c8caf86b06ffd6a
```

Command per n: `systemd-run --user --scope -q -p CPUQuota=100% nice -n 10 ./drat-trim nN_k3_s5_cC.cnf proof_nN_cC.drat`
(my drat-trim, my CNF), run one after another. Full output:

```
=== n=17: drat-trim n17_k3_s5_c6.cnf proof_n17_c6.drat
exit 0 wall 0 s
c turning on binary mode checking
c parsing input formula with 204 variables and 2283 clauses
c finished parsing, read 525 bytes from proof file
c detected empty clause; start verification via backward checking
c 146 of 2283 clauses in core
c 9 of 10 lemmas in core using 407 resolution steps
c 0 RAT lemmas in core; 0 redundant literals in core lemmas
s VERIFIED
c verification time: 0.031 seconds
=== n=18: drat-trim n18_k3_s5_c7.cnf proof_n18_c7.drat
exit 0 wall 0 s
c turning on binary mode checking
c parsing input formula with 420 variables and 8046 clauses
c finished parsing, read 5285 bytes from proof file
c detected empty clause; start verification via backward checking
c 699 of 8046 clauses in core
c 82 of 83 lemmas in core using 5324 resolution steps
c 0 RAT lemmas in core; 3 redundant literals in core lemmas
s VERIFIED
c verification time: 0.033 seconds
=== n=19: drat-trim n19_k3_s5_c8.cnf proof_n19_c8.drat
exit 0 wall 0 s
c turning on binary mode checking
c parsing input formula with 760 variables and 22901 clauses
c finished parsing, read 37037 bytes from proof file
c detected empty clause; start verification via backward checking
c 2840 of 22901 clauses in core
c 844 of 852 lemmas in core using 34335 resolution steps
c 0 RAT lemmas in core; 22 redundant literals in core lemmas
s VERIFIED
c verification time: 0.041 seconds
=== n=20: drat-trim n20_k3_s5_c9.cnf proof_n20_c9.drat
exit 0 wall 0 s
c turning on binary mode checking
c parsing input formula with 1260 variables and 56306 clauses
c finished parsing, read 375564 bytes from proof file
c detected empty clause; start verification via backward checking
c 12958 of 56306 clauses in core
c 8822 of 8863 lemmas in core using 326671 resolution steps
c 0 RAT lemmas in core; 771 redundant literals in core lemmas
s VERIFIED
c verification time: 0.137 seconds
=== n=21: drat-trim n21_k3_s5_c10.cnf proof_n21_c10.drat
exit 0 wall 2 s
c turning on binary mode checking
c parsing input formula with 1960 variables and 124103 clauses
c finished parsing, read 2989068 bytes from proof file
c detected empty clause; start verification via backward checking
c 36576 of 124103 clauses in core
c 64754 of 65171 lemmas in core using 2003604 resolution steps
c 0 RAT lemmas in core; 5762 redundant literals in core lemmas
s VERIFIED
c verification time: 1.427 seconds
```

All five: 's VERIFIED', exit 0, no "trivial" or "empty clause in formula" message, 0 RAT lemmas.

Negative control (to show my drat-trim rejects a wrong pairing): proof_n17_c6.drat against n18_k3_s5_c7.cnf gives
`c conflict claimed, but not detected` / `s NOT VERIFIED`, exit 1; proof_n18_c7.drat against n17_k3_s5_c6.cnf gives
`c conflict claimed, but not detected` / `s NOT VERIFIED`, exit 1.

## Check 4: n = 22 proof regenerated with my CaDiCaL and checked

Command (as object/proof_n22_c11_not_shipped.txt prescribes, on my CNF whose sha256 is b5caefba...544adb):
`systemd-run --user --scope -q -p CPUQuota=100% nice -n 10 ./cadical -q --no-binary n22_k3_s5_c11.cnf n22.drat`

```
3.0.1
b5caefbad0996e1d8836998e01b134b50edb1a66c14dc3b589d91c87cd544adb  n22_k3_s5_c11.cnf
s UNSATISFIABLE
exit 20 wall 322 s
```

Proof file: `-rw-r--r-- ... 752653807 ... n22.drat`; `sha256sum n22.drat` gives
`d24a47fc195dbc48aa70d8fad7c970c18780a40ab878c08d8ce0a8e088af0c7b`.
Claimed: 752,653,807 bytes, sha256 d24a47fc195dbc48aa70d8fad7c970c18780a40ab878c08d8ce0a8e088af0c7b. Both match
exactly, so the solver run is deterministic across the author's machine and mine.

Check: `systemd-run --user --scope -q -p CPUQuota=100% nice -n 10 ./drat-trim n22_k3_s5_c11.cnf n22.drat`

```
c parsing input formula with 2904 variables and 251225 clauses
c finished parsing
c detected empty clause; start verification via backward checking
c 102310 of 251225 clauses in core
c 3226808 of 4971152 lemmas in core using 126983372 resolution steps
c 0 RAT lemmas in core; 2153746 redundant literals in core lemmas
s VERIFIED
c verification time: 303.451 seconds
exit 0 wall 304 s
warning lines: 0
```

The core counts (3,226,808 of 4,971,152 lemmas, 0 RAT) equal the ones claimed in object/proof_n22_c11_not_shipped.txt.
The 752 MB n22.drat was then deleted (`rm -f n22.drat`; a later `ls -la` of my work folder no longer shows it).

## Check 5: my own colouring checker

mycolcheck.py builds the 5-stable 3-subsets of [n] from the definition, then requires: every non-comment line has 4
integers and names a 5-stable 3-subset of [n]; no subset is listed twice; none is missing; colours lie in 0..n-11
(n - 10 colours); no two disjoint subsets share a colour (all pairs checked, not a sample).

Command: `python3 -I mycolcheck.py N object/colouring_nN_Mcolours.txt` for (N, M) = (17,7) ... (22,12):

```
n=17 listed=34 expected=34 missing=0 bad_lines=0 edges=374 conflicts=0 colours_allowed=7 colours_used=7 gives OK
n=18 listed=60 expected=60 missing=0 bad_lines=0 edges=1140 conflicts=0 colours_allowed=8 colours_used=8 gives OK
n=19 listed=95 expected=95 missing=0 bad_lines=0 edges=2850 conflicts=0 colours_allowed=9 colours_used=9 gives OK
n=20 listed=140 expected=140 missing=0 bad_lines=0 edges=6240 conflicts=0 colours_allowed=10 colours_used=10 gives OK
n=21 listed=196 expected=196 missing=0 bad_lines=0 edges=12390 conflicts=0 colours_allowed=11 colours_used=11 gives OK
n=22 listed=264 expected=264 missing=0 bad_lines=0 edges=22814 conflicts=0 colours_allowed=12 colours_used=12 gives OK
```

(each exit 0). Each file has exactly one comment line (`grep -c '^#'` = 1 for all six) and vertices + 1 lines in total.

Negative controls on edited copies of object/colouring_n17_7colours.txt: giving 1 6 11 the colour of the disjoint
vertex 2 7 12 gives `conflicts=3 ... gives FAIL`; deleting one vertex line gives `missing=1 ... gives FAIL`; colour 7 on one
line gives `bad: (2, 'colour out of range', '1 6 11 7')` gives FAIL. (A first attempt that changed a vertex with no
same-coloured disjoint neighbour correctly stayed OK.)

## Conclusion

- n = 17..22: my independently written generator reproduces all six CNF files byte for byte (sha256 match).
- The clique Q_j is a set of pairwise disjoint 5-stable 3-subsets for every n = 17..22, with min(t, C) units; the
  symmetry breaking is sound and of the permitted kind.
- n = 17..21: the shipped DRAT proofs give 's VERIFIED' under a drat-trim I built from the named commit, on my CNFs.
- n = 22: CaDiCaL 3.0.1, built from the tarball whose sha256 matches, reproduces the 752,653,807-byte proof with the
  exact claimed sha256 (exit 20), and drat-trim prints 's VERIFIED' with the claimed core counts.
- All six colourings are proper (n - 10)-colourings listing exactly the 5-stable 3-subsets of [n] once each.

Hence chi(KG(n,3)_{5-stab}) = n - 10 for n = 17..22, in particular chi(KG(17,3)_{5-stab}) = 7 and
chi(KG(22,3)_{5-stab}) = 12, as claimed. No mismatch, missing object or non-determinism found.

Minor notes (do not affect the result): the tools/ folder contains a stray compiled file
tools/__pycache__/gen_cnf.cpython-314.pyc (I did not run it or any author code); the tools/gen_cnf.py docstring cites
PREREG.md, which is not shipped. Whether n = 17 and n = 22 are open in the literature is outside this check.

pass: true
