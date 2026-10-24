# Criterion skeptic: lychrel-new-base-proof, base 13

Material examined: only the claim-package copy in panel-work-b13/criterion/ (CLAIM.md, REPRODUCE.md, code/, result/,
status/). All programs ran on the job queue: job 2340 (the claim's code/prove_claim.py), job 2344 (my own independent
checker panel-work-b13/criterion/indep_check.py, which shares no code with code/rle_check.py), job 2347 (checks that
result/b13.tpl matches the JSON, then compiles and runs code/longorbit.c for 100000 steps).

## Condition (1): start n and templates with integer-parameter repeated blocks — MET
- n = 134 base-13 digits. The JSON digits, result/seed_base13.txt and result/seed_decimal.txt all describe the same
  number (job 2344: `seed len 134 txt matches json: True decimal matches: True json decimal matches: True`).
- There are 10 templates T_0..T_9. Each is a list of runs (digit, a, k) and run length = a + k*m. Every template has
  exactly one growing run, with slope 3, and every run has a >= 1 and no negative slope (job 2344, e.g.
  `T0: runs=96 len(m)=134+3m growing=[(50, (4, 30, 3))] prefix=52 suffix=52 adjacent-distinct=True min a=1 negslope=False`).
  So every run is non-empty for every m >= 0, and adjacent runs always have different digits.
- result/b13.tpl matches the JSON exactly (job 2347: `seed eq True`, `tpl templates eq json: True`).

## Condition (2): closure for ALL m >= 0 by an accepted mechanical reduction — MET
- The method is an explicit symbolic carry computation, one of the accepted kinds. The digit positions are cut into
  segments at the run boundaries of x and of reverse(x). Within a segment the pair sum s is constant. The carry lemma
  (code/rle_check.py docstring) says a run of length L >= 1 gives one digit (s+c) mod b, then L-1 copies of
  (s+c1) mod b, with a constant carry c1. I checked the proof for all three cases (s >= b, s <= b-2, s = b-1) and it
  is correct.
- Review of the code in code/rle_check.py `sym_ra`:
  - Its thresholds are conservative: pairwise boundary orders become stable, segment lengths are >= 1, and
    output-run lengths are >= 1.
  - The final carry is computed symbolically and becomes the new leading digit.
  - The T_9(m) -> T_0(m+1) step uses `shift` (a + k), and the brute force uses `expand(T[0], m+1)`. No off-by-one.
  - The result is compared with the target as normalised affine run lists. Equal lists give equal expansions for
    every m, so the comparison is sound.
- Job 2340 output:
  `symbolic closure for m >= M0: OK M0 = 0` and `exact closure and non-palindromicity for 0 <= m <= 200 (+ special m []): OK`.
  So the threshold is 0 and the symbolic step alone covers every m >= 0. The brute force is a redundant extra check.
- My own checker (job 2344) uses a two-pointer symbolic merge from the LSB end. It asserts the carry lemma on every
  parameter-dependent segment and reproduces all 10 steps with threshold M = 0
  (`symbolic closure all 10 steps: True threshold M = 0`). It prints the constant digit/carry run of the growing block
  at every step, for example:
  - `step T0 -> T1(m)`: `pair-sum 8 len 30+3m carry-in 1 -> first digit 9, then run of 8 x(29+3m), carry 0->0 (constant)`, then `final carry 1 -> new leading digit 1`
  - `step T9 -> T0(m+1)`: `pair-sum 16 len 33+3m carry-in 1 -> first digit 4, then run of 4 x(32+3m), carry 1->1 (constant)`, then `final carry 0 -> no new digit`

  The pair sums on the growing segment are always 8 or 16, never b-1 = 12, so the carry never depends on m. Integer
  brute force over 0 <= m <= 400 found `closure+nonpal failures = 0`.
- Self-paired central block:
  - In T_0..T_6 and T_9 the growing block sits exactly at the centre (prefix length = suffix length), so it pairs with
    itself as one segment (pair sum 2d).
  - In T_7 (prefix 51, suffix 52) and T_8 (prefix 52, suffix 51) it is off-centre by one digit. The generic boundary
    merge handles this: the overlap is a growing segment of length 33+3m, and two fixed length-1 segments pair the
    block digit with its neighbours. Both checkers agree.
  - Edge cases: no run has length 0 at any m >= 0. A length-1 run (a = 1, k = 0) is treated digit by digit.
- Independent simulation (job 2347):
  `RESULT base=13 steps=100000 final_len=30134 template_checks=100001 mismatches=0 palindromes=0`.

## Condition (3): no template string is a palindrome — MET
- For every m >= 0 all runs have length >= 1 and adjacent runs have different digits. So the run list is the
  string's unique run-length encoding.
- In all 10 templates the sequence of run digits is not a palindrome (job 2344, e.g.
  `T0 run-digit sequence palindromic: False (first mismatch at run 0: 10 vs 9)`; T4, T7 and T8 first differ at runs
  1, 2 and 1).
- Hence no T_i(m) is a palindrome for any m. No m where mirrored run lengths coincide needs a special check, which is
  why the special set in job 2340 is `[]`. The brute force up to m = 400 agrees.

## Condition (4): the orbit enters the template set — MET
- entry_step = 0 and n = T_0(0) (job 2340: `entry: OK at step 0`; job 2344: `seed == T_0(0): True`).
- By induction with (2), x_t = T_(t mod 10)(t div 10) for every t >= 0. By (3), every iterate (and n itself) is not a
  palindrome.

## Condition (5): base and novelty — base condition MET; novelty NOT shown in this package
- 13 is not a power of 2 and is not in {11, 17, 20, 26}.
- The Wikipedia snapshot (sha256 e574eb9d…, verified, fetched 2026-10-23) says "Lychrel numbers have been proven to
  exist in the following bases: 11, 17, 20, 26, and all powers of 2."
- The package holds only the Wikipedia and OEIS (A060382, A023108) snapshots. It has no arXiv search and no record of
  the 2023 construction paper. So it does not meet the full-CONFIRMED novelty wording. The snapshot is also one day
  older than verification time.
- The novelty skeptic decides novelty. On the criterion wording, the right level is partial win p1 (VERIFIED PROOF,
  NOVELTY UNCONFIRMED), not full CONFIRMED.

## Gaps found
- Cosmetic only: the docstring of code/prove_claim.py names "result/lychrel_base9.json" (left over from a copy). The
  code reads the file given on the command line, so this does not affect the result.
- The claim's own code checks the carry lemma implicitly, without printing per-block traces. My checker (job 2344)
  supplies the explicit per-block trace.
- No mathematical gap was found. No step rests on "by inspection".

confirmed_scope: In base 13, the 134-digit number n of result/seed_base13.txt equals T_0(0) of the 10 affine run-length templates in result/lychrel_base13.json, and a mechanically checked symbolic carry computation with threshold 0 (re-run in jobs 2340 and 2344, cross-checked by integer brute force for m <= 400 and a 100000-step simulation in job 2347) proves RA(T_i(m)) = T_(i+1)(m) for i < 9 and RA(T_9(m)) = T_0(m+1) for every m >= 0, with no T_i(m) a palindrome, so n is a Lychrel number in base 13 at the level of partial win p1 (novelty not established by this package).
context: subagent (Claude Code Agent tool, fresh context)

pass: true
