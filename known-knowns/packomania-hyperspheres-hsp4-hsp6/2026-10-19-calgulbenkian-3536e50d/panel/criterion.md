# criterion, hsp4 N=170
context: Claude Code subagent, fresh context [Sonnet 5.5]

Literal criterion (hsp, d=4): r* = min(half min pair distance, 1 - max |c_i|) at 50 digits, no tolerance, strictly greater than the live 12-decimal row for N by >= 1e-10; AND sorted pairwise-distance multisets differ by more than 1e-8 somewhere from the posted N=170 file; AND (d, N) not in a newer History entry; queue rule; the verdict must state the *many* caveat.

My own check (exact rationals, all 14365 pairs, 60-digit roots): r* = 0.215645059468390008128190279493; wall-limited (half min pair distance 0.2156450644). The file header radius differs in the 17th digit; the criterion reads the coordinates, so the header is irrelevant.

Clauses:
- Greater than live row (0.215589695168) by >= 1e-10: MET, gain 5.536e-5.
- Propagated bar: the live hsp4 rows decrease with N (row 171 is 0.215441346347, and so on), so the largest row at N' >= 170 is the row for 170 itself; nothing to propagate. MET.
- Non-isometry to the posted file: MET (largest sorted-distance difference 9.0e-3, far above 1e-8; both files have 4 coordinates here, so the comparison is well defined for d=4).
- History: MET (hsp4 page entries are July 2025 only, page hash unchanged).
- Queue: MET (hsp4 not named). *many* bundle caveat UNRESOLVED; the cell's copy of the manifest row (0.2155917530, tagged NEW ARRANGEMENT) is below the claim by 5.3e-5 but was not re-fetched.
- Refile: same object as closed PR #106 (bulk close, not for defect), per the the contributor's review ruling R1 not a competing value.
Live fetch (once, honest client, no retries; the saved pages are not shipped in this package): 2026-10-19T05:38Z, HTTP 200 for the hsp4 and hsp5 radius tables and the hsp4, hsp5 and pending-requests pages; every sha256 equals the one recorded in the cell's the-record-we-beat/README.md, so the tables and pages are unchanged since the claim's fetch. History pages show no entry newer than the claim's; no pending-requests entry names hsp4 or hsp5; the 26-Sep-2026 'many' bundle (4666 candidates, category unspecified) is still listed and cannot be resolved, so the criterion's own caveat applies and is stated here.

confirmed_scope: A 170-point packing in the unit 4-ball with exact feasible radius 0.2156450594683900081 (checked here), above the live Packomania hsp4 row for N=170 (0.215589695168) by 5.5e-5 and non-isometric to the posted file; the unresolved Moki and Julio bundle could still hold an equal or higher value.
pass: true
