# Reproduce skeptic: SM census rows Q_max 39 and 40

Scope: I read only claim/ (CLAIM.md, REPRODUCE.md, status.md, object/counts.txt, object/receipts/, source/,
checker/). All work, code and outputs are in panel_work/reproduce/. Every number below was copied from a saved
output file there; the file is named in brackets. Run window: 09:40 to 10:02 UTC on 2026-11-08.

## 1. My own checker and counters (written from CLAIM.md before I read source/ or checker/)

- `mycheck.c` is a strict streaming checker. It requires exactly 15 integers per line, separated by single
  spaces, with a "\n" line end and no leading zeros or "-0". It also checks: |F| <= Q_max; all six SM ACCs (the
  hypercharge one multiplied by 6); each species non-decreasing; F >= canon(-F) lexicographically, where canon(-F)
  is each species negated and re-sorted; gcd 1; nonzero; lines strictly increasing. Its count is lines + 1.
  - Negative tests [negtests_mycheck.txt]: it rejects a duplicate line, swapped lines, a zero line, a line replaced
    by its negation, a doubled line, a perturbed line (ACC), a doubled primitive line (gcd), a double space and a
    missing final newline.
- `orbcount.c` is an independent counter that uses no canonical forms. It counts all multiset tuples (zero and
  non-primitive included) with a hash join of (Q,u) against (d,L,e) for each value of the species sum s, which the
  linear ACCs fix as (s,-4s,2s,-3s,6s). Burnside for the overall sign uses the sign-fixed tuples {-a,0,a}. A
  Moebius sum over the gcd gives the primitive count. Run with 2 threads.
  - Caveat: after reading mitm.c, I found it uses the same mathematics (multisets + Burnside + Moebius). My code is
    separate and uses a different split (mitm.c uses (Q,L,nu)|(u,d,e)), so orbcount is independent code but not an
    independent method from mitm.c. It is independent in method from the lister.
- `direct.c` is a second counter in a different style: no join, no Burnside, no Moebius. It enumerates the Q, u,
  d and L multisets and solves for the e multiset, whose power sums 1 to 3 the ACCs fix. It then tests each
  solution explicitly for nonzero, gcd 1 and sign-canonical form. Its cost grows like Q^9, so it covers only
  Q_max <= 20 (calibration).

Calibration against the published SM values for Q_max 1..10 (8 22 82 251 626 1983 3902 7068 14354 23800):
- mycheck, run on acclist output: lines + 1 = 8 22 82 251 626 1983 3902 7068 14354 23800, all PASS
  [calib_mycheck_1_10.txt].
- orbcount: 8 22 82 251 626 1983 3902 7068 14354 23800 [calib_orbcount_1_10.txt].
- direct: 8 22 82 251 626 1983 3902 7068 14354 23800 [calib_direct_1_10.txt].
- Small rows:
  - Q 12: direct 67968 = mycheck 67968 [direct_12.txt, calib_mycheck_12.txt].
  - Q 16: direct 310691 = mycheck 310691 [direct_16.txt, calib_mycheck_16.txt].
  - Q 20: direct 1071441 = orbcount 1071441 = mitm.c 1071441 = acclist list (1071440 lines, PASS from both
    checkers, sha256 f8e2ce35...e770 as in REPRODUCE.md) [direct_20.txt, orbcount_20.txt, mitm_SM_1_10_20.txt,
    sm20.*].

## 2. Full regeneration of both lists (REPRODUCE.md), streamed and never stored

Commands:
```
gcc -O2 -o acclist claim/source/acclist.c; gcc -O2 -o checklist claim/checker/checklist.c
gcc -O3 -o mitm claim/source/mitm.c; gcc -O2 -o mycheck mycheck.c
./run_row.sh 39 & ./run_row.sh 40 &   # run in parallel
```
What `run_row.sh q` does, with `set -o pipefail`:
- `./acclist q 0 2> smq.lister.log | tee fifo.sha fifo.chk fifo.my > fifo.wc`
- The four FIFOs feed `sha256sum`, `./checklist q 0`, `./mycheck q` and `wc -l`. All four read the same bytes.
- It records PIPESTATUS and the exit status of each consumer.

Background PIDs are in panel_work/reproduce/pids.txt. All of these jobs exited on their own and none was killed.

| row | lister exit | lines (wc) | claim checklist | my checker | sha256 (regenerated) | claimed (object/counts.txt) |
|---|---|---|---|---|---|---|
| SM 39 | 0 (tee 0), DONE count=51237624, 931 s | 51237624 | valid 51237624, PASS | lines 51237624, count 51237625, PASS | 0ec7c2c03acf589cbce61249d265f7352db69f43ebaaeee3d1bcc74c6f348743 | 51237625 / 51237624 / same hash |
| SM 40 | 0 (tee 0), DONE count=58626333, 1127 s | 58626333 | valid 58626333, PASS | lines 58626333, count 58626334, PASS | 8d83e4182d630423ce5fa25512de702d30cb1889af96bdeaea001ebf7e673694 | 58626334 / 58626333 / same hash |

Sources: [sm39.*, sm40.*, summary_rows.txt]. For each row, sha256 and line count are equal to object/counts.txt,
and count = lines + 1. Both checkers exited 0.

Python checker on the 200000-line head of a fresh stream [pysample_39_40.txt]:
- PASS for both rows; mycheck also PASS.
- Sample sha256 for SM 39: d57a1f61...497f. For SM 40: e5ab38b3...3530. Both equal the claim's receipts.

## 3. Independent counts

- mitm.c, published range [mitm_SM_1_10_20.txt]: 8 22 82 251 626 1983 3902 7068 14354 23800 (all match).
- mitm.c, Q 39 [mitm_SM_39.txt]: RESULT 51237625. Intermediate values: N(39) = 104332520, Fix = 35868.
- mitm.c, Q 40 [mitm_SM_40.txt]: RESULT 58626334. Intermediate values: N(40) = 119628509, Fix = 38069.
- My orbcount [orbcount_39.txt, orbcount_40.txt]: COUNT SM 39 = 51237625 and COUNT SM 40 = 58626334.
  - For every bound used, its N_ms and N_sym equal mitm.c's N and Fix: 39, 19, 13, 7, 6, 5, 3, 2, 1 and 40, 20,
    13, 8, 6, 5, 4, 3, 2, 1.
  - The Burnside parity check passed.

Three routes agree on each row:
- the canonical list (acclist, two checkers, sha256);
- the claim's counter (mitm.c);
- my own counter (orbcount).

## 4. Source review: is the convention the one CLAIM.md states?

- acclist.c, mode 0:
  - Species are sorted triples, so family permutations within each species are quotiented.
  - The linear ACCs fix the sums. Half A = (Q,u,d) is matched to half B = (L,e) on the key (quadratic, cubic) by
    binary search in a sorted block. Each key packs `quad*2^32 + cub`; |cub| < 2^31 at Q 40, so keys are unique.
  - The sign representative is kept iff F >= canon(-F). The comparison is decided at the first species whose
    triple differs from its negation (`tcmp`), which is the same as the full lexicographic comparison.
    Self-conjugate solutions are kept once.
  - The zero solution (g = 0) and gcd > 1 are skipped. The +1 for zero is added outside, as count = lines + 1.
  - Output order is the lexicographic order of triple indices, which equals the lexicographic order of tuples.
    Both checkers confirmed it.
- mitm.c:
  - It counts all multiset tuples and applies Moebius over the gcd to get primitive tuples.
  - Burnside for the sign uses the sign-fixed tuples {-a,0,a} under the quadratic ACC.
  - It returns 1 + (P + Fx)/2, which is the same convention.
- Both programs implement the convention stated in CLAIM.md: inequivalence under family permutations within each
  species and the overall sign, primitive, nonzero, plus one for the zero assignment.

Minor remarks (none affects the result):
- checklist.c and check_list.py skip blank lines and accept any whitespace. Format strictness rests on the sha256
  and on mycheck, which is strict and passed.
- acclist's `putint` handles |F| <= 99 and refuses Q > 99. That is fine for these rows.
- mitm.c is not independent in method from a Burnside count. Its independence is from the lister.

## Anything wrong in the claim

I found nothing wrong. The stated runtimes (~15 and ~18 min) match what I saw (931 s and 1127 s, run in
parallel). The receipts (hashes, sample hashes, mitm results) match my regenerated outputs.

context: subagent (fresh context, Claude Code Agent tool)
pass: true
