# criterion, scu N=733
context: Claude Code subagent, fresh context [Sonnet 5.5]

Literal criterion (success for scu, N listed in the radius table): r* = min(half min pair distance, 1/2 - max |coord|) at 50 digits, no tolerance, STRICTLY greater than the live row for N by at least 1e-11; AND not isometric to the posted N=733 file (sorted distance multisets differ); AND N not in a newer History line; AND queue rule; centred coordinates.

My own check (exact rational arithmetic on the printed decimals, all pairs, 60-digit roots, script written from the definition): N=733, r* = 0.0589437529548279448024778. The pair bound is the binding one; the wall bound is slightly larger (positive wall slack), so r* is the half minimum distance.

Clauses:
- Strictly greater than the live row for N by >= 1e-11: MET. Live row 0.058531064607; gain 4.1269e-4.
- Hidden-quantifier check (comparison set). The row for N=733 is below its neighbours (the same 0.0585310646 value sits at several N, a leftover fill), so the honest bar is the larger of the row and every row N' > N (a packing of N' spheres gives one of N). From the live file for N' up to 1000 the largest is 0.058943675866 at N'=734. The claimed r* exceeds that propagated bar by 7.709e-8, far above the 1e-11 margin: MET against the propagated bar as well. The win is not implied by the table by deletion alone; it needs the re-jam, which is the strict gain.
- Not isometric to the posted N=733 file: MET literally (largest sorted-distance difference about 7.7e-2 read from the cell's own comparison; posted file is a different, stale arrangement). Reading the clause against the packing the object was derived from (one sphere deleted from the posted N=734 packing and re-jammed) is not what the criterion says; PR #350 propagation: the object is not a value that follows from the table by a standard rule (deletion gives exactly the larger row; the object is strictly above it), so I treat it as a separate, if small, record.
- N not in a newer History-of-updates line: MET (page hash unchanged; no 2026 entry names N=733, though neighbours were updated on 17-Oct-2026 and the table was 'reorganized'; the row could still be revised, which would only raise the bar).
- Queue rule: MET for scu (not named); the *many* bundle caveat is UNRESOLVED and must be restated in the verdict; the cell's manifest copy (manifest N=733: 0.0588218693815) is below the claim and was not re-fetched.
- Exact-evaluation reading (20-decimal coordinates evaluated exactly): acceptable, it is stricter than a tolerance reading.
Live fetch (once, honest client, no retries; the saved pages are not shipped in this package): 2026-10-19T05:38Z, HTTP 200 for the scu radius table and the scu and pending-requests pages; every sha256 equals the one recorded in the cell's the-record-we-beat/README.md, so the tables and pages are unchanged since the claim's fetch. History pages show no entry newer than the claim's; no pending-requests entry names scu; the 26-Sep-2026 'many' bundle (4666 candidates, category unspecified) is still listed and cannot be resolved, so the criterion's own caveat applies and is stated here.

Weakness to carry forward: the gain over the propagated bar is tiny in relative terms; it is real under the literal wording.

confirmed_scope: The point file in this cell is a valid cube packing with exact feasible radius r* = 0.0589437529548279448024778 (checked here), strictly above both the live Packomania scu row for N=733 and the best live row at any larger N up to 1000, with the posted file non-isometric; whether the unresolved Moki and Julio bundle or a later table revision already holds a higher value is not decidable from the folder.
pass: true
