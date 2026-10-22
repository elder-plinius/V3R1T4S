context: Claude Code subagent, fresh context [claude-sonnet-5-5]

# Reproduce report: scu-733

Definition quoted from the target's success criterion: the FEASIBLE radius r* := min( (smallest pairwise distance |c_i - c_j| over all pairs) / 2, 1/2 - max_i max(|x_i|,|y_i|,|z_i|) ), computed at 50 digits from the submitted coordinates with no tolerance, strictly greater than the live radius table value for that N by at least 1e-11, AND the configuration not isometric to the posted file (sorted pairwise-distance multisets differ (sorted distance multisets differ)).

Method. Before opening the author's checker I wrote my own checker (standard Python plus mpmath, run with python -I; not shipped in this package). It reads every coordinate as an exact decimal, scales to integers, computes all N(N-1)/2 squared distances exactly in integers, takes the square root of the smallest at 60 digits, computes the wall term exactly (largest norm or largest coordinate, as an integer square root at 60 digits), and prints r*. A second small script of mine (not shipped) reads the saved radius table and prints the row for N and the largest row at any N' >= N. The files were first checked against the contributor's hash list from inside the package folder (all lines OK), then copied to a private location; no network was used.

My command:

    (own checker, run on object/WIN_scu_733.txt and the posted N=733 file, which is not shipped)

My real output:

    file WIN_scu_733.txt N 733 decimals scale 1e20
    half min dist 0.0589437529548279448024778016876
    wall bound    0.05894375295482795485
    r*            0.0589437529548279448024778016876
    limited by pair
    pairs within 1e-6 relative of min: 1550
    POSTED N 733 r* 0.058531064606277395414
    max abs diff sorted distances 0.07747458301500298

The saved table (the-record-we-beat/radius_rows_N733_to_1000.txt) read by my own second script:

    row N 0.058531064607 | rows count 1134 | max N 1024192
    max row over N>=733: 0.058943675866 at N= [734]
    claimed - row(N) = 0.0004126883478279448024778 ; claimed - max row(N>=N) = 7.70888279448024778E-8

Checks against the clauses I can test from the saved files:

- 733 points, 3 coordinates each, 20 decimals; exact r* = 0.0589437529548279448024778016876 (pair-limited; the wall term is 0.05894375295482795485, larger). The claim sentence gives 0.0589437529548279448024778, matching to every digit given.
- Table row for N = 733 in the saved radius table: 0.058531064607; gain 4.1269e-4, far above 1e-11 (my output above).
- Posted file parse sanity: the saved posted N=733 file (index, x, y, z, radius columns) gives r* = 0.0585310646062774 by my checker, matching the table row 0.058531064607 to its 12 decimals. The sorted-distance multisets of the object and the posted file differ, largest difference 0.0775 (claim says 7.7e-2), far above 1e-8.
- Neighbour rows (from the same saved file): the row for N = 734 is 0.058943675866, the largest row at any N' >= 733; the object exceeds it by 7.7089e-8 (exactly 0.0589437529548279448 - 0.058943675866). So the object also beats the propagated bar of the N = 734 row (open question 1: the numbers are as stated; whether a packing derived by deleting one sphere from the posted 734 packing is a separate record is a judgement for the criterion and novelty skeptics, not something the files can decide).

Answers to open questions that concern reproduction:

- Open question 5 (20 decimals, exact evaluation): I evaluated the printed decimals exactly (integers), so r* is the exact radius of the printed configuration; the 50-digit mpmath reading and the exact reading give the same number to the 50 digits requested, because only the last digit of rounding at 1e-20 could differ.
- Open question 2 (relation to the posted 734 packing): I did not have the posted 734 file (it is not saved in the folder), so I cannot confirm the statement that the object is the 734 packing with one sphere removed. What I can confirm is the non-isometry to the posted 733 file.
- Open questions 3 and 4 (manifest copy faithful; table mid-revision): the manifest copy is only in the-record-we-beat/mj_rows_extract.csv (value 0.0588218693815 for N = 733, below r*); I had no network and could not re-fetch it. Not reproducible from the folder.

Only after that I ran the author's sh verify-it-yourself/run_checks.sh (lines that matter):

    sha256 of object/WIN_scu_733.txt matches INDEX.csv (14cbb77e014f41d2dd0cb795eed3095d31591a76985ab0a9b57e04db7e63082d)
    object_points N=733 dim=3 decimals_scale=20
    r_star=0.058943752954827944802477801688
    gain_over_table=4.126883478279448e-4
    gain_at_least_margin(1e-11)=True
    posted_points N=733 posted_header_radius=0.058531064607 posted_r_star=0.058531064606277
    differs_from_posted_by_more_than_1e-8=True
    RESULT PASS
    == table_compare.py: facts against the saved table records
    table row N=733: 0.05853106460700  r_star minus this = 4.126883e-4
    largest table row at N' >= 733: 0.05894367586600 (at N=734)  r_star minus this = 7.708883e-8
    Moki-Julio manifest N=733: 0.05882186938148  r_star minus this = 1.218836e-4
    largest manifest value at N' >= 733: 0.05882186938148 (at N=733)  r_star minus this = 1.218836e-4
    RESULT facts printed
    == negative control: the first point is moved onto the second; the check must FAIL
    negative control rejected as expected (r_star=0.000000000000000000000000000000)
    ALL CHECKS PASS
    exit 0

The author's checker and mine agree on r* to every printed digit. No mismatch, no missing object, no non-determinism (the computation is exact integer arithmetic).

Verdict: r* = 0.0589437529548279448024778 confirmed exactly; it exceeds the saved row for N = 733 by 4.1269e-4 and the largest saved row at N' >= 733 (N = 734) by 7.7089e-8; non-isometry to the posted 733 file confirmed (largest sorted-distance difference 0.0775). Not reproducible from the files: the current live table, the queue rule, and the Moki and Julio manifest (no network).

pass: true
