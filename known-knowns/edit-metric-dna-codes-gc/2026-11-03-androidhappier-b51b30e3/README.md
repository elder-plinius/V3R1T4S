# A (9,3,4)_4 DNA edit-metric code with GC and reverse-complement constraints, 1042 codewords (best known: 939)

## What

Confirmed scope, quoted word for word from panel/gate.md:

> The 1042-word list in claim/object/code_n9_d3_k1042.txt (sha256 b51b30e3082648bc6cb0511bd156b71ae51c967f7281a83010d2c0e844e4a93a) is a code of length 9 over {A,C,G,T} with every word of GC weight 4 and Levenshtein distance at least 3 between any two distinct words and between any word and the reverse complement of any word including itself, which is strictly larger than the lower bound 939 (not marked exact) given for cell (n,d)=(9,3) in Table 7.1 of J. Sun's 2009 Brock M.Sc. thesis under that thesis's own constraint set; whether it also beats every later published value is left to the NOVELTY check.

The object is object/code_n9_d3_k1042.txt (same bytes as the run's claim/object/ file named in the quote, full sha256
b51b30e3082648bc6cb0511bd156b71ae51c967f7281a83010d2c0e844e4a93a).

Format: 1042 lines, each a codeword of 9 letters from {A, C, G, T}, newline-terminated.
Properties, in the constraint set of J. Sun's thesis (Sec. 1.5, E_4^{RC,GC}(n,d,w) with w = floor(n/2)):
- every word has exactly 4 letters from {G, C} (fixed GC weight w = floor(9/2) = 4);
- the Levenshtein (edit) distance, with substitutions, insertions and deletions each of cost 1, is at least 3 between
  any two distinct codewords;
- the edit distance between any codeword x and the Watson-Crick reverse complement rc(y) of any codeword y is at least
  3, including x = y (A<->T, C<->G, then reverse).
So E_4^{RC,GC}(9,3,4) >= 1042, for this one cell, lower bound only.

## Check it yourself

From this folder:

    sh verify-it-yourself/run_checks.sh

Expected last line: `PASS`. About 1-2 minutes on an idle laptop (see verify-it-yourself/RECEIPTS.md for the time
on a heavily loaded shared 8-core machine at nice 19). Python 3 standard library only. It checks the sha256, that
there are 1042 distinct words of length 9 over ACGT with GC weight 4, and, exhaustively over all 542361 pairs and all
1085764 ordered (x, rc(y)) pairs including x = y, the edit-distance constraints, by two independent methods (exact
Levenshtein distance by the bit-parallel form of the dynamic program, self-tested against the plain dynamic program,
and explicit radius-1 edit balls built by breadth-first search, met in the middle through a hash index). Six controls
must fail: the object read with d = 4 (method A only), a word replaced by a 1-substitution neighbour of another, a
duplicated word, a word replaced by the reverse complement of another, a word with GC weight 5, and a one-word code
whose word is within edit distance 2 of its own reverse complement.

The package also carries the family's plain-DP checker verify-it-yourself/verify_dna_edit_code.py (the same file,
unchanged, as in the (7,3), (8,3), (8,4), (9,4) and (9,5) packages of this family). It is too slow for 1042 words to
run inside run_checks.sh under a load-dependent time cap, so it is a by-hand cross-check (RUN_IT_YOURSELF.md); its
real output on this object is in RECEIPTS.md. Details in RUN_IT_YOURSELF.md and verify-it-yourself/RECEIPTS.md.

## Compared to

| table | cell (n, d), w = floor(n/2) | best known value | this package | fetched (UTC) |
|---|---|---|---|---|
| J. Sun, Bounds on Edit Metric Codes with Combinatorial DNA Constraints, M.Sc. thesis, Brock University (2009, deposited 2010), Table 7.1 "Best-known Bounds on DNA Codes" | (9, 3) | 939, superscript g (lower bound found by the thesis's Randomized GA; not marked exact) | 1042 | 2026-11-03 about 19:38Z (run), 20:25Z (panel, novelty), 20:27Z (panel, criterion), 20:49Z-20:50Z (packaging), unchanged |

URL: https://brocku.scholaris.ca/items/43d5f016-9190-4ec2-8066-81f3860f672b (repository item);
the table was read from the repository's extracted-text bitstream
https://brocku.scholaris.ca/server/api/core/bitstreams/afcc7fb0-758c-4e61-be7a-b5536c9f7fb6/content.
The same cell is 914* in Table 5.2 (exhaustive search that did not finish within two weeks, so a lower bound only),
939 / 869 / 855 in Tables 6.4 / 6.5 / 6.6 (GA) and 912 in Table 5.1 (lexicode). The snapshot record (fetch times,
statuses, metadata, hashes, the extracted rows) is in the-record-we-beat/TABLE_SNAPSHOT.md. The V3R1T4S bank target is
edit-metric-dna-codes-gc.

Panel copies: panel/ holds byte copies of the run's reproduce.md, criterion.md and gate.md. In panel/novelty.md one
machine-local path on line 4 (the skeptic's scratch folder, under the run's workspace) was replaced by
`[workspace]/scratch/panel-dna93-novelty-151037/claim/`, because the kit's leak check rejects absolute paths; nothing
else was changed (no wording, verdict or pass line). The run's original novelty.md has sha256
57be83793ac0375be0575d9a0740b8c16fa24f42a41c60ab5ba6ed24d588ab46.

## Not claimed

- Only the single cell (n, d) = (9, 3). The other cells explored in the carrier and sibling runs ((6,3), (7,3), (7,4),
  (8,3), (8,4), (9,4), (9,5)), packaged separately, are not part of this package and were not judged by this panel.
  The pre-existing 1011-word candidate (disclosed in the preregistration) and the other push results (1032, 1026 words)
  are not claimed either.
- No optimality: 1042 is a lower bound only. No upper-bound work was done for this cell (Sun gives no numeric upper
  bound for it; only Theorem 3, E^{RC,GC} <= E^{GC}/2).
- No other constraint (homopolymer runs, forbidden subwords, frame shift, other GC weights) is claimed. Unconstrained
  quaternary edit tables (Houghten's table, E_4(9,3) between 3451 and 9360), GC-only edit tables (Orth's Brock thesis,
  no n = 9 row) and Hamming-metric GC+RC tables (for example 906 for (9, d_H = 3) in the Hamming literature) are
  different quantities and are not compared or claimed here.
- "Best known" rests on the sources checked by the panel on 2026-11-03 (panel/novelty.md); it must be re-checked at
  submission time. Not opened: the journal version of the thesis (Sun, Houghten, Ross, Congressus Numerantium 204
  (2010) 65-92, presumed to carry the same tables; the main residual risk), the full text of Orth & Houghten, CIBCB
  2011, full texts of the Ashlock/Houghten CIBCB / ACM-BCB / BioSystems papers, and the full text of Benerjee &
  Banerjee, ISIT 2025 (paywalled; per its abstract a Hamming-type RC constraint). The thesis was read through the
  repository's extracted text, not the PDF image (the box's direct HTTPS connection to the repository fails at TLS).
- The preregistered push budget ("<= 30 min total") was borderline: the object was written 28.8 min after its own job
  started and about 30-31 min after the first push job started (disclosed in the run and to the panel; the 1032 and
  1011 fallbacks are also above 939).
- The construction is a seeded tabu local search over symmetry orbits, not a new algebraic construction.

## Credits

- Jing Sun, Bounds on Edit Metric Codes with Combinatorial DNA Constraints, M.Sc. thesis, Brock University, supervised
  by Sheridan Houghten (https://brocku.scholaris.ca/items/43d5f016-9190-4ec2-8066-81f3860f672b): the definition and
  the table compared against.
- V3R1T4S kit (target bank, panel protocol, checker gate): https://github.com/elder-plinius/V3R1T4S
- Contributor: GitHub account CharanRayudu (https://github.com/CharanRayudu), which submits this folder.
