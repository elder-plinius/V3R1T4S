# Honesty gate — dna-codes-gc-rc-king-table, (n,d) = (20,15)

status: CONFIRMED_SOLUTION
confirmed_scope: The 16-word list in object/code_20_15_16.json is a valid length-20 DNA code with GC count 10, minimum Hamming distance 15 and reverse-complement distance at least 15 (self-pairs included), so A_4^GC,RC(20,15,10) >= 16, exceeding the unmarked live King-table entry 15 (re-fetched 2026-10-17T23:07Z) and every post-2010 published value for (20,15) found in the sources checked (all 15), with one paywalled 2023 IEEE TIT paper unread.

Read by the main session on 2026-10-17T23:35Z (UTC).

- reproduce.md: pass. Own checker written before the author's; sha256 matches; 16 words, GC 10, min distance 15, min RC distance 15 (self 16). Started with procedural steps written by the main session (no source hints).
- novelty.md: pass. Protocol-only instruction; claim/ held three source PDFs the human downloaded after automated 403s. Live table fetched once at 2026-10-17T23:07:32Z: (20,15) = 15^v, unmarked. Aboluion 2012 Table 9, Aboluion 2011 thesis Table 10.72, Montemanni-Smith-Koul 2014 Table 2: all 15. Blocked: arXiv API (429).
- criterion.md: pass. Full criterion, not a partial win; w fixed at 10 (the max-over-w tables still give 15); halving-gap does not apply.
- Unread source named in the scope: Dougherty, Korban, Sahinkaya, Ustun, IEEE Trans. Inf. Theory 69(3) 2023, doi:10.1109/TIT.2022.3217518 (paywalled). The same group's open preprint arXiv 2108.02033 (same method) treats lengths 16, 24, 32, 36, 48, 56, 60, 64, 72 only, not 20. The scope keeps this caveat.
- Superseded panel runs kept for the record: novelty_protocol_run1.md (pass: false; its own save bug lost the single table fetch, and the 2012 paper was blocked), novelty_hinted.md (pass: false; the main session had listed sources in its instruction, so it is not a protocol panelist; blocked by the same 403s), criterion_run1_hinted.md (pass: false; extra instructions from the main session, literature clause unestablished). Both failures were missing inputs, now supplied; no failure was a contrary finding.
- Table fetch age at gate: under 1 hour.
