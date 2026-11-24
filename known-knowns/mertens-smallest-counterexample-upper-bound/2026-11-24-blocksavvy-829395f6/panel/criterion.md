role: CRITERION
context: fresh subagent
claim: runs/2026-11-24-0728/claim_v3 (copied to sandbox/panel-0728v3-criterion/claim_v3; sha256sum -c SHA256SUMS.txt: 17/17 OK)
date_utc: 2026-11-24T12:15:31Z

## What I read
Only: PANEL_BRIEFS_v3.md (header + CRITERION), kit/RULES.md, the bank entry
mertens-smallest-counterexample-upper-bound (repo/bank/targets.json), and my copy of claim_v3/. I did not open
claim/, claim_v2/, panel/, panel_v2/, attempts/, notes/ or any other sandbox/panel-* folder.

## Criterion (bank p1, verbatim)
"An independent certified re-evaluation of Kim-Nguyen's best y values (Tables 1-2) for h_P and h_StR, confirming
or correcting their reported values to 3 decimals."

## Source check (one honest fetch)
GET https://arxiv.org/pdf/2502.21021v1, User-Agent "V3R1T4S-panel/1.0 (criterion skeptic; honest client)",
at 2026-11-24T12:14:02Z: HTTP 200, application/pdf, 828676 bytes, 17 pages,
sha256 3141e044428b0ec955407ef0ef44682faed61c36cc8b8cfec3b26587b5818f54 (same as the hash the claim gives for its excerpt).
Row count, done by me on my own pdftotext of that PDF: Table 1 ("Best values of y for the function hP") has 5 rows,
Table 2 ("... for the function hStR") has 14 rows, 19 in total. The 19 y strings in the PDF are, in order, exactly
inputs/Test-Pinch.txt + inputs/Test-ST.txt (string equality: True). Definitions (2.6) and (2.7) in the PDF
(k = 1.5e-6, gamma < 14000; k = 3e-9, gamma < 74000; alpha, psi) match CLAIM.md and code/verify_p1.py. (KNOWN)

## Independent classification (my own script, sandbox mycheck.py, sha256 fab92e81...12bdadd)
Written from scratch with Python Decimal on the shipped 320-bit balls (result/p1_certified_values.json) and the
printed values parsed from my own PDF text; half away from zero and toward zero applied to both ball endpoints.
Result (NUMERICAL, on the shipped balls; their certification is REPRODUCE's job, not re-done here):
- printed precision, rounding: 8 MISMATCH (T2 rows 1, 2, 4, 7, 9, 10, 12, 14), 0 ambiguous;
- printed precision, truncation: 6 MISMATCH (T1 row 4; T2 rows 1, 4, 6, 12, 14), 0 ambiguous;
- wrong under both conventions: T2 rows 1, 4, 12, 14 only. These four also stay wrong under floor and ceiling
  (I checked floor and ceiling at printed precision for these four rows: no directed rounding gives the printed digits), so
  calling them corrections at printed precision is convention-free;
- no ball straddles a 3-decimal boundary under either convention, so all 19 certified 3-decimal renderings are
  well defined; h_256 and h_320 agree for all 19;
- at 3 decimals (printed and certified rendered with the same convention): 15 rows agree under both conventions;
  T2 row 5 is printed with 2 decimals (-1.02) and agrees at 2 decimals only (certified -1.0206515: -1.021 rounded,
  -1.020 truncated); T2 rows 7 and 9 disagree only under rounding, T2 row 4 only under truncation. There is
  therefore NO convention-free correction at 3 decimals;
- the y+sqrt(y) column mixes conventions exactly as claimed (rounded only: T1 r4, T2 r2, r10, r12, r13;
  truncated only: T2 r7, r9, r14). The h column itself is also mixed (T1 r4 fits only rounding, T2 r7/r9 fit only
  truncation), so no single convention explains the print.
check/compare_printed.py run on my copy reproduces the same tables, and its JSON output is byte-identical to the
shipped file (deterministic).

## Hidden quantifiers and stretched definitions
1. All table rows: yes, 19 of 19, both tables, both functions (h_P for Table 1, h_StR for Table 2). Reading p1 as
   requiring cross-evaluation (Table 1 y under h_StR) is not supported: no reported value exists to confirm.
2. "Independent": the zeros were computed separately and the evaluator is separately written, but with the same
   Arb library (acb.zeta_zeros) that Kim-Nguyen used for h_StR; for h_P they used Hurst's zeros, so that table is
   source-independent. The claim states this caveat itself ("independent computation, not an independent method").
   The bank's own verification_method prescribes Arb zeros below 74,000, so the bank counts this as independent. Accepted.
3. "Certified": ball arithmetic over complete lists (index-rigorous isolation; the shipped counts are N = 14,950 and 98,625; I have not independently verified completeness). Caveat: the shipped balls were produced from v1 zero files written with arb `more=True`
   strings and were not recomputed; this rests on the 1,200-zero spot check and on REPRODUCE's own zeros. My pass
   is conditional on REPRODUCE confirming the balls.
4. "To 3 decimals": met as a deliverable (19 well-defined certified values at 3 decimals plus the balls). The claim
   does not stretch it: it says rows 1, 12, 14 agree at 3 decimals, that row 4 at 3 decimals and rows 7, 9 are
   convention-dependent, and that T2 row 5 is only a 2-decimal check. The four "corrections" are at printed
   precision (4 to 6 decimals), which is finer than p1 asks for. That is extra and true. It is not a 3-decimal correction claim.
5. Calling only T2 rows 1, 4, 12, 14 corrections and marking rows 2, 7, 9, 10 (and row 4 at 3 decimals)
   convention-dependent: justified by the mixed-convention evidence, and the most conservative labelling the data allow.
6. Edition scope: only arXiv v1 was compared directly (the bank's primary source arxiv.org/abs/2502.21021). The
   journal version and the ANTS PDF were not compared by me. The claim's corrections are of the arXiv v1 print.
7. Subsumption: the record cell (T2 row 3) was already re-evaluated by others, and the claim credits that. The
   other 18 rows plus the full table are what is new here. Kim-Nguyen's own Zenodo evaluator is not an independent
   re-evaluation. Whether this is already published elsewhere is NOVELTY's question. My pass assumes NOVELTY passes.
8. No overreach found: no new bound, no theorem-hypothesis claim, no "solved/first" wording.

## Concerns (non-blocking)
- Independence is computational, not methodological (same Arb zero routine for h_StR).
- The certified values rely on the v1 `more=True` zero strings plus a spot check, not a full recompute by the author.
- The "Corrections" heading could be misread as 3-decimal corrections. The text is explicit, but the gate summary
  should say "at printed precision".
- Journal (Res. Number Theory 11 (2025)) tables not compared.

confirmed_scope: For all 19 rows of Kim-Nguyen's arXiv:2502.21021v1 Tables 1-2 (5 for h_P, 14 for h_StR), the claim gives certified 320-bit ball values of h at the exact published y, computed from separately computed Arb zeros and well defined at 3 decimals under both rounding and truncation; at 3 decimals they agree with the print for 15 rows under both conventions, for Table 2 row 5 only at its printed 2 decimals, and convention-dependently for Table 2 rows 4, 7 and 9; and at printed precision Table 2 rows 1, 4, 12 and 14 are wrong under either convention.

pass: true
