# Criterion verdict
context: fresh subagent started for this claim only

Claim: runs/2026-11-27-1642-itc2021-ub6/claim (six ITC2021 timetables below their Best UB). Skeptic role: CRITERION.
Everything below was produced in panel/work-criterion/ (nothing written in claim/). Python was run as `python3 -I`, standard library only, with no imports from claim/.

## Method

1. `sha256sum -c claim/SHA256SUMS`: every line OK; `PREREG.md` hash equals `PREREG.sha256`.
2. Fetched the live bank entry and the board once each, then the six history pages once each, with curl and User-Agent `V3R1T4S-criterion-skeptic/1.0`. Times come from `date -u`. Log: work-criterion/fetch_log.txt.
3. Parsed the board myself (work-criterion/scripts/parse_board.py, output board_parsed.tsv, board_all.txt) and read each history page's solution and bound lists.
4. Ran the source-built RobinX (scans/2026-11-26-robinx-build/src/RobinX, sha256 080fcf6b...f1142, which matches that scan's SHA256SUMS; its README.md is in the scan's top folder, not in src/) on each object and each posted record in claim/data/records, using the claim's original instance files. Outputs: work-criterion/robinx_out/.
5. Wrote my own structure-and-penalty checker from the ITC2021 rule definitions without reading claim/code first (work-criterion/scripts/mycheck.py, sha256 9dd6487e...a9015). It covers the compact 2RR structure, phase (gameMode P), and CA1-CA4, GA1, BR1, BR2, FA2 and SE1. I ran it on all six objects and all six records, not only the two the brief requires. Three mutations of the Late 11 timetable (venue flip, moved game, deleted game) were all rejected by my checker, verify.py and RobinX (RobinX infeasibility 3, 4 and 3).
6. Copied claim/code/verify.py to work-criterion/verify_copy.py (sha256 12eb7674...74c1, the same as in SHA256SUMS) and ran it on all six rows with the board's Best UB. As a control I gave it the Middle 5 record at its own UB 279: it printed FAIL, as it should, because 279 is not strictly below 279.

## Verbatim criterion (live bank entry, fetched 2026-11-27T14:47:52Z, HTTP 200, sha256 be207de1dfbf1aded338e89902eaaa0b017b31b7d062d4b0a201f295dc2e54a2)

> A solution XML for an ITC2021 instance listed on https://robinxval.ugent.be/ITC2021/instances.php that the open-source RobinX/ITC2021 validator (github.com/Robin-X/RobinX) evaluates to infeasibility 0 and a penalty strictly below that instance's 'Best UB' value, also reproduced by a second, independently written evaluator, with the table and the instance's history page re-fetched live immediately before claiming.

Partial wins (verbatim):

> - **itc2021-middle-late-improve:** Strict improvement on any Middle or Late instance whose UB is more than 500 above its LB (e.g. Middle_1/2/3, Late_2, Late_12), validated by the RobinX validator.
> - **itc2021-lower-bound-certificate:** A strictly higher lower bound for any open instance, given as a saved MIP/CP model file plus solver log and seed whose dual bound a skeptic re-runs to the same value (or better) in a fresh session; or, more strongly, a feasible timetable whose penalty equals the listed Best LB, which closes the instance and is checked by the validator alone.
> - **itc2021-reproduce-validator:** Build the RobinX validator and reproduce the listed penalty of every posted best solution (45 files) exactly; a prerequisite that also catches stale table entries.

The live entry's sha256 equals claim/data/target_live.md (be207de1...). claim/target.md differs from it only by a leading `id: itc2021-sports-timetabling-ub` line and a blank line; the rest is byte-identical (diff). The criterion text in claim/target.md is therefore the live one.

## Re-fetch (all HTTP 200; all byte-identical to the claim's copies)

| page | UTC | HTTP | sha256 | equals claim/data |
|---|---|---|---|---|
| bank entry (raw.githubusercontent) | 2026-11-27T14:47:52Z | 200 | be207de1...54a2 | target_live.md: yes |
| instances.php (board) | 2026-11-27T14:47:52Z | 200 | e008069e...40832f75 | board.html: yes |
| history Early_9 | 2026-11-27T14:48:33Z | 200 | 0be1eb4b...61f6 | yes |
| history Early_12 | 2026-11-27T14:48:33Z | 200 | 05615570...cc76 | yes |
| history Middle_5 | 2026-11-27T14:48:33Z | 200 | 2baa0e25...1216 | yes |
| history Middle_12 | 2026-11-27T14:48:33Z | 200 | 0cecebad...43db | yes |
| history Middle_15 | 2026-11-27T14:48:33Z | 200 | bbac4dfe...7e11 | yes |
| history Late_11 | 2026-11-27T14:48:34Z | 200 | e618938b...0517 | yes |

Full hashes are in work-criterion/fetch_log.txt. I did not fetch the instance XMLs or the posted solution files, because the brief allows only the board and the six history pages. Their identity with the board links therefore rests on claim/data/fetch.json (status 200 and sha256, no URLs) plus indirect evidence: RobinX scores each claim/data/records file at exactly the board's Best UB on these instance files.

## Per-row results

Board values are from my own parse. "Hist min" is the lowest solution on the history page. RobinX prints `Objective: infeasibility penalty`.

| instance | board LB | board UB | hist min | RobinX on record | RobinX on ours | my checker on ours (struct errs / hard / pen) | verify.py | ours < UB | criterion |
|---|---|---|---|---|---|---|---|---|---|
| Early 9 | (0, 0) | (0, 56) | 56 | 0 56 | **0 51** | 0 / 0 / 51 | PASS 51 | yes, by 5 | met |
| Early 12 | (0, 0) | (0, 315) | 315 | 0 315 | **0 300** | 0 / 0 / 300 | PASS 300 | yes, by 15 | met |
| Middle 5 | (0, 47) | (0, 279) | 279 | 0 279 | **0 278** | 0 / 0 / 278 | PASS 278 | yes, by 1 | met |
| Middle 12 | (0, 1) | (0, 358) | 358 | 0 358 | **0 338** | 0 / 0 / 338 | PASS 338 | yes, by 20 | met |
| Middle 15 | (0, 1) | (0, 462) | 462 | 0 462 | **0 459** | 0 / 0 / 459 | PASS 459 | yes, by 3 | met |
| Late 11 | (0, 0) | (0, 196) | 196 | 0 196 | **0 191** | 0 / 0 / 191 | PASS 191 | yes, by 5 | met |

- The three evaluators agree exactly on all 12 files (6 objects and 6 records), including the per-rule breakdown. For example, Late 11 ours is CA2 150 + CA3 40 + GA1 1 in both my checker and verify.py.
- No history page lists a solution at or below ours. Every history minimum equals the board's Best UB.
- My checker confirms each object is a compact double round robin. For the four phased instances (Early 12, Middle 5, Middle 12, Late 11) it also confirms that every pair meets once in each half.
- **"Reproduced by a second, independently written evaluator":** met. verify.py is a separate code base from RobinX: 96 lines of Python, its docstring says it was written from the ITC2021 definitions without RobinX's code, and it does not call RobinX. Its author is the claim's own team (PREREG: "split.py plus a round-robin structure check"), so it is independent of RobinX but not of the search. My own checker, written in this fresh context, is a third evaluator and agrees exactly, which removes the shared-bug risk between search and verifier for these six files.
- The RobinX build is from source at commit 878bf2db... (scan README). The bank's "first confirm it reproduces the posted best solution's penalty" step holds for all six records.

## Partial wins

itc2021-middle-late-improve needs a Middle or Late instance with UB - LB > 500. Gaps from my parse: Middle 5 279-47 = 232, Middle 12 358-1 = 357, Middle 15 462-1 = 461, Late 11 196-0 = 196. Early 9 and Early 12 are not Middle or Late. **No row qualifies.** The claim says so correctly, and it does not claim the partial win. The other two partial wins are not claimed, and nothing here bears on them.

## Overstatement and consistency findings

The result itself is not overstated. CLAIM.md's one-sentence scope matches what I measured. The numbers in CLAIM.md, rows.csv and my runs agree:

- Best UB, ours and the margin match on every row. The total margin is 5+15+1+20+3+5 = 49, as stated.
- The rows.csv venue/opponent split agrees with verify.py's output.
- The record holders agree with the board. "Clemence" is an ASCII spelling of the board's "Clémence". "Saturn (board entry)" reflects the board's holder text, "Andreas Krystallidis, Nysret Musliu, Saturn".
- The label NUMERICAL fits, the not-claimed list is accurate, and the text makes no "solved", "optimal" or "record" wording beyond "below Best UB".

Minor documentary defects (none changes a number or the verdict):

1. CLAIM.md says data/fetch.json holds "URLs, HTTP status, sha256, time". It has no URLs and one global time (2026-11-27T14:42:43Z) for all 14 fetches.
2. PREREG.md fixes the objects through `data/object_list.csv (sha256 6fe37290...)`, but that file is not in claim/, so a reader of the frozen claim cannot check the binding. The objects are instead bound by claim/SHA256SUMS and the rows.csv object_sha256 column.
3. verify.py's docstring says it "reproduces the posted Best UB of all 42 open ITC2021 records exactly". Only 6 records are in the package, so that sentence cannot be checked from claim/. It is a code comment, not part of the claim.
4. provenance/README.md calls the five fixed-pattern rows an "exact CP-SAT opponent re-solve". rows.csv says OPTIMAL only for Early 9; the other four are 180 s "fixed-pattern sweep" runs. The word "exact" is loose, but it is provenance, not evidence.
5. The object for Early 9 has `<InstanceName>ITC2021 Early 9</InstanceName>` while the instance says "Early 9". RobinX ignores this, and the posted records vary in the same way ("Middle12", "\"Late 11\"").

## Points for the gate

- **RULES.md rule 4, "One object or table cell per claim":** this claim is a batch of six cells in one package. Each row is its own table cell with its own object, and the claim says each row meets the criterion separately. The counting rule (PREREG) drops rows one at a time. Read literally, rule 4 asks for one cell per claim, which this batch does not satisfy. Whether six separable rows in one package are acceptable is for the gate to decide and disclose. If any row is later withdrawn, the others stand on their own evidence.
- **"Re-fetched live immediately before claiming":** the claim fetched the board, the history pages and the instances at 2026-11-27T14:42:43Z and froze PREREG at 14:45:58Z. My re-fetch at 14:47:52-14:48:34Z is byte-identical for the board, all six history pages and the bank entry. The criterion's "immediately before claiming" refers to the public claim, so a re-fetch at filing time is still needed. PREREG commits to that and to withdrawing any row whose Best UB has dropped to or below ours. This verdict covers the table only as of 14:48:34Z.
- Five of the six timetables (all except Late 11) keep the posted record's home/away pattern exactly (0 venue cells differ) and change the slots of 35-244 of 306-380 games. Late 11 differs from its record in 6 venue cells and 15 games. This does not affect the criterion; it is for the NOVELTY skeptic and the gate to weigh. The bank's own ideas list suggests starting from the posted best solutions.
- The fetches I made were not repeated, and none was blocked.

pass: true
