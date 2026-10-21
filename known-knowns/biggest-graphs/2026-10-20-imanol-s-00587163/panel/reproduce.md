# Independent reproduction verdict

Context: fresh headless opencode run --standalone (role reproduce). Independent checker written from the definition before reading any author's code; no author's checker or construction code was used. Only supplied claim data and this role's own artifacts were read. No submissions, messages, pushes, or other outward actions were performed; public HTTP requests were read-only.

Definition quoted from `claim/CLAIM.md`: “The input is a two-column undirected edge list, an explicit adjacency encoding. Lines beginning with # or % are comments. Labels must be all integers 0 through 6636. Reject loops or repeated undirected edges.” The graph claim is “6637 vertices, maximum degree at most 13, and diameter at most 4”. The binding criterion additionally requires connectedness, all-pairs BFS, the Moore bound, and strict improvement over the live general-graph table.

## Object and deterministic check

Object: `claim/object/G_13_4_n6637.edges`.

Exact SHA-256: `00587163283c37fbb2d5d83ebd2c533e010af603f5e27d59a01c55a527185059`, independently computed from the saved bytes and equal to the frozen claim.

`checker.cpp` independently parses exact integer tokens, rejects extra columns, out-of-range or missing labels, loops, duplicate undirected edges, and degree overflow. It constructs symmetric adjacency directly from undirected edges. It runs a complete BFS from every vertex, rejecting disconnectedness and diameter overflow. No sampling, quotient, or transitivity assumption is used.

Actual candidate output:

```text
PASS N=6637 edges=43140 min_degree=12 max_degree=13 diameter=4 BFS_roots=6637 Moore_bound=24506
```

The exact Moore bound is `1 + 13(1 + 12 + 12² + 12³) = 24506`; `6637 <= 24506`. All 6,637 BFS roots completed; the graph is connected and its exact diameter is 4.

Actual commands were `python3 run.py`, which compiled with `clang++ -O3 -std=c++17 checker.cpp -o checker`, then ran `./checker claim/object/G_13_4_n6637.edges 6637 13 4`, and `python3 comparison.py`. Both Python orchestration commands ran with shell `background:true`. Full commands, UTC readings, exit statuses, outputs, and elapsed timings are preserved in `receipt.txt` and `comparison_receipt.txt`.

The first run started at 2026-10-20T21:28:03.326958+00:00 and ended at 2026-10-20T21:28:08.455703+00:00, elapsed 5.128820 seconds. Compilation took 1.333563 seconds; the candidate's all-pairs verification took 0.612643 seconds.

The valid triangle control passed with diameter 1 and Moore bound 3. Deliberately invalid saved controls rejected duplicates, loops, missing labels, malformed integers, degree overflow, disconnectedness, and invalid labels. The initial path/diameter control hit the Moore-bound guard first; a separate path control with degree allowance 3 was run to exercise the diameter-overflow branch specifically. Control commands and actual diagnostics are in the receipts, with inputs in `tiny.edges` and `invalid_*.edges`.

## Live comparison

The live general-graph table was fetched read-only at 2026-10-20T21:28:05.611915+00:00, HTTP 200, saved as `live_table.txt`, SHA-256 `e155b7ea159c5dd6f43808767b3e31ed386dfaf7c4969bec4e7d07d50c1c17ab`. Its degree-13, diameter-4 cell links to `desc_g/desc_g4.html#134` and reads `6 615`, not boldface. Thus the verified object improves the live entry by 22 vertices. This is a full-criterion comparison, not a partial-win snapshot claim.

The live GitHub API independently confirmed that PR #598 is open and claims 6,631 vertices for (13,4), so this verified object exceeds that prior submission by 6 vertices rather than resubmitting its result. The supplied trophy case lists 6,630. All 284 currently open PR descriptions were fetched across three pages (`open_prs.txt`, `open_prs_page2.txt`, `open_prs_page3.txt`); the saved matching descriptions disclose no competing 6,637-vertex claim for this cell. This is a bounded repository check, not an exhaustive literature novelty proof; the binding target defines success against the live Comellas entry.

`comparison_receipt.txt` confirms the additional control actually returned `FAIL diameter overflow`, parsed the live cell as 6615, and completed at 2026-10-20T21:28:36.695793+00:00 after 1.881262 seconds. Both execution phases finished before the stated search deadline and within the panel allowance. No blocked sources or retries occurred.

All five binding success conditions are established for the saved object at this verification time: explicit simple undirected graph; maximum degree 13; connected with diameter 4 by every-source BFS; 6,637 strictly greater than the immediately fetched live value 6,615; and order below the exact Moore bound with no proven-optimal cell being beaten. No optimality claim is inferred.

pass: true
