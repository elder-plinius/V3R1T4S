# A_4^GC,RC(n,d,w) (n=18 d=13 w=9): 36 words for GC,RC at (n, d, w) = (18, 13, 9), beating the King table entry 21

## What

The file object lists 36 distinct words of length 18 over ACGT, each with exactly 9 letters from C and G and pairwise Hamming distance at least 13 and Hamming(x, rc(y)) at least 13 for all x, y including x = y, which beats the live King-page entry 21 for this cell; comparison with post-2010 literature is not decided here.

## Check it yourself

From this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Requirements**: `python3` 3.8 or later, standard library only.
- **Rough laptop time**: well under a few seconds.
- **Expected last line**: `ALL CHECKS PASS` (the script also runs two negative controls that must be rejected).

## Compared to

| Source | Cell | Value | URL | UTC fetch time |
|---|---|---|---|---|
| King table page (last updated June 23, 2010) | GC,RC, n=18, d=13 | 21 | https://rambutan.umassmed.edu/king/dnacodes.html | 2026-10-19T05:15:07Z (novelty skeptic, HTTP 200); 2026-10-19T04:34:24Z (triage, HTTP 200, same page sha256 25d6e9f8...) |
| Aboluion 2011 PhD thesis, Tables 10.69 to 10.72 (maximum over w; entry 21m3) | n=18, d=13 | 21 | https://pure.southwales.ac.uk/ws/portalfiles/portal/991721/PhD_thesis_Niema.pdf | 2026-10-19T05:15:33Z (HTTP 200) |
| Survey arXiv:1607.00266 | no GC table; RC tables repeat the thesis values | no separate value | https://arxiv.org/pdf/1607.00266 | 2026-10-19T05:15:33Z (HTTP 200) |
| arXiv:1903.03535, 2108.02033, 2403.11551, 2409.06519 | comparison tables do not contain this (n, d) with w = floor(n/2) | no value | https://arxiv.org/abs/1903.03535 , https://arxiv.org/abs/2108.02033 , https://arxiv.org/abs/2403.11551 , https://arxiv.org/abs/2409.06519 | 2026-10-19T05:16:20Z to 05:20:17Z (HTTP 200; per-paper times in panel/novelty.md) |

Snapshot metadata with HTTP status and page sha256: `the-record-we-beat/README.md`. The panel's novelty report is `panel/novelty.md`. The table value used in INDEX.csv is 21, fetched 2026-10-19T04:34:24Z.

## Not claimed

- Comparison with post-2010 literature is not decided by the gate (the gate's confirmed_scope says so in these words). The readable sources, listed above, have no value at or above 36 for this cell.
- Two sources were not read, in plain words: Aboluion, Smith and Perkins, Discrete Math. 312 (2012) 1062-1075, and Montemanni, Smith and Koul, Lecture Notes in Management Science 6 (2014) 167-175, were behind a paywall and not retrievable with one plain request. The 2014 chapter is the one source that could plausibly hold a small improvement on this kind of entry. Google Scholar was not searched.
- The novelty skeptic passed this cell because its margin over every readable value (King table, Aboluion thesis, four arXiv papers) is at least 3 codewords. This cell's margin is 15 (36 against 21). If the unread 2014 chapter holds a value within that margin, the claim would not be new.
- The thesis table gives the maximum over w, not the value at the fixed w = floor(n/2). That can only make a thesis value larger than the fixed-w value, and the thesis value for this cell (21m3) is not above the claim. The thesis number cannot be matched to the fixed-w cell exactly.
- The claim is a lower bound only: it says nothing about the best possible size, about other (n, d) cells, or about the other table (the GC table and the GC,RC table are different constraints).
- The panel's three skeptics are Claude Code subagents of one model family; the object's builder (Gemini, Argon) is a different family. The skeptics were given only the claim folder. This is not peer review.
- The panel checked the object file as shipped (sha256 e5eed8a3ba787f959f144f130a6fe81dde0a14f60d6b7ed7d79a1f17df2fd852).

Gate notes, as written by the gate (panel/gate.md):

- Object: object/gc_rc_18_13_9.txt, sha256 e5eed8a3ba787f959f144f130a6fe81dde0a14f60d6b7ed7d79a1f17df2fd852.
- Panel verdicts: reproduce `pass: true`, novelty `pass: true`, criterion `pass: true`.
- confirmed_scope is the criterion skeptic's sentence, quoted word for word.
- The three skeptics are Claude Code general-purpose subagents, each started fresh and given only the claim folder; the object's builder (Gemini, Argon) is a different model family from every skeptic.
- The Montemanni-Smith-Koul 2014 chapter was not readable (paywalled); the novelty skeptic passed this cell because its margin over every readable value (King table, Aboluion thesis, four arXiv papers) is at least 3 codewords.

## Credits

- **Oliver King**, the DNA-code table at https://rambutan.umassmed.edu/king/dnacodes.html (last updated June 23, 2010) and the paper Bounds for DNA codes with constant GC-content, Electronic Journal of Combinatorics 10 (2003) R33, https://www.combinatorics.org/ojs/index.php/eljc/article/view/v10i1r33: the table compared against and the definitions of the GC and GC,RC cells.
- **Aboluion**, PhD thesis (2011), https://pure.southwales.ac.uk/ws/portalfiles/portal/991721/PhD_thesis_Niema.pdf: the thesis tables compared against; and Aboluion, Smith and Perkins, Discrete Math. 312 (2012) 1062-1075, and Montemanni, Smith and Koul, Lecture Notes in Management Science 6 (2014) 167-175, named by the panel as sources that were not readable.
- The authors of arXiv:1607.00266 (survey of DNA coding theory), arXiv:1903.03535, arXiv:2108.02033, arXiv:2403.11551 and arXiv:2409.06519, listed at https://arxiv.org/abs/ with those numbers: compared against; we do not name individual authors we did not see attributed in a fetched page.
- The table page's own references (its guide letters for linear coding, local search and variable-neighbourhood search) name further sources; see the page.
- The search code and pre-registration: the contributor's AI search agent (Gemini, Argon), under the contributor credit `calgulbenkian`.
