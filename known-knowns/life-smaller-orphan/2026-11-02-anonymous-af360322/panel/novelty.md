# NOVELTY skeptic verdict: no 5 x w Life orphan for w <= 8 (new size 5x8), target life-smaller-orphan (partial win p1)
context: fresh headless Grok Build CLI session (grok --prompt-file), started with no prior conversation in a copy of claim/

## What you read
- `claim/CLAIM.md` and `claim/TARGET_CRITERION.md` only, to see that the offered statement is “no Life orphan in a 5×w box for w ≤ 8,” with 5×8 (area 40) as the new size. Did not use `claim/NOVELTY_RECORD.md`.
- Hartman, Heule, Kwekkeboom, Noels, “Symmetry in Gardens of Eden,” Electron. J. Combin. 20(3) (2013) #P16, PDF `https://www.combinatorics.org/ojs/index.php/eljc/article/download/v20i3p16/pdf` (DOI `https://doi.org/10.37236/2611`). Full text via `pdftotext`. They prove no orphan inside a 6×6 box (improving an older 6×5 bound) and say a 6×7 search was then out of reach (§5.4, pp. 15).
- Randall D. Beer, “Cultivating the Garden of Eden,” Complex Systems 32 (2023), PDF `https://content.wolfram.com/sites/13/2023/06/32-1-1.pdf` (preprint `https://arxiv.org/abs/2210.07837`, `https://arxiv.org/pdf/2210.07837`). Square grids only. Proves every 7×7 configuration has a precursor (562,949,953,421,312 configurations). For 8×8, only a density window and a heuristic that none exist; nonsymmetric 8×8 is left open. A configuration of an n×n region is a full assignment with no (n+2)×(n+2) precursor, so this is the orphan problem on squares.
- LifeWiki Garden of Eden, `https://conwaylife.com/wiki/Garden_of_Eden` (page dated 2026-06-05; current source via `https://www.conwaylife.com/w/index.php?title=Garden_of_Eden&diff=cur&oldid=119133` and the edit source). States: no Garden of Eden inside a 7×7 box (cites Beer); no reflectionally or rotationally symmetric Garden of Eden in 8×8 or 9×9 (cites Hartman et al.); 8×8 density between about 0.15 and 0.8 is only a constraint plus a heuristic. Shortest known height-5 orphan is Eker’s 5×45 (`https://conwaylife.com/wiki/Garden_of_Eden` records table; Flammenkamp `http://wwwhomes.uni-bielefeld.de/achim/orphan_10th.html`). Smallest known bounding-box area is Eker’s 8×12 = 96.
- Achim Flammenkamp, `https://wwwhomes.uni-bielefeld.de/achim/orphan.html` (2017-01-27): Eker proved no height-2 or height-3 Garden of Eden and found a height-5 orphan; height 4 was then open. Records only “all patterns bounded by a 6×6 rectangle have a predecessor” (Heule et al., end of 2011). No 5×8 negative result.
- Andrew J. Wade, forum post 2023-06-11, `https://conwaylife.com/forums/viewtopic.php?t=6042`, code `https://codeberg.org/ajwade/orphan_disprover`: no orphan of height 4, any width, when every cell in the four rows is specified. Same thread (2023-07-27 discussion linked from LifeWiki, and `https://conwaylife.com/forums/viewtopic.php?f=2&t=6066&p=164201`) keeps height-5 existence separate and does not claim a width bound of 8. A 2024-07-20 reply is about 4-row Gardens of Eden with live cells only, not about 5×8.
- Steven Eker 2016, as recorded on LifeWiki and Flammenkamp: height at least 4, and explicit orphans in 5×83 and 5×45. The phrase on LifeWiki is “the shortest known” height-5 box, not a proven minimum width.
- Nathaniel Johnston & Dave Greene, book source `https://raw.githubusercontent.com/nathanieljohnston/game-of-life-book/master/early_life.tex`: no orphan fits in a 6×7 box (Eker and Heule, 2016, independent of the later 7×7 result); no orphans of height 1, 2, or 3; a 5×45 orphan exists; height 4 was still open in that source.
- Wikipedia “Garden of Eden (cellular automaton),” `https://en.wikipedia.org/wiki/Garden_of_Eden_(cellular_automaton)` and the mobile HTML API: smallest known orphan is Eker’s 8×12 (57 live cells). No 7×7 or 5×8 non-existence sentence.
- Salo & Törmä, arXiv:1912.00692 (`https://ar5iv.labs.arxiv.org/html/1912.00692`): finite-support Gardens of Eden are in co-NP via a padding reduction. No small-box census.
- OEIS A196447 / A197734 (`https://oeis.org/search?q=id:A196447&fmt=text`, `https://oeis.org/A197734`): one greedy spiral construction of some Garden of Eden, not a 5×8 census.
- MathOverflow revisions `https://mathoverflow.net/revisions/188361/3` and `https://mathoverflow.net/revisions/206698/3`: orphan size discussed with outdated 10×10 / 10×11 bounds. No 5×8 theorem.
- GitHub `https://github.com/marijnheule/eden`: Heule’s old QBF Garden-of-Eden code, not a 5×8 result. Broader GitHub queries for “5x8” plus Life orphan did not surface a proof.
- arXiv searches for a later 5×8 / height-5 width paper (including 2024–2026) returned Beer, Salo–Törmä, and unrelated Life dynamics papers, not an exhaustive 5×8 result.

## What you ran
- Web searches (read-only) listed above, plus LifeWiki, forum, OEIS, MathOverflow, GitHub, and arXiv queries for “5×8”, “5x8”, “no orphan”, “6×7”, “7×7”, “height 5”, Eker, Wade, Beer, Hartman.
- `timeout 400 nice -n 19 sh -c 'mkdir -p .../scratch && cd .../scratch && curl -fsSL -o beer.pdf https://content.wolfram.com/sites/13/2023/06/32-1-1.pdf && curl -fsSL -o hartman.pdf https://www.combinatorics.org/ojs/index.php/eljc/article/download/v20i3p16/pdf && curl -fsSL -o early_life.tex https://raw.githubusercontent.com/nathanieljohnston/game-of-life-book/master/early_life.tex && pdftotext -q beer.pdf beer.txt && pdftotext -q hartman.pdf hartman.txt'` — exit 0; `wc -l` gave beer.txt 687, hartman.txt 1234, early_life.tex 1050.
- Key lines from those files:
  - Hartman: “There exists no orphan fitting in a 6×5 bounding box.” Later: “we improved the lower bound of 6×5 by proving that no orphans exist within a bounding box of 6×6 or smaller. Improving this lower bound to 6×7 or larger grid sizes falls outside currently available resources.”
  - Beer: “we have shown that no GOEs exist in 7×7 grids”; “What are the prospects for finding any 8×8 or 9×9 GOE configurations? … the nonsymmetric cases remain open”; heuristic “suggests that there will be no 8×8 GOEs”.
  - Book: “there does not exist an orphan that fits within a 6 × 7 bounding box”; caption “An orphan that fits within a 5 × 45 bounding box.”
- Scratch PDFs and text were deleted with `timeout 60 nice -n 19 rm -rf .../scratch`.

## Findings
No prior publication states, or implies, that there is no orphan in a 5×8 box.

A 5×8 rectangle does not fit in a 7×7 square, so Beer’s theorem (and LifeWiki’s “no Gardens of Eden contained within a 7×7 bounding box”) covers 5×w only for w ≤ 7, and every box with both sides ≤ 7. It does not cover 5×8 (area 40). Hartman’s published bound is 6×6. The Johnston–Greene source stops at 6×7. Wade 2023 clears every width at height ≤ 4 and does not clear height 5. Eker’s height-5 examples start at width 45 and are described as the shortest known, which is an existence record, not a proof that every smaller width is impossible.

Nothing found is an exhaustive census of all 5×w boxes through width 8, or of all boxes with maximum side 8. Beer’s 8×8 density window plus heuristic would, if it were a proof of “no 8×8 Garden of Eden,” imply no 5×8 orphan (a 5×8 orphan would complete to 8×8 Gardens of Eden). He explicitly leaves nonsymmetric 8×8 open. No source claims “no orphan with minimum side 5 and area ≤ 40.”

So 5×8 is not already ruled out in the public record. The smaller widths inside the claim (5×w for w ≤ 7) are already implied by the 7×7 theorem; the new public increment is 5×8.

## Caveats
Forum search on conwaylife.com is noisy (large RLE posts). I read the Garden of Eden wiki page, its cited threads (Wade t=6042, the orphan thread t=797), and Flammenkamp’s pages, and I did not open every historical forum page. I did not bypass Cloudflare. A private note or an unindexed post could exist; none of the standard citations, the 2013 and 2023 papers, the book source, Wikipedia, OEIS, MathOverflow, arXiv, or the Heule GitHub repo contains a 5×8 non-existence proof. This review did not check the SAT certificates; that is outside the novelty question.

scope: Verified from the public literature that no orphan result already covers a 5×8 Life box (Beer’s 7×7 and Wade’s height ≤ 4 stop short of it); did not audit the claim’s proofs or search non-public correspondence.
pass: true
