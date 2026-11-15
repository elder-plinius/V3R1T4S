# Honesty gate — run 2026-10-20-2306, langton-ant-highway, bank partial win p1
gate written: 2026-10-21T03:06Z (date -u) by the run's main session, after reading all panel files.
status: CONFIRMED_PARTIAL
confirmed_scope: All 2^36 black-cell patterns of the 6x6 box x,y in -2..3, with the ant at (0,0) facing north, are reported by the lant4 exhaustive run (attested by per-chunk summaries and sha256, 3 chunks reproduced) to reach the period-104 (+-2,+-2) highway by T_cap <= 375,545 under a certificate I verified to be sound; the independent simulator lantx2, with its own sound certificate, re-captured a frozen hash-uniform 1.000057% sample and all 4096 per-chunk maximum-T_cap masks with no failure, which meets bank partial win p1 for this one box placement and heading.
partial win: p1 (only). The full success criterion (a counterexample, or a formal proof of the conjecture) is not claimed and not met.

## Panel record (plain)
- NOVELTY (novelty.md): pass. arXiv 2505.05426 fetched 2026-10-21T01:08:18Z (HTTP 200, only v1); Zenodo 21716510 and arXiv 2606.26677 read; TROPHY_CASE.md has no entry; no prior exhaustive certified 6x6-or-larger box verification found. Caveat it states: only the first 100 open pull requests (created 2026-10-19T06:29Z onward) were inspected.
- CRITERION (criterion.md): pass, with the confirmed_scope above. NOTE: this vote was cast on the claim BEFORE the fix below: METHOD.md section 2 then gave lant4's certificate C(s) only as a sketch and wrongly said checkC uses the grid at the detection step t. The criterion reviewer proved C(s) sound itself and flagged the t-versus-s error. The fix (claim/CHANGES.md) only replaced the sketch with a full proof of that same certificate and corrected the wording; the claim sentence, data and numbers did not change. I judge that the vote carries over; I did not re-run the criterion reviewer.
- REPRODUCE, round 1 (reproduce.round1-fail.md, kept unchanged): FAIL. Reasons: (a) within its session budget it re-simulated only about 0.65% of the masks (part of the 1% sample), and a partial sample cannot pass; (b) C(s) was only sketched (and the t-versus-s error).
- REPRODUCE, round 2 (reproduce.md; written by a new fresh reviewer on the fixed claim, prompt attempts/panel-prompts/reproduce2.prompt.txt; the file was saved as reproduce2.md and renamed to reproduce.md for this gate, content unchanged): pass. With its own C simulator and certificate, written before it opened code/, it re-simulated all 16,384 sample units (687,234,013 masks) with all of them captured and 16,384 of 16,384 units equal in n, CAP, UNCAP+OOB, maxtcap, maxtcap_mask and sumtcap. It also matched all 4096 hard cases and all 65,536 4x4 masks. It re-derived both certificate proofs as sound. It only consistency-checked the exhaustive lant4 run itself.
- File sha256 at gate time: criterion.md 43938c72..., novelty.md aa39cd08..., reproduce.md f491ec95..., reproduce.round1-fail.md c1d3c1e4....

## Downgrade check (kit/RUN.md step 7)
- Hedging panelist: no. Each passing verdict states its caveats and passes outright.
- Reproduction mismatch: none in round 2. The round-1 failure was about coverage and documentation, not a wrong number.
- Table value: not a numeric record. Novelty is status-based, and the fetch is 2 h old (within 6 h).
- Stretched criterion or hidden quantifier: these were weighed by CRITERION, which passed them on disclosed readings.
  - one box placement, with the ant at (0,0) facing north;
  - "all hard cases" read as the per-chunk maxima, given that there were 0 UNCAP, OOB or fix-up masks;
  - the exhaustive part is attested by per-chunk summaries plus sha256, with 3 chunks reproduced.
  The scope sentence names all three, so it is no wider than the evidence.
- Sample presented as complete: no. The scope separates the exhaustive run (lant4, summaries) from the independent re-check (1.000057% sample plus hard cases).
- Capped search used as an exclusion: no. The cap only bounds capture, and no mask was uncaptured.
- Several objects bundled: no. This is one claim, one box.
Result: no downgrade. Final status CONFIRMED_PARTIAL (p1), subject to CHECK_RUN: PASS.
