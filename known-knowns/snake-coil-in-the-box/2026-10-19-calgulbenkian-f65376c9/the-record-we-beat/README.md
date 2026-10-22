# The record we compare against (metadata and saved excerpts)

Each row is one honest GET (curl, User-Agent naming V3R1T4S, no retries). The first two rows were made by the orchestrator's triage agent, the Caltech CSV rows by the builder on 2026-10-19 (identical bytes to the author's snapshot copies).

| Source | URL | UTC fetch time | HTTP | sha256 | Extracted cell |
|---|---|---|---|---|---|
| minortriad_snake.html | https://www.minortriad.com/snake/ | 2026-10-19T04:32:30Z | 200 | af45d6499dcae6cb6d3e1942c5ccd0ab8159c7755dec1667e097a1859dfcebb2 | table value for the cell: 1434; page analyzer symmetric test quoted in minortriad_page_symmetric_test.txt |
| caltech_snake_README.md | https://raw.githubusercontent.com/Math-AI-Caltech/Snake-in-the-Box/main/README.md | 2026-10-19T04:43:29Z | 200 | b56bf45b4a8bbbb2c5df625ccdaa47693d3832397333c683f691f00daec14a77 | README tables (snakes, coils, symmetric coils) and the sentence 'Subsequent bounds by others: 750 in Q11 (Echols), 1480 in Q12 and 2934 in Q13 (Itty)'; coils: 'Subsequent coil bounds by others: 740, 1468 and 2930 in dimensions 11-13'; symmetric table lists 10: 370, 11: 734 |

Table value used: 1434. Source: minortriad symmetric-coil column, dimension 12 (page https://www.minortriad.com/snake/, fetched 2026-10-19T04:32:30Z).

The minortriad page defines its symmetry test in its analyzer script (saved in minortriad_page_symmetric_test.txt, an excerpt of the page script).
