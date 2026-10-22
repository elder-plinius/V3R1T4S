# reproduce report: sc-30-62
context: Claude Code subagent, fresh context [Sonnet 5.5]

Hash check: shasum -a 256 -c on the contributor's hash list run inside the package folder printed no failure (all listed files OK). The package folder was copied to a private workspace; all work done there. No network used.

Definition (quoted from the target's success criterion): "after normalizing each vector to unit length in mpmath at 50 digits the maximum pairwise inner product c* (cosine of the minimal angle) is STRICTLY LOWER (direction: min) than the table's 12-decimal cosine for (d, N) ... by at least 1e-10, AND ... the (d, N) row has NO '&ast;' (proven optimal) mark AND does NOT contain the text 'needs more optimization'".

My checker (written before opening verify-it-yourself/): my own script, not shipped in this package, kept outside the package copy; its output is shown below. It checks per object file: line count equals N; every line has exactly d comma-separated coordinates; coordinates have at least 20 significant digits; each vector normalised with mpmath at dps=50; ALL N(N-1)/2 pairwise inner products computed in mpmath (no sampling), c* = max; gain = (12-decimal /plain cosine) minus c* >= 1e-10; the plain_rows.csv cosine, the index_rows.html cosine and the cosine in README.md agree as strings; the index row has no &ast; star; the row does not contain "needs more optimization"; the kissing-number exclusion (9<=d<=23 and c*<=0.5) does not apply.

Command: (own checker, run on the private copy of the package; interpreter: the V3R1T4S venv python). Real output (shown below):
```
(d=30,N=62) lines=62 dim_ok=True min_sigdigits~27 c*=0.0312731833638132426153248 angle_deg=88.2078863822239 table=0.031273236170 gain=5.2806187e-8 gain>=1e-10:True ast=False needs_opt=False cos_consistent=True ref='Ilmari Vahteristo, New spherical codes by tuning an annealing solver, preprint, 2026, arXiv:2610.19988.' kissing_excl=n/a ROW_OK
rows_ok 1 of 1
```

Then the author's checker: PYTHON=venv-python sh verify-it-yourself/run_checks.sh (run in the private copy). Last line: ALL CHECKS PASS. Its sha256 lines: 1 ok, 0 mismatch. Its c* values agree with mine to 20 digits for 1 of 1 rows; mismatches: none.

Not judged here: whether the table value is current, and novelty (other skeptics).
Mismatches: none

pass: true
