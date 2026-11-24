# Multi-activity shift scheduling: 123 rosters below their best known penalty

## What

For each of the 123 listed instances of the Curtois-Qu multi-activity shift scheduling benchmark (40 of 7 days, 41 of 14, 42 of 28), the roster in object/ satisfies every hard constraint of ProblemDefinition.pdf under an independently written checker that reproduces the site's example penalty 889, with a total penalty strictly below the instance's TRA26 best known value on the table fetched 2026-11-24 (sha256 f14664f5...e984, unchanged at 14:12:51Z), 26,224 below in total, so each meets the full criterion separately and rows 6, 7, 81, 82, 156 and 157 also meet matsp-small-instance-improve; nothing is confirmed about optimality or about acceptance by the site's closed-source verifier.

## Check it yourself

Run `sh verify-it-yourself/run_checks.sh` from this folder (POSIX shell, curl, sha256sum, Python 3 standard library; a few minutes, mostly the 21 MB download and the large rosters). It checks the hashes, downloads the instance archive and the site's example solution and checks their sha256, confirms the evaluator reproduces the example's posted penalty 889, then evaluates every claimed roster against every hard constraint of ProblemDefinition.pdf and requires its penalty strictly below the best known value. Expected last line: PASS.

## Compared to

Table https://www.schedulingbenchmarks.org/matsp/ fetched 2026-11-24T13:34:54Z (the-record-we-beat/); every best known value credits TRA26. 123 instances (40 of 7 days, 41 of 14 days, 42 of 28 days), 26224 below the best known values in total; the 6 rows with at most 20 staff also meet partial win matsp-small-instance-improve.

| # | instance | best known (TRA26) | ours | below by |
|---:|---|---:|---:|---:|
| 6 | 6_7_20_1 | 751 | **743** | 8 |
| 7 | 7_7_20_1 | 727 | **715** | 12 |
| 11 | 11_7_30_1 | 726 | **710** | 16 |
| 12 | 12_7_30_2 | 1375 | **1339** | 36 |
| 13 | 13_7_30_2 | 1283 | **1253** | 30 |
| 16 | 16_7_40_2 | 1486 | **1450** | 36 |
| 17 | 17_7_40_2 | 1563 | **1507** | 56 |
| 21 | 21_7_50_2 | 1461 | **1421** | 40 |
| 22 | 22_7_50_3 | 2424 | **2360** | 64 |
| 23 | 23_7_50_4 | 1927 | **1905** | 22 |
| 26 | 26_7_60_2 | 1490 | **1442** | 48 |
| 27 | 27_7_60_3 | 2402 | **2324** | 78 |
| 28 | 28_7_60_4 | 2582 | **2482** | 100 |
| 31 | 31_7_70_3 | 2324 | **2250** | 74 |
| 32 | 32_7_70_4 | 3022 | **2942** | 80 |
| 33 | 33_7_70_5 | 2709 | **2693** | 16 |
| 36 | 36_7_80_3 | 2300 | **2254** | 46 |
| 37 | 37_7_80_4 | 3132 | **2978** | 154 |
| 38 | 38_7_80_6 | 3272 | **3270** | 2 |
| 41 | 41_7_90_3 | 2341 | **2311** | 30 |
| 42 | 42_7_90_5 | 4014 | **3902** | 112 |
| 43 | 43_7_90_6 | 4119 | **3981** | 138 |
| 46 | 46_7_100_4 | 3249 | **3093** | 156 |
| 47 | 47_7_100_5 | 4060 | **3920** | 140 |
| 48 | 48_7_100_7 | 3893 | **3871** | 22 |
| 51 | 51_7_110_4 | 3111 | **2993** | 118 |
| 52 | 52_7_110_6 | 4942 | **4676** | 266 |
| 53 | 53_7_110_8 | 4448 | **4410** | 38 |
| 56 | 56_7_120_4 | 3036 | **2958** | 78 |
| 57 | 57_7_120_6 | 4743 | **4595** | 148 |
| 58 | 58_7_120_8 | 5293 | **5113** | 180 |
| 61 | 61_7_130_5 | 3941 | **3783** | 158 |
| 62 | 62_7_130_7 | 5642 | **5368** | 274 |
| 63 | 63_7_130_9 | 5605 | **5491** | 114 |
| 66 | 66_7_140_5 | 3988 | **3770** | 218 |
| 67 | 67_7_140_7 | 5610 | **5352** | 258 |
| 68 | 68_7_140_10 | 5997 | **5931** | 66 |
| 71 | 71_7_150_5 | 3829 | **3721** | 108 |
| 72 | 72_7_150_8 | 6481 | **6305** | 176 |
| 73 | 73_7_150_10 | 6482 | **6376** | 106 |
| 81 | 81_14_20_1 | 1510 | **1506** | 4 |
| 82 | 82_14_20_1 | 1493 | **1484** | 9 |
| 86 | 86_14_30_1 | 1585 | **1539** | 46 |
| 87 | 87_14_30_2 | 2397 | **2329** | 68 |
| 88 | 88_14_30_2 | 2337 | **2301** | 36 |
| 91 | 91_14_40_2 | 3080 | **2988** | 92 |
| 92 | 92_14_40_2 | 3342 | **3264** | 78 |
| 93 | 93_14_40_3 | 2988 | **2986** | 2 |
| 96 | 96_14_50_2 | 3184 | **3122** | 62 |
| 97 | 97_14_50_3 | 4066 | **3982** | 84 |
| 98 | 98_14_50_4 | 3867 | **3855** | 12 |
| 101 | 101_14_60_2 | 3125 | **3093** | 32 |
| 102 | 102_14_60_3 | 4807 | **4673** | 134 |
| 103 | 103_14_60_4 | 5412 | **5288** | 124 |
| 106 | 106_14_70_3 | 4770 | **4642** | 128 |
| 107 | 107_14_70_4 | 6156 | **5910** | 246 |
| 108 | 108_14_70_5 | 5103 | **4975** | 128 |
| 111 | 111_14_80_3 | 4662 | **4576** | 86 |
| 112 | 112_14_80_4 | 6373 | **6181** | 192 |
| 113 | 113_14_80_6 | 6356 | **6102** | 254 |
| 116 | 116_14_90_3 | 4672 | **4568** | 104 |
| 117 | 117_14_90_5 | 7413 | **7279** | 134 |
| 118 | 118_14_90_6 | 7901 | **7701** | 200 |
| 121 | 121_14_100_4 | 6234 | **5984** | 250 |
| 122 | 122_14_100_5 | 8099 | **7769** | 330 |
| 123 | 123_14_100_7 | 8673 | **8527** | 146 |
| 126 | 126_14_110_4 | 6447 | **6283** | 164 |
| 127 | 127_14_110_6 | 9165 | **8847** | 318 |
| 128 | 128_14_110_8 | 8715 | **8605** | 110 |
| 131 | 131_14_120_4 | 6163 | **6139** | 24 |
| 132 | 132_14_120_6 | 9885 | **9499** | 386 |
| 133 | 133_14_120_8 | 10709 | **10355** | 354 |
| 136 | 136_14_130_5 | 7816 | **7524** | 292 |
| 137 | 137_14_130_7 | 11406 | **10770** | 636 |
| 138 | 138_14_130_9 | 10566 | **10530** | 36 |
| 141 | 141_14_140_5 | 7915 | **7677** | 238 |
| 142 | 142_14_140_7 | 11507 | **10935** | 572 |
| 143 | 143_14_140_10 | 11255 | **11145** | 110 |
| 146 | 146_14_150_5 | 7761 | **7651** | 110 |
| 147 | 147_14_150_8 | 13141 | **12393** | 748 |
| 148 | 148_14_150_10 | 12992 | **12716** | 276 |
| 156 | 156_28_20_1 | 3359 | **3298** | 61 |
| 157 | 157_28_20_1 | 3074 | **2999** | 75 |
| 161 | 161_28_30_1 | 3058 | **2997** | 61 |
| 162 | 162_28_30_2 | 4937 | **4813** | 124 |
| 163 | 163_28_30_2 | 4896 | **4794** | 102 |
| 166 | 166_28_40_2 | 6467 | **6217** | 250 |
| 167 | 167_28_40_2 | 6455 | **6411** | 44 |
| 168 | 168_28_40_3 | 6000 | **5942** | 58 |
| 171 | 171_28_50_2 | 6207 | **6069** | 138 |
| 172 | 172_28_50_3 | 8164 | **8110** | 54 |
| 173 | 173_28_50_4 | 7399 | **7397** | 2 |
| 176 | 176_28_60_2 | 6233 | **6195** | 38 |
| 177 | 177_28_60_3 | 9343 | **9245** | 98 |
| 178 | 178_28_60_4 | 11590 | **11288** | 302 |
| 181 | 181_28_70_3 | 9509 | **9359** | 150 |
| 182 | 182_28_70_4 | 12791 | **12413** | 378 |
| 183 | 183_28_70_5 | 12291 | **12195** | 96 |
| 186 | 186_28_80_3 | 9466 | **9284** | 182 |
| 187 | 187_28_80_4 | 13012 | **12722** | 290 |
| 188 | 188_28_80_6 | 13799 | **13791** | 8 |
| 191 | 191_28_90_3 | 9142 | **9094** | 48 |
| 192 | 192_28_90_5 | 14830 | **14442** | 388 |
| 193 | 193_28_90_6 | 14741 | **14547** | 194 |
| 196 | 196_28_100_4 | 12613 | **12379** | 234 |
| 197 | 197_28_100_5 | 15969 | **15451** | 518 |
| 198 | 198_28_100_7 | 17649 | **17547** | 102 |
| 201 | 201_28_110_4 | 12674 | **12360** | 314 |
| 202 | 202_28_110_6 | 19760 | **18698** | 1062 |
| 203 | 203_28_110_8 | 19298 | **18988** | 310 |
| 206 | 206_28_120_4 | 12566 | **12140** | 426 |
| 207 | 207_28_120_6 | 19526 | **18720** | 806 |
| 208 | 208_28_120_8 | 19777 | **19661** | 116 |
| 211 | 211_28_130_5 | 15906 | **15402** | 504 |
| 212 | 212_28_130_7 | 22831 | **21467** | 1364 |
| 213 | 213_28_130_9 | 22510 | **22080** | 430 |
| 216 | 216_28_140_5 | 15732 | **15222** | 510 |
| 217 | 217_28_140_7 | 22719 | **21503** | 1216 |
| 218 | 218_28_140_10 | 21729 | **20349** | 1380 |
| 219 | 219_28_140_14 | 18990 | **18988** | 2 |
| 221 | 221_28_150_5 | 15859 | **15127** | 732 |
| 222 | 222_28_150_8 | 26127 | **24723** | 1404 |
| 223 | 223_28_150_10 | 24515 | **24039** | 476 |

## Not claimed

Optimality of any roster (three, on instances 23, 98 and 219, equal a lower bound from our own screen; that is information, not a claim); anything about instances not listed; anything about the search method beyond how-we-built-it/. The closed-source official verifier was not run by any agent; the rosters follow the site's example format (0-based days) but omit the schema reference, the metadata fields and the WorkLength attribute, and the site's Solution.xsd is not published, so a format rejection by the official tool cannot be ruled out. The search was exploratory and not preregistered; the plan fixing the object list and the checks was frozen after it (how-we-built-it/PREREG.md).

## Credits

Instances, definition and table: Tim Curtois and Yi Qu, [Shift Scheduling Benchmark Data Sets](https://www.schedulingbenchmarks.org/matsp/). Best known values: Laszlo Kalman Trautsch and Bence Kovari, [Journal of Scheduling (2026)](https://doi.org/10.1007/s10951-026-00886-z). Tools: HiGHS, OR-Tools CP-SAT, NumPy, Numba. Run by the V3R1T4S kit: Antigravity (search) and Claude Code (lead agent, checks and claim), with three fresh reviewer subagents.
