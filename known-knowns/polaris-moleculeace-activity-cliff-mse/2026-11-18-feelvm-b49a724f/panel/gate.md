status: PROMISING
confirmed_scope: On the official MoleculeACE CHEMBL244_Ki split (Polaris benchmark moleculeace-chembl244-ki, whose live API split[1] equals the 621 split=='test' rows of data/CHEMBL244_Ki.csv with targetCols ['y']), result/M1_predictions.json achieves sklearn mean_squared_error 0.5501943375378687 on the 296 test molecules with cliff_mol==1, strictly lower than the 0.634573831368627 of the repo-config SVM/ECFP baseline (result/B_predictions.json; C=10, epsilon=0.1, gamma=0.01, rbf, ECFP radius 2 / 1024 bits, retrained from the official train rows and matching the paper's corrected rmse 0.715156602 to ~1e-9), while also being lower on the 325 non-cliff test molecules (0.33343039149183445 vs 0.39931062625682384), with the real result beating all 400 label-shuffle null controls on overall test MSE.

# Honesty gate reasoning (run's main session, 2026-11-18T07:2xZ)

Panel on the M1 (CHEMBL244_Ki) claim:
- REPRODUCE: pass: true (own checker from the definition; baseline re-derived bit-for-bit;
  determinism confirmed; full-precision agreement on every claimed value).
- CRITERION: pass: true (every quantifier judged literally; confirmed_scope above; package
  defects noted but not overturning).
- NOVELTY: pass: false — decisive, verified finding: open V3R1T4S PR #568 (mizopl,
  2026-10-19, same bank target id, identical CSV sha256 and split) ships a 30-target CLSS
  sweep whose CHEMBL244_Ki entry already satisfies p2 (cliff 0.554219 vs the same reproduced
  baseline 0.634574) and BEATS M1 on non-cliff (0.324309 vs 0.333430) and overall (0.433896 vs
  0.436751), while M1's cliff edge is only 0.73% with companion regressions and the prior
  object was not named in the original claim. "Strictly beats everything known" is not met;
  a tie is not a record.

Downgrades applied beyond the panel:
- The 4616 (PREREG.v3) repair attack FAILED both its candidate reads: M1' (RF-heavy greedy
  blend) worse than ITS reproduced baseline on all three metrics (cliff 0.503001 vs 0.479459,
  noncliff 0.356544 vs 0.319622, overall 0.433460 vs 0.403565); the declared repair M2'
  (all-SVR blend, max-min-projected-margin selection) improved noncliff (0.307622 vs
  0.319622) and overall (0.403808 vs 0.403565-equivalent CLSS bar 0.405850) but FAILED the
  cliff subset vs both bars (0.490771 vs baseline 0.479459 and vs CLSS 0.486650). The p2 win
  does not exist on that target; the v3 read budget (baseline + 2 candidates) is exhausted.
- The 238 cell was swept OOF-only and NOT read (projection unfavorable under the same honest
  calibration).
- No CONFIRMED_* status is possible; the claim stays in the run folder; outbox/ was cleared
  of the draft package (moved to claim/packaged_draft_unconfirmed for the record).

Final status: PROMISING (survived reproduce + criterion; novelty fail vs a verified prior
open-PR object; two further cells attacked honestly with all reads declared — both negative).
