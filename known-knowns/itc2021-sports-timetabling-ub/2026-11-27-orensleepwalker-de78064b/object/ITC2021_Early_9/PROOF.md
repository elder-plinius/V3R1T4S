# A lower bound of 40 for ITC2021 Early 9

A repeat occurs when a team plays at the same venue type, home or away, in two consecutive slots. At most two teams can have zero repeats. They must alternate, and two teams with equal venue sequences could never play each other. Thus at least 16 teams have a repeat.

Team 2 must play away in slot 13 against Team 5 and play 17 of 34 matches at home. Exhaustively enumerate both initial venues and every choice of up to three repeat indices. The hard CA1 rules and the forced away slot eliminate every pattern with fewer than three repeats. Exactly 16 three-repeat sequences survive. Each has at least one odd repeat index. The attached CSV and standard-library program calculate these counts from the original instance.

Thus Team 2 plus the other repeating teams require at least 3+15=18 repeats. Suppose exactly 18 suffice. Then Team 2 repeats exactly three times, 15 other teams repeat once each and two teams never repeat. Any balanced sequence of 34 slots with one repeat has its repeat at an even slot index. If it occurred at an odd index, the alternating prefix and suffix would both be odd in length and have the same majority venue, violating balance.

So at an odd index where Team 2 repeats, every other team alternates. Each slot has exactly nine home teams, so any home-home repeat must be balanced by an away-away repeat and vice versa. A single repeat is impossible. At least 19 repeats are therefore needed. At every transition, equal home-home and away-away counts also make the total number of repeats even. The entire season must consequently have at least 20 repeats. BR2 allows the first 16 without penalty and charges 10 for each additional repeat. Every other penalty is nonnegative, so a feasible Early 9 timetable has penalty at least 40.

The CP-SAT model represents the two cases where Team 2 has exactly three repeats with an odd index, or at least four repeats. Both force at least 19 total repeats. Its objective bound of 40 applies to the original instance by the projection above.
