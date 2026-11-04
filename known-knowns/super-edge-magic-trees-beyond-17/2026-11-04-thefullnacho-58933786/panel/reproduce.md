# Reproduce skeptic report

context: subagent (Claude Code Agent tool, fresh context, saw only claim/)

## Definition checked against (quoted from CLAIM.md)
"for each n in 18..22, the file object/cert_nN.txt(.xz), N = 18..22 gives every unlabeled tree on n vertices (A000055(n) of them:
123867, 317955, 823065, 2144505, 5623756) with a bijection from its vertices to {1..n} whose n-1 edge sums are
consecutive integers"

## Own checker (written before opening checkers/)
File: panel/reproduce-work/mycheck.py (python3 standard library, run with nice -n 19, at most 2 processes).
For EVERY line of all five files (no sampling; n21/n22 read through lzma):
- first field equals n; exactly n-1 edges; endpoints in 0..n-1, no self-loops, no repeated edge; connected by DFS
  (n-1 edges + connected = tree);
- labels: sorted list equals [1..n] (bijection);
- edge sums: sorted sums strictly consecutive (distinct, step 1);
- canonical form: centres by leaf peeling, AHU parenthesis code rooted at each centre, minimum over centres, packed
  exactly into a 2n-bit integer (no hashing); sorted and checked for adjacent duplicates;
- line count and distinct count must both equal A000055(n), computed by me from the A000081 recurrence and Otter's
  formula (not the b-file).
Counts computed: n=18..22 -> 123867, 317955, 823065, 2144505, 5623756 (match the claim).

Self-tests before trusting it:
- brute force over all Pruefer sequences, n=3..9: distinct canonical classes = Otter count (1,2,3,6,11,23,47) for every n.
- four injected defects in copies of cert_n18 (swapped two labels; an isomorphic relabelled copy replacing another
  line; last line dropped; label 18 replaced by 19): all four reported FAIL with the right reason
  (sums not consecutive / iso_duplicates=1 / lines=123866 / labels not bijection).

Exact output lines of my checker:
n=18 file=object/cert_n18.txt lines=123867 invalid=0 first_invalid=None iso_duplicates=0 distinct=123867 A000055=123867 -> OK
n=19 file=object/cert_n19.txt lines=317955 invalid=0 first_invalid=None iso_duplicates=0 distinct=317955 A000055=317955 -> OK
n=20 file=object/cert_n20.txt lines=823065 invalid=0 first_invalid=None iso_duplicates=0 distinct=823065 A000055=823065 -> OK
n=21 file=object/cert_n21.txt.xz lines=2144505 invalid=0 first_invalid=None iso_duplicates=0 distinct=2144505 A000055=2144505 -> OK
n=22 file=object/cert_n22.txt.xz lines=5623756 invalid=0 first_invalid=None iso_duplicates=0 distinct=5623756 A000055=5623756 -> OK
(n=18 run twice with identical output; deterministic.)

Completeness: each file holds A000055(n) pairwise non-isomorphic trees on n vertices, and there are exactly A000055(n)
isomorphism classes, so every class appears exactly once (pigeonhole). I did not write my own tree generator (no
nauty on this machine); one-to-one regeneration was confirmed only by the author's WROM generator below.

## Hashes
sha256sum -c object/certificates.sha256: cert_n18.txt, cert_n19.txt, cert_n20.txt, cert_n21.txt.xz, cert_n22.txt.xz all OK.

## Author's commands (REPRODUCE.md)
Run from claim/ as written, except the `work/` decompression target was put in panel/reproduce-work/work/ (not inside
claim/) and deleted afterwards.
n=18 lines=123867 distinct=123867 A000055(Otter)=123867 malformed=0 wrong_n=0 not_tree=0 bad_label=0 dup=0 regenerated=123867 missing=0 extra=0 -> PASS
n=19 lines=317955 distinct=317955 A000055(Otter)=317955 malformed=0 wrong_n=0 not_tree=0 bad_label=0 dup=0 regenerated=317955 missing=0 extra=0 -> PASS
n=20 lines=823065 distinct=823065 A000055(Otter)=823065 malformed=0 wrong_n=0 not_tree=0 bad_label=0 dup=0 regenerated=823065 missing=0 extra=0 -> PASS
n=21 lines=2144505 distinct=2144505 A000055(Otter)=2144505 malformed=0 wrong_n=0 not_tree=0 bad_label=0 dup=0 regenerated=2144505 missing=0 extra=0 -> PASS
n=22 lines=5623756 distinct=5623756 A000055(Otter)=5623756 malformed=0 wrong_n=0 not_tree=0 bad_label=0 dup=0 regenerated=5623756 missing=0 extra=0 -> PASS
n=18 lines=123867 distinct_canonical=123867 A000055=123867 not_tree=0 wrong_n=0 dup=0 unlabeled=0 label_failures=0 -> PASS
n=19 lines=317955 distinct_canonical=317955 A000055=317955 not_tree=0 wrong_n=0 dup=0 unlabeled=0 label_failures=0 -> PASS
n=20 lines=823065 distinct_canonical=823065 A000055=823065 not_tree=0 wrong_n=0 dup=0 unlabeled=0 label_failures=0 -> PASS
n=21 lines=2144505 distinct_canonical=2144505 A000055=2144505 not_tree=0 wrong_n=0 dup=0 unlabeled=0 label_failures=0 -> PASS
n=22 lines=5623756 distinct_canonical=5623756 A000055=5623756 not_tree=0 wrong_n=0 dup=0 unlabeled=0 label_failures=0 -> PASS
All exit codes 0. Agrees with my checker on every count.

## Mismatches
None.

## Scope notes (not grounds for fail in this role)
- Orders up to 17 rest on the cited Lee-Shan computation; I did not check that citation or the novelty record (record/
  not reviewed by me).
- Independent regeneration came from the author's checker only; my own completeness argument is the count + pairwise
  non-isomorphism pigeonhole, with my own canonical form and my own A000055 computation.

edit: the n-in-angle-brackets notation replaced at the main session's request; no finding changed
pass: true
