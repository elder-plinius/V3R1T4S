# How we found it (contributor text, unverified)

The table gave 18-20 for dom(Q_11). The idea is a count. Twenty classes of 7 squares or more would need 140 squares
and the board has 121, so in a domatic 20-partition the classes must fall short of 7 by at least 19 squares in
total. A class of 6 squares falls short by one, a class of 5 by two, and no dominating set has fewer than 5 squares.
A dominating class of at most 6 squares contains one of 434 small dominating sets (the 2 dominating 5-sets and the
432 minimal dominating 6-sets, in how-we-built-it/lists/). In an earlier computation of ours, which is not part of
this package, at most 14 of those 434 sets are pairwise disjoint; so at most 14 classes can fall short, by at most
14 + 2 = 16 squares in total (one more for each of the two 5-sets), and 16 is less than 19. The certificate does not
rely on the number 14: the final refutation establishes the contradiction itself. The difficulty was to make a
proof checker follow such a count.

A plain SAT encoding does not work, because the argument counts, and resolution counts badly. What worked: (1) three
lemmas per class ("at least 5 squares", "at least 6 or contains a listed 5-set", "at least 7 or contains a listed
set"), each proved by the solver from the clauses that mention only that class and the lemmas proved before it, the
third cut into 31 cases by the square that dominates the corner; (2) one final refutation of the formula plus the 60
lemma clauses; (3) the counting bound itself derived inside that final proof, by introducing new variables through
definitions and stepping through the squares one at a time, so that it is not a premise. Every refutation has a
DRAT proof checked by drat-trim: 681 per encoding, for two encodings written in separate contexts. Two scripts
written in separate contexts check that the 680 lemma refutations compose (two panel skeptics wrote their own as
well); a second proof checker written from the definition accepted all 2 x 680 saved proofs of the chain (on the
two proofs of the final step it reached its time limit and gave no verdict).

What failed on the way: holding the solver's proof in memory (the machine ran out); checking binary proofs with a
text-mode build of the checker on Windows (it silently corrupts them); one proof per class (too large to load);
merging everything into one proof file (80% of the lemmas are needed: about 28 GB for the first encoding, more for
the second).
