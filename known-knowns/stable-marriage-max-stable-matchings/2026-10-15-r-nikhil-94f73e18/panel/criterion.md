# CRITERION

context: codex exec (fresh context via codex-fresh)

confirmed_scope: The complete strict preference profile in `object.prefs` for 23 men and 23 women has exactly 19,305,568 stable matchings, exceeding the supplied preceding same-size profile's 19,290,640 by 14,928 and the historical OEIS A357271 n=23 lower bound of 15,481,956.

Verdict: the full inherited success criterion is met at n=23; no partial-win category is used.

The criterion in `CLAIM.md` and `search/PREREG.md` says “for an n,” so it requires one eligible size, not improvements at every listed size. Order 23 belongs to the permitted n >= 17 range and is outside the exclusions. The saved status source `data/oeis.html` supplies lower bounds and does not identify the order-23 maximum as known. The required order-7 calibration is distinct from claiming a win at an excluded size. No enumerated partial wins exist.

Verification performed:

- All 51 entries in `MANIFEST.json` matched their files.
- `python3 verify.py` returned PASS: reconstruction matched the explicit preferences; the complete exhaustive count was 19,305,568 over 35,526,695 search nodes, with every accepted leaf checked for blocking pairs.
- A separate build of `search/smcount3_copy.c` returned 19,305,568 for `object.prefs` and 19,290,640 for `data/prior_n23.prefs`. It also returned 1 and 85 for the saved calibration input and output. This supplies the required cross-check by a different counting method.
- `python3 search/replay.py` returned PASS. The repair search reproduced its saved preference/word pair at proposal 669,716; calibration reproduced its pair at proposal 34,618; the suffix scan reproduced the final construction and preferences, visiting all 93 traversal nodes through depth four with `cutoff: false`.

The comparison does not stop at the weaker public table entry. The count exceeds the stronger saved order-23 predecessor and the earlier local bar of 19,025,864. I also maximized disjoint-block products over all partitions of 23 using the supplied smaller-size public and local bounds, including the calibration value 85: the largest was 195,472 × 85 = 16,615,120 at 16 + 7. That straightforward composition null does not subsume the result. Adaptive selection among candidates does not require a statistical significance test for this existential, exactly counted witness.

The calibration receipts place its start at 16:51:11 UTC, before the historical order-19 start at 16:55:40 and the order-23 start at 17:08:43. These are local historical receipts, not independently authenticated clocks. The input was a previously sampled random profile reused for this trajectory; its sampling RNG is not certified. The evidence supports this calibration trajectory, without establishing performance across independent random starts.

The 93-node scan is exhaustive only within its stated suffix family, and traversal nodes may include commuting duplicates. Neither that scan nor the final matching count establishes a maximum over preference profiles, a general search success rate, or a later worldwide literature record. The pass applies to the inherited historical one-cell criterion and comparisons.

pass: true
