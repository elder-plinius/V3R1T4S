context: Claude Code subagent, fresh context [claude-sonnet-5-5]

# Reproduce report: scu-739

Definition quoted from the target's success criterion: the FEASIBLE radius r* := min( (smallest pairwise distance |c_i - c_j| over all pairs) / 2, 1/2 - max_i max(|x_i|,|y_i|,|z_i|) ), computed at 50 digits from the submitted coordinates with no tolerance, strictly greater than the live radius table value for that N by at least 1e-11, AND the configuration not isometric to the posted file (sorted pairwise-distance multisets differ (sorted distance multisets differ)).

Method. Before opening the author's checker I wrote my own checker (standard Python plus mpmath, run with python -I; not shipped in this package). It reads every coordinate as an exact decimal, scales to integers, computes all N(N-1)/2 squared distances exactly in integers, takes the square root of the smallest at 60 digits, computes the wall term exactly (largest norm or largest coordinate, as an integer square root at 60 digits), and prints r*. A second small script of mine (not shipped) reads the saved radius table and prints the row for N and the largest row at any N' >= N. The files were first checked against the contributor's hash list from inside the package folder (all lines OK), then copied to a private location; no network was used.

My command:

    (own checker, run on object/WIN_scu_739.txt and the posted N=739 file, which is not shipped)

My real output:

    file WIN_scu_739.txt N 739 decimals scale 1e20
    half min dist 0.0586275441666459796140566738887
    wall bound    0.05862754416664600621
    r*            0.0586275441666459796140566738887
    limited by pair
    pairs within 1e-6 relative of min: 1684
    POSTED N 739 r* 0.058531064606
    max abs diff sorted distances 0.07616533888009602

The saved table (the-record-we-beat/radius_rows_N739_to_1000.txt) read by my own second script:

    row N 0.058531064606 | rows count 1134 | max N 1024192
    max row over N>=739: 0.058627036756 at N= [740, 741]
    claimed - row(N) = 0.0000964795606459796140567 ; claimed - max row(N>=N) = 5.074106459796140567E-7

Checks against the clauses I can test from the saved files:

- 739 points, 3 coordinates, 20 decimals; exact r* = 0.0586275441666459796140566738887 (pair-limited; wall term 0.05862754416664600621). The claim sentence gives 0.0586275441666459796140567, matching.
- Table row for N = 739: 0.058531064606; gain 9.6480e-5 (above 1e-11). The largest row at any N' >= 739 is 0.058627036756 (N = 740 and 741); the object exceeds it by 5.0741e-7.
- Posted file parse sanity: the saved posted N=739 file gives r* = 0.058531064606 (the table row) by my checker. Sorted-distance multisets differ; largest difference 0.0762 (claim: 7.6e-2).
- Open questions 1, 2, 3, 4: the files confirm the numbers; the 741 file from which the object is said to derive is not in the folder (cannot confirm the derivation); the manifest value 0.0586073866758 for N = 739 sits only in the-record-we-beat/mj_rows_extract.csv and I could not re-fetch it; live-table revision state is not reproducible offline. Open question 5: exact evaluation of the printed decimals, as above.

Only after that I ran the author's sh verify-it-yourself/run_checks.sh (lines that matter):

    sha256 of object/WIN_scu_739.txt matches INDEX.csv (a7296ee4e9a17d4490e65a696af8c4d64266a39af7cd383cfdd0e54d641baf76)
    object_points N=739 dim=3 decimals_scale=20
    r_star=0.058627544166645979614056673889
    gain_over_table=9.647956064597961e-5
    gain_at_least_margin(1e-11)=True
    posted_points N=739 posted_header_radius=0.058531064606 posted_r_star=0.058531064606000
    differs_from_posted_by_more_than_1e-8=True
    RESULT PASS
    == table_compare.py: facts against the saved table records
    table row N=739: 0.05853106460600  r_star minus this = 9.647956e-5
    largest table row at N' >= 739: 0.05862703675600 (at N=740)  r_star minus this = 5.074106e-7
    Moki-Julio manifest N=739: 0.05860738667577  r_star minus this = 2.015749e-5
    largest manifest value at N' >= 739: 0.05860738667577 (at N=739)  r_star minus this = 2.015749e-5
    RESULT facts printed
    == negative control: the first point is moved onto the second; the check must FAIL
    negative control rejected as expected (r_star=0.000000000000000000000000000000)
    ALL CHECKS PASS
    exit 0

The author's checker and mine agree on r* to every printed digit. No mismatch, no missing object, no non-determinism (the computation is exact integer arithmetic).

Verdict: r* = 0.0586275441666459796140567 confirmed exactly; it exceeds the saved row for N = 739 by 9.648e-5 and the largest saved row at N' >= 739 (N = 740, 741) by 5.074e-7; non-isometry to the posted 739 file confirmed (largest sorted-distance difference 0.0762). Live table, queue and manifest not reproducible offline.

pass: true
