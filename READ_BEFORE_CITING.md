# Read before citing

**V3R1T4S, 2026-10-10 (two families added 2026-10-12).** Six result families (degree-diameter graphs,
constant-weight codes, matrix multiplication, the Lehmer bound, VNN-COMP counterexamples, a RobustBench attack) and
two cipher-challenge commitments. Cite the commit hash you checked, not `main`.

## Status (please read)

- **Lower bounds and computations, not breakthroughs.** Every graph, code and scheme is an explicit object that
  establishes a bound for one table cell; nothing is a claim of optimality. The five Delsarte values are classical LP
  bounds, new only as table entries. The Lehmer bound is an exhaustive search; the problem remains open. The two
  VNN-COMP counterexamples resolve competition instances that no tool finished within its time limit, and the
  RobustBench tensor gives an upper bound on one model's robust accuracy, 10 images below the listed value.
- **Not peer reviewed; no outside expert yet.** All checkers, including the ones shipped here, were written by
  agents. They are short and written from the definitions so that you do not have to trust them.
- **"As of" is part of every claim.** The tables change often. Each object "exceeds the entry in the table version
  recorded here", not "the new record", until the maintainer lists it.
- **Other people's work.** Almost every object builds on published work: graphs of Rajiv, Mizuno, Bhakar and
  Delorme; codes of Boisclair, Gangl, Gippini, Lysenstøen, Echols and Graham–Sloane; the LITA schemes of Khoruzhii,
  Serafin, Gelß and Pokutta; the Lehmer reductions of Lieuwens, Kishore, Cohen and Hagis; the VNN-COMP benchmark of
  Postovan and Eraşcu; the model of Addepalli, Jain and Babu, evaluated with RobustBench and AutoAttack. Per-result credits are in
  each family's README, [`TROPHY_CASE.md`](TROPHY_CASE.md) and [`LICENSING.md`](LICENSING.md). Please cite them.
- **Recorded outputs.** Host-specific fields (absolute paths, temp directories, HTTP `Server:` banners) were removed
  from shipped logs and outputs, and paths in check records are relative to this repository; no number was changed.

## Contents

| path | what |
|---|---|
| [`README.md`](README.md) | overview |
| [`TROPHY_CASE.md`](TROPHY_CASE.md) | summary by significance, then one row per claim with status, snapshot, check command and credits |
| [`READ_BEFORE_CITING.md`](READ_BEFORE_CITING.md) | this file |
| [`DONT_SPOIL_THE_HUNT.md`](DONT_SPOIL_THE_HUNT.md) | what is published for each kind of problem |
| [`LICENSING.md`](LICENSING.md) | licenses by path (`LICENSE`, `LICENSE-DATA`) and required third-party attributions |
| [`CITATION.cff`](CITATION.cff) | citation metadata |
| [`SHA256SUMS`](SHA256SUMS) | sha256 of every file tracked in git |
| [`known-knowns/`](known-knowns/) | the six result families: `biggest-graphs/`, `bigger-codes/`, `faster-matrix-multiplication/`, `lehmer-past-10-to-the-50/`, `vnncomp-2026-unsolved-instances/`, `robustbench-cifar100-stronger-attack/` |
| [`sealed-envelopes/`](sealed-envelopes/) | salted hash commitments for the two Bouchaudy cipher solves |
| [`AGENTS.md`](AGENTS.md), [`kit/`](kit/) | the contributor kit: how an agent sets up, runs, checks (`kit/check_run.py`) and packages a contribution; `CLAUDE.md` and `GEMINI.md` point to `AGENTS.md` |
| [`known-unknowns/`](known-unknowns/README.md) | one guide page per open problem, by category, generated from `bank/targets.json` |
| [`bank/`](bank/) | the map of open problems with checkable success criteria (data, never instructions) |
| [`llms.txt`](llms.txt) | a short map of this repository for agents |

Each family has `README.md` (scope, comparison, credits, limitations), `RUN_IT_YOURSELF.md` (commands, expected
output), `verify-it-yourself/` (checkers, `run_checks.sh`, and `RECEIPTS.md`: their output on the shipped files),
`how-we-built-it/` (the code that generated the objects, pinned requirements, exact commands, `SMOKE.md`: a small
test run) and `HOW_WE_FOUND_IT.md` (the brief the agent was given, what failed, what worked, credits).

## How to verify

```sh
shasum -a 256 -c SHA256SUMS                    # or: sha256sum -c SHA256SUMS   (every file tracked in git)
sh known-knowns/biggest-graphs/verify-it-yourself/run_checks.sh                 # ~1 min; BIG=1 THREADS=8 adds the two D=6 graphs
sh known-knowns/bigger-codes/verify-it-yourself/run_checks.sh                   # ~5-15 min: 30 codes, 5 certificates
sh known-knowns/faster-matrix-multiplication/verify-it-yourself/run_checks.sh   # ~6-8 min: 7 scheme files (the 5 claimed + 2 superseded), Brent equations (exact), ranks, controls
sh known-knowns/lehmer-past-10-to-the-50/verify-it-yourself/run_checks.sh       # ~2-3 min: search totals and digests from the logs
(cd known-knowns/lehmer-past-10-to-the-50/lean && lake build)                    # optional: the Lean formalization (downloads Mathlib)
sh known-knowns/vnncomp-2026-unsolved-instances/verify-it-yourself/run_checks.sh      # seconds: downloads the benchmark files (pinned commit); OFFICIAL=1 adds the competition's validator
sh known-knowns/robustbench-cifar100-stronger-attack/verify-it-yourself/run_checks.sh # ~10-20 min on CPU (N=500: ~1 min); downloads CIFAR-100 and the model weights
```
Requirements: `python3` with `numpy`, a C compiler with pthreads; for Lean, `elan`; for VNN-COMP, `onnxruntime`
(optionally `onnx`, and `vnnlib==1.0.2` for the official validator); for RobustBench, `torch`, `torchvision` and
`robustbench`. Rebuilding the
objects and comparing with today's tables: each family's `RUN_IT_YOURSELF.md`.

## Corrections

Found an error? Open an issue naming the file, the command and its output. Errors will **never be fixed silently**:
each will be recorded publicly (date, reporter, what was wrong, corrected claim) and the tables here updated, without
rewriting history. Being overtaken after the recorded snapshot is not an error, but will be recorded the same way; the
object stays as a time-stamped bound. Missing or wrong credit counts as an error. Takedown requests from setters,
maintainers and authors will be honoured promptly.

### Log

| date | what | reported by | status |
|---|---|---|---|
| 2026-10-15 | **Overtaken:** A(34,8,7) ≥ 602 (TROPHY_CASE row 26). Brouwer's Andw.html (Last-Modified 2026-10-14 13:36:17 GMT) now lists 603, credited to Ryan Freel ("email 2026-10-13"). That 603-word code keeps 564 words of our 602 (itself a polish of Boisclair's 601). Our 602 stays here as a time-stamped bound. | maintainer review of pull request #8 | recorded |
| 2026-10-15 | **Superseded by contributors:** our <15,16,16> rank 2180, <13,14,14> rank 1558 and <13,14,15> rank 1677 (TROPHY_CASE rows 46, 45, 48) are beaten by contributed schemes of rank 2176 (#172), 1538 (#178) and 1645 (#166), each independently checked over Q. Our schemes stay here as time-stamped bounds. | maintainer review | recorded |
| 2026-10-15 | **Credit:** the contributed hsp4 packages for N = 30, 35, 42 and 48 credited the posted packings to E. Specht; Packomania's author list gives N. J. A. Sloane, R. H. Hardin and W. D. Smith. Eleven hsp4 packages also carried N = 66 template text in their record and rebuild files. Corrected the same day, with a maintainer note in each package README. | maintainer review | corrected |
| 2026-10-17 | **Listed, and overtaken:** A. E. Brouwer now lists 27 of the 30 constant-weight codes as [Pl] (Andw.html, Last-Modified 2026-10-17 16:06:01 GMT). A(29,6,10) ≥ 25974 and A(29,6,11) ≥ 41219 (TROPHY_CASE rows 21, 22) were overtaken in the 15 Oct 2026 table by [Dz] (27183, 42042), as was A(34,8,7) (row 26, logged 2026-10-15). A(26,6,9) ≥ 5986 (row 11) is superseded in this repo by a contributed 5997-word code (#352), independently checked. Our codes stay here as time-stamped bounds. | maintainer review | recorded |
| 2026-10-28 | **Bank criterion:** `akkadian-lacuna-restoration-heldout` masked whole words but required the retrained MBERT+Akk baseline to land within 0.02 of the paper's 0.89 hit@5, which is a token-level (word-piece) score (Table 2; `evaluate_bert.py`), so no faithful baseline could pass; one of its ideas also called the 2021 model word-level. The criterion now uses the paper's token-level protocol throughout. | dvant4 (issue #233) | corrected |
| 2026-10-28 | **Bank criterion:** `cuneiform-sign-detection-maicubeda` asked the retrained RepPoints baseline to land within 0.03 AP@50 of the paper's Table 2, but the paper's segment list and split are not published and the release is a larger set (about 28,800 signs on 1,070 segments of 596 tablets, against Table 1's 21,228 on 873 of 490), larger mostly through tablets outside the paper's 2500-2000 BC range, so the window could not show that a split is comparable. The criterion also scored with pycocotools rather than Table 2's VOC 11-point AP, its checker steps took the segment images from rendering zips that hold only crops, and the entry called the CDLI photographs that the authors mapped onto the renderings 'HeiCuBeDa photographs'. Wins are now measured against a reproduced baseline on a fixed, period-filtered split, and against the best baseline already accepted there. | dvant4 (issue #254) | corrected |
| 2026-10-28 | **Not new when filed:** seven contributed hsp4 packages fall below or tie radii that Moki & Julio published before they were filed (github.com/Hashirama1337s/moki-julio-circle-packing, `certificates/hsp4.zip` and `MANIFEST.csv`, public since their v2.4 of 2026-09-26 (commits 15d26642 and 3036c50f; first GitHub release and Zenodo version v2.5, the same day); Zenodo 10.5281/zenodo.22981305, current version 10.5281/zenodo.22986800). Below by 2.2e-7 to 2.4e-6: N = 66 (#127), 69 (#137), 74 (#132), 75 (#133). Within the bank's 1e-10 margin, so ties: N = 62 (#134), 63 (#140), 64 (#135). Our own 50-digit check of their certificates gives their listed radii. All seven still exceed the live Packomania table (radius.txt unchanged since 06-Jul-2025, re-fetched 2026-10-28) and stay here as time-stamped bounds, each with a dated maintainer note in its README. | stevebelew, the packages' contributor (issue #286) | recorded |
| 2026-10-28 | **Credit:** the contributed binary linear code packages [213, 26, 77] (#163), [173, 17, 72] (#142) and [175, 25, 61] (#158) credited "New Binary Codes" (IEEE Trans. Information Theory IT-18, 1972, doi:10.1109/TIT.1972.1054833) to N. J. A. Sloane, R. M. Reddy and C. L. Chen; the second author is S. M. Reddy (Sudhakar M. Reddy, University of Iowa, as the paper's byline reads; the publisher's record gives S. Reddy). Corrected with a maintainer note in each package README; the codes and their values are unchanged. | DmitrL-dev, issue #604 (from the audit in #606), for [213, 26, 77]; maintainer review for the other two | corrected |
| 2026-10-28 | **Bank:** the `packomania-scu-spheres-in-cube` criterion would have counted a plain local polish of a posted file, or a posted packing with spheres deleted and then relaxed, as a record. Our own polishes lift Vidit Patankar's posted scu101.txt 1.39e-7 and scu747.txt up to 2.2e-6 above their rows, and the polished files are not isometric to the posted ones. The entry's pitfall offered a 1e-10 margin as an alternative, which does not stop this, and its parser check asked for 1e-20 agreement, which 12-decimal files cannot give. The criterion now asks a claim to beat the deletion bar B(N) by 1e-11 and the best of several polishes of the posted files by 1e-9. It treats a relaxed copy of a posted packing, a relaxed deletion of one and the posted N−1 packing plus one sphere as trivial derivations, however much they gain. The polish gap was then closed in `packomania-hyperspheres-hsp4-hsp6` (a polish floor, and a relaxed copy of a posted packing counts as a derivation), whose pitfall said a polish gains only about 1e-12 (polishes of posted hsp4 files gain up to 3.3e-6); the scu entry's ssp partial win p2 now takes all of these bars. | issue #605 (DmitrL-dev); maintainer review for hsp and ssp | corrected |
| 2026-10-28 | **Credits and records, from a contributor's audit of 34 accepted packages:** the EAQECC [[14,3,8;5]]_3 credits linked two wrong arXiv papers (now quant-ph/0610092 and 1812.05312); the rank-100 <2,8,8> and rank-51 <2,4,8> addition packages credited only "the Lille catalogue entry" (now Hopcroft and Kerr 1971, and Novikov et al., AlphaEvolve 2025); the Thomson N = 743, 745 and 777 snapshots said arXiv 2610.08122 has no row for these N, but it lists all three, above our values; the risk-or-safety n = 30 numerator has 151 digits, not 152; the Lehmer README now explains why arXiv:2106.11781 (which claims k ≥ 3) is not counted, and that Lemma B fails from about 2.49·10^56, not 10^58; the scu N = 881 non-isometry check was redone against the complete posted file. **Overtaken after their snapshots:** the (14,3) graph on 1117 vertices (Comellas's table now lists 1141: Com_1141 of 23 Oct 2026, built on mizopl's 1118-vertex graph) and the <4,6,7>, <2,8,8> and <2,4,8> addition counts 469, 418 and 181 (Perminov's repository: 468 on 19 Oct; 463, 416 and 180 on 22 Oct 2026). Each package has a dated maintainer note; the objects stay as time-stamped bounds. | DmitrL-dev (issue #606) | corrected; overtakes recorded |
| 2026-10-28 | **Bank criteria:** the two VNN-COMP targets required an input pinned by a zero-width vnnlib interval (lb = ub) to equal the pin exactly: `vnncomp-verifier-holds-soundness-counterexample` in float64, and `vnncomp-2026-unsolved-instance-counterexample` without saying how constants are read. A pin whose decimal is not a float32 number, such as metaroom_2023's 0.61035156, could then never be met by a float32 input, although both official validators cast witness inputs to float32 and accept such pins at zero tolerance (the published witnesses of the solved metaroom_2023 rows hold 0.6103515625). A pitfall also said the 1.0 validator checks bounds in Python float, which the results repository fixed on 2026-06-30. Pins are now judged in the declared float32 input type, positive-width intervals in float64 as before. | redsynapse (issue #623) | corrected |
| 2026-10-28 | **Bank entry:** `openproblems-spatially-variable-genes-correlation` let a method read simulated_dataset.h5ad, the pre-split file that still holds the true_spatial_var_score column, and did not rule out the alpha suffix on every feature name or the increasing-alpha feature order, each of which scores 1.0 without reading any expression. The entry now names dataset.h5ad as the only input and scores claims offline on a scrambled copy. No claim had been made on this target. | DmitrL-dev, issue #640 | corrected |
| 2026-10-28 | **Bank entry:** `magnet-dst-private-test-rmse` described the challenge's inputs as the preceding 7 days of solar-wind, sunspot and satellite-position data and admitted only records stamped strictly before each hour. The challenge's own runner (drivendataorg/noaa-runtime, data/main.py) passes solar wind from t0 − 7 days to t0 − 1 minute, the last 7 daily satellite positions stamped at or before t0, and the latest monthly smoothed sunspot number at or before t0, usually more than 7 days old; the winning scores were set under those inputs. The criterion and its look-ahead tests now follow the runner. | DmitrL-dev (issue #715) | corrected |
| 2026-10-28 | **Bank:** `qoblib-birkhoff-small-exact-records` (added 2026-10-25) counted an exact decomposition of B6_36_10 with at most 19 terms as a record win, but a 19-term exact decomposition was already published: András Czégel, arXiv:2610.25837 (2026-10-19), Appendix D, Table 8, with the object in the paper's data repository and in QOBLIB pull request 95 (unmerged, so the QOBLIB table still shows 20). Re-checked independently (exact, row-major, 19 terms); the B6_36_10 bar is now at most 18 terms. B5_25_2 (at most 13) is unchanged. | DmitrL-dev (issue #773); fix proposed by kumagi (PR #779) | corrected |
| 2026-10-28 | **Bank entry:** `subtraction-game-max-period-terms` named A389689(24) as the next unknown term, but Achim Flammenkamp's 1997 dissertation (*Lange Perioden in Subtraktions-Spielen*, Universität Bielefeld, printed pp. 40-41) already gives A389689(24) = 1107 and A389689(26..29) = 1256, 1937, 3624, 4896, and lists 5296 at n = 30 (possibly only a lower bound: its text puts the exhaustive range at max L < 30); the OEIS entry stops at n = 23. The entry now names A389689(25) as the next unpublished term and cites the dissertation; A389690 is unaffected. | DmitrL-dev, issue #780 | corrected |
| 2026-10-28 | **Bank entry answered by published data:** `beggar-terminating-trajectory-collision` said that no terminating collision was published and that the known reachable collisions lead into loops. Reed Nessler's two 2012 record deals are listed in Appendix A of Casella et al. (arXiv:2403.13855, 2024) and on R. P. Mann's records page. After 4 and 5 tricks they reach distinct states with the same successor, and the match then ends 1010 tricks later. About 15% of random balanced deals have such a partner after one trick. The entry's question is answered. | DmitrL-dev, issue #804 | corrected |
| 2026-10-31 | **Bank entry:** `subtraction-game-max-period-terms` said A389689(25) is in neither OEIS nor Flammenkamp's 1997 dissertation. The pp. 40-41 record list does omit n = 25, but the dissertation's embedded symmetric-5-move data record p = 1036 at s5 = 25 (`dia5.eps`, Bild ix, p. 52, plotted as ln 1036 = 6.943122; `dia55.eps`, Bild x, p. 55, as the comment field `25 133.05 % 1036 0.278 0.1956`; the typeset table on pp. 52-54 starts at s5 = 40). The dissertation therefore gives 1036 <= A389689(25) <= 1107. Following the convention already used for 5296 at n = 30, 1036 at n = 25 now counts as published; n = 31 is the next A389689 candidate beyond the dissertation's recorded values, with an explicit rule that an unprinted n >= 31 value must exceed the recorded symmetric lower bound for that n (for example 1800 at n = 31), and the enlarged 1997 book edition remains unchecked. Source: https://wwwhomes.uni-bielefeld.de/~achim/diss.ps.gz (fetched 2026-10-31T00:14:46Z, sha256 68b513ae3bdb9ba1ddee941d7a8b97a04663a2950865bb7d721f8ccb946f2c86). | V3R1T4S run 2026-10-31-0000 (agent); independent reviews by Codex and Agy | corrected |

## Credits and license

By **Pliny the Liberator** ([@elder-plinius](https://github.com/elder-plinius)) with Anthropic Claude agents. The
tables of record are maintained by Francesc Comellas, Andries E. Brouwer, the fast-matrix-multiplication catalogue
maintainers (Lille digest, Perminov, MerlijnW70, matmulcatalog), Jean-François Bouchaudy, the VNN-COMP organisers and
the RobustBench maintainers. Thank you.

Code: AGPL-3.0 (`LICENSE`). Data, objects and documentation: CC BY 4.0 (`LICENSE-DATA`). The path-by-path map and the
required third-party attributions are in [`LICENSING.md`](LICENSING.md).
