status: CONFIRMED_PARTIAL
confirmed_scope: dom(Q_11) <= 19, one below the upper bound 20 of Table 1 of Lauri's Corrigendum (upper bound only), certified for each of two CNF encodings written in separate contexts (formulas/enc1/Fbase.cnf and formulas/enc2/Fbase.cnf, which besides the partition and domination clauses contain, as premises not derived in any proof, two-way definitions of auxiliary variables and symmetry breaking on class labels) not by one proof but by a chain of 681 refutations per encoding, each with its own DRAT proof checked by drat-trim (a Windows build of the unmodified upstream source) and composed by a clause-inclusion argument checked by scripts, the generators of both encodings accepting the authors' own unpublished 19-partition and Lauri's published 18-partition as satisfiable cases.
table_fetched_utc: 2026-11-12T00:50:25Z
partial_win: p2 of the bank target queens-graph-domatic-numbers ("A DRAT-certified upper bound improvement for one of the open pairs, with two independently written encodings agreeing.")

# Honesty gate, run 2026-11-11-2141 (written by the run's main session, 2026-11-12T03:11Z)

I read the three panel files myself, in full: reproduce.md (ends pass: true), novelty.md (ends pass: true),
criterion.md (ends pass: true, conditional). Each was written by a subagent started in a fresh context (Claude Code
Agent tool, model Opus 5.5); none saw another panel file. The confirmed_scope above is the CRITERION skeptic's sentence,
copied without change. The status stands only if kit/check_run.py prints CHECK_RUN: PASS; the full success criterion
of the target is NOT claimed (CRITERION: "not met to the letter").

## The two conditions of the CRITERION skeptic, and whether they hold

1. "every drat-trim verdict the claim relies on being confirmed": REPRODUCE re-ran all of them with the checker of
   claim/checker/bin: 680 of 680 and 680 of 680 chain checks with exactly one line "s VERIFIED" and exit code 0
   (its section 4), and both final steps "s VERIFIED" (its section 1: enc1 6,114.0 s, enc2 6,310.5 s, proof bytes read
   equal to the file sizes). For the final step of enc2 this was the first verdict in the folder; the author's own
   check of the same pair ended later, at 01:04:25Z, also "s VERIFIED" (attempts/counting-in-proof/report.md). Holds.
2. "the NOVELTY skeptic's live re-fetch showing dom(Q_11) still open at 18-20": fetched 2026-11-12T00:50:25Z, HTTP 200,
   same sha256 as the run's fetch, cell 18-20; OEIS A292192 has no term for n = 11; no later paper found. Holds. The
   fetch is less than 6 hours old at the time of this gate, so it was not repeated.

## Downgrade triggers of RUN.md step 7, one by one

- A hedging panelist: none hedges on what it checked. CRITERION's pass is conditional on two facts supplied by the
  other two reports (above). Its "met only with disclosure" points are written into the scope sentence.
- A reproduction mismatch: none ("No mismatch between the files and CLAIM.md / REPRODUCE.md was found"). The 570
  piece targets of enc1 that REPRODUCE reads as one literal stronger than described subsume the described ones.
- Not strictly better than the live table: 19 is strictly below the table's 20.
- A stretched criterion or hidden quantifier: two points, both judged by CRITERION and both disclosed in the scope;
  I state them again here because they are the points a reader may weigh differently, and I did not downgrade on them.
  (a) "DRAT-certified": there is no single DRAT proof and no solver run on the whole formula. There are 681 DRAT
      proofs per encoding and one non-DRAT step, the rule "if every clause of G follows from Fbase and G with the
      negation of C is refuted, then Fbase implies C", whose side conditions (which clauses each file contains) were
      checked by four programs written separately: the author's two, CRITERION's and REPRODUCE's. The partial win's
      wording does not ask for one proof; the full criterion's evidence clause does, and it is not claimed.
  (b) "two independently written encodings": that enc2.py was written without reading enc1.py is the author's
      statement; the brief given to its writer is not archived in the workspace and it prescribed the same design.
      The scope therefore says "written in separate contexts". What protects against a shared design error is not the
      second encoding but the checks that use no encoder: REPRODUCE's formula_check.py (written from the definition
      before reading any author program: every clause of each Fbase is true for a domatic 20-partition, 0
      unaccounted), CRITERION's semantic_check.py and the author's formula_audit.py.
- A scope wider than what was reproduced: every part of the sentence was reproduced by a skeptic except the
  parenthesis "(a Windows build of the unmodified upstream source)", which REPRODUCE lists under "could not check".
  I checked it myself for this gate (two checks, below); these are the author session's checks, not panel checks.
- A sample presented as complete / a capped search used as an exclusion: no. All 1,362 checks were re-run, none sampled.
- Several objects bundled as one claim: one bound; the two encodings certify the same statement.

## Checks made for this gate (files in panel/gate-checks/)

1. upstream-drat-trim.txt: one GET of drat-trim.c at the pinned upstream commit 2e3b2dc0 (2026-11-12T03:09:48Z, HTTP
   200, 59,546 bytes): byte-identical to claim/checker/src/drat-trim.c (sha256 d834b649...c2ee).
2. rebuild.txt: drat-trim-bin.exe rebuilt from claim/checker/src with the documented command. Same size; 20 bytes
   differ, all of them build stamps (the PE TimeDateStamp, two timestamp fields of the debug directory, 8 bytes of
   the CodeView GUID); the sections .text, .rdata, .data, .pdata, .tls and .reloc are byte-identical.

## What happened after the claim folder was built (00:48Z), so that the panel did not see it

- The author's own final-step check of enc2 ended at 01:04:25Z: "s VERIFIED" after 6,990.3 s.
- A second proof checker written from the definition (attempts/second-checker) accepted all 1,360 proofs of the chain
  (attempts/verify-chain/output/second-checker-*.txt; last file ended 02:59Z). It was not run on the two final proofs.
- Note added 2026-11-12T10:15Z, before any submission (the only change to this file since 03:11Z): after this gate
  was written the second checker was run on the two final proofs (03:13:58Z to 04:41Z, both of its deletion modes,
  limit 5,200 s of processor time per run). All four runs ended with "s TIMEOUT": no verdict, neither accepted nor
  rejected (attempts/verify-chain/output/second-checker-final-*.txt). drat-trim remains the only checker for these
  two proofs; the status and the scope sentence above are unchanged.
- attempts/verify-chain/output/no-comment-lines.txt (03:02Z): none of the 1,364 formula files has a comment line
  after its header. I wrote this check after seeing REPRODUCE's pitfall test in its working folder, before its report;
  REPRODUCE's own lexical check (token_check.py) says the same.
- One file was MOVED out of claim/ after the panel ended (not deleted, not changed): claim/checker/bin/drat-trim.pdb,
  the debug-symbol by-product of compiling the text-mode checker, now in tmp-check/claim-moved-2141/. No command of
  the claim uses it. Reason: claim/ was assembled with hard links, this file kept its creation time (2026-11-11
  20:05:45Z, when the checker was compiled during the previous run, before this run's PREREG.md of 21:42:12Z), and
  kit/check_run.py reads any claim file older than PREREG.md as "PREREG.md was written after the claim was built".
  It was the only such file (checked with check_run's own function). The pre-registration did precede every
  measurement of this run: the first chain computation started at 22:12Z. No other file of claim/ was touched;
  no file of claim/ has a modification time after 00:49Z.

## Points raised by the panel that stay open, for the human and the maintainer

- NOVELTY: draft pull request #954 (same contributors, 2026-11-05) mentions, under "Not claimed", an earlier
  certificate of the same bound that is not in DRAT form. claim/CLAIM.md does not mention it; the package README does.
- CRITERION: the 22:02Z note on cutting the third lemma into 31 pieces is not in claim/prereg/ (it is in
  attempts/lemma3-pieces/NOTES.md); CLAIM.md's "681 solver refutations" is loose (the 40 glue steps are unit
  propagation; each final proof is a derivation followed by a solver refutation).
- REPRODUCE: drat-trim, with a binary proof, reads a comment line placed after the header of a formula as empty
  clauses and can answer "s VERIFIED" on a satisfiable formula. Not exploited here (no formula has such a line), but
  the author's parsers skip comment lines and would not have seen one. One checker implementation of record.
- Not checked by anyone in the panel: a rebuild of the proofs from the generators (REPRODUCE parts A6, B, C). The
  author's regen_formulas.py rebuilds all 1,360 formulas without a solver and matches every sha256.
- The proofs (79.5 GB) cannot be published; a reader has to rebuild them.
