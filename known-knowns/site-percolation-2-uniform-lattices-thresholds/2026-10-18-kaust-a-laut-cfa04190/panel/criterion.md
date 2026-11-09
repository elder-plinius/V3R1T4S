context: subagent (fresh Claude Code Agent-tool context, general-purpose)

# CRITERION skeptic: lattice #23 site threshold

I read only claim/. What I ran myself, inside my copy:
- the MANIFEST.sha256 check: 2013 of 2013 files match
- evaluator-first/code/test_lattices.py: PASS, and #23 = SSST, fractions 1/2 and 1/2, zbar 9/2, 2 orbits
- tmcrit.c, built and run through exact-polynomial/code/regress.py: REGRESSION: PASS, worst difference 5e-16
- #23 site roots recomputed for n = 1..9 and bond roots for n = 1..7: identical to the saved series to all printed digits
- exact-polynomial/code/extrapolate.py on both #23 series, and calib_rule.py on the square-site and (3^3,4^2)-bond series
- timeline-aligner/code/agreement.py for #23 site and #23 bond, fss_mc.py for kagome, and analyze_mc.py on the 2048 x 512 torus
- block 0 of the #23 site L1 = 64, L2 = 16 dataset (seed 23016) regenerated with nzwrap2: byte-identical to the saved .hist
- a split of the #23 site Monte Carlo into blocks 0-19 and blocks 20-59, with the PREREG.md one-term fit on each part

Every number below is one I reproduced, unless I say otherwise.

## Uncertainty bound (one sigma at most 2e-6)

- The claimed sigma is sigma_TM = 1.04e-7. That is 24 estimates (K = 1..4, j = 0..2, both readings of the window), the median taken, and the largest deviation from it used as sigma. I reproduced p_TM = 0.57176453954634.
- Is that sigma honest? The same frozen rule was run on Jacobsen's square-site sequence cut at n_max = 10..21. At every cut the true error was 0.00 to 0.02 sigma_TM, so the bar is conservative there.
  - On the (3^3,4^2) bond series it covers the truth for n_max >= 7: 0.04 to 0.61 sigma.
  - It fails only at n_max = 6, where it is off by 9.7 sigma.
  - #23 site uses n_max = 16. Its local exponent is 4.08, the same regime as the square-site calibration.
- Within the family the estimates drift down as K grows: K = 1 gives about 0.5717646, K = 4 about 0.5717645 (0.57176450 to 0.57176451). All of them lie inside the bar.
- The Monte Carlo value has its own sigma of 1.393e-6, which also meets 2e-6. So the bound holds even if sigma_TM were too small by an order of magnitude. Met.

## (a) Two independent methods agree within three combined sigma

- Method A (transfer matrix): 0.5717645395 +- 1.04e-7. Method B (Monte Carlo): 0.571766679 +- 1.393e-6.
  - |difference| = 2.139e-6, against 3 combined sigma = 4.191e-6, so 1.53 combined sigma. AGREE.
  - Stability fit (L2 >= 24): 0.57176786 +- 1.74e-6. It differs from the primary fit by 1.18e-6, under one sigma_MC, so STABLE.
- Independence:
  - The two methods use different algorithms and different code: tmcrit.c, a cylinder eigenvalue root, against nzwrap.c, a Newman-Ziff torus wrapping crossing.
  - They share one input, the lattice built by lattices.py, which both sweep.py and mc_worker.py import. A wrong lattice would therefore fool both methods together. The identity test guards against that: test_lattices.py checks vertex types, fractions, zbar and orbits, and rejects the near misses SST and SSTT.
  - I judge the methods independent in the sense the criterion intends.
- The example (Newman-Ziff tori "up to L >= 2048", Jacobsen-Scullard roots "for growing bases"):
  - It is introduced by "for example", so I read it as illustrative, not binding.
  - Method A is Jacobsen's n x infinity eigenvalue form of the critical-polynomial root (arXiv:1507.03027 eq. 13), with the base growing to n = 16.
  - The Monte Carlo fit uses tori up to L1 = 512 (L2 = 128). The only L1 >= 2048 torus is a low-statistics check: 2048 x 512, 20 blocks of 200 samples. It gives p_L = 0.571764522 +- 2.27e-5, which is consistent with p_MC (2.2e-6 apart against a 3-sigma limit of 6.8e-5), but it is not in the fit.
  - So the claim does not meet the example literally at the 2e-6 level. It needs no stretching, though, as long as the example is read as non-binding. Panel note: a reader who treats "L >= 2048" as binding would fail (a).
- Null check on the sequence of looks: rules/PREREG.v2.md discloses an interim look at 20 blocks. There the Monte Carlo was 0.571771431(2262), 3.04 combined sigma above the transfer matrix. The extension to 60 blocks was then fixed in advance, and it was needed anyway because sigma_MC = 2.26e-6 > 2e-6.
  - I fit the 40 blocks added after the interim (blocks 20-59) on their own: 0.5717643(18), which is -0.12 sigma from p_TM.
  - The data that had not been seen therefore agree with the transfer matrix independently. The agreement is not a product of choosing when to stop.
  - The two halves differ from each other by about 2.5 sigma. That is worth noting but is not disqualifying.

## (b) Within 3 sigma of the table value, or the discrepancy explained

- Table value 0.5720(2). |p_TM - table| = 2.355e-4. The frozen rule's limit is 3 sqrt(sigma_TM^2 + (2e-4)^2) = 6.0e-4, so WITHIN.
- That is 1.18 of the table's own sigma.
- Measured against our sigma alone it would be thousands of sigma. The natural reading of "within 3 sigma of the table value" uses the table's stated error, and the frozen PREREG.md rule says so explicitly. Met.

## (c) Reproductions by the same code

**First half: the BOND threshold of #23 to at least 6 digits.** The frozen standard is |ours - published| < 1e-6 with our sigma <= 1e-7.
- Transfer matrix (the code that produces the claimed value), n_max = 13: 0.45844602208 +- 3.75e-8.
  - Against the table's 0.45844622(40), |diff| = 1.98e-7. Both round to 0.458446. Met.
  - The local exponent at n = 13 is 3.61, so the series has not fully settled. Even a bar several times larger would still leave |diff| < 1e-6.
- Monte Carlo bond: 0.458445217 +- 1.553e-6. It is 1.0e-6 from the table (0.65 sigma) and 8.1e-7 from the transfer-matrix bond value.
- Caveat on the word "published": in table/table_record.md the table's bond value carries {{citation needed|date=June 2019}}, and no paper is named. I count it as the lattice's published bond threshold because:
  - it is the only bond value on public record for this lattice in the table the bank names;
  - the bank itself, in p2, treats such entries as the reference values to check.
  If "published" is read as "in a citable paper", (c) is not demonstrated, and the panel should weigh that. As a test of the code, the match to 0.5 of the table's error on an 8-digit value is strong whatever the value's provenance.

**Second half: the kagome or (3,12^2) site threshold to at least 6 digits.**
- The transfer matrix gives kagome site 0.6527036446661393 and (3,12^2) site 0.8079007641202843. Both are exact to 1e-16 for n = 1..4 (I re-ran this).
  - For these lattices the root is the same at every n. The check therefore tests the code, not the extrapolation, but the literal requirement is met.
- Monte Carlo kagome site: 0.652704208 +- 9.89e-7 against exact 0.6527036447. That is +5.6e-7 and 0.57 sigma, so the Monte Carlo also meets 6 digits.
- The other Monte Carlo calibrations pass too:
  - square site, -0.76 sigma;
  - common offset, D = +4.2e-7 +- 6.5e-7, PASS;
  - the triangular test, PASS (outputs/triangular_test_output.txt);
  - (3^3,4^2) site: the transfer matrix and the Monte Carlo agree within 2.6e-7, and both are consistent with 0.550213(3).

## (d) No published site value for #23 with uncertainty below 2e-6

- I did not fetch anything. I relied on table/literature_record.md:
  - an arXiv API query, 40 entries, sha256 given;
  - two web searches, run 2026-10-17 23:58Z to about 00:02Z;
  - the table citing only Neher, Mecke and Wagner 2008, with 0.5720(2).
- The search is narrow: one arXiv abstract query and two web queries. Nothing in claim/ contradicts it. Confirming it is for the NOVELTY skeptic.

## "Re-fetched immediately before claiming"

- table/table_record.md records a fetch at 2026-10-17T23:58:22Z: HTTP 200, with the sha256 of the HTML and the wikitext. That is about 4.5 minutes before the one look at 00:02:53Z, and the claim follows it.
- The wikitext is recorded as identical to three earlier fetches. Row 23 is quoted as the raw wikitext line.
- The saved HTML and wikitext are not in claim/, so I could not check the hashes. I relied on the record. Met, as recorded.

## Rules frozen before the data, and the single look

- PREREG.md was frozen at 2026-10-16T05:22:16Z, before any measurement on a two-uniform lattice. It fixes the statistic, both methods, the extrapolation rule, the fit and rules (a)-(d).
- v2 to v6 only add a stopping rule, calibrations, evaluators and the n_max rule, and each states that it changes no threshold.
- PREREG.v6 had one edit 39 s after its freeze, and that edit made rule (c) stricter.
- Each freeze is ordered relative to the data it judges: v5 came before the n = 16 root existed, and v2 before blocks 20-59. The timestamps are self-reported, and I cannot verify them from file times in a copy.
- outputs/one_look_output.txt is one run, 00:02:53Z to 00:04:16Z, of outputs/one_look.sh, which calls the same scripts as REPRODUCE.md. I reproduced its #23 site, #23 bond and kagome numbers exactly.
- The data are real outputs of the frozen code: the 64 x 16 site block 0 regenerated byte-identical, and the small-n transfer-matrix roots recompute identically.
- The one earlier evaluation of rule (a), at 20 blocks, is disclosed and was non-decisive under a requirement stated beforehand. See (a).

## Partial wins

- The claim targets the full criterion, not p1 or p2.
- For the record, #23 bond would not meet p2 under the frozen rule: PREREG.md asks for p_bond,TM sigma <= 1e-8, and the result has 3.75e-8.

## Verdict

- The full criterion is met for lattice #23 under these readings:
  - the "for example" clause is illustrative;
  - "within 3 sigma of the table value" uses the table's stated error;
  - the "published BOND threshold" is the table's citation-needed bond value 0.45844622(40).
- The last reading is the weakest point, and the panel should note it.
- The uncertainty is honest by calibration, and the Monte Carlo blocks not seen at the interim look agree with the transfer matrix on their own (-0.12 sigma).

confirmed_scope: For 2-uniform lattice #23, (1/2)(3^3,4^2)+(1/2)(4^4), the site percolation threshold is 0.57176454 +- 0.00000010 by the frozen transfer-matrix extrapolation (n <= 16), and it agrees within 1.53 combined sigma with an independent Monte Carlo wrapping-probability value of 0.5717667 +- 0.0000014 on tori up to 512 x 128 cells, while the same transfer-matrix code reproduces the table's citation-needed #23 bond value 0.45844622(40) to 2e-7 and the exact kagome and (3,12^2) site thresholds, the value lies 1.2 table sigma from the table's 0.5720(2), and the recorded literature search found no published #23 site value more precise than 2e-4.

pass: true
