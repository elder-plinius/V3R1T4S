# Criterion skeptic: instance 80 (80_14_10_2), penalty 0 against best known 6

context: fresh subagent started for this claim only

Worked only from claim/. Nothing in claim/ was modified. `sha256sum -c SHA256SUMS` and `PREREG.sha256` both give OK.

## Clause-by-clause reading of the success criterion (target.md)

1. **"one instance listed on .../matsp/ with a positive Best known value"**: met. In data/matsp.html (227 rows) the row reads `80 | 14 | 10 | 2 | 6 | TRA26`, so 14 days, 10 staff and 2 tasks match the file name 80_14_10_2, and the best known value is 6 > 0. It is not instance 5 (best known 0), not the 8_7_20_2 example trap, and not a nurse-rostering instance.
2. **"an independent checker written from the published ProblemDefinition.pdf"**: met. I compared code/verify_claim.py with data/ProblemDefinition.txt one constraint at a time:
   - C1, one shift per calendar day, with D = {0..h}: checked.
   - The start-time sets: 00:00, 06:00-10:00, 14:00-18:00, 20:00-23:45. No 00:00 on day 0, and only 00:00 on day h. Checked.
   - Shift length L in {24..40} intervals: checked.
   - C2, the shift ends within h*96: checked, on every day, which is stricter than the PDF.
   - C3, u_ed <= t_e(d+1) - 56: checked.
   - C4, b_e <= minutes <= c_e: checked.
   - C5, at most 5 of any 6 consecutive days, for d in {0..h-5}: checked.
   - C6, the literal pattern with s = 1..3: checked.
   - C7, activities only inside a shift and one activity per interval: holds by construction, because shift length = sum of task lengths and overlaps are flagged.
   - C8, min cover is hard: checked.
   - Objective: sum of max(0, cover - w)^2, which is what minimising y^2 under C8 yields.

   It reproduces the example: `verify_claim.py data/8_7_20_2.txt data/8_7_20_2.Solution.889.xml 890` gives violations 0, penalty 889. The example contains Day 0 and Day 7 entries, which confirms 0-based calendar days in solution files.
3. **"reports all hard constraints satisfied and a total penalty strictly below that instance's Best known value"**: met. `verify_claim.py data/80_14_10_2.txt object/80_14_10_2.Solution.0.xml 6` gives violations 0, penalty 0, PASS. 0 < 6.
4. **"in the site's XML solution format"**: met, with one caveat.
   - object/80_14_10_2.Solution.0.xml has the same element tree as data/8_7_20_2.Solution.889.xml: Solution / ProblemFile, Penalty / Employee[@ID] / Shift / Day, Start(HH:MM:SS) / Task / ID, Length. Day numbering is the same (0-based), and no shift has adjacent tasks with the same ID.
   - It omits the xsi:noNamespaceSchemaLocation attribute, the descriptive metadata (TimeStamp, Author, Reference, Machine, SolveTime) and the `WorkLength` attribute on Task. In the example, WorkLength always equals Length (140/140).
   - I count it as the site's format, because every field that defines the roster is present in the site's structure.
   - Caveat: if the site's Solution.xsd requires WorkLength, a schema-validating official tool could reject the file. The human's optional cross-check would catch this, and the target says a disagreement withdraws the claim. Before any such cross-check, a copy with WorkLength="<Length>" added would avoid this; it does not change the penalty.
5. **"table and changes.html re-fetched live immediately before claiming"**: met so far. Filing must re-fetch again.
   - data/fetched-utc.txt = 2026-11-22T08:03:12Z.
   - I re-fetched both pages live at 2026-11-22T08:08:03Z (HTTP 200 for each). They are byte-identical to data/matsp.html (sha256 f14664f5...) and data/changes.html (sha256 6eb567e7...). Instance 80 is still 6 (TRA26), and the newest Changes entry is 29-Oct-2026 (nurse rostering). No multi-activity update has appeared since 07-Oct-2026.
   - "Immediately before claiming" means the filer must re-fetch both pages again just before filing and withdraw if instance 80's best known value is <= 0 or a newer multi-activity entry changes it. This snapshot is fresh only for filing within minutes.
6. **Closed-source verifier optional, done by the human; nothing submitted by the agent**: met. Nothing in claim/ downloads or runs MATSP_Verifier or RosterViewer, and nothing emails or submits anything. The official cross-check stays a human option.

## Code-independent spot check (my own script, not derived from code/)

Design of the script:
- Cover requirements come from the instance XML data/80_14_10_2.ros, and times use datetime arithmetic rather than interval indices.
- The .ros cover (2688 entries) is identical to the .txt cover.

Rules it checks, some stricter than the PDF:
- Every maximal same-task run within a shift is >= 60 min.
- 14 h rest holds between every pair of consecutive shifts, not only adjacent calendar days.
- At most 5 working days in every 6-day window.
- Every shift lies inside [day0 06:00, day h 06:00].
- Start sets, lengths, and min/max minutes per employee.
- Min cover and the quadratic over-cover penalty.

Results:
- Example: 0 violations, penalty 889.
- Claimed roster: 0 violations, 0 under-minimum intervals, penalty 0.
- Several employees sit exactly at their minimum minutes, all within range: e.g. e1 2160 in [2160, 2400], e8 1440 in [1440, 2400].

## Other points

- **Non-preregistered pilot**: does not matter here. The criterion is a property of one exact object (feasible, with penalty < 6), checked deterministically. No statistic or selection over many tries enters it, so search-side forking cannot inflate it. PREREG.md fixes the object hash (it matches object/ and data/selected_solution.xml) and the checks.
- **Null model**: not applicable to a deterministic feasibility-and-penalty check. The comparison baseline is the published best known value 6.
- **"0 is also optimal"**: trivially true, because the objective is a sum of squares. That is not the optimality-certificate partial win, and it adds no scope.
- **Subsumption**: instance 80 also falls in matsp-small-instance-improve (76-85), but the full criterion is met, so this is a full win, not a subsumed partial one.

confirmed_scope: For instance 80 (80_14_10_2) of the schedulingbenchmarks.org multi-activity set, the roster object/80_14_10_2.Solution.0.xml satisfies every hard constraint of ProblemDefinition.pdf and has total penalty 0 under two independent checkers that reproduce 889 on 8_7_20_2.Solution.889.xml, strictly below the best known value 6 (TRA26) shown on the table and Changes page as fetched 2026-11-22T08:03:12Z and unchanged at 08:08:03Z.

pass: true
