# How we found it (contributor text, unverified)

Brief: find a glider synthesis cheaper than Catagolue's listed cost for some still life or oscillator.

What failed first: a shortest-path (Dijkstra) pass over Shinjuku's published components alone found nothing cheaper than
the Catagolue tables (the tables already are that minimum). Direct one-glider and two-glider attacks on the most
expensive objects were too slow or found nothing new for these particular still lifes.

What worked: take still lifes for which we already had a verified cheaper all-glider synthesis than Catagolue lists,
inject those as seeds into Shinjuku's component graph, and re-run Dijkstra. For any tabulated object whose new shortest
path was cheaper than its live listed cost, the seed RLE was stitched with the path's published components into one
all-glider pattern (later stages' gliders rewound so they arrive after the previous stage settles), and the result was
checked with lifelib and a live re-read of the Catagolue cost. This object came out of that harvest on 2026-11-15:
the cheaper synthesis of xs26_08ehmkk8z6a87066 (12 gliders; V3R1T4S PR #969 (package 2026-11-06-whosedreams-a855292d), merged upstream as 1209b9b; Catagolue still lists 58 (true) at this refetch) plus 2 published-component gliders
gives a 14-glider synthesis of xs31_g8e1ugmmzd553w643, listed at 60 (true). Using only the still-listed Catagolue cost of the
seed (58) plus those 2 gliders would cost 60.

The ConwayLife forums were only text-searched, not read. On 2026-11-18 around 19:27 ET, searches for the part after the
underscore of this object and of its seed, the full apgcodes, and the general queries "cheaper syntheses" 2026 and
"synthesis" "xs28" 2026 found no post that named any of these codes. A post that gave only an RLE, without the apgcode,
would not have been found.

The plan file how-we-built-it/PREREG.md was written after the search, when this claim was packaged; it says so.
