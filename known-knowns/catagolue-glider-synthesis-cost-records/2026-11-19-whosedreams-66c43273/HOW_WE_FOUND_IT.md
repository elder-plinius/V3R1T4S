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
object came out of that sweep on the morning of 2026-11-04 (about 10 AM ET): xs27_3lkmz01iu1u8zw1221 (10 gliders) plus one glider on
lane 12 gives xs26_oo0o4qabqiczx321, listed at 35. It is the same search, and the same code, as the merged claims #969 and #970.

Novelty checks at packaging (2026-11-19): live Catagolue object page and xs26 class table (both 35, true); the input
xs27_3lkmz01iu1u8zw1221 is listed at 10 (true), so its route is already public. A general web search for the exact apgcode
(2026-11-19 about 10:23 ET) returned no page naming it. The ConwayLife forums were not searched or read in this run; a post giving
only an RLE, without the apgcode, would not be found by such a search anyway. No V3R1T4S known-knowns package or merged
claim names this object.

The plan file how-we-built-it/PREREG.md was written after the search, when this claim was packaged; it says so.
