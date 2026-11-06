# How we found it

*Contributor text, unverified.*

The brief: Bell's peg solitaire pages list the shortest known central-game solution on the 81-hole 9x9 square board
as Alain Maye's 34-move hand solution (2004) and call the minimum an open question. The bank target asked for a
legal solution of at most 33 moves, strictly shorter than the table at claim time.

We wrote the replay checker first, straight from the definition (verify-it-yourself/check9.py), with three negative
fixtures, then a move-layer beam search in C (how-we-built-it/beam9.c): layer k holds the best B distinct
board positions (up to the 8 symmetries of the square) reachable in k moves, where a move is any chain of jumps by
one peg, ranked by a score of pegs left plus weighted terms.

What failed: ranking by pegs alone, or adding a filled-region (Merson-style) count, stranded pegs at B = 2,000 and
B = 20,000. What worked: adding penalties for isolated pegs and for pegs on the edge. With those, B = 20,000 solved
in 34 moves (a tie with Maye, kept as a calibration fixture), B = 100,000 in 32, and B = 200,000 in 31 moves
(79 jumps), in about 19 minutes on one core. A separately written C replay checker (replay9.c) and two hand-made
negatives built from the 31-move file (moves 3 and 4 swapped, last move dropped) were added as fixtures. Three
fresh skeptics (reproduce, novelty, criterion) passed it and the gate confirmed it; see panel/.

An earlier draft of the claim called the board "English"; that was wrong (English is the 33-hole cross). This
package is about the 81-hole 9x9 square board only.
