# Glue-potential lead cluster Pb_121 (CCD): a certified minimum 0.2676 eV below the table row

## What
The 121 coordinates in result/Pb_121.xyz form a certified local minimum of the Lim-Ong-Ercolessi Pb glue potential (data/lead.f) at -198.47902916627225 eV, 0.26763 eV below the N = 121 value of the lead table as fetched 2026-11-23T07:06:49Z (-198.211397 eV), and 0.26763 eV below the polished posted N = 121 structure, with no lower published value found by web search; this is conditional on the gate's live re-fetch still showing -198.211397 (or any value above -198.479029) for N = 121.

(The panel saw the object as claim/result/Pb_121.xyz and the potential as claim/data/lead.f; in this package the same
bytes are object/Pb_121.txt, sha256 8ca649c53d8313596865518053c774f590b05616361f9f239b6705388b47d2d9, and lead.f is fetched by the checker.)

## Check it yourself
`sh verify-it-yourself/run_checks.sh` (needs curl and python3 with numpy, scipy and mpmath; set V3R1T4S_PYTHON to choose
the interpreter). It fetches the CCD lead point archive and the archived lead.f once each and checks their sha256, then
it calibrates a pure-Python evaluator on ten random posted files plus N = 121, polishes the object in 30-digit mpmath,
counts Hessian modes, and polishes the posted N = 121 structure. Expected last line `PASS` (under a minute on a laptop).

## Compared to
| table | cell | value | URL | fetched (UTC) |
|---|---|---|---|---|
| CCD glue lead clusters (Doye and Hendy 2003) | N = 121 | -198.211397 eV | https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/lead/table.html | 2026-11-23T07:06:49Z; NOVELTY panel 07:23:51Z; gate 07:47:19Z (all byte-identical) |

## Not claimed
- Not a global minimum: only that this certified local minimum lies below the table row and below everything the
  panel and the authors' trivial-edit bars reached from the posted structures (the 2- and 3-atom relocation families
  were sampled, about 40,000 trials each side, not searched exhaustively).
- Nothing about real lead clusters: these are energies of one empirical model potential (Lim-Ong-Ercolessi glue).
  Doye (2004) argues this potential has deficiencies; the Pb Gupta table is a different potential.
- No other cell is claimed. Neighbouring Pb cells (118..123) also have structures below the table in our notes; they
  are unpanelled and are not part of this package.

## Credits
- J. P. K. Doye and S. C. Hendy, "The structure of small lead clusters", Eur. Phys. J. D 22, 99 (2003),
  https://arxiv.org/abs/cond-mat/0207432 (the table).
- H. S. Lim, C. K. Ong and F. Ercolessi, Surf. Sci. 269/270, 1109 (1992) (the potential); F. Ercolessi's lead.f,
  archived at http://web.archive.org/web/20170523125240/http://www.fisica.uniud.it:80/~ercolessi/potentials/Pb/
- D. J. Wales and the Cambridge Cluster Database, https://www-wales.ch.cam.ac.uk/CCD.html
- J. P. K. Doye, "Lead clusters: different potentials, different structures", https://arxiv.org/abs/cond-mat/0405234
- Basin hopping: D. J. Wales and J. P. K. Doye, J. Phys. Chem. A 101, 5111 (1997).
