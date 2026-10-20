# Honesty gate - degree-diameter-table, cell (13,4)

status: CONFIRMED_SOLUTION
confirmed_scope: The submitted 6 631-vertex edge list is a simple, connected undirected graph with maximum degree 13 and diameter exactly 4, strictly larger than the live Comellas (13,4) cell of 6 615 (re-fetched 2026-10-20) and than the repo's 6 630-vertex trophy, and below the Moore bound of 24 506.
gate_utc: 2026-10-20T19:12Z
gate_by: the run's main session, reading all three panel files and re-running the checkers; not one of the skeptics

## Gate notes

- Panel: three fresh subagent contexts, each given only `claim/`; reproduce (pass), novelty
  (pass), criterion (pass), each file carries `context: subagent` and ends `pass: true`.
- Table: the status source was fetched twice today with one honest GET each: 18:21Z
  (sha256 8610e580..., cell 6 615) and 19:06:44Z (sha256 69486132..., cell still 6 615,
  not boldface). The novelty skeptic's own fetch at 19:07:30Z returned the same page hash.
  The panel's fetch is under 6 hours old, so no further re-fetch is required at the gate.
- My own check before the gate: `ddlib.bad_pairs` (bit-parallel all-pairs, a different algorithm
  from the stdlib BFS) reports cost 0, and scipy shortest_path reports diameter 4, max degree 13,
  connected. The object sha256 is 391f09bb6f72f16ca5b867694b96d1d1ca31569c8974ba0f0ef00099c6cd5cbe.
- The object is the cost-0 artifact of the run's own SA chain: initial cover-subdivision cost 333,
  pivoted to 268, annealed 268 -> 190 -> 162 -> 95 -> 57 -> 33 -> 9 -> 0
  (attempts/constructor/output/sa57.log, seed 43). Every earlier state is invalid and none is
  shipped.
- Non-disqualifying: the margin over the workspace trophy is +1 vertex. The criterion is a
  strict inequality with no minimum margin, and the edge set is not the trophy plus a pendant
  (the criterion skeptic verified the induced edge set differs in 594 positions).
- Checker caveat raised by the criterion skeptic: `claim/checkers/verify_scipy.py` prints but
  does not assert the diameter, and needs scipy. That is a packaging defect, not a criterion
  failure: criterion (3) is met by the stdlib all-pairs BFS and by two independently written
  bitset BFS implementations in the panel. The package ships its own stdlib checker with an
  explicit diameter assertion (`verify-it-yourself/check_graph.py`), and the panel files are
  copied unedited.
- Status vocabulary: all five numbered clauses hold, so CONFIRMED_SOLUTION, not a partial win.

## Post-gate packaging edits (path redaction only)

Two files had absolute temporary-folder paths removed so the package passes the leak scan:
`panel/reproduce.md` (the phrase "(a shuffled copy of the edge list)" replaces a temp-file path
in the determinism bullet) and `HOW_WE_FOUND_IT.md` (the example commands use a relative
`state/` folder). No verdict, number, hash or scope sentence was changed.
