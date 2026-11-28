# How we found it (contributor text, unverified)

Plain tabu search on colourings of the board could not even rebuild the published partitions, so we changed the
representation: for plain domination, a k-partition exists exactly when k pairwise disjoint dominating sets exist
(left-over squares can join any class). Shrinking classes to minimal dominating sets gives a counting constraint
(2 t5 + t6 >= 7k - 121 for Q_11), which told us a 19-partition must use about a dozen minimal 6-sets. We enumerated all
of them exhaustively (2 five-sets, 432 minimal six-sets), let a MILP propose disjoint families of them, enumerated every
dominating 7- and 8-set in the remaining squares, and packed those. The fourth family tried gave 19 classes.
