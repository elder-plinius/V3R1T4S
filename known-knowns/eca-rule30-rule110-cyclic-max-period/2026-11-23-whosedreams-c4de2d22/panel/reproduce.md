role: REPRODUCE
context: subagent (started as a fresh executor subagent for this panel; saw only files and ran its own checks, no earlier panel votes)

# Reproduce — A334497(37) = 49276415 (Rule 30, cyclic width 37)

## Definition used (quoted)

From how-we-built-it/TARGET_CRITERION.md (bank success criterion, quoted in part):

> The exact value of A334497(37) or A204371(37) (or any later term), from an exhaustive search over all 2^n states, or over all rotation orbits with the rotation factor accounted for. It must be run by two independent implementations that agree. Both must reproduce A334497(1..24) and A204371(1..30) exactly, and both must report their values for A334497(25..30). [...] A witness state on the maximal cycle must be given, so a skeptic can confirm the cycle length by direct iteration. Bit order must follow the Wolfram rule-number convention, which the small-n reproduction checks.

The object (object/a334497_37.txt, sha256 c4de2d229d66b00658b0160e316c1992afc9cd8f8010649bcf2ec34a4371247c, equal to verify-it-yourself/OBJECT_SHA256) claims n=37, rule=30, max_period=49276415, witness=0x7fbfe703e. Convention used here: cell 0 is the least significant bit; for cell i, L = cell (i-1) mod n, C = cell i, R = cell (i+1) mod n; idx = (L<<2)|(C<<1)|R; next bit = (rule>>idx)&1. The eventual period of a start is the length of the cycle it eventually enters; A334497(n) is the maximum over all 2^n configurations.

I wrote my own iterator, cycle finder and exhaustive census in C from that definition before reading how-we-built-it/impl1/maxcycle.c or impl2/maxcycle.c, and did not use verify-it-yourself/check_period.py for my own checks.

## 1. Shipped check script

`sh verify-it-yourself/run_checks.sh` (run under nice -n 19 on 2026-11-23, about 18:51 ET, America/Toronto UTC-5): 30.9 s, last line `PASS` (first_return 49276415, no shorter period among the divisors). `sha256sum -c SHA256SUMS` passes for every listed file.

## 2. Witness period (own iterator)

Own program, two step functions (a bitwise rotate-based one and a literal per-cell one, checked equal on 1000 steps):

- From 0x7fbfe703e at n=37 under Rule 30, the first return is at step 49276415.
- 49276415 = 5 * 37 * 266359 (266359 prime). States after the proper divisors: 1 → 0x808039843, 5 → 0x909ba0e6c, 37 → 0x1463aa56b6, 185 → 0x179b120968, 266359 → 0x10ec393945, 1331795 → 0x1eff9c0f8f, 9855283 → 0x740e77ad2; none equals the start (first return already makes this redundant). These match the states printed by run_checks.sh.
- A separate Brent cycle-detection program using only the per-cell step: from 0x7fbfe703e, lambda = 49276415, mu = 0 (the witness is on its cycle); from a single live cell 0x1, lambda = 49276415, mu = 260564, and the first cycle state reached is exactly 0x7fbfe703e. So the witness lies on the single-cell cycle, whose length is the floor A334496(37) = 49276415.

The witness's eventual period is exactly 49276415.

## 3. Own exhaustive census at small widths (no shared code)

Own C program: for every one of the 2^n states, walk the functional graph with a walk id and step index per state; a cycle is counted when a walk meets its own id (period = step difference). No rotation or reflection folding. Compared with the live OEIS b-files, fetched once each on 2026-11-23 at 18:53:27 ET (23:53:27 UTC), HTTP 200:
- https://oeis.org/A334497/b334497.txt sha256 7339a6ff9bd1784e65389af0b1c40de0f308d57dc1b30f6be925ee8b8c26b6f4 (ends at n=36, a(36)=2237472; no n=37)
- https://oeis.org/A204371/b204371.txt sha256 9237e577a1b8e6c74b30a2c2ee7c95e67b20f061fc22e230230f59b12ce41091

Results: Rule 30 n=1..27 and Rule 110 n=1..27, 54 widths, 0 mismatches against the b-files (e.g. A334497(24)=185040, (25)=588425, (26)=312156, (27)=240300; A204371(26)=351, (27)=567). This independently fixes the definition and the Wolfram bit order. These b-file sha256s equal those in logs/kit_sha256.txt (data/b334497.txt, data/b204371.txt), so the PC self-test used the same reference data.

## 4. Rebuild and re-run of the shipped programs (box, not n=37)

Copied how-we-built-it/impl1/maxcycle.c and impl2/maxcycle.c out of the package. Their sha256s (9e24406731671802a57bdc13dd3f2a3b47c1f0ddbba4876ad2ff133a61a330cc and bf2321ce02bef42ef6fe45219c39b85832af35694d054704f664051c2a7333bc) equal both logs/kit_sha256.txt and the sources frozen in how-we-built-it/PREREG.md (PREREG.md is byte-identical to the frozen file, sha256 1d5713b3...). Built with `cc -O3 -march=native`, as in build.sh. The binary hashes differ from the PC's (logs/kit_sha256.txt), as expected for a different compiler and CPU; the sources are identical. All runs used nice -n 19, at most 2 jobs at once, peak about 0.55 GB each.

- Both programs, Rule 30 and Rule 110, n=1..24 (96 runs): every max_period equals my own census (and therefore OEIS).
- impl1 Rule 30 n=32 (own held-out choice; 512 MiB bitset): max_period=2002272, witness 0xf7c37cc3, 128.5 s, 18:54:43–18:56:52 ET. This equals the listed A334497(32)=2002272. My iterator confirms 0xf7c37cc3 first returns at 2002272.
- impl2 Rule 30 n=31 (512 MiB colour array): max_period=2841150, witness 0x706f863e, 778.3 s, 18:54:43–19:08:04 ET. This equals the listed A334497(31)=2841150 and the shipped impl1 and impl2 held-out results (heldout/r30_n31/). My iterator confirms 0x706f863e first returns at 2841150.

## 5. Consistency of the shipped outputs

- results/result_impl1.txt and result_impl2.txt both say rule=30 n=37 max_period=49276415 witness=0x7fbfe703e. The witness_impl*.txt files agree, compare.txt says AGREE and FLOOR_OK, and both results/check_period_impl*.txt end PASS.
- selftest/selftest.log: 120 lines, 108 `OK` + 12 `REPORT_MATCHES_LISTED`, no BUG or MISMATCH. It is identical to the self-test section of logs/run.log. All 120 per-width result files (r30_n1..30 and r110_n1..30, impl1 and impl2) match the log and the live b-files. The only adjustment line is selftest/r110_n26/err_impl1.txt (702 → 351), which the README discloses. The n=37 and held-out err files contain no adjustment.
- heldout/: both programs give A204371(31)=2759 (witness 0x3f647ff8) and A334497(31)=2841150 (witness 0x706f863e). check_period_r110.txt ends PASS.
- logs/run.log timing: impl1 ran 13:24:13–14:26:39 ET on 2026-11-22 (3746 s wall vs time_sec 3739.4) and impl2 ran 14:26:39 on 2026-11-22 to 01:51:05 on 2026-11-23 ET (41066 s wall vs 41058.0). The ratio is about 11.0, as with the Rule 110 n=37 sibling (1699 s vs 11947 s). The self-test started after the build at 13:06:21 ET (18:06:21 UTC).
- Peak RSS: impl1 16791800 kB vs a 2^37/8 B bitset = 16777216 kB, leaving about 14 MB, which fits a path array of about 1.6 M orbit states (cycle/37 + transient). impl2 33943584 kB vs a 2^37/4 B colour array = 33554432 kB, leaving about 380 MiB, which fits a uint64 stack of about 49.5 M entries (the full 49276415-state cycle plus its transient). Both are consistent with a real full-width census that walked this cycle.
- Raw send-back: sendback/raw/*.gz sha256 e5a8004c7d9ab4b68005580197bcd96855a1a007b272fd3c6b377eb51ef8867c (equal to the user's attachment). I unpacked it myself: it is identical to sendback/unpacked/work. Compared with the package, selftest/, heldout/ and main_r30_n37/ (= results/) are byte-identical, as are all_results.txt, STATUS.txt and kit_sha256.txt. run.log differs only in three home-directory-to-~ path edits, and sysinfo.txt only in the hostname and kernel build host. Package run_r30.sh differs from the PC kit's (sha256 1f33388a..., equal to kit_sha256.txt) only in the WIN_DL default line. build.sh, check_period.py and both sources are identical to the PC kit. No result value was changed.

## 6. Source audit (read after my own checks)

- Both programs use the same step as the definition: L = bit (i-1) mod n, R = bit (i+1) mod n, idx = (L<<2)|(C<<1)|R, cell 0 = LSB. Neither folds reflections.
- impl1: the loop runs over every s0 in 0..2^n-1. It skips states whose rotation orbit is already marked; that is valid because rotation commutes with the rule, so a rotated start reaches a rotated copy of an already measured cycle with the same period. Along a walk it marks each new state's whole orbit. A walk ends when it meets a marked state. If that state is a rotation of an earlier path element path[hit], then k = plen-hit is the least j>0 with f^j(path[hit]) in the orbit of path[hit] (path orbits are pairwise distinct). The offset r is recomputed by evolving k steps, and the period is k (r=0) or k*n/gcd(r,n). That formula is exact when the state has a trivial rotation stabiliser. At prime n=37 only all-0 and all-1 have non-trivial stabilisers, and under Rule 30 all-1 → all-0 → all-0 (rule bits 7 and 0 are 0), so the n=37 value cannot be affected. The winner is also re-checked by direct first return, with no adjustment in results/err_impl1.txt. Each cycle is counted from its eventual image once.
- impl2: a 3-colour walk over all 2^n states with 2 bits per state. Meeting a grey state gives period = stack distance (exact); meeting black means a transient into finished territory. The stack is painted black afterwards, so each cycle is measured once. There is no rotation formula, and the witness gets a direct first-return check.
- The two methods (orbit marking with offset conversion vs plain colouring) are independent. I found no defect.

## What was reproduced and what was accepted

Reproduced on this box:
- the witness period, exactly 49276415, with its divisor checks;
- the witness lies on the single-cell cycle (transient 260564);
- the definition and bit order, by an own census matching OEIS A334497(1..27) and A204371(1..27);
- the source hashes;
- both rebuilt programs matching the census at n=1..24;
- impl1 = A334497(32) and impl2 = A334497(31) on held-out widths;
- byte-level agreement between the package and the raw send-back.

Accepted from the shipped PC logs, not re-run: the 2^37 census itself (impl1 3739 s with a 16 GiB bitset, impl2 41058 s with a 32 GiB colour array; this box has about 16 GB). No sample of the 2^37 space is offered as a census here. The n=37 maximum rests on the two audited exhaustive programs, whose agreement, timings and memory footprints in the PC logs are internally consistent.

## Verdict

The packaged witness has eventual period exactly 49276415, equal to the single-cell floor. Both shipped programs are correct exhaustive eventual-period searches under the required bit order. Rebuilt from hash-matching sources, they agree with an independent census and with live OEIS, and they reproduce listed terms at held-out widths 31 and 32. The shipped n=37 outputs agree with each other and are byte-identical to the raw PC send-back, apart from the disclosed path, hostname and WIN_DL edits. I found no mismatch, missing object or non-determinism.

pass: true
