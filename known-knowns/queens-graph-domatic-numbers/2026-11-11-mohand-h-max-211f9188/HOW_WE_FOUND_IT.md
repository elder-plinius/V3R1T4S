# How we found it (contributor text, unverified)

A superset of a total dominating set is total dominating, so every class of a total domatic partition can be shrunk to
a minimal one. Q_10 has total domination number 6 and 100 squares, so 16 classes leave a slack of only 4 squares: at
least 12 classes must be total dominating 6-sets. We enumerated those exhaustively (216, with an enumerator that
branches on an undominated square). At most 15 of them are pairwise disjoint by an exact linear-programming dual, and
an integer program found 14. We then enumerated families of 14 disjoint ones and tested whether the 16 squares left
over split into two total dominating sets. The sixth family did, giving 14 classes of 6 squares and 2 classes of 8.
