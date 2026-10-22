# Honesty gate (RUN.md step 7): run 2026-10-17-2357, #23 site claim

Gate written 2026-10-18T07:42:22Z by the setup session (Claude Code, claude-opus-5-5), acting as the run's main
session after the run was cut off; the panel ran in three fresh subagent contexts started from this session, each
given only a copy of claim/ (claim/MANIFEST.sha256 rebuilt with the run's own manifest.py before the copies, because
the run had added table/literature_record.md after its manifest).

Read: panel/reproduce.md, panel/novelty.md, panel/criterion.md, all ending pass: true (reproduce.md re-read after its author reworded one housekeeping line to name no temporary path; verdict and findings unchanged).

Downgrade checks:
- Hedging panelist: none. CRITERION names its readings (the "for example" clause as illustrative; "within 3 sigma of
  the table value" with the table's error; "published BOND threshold" as the table's citation-needed #23 bond value)
  and its confirmed_scope states the last one explicitly. The bank's own statement calls the table's 8-digit bond
  entries "the bond thresholds on the same rows", so that reading is the bank's, not a stretch.
- Reproduction mismatch: none. Repair round: REPRODUCE recomputed the #23 site roots n = 9..16 with the claim's
  streamed program (bit-identical to the saved series) and the extrapolation (identical), and ran fresh-seed Monte
  Carlo at 64 x 16 (own evaluator, 0.21 sigma) and 96 x 24 (claimant's evaluator, 0.76 sigma), as the bank's
  verification method asks.
- Value strictly better than the live table: yes; NOVELTY fetched the table at 2026-10-18T05:11:54Z (HTTP 200,
  wikitext sha256 588b98d3...742ba3, unchanged): 0.5720(2) against 0.57176454(10). Fetch age at this gate under 6 h.
- Scope wider than reproduced, sample presented as complete, capped search as exclusion, bundling: none.
- Contrarian frozen stream test (runs/2026-10-17-2357/attempts/contrarian, kill criterion 5 if failed): STREAM CHECK:
  PASS (kagome, #23, triangular tiny tori at 60 blocks; pooled late-early -0.36 sigma).

status: CONFIRMED_SOLUTION
confirmed_scope: For 2-uniform lattice #23, (1/2)(3^3,4^2)+(1/2)(4^4), the site percolation threshold is 0.57176454 +- 0.00000010 by the frozen transfer-matrix extrapolation (n <= 16), and it agrees within 1.53 combined sigma with an independent Monte Carlo wrapping-probability value of 0.5717667 +- 0.0000014 on tori up to 512 x 128 cells, while the same transfer-matrix code reproduces the table's citation-needed #23 bond value 0.45844622(40) to 2e-7 and the exact kagome and (3,12^2) site thresholds, the value lies 1.2 table sigma from the table's 0.5720(2), and the recorded literature search found no published #23 site value more precise than 2e-4.
