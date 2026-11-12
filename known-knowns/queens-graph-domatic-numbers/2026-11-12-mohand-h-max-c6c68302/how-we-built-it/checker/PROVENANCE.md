# SAT tooling of this workspace (authorised by the human operator on 2026-11-11)

Everything lives inside the workspace. Nothing was installed system-wide, no prebuilt checker binary was downloaded.

- venv-sat/ : Python 3.14 virtual environment.
  - python-sat 1.9.dev22 (pip, prebuilt wheel): CaDiCaL 1.5.3 and 1.9.5, Glucose 3 and 4, Lingeling give DRAT proofs
    through `Solver(..., with_proof=True)` and `get_proof()`.
  - ziglang 0.17.1 (pip, prebuilt wheel, 101.9 MB): used only as a C compiler (`python -m ziglang cc`).
- tools/drat-trim/src/drat-trim.c : fetched once 2026-11-11T20:04:51Z from
  https://raw.githubusercontent.com/marijnheule/drat-trim/master/drat-trim.c , HTTP 200, 59546 bytes,
  sha256 d834b649f437e091597f5347f259b9f681087f89ca0844d0cee250a1a1a0c2ee. Upstream master at fetch time: commit
  2e3b2dc0ecf938addbd779d42877b6ed69d9a985 (2024-11-25). Licence file fetched with it (MIT-style permission notice,
  sha256 71ab2a9dc5a294ad8fba4ccb8c45aaa8a439596d314a2a046ac9b62266872a18). Source read before use: file input/output
  only; it deletes the proof file only when its own delete option is passed (never used here).
- tools/drat-trim/bin/drat-trim.exe : compiled here, source unmodified, with
  `python -m ziglang cc -O2 -Dgetc_unlocked=getc -o bin/drat-trim.exe src/drat-trim.c`
  (the define maps a POSIX-only function to its standard equivalent on Windows).
  sha256 d543948c3900c616735ab32fc34364af1520f36d395fde1cbf930759eb0d53b2.
- Self-test (tools/drat-trim/selftest.py, output in selftest-output.txt, 2026-11-11T20:05:58Z): pigeonhole 6/5 proofs
  from CaDiCaL and Glucose are VERIFIED; a proof with every second lemma removed and a genuine proof checked against a
  satisfiable formula are NOT VERIFIED. SELFTEST: PASS.

Use: write the CNF and the proof with LF line endings, then `bin/drat-trim.exe formula.cnf proof.drat`; the line
`s VERIFIED` is the only accepted outcome. The bank also asks for two independently written encodings and for the
neighbouring satisfiable case to be found SAT.

## Binary-mode build (added 2026-11-11T21:59:42Z)

The first build opens files in Windows text mode, which mangles BINARY DRAT proofs (its self-test on a binary proof:
NOT VERIFIED, see selftest-bin-output.txt). A second executable, bin/drat-trim-bin.exe, is the same unmodified
drat-trim.c compiled together with src/binmode.c (five lines written here: a constructor that sets the C runtime to
binary file mode before main):
    python -m ziglang cc -O2 -Dgetc_unlocked=getc -o bin/drat-trim-bin.exe src/drat-trim.c src/binmode.c
sha256 of the executable and of binmode.c: last lines of selftest-bin-output.txt.
Self-tests (selftest_bin.py and selftest.py, both run on drat-trim-bin.exe): a genuine binary proof containing the
bytes 0x0D, 0x0A and 0x1A is VERIFIED; a cut proof and a proof against a satisfiable formula are NOT VERIFIED; the text
self-test still passes. Use drat-trim-bin.exe for binary proofs and either build for text proofs with LF line endings.

## What "unmodified" means here, and a size limit of these builds (added 2026-11-11T23:02Z)

- The file src/drat-trim.c is byte-identical to the upstream file (sha256 above). The builds differ from an upstream
  `make` in exactly two ways, both visible in the compile commands: the compile-time define `-Dgetc_unlocked=getc`
  (Windows has no getc_unlocked; getc is its locked equivalent) and, for drat-trim-bin.exe only, the extra file
  src/binmode.c, which changes nothing but the file mode (binary instead of text) of the C runtime.
- Data model: `python -m ziglang cc` targets 64-bit Windows, where the C type `long` has 32 bits (on Linux and macOS it
  has 64). drat-trim stores clause positions in variables of type `long`, shifted left by two bits, so these two
  executables are only reliable while the clause database (formula plus all proof clauses, four bytes per literal
  plus four integers per clause) stays below 2^29 integers, about 2 GB. Past that limit the positions would overflow.
  Every proof checked in this workspace is far below it (largest so far: a binary proof of about 150 MB, a database
  of a few hundred MB). A proof of several GB must not be checked with these builds.
- Default time limit of drat-trim: 40000 s per check; a check that runs out prints `s TIMEOUT`, which is not accepted.
- A visible effect of the same 32-bit type, seen on 2026-11-12: drat-trim's own last line "c verification time" is
  wrong for a check that lasts more than 2147 s. A check that took 5694.6 s by the clock of the calling script was
  reported as "verification time: 1399.570 seconds" (5694.57 s minus 2^32 microseconds). The verdict line is not
  affected; durations quoted in this workspace are those measured by the calling scripts.
