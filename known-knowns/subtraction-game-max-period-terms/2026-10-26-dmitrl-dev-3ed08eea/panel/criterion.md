# CRITERION skeptic: A389690(23) = 3570 (target `subtraction-game-max-period-terms`)

context: subagent (fresh context, Claude Science delegation)

Path key (added by the claimant on 2026-10-28 at the maintainer's request, PR #781 review): this review was run on the panel zip, whose layout differs from this package. Its code/A/ and code/B/ are how-we-built-it/A/ and how-we-built-it/B/ here (byte-identical). These panel inputs are not shipped: CLAIM.md and REPRODUCE.md (the claim summary and its commands; see README.md, RUN_IT_YOURSELF.md and how-we-built-it/BUILD.md), histogram_sg_23_A.txt, histogram_sg_23_B.txt and maximising_set.txt (objects/; object/A389690_23.txt holds the same maximising set and, as lines 10-682, the same 673 histogram lines, sha256 760aabce6a540d00660f1e4ab4a243b83a5d6e3640773d6497d67ea630bc00ac), the check helpers verify_oeis.py and sg_ref.py (code/check/), and a389690_2.txt (inputs/), the OEIS program https://oeis.org/A389690/a389690_2.txt (sha256 9fe51a4caa7f2d3f381c44fcb39b43c270c7bab12204e9cbf7e6e2c59999b61f). File references in the text were changed only to name these package paths, URLs or bare file names; no finding, number or verdict changed. Verbatim logs keep the zip's paths.

Role: CRITERION (kit/RUN.md step 6). I worked only from the claim package (unzipped from the panel zip) plus the network: OEIS for clause (3), the upstream repository for the criterion text, and arXiv/web search for subsumption. All times are UTC on 2026-10-26. File names are those of the claim package; verifier-side outputs (out_A.txt, out_B.txt) were written outside it, so the package itself was not modified.

## Verdict in brief

The claim meets the **full CONFIRMED criterion**. It is not a partial win; the only enumerated partial win, p1, is a correction of a listed term and does not apply. Every clause holds when read word by word (sections 2 to 7).
- The criterion is quoted exactly.
- n = 23 is the next unknown term of A389690.
- The definition used matches the entry's definition.
- The maximising set's period is recomputed exactly by independent code.
- Two independently written exhaustive searches agree byte for byte on the maximum and on the full histogram. I rebuilt and reran both. A third search that I wrote for this review also agrees.
- a(23) appears in none of the entry, the b-file and the 36 history revisions at my verification time.

I found two weak points in the package. Neither is fatal, and I closed both myself:
- The claimant's history record is one request. That request shows only revisions #27 to #36 of 36.
- A and B were evidently written by the same claimant, so "independently written" rests on their differing code paths. Authorship is not independent.

## 1. The yardstick: is the criterion quoted verbatim?

- `GET https://api.github.com/repos/elder-plinius/V3R1T4S/commits/8846324` returned HTTP 200 and full SHA `8846324a8fe813bf89a9ef2a60eb9b13d0ba79fd`. The commit message begins "bank: 56 new targets from contributor proposals" and the commit time is 2026-10-25T19:26:25Z.
- `bank/targets.json` at that SHA (raw.githubusercontent.com, fetched 07:40:55Z, HTTP 200, 2146913 bytes) has the entry `id = subtraction-game-max-period-terms`. Its `success_criterion` is **identical** to the text in CLAIM.md: an exact string comparison gave True. Both are 777 characters, sha256 `7d17435ea0c966e2ab31a4e2666188beefa13937437138e83f854deb8b067030`.
- Upstream HEAD at 07:41:45Z is the same commit 8846324. The target entry at HEAD is identical to the one at 8846324.
- `partial_wins` lists only **p1**: "A correction of a published term ... an explicit set S with max S = n whose eventual period exceeds the listed value". The claim is not of that kind, so I judged it against the full CONFIRMED criterion.

## 2. "the exact value of the next unknown term (... A389690 at n = 23)"

- https://oeis.org/A389690 was fetched once at 07:39:16Z: HTTP 200, 16801 bytes, sha256 `e13861cdf6d62b033297ee742046a3ba587735557239a419e7731d1f709305e8`. The DATA line is "2, 4, 6, 8, 10, 12, 22, 25, 28, 58, 54, 87, 114, 144, 189, 336, 306, 456, 728, 1178, 1180, 4464", which is n = 1..22 (OFFSET 1,1). The LINKS field reads "Table of n, a(n) for n=1..22.", KEYWORD is "nonn, more" and STATUS is "approved". So n = 23 is the next unknown term.
- My sha256 of the entry page differs from the claimant's (`66970fe1...`). The term list, links and keywords are the same as CLAIM.md records. The page footer is dynamic: it reads "Last modified October 26 03:23 EDT 2026", which explains the hash change.
- The claim gives an exact value, 3570. This is not a bound.

## 3. "using the entries' own definitions (S ranges over all subsets of {1, ..., n} that contain n; ... minimal eventual period, found as the first repeat of the length-n window ...)"

- The entry's NAME, quoted from the page fetched at 07:39:16Z: "Length of the longest possible eventual period of the Sprague-Grundy value of a subtraction game where the largest element of the subtraction set is n." Its n = 3 EXAMPLE gives periods {1,2,3}: 4, {2,3}: 5, {1,3}: 2 and {3}: 6. My own search reproduces exactly that n = 3 histogram (periods 2, 4, 5, 6, once each).
- **Set range.** All three searches enumerate masks m over [0, 2^(n-1)) with bit i-1 meaning move i, and always add move n:
  - A: `maskS = m | (1ULL << (n - 1))`.
  - B: `moves.push(n)`.
  - mine: `S[k++] = n`.
  The histograms sum to 4194304 = 2^22.
- **Conventions.** All searches take position 0 as terminal (SG 0) and allow move s only when s <= p.
- **Window.** The window is counted only once n values exist:
  - A starts Brent's algorithm at the full window ending at p = n-1.
  - B records keys only when `p + 1 >= n`.
  - The OEIS function records states only for `n >= m - 1`; its zero padding is never stored.
  - Mine starts at i0 = n-1.
  None of these uses the padded-prefix trap listed in the bank's pitfalls.
- **Minimal eventual period.** The window sequence is the orbit of a deterministic map (for max S = n, g(p) depends only on g(p-n..p-1)). At the first repeat W(p) = W(q), the difference p - q is the orbit's cycle length λ. λ equals the minimal eventual period of the value sequence: if values have eventual period d then windows do too, so λ | d; conversely windows of period λ force values of period λ. Brent's λ in program A is therefore the same quantity as B's literal first repeat. I also tested the maximising set without the window argument (section 4).

## 4. Clause (1): "an explicit maximising set S whose period an independent program recomputes exactly"

- maximising_set.txt gives mask 3846998 and set 2 3 5 7 9 10 13 14 16 18 20 21 22 23, with period 3570. The mask decodes to that set, and the argmask 8041302 in program A's output equals 3846998 + 2^22.
- The claim's helper verify_oeis.py (`python3 verify_oeis.py sg 2,3,5,7,9,10,13,14,16,18,20,21,22,23`, 07:43:46Z) printed `OEIS program: period 3570 preperiod_start 1012 (0.0s) | sg_ref: period 3570 first window end 1034`.
- **Provenance of the OEIS function.** The claim's copy of the OEIS program, a389690_2.txt, has sha256 `9fe51a4c...b61f`. I compared its code before the demo loop, whitespace-insensitively, with the PROG field of history revision #2. They are identical apart from an en dash versus a hyphen in one docstring and a duplicated, unreachable `return best_period` line. So the recomputation really uses the entry author's function. I did not re-fetch the linked txt file itself.
- **My own check** (numpy, written for this review). I computed g(0..40000) for S. The maximum SG value is 13.
  - The tail [6000, 40000] (34001 values) has least string period **3570**, found by direct vectorised comparison. This is the minimal eventual period with no window argument involved.
  - g(p) = g(p+3570) fails last at p = 1011, so the sequence is periodic from p = 1012.
  - The literal first repeat of the length-23 window is at p = 4604, matching the window seen at p = 1034, a difference of 3570.

## 5. Clause (2): "two independently written exhaustive searches over all 2^(n-1) sets that agree on the maximum AND on the full histogram"

**Do A and B differ in substance?**
- A (C) computes each new value from a newest-first packed u128 window and uses Brent cycle detection.
- B (Rust) computes values from a value array, uses an oldest-first packed key and a HashMap first repeat.
- The two share no code. What they do share follows from the definition: the mask-to-set encoding, and 5-bit fields, which are safe because SG <= |S| <= 23 < 32 and 23 x 5 = 115 < 128 bits.
- Hidden quantifier: both programs evidently come from the same claimant, so their independence is independence of implementation, not of authorship. The criterion does not literally require different authors. I still removed the doubt with a third search written by me (below).

**Rebuild and rerun** (07:43:20Z to 07:43:36Z, at most 2 processes or threads):
- I compiled A with `cc -O2 -o how-we-built-it/A/subper_a how-we-built-it/A/subper_a.c` and built B with `cargo build --release` (rustc 1.99.0).
- `python3 how-we-built-it/A/run_a.py sg 23 2 out_A.txt` printed `A sg 23 max 3570 set [2, 3, 5, 7, 9, 10, 13, 14, 16, 18, 20, 21, 22, 23] sets 4194304 periods 673 overflow 0 7.1s`.
- `how-we-built-it/B/target/release/subper_b sg 23 2 > out_B.txt` took 9.1 s wall time.
- `python3 how-we-built-it/A/compare.py out_A.txt out_B.txt` printed `"max_equal": true, "set_equal": true, "hist_equal": true, "sets_A": 4194304, "sets_B": 4194304, "distinct_periods": 673`.
- `cmp` shows the reruns are byte-identical to the saved objects:
  - out_A.txt = histogram_sg_23_A.txt (sha256 `39b1a00d71e154a3224d7e7ef88bb54a9ba742e9fdae9588ef662bee311ad68a`, as listed in CLAIM.md).
  - out_B.txt = histogram_sg_23_B.txt (sha256 `deea076cb4d0e6087957f61a11286c227fe93fd2d717cceec277552b69462b4b`, as listed).

**Both object histograms, parsed by me:**

| quantity | value |
|---|---|
| sum of counts | 4194304 |
| maximum period | 3570 |
| sets with period 3570 | 1 |
| next-largest period | 2232 |
| distinct periods | 673 |
| A overflow line | `overflow 0` |

The canonical period-count listing has sha256 `760aabce6a540d00660f1e4ab4a243b83a5d6e3640773d6497d67ea630bc00ac` for A and for B.

**Verifier's own third search** (`sg_floyd.c`, source in the appendix, sha256 `bfdffd59...dd02`):
- It uses byte-array SG values, memcmp windows, and Floyd tortoise and hare, followed by a search for the least d with W(t+d) = W(t).
- Run: `./sg_floyd 23 0 2097152 & ./sg_floyd 23 2097152 4194304 & wait` (07:47:32Z to 07:47:37Z).
- Result: max 3570 at first mask 3846998, which is the claimed set; 4194304 sets; 673 distinct periods.
- Its merged histogram equals both object histograms entry by entry, with the same canonical sha256 `760aabce...00ac`.

## 6. Clause (3): "not yet in the OEIS entry, its b-file or its history at verification time"

- **Entry** (07:39:16Z, section 2): n = 1..22 only; the string "3570" does not occur.
- **b-file** https://oeis.org/A389690/b389690.txt (07:39:17Z, HTTP 200, 183 bytes, sha256 `a0fc3d77b3ef73421b37232cc8d9071031a7eddaf9f5d6f3ce5b0c6fa418a2b8`): this is byte-identical to the claimant's fetch. The first line is "# A389690 (b-file synthesized from sequence entry)", followed by 22 lines, n = 1..22, ending "22 4464".
- **History** https://oeis.org/history?seq=A389690 (07:39:18Z, HTTP 200, 20156 bytes, sha256 `dd43283bfb63a77dffde9dbf994a00f6c0020a4a99d664f9e69ae1e7833020d7`): the page says "Showing entries 1-10" and has an "older changes" link. It covers revisions #36 to #27 only.
- **Hidden quantifier.** "its history" means all revisions. The claimant's record is one request, so it covers only #27 to #36. I fetched the three older pages once each, beyond the three named pages:

  | page | fetched | HTTP | sha256 | revisions |
  |---|---|---|---|---|
  | `&start=10` | 07:40:17Z | 200 | `897d5695...b571` | #26 to #17 |
  | `&start=20` | 07:40:18Z | 200 | `5a48bfb4...ec7e` | #16 to #7 |
  | `&start=30` | 07:40:19Z | 200 | `b43fcf4c...ba60` | #6 to #1 |

  Together the four pages cover revisions #1 to #36 exactly. The only DATA field in the whole history is in revision #2, and it holds the same 22 terms. No page contains "3570" or "a(23)".
- **No pending edit.** The newest revision is #36 (Sun Oct 26 16:51:55 EDT 2025, STATUS proposed → approved).
- Clause (3) therefore holds at 2026-10-26T07:39:16Z to 07:40:19Z.

## 7. "Submitting to OEIS is an action for the human only"

Nothing in the claim package asserts or implies a submission. The OEIS history has no revision after #36 of Oct 2025, so no submission had been made as of 07:40Z.

## 8. Null models and sanity checks

- **Known terms.** I ran A (1 process) and B (2 threads) for n = 1..22 (07:45:24Z to 07:45:38Z), and my own search for n = 1..22 (07:47:26Z to 07:47:32Z).
  - All three return maxima exactly equal to the 22 listed terms.
  - All three histograms agree with each other for every n, and each sums to 2^(n-1).
  - So the definition and conventions reproduce the entry author's independent Python/Mathematica results on 22 instances. A shared definitional error between A and B would have had to leave all 22 values unchanged.
- **A drop below a(22) is expected.** 3570 < a(22) = 4464 is consistent with the entry: the sequence is not monotone (58 → 54 at n = 10 to 11, 336 → 306 at n = 16 to 17).
- **No period cap.** A records an overflow count (0), B has no cap, and my search would exit at 2^23 positions. All three completed with 4194304 sets counted.
- **Agreement is real.** B is self-contained and does not read A's output. Fresh rebuilds reproduced the saved files byte for byte.

## 9. Subsumption ("genuine, non-subsumed win")

- **Not already in the bank.** TROPHY_CASE.md at HEAD 8846324 contains neither "subtraction" nor "389690". GitHub issue search for `repo:elder-plinius/V3R1T4S A389690` (07:41:33Z) returns only PR #699, the closed bank proposal for this target. No other claim on this term exists in the bank.
- **Literature.** The arXiv API abstract of 2601.18715 ("Additive sink subtraction", fetched 07:41:18Z) concerns additive three-move sets under a sink convention, not maxima over all S with max S = n. I read only the abstract. Two web searches found no published value for A389690(23). Absence from the literature is therefore **provisional**. The criterion itself requires absence only from OEIS.

## Residual caveats (do not change the verdict)

- The OEIS state can change after 07:40Z, so a final pre-submission re-check is needed (the human submits).
- The claimed uniqueness ("exactly one set") rests on the histograms, which three searches agree on.
- I did not re-fetch https://oeis.org/A389690/a389690_2.txt. I checked the packaged copy against the revision-#2 PROG text instead.

## Appendix: verifier's search `sg_floyd.c`

```c
/* Verifier's own exhaustive search (written for this review; not derived from programs A or B).
   For every S = {bits of m} U {n}, m in [lo, hi): SG values g[p] = mex{ g[p-s] : s in S, s <= p } in a byte array;
   window W(i) = g[i-n+1 .. i] for i >= n-1; Floyd tortoise/hare on W (compared with memcmp) finds a cycle point,
   then the cycle length is the least d >= 1 with W(t+d) == W(t). Output: "max M first_mask X", then "period count". */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#define CAP (1u << 23)
static unsigned char g[CAP];
static int S[64], k, n;
static long upto;                 /* g[0..upto-1] are computed */
static void extend(long need) {   /* compute g up to index need (inclusive) */
    if (need >= (long)CAP) { fprintf(stderr, "cap exceeded\n"); exit(3); }
    while (upto <= need) {
        long p = upto; uint64_t opt = 0;
        for (int j = 0; j < k; j++) if (S[j] <= p) opt |= 1ull << g[p - S[j]];
        int v = 0; while (opt >> v & 1) v++;
        g[p] = (unsigned char)v; upto++;
    }
}
static int weq(long a, long b) { extend(a > b ? a : b); return memcmp(g + a - n + 1, g + b - n + 1, (size_t)n) == 0; }
int main(int argc, char **argv) {
    n = atoi(argv[1]);
    uint64_t lo = strtoull(argv[2], 0, 10), hi = strtoull(argv[3], 0, 10);
    uint64_t *cnt = calloc(CAP, sizeof(uint64_t));
    uint64_t best = 0, first = 0;
    for (uint64_t m = lo; m < hi; m++) {
        k = 0;
        for (int s = 1; s < n; s++) if (m >> (s - 1) & 1) S[k++] = s;
        S[k++] = n;
        upto = 0;
        long i0 = n - 1, t = i0 + 1, h = i0 + 2;
        while (!weq(t, h)) { t += 1; h += 2; }
        long d = 1;
        while (!weq(t, t + d)) d++;
        cnt[d]++;
        if ((uint64_t)d > best) { best = d; first = m; }
    }
    printf("max %llu first_mask %llu\n", (unsigned long long)best, (unsigned long long)first);
    for (uint64_t p = 1; p < CAP; p++) if (cnt[p]) printf("%llu %llu\n", (unsigned long long)p, (unsigned long long)cnt[p]);
    return 0;
}
```

confirmed_scope: Under the OEIS A389690 definition (S ranging over all 2^22 subsets of {1, ..., 23} that contain 23; period = minimal eventual period of the Sprague-Grundy sequence, i.e. the first repeat of the length-23 window counted once 23 values exist), the maximum period at n = 23 is 3570, attained by exactly one set, S = {2, 3, 5, 7, 9, 10, 13, 14, 16, 18, 20, 21, 22, 23}, as shown by the claimant's two independently written exhaustive searches (A in C, B in Rust, both rerun here) and by this verifier's own third search, all three agreeing on the maximum and on the full 673-period histogram over 4194304 sets, with that set's period recomputed as 3570 by the entry's own Python function (https://oeis.org/A389690/a389690_2.txt) and by a direct tail-periodicity check, and with no a(23) in the OEIS entry, its b-file or any of its 36 history revisions as fetched 2026-10-26T07:39:16Z to 07:40:19Z.

pass: true
