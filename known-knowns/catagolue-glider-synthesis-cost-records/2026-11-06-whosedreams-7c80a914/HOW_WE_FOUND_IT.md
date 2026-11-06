# How we found it (contributor text, unverified)

Brief: find a glider synthesis cheaper than Catagolue's listed cost for some still life or oscillator.

What failed first: a shortest-path (Dijkstra) pass over Shinjuku's components found nothing cheaper than the Catagolue
tables for xs24 (the tables already are that minimum). Attacking the most expensive xs24 object (167 gliders) through
its 8-glider bottleneck edge found nothing with one glider and was too slow with two.

What worked: brute force with one glider. Every still life of 24 to 28 cells that Catagolue can already build was hit
with a single glider on every lane, phase and direction (about half a million inputs). Whenever the collision left
one clean still life whose listed cost was higher than the input's cost plus one, the published route to the input
was stitched with the extra glider into one all-glider pattern (later stages' gliders rewound so they arrive after the
previous stage settles), and the result was checked with lifelib and a live re-read of the Catagolue cost. This
object came out of that sweep on the evening of 2026-11-05: xs27_8ehf8bbgz6430321 (31 gliders) plus one glider on
lane 4 gives xs27_0ca1ugmicz651346, listed at 66. Three fresh reviewers then checked it separately (reproduction with
their own simulator, novelty against Catagolue, Shinjuku and the forums, and the criterion wording).

The plan file how-we-built-it/PREREG.md was written after the search, when this claim was packaged; it says so.
