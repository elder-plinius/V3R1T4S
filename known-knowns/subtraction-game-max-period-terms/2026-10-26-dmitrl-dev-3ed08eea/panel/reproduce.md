# A389690(23) = 3570: REPRODUCE skeptic

context: subagent (fresh context, Claude Science delegation)

Path key (added by the claimant on 2026-10-28 at the maintainer's request, PR #781 review): this review was run on the panel zip, whose layout differs from this package. Its code/A/ and code/B/ are how-we-built-it/A/ and how-we-built-it/B/ here (byte-identical). These panel inputs are not shipped: CLAIM.md and REPRODUCE.md (the claim summary and its commands; see README.md, RUN_IT_YOURSELF.md and how-we-built-it/BUILD.md), histogram_sg_23_A.txt, histogram_sg_23_B.txt and maximising_set.txt (objects/; object/A389690_23.txt holds the same maximising set and, as lines 10-682, the same 673 histogram lines, sha256 760aabce6a540d00660f1e4ab4a243b83a5d6e3640773d6497d67ea630bc00ac), the check helpers verify_oeis.py and sg_ref.py (code/check/), and a389690_2.txt (inputs/), the OEIS program https://oeis.org/A389690/a389690_2.txt (sha256 9fe51a4caa7f2d3f381c44fcb39b43c270c7bab12204e9cbf7e6e2c59999b61f). File references in the text were changed only to name these package paths, URLs or bare file names; no finding, number or verdict changed. Verbatim logs keep the zip's paths.

Role: REPRODUCE (kit/RUN.md step 6). Input: the claim package only (the panel zip, 21 entries). The network was used for the OEIS status check and the bank text.

Claim (CLAIM.md): "A389690(23) = 3570: over all 2^22 subtraction sets S with max S = 23, the longest eventual period of the Sprague-Grundy sequence is 3570, attained by exactly one set, S = {2, 3, 5, 7, 9, 10, 13, 14, 16, 18, 20, 21, 22, 23}."

Summary: I wrote two exhaustive checkers from the definition before reading the claimant's code (how-we-built-it/A and how-we-built-it/B). Both cover all 4194304 sets. Both give a maximum of 3570, attained by exactly one set, the claimed one. Both produce a 673-line period histogram that matches histogram_sg_23_A.txt and histogram_sg_23_B.txt line by line. The claim's own commands reproduce the saved objects byte for byte. The term is not in the OEIS entry, its b-file or its history. I found no mismatch, missing object or non-determinism.

## 1. Definition (quoted before reading any code)

- OEIS A389690 name, fetched as https://oeis.org/search?q=id:A389690&fmt=json at 2026-10-26T07:15:30Z UTC (HTTP 200): "Length of the longest possible eventual period of the Sprague-Grundy value of a subtraction game where the largest element of the subtraction set is n."
- Bank success criterion, from bank/targets.json at commit 8846324, fetched from https://raw.githubusercontent.com/elder-plinius/V3R1T4S/8846324/bank/targets.json at 2026-10-26T07:23:31Z UTC (HTTP 200). Its success_criterion matches the quote in CLAIM.md character for character: "S ranges over all subsets of {1, ..., n} that contain n; the period is the minimal eventual period, found as the first repeat of the length-n window of outcomes or Sprague-Grundy values".
- How I formalised it: S is a subset of {1..n} with n in S; g(0) = 0 and g(k) = mex{ g(k-s) : s in S, s <= k }; period(S) is the least p >= 1 with g(k+p) = g(k) for all large k; a(n) is the maximum of period(S) over the 2^(n-1) sets.
- My plain reference (ref.py) reproduces the entry's worked examples. For n = 3 it gives {1,2,3} -> 4, {2,3} -> 5, {1,3} -> 2 and {3} -> 6. For S = {1,4,10} it gives the sequence 0,1,0,1,2,0,1,0,1,2,3,2,3,0,1,3, then the block (0,1,0,1,2,0,1,2,0,1,2) repeating with period 11, as in the entry.

## 2. Own checkers (written before opening the claimant's code; kept outside the claim files)

1. sgper.c runs Brent cycle detection on the window state W_k = (g(k), ..., g(k+n-1)). The window is packed 5 bits per value into an unsigned __int128. There is no step cap. The histogram array has 2^20 slots plus an overflow counter.
2. sgdict.c uses a different algorithm, the literal first repeat of the length-n window. It computes values from the value array and stores windows in an open-addressing hash table, starting at k = n-1 (no padding). The period is k - q at the first repeat.
3. ref.py is a plain Python transcription of the definition: a dict of window tuples, with the period taken at the first repeat.

Compiler: Apple clang 21.0.0 (arm64), `cc -O2`; Python 3.11. Full sources and sha256 values are in the appendix.

## 3. Validation of the own checkers

- ref.py vs sgper.c: full period histograms identical (diff over all lines) for every n = 1..14. sgdict.c vs ref.py: identical for n = 1..14. sgdict.c vs sgper.c: identical for n = 15..22.
- Maxima for n = 1..22 from sgper.c: 2 4 6 8 10 12 22 25 28 58 54 87 114 144 189 336 306 456 728 1178 1180 4464. From sgdict.c: 2 4 6 8 10 12 22 25 28 58 54 87 114 144 189 336 306 456 728 1178 1180 4464. OEIS data field: 2 4 6 8 10 12 22 25 28 58 54 87 114 144 189 336 306 456 728 1178 1180 4464. All three lists are equal.
- For every n = 1..22, the first maximising set from sgper.c equals the first maximising set that program A prints (see the log in section 7).

## 4. Exhaustive n = 23 run and line-by-line histogram comparison

```
cc -O2 -o sgper sgper.c   && ./sgper 23 0 4194304 > c_23.txt     # 1 process, 7.4 s
cc -O2 -o sgdict sgdict.c && ./sgdict 23 0 4194304 > d_23.txt    # 1 process, 3.0 s
diff <(tail -n +2 c_23.txt) <(tail -n +3 objects/histogram_sg_23_A.txt)   # no output
diff <(tail -n +2 c_23.txt) <(tail -n +2 objects/histogram_sg_23_B.txt)   # no output
diff <(tail -n +2 d_23.txt) <(tail -n +2 c_23.txt)                              # no output
```

Header lines (verbatim):

```
n 23 lo 0 hi 4194304 total 4194304 max 3570 nmax 1 firstmaxmask 3846998 over 0 steps_total 458992481 steps_max 7665
n 23 lo 0 hi 4194304 total 4194304 max 3570 nmax 1 firstmaxmask 3846998 maxvalues 4605
```

- Both histograms have 673 lines of the form "period count", and the counts sum to 4194304 = 2^22. The first lines are 2 1526; 3 14853; 4 30810; 5 37891; 6 32827; the last lines are 1536 1; 1612 1; 1620 1; 1650 1; 2232 1; 3570 1.
- The sha256 of the 673 histogram lines (each ending in a newline) is 760aabce6a540d00660f1e4ab4a243b83a5d6e3640773d6497d67ea630bc00ac. It is the same for c_23.txt, d_23.txt, histogram_sg_23_A.txt (from line 3) and histogram_sg_23_B.txt (from line 2).
- Determinism: sgper was rerun as two halves in 2 parallel processes (masks [0, 2^21) and [2^21, 2^22)) and the halves were merged. The merged histogram is identical to the single run. The half maxima are 1650 (sets without move 22) and 3570 (sets with move 22).

## 5. The maximising set

- maximising_set.txt reads "n 23 / mask 3846998 / set 2 3 5 7 9 10 13 14 16 18 20 21 22 23 / period 3570". Recomputed from the set: the sum of 2^(s-1) over s < 23 is 3846998. Adding bit 22 for move 23 gives 8041302, which is the argmask in the header of histogram_sg_23_A.txt.
- sgper.c and sgdict.c both report firstmaxmask 3846998 and nmax 1, i.e. exactly one set has the maximum.
- ref.py gives period 3570 for this set. The first repeated window is g(1012..1034), and it recurs at g(4582..4604); 4605 values were computed. The preperiod is 1012. No proper divisor of 3570 is a period of g on [1012, 4605). The largest SG value is 13.
- The claim's copy of the OEIS program, a389690_2.txt, has the same sha256 (9fe51a4c...b61f) as https://oeis.org/A389690/a389690_2.txt fetched at 2026-10-26T07:17:25Z. Run through the claim's helper verify_oeis.py, it gives period 3570 and preperiod_start 1012.
- Over all sets, the longest prefix needed before the first window repeat is 4605 values (sgdict maxvalues), which is this set.

## 6. Proof steps re-derived

1. The window determines the future. For k >= n every s in S satisfies s <= k, so g(k) depends only on (g(k-n), ..., g(k-1)). Hence W_{k+1} = F(W_k) for all k >= 0, where W_k = (g(k), ..., g(k+n-1)).
2. The state space is finite. A mex over at most |S| values is at most |S| <= 23 < 32, so 5 bits per value are enough and the orbit of W_0 is eventually periodic.
3. The cycle length is the minimal eventual period. Let lambda be the cycle length of the orbit. Then g has eventual period lambda. Conversely, any eventual period q of g gives W_{k+q} = W_k for large k, so lambda divides q. The minimal eventual period is therefore lambda, which is also the distance of the first repeated length-n window (the criterion's wording).
4. Brent's algorithm returns exactly lambda. A tortoise = hare match can only occur once the tortoise is on the cycle, because a state off the cycle never recurs. On the cycle the first return takes exactly lambda steps, and power doubling ensures that eventually power >= lambda with the tortoise on the cycle. sgper.c, program A and program B have no step cap. sgdict.c's value-array limit of 65536 was not reached (the maximum used was 4605).
5. The search is exhaustive. Masks 0..2^22-1 were all enumerated, and the counts sum to 4194304 in all four histograms (sgper, sgdict, A, B).
6. Maximum and uniqueness. The last histogram line is "3570 1": no set has a longer period, and exactly one set has 3570. The next largest period is 2232.
7. a(23) = 3570 < a(22) = 4464 is not suspicious. No program caps the search by the previous term, and the listed terms already drop (a(11) < a(10), a(17) < a(16)).

## 7. The claim's REPRODUCE.md commands (run in a fresh copy of the claim files)

Log (verbatim; timings vary; the n = 1..22 lines have their timing suffix removed):

```
$ cc -O2 -o code/A/subper_a code/A/subper_a.c
(ok)
$ python3 code/A/run_a.py sg 23 2 out_A.txt
A sg 23 max 3570 set [2, 3, 5, 7, 9, 10, 13, 14, 16, 18, 20, 21, 22, 23] sets 4194304 periods 673 overflow 0 6.8s
$ python3 code/A/compare.py out_A.txt out_B.txt
{"max_A": 3570, "max_B": 3570, "set_A": [2, 3, 5, 7, 9, 10, 13, 14, 16, 18, 20, 21, 22, 23], "set_B": [2, 3, 5, 7, 9, 10, 13, 14, 16, 18, 20, 21, 22, 23], "max_equal": true, "set_equal": true, "hist_equal": true, "sets_A": 4194304, "sets_B": 4194304, "distinct_periods": 673}
$ python3 code/A/compare.py out_A.txt objects/histogram_sg_23_A.txt
{"max_A": 3570, "max_B": 3570, "set_A": [2, 3, 5, 7, 9, 10, 13, 14, 16, 18, 20, 21, 22, 23], "set_B": [2, 3, 5, 7, 9, 10, 13, 14, 16, 18, 20, 21, 22, 23], "max_equal": true, "set_equal": true, "hist_equal": true, "sets_A": 4194304, "sets_B": 4194304, "distinct_periods": 673}
$ python3 code/A/compare.py out_B.txt objects/histogram_sg_23_B.txt
{"max_A": 3570, "max_B": 3570, "set_A": [2, 3, 5, 7, 9, 10, 13, 14, 16, 18, 20, 21, 22, 23], "set_B": [2, 3, 5, 7, 9, 10, 13, 14, 16, 18, 20, 21, 22, 23], "max_equal": true, "set_equal": true, "hist_equal": true, "sets_A": 4194304, "sets_B": 4194304, "distinct_periods": 673}
$ cmp out_A.txt objects/histogram_sg_23_A.txt && cmp out_B.txt objects/histogram_sg_23_B.txt && cmp out_A_p1.txt objects/histogram_sg_23_A.txt && cmp out_B_t1.txt objects/histogram_sg_23_B.txt
(all four byte-identical)
$ shasum -a 256 out_A.txt out_A_p1.txt out_B.txt out_B_t1.txt objects/*.txt inputs/a389690_2.txt
39b1a00d71e154a3224d7e7ef88bb54a9ba742e9fdae9588ef662bee311ad68a  out_A.txt
39b1a00d71e154a3224d7e7ef88bb54a9ba742e9fdae9588ef662bee311ad68a  out_A_p1.txt
deea076cb4d0e6087957f61a11286c227fe93fd2d717cceec277552b69462b4b  out_B.txt
deea076cb4d0e6087957f61a11286c227fe93fd2d717cceec277552b69462b4b  out_B_t1.txt
39b1a00d71e154a3224d7e7ef88bb54a9ba742e9fdae9588ef662bee311ad68a  objects/histogram_sg_23_A.txt
deea076cb4d0e6087957f61a11286c227fe93fd2d717cceec277552b69462b4b  objects/histogram_sg_23_B.txt
5eb9b6efe05eabd3a01db9d9c9e8e89f13160b32996699446c3141cbf6e5900c  objects/maximising_set.txt
9fe51a4caa7f2d3f381c44fcb39b43c270c7bab12204e9cbf7e6e2c59999b61f  inputs/a389690_2.txt
$ python3 code/check/verify_oeis.py sg 2,3,5,7,9,10,13,14,16,18,20,21,22,23
mode sg n 23 S [2, 3, 5, 7, 9, 10, 13, 14, 16, 18, 20, 21, 22, 23] | OEIS program: period 3570 preperiod_start 1012 (0.0s) | sg_ref: period 3570 first window end 1034
$ for n in $(seq 1 22); do python3 code/A/run_a.py sg $n 1 /dev/null; done
A sg 1 max 2 set [1] sets 1 periods 1 overflow 0
A sg 2 max 4 set [2] sets 2 periods 2 overflow 0
A sg 3 max 6 set [3] sets 4 periods 4 overflow 0
A sg 4 max 8 set [4] sets 8 periods 5 overflow 0
A sg 5 max 10 set [5] sets 16 periods 8 overflow 0
A sg 6 max 12 set [6] sets 32 periods 8 overflow 0
A sg 7 max 22 set [2, 5, 7] sets 64 periods 13 overflow 0
A sg 8 max 25 set [1, 4, 7, 8] sets 128 periods 15 overflow 0
A sg 9 max 28 set [2, 3, 6, 7, 9] sets 256 periods 18 overflow 0
A sg 10 max 58 set [2, 3, 6, 7, 9, 10] sets 512 periods 25 overflow 0
A sg 11 max 54 set [3, 8, 11] sets 1024 periods 35 overflow 0
A sg 12 max 87 set [2, 3, 5, 6, 7, 9, 12] sets 2048 periods 44 overflow 0
A sg 13 max 114 set [2, 3, 6, 7, 10, 13] sets 4096 periods 57 overflow 0
A sg 14 max 144 set [3, 4, 5, 9, 10, 11, 12, 14] sets 8192 periods 85 overflow 0
A sg 15 max 189 set [3, 4, 8, 10, 11, 12, 15] sets 16384 periods 99 overflow 0
A sg 16 max 336 set [3, 4, 5, 7, 9, 11, 12, 16] sets 32768 periods 133 overflow 0
A sg 17 max 306 set [2, 3, 4, 7, 8, 10, 13, 14, 16, 17] sets 65536 periods 153 overflow 0
A sg 18 max 456 set [3, 4, 6, 7, 11, 12, 14, 18] sets 131072 periods 195 overflow 0
A sg 19 max 728 set [2, 3, 8, 10, 12, 16, 17, 19] sets 262144 periods 263 overflow 0
A sg 20 max 1178 set [2, 3, 5, 7, 8, 9, 11, 13, 15, 18, 20] sets 524288 periods 340 overflow 0
A sg 21 max 1180 set [2, 5, 7, 13, 16, 18, 20, 21] sets 1048576 periods 424 overflow 0
A sg 22 max 4464 set [2, 3, 5, 6, 9, 13, 16, 17, 19, 20, 22] sets 2097152 periods 530 overflow 0
```

Program B: Rust was not preinstalled, so cargo 1.99.1 and rustc 1.99.1 came from conda-forge. `(cd how-we-built-it/B && cargo build --release --offline -j 2)` finished with "Finished `release` profile [optimized]". Then `how-we-built-it/B/target/release/subper_b sg 23 2 > out_B.txt` (7.0 s) and `how-we-built-it/B/target/release/subper_b sg 23 1 > out_B_t1.txt` (10.2 s) were run. Both outputs are byte-identical to histogram_sg_23_B.txt (see the cmp and shasum lines above).

Process/thread counts of 2 and 1 replaced REPRODUCE.md's 4, because of the panel's 2-process limit. For both programs and both counts the output is byte-identical to the saved object, so the result does not depend on the count.

## 8. Saved-file integrity

- The sha256 values of maximising_set.txt, histogram_sg_23_A.txt and histogram_sg_23_B.txt equal those in CLAIM.md.
- Every file named under Files in CLAIM.md is present in the panel zip. verify_oeis.py mentions a389689_1.txt, but only in its wl branch. That file is absent, and this sg claim does not need it.
- Program A (Brent on the packed window, values computed from the window) and program B (hash map of oldest-first windows, values from the array) share no code. They agree with each other: compare.py reports max_equal, set_equal and hist_equal as true. Both also agree with my two checkers.

## 9. OEIS status at verification time (property 3)

- Entry, from the JSON fetched at 07:15:30Z: data 2,4,6,8,10,12,22,25,28,58,54,87,114,144,189,336,306,456,728,1178,1180,4464 (22 terms, n = 1..22), keyword nonn,more, revision 36 (2025-10-26). There is no term for n = 23. The entry HTML fetched at 07:15:29Z does not contain the string 3570.
- The b-file https://oeis.org/A389690/b389690.txt (07:17:23Z, HTTP 200, 183 bytes) is synthesized from the entry and lists n = 1..22. Its sha256 a0fc3d77b3ef73421b37232cc8d9071031a7eddaf9f5d6f3ce5b0c6fa418a2b8 equals the value recorded in CLAIM.md.
- History: https://oeis.org/history?seq=A389690 plus &start=10, &start=20 and &start=30 (07:17:24Z to 07:17:45Z, HTTP 200) show revisions #36 down to #1, all present. The string 3570 occurs on none of these pages.
- The recorded sha256 values of the entry and history HTML cannot be re-matched. Two fetches of the entry 3 s apart (07:22:15Z and 07:22:18Z) already differ, and only in per-request Cloudflare tokens. This is expected and is not a content mismatch.

## 10. Deviations and limits

- Process/thread counts of 2 and 1 replaced 4 (section 7); the outputs are byte-identical.
- The Rust toolchain came from conda-forge, and the build used `--offline -j 2`.
- The sha256 values of the entry and history HTML are not reproducible, because the pages are dynamic. The b-file hash matched, and the content checks were done on my own fetches.
- Not run: the OEIS Mathematica program, and the OEIS Python program's exhaustive loop at n = 23. Only that program's period function was run, on the maximising set.
- No sampling: both of my checkers covered all 4194304 sets.

## Verdict

My own exhaustive computations confirm the claimed value 3570, the maximising set and its uniqueness, and the full 673-line histogram in both saved objects. The claim's commands reproduce the saved objects byte for byte. The term is absent from the OEIS entry, its b-file and its history as of 2026-10-26T07:17Z.

## Appendix: own checker sources

sgper.c (sha256 24932a298a2fd819151fba8be1047b377e0f5ca8b3428458dea64c568a425499)

```c
/* Independent checker (REPRODUCE skeptic), written from the definition only.
 * For every S subset of {1..n} with n in S (mask bit i <-> move i+1, i = 0..n-2; move n always present):
 *   g(k) = mex{ g(k-s) : s in S, s <= k },  k = 0, 1, 2, ...
 * The state W_k = (g(k), ..., g(k+n-1)) determines W_{k+1} (all s <= n <= k+n), so the orbit
 * W_0, W_1, ... is eventually periodic and its cycle length is the minimal eventual period of g.
 * The cycle length is found exactly with Brent's algorithm (no step cap).
 * Window packing: 5 bits per value (mex <= |S| <= n <= 23 < 32), most recent value in the low bits,
 * so g(k+n-s) sits in field s-1 of W_k.
 * Usage: sgper n lo hi  -> histogram over masks lo <= m < hi.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

typedef unsigned __int128 u128;
#define CAP (1u << 20)

static uint64_t steps_total = 0, steps_max = 0;

static uint64_t period_of(int n, uint32_t mask, uint64_t *steps_out) {
    int S[32], cnt = 0;
    for (int i = 0; i < n - 1; i++) if (mask >> i & 1u) S[cnt++] = i + 1;
    S[cnt++] = n;
    /* first n values directly from the definition */
    unsigned g[32];
    for (int k = 0; k < n; k++) {
        uint32_t seen = 0;
        for (int j = 0; j < cnt; j++) if (S[j] <= k) seen |= 1u << g[k - S[j]];
        g[k] = (unsigned)__builtin_ctz(~seen);
    }
    u128 wmask = (((u128)1) << (5 * n)) - 1;
    u128 w0 = 0;
    for (int k = 0; k < n; k++) w0 = (w0 << 5) | g[k];
    int sh[32];
    for (int j = 0; j < cnt; j++) sh[j] = 5 * (S[j] - 1);
#define STEP(w) do { uint32_t seen_ = 0; \
        for (int j_ = 0; j_ < cnt; j_++) seen_ |= 1u << (unsigned)((w >> sh[j_]) & 31u); \
        w = ((w << 5) | (u128)(unsigned)__builtin_ctz(~seen_)) & wmask; } while (0)
    u128 tort = w0, hare = w0;
    STEP(hare);
    uint64_t power = 1, lam = 1, steps = 1;
    while (tort != hare) {
        if (power == lam) { tort = hare; power <<= 1; lam = 0; }
        STEP(hare); lam++; steps++;
    }
    *steps_out = steps;
    return lam;
}

int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage: %s n lo hi\n", argv[0]); return 2; }
    int n = atoi(argv[1]);
    uint64_t lo = strtoull(argv[2], 0, 10), hi = strtoull(argv[3], 0, 10);
    if (n < 1 || n > 24 || hi > (1ull << (n - 1)) || lo > hi) { fprintf(stderr, "bad args\n"); return 2; }
    uint64_t *hist = calloc(CAP, sizeof(uint64_t));
    uint64_t over = 0, best = 0, nbest = 0, total = 0; uint32_t bestmask = 0;
    for (uint64_t m = lo; m < hi; m++) {
        uint64_t st;
        uint64_t p = period_of(n, (uint32_t)m, &st);
        steps_total += st; if (st > steps_max) steps_max = st;
        if (p < CAP) hist[p]++; else { over++; fprintf(stderr, "period>=CAP mask %llu p %llu\n", (unsigned long long)m, (unsigned long long)p); }
        if (p > best) { best = p; nbest = 1; bestmask = (uint32_t)m; }
        else if (p == best) nbest++;
        total++;
    }
    printf("n %d lo %llu hi %llu total %llu max %llu nmax %llu firstmaxmask %u over %llu steps_total %llu steps_max %llu\n",
           n, (unsigned long long)lo, (unsigned long long)hi, (unsigned long long)total, (unsigned long long)best,
           (unsigned long long)nbest, bestmask, (unsigned long long)over,
           (unsigned long long)steps_total, (unsigned long long)steps_max);
    for (uint64_t p = 0; p < CAP; p++) if (hist[p]) printf("%llu %llu\n", (unsigned long long)p, (unsigned long long)hist[p]);
    return 0;
}
```

sgdict.c (sha256 19c6643e81d248b15a97b6c7c3a977aa56c6af77b93a2b8462dab8f20bf23405)

```c
/* Second own exhaustive checker (REPRODUCE skeptic), different algorithm from sgper.c:
 * literal first repeat of the length-n window. Values are computed from the value array
 * g(k) = mex{ g(k-s) : s in S, s <= k }; windows (g(k-n+1..k)) for k >= n-1 are stored in an
 * open-addressing hash table with their end index; at the first k whose window was seen at q,
 * the period is k - q. Usage: sgdict n lo hi */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef unsigned __int128 u128;
#define TB 17
#define TSZ (1u << TB)
#define LMAX (1u << 16)
static u128 key[TSZ]; static uint32_t idx[TSZ], gen[TSZ]; static uint32_t curgen = 0;
static unsigned char g[LMAX];
static inline uint32_t hsh(u128 k) {
    uint64_t a = (uint64_t)k, b = (uint64_t)(k >> 64);
    uint64_t h = a * 0x9E3779B97F4A7C15ull ^ (b + 0x632BE59BD9B4E019ull) * 0xC2B2AE3D27D4EB4Full;
    h ^= h >> 29; h *= 0xBF58476D1CE4E5B9ull; h ^= h >> 32;
    return (uint32_t)(h >> (64 - TB));
}
static uint64_t period_of(int n, uint32_t mask, uint64_t *len) {
    int S[32], cnt = 0;
    for (int i = 0; i < n - 1; i++) if (mask >> i & 1u) S[cnt++] = i + 1;
    S[cnt++] = n;
    curgen++;
    u128 w = 0, wm = (((u128)1) << (5 * n)) - 1;
    for (uint32_t k = 0;; k++) {
        if (k >= LMAX) { fprintf(stderr, "LMAX exceeded mask %u\n", mask); exit(4); }
        uint32_t seen = 0;
        for (int j = 0; j < cnt; j++) if ((uint32_t)S[j] <= k) seen |= 1u << g[k - S[j]];
        unsigned v = (unsigned)__builtin_ctz(~seen);
        if (v > 31) { fprintf(stderr, "value overflow\n"); exit(5); }
        g[k] = (unsigned char)v;
        w = ((w << 5) | v) & wm;
        if (k + 1 >= (uint32_t)n) {
            uint32_t h = hsh(w);
            while (gen[h] == curgen) {
                if (key[h] == w) { *len = k + 1; return k - idx[h]; }
                h = (h + 1) & (TSZ - 1);
            }
            gen[h] = curgen; key[h] = w; idx[h] = k;
        }
    }
}
int main(int argc, char **argv) {
    int n = atoi(argv[1]);
    uint64_t lo = strtoull(argv[2], 0, 10), hi = strtoull(argv[3], 0, 10);
    if (n < 1 || n > 24 || hi > (1ull << (n - 1))) return 2;
    static uint64_t hist[LMAX];
    uint64_t best = 0, nbest = 0, total = 0, lenmax = 0; uint32_t bm = 0;
    for (uint64_t m = lo; m < hi; m++) {
        uint64_t L; uint64_t p = period_of(n, (uint32_t)m, &L);
        if (L > lenmax) lenmax = L;
        hist[p]++; total++;
        if (p > best) { best = p; nbest = 1; bm = (uint32_t)m; } else if (p == best) nbest++;
    }
    printf("n %d lo %llu hi %llu total %llu max %llu nmax %llu firstmaxmask %u maxvalues %llu\n", n,
           (unsigned long long)lo, (unsigned long long)hi, (unsigned long long)total, (unsigned long long)best,
           (unsigned long long)nbest, bm, (unsigned long long)lenmax);
    for (uint32_t p = 0; p < LMAX; p++) if (hist[p]) printf("%u %llu\n", p, (unsigned long long)hist[p]);
    return 0;
}
```

ref.py (sha256 ed5bb63089f15857ac74f04c863836c8e62565ce887b0bcea713a482e3965be2)

```python
"""Plain reference from the definition (REPRODUCE skeptic): g(k) = mex{g(k-s): s in S, s <= k};
period = distance between the first repeated length-n window (dictionary of all windows seen)."""
import sys
from collections import Counter

def sg_period(S, n):
    g = []
    seen = {}
    k = 0
    while True:
        vals = {g[k - s] for s in S if s <= k}
        m = 0
        while m in vals:
            m += 1
        g.append(m)
        k += 1
        if k >= n:
            w = tuple(g[k - n:k])
            if w in seen:
                return k - seen[w], seen[w] - n, g   # period, preperiod start index of window, sequence
            seen[w] = k

def hist(n):
    H = Counter()
    for mask in range(1 << (n - 1)):
        S = [i + 1 for i in range(n - 1) if mask >> i & 1] + [n]
        p, _, _ = sg_period(S, n)
        H[p] += 1
    return H

if __name__ == "__main__":
    if sys.argv[1] == "ex":
        for S in ([1, 2, 3], [2, 3], [1, 3], [3]):
            print(S, sg_period(S, 3)[0])
        p, mu, g = sg_period([1, 4, 10], 10)
        print("{1,4,10} period", p, "first 40:", g[:40])
    else:
        n = int(sys.argv[1])
        H = hist(n)
        print("n", n, "total", sum(H.values()), "max", max(H))
        for p in sorted(H):
            print(p, H[p])
```

pass: true
