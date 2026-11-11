# REPRODUCE skeptic report

context: subagent (Claude Code Agent tool, fresh context, saw only claim/)

## Definition checked against (quoted from CLAIM.md)
"for each n in 18..25, the file object/cert_nN.txt or object/cert_nN.txt.xz (N = n) gives every unlabeled tree on n
vertices (A000055(n) of them: 123867, 317955, 823065, 2144505, 5623756, 14828074, 39299897, 104636890) with a
bijection from its vertices to {1..n} whose n-1 edge sums are consecutive integers"
Format: "One line per tree: n;u-v,u-v,...;l0,l1,...,l(n-1)[;extra fields]. Vertices are 0..n-1 ... li is the label of vertex i."

## Own checker (written before opening checkers/): reproduce-work/sem_check.py (python3 stdlib, run under nice -n 19)
Per line, every line of every file (xz read with the lzma module, streamed): first field == n; exactly n-1 edges,
endpoints in 0..n-1, no loops, no repeated edge, connected (hence a tree); exactly n labels, sorted == [1..n];
the n-1 sums l(u)+l(v) pairwise distinct with max-min == n-2 (n-1 consecutive integers).
Canonical form: centre(s) by leaf peeling, AHU parenthesis code rooted at the centre; bicentral = sorted pair of the
two half-codes, with a distinct key length so the two cases cannot collide; packed exactly (no hashing) into a 64-bit int.
Distinctness in bounded memory: keys spilled to 8 bucket files by a hash of the key, each bucket deduplicated
separately with an exact set, per-bucket counts summed (peak well under 8 GB).
A000055(n) computed in-script: A000081 recurrence + Otter's formula (not the b-file); values for n=1..25 printed and
match 1,1,1,2,3,6,11,23,47,106,... and the claimed counts.
Pass condition: invalid == 0, lines == A000055(n), distinct canonical keys == lines. Equal-count distinct trees on n
vertices means every isomorphism class appears exactly once.

Self-tests: canonical form run over every labeled tree (all Prufer sequences) for n = 3..9: distinct keys equal
A000055(n) for each n (so isomorphic trees get one key and non-isomorphic trees different keys).
Injected defects on a copy of the n=18 file, every one reported FAIL: swapped labels (edge sums not consecutive),
duplicated line, isomorphic relabelled copy carrying a valid labeling (distinct 123866), dropped line, extra line,
label out of range, repeated edge, cycle + isolated vertex (not connected), wrong n field, and the isomorphic copy
again via an xz file; the unmodified file via xz reported OK.

## Own checker output, exact lines, all n (full files, no sampling)
n=18 lines=123867 invalid=0 distinct_canonical=123867 A000055=123867 -> OK
n=19 lines=317955 invalid=0 distinct_canonical=317955 A000055=317955 -> OK
n=20 lines=823065 invalid=0 distinct_canonical=823065 A000055=823065 -> OK
n=21 lines=2144505 invalid=0 distinct_canonical=2144505 A000055=2144505 -> OK
n=22 lines=5623756 invalid=0 distinct_canonical=5623756 A000055=5623756 -> OK
n=23 lines=14828074 invalid=0 distinct_canonical=14828074 A000055=14828074 -> OK
n=24 lines=39299897 invalid=0 distinct_canonical=39299897 A000055=39299897 -> OK
n=25 lines=104636890 invalid=0 distinct_canonical=104636890 A000055=104636890 -> OK
(n=18 was run twice on the file, with 4 and with 8 buckets, plus once from an xz copy: identical counts each time.)

## Hashes (sha256sum -c certificates.sha256, run from inside object/)
cert_n18.txt: OK / cert_n19.txt: OK / cert_n20.txt: OK / cert_n21.txt.xz: OK / cert_n22.txt.xz: OK /
cert_n23.txt.xz: OK / cert_n24.txt.xz: OK / cert_n25.txt.xz: OK
Note: object/cert_n23..25.txt.xz are symlinks to files outside claim/; the hashes verify their content. The n=25
file's mtime is the day of review (later than the run id); no process other than my reader had it open, and its hash
matches certificates.sha256.

## Author's commands (REPRODUCE.md), run after my checker
checkers/indep_check.py --regen and checkers/verify_sem_coverage.py, n = 18..23 (both), n = 24 (coverage only):
n=18..23 indep_check: lines = distinct = A000055(Otter) = regenerated, malformed/wrong_n/not_tree/bad_label/dup = 0,
missing=0 extra=0 -> PASS for every n (e.g. n=23 lines=14828074 ... regenerated=14828074 missing=0 extra=0 -> PASS).
n=18..24 verify_sem_coverage: distinct_canonical = A000055 = lines, all failure counters 0 -> PASS for every n
(n=24: 39299897, 898.56 s, 3.5 GB peak).
Not run: author's n=24 indep_check (another panel member was running it at the time) and both author checkers at
n=25 (~11.5 GB each; free memory with the other skeptic's job did not leave safe headroom). My own full check
above is what decides n=24 and n=25.
All author results agree with mine. No mismatch found.

## Scope notes
I verified the certificate (criterion (a) object): every tree on 18..25 vertices appears exactly once with a valid
super edge-magic labeling. I did not assess the DS6 literature-bound statement (record/), which is outside this role.
Files: reproduce-work/sem_check.py, reproduce-work/test_canon.py, reproduce-work/make_defects.py, logs out_*.log,
author_out.log in reproduce-work/.

pass: true
