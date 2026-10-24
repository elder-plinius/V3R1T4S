# site-percolation-2-uniform-lattices-thresholds, partial win p2: bond threshold of row #22, (2/3)(3^3,4^2) + (1/3)(4^4)

## What

Confirmed scope (panel/gate.md, status CONFIRMED_PARTIAL, partial win p2), quoted word for word:

> For the bond threshold of row #22 of the 2-uniform table in Wikipedia's "Percolation threshold" article (lattice (2/3)(3^3,4^2) + (1/3)(4^4), built as the row tiling TSS), the claim's extrapolation of eigenvalue-form critical-polynomial roots on W x infinity cylinders (W = 2..10, reproduced here for W = 5..10) gives an independent estimate p_c = 0.445287065(21) whose one-sigma bar is a convergence-and-calibration estimate rather than a rigorous bound (23 alternative extrapolations all lie within 3.4e-8 of it), and this lies 9.6e-7 above the table's "citation needed" value 0.44528611(40), a discrepancy 2.4 times that value's stated error bar but within 3 combined sigma.

"Reproduced here" in that sentence refers to the panel: the CRITERION skeptic reran W = 5..10 and the REPRODUCE
skeptic W = 2..10 of the claim's programs (panel/). This package's own checker recomputes W = 2..6 independently.

The object: object/p2_value.json (the value 0.445287065459697, sigma 2.093e-08 by PREREG.v2, rule-4 sigma 7.293e-09,
and the root sequence p(W), W = 2..10; sha256 51d575bafaa6558f1f65bd6cd46f1fd2bc113e4717d93994d9bbbdeccec68c23) and
object/TSS_bond_roots.tsv (the same roots as computed, with run time and state-space sizes per W). NUMERICAL.

## Check it yourself

From this folder, with only Python 3 (standard library):

    sh verify-it-yourself/run_checks.sh

Expected last line: `PASS`. Rough time: about a minute or less on a laptop (47.65 s wall clock, 7.07 s of CPU, on
the shared build machine under heavy load; see the receipts). It rebuilds the TSS tiling and counts its vertex
configurations, self-tests its own transfer matrix on the exactly solved square (1/2) and triangular (2 sin(pi/18))
bond cases, recomputes p(W) for W = 2..6 and compares them with object/TSS_bond_roots.tsv (tolerance 1e-12),
recomputes the claim's elongated-triangular calibration roots for W = 2..4, checks the JSON against the tsv,
recomputes the PREREG rule-4 extrapolation and the PREREG.v2 error bar, and prints the comparison with the table.
It also checks the object files against SHA256SUMS. Real output: verify-it-yourself/RECEIPTS.md.
`python3 -I -B verify-it-yourself/check_p2.py --wmax 7` adds W = 7. W = 8..10 are not recomputed by this pure-Python
checker; the REPRODUCE skeptic reran the claim's two programs for W = 2..10 (panel/reproduce.md).

## Compared to

| table | cell | table value | this value | difference | URL | fetched (UTC) |
|---|---|---|---|---|---|---|
| Wikipedia, "Percolation threshold", section "2-uniform lattices" | row #22, (2/3)(3^3,4^2) + (1/3)(4^4), bond column, marked "citation needed" | 0.44528611(40) | 0.445287065(21) | +9.5546e-7 = 2.385 combined sigma = 2.389 times the table's stated 4.0e-7 | https://en.wikipedia.org/wiki/Percolation_threshold | 2026-10-16T07:52:05Z (HTTP 200, sha256 2f44ce4065839fa2baf1c1655cdcf5aa40e21fcdb7cdabf69287093e0fd27e95) |

The table's bond value traces to unpublished work (Hang Gu and R. M. Ziff, "to be published", 2007, per the page
history; see the-record-we-beat/README.md). The panel found no published bond value for this lattice.

## Not claimed

- No record claim. The bank's own pitfall for this target applies: some "citation needed" bond values may come from
  unpublished critical-polynomial runs, and a discrepancy with them is reportable but not by itself a record. This
  package is an independent determination of that cell, nothing more.
- The error bar is convergence-based, not a rigorous bound: PREREG rule 4 (window shift and a second accelerator),
  widened by PREREG.v2 (written after the results existed; it only widens). The CRITERION skeptic judged the central
  value probably about 1e-8 high, still inside the bar.
- Agreement, stated plainly (wording revised after review, 2026-10-17): this value agrees with the table's to 6 digits
  (0.445287) and differs from 0.44528611(40) by +9.55e-7, which is 2.4 times the table's stated error bar (2.385
  combined sigma). It does not confirm the table value. The frozen PREREG's rule 9 names any difference within 3
  combined sigma "confirms", and the checker still prints that rule name, but the label is not a claim that the table
  value is right.
- Width 11 (added after review, 2026-10-17): our own transfer-matrix root at W = 11 is p(11) = 0.44528707914717824
  (run 2026-10-16-0731, extender lens; how-we-built-it/data/TSS_bond_W11_analysis.txt). With W = 2..11 the rule-4
  estimate E1 moves from 0.445287065 to 0.445287060 (-5.5e-9, inside the stated bar), and the downward drift has not
  stopped. The 7th rounded digit is therefore borderline: both values round to 0.4452871, but an estimate below
  0.44528705 would round to 0.4452870. "7 digits" is read as a stated sigma of at most 5e-8 (frozen PREREG rule 9).
- No site threshold. The row's site value 0.5648(2) and the bank's full win (site thresholds) are not addressed here.
- One cell only. how-we-built-it/data also holds roots for other lattices (the elongated triangular and kagome
  calibrations, and rows TSSS, TTS, TTTS); none of them is claimed here.
- Nothing was submitted to or edited on Wikipedia. After this package was built, the human emailed R. M. Ziff
  (2026-10-16), whose unpublished 2007 value with H. Gu the table row cites, describing this independent value; there
  has been no reply, and nobody else was contacted.

## Credits

- Jesper L. Jacobsen and Christian R. Scullard: the critical-polynomial method, its transfer-matrix and eigenvalue
  forms (Lambda_open = Lambda_closed, Jacobsen 2015, eq. 13), and the published test values used for calibration
  (elongated triangular "frieze" bond 0.41964035886369(2), kagome bond roots of Table II):
  https://arxiv.org/abs/1209.1451, https://arxiv.org/abs/1401.7847, https://arxiv.org/abs/1507.03027,
  https://arxiv.org/abs/1910.12376.
- M. E. J. Newman and R. M. Ziff: the Monte Carlo algorithm and the displacement-vector wrapping test (used for the
  table's site values and in the run's Monte Carlo work; not used for this bond value),
  https://arxiv.org/abs/cond-mat/0005264, https://arxiv.org/abs/cond-mat/0101295.
- R. Neher, K. Mecke and H. Wagner: the table's 2-uniform site values and lattice list,
  https://arxiv.org/abs/0708.3250, https://arxiv.org/abs/0708.3251.
- The table's bond value for this row: unpublished work credited on Wikipedia to Hang Gu and R. M. Ziff
  ("Percolation thresholds of 2-uniform lattice", to be published, 2007; per the page history).
- Wikipedia's "Percolation threshold" editors, https://en.wikipedia.org/wiki/Percolation_threshold (history:
  https://en.wikipedia.org/w/index.php?title=Percolation_threshold&action=history).
- Submission credit: psmoros. Built and reviewed with the V3R1T4S protocol, https://github.com/elder-plinius/V3R1T4S;
  panel: REPRODUCE (fable), NOVELTY and CRITERION (opus) subagents, each seeing only the claim.
