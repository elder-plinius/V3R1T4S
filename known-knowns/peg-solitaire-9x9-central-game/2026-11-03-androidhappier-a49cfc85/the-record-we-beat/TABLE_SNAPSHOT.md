# Table snapshot: peg-solitaire-9x9-central-game

Status source: George I. Bell, Peg Solitaire pages. The pages themselves are not copied here; only their fetch
records and the extracted cell.

| page | URL | fetched (UTC) | HTTP | sha256 of the page bytes | stage |
|---|---|---|---|---|---|
| main index | https://www.gibell.net/pegsolitaire/ | 2026-11-03T13:21:08Z | 200 | 0cab8355faee4011f206a657fb79c15338f090d90500168e682862b5173e4e68 | scout |
| main index | https://www.gibell.net/pegsolitaire/ | 2026-11-03T14:09:43Z | 200 | 0cab8355faee4011f206a657fb79c15338f090d90500168e682862b5173e4e68 | claim (byte-identical to scout) |
| main index | https://www.gibell.net/pegsolitaire/ | 2026-11-03T14:10:42Z | 200 | 0cab8355faee4011f206a657fb79c15338f090d90500168e682862b5173e4e68 | novelty skeptic (same) |
| 9x9 subpage | https://www.gibell.net/pegsolitaire/9x9/9x9index.html | 2026-11-03T14:11:36Z | 200 | 59f3a9d9f84177a02d92e19316c68d08f229a8085c83a27d7d35f8958ada5c6c | gate re-fetch |

Selected page facts:
- Main index: "Last Modified October 23rd, 2026". Section "The 9x9 Board (81 holes)": "On this board, what is the
  shortest solution to the central game? This is currently an open question. In 2004, Alain Maye found a solution
  by hand in 34 moves."
- 9x9 subpage: "Last Modified November 14th, 2015"; "The best solution I have seen was constructed by Alain Maye, by
  hand, and has 34 moves"; it gives a lower bound of 24 moves. No solution shorter than 34 is listed. (At scout time,
  2026-11-03T13:21Z, this subpage returned HTTP 500; the gate re-fetch above returned 200.)

## Extracted cell

| table | cell | value | holder | status |
|---|---|---|---|---|
| Bell, 9x9 board (81 holes), central game e5 -> e5, orthogonal jumps | shortest known solution (moves = maximal same-peg jump runs) | 34 moves | Alain Maye, 2004 (by hand) | open (Bell: "currently an open question"; lower bound 24) |

This package's object: 31 moves (79 jumps). 31 < 34.
