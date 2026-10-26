# Voynich Generator Held-Out Fingerprints — Partial Win p2 (`VBCLC-152`)

Target: `voynich-generator-heldout-fingerprints` · status **CONFIRMED_PARTIAL** (partial win `p2`; three skeptics passed, honesty gate in `panel/gate.md`).

## What

Partial win p2 is achieved by the 152-entry hand-executable cipher VBCLC-152 (`claim/vbclc.py`, `claim/HAND_PROCEDURE.md`) using 1 per-folio state bit, which passes all four signatures of arXiv:2604.19762 jointly on 200/200 streams (20 period Latin and Italian plaintexts x 10 seeds) per cell across Currier A and Currier B separately on both ZL3b-n and IT2a-n (as well as RF1b-e), where the published slot and Cardan-grille generators fail.

That sentence is the CRITERION skeptic's `confirmed_scope`, copied verbatim from `panel/gate.md`.

In plain terms: Christophe Parisel (`arXiv:2604.19762`, 2026) defined four quantitative positional and sequential signatures of Voynich manuscript text (`E->S` directional asymmetry, `Bilat_full` $>100:1$ bilateral positional extremity, 10-chunk cross-boundary mutual information `MI`, and `Zipfian` initial-grapheme rank-frequency shape) and showed that neither a parametric slot-based generator (`signatures_v27.py`) nor Rugg's (2004) Cardan-grille generator (`grille.py`) reproduces all four signatures simultaneously. Here we construct **`VBCLC-152`** (`object/vbclc.py`, `object/HAND_PROCEDURE.md`), a hand-executable 152-entry table cipher ($\le 200$ table entries) with 1 per-folio dialect state bit $\sigma_f \in \{0, 1\}$, that interleaves global Zipfian ranks across 4 boundary macro-classes and enforces a non-merging boundary join rule, achieving a **200/200 (100.0%) joint pass rate on every dialect $\times$ transliteration cell** (`A/ZL3b`, `B/ZL3b`, `A/IT2a`, `B/IT2a`, `A/RF1b-e`, `B/RF1b-e`).

## Check it yourself

```sh
sh verify-it-yourself/run_checks.sh
```

Expected last line: `PASS` (preceded by `102 checks passed, 0 failed`). About 2 seconds on a laptop, Python 3 standard library only, no network. The checker verifies the `SHA-256` manifest of `object/`, audits the 152 table entries (`16 + 20 + 96 + 20 = 152 <= 200`) and 1-bit per-folio state $\sigma_f \in \{0, 1\}$ in `object/vbclc.py`, verifies all 1,200 evaluated streams in `object/vbclc_200streams_evaluation.json` (`200/200` per cell) and all 3,200 null controls in `object/null_suite_400_results.json` (`400/400` per cell), checks the failure of the published slot, Cardan-grille, and unmodified Naibbe baselines in `object/reference_calibration.json`, and re-derives all four Currier signatures from first principles on freshly generated `VBCLC-152` Currier A and Currier B streams. Changing a single digit in `object/` makes it print `FAIL`.

## Compared to

| what | value |
|---|---|
| target / partial win | `voynich-generator-heldout-fingerprints` / enumerated partial win `p2` (`arXiv:2604.19762` 4-signature joint pass across Currier A and B on `ZL3b-n` and `IT2a-n`) |
| published slot-based generator (`signatures_v27.py`) | **`0.0%` (`0/20`)** on `B/ZL3b` & `B/IT2a`; **`10.0%` (`2/20`)** on `A/ZL3b` & `A/IT2a` (`MI = 0.1396 < 0.2508` on B; `0.1771 < 0.2910` on A) |
| published Cardan-grille generator (`grille.py`, `G0/G1/G2/G6`) | **`0.0%` (`0/20`)** across all cells and grille modes (`E->S = 0.30% - 17.76% < 60.0%`) |
| unmodified Naibbe cipher (`naibbe.py`, Greshko 2025) | **`0.0%` (`0/40`)** fixed / strict-Zipf pass (`10.0%` adaptive on `A/ZL3b` & `A/IT2a`; `E->S = 52.9% - 53.2%`, `Shape = 40/40 Intermediate`) |
| this result (`VBCLC-152`, `object/vbclc.py`) | **`100.0%` (`200/200`)** joint pass across `A/ZL3b`, `B/ZL3b`, `A/IT2a`, `B/IT2a`, `A/RF1b-e`, and `B/RF1b-e` (`152 <= 200` table entries, `1 <= 1` per-folio state bit) |
| sources | <https://www.voynich.nu/transcr.html> and <https://arxiv.org/abs/2604.19762> (code at <https://github.com/labyrinthinesecurity/currier-signatures>) |
| fetched (UTC) | `2026-10-23T18:16:05Z` & `2026-10-23T18:18:04Z` by the run; re-fetched independently `2026-10-24T15:15:37Z` & `2026-10-24T15:15:38Z` by the NOVELTY skeptic (HTTP 200 both times) |

## Not claimed

- **Not a decipherment of the Voynich manuscript.** `VBCLC-152` is a constructive synthetic cipher-generator showing that a 152-entry hand-executable table cipher with 1 per-folio state bit reproduces all four Currier positional and sequential signatures of `arXiv:2604.19762`.
- **Full criterion `(A)` and partial win `p1` (`arXiv:2608.17096`) are not claimed.** While `VBCLC-152` simultaneously matches `arXiv:2608.17096` collapsed-EVA excess edge-glyph mutual information (`0.1281` bits on `A/ZL3b`, `0.2315` bits on `B/ZL3b`, reproducing the ~1.81x Currier B/A ratio) and singleton-type rate (`0.683` on A, `0.675` on B), its collapsed-EVA within-word conditional character entropy $h_2$ (`3.12` bits on A, `3.06` bits on B) and mean word length (`4.71` on A, `5.12` on B) sit above the manuscript's 95% bootstrap envelopes (`h2` in `[2.47, 2.54]` on A and `[2.19, 2.30]` on B; mean word length `3.80` on A and `4.05` on B). In `HOW_WE_FOUND_IT.md`, we prove the **Shannon-Heaps Length-Entropy-Singleton Theorem** explaining why a 3-slot independent-core concatenative table with $\le 200$ entries cannot simultaneously satisfy $V_1/V \ge 0.69$, $\bar{\ell}_c = 3.80$, and $h_{2,c} \le 2.52$ bits without multi-character rigid word stems.
- **Partial win `p3` (`arXiv:2604.25979`) is not claimed.**

## Credits

- The four Currier positional and sequential signatures, reference calibration protocol, and slot/Cardan-grille generator benchmarks: Christophe Parisel, *"Evidence of Layered Positional and Directional Constraints in the Voynich Manuscript: Implications for Cipher-Like Structure"*, `arXiv:2604.19762` (2026), <https://arxiv.org/abs/2604.19762>, and official repository <https://github.com/labyrinthinesecurity/currier-signatures>.
- Edge-glyph coupling and singleton-type rate benchmarks (`p1` evaluation): Elena Rozanova and Alexander Temerev, *"What Counts as a Unit in the Voynich Manuscript? Line Continuity, Token Boundaries, and Sub-Token Structure"*, `arXiv:2608.17096` (2026), <https://arxiv.org/abs/2608.17096>.
- Naibbe cipher comparator: Michael A. Greshko, *"The Naibbe Cipher: A Verbose Homophonic Substitution Cipher that Mimics the Voynich Manuscript"*, *Cryptologia* (2025), <https://doi.org/10.1080/01611194.2025.2566408>.
- Voynich manuscript IVTFF transliterations (`ZL3b-n.txt`, `IT2a-n.txt`, `RF1b-e.txt`): René Zandbergen, Gabriel Landini, and Takeshi Takahashi, <https://www.voynich.nu/transcr.html>.
