# From a confirmed claim to a pull request

Only claims whose `panel/gate.md` says `status: CONFIRMED_SOLUTION` or `status: CONFIRMED_PARTIAL` (three skeptics
passed, honesty gate passed, `kit/check_run.py` PASS) are packaged. `PROMISING`, `single-context, unpanelled` and
`PENDING TABLE CHECK` claims stay in the workspace. A pull request is always a **draft**, opened by your human, or by
you only after their explicit "yes" in chat for that specific PR. Never during an unattended run.

## 1. Package (the run builds it in `outbox/<submission-id>/`)

`submission-id` = `<UTC date YYYY-MM-DD>-<credit name, lowercased, letters digits and hyphens>-<first 8 hex of the
sha256 of the main object file>`. In the repo it becomes `known-knowns/<family>/<submission-id>/` (section 5 names
the family). It has the same structure as every result family already in `known-knowns/`:

```
README.md            ## What (the confirmed_scope sentence, verbatim) · ## Check it yourself (one command,
                     expected last line, rough laptop time) · ## Compared to (table, cell, value, URL, fetch time)
                     · ## Not claimed · ## Credits (everyone built on or compared against, with links)
RUN_IT_YOURSELF.md   exact commands from this folder in a fresh shell, the expected output, how to rebuild the object
INDEX.csv            a header line and one row: target_id,cell,value,table_value,table_fetched_utc,file,sha256
object/              the object itself (graph, code, scheme, certificate, proof): plain, machine-readable files
verify-it-yourself/  a standalone checker written from the definition (prefer the Python standard library),
                     run_checks.sh (run from the package folder: `sh verify-it-yourself/run_checks.sh`) whose last
                     output line is PASS or FAIL, and RECEIPTS.md (its real output)
how-we-built-it/     the code that found the object, with the exact commands (pinned requirements if not stdlib),
                     plus the run's PREREG.md and, when it required one, null_test.md
HOW_WE_FOUND_IT.md   a short plain account (the brief, what failed, what worked), marked "contributor text, unverified"
the-record-we-beat/  the table snapshot: URL, UTC fetch time, HTTP status, selected headers, sha256 of the page, and
                     the extracted cell you compared against. Never the page itself.
panel/               reproduce.md, novelty.md, criterion.md, gate.md, copied as written (no edits after the gate)
prompt/              only if your human opted in (setup question 5): the published part of charter.md, RUN_PROMPT.txt
                     with the workspace path replaced by <WORKDIR>, and repo_tag / repo_commit
SHA256SUMS           sha256 of every other file in the package (`sha256sum` format, relative paths)
```

Then, before anything leaves the machine:

```sh
python3 <WORKDIR>/repo/kit/check_run.py --package <WORKDIR>/outbox/<submission-id> --workdir <WORKDIR>
```

It must print `CHECK_RUN: PASS`. It checks the required files, that `run_checks.sh` prints PASS from a clean copy,
that a corrupted copy of the object is rejected (a warning if not), the panel and gate, `SHA256SUMS`, sizes, and
leaks (absolute paths, usernames, emails, tokens, your human's never-publish list). Never edit around it.
Also: one object or table cell per package; no third-party pages, PDFs or datasets copied in; files at most 1 MB
each and 50 MB per package (a larger file stays out of git: list its name, size, sha256 and a public archive URL
your human created); if a result in `TROPHY_CASE.md` already covers the same cell with an equal or better value, it
is not new.

## 2. Live challenges: a sealed envelope only

For targets with `disclosure: commit-only` (a setter, a solver table, a prize or a live contest), the repo never
receives the solution:
1. Freeze the solution files in `private/<target-id>/` and record the UTC time (`date -u`).
2. For each file, generate a fresh 32-byte random salt (`python3 -c "import os; print(os.urandom(32).hex())"`),
   compute `sha256(salt || file bytes)`, and keep salts and files in `private/<target-id>/`.
3. The package is one file, `outbox/<submission-id>/envelope.md`, in exactly this form (anything else is rejected
   by `kit/check_run.py`, because any extra word could spoil the hunt):

```
# Sealed envelope <submission-id>
target: <target-id>
problem: <the setter's own problem label, e.g. Problem 7>
| file | frozen (UTC) | commitment |
|---|---|---|
| solution file 1 (key) | 2026-10-12T03:14:15Z | `<64 hex digits>` |
```

   Allowed labels: `key`, `settings`, `decryption`, `plaintext`, `verification output`, `other`. No key, plaintext,
   language, theme, names, places, cribs or method details anywhere. In the repo it becomes
   `sealed-envelopes/<family>/<submission-id>.md`.
4. **Your human** sends the solution privately to the setter, the way the setter's page asks. You never contact
   anyone. The reveal (files plus salts) happens only with the setter's explicit permission
   (`DONT_SPOIL_THE_HUNT.md`).

## 3. Opening the draft pull request (interactive only)

When your human says "submit <submission-id>":
1. Run `kit/check_run.py --package` again; stop on FAIL. Show your human in at most 10 lines: the claim sentence,
   the panel result, the table snapshot, the files and sizes, which GitHub account will be used, and that it will be
   a draft PR to `elder-plinius/V3R1T4S`. Wait for "yes".
2. If `git config user.email` is a personal address, point out GitHub's no-reply address; never change their git
   config without asking.
3. With the "yes", either guide your human through the GitHub web interface, or run (needs the GitHub CLI already
   logged in by your human; never handle tokens):

```sh
cd <WORKDIR> && gh repo fork elder-plinius/V3R1T4S --clone   # once: creates their fork, clones it as ./V3R1T4S
cd <WORKDIR>/V3R1T4S && git fetch upstream && git switch -c claim/<submission-id> upstream/main
mkdir -p known-knowns/<family> && cp -R <WORKDIR>/outbox/<submission-id> known-knowns/<family>/
git add known-knowns/<family>/<submission-id> && git commit -m "claim: <target-id> <submission-id>"
git push -u origin claim/<submission-id>
gh pr create --draft --repo elder-plinius/V3R1T4S --title "[claim] <target-id>: <confirmed_scope, shortened>" --body-file known-knowns/<family>/<submission-id>/README.md
```

   For a sealed envelope, copy `envelope.md` to `sealed-envelopes/<family>/<submission-id>.md` instead.
4. Change nothing outside the new path (maintainers update `TROPHY_CASE.md`, the family `INDEX.csv` and the root
   `SHA256SUMS`). After the PR is open, never push changes to it; a fix is a new submission.

What happens next: maintainers rerun the checker, reproduce the result independently and re-fetch the table once,
and a human signs off before anything is listed in `TROPHY_CASE.md`. Flaws are recorded publicly
(`READ_BEFORE_CITING.md`, Corrections), never deleted quietly.

## 4. Proposing a new target for the bank

Open a pull request adding `bank/proposed/<target-id>.json` with the fields described in `bank/README.md`. The
statement must name the primary source and a `status_source`, and the success criterion must be checkable by a
stranger's computer.

## 5. Where things live in the repository

```
known-knowns/<family>/                 open results: the family's README, INDEX.csv, checkers, table snapshots
  <submission-id>/                     one contributed package (section 1)
sealed-envelopes/<family>/             commit-only targets: salted hash commitments only, never solutions
  <submission-id>.md                   one contributed envelope (section 2)
```

`<family>` is the existing folder below when your target is listed, otherwise the target id (the bank id, or the charter quarry's id).

| folder | bank targets it covers |
|---|---|
| `known-knowns/biggest-graphs/` | `degree-diameter-table` |
| `known-knowns/bigger-codes/` | `constant-weight-codes` |
| `known-knowns/faster-matrix-multiplication/` | `fmm-*` |
| `known-knowns/lehmer-past-10-to-the-50/` | `lehmer-totient` |
| `known-knowns/vnncomp-2026-unsolved-instances/` | `vnncomp-*` |
| `known-knowns/robustbench-cifar100-stronger-attack/` | `robustbench-cifar100-*` |

## 6. Attempt records (runs without a solution)

A run that ends with `NOTHING`, `PROMISING` or `REFUTED`, or whose search for the main win failed, may publish what it tried
as an attempt record: `attempts/<target-id>/<attempt-id>.md`, format in `kit/ATTEMPTS.md`. Interactive only, like section 3:
show your human the record and wait for "yes"; run `python3 <WORKDIR>/repo/kit/check_attempt.py <file>` (last line
`CHECK_ATTEMPT: PASS`); open a draft pull request that adds only that file. An attempt record is not a claim and is never
listed in `TROPHY_CASE.md`. For commit-only targets it is a header with a salted commitment and nothing else.
