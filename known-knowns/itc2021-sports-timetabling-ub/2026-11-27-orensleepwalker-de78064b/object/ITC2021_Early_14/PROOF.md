# Proof that the Early 14 optimum is 4

Assume there is a feasible Early 14 schedule of penalty at most 3. A break means two consecutive home games or two consecutive away games. BR2 covers all 20 teams and all 38 rounds. A 19th break alone would cost 10, so the schedule has at most 18 breaks.

A team with no break must alternate, with two possible starting venues. Two teams with identical venue sequences cannot meet, since each of their meetings needs a home team and an away team in the same round. Thus at most two teams have no break. At least 18 teams each need at least one break, so every team has at most one break.

Every team plays 19 home games. The hard fixtures with slot IDs 7 and 4 force team 0 and team 15, respectively, to be away in those slots. For each of those teams enumerate the two starting venues and the optional location of a single break. Keep balanced sequences that are away on the required slot. This gives 19 patterns for each team. Adding the costs of just their soft CA1 rules gives minimum 3 for team 0, attained by starting away and breaking at slot 6, and minimum 1 for team 15, attained by starting away and breaking at slot 28. These minima can be checked from the XML by `certificate.py` or from the full enumeration in `patterns.csv`.

The two CA1 sums concern different teams and different rule rows. All other penalties are nonnegative. The supposed schedule therefore costs at least 4, a contradiction. Team Gionar's published schedule has no hard violations and penalty 4, so the lower bound is attained.
