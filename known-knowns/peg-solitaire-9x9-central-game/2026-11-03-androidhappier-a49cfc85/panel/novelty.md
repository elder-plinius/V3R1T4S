# NOVELTY skeptic: peg-solitaire-9x9-central-game

context: subagent (executor NOVELTY, scratch $TMPDIR/panel1321-novelty)

Inputs read: only the claim package (claim.md, table_record.md, result/sol31.txt, code/check9.py, data/). No run NOTES or REPORT were read.

## 1. Status page, one honest fetch (no retries)

- Command: `nice -n 19 curl -s -A V3R1T4S https://www.gibell.net/pegsolitaire/`
- Time: 2026-11-03T14:10:42Z to 14:10:43Z (09:10 EST). HTTP 200.
- sha256 0cab8355faee4011f206a657fb79c15338f090d90500168e682862b5173e4e68. This is byte-identical to data/bell_index.html (scout 13:21:08Z) and data/bell_index_claim.html (claim 14:09:43Z).
- Page: "Last Modified October 23rd, 2026". In the section "The 9x9 Board (81 holes)": "On this board, what is the shortest solution to the central game? This is currently an open question. In 2004, Alain Maye found a solution by hand in 34 moves."
- **Value to beat: 34 moves (Maye, 2004). Status: open.**
- 9x9 subpage: the parent fetched https://www.gibell.net/pegsolitaire/9x9/9x9index.html at 2026-11-03T14:11:36Z (HTTP 200) and saved it as data/bell_9x9_gate.html, sha256 59f3a9d9f84177a02d92e19316c68d08f229a8085c83a27d7d35f8958ada5c6c. I checked the hash and read the file; I did not fetch this page myself. It says: "Last Modified November 14th, 2015", "The best solution I have seen was constructed by Alain Maye, by hand, and has 34 moves", and a lower bound of 24.

## 2. Object vs. cell

- The cell is the central game on the 9x9 square board (81 holes, orthogonal jumps only), from e5 to e5. A move is a maximal run of consecutive jumps by one peg.
- Object: result/sol31.txt, 31 lines. I re-ran `python3 code/check9.py result/sol31.txt` and got: `jumps=79 moves=31 pegs_left=1 final=e5`, `VALID central game e5->e5 in 31 moves`. The jump count of 79 matches 81 − 1 − 1.
- 31 < 34 by 3 moves, so this is a strict improvement, not a tie. A trivial edit of Maye's object, such as a symmetry or reordering, cannot change the move count by 3, so the result counts as a new object for this cell.
- It also meets the bank's success criterion (≤ 33 moves, strictly below Bell's 34).

## 3. Literature and code (last 24 months, to 2026-11-03)

- Web searches: "9x9 peg solitaire central game shortest solution moves"; "9x9 peg solitaire 31/32/33 moves central game"; "peg solitaire square board 9x9 shortest solution 2025 2026 arXiv github beam search". Every hit (gibell.net and the recmath.org mirrors) gives Maye's 34 as the best and the minimum as open. isnphard.com/g/solitaire-army covers a different problem (the Solitaire Army desert, 39 moves), not this cell. Markus Thill's 2024 blog post covers Diamond-41, and arXiv math/0606122 covers diagonal-jump boards. No 9x9 orthogonal central-game solution under 34 moves turned up.
- GitHub repository search "peg solitaire 9x9": 0 results.

## 4. This repo (elder-plinius/V3R1T4S)

- TROPHY_CASE.md (raw main, 31306 bytes): no match for peg, solitaire, 9x9 or Bell.
- known-knowns/ (27 folders listed via the contents API): no peg-solitaire folder.
- Code search "solitaire" finds only the bank entries known-unknowns/graphs-games-automata/peg-solitaire-9x9-central-game.md (which still says open, best 34) and triangular-peg-solitaire-shortest-11-12.md, plus the README and an unrelated metamath file.
- Pull requests, open and closed: search for solitaire / 9x9 / Maye / "central game" / gibell found only #905 and #906 (triangular boards T11 and T12, a different cell). I also listed the 100 most recent PRs (#814, 2026-10-28, through #917, 2026-11-03T13:57:35Z) and scanned titles and bodies: there is no 9x9 claim.

## 5. Notes (not blocking)

- claim.md calls the board "9x9 English peg-solitaire". That is a misnomer: it is the 81-hole square board ("The 9x9 Board (81 holes)" on Bell's page). The wording should be fixed before packaging. The object and checker use the correct board.
- This is an upper bound only. Nothing about optimality is claimed or shown (Bell's lower bound is 24).

## Verdict

The table value is 34 moves (Bell, fetched 2026-11-03T14:10:42Z, HTTP 200). The claimed object has 31 moves, verified VALID. Nothing published in the last 24 months, in the repo trophy case, in known-knowns, or in any PR reaches 33 or fewer. The result strictly beats everything known.

pass: true
