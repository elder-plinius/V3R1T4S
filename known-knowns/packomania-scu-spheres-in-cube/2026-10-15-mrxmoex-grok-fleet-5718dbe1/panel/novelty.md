# Novelty skeptic (scu N=507, p3), re-run 2026-10-16

Inputs: this package plus novelty-evidence/ only (fresh Packomania fetches 2026-10-16 02:37-02:41 UTC, hashes in novelty-evidence/EVIDENCE_SHA256SUMS).

## Findings
- Still current: live https://packomania.com/scu/txt/scu507.txt (sha256 a62939a8…8a04, Last-Modified Fri, 01 Jun 2012 20:54:00 GMT) is byte-identical to the-record-we-beat/scu507-posted.txt; live radius.txt row 507 is unchanged (0.065932119200351706079281328718). how-we-built-it/mp_recheck.py on the live files, cores 4-7: r*-cell = -3.761186769e-6. The mismatch is live and unfixed.
- Not previously reported (Packomania): scu.html "History of updates" (08-Feb-2012 to 08-Oct-2026, novelty-evidence/scu_scu.html) has no entry about an error, wrong file, correction or replacement for any N (text search for wrong|error|incorrect|mistake|discrepan|overlap|infeasib|fixed|replac: no hits). The last entry naming N = 507 is 25-Jun-2013 (improvement by program Packntile); no 2026 update lists 507.
- pending-requests.html (08-Oct-2026): no scu row. The 26-Sep-2026 Moki & Julio "*many* 4666 candidates" row names no category or N; it could later change this row, which README states as a caveat, but it is not a report of this flaw.
- No other history/errata page exists: /scu.html, /history.html, /news.html return 404; the homepage links none. Per-N page scu507.html shows no remark.
- Not checked: private correspondence with E. Specht, papers or other sites. Scope of "not reported" is Packomania's public pages.

novelty: current (not fixed); not previously reported on Packomania (history + pending requests checked)
context: executor subagent; re-read only this package and novelty-evidence/ (earlier panel verdicts not used as evidence)
pass: true
