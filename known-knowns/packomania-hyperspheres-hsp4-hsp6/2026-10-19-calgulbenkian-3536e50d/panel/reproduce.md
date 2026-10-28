context: Claude Code subagent, fresh context [claude-sonnet-5-5]

# Reproduce report: hsp4-170

Definition quoted from the target's success criterion: the FEASIBLE radius r* := min( (smallest pairwise distance |c_i - c_j| over all pairs) / 2, 1 - max_i |c_i| (Euclidean norm) ), computed at 50 digits from the submitted coordinates with no tolerance, strictly greater than the live radius table value for that N by at least 1e-10, AND the configuration not isometric to the posted file (sorted pairwise-distance multisets differ by more than 1e-8 somewhere).

Method. Before opening the author's checker I wrote my own checker (standard Python plus mpmath, run with python -I; not shipped in this package). It reads every coordinate as an exact decimal, scales to integers, computes all N(N-1)/2 squared distances exactly in integers, takes the square root of the smallest at 60 digits, computes the wall term exactly (largest norm or largest coordinate, as an integer square root at 60 digits), and prints r*. A second small script of mine (not shipped) reads the saved radius table and prints the row for N and the largest row at any N' >= N. The files were first checked against the contributor's hash list from inside the package folder (all lines OK), then copied to a private location; no network was used.

My command:

    (own checker, run on object/WIN_hsp4_170.txt and the posted N=170 file, which is not shipped)

My real output:

    file WIN_hsp4_170.txt N 170 decimals scale 1e17
    half min dist 0.215645064369925650688523058284
    wall bound    0.215645059468390008128190279493
    r*            0.215645059468390008128190279493
    limited by wall
    pairs within 1e-6 relative of min: 471
    POSTED N 170 r* 0.21558969516778170845
    max abs diff sorted distances 0.009031040430996784

The saved table (the-record-we-beat/radius_rows_N170_to_300.txt) read by my own second script:

    row N 0.215589695168 | rows count 299 | max N 300
    max row over N>=170: 0.215589695168 at N= [170]
    claimed - row(N) = 0.0000553643003900081281903 ; claimed - max row(N>=N) = 0.0000553643003900081281903

Checks:

- 170 points in 4 dimensions (index column dropped, 17 decimals). Exact r* = 0.215645059468390008128190279493, limited by the wall (half minimum distance 0.215645064369925650688523). The claim sentence: 0.2156450594683900081281903, matching.
- The object file header line prints 0.21564505946838996575, which differs from the exact r* in the 17th digit (open question 3). The criterion reads r* from the coordinates, as I did; the header is only a comment.
- Table row for N = 170: 0.215589695168; gain 5.5364e-5 (above 1e-10). N = 170 is the last row at or above itself in the sense of no larger row at N' >= 170 (the table's own rows after 170 are all smaller), so the propagated bar equals the row (output above).
- Posted file parse sanity: the posted N=170 file gives r* = 0.21558969516778 by my checker, equal to the row 0.215589695168 to 12 decimals. Sorted-distance multisets differ by 9.03e-3 at most (claim: 9.0e-3), above 1e-8.
- Open question 1 (manifest copy): the manifest copy (the-record-we-beat/mj_rows_extract.csv) lists 0.2155917530134953 for hsp4 N = 170, below r*; I could not re-fetch the manifest. Open question 2: the saved history excerpt shows no change since 2025; I cannot reproduce a same-day live fetch offline.

Only after that I ran the author's sh verify-it-yourself/run_checks.sh (lines that matter):

    sha256 of object/WIN_hsp4_170.txt matches INDEX.csv (3536e50dd047d04f09605dabb6bf33b5c17a9bfaf502147c2cc43c9da215bb65)
    object_points N=170 dim=4 decimals_scale=17
    r_star=0.215645059468390008128190279493
    gain_over_table=5.536430039000813e-5
    gain_at_least_margin(1e-10)=True
    posted_points N=170 posted_header_radius=0.215589695168 posted_r_star=0.215589695167782
    differs_from_posted_by_more_than_1e-8=True
    RESULT PASS
    == table_compare.py: facts against the saved table records
    table row N=170: 0.21558969516800  r_star minus this = 5.536430e-5
    largest table row at N' >= 170: 0.21558969516800 (at N=170)  r_star minus this = 5.536430e-5
    Moki-Julio manifest N=170: 0.21559175301350  r_star minus this = 5.330645e-5
    largest manifest value at N' >= 170: 0.21559175301350 (at N=170)  r_star minus this = 5.330645e-5
    Cohn table converted, N=170: 0.20853075981595  r_star minus this = 7.114300e-3
    largest converted Cohn value at N' >= 170: 0.20853075981595 (at N=170)  r_star minus this = 7.114300e-3
    RESULT facts printed
    == negative control: the first point is moved onto the second; the check must FAIL
    negative control rejected as expected (r_star=0.000000000000000000000000000000)
    ALL CHECKS PASS
    exit 0

The author's checker and mine agree on r* to every printed digit. No mismatch, no missing object, no non-determinism (the computation is exact integer arithmetic).

Verdict: r* = 0.2156450594683900081281903 (wall-limited) confirmed exactly from the printed coordinates; gain over the saved row 5.5364e-5; non-isometry to the posted file confirmed (9.03e-3 > 1e-8). Live table, queue and manifest not reproducible offline.

pass: true
