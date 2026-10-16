# Novelty skeptic (scu N=83, p3), re-run 2026-10-16

Inputs: this package plus novelty-evidence/ only (fresh Packomania fetches 2026-10-16 02:37-02:41 UTC, hashes in novelty-evidence/EVIDENCE_SHA256SUMS).

## Findings
- Still current: live https://packomania.com/scu/txt/scu83.txt (sha256 cc08dcaf…1c62, Last-Modified Tue, 28 Feb 2012 07:05:00 GMT) is byte-identical to the-record-we-beat/scu83-posted.txt; live radius.txt row 83 is unchanged (0.116285160418976515059766617287). how-we-built-it/mp_recheck.py on the live files, cores 4-7: r*-cell = -7.18581149e-7. The mismatch is live and unfixed.
- Not previously reported (Packomania): scu.html "History of updates" (08-Feb-2012 to 08-Oct-2026, novelty-evidence/scu_scu.html) has no entry about an error, wrong file, correction or replacement for any N (text search for wrong|error|incorrect|mistake|discrepan|overlap|infeasib|fixed|replac: no hits). The last entry naming N = 83 is 29-Jun-2018 (improvement by Bagattini, Schoen and Tigli); no 2026 update lists 83.
- pending-requests.html (08-Oct-2026): no scu row. The 26-Sep-2026 Moki & Julio "*many* 4666 candidates" row names no category or N; it could later change this row, which README states as a caveat, but it is not a report of this flaw.
- No other history/errata page exists: /scu.html, /history.html, /news.html return 404; the homepage links none. Per-N page scu83.html shows no remark.
- Not checked: private correspondence with E. Specht, papers or other sites. Scope of "not reported" is Packomania's public pages.

novelty: current (not fixed); not previously reported on Packomania (history + pending requests checked)
context: executor subagent; re-read only this package and novelty-evidence/ (earlier panel verdicts not used as evidence)
pass: true
