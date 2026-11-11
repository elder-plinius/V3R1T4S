# How we found it (contributor text, unverified)

The brief: Lee and Shan's 2002 computer check stopped at 17 vertices, and the bank's full criterion asks for every
tree up to 25. Earlier packages took it to 20 (#917) and 22 (#945). This run did 23, 24 and 25 on the contributor's
own desktop, at low priority on 16 and then 28 of its 32 threads: 14.8, 39.3 and 104.6 million trees.

The search was the same code at every order: an alpha-labeling search first, a randomised backtracker on what was
left, the caterpillar construction of Enomoto, Llado, Nakamigawa and Ringel after that, and a long last-resort search.
Each order took about 3.4 times the one before (8.6 hours, 23 hours, 3.5 days), faster than the tree count grows,
because the hard trees get harder.

What did not go to plan, and what we did about it: at each new order some trees beat the search's time limit (301,
then 1,012, then 23,458). Each time a longer search labelled them all, mostly within minutes; at n = 25 the last
1,471 needed a second, longer pass. Every change of that kind was written into the pre-registration before the
results it affected existed. The leftover trees turned out to be one family: short, bushy trees with several hubs,
never caterpillars (the construction handles those), almost all lobsters. They are listed in how-we-built-it/leftovers/
for anyone looking for where a counterexample would have to live.

The checking took nearly as long as the search: two checkers on every line of every order, the second one regenerating
every tree from scratch, then three fresh-context skeptics who each wrote their own.
