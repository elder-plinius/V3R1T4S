context: REPRODUCE skeptic, subagent (Agent tool, fresh context), model opus (a first attempt on fable was stopped unfinished at the human's request, to save Fable usage); saved by the gate session from the returned text. First report (v1) on the package before its checksum file was regenerated, then the re-check (v2) on the corrected package; v2 is the verdict.

## First report (v1, superseded)

# REPRODUCE skeptic report: panel-dfffa2e6, (d,N) = (6,526)

Work folder: ~/v3r1t4s/uploads/panel-dfffa2e6/reproduce/work2/. The claim folder was only read. No network was used.

## Method (my checker was written before I read the claim's checker)

`work2/mycheck.py` was run as `~/v3r1t4s/venv/bin/python -I` (Python 3.9.6, mpmath 1.4.1).
- Each coordinate is parsed as an exact decimal string and turned into an exact integer on a common 10^-29 scale.
- The Gram matrix entries and squared norms are exact integers, for all 138,075 pairs.
- Every pair's cosine is computed in mpmath at 60 dps from those exact integers. No float screen is used.
- The argmax is confirmed exactly: for every pair within 1e-40 of the mp maximum, the rational dot^2/(|a|^2|b|^2) is compared.
- The SHA256SUMS check, the INDEX.csv and cell.json hash checks, and a second sha256 computed with a different interpreter (/usr/bin/python3) are all part of the run.

## Results (mine)

| check | result |
|---|---|
| object sha256 | dfffa2e676f24cbecc11657a119d33fd2169f06963446dbde15c10e6455c8eb8 |
| = INDEX.csv sha256 | yes |
| = cell.json sha256 | yes |
| = SHA256SUMS entry | **NO**: SHA256SUMS lists 9ab8021055cf16bc...b5ff62c65ce9a9660c1c907fca8e202f9def2d5b83a, the superseded PR #231 object |
| file format | 102,565 bytes, ASCII, LF, trailing newline, no CR |
| shape | 526 rows x 6 columns, 0 unparseable tokens, 526 distinct rows, no zero vectors |
| significant digits per coordinate | min 26, max 26 over all 3,156 coordinates; 0 coordinates below 20 |
| raw norms | max abs(norm - 1) = 2.68e-16 (the raw vectors are normalised anyway) |
| pairs evaluated | 138,075 = 526*525/2 |
| c* | 0.78642753233007415287205736715522202517220615646 |
| argmax pair | rows (202, 395) 0-based, which are file lines 203 and 396; it is the unique exact maximum (1 pair within 1e-40, exact rational tie count 1) |
| claimed 0.786427532330074152872057 | agrees: abs(c* - claim) = 3.67e-25, and the claim is c* truncated (and rounded) to 24 dp |
| gain = 0.786636400242 - c* | 2.0886791192584712794e-4 (claimed "about 2.0887e-4": correct) |
| gain > 1e-10 | yes, by a factor of about 2.1e6 |
| minimal angle | 38.1470990174209942184860898914 deg (README: 38.14710, correct) |
| table angle | 38.1277204106990... deg, so the angle gain is +0.01937860672 deg |
| contact structure (context) | pairs within 1e-12 / 1e-9 / 1e-6 of c*: 1 / 5 / 2344. The next-largest cosine is 8.96e-11 below c*. |
| live-table cross-check | ceil(c*, 12 dp) = 0.786427532331, which equals the live row cited in cell.json |

Determinism: two runs produced byte-identical output, sha256 d8d27afb112f72ea961783a73f7b14ed2508c832a88186dd27e5fe56f1b0ce0b for both run1.txt and run2.txt.

## Claim's own checker (from a scratch copy, work2/scratch/)

`sh verify-it-yourself/run_checks.sh` was run with Python 3.13.2. It uses only the standard library: exact Decimal at 70 digits over all pairs. It exited 0 and printed:

```
object object/d6_N526.txt sha256 dfffa2e676f24cbecc11657a119d33fd2169f06963446dbde15c10e6455c8eb8
points 526 dimension 6 minimum significant digits 26
pairs checked 138075
c* = 0.786427532330074152872057367155 at points (202, 395)
table cosine 0.786636400242 (https://spherical-codes.org/plain, fetched 2026-10-16T05:12:04Z)
gain = table - c* = 0.00020886791192584713
PASS
```

- This output is identical line for line to the block in RECEIPTS.md (checked with diff) and to the expected output in RUN_IT_YOURSELF.md.
- It agrees with my checker on c* to all 30 printed digits, on the argmax pair (202, 395), on the gain to 20 digits, and on the minimum significant digits (26).
- The two implementations are independent: exact integers with mpmath and exact rational argmax in mine, against Decimal at 70 digits in theirs.
- One small note on the claim's checker: its significant-digit count also strips trailing zeros after leading zeros are gone. That does not matter here, because every coordinate has 26 digits.

## Package integrity: FAILS

RUN_IT_YOURSELF.md makes `shasum -a 256 -c SHA256SUMS` the first verification step. That command exits 1.

- **9 checksum mismatches.** The files are HOW_WE_FOUND_IT.md, INDEX.csv, README.md, RUN_IT_YOURSELF.md, **object/d6_N526.txt**, the-record-we-beat/README.md, the-record-we-beat/cell.json, verify-it-yourself/RECEIPTS.md and verify-it-yourself/check_code.py.
- **4 listed files are missing.** These are panel/criterion.md, panel/gate.md, panel/novelty.md and panel/reproduce.md.
- **16 present files are not listed.** These are how-we-built-it/PREREG_run0758.md and all 15 files in how-we-built-it/repolish-run0758/, which is the provenance of this object.
- The 18 files that do match are prompt/*, run_checks.sh, requirements.txt, code_hashes.json and how-we-built-it/code/*.

SHA256SUMS is the stale manifest of the superseded PR #231 package. Its object hash 9ab80210... is the first code, with c* 0.786430618545 according to README.md. Anyone who follows the documented procedure is told that the claimed object FAILED its checksum.

how-we-built-it/code_hashes.json matches all 10 files in how-we-built-it/code/. It covers no file in repolish-run0758/.

## Verdict

The mathematical claim reproduces exactly and deterministically. It also agrees with the claim's checker and with RECEIPTS.md: c* = 0.786427532330074152872057..., the argmax pair is unique, there are 26 significant digits everywhere, and the gain of 2.0887e-4 is above 1e-10.

The package as shipped does not pass its own documented integrity step. SHA256SUMS does not match the object or 8 other files, lists 4 absent files and omits 16 present ones.

This is the only blocking defect, and it is purely a packaging one. To fix it, regenerate SHA256SUMS over the final file set, after the panel/ files are written, so that it includes repolish-run0758/ and PREREG_run0758.md, and confirm that `shasum -a 256 -c SHA256SUMS` exits 0. If the gate does that, this skeptic's numerical findings support a pass.

(v1 verdict, superseded) pass: false

## Re-check (v2, the verdict)

# REPRODUCE skeptic re-check (v2): panel-dfffa2e6, (d,N) = (6,526), copy claim2/

This is a re-check of the new read-only copy at ~/v3r1t4s/uploads/panel-dfffa2e6/reproduce/claim2/. All work was done in work2/ and no network was used. The v1 report (work2/reproduce.md) failed only on a stale SHA256SUMS.

## What changed between claim/ and claim2/ (byte comparison of every file)

- **Changed:** SHA256SUMS, README.md, RUN_IT_YOURSELF.md and HOW_WE_FOUND_IT.md.
- **New:** prompt/NOTE.md, a 3-line provenance note saying prompt/ comes from run 0024 and the object from re-polish run 0758.
- **Unchanged (byte-identical):** every other file. That includes object/d6_N526.txt, verify-it-yourself/check_code.py, run_checks.sh, RECEIPTS.md, the-record-we-beat/cell.json and INDEX.csv.

I checked the wording changes for numbers:
- README and RUN_IT_YOURSELF change only wording, mostly the upload and robots.txt disclosure and the live-table framing.
- The README numbers are unchanged: c*, sha256, 26 digits, 2.0887e-4, 0.786636400242 and 38.14710 deg.
- The new README statement that the live value 0.786427532331 is "this c* rounded up at the 12th decimal" is correct. I get ceil(c*, 12 dp) = 0.786427532331.
- HOW_WE_FOUND_IT only drops a sentence about other rows. Its retained "2.06e-4" describes the first-stage code (0.786636400242 - 0.786430618545 = 2.058e-4), not this object (2.0887e-4). That is accurate as written and does not affect the claim.

## Integrity

`shasum -a 256 -c SHA256SUMS` was run from claim2/ and **exited 0**: 44 OK, 0 mismatched, 0 missing.

My checker independently confirms the same result: ok=44, mismatched=0, missing=0. Every file on disk is listed except SHA256SUMS itself. As stated, there is no panel/ entry; the panel files are added after the gate.

The object's sha256 is dfffa2e676f24cbecc11657a119d33fd2169f06963446dbde15c10e6455c8eb8. SHA256SUMS, INDEX.csv and cell.json now all list that value.

## Re-run of my checker on claim2

The command was `~/v3r1t4s/venv/bin/python -I mycheck.py ../claim2`, and its output is in run3_claim2.txt. All numerical lines are identical to v1 run1.txt; the diff shows only the SHA256SUMS lines and the output digest. The results are:

- shape 526 x 6, all 3,156 coordinates at 26 significant digits, 526 distinct rows
- 138,075 pairs, all evaluated in mpmath at 60 dps from exact integer Gram entries
- c* = 0.78642753233007415287205736715522202517220615646
- unique exact argmax at rows (202, 395), 0-based
- the claimed 0.786427532330074152872057 agrees to 3.67e-25
- gain = 0.786636400242 - c* = 2.0886791192584712794e-4, which is above 1e-10
- minimal angle 38.1470990174209942184860898914 deg

v1 had already shown determinism: two runs gave byte-identical output.

## Re-run of the package checker

`sh verify-it-yourself/run_checks.sh` was run from a scratch copy (work2/scratch2/) with Python 3.13.2. It exited 0 and printed PASS:

```
object object/d6_N526.txt sha256 dfffa2e676f24cbecc11657a119d33fd2169f06963446dbde15c10e6455c8eb8
points 526 dimension 6 minimum significant digits 26
pairs checked 138075
c* = 0.786427532330074152872057367155 at points (202, 395)
table cosine 0.786636400242 (https://spherical-codes.org/plain, fetched 2026-10-16T05:12:04Z)
gain = table - c* = 0.00020886791192584713
PASS
```

This output is identical line for line to the RECEIPTS.md block, and it agrees with my checker on c*, the argmax, the gain and the digits.

## Verdict

The only blocking defect in v1 was the stale SHA256SUMS, and it is fixed. The documented `shasum -c` step passes on every file. The object, checker and cell.json are byte-identical to the copy I verified in v1. The claim reproduces exactly under two independent implementations:
- c* = 0.786427532330074152872057...
- unique argmax at (202, 395)
- 26 significant digits everywhere
- gain 2.0887e-4, above 1e-10, against the 0.786636400242 value recorded on 2026-10-16T05:12:04Z

pass: true
