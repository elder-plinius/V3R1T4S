# Criterion skeptic: claim 2026-11-25-whosedreams-36afb636 (heptiamonds M-X, bounded UNSAT k = 2..20, partial win p3)

context: subagent (started as a fresh executor subagent; I saw only files on the box and my own command output, not the run's conversation)
date: 2026-11-24 ET

## What I read and ran
- Bank entry polyform-compatibility-open-pairs (repo/bank/targets.json): success_criterion, partial_wins p1-p3,
  verification_method, pitfalls. kit/SUBMIT.md section 1. Package README.md, INDEX.csv, object/*.json,
  RUN_IT_YOURSELF.md, HOW_WE_FOUND_IT.md, how-we-built-it/PREREG.md, the-record-we-beat/RECORD.md,
  how-we-built-it/code/py/sat_compat.py and cnfutil.py.
- `sha256sum -c SHA256SUMS`: all 43 listed files OK. sha256 of object/mx_k2_20_bounded_unsat.json = 36afb636...,
  matching the submission id and INDEX.csv.
- object/SHA256SUMS-archive.txt and SHA256SUMS-files.txt are identical (hashes and relative paths) to the
  contributor's raw send-back in the PC send-back folder (zenodo-MX). The archive hash is 6fc6276d9ba8f6b6...,
  and the object records 175028808 bytes, the same as the size the contributor reported.
- In a scratch copy, `KMAX=5 sh verify-it-yourself/run_checks.sh` ended in PASS (rc 0, about 3 min, under a 3 GB
  ulimit). Output: k=5 had 230145 connected M-figures and 51373 connected X-figures, 0 in common, with no board.
- No file is larger than 1 MB; the package is about 253 KB. No absolute machine paths (home, workspace or mount folders) appear
  in the package files.

## 1. Fit to p3
p3 reads: "A computer-certified impossibility (SAT/DLX exhaustive, with checkable proof) up to a stated figure size
for a '?' pair, clearly labelled as bounded."
- '?' pair: RECORD.md records the M-X and X-M cells as '?' in both the unrestricted and holeless tables
  (fetched 2026-11-25T00:18:18Z). Whether that is still true live is the novelty skeptic's check.
- Computer-certified and exhaustive: the model (sat_compat.build_joint_cnf) has board-cell variables F (exactly 7k
  true), exactly k M placements and exactly k X placements. Each placement implies its cells are in F. Each F cell
  is covered by at least one M placement and at least one X placement, and M placements overlap pairwise nowhere,
  and the same holds for X. That is exactly "F is tiled by k M's and by k X's". There is no connectivity or
  holeless constraint, so UNSAT also excludes disconnected figures and figures with holes. That makes it stronger,
  which is right for the unrestricted table. The sequential counter is standard Sinz in both directions.
  Soundness of the placement enumeration is the reproduce skeptic's job; the model matches the claim sentence.
- Stated figure size: the bound is k <= 20 tiles of each kind AND the figure must fit inside a fixed board per k
  (board_rows = max(6, ceil(2*sqrt(7k))) + 2, board_cols = board_rows + 2, from 10x12 to 26x28). This is not a bound
  in tile count alone. Still, p3 asks for a stated, clearly labelled bound, and this bound is stated exactly
  (formula and per-k numbers) and machine-checkable. I accept it under p3 only if the board is named in the scope.
  The board-free part covers k = 2..5. I re-ran it myself (connected figures only). That is enough: each component
  of a disconnected common figure would itself be a common figure with fewer tiles, because the areas force equal
  M and X counts per component.
- Clearly labelled as bounded: the README title says "inside the stated boards (bounded UNSAT ...)". The opening
  note says it is NOT an incompatibility proof. "What", "Not claimed", the INDEX.csv value ("bounded UNSAT for
  k=2..20 inside the stated boards"), the object's "claim" field ("Bounded result only"), each per-k p3_label and
  HOW_WE_FOUND_IT all say bounded. This is adequate.
- Main criterion, p1 and p2 are explicitly not claimed. That is correct, because no figure was found.

## 2. "with checkable proof": must CONFIRMED_PARTIAL wait for Zenodo publication?
YES. CONFIRMED_PARTIAL MUST WAIT UNTIL THE ZENODO RECORD 10.5281/zenodo.24518087 IS PUBLISHED.
The DRAT proofs are the "checkable proof" p3 requires. They are not in the package and not on this box. They exist
only on the contributor's PC and in a Zenodo record that is an unpublished DRAFT. A stranger cannot download a
draft, and SUBMIT.md requires a large file to carry "a public archive URL". Until publication the certificate
cannot be checked by anyone else. The packager's byte-identical regeneration on the box (reproduce skeptic's
check) shows the proofs exist and are deterministic, but that does not make them publicly checkable.
Condition for upgrading: after the user publishes, someone must fetch the public record and confirm it serves
heptiamond-MX-k2-20-proofs.tar.xz with exactly 175028808 bytes and sha256 6fc6276d9ba8f6b61cc4bde2a5210dbccd23ee47c9904c6bcac1df50c350b1be.
Only then may the gate move from PROMISING to CONFIRMED_PARTIAL. The README states this correctly in "What" ("The
record must be published before this package is submitted"), RUN_IT_YOURSELF.md step 2 and "Not claimed".

## 3. SUBMIT.md rules
- One cell per package: yes, M-X unrestricted only. The holeless table is only mentioned as "nothing beyond what
  follows", and the other 20 pairs are excluded.
- Files at most 1 MB and package at most 50 MB: yes. The large archive is listed by name, size, sha256 and DOI URL.
  The URL is public only after publication (see 2).
- No third-party pages copied in: RECORD.md is a snapshot (URL, time, status, headers, sha256, extracted cell),
  not the page. how-we-built-it/ holds only the contributor's kit code, scripts, the box-reproduction scripts and
  logs, and a generated piece table (data/heptiamonds.json: coordinates of the 24 free heptiamonds, read by
  shapes.py). No CaDiCaL or drat-trim sources are included; those tools are only mentioned and credited.
- Credit: whosedreams (README Credits, submission id). Third parties are credited with links.
- PACKAGING DEFECT TO FIX (not a criterion failure): the staging folder now contains
  verify-it-yourself/__pycache__/indep_compat.cpython-313.pyc (mtime 2026-11-24 19:37:53 ET, probably left by another
  skeptic's run_checks.sh). It is not in SHA256SUMS. The parent must delete that directory BEFORE regenerating
  SHA256SUMS, or the .pyc will be packaged. I did not touch it, because PKG is read-only for me.

## 4. PREREG written after the search
PREREG.md says plainly that it was frozen at packaging time, after the 2026-11-03..05 runs. For a deterministic
certificate this does not matter. There is no statistic to tune and no multiple comparison: the result is UNSAT
plus a DRAT proof for every k = 2..20, and it is reproducible byte for byte. The one choice that could have been
tuned is the board formula, and it is fixed in the code (board_for_k), stated in the scope and used for all 21 pairs.
The late PREREG is disclosed honestly, so it does not block.

## 5. Scope
The README's proposed scope is supported. I keep its content, name the board formula explicitly, and add the
publication condition.

confirmed_scope: For heptiamonds M and X (Ishino names as on George Sicherman's Heptiamond Compatibility page, where the unrestricted M-X cell is '?'), for each k = 2..20 the joint cover CNF on the triangular-lattice board of board_rows = max(6, ceil(2*sqrt(7k))) + 2 rows by board_rows + 2 triangles listed per k in object/mx_k2_20_bounded_unsat.json (10x12 at k=2 up to 26x28 at k=19 and 20) is unsatisfiable, with CaDiCaL 3.0.1 reporting UNSAT and drat-trim reporting s VERIFIED on its DRAT proof (archived as heptiamond-MX-k2-20-proofs.tar.xz, 175028808 bytes, sha256 6fc6276d9ba8f6b61cc4bde2a5210dbccd23ee47c9904c6bcac1df50c350b1be, at https://doi.org/10.5281/zenodo.24518087), so no figure of area 7k inside that board (connected or not, with or without holes) can be tiled both by k copies of M and by k copies of X; for k = 2..5 an independent board-free exhaustive search also finds no common figure; nothing is claimed for figures outside the stated boards, for k > 20, or about incompatibility of M and X.

## Verdict
The claim fits p3 as a clearly labelled bounded impossibility, and the scope sentence above is supported by the
files and my checks. Conditions: (a) the gate stays PROMISING and CONFIRMED_PARTIAL is not written until the Zenodo
record is published and its public file is checked for 175028808 bytes and sha256 6fc6276d...; (b) remove
verify-it-yourself/__pycache__/ before regenerating SHA256SUMS; (c) live re-fetch of 7compat.html immediately
before submitting.

pass: true
