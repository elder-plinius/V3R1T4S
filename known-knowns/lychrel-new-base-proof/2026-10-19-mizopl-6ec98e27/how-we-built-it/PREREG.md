# PREREG — lychrel-new-base-proof (Base-98 Template-Closure Proof)

> **Dated Note (2026-11-03):** This single-object package for base $b = 98 = 2 \cdot 7^2$ (`object/lychrel_base98_certificate.json`, `sha256: 6ec98e276bfb691187e5ebdb4c8ccf0c149f2754e201e362c15a4a681dbb5256`) was split from the initial multi-base submission in [PR #517](https://github.com/elder-plinius/V3R1T4S/pull/517) so that each PR contains a single result and no copied third-party files. The pre-registration rules below are scoped to the files shipped in this base-98 package.

frozen_before_evaluation: true
target_id: lychrel-new-base-proof
preregistered_rule: >
  We search the decoupled carry-wire family in bases b == 2 (mod 24) (combining the b == 2 (mod 3) outer-engine transition constraint and b == 2 (mod 8) inner-core transition constraint of our search ansatz) for a Period-4 template cycle T_1(m) -> T_2(m) -> T_3(m) -> T_4(m) -> T_1(m+1) in base b = 98 = 2 * 7^2. A candidate solution is accepted if and only if:
  1. David Seal's 1996 Period-4 Base-26 template cycle (https://www.mathpages.com/home/dseal.htm) is first reproduced and mechanically verified by the exact same symbolic run-length block carry transducer (`verify-it-yourself/check_lychrel.py`).
  2. The base b = 98 satisfies b not in {2^k, 11, 17, 20, 26} and is not listed as proven on https://en.wikipedia.org/wiki/Lychrel_number (`the-record-we-beat/README.md`) at verification time.
  3. Closure under base-b reverse-and-add for ALL integer parameters m >= 1 in `object/lychrel_base98_certificate.json` is mechanically proved by an explicit block-by-block symbolic carry computation (`symbolic_rle_rev_add` in `verify-it-yourself/check_lychrel.py`) in which every parameter-dependent block ((b-1)^m paired with 0^m at exact mirror offsets) is verified to produce a constant digit/carry run with outgoing carry equal to incoming carry (c_out == c_in), together with exhaustive brute-force verification for all 1 <= m <= 500 (strictly exceeding max(m_0, 200) = 200).
  4. Symbolic non-palindromicity is mechanically proved for every template T_1(m)..T_4(m) and all m >= 1.
  5. The starting integer n = T_1(1) (and a 1-step pre-template seed n_seed entering T_2(1) at step 1) is simulated and matched at every step to one of T_1..T_4 via compiled regular expressions (`re.Pattern.fullmatch`).

holdout_discipline: >
  Not an empirical train/test task. Every step of the template-closure proof for base b = 98 (`object/lychrel_base98_certificate.json`) is verified by a finite mechanical symbolic carry-transducer check, brute force over 1 <= m <= 500, and regex-verified 2,000-step orbit simulation (`t = 0..2,000`), alongside 400 seeded random 92-digit base-98 starting numbers and two structural perturbation controls in `verify-it-yourself/check_lychrel.py`.

ratchet_budget: n/a (deterministic symbolic template-closure proof)
