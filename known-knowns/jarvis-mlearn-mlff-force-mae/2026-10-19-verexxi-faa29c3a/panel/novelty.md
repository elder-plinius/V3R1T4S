# panel/novelty.md

context: subagent (same VM)

## Scope
I read only files under `panel-claim/Mo`: `CLAIM.md` and `the-record-we-beat/snapshot.md`. I changed nothing in the folder.

## Live table fetch
- URL: https://pages.nist.gov/jarvis_leaderboard/AI/MLFF/mlearn_Mo_forces/
- Method: one plain curl with User-Agent "V3R1T4S-skeptic (plain fetch)", no retries.
- Fetched at 2026-10-19T22:54:48Z. HTTP 200, 165096 bytes, no challenge or block.
- The table lists 7 entries for mlearn_Mo (multi-MAE of forces), best first:
  - snap_mlearn 0.18434104563832232 (01-14-2023)
  - alignnff_mlearn_all_wt1 0.185323534449972
  - matgl_pretrained 0.3181
  - m3gnet_pretrained 0.3452
  - chgnet_pretrained 0.3648 (08-07-2023)
  - alignnff_mlearn_wt1 0.8090
  - alignnff_pretrained_wt10 0.9524
- This matches the claim's snapshot (`the-record-we-beat/snapshot.md`, fetched 22:52:53Z) exactly.
- Best listed is 0.18434. The claimed 0.097400 is lower by (0.18434 - 0.0974) / 0.18434 = 47.2%, which is well over the 5% requirement.

## TROPHY_CASE.md
- Fetched once from https://raw.githubusercontent.com/elder-plinius/V3R1T4S/main/TROPHY_CASE.md. HTTP 200, 31235 bytes.
- It lists six result families (degree-diameter graphs, constant-weight codes, matrix multiplication, Lehmer bound, VNN-COMP, RobustBench) plus two cipher commitments.
- A grep for mlearn, jarvis, force and Mo found no entry for this task. No prior claim on it.

## Open pull requests
- Fetched once from https://github.com/elder-plinius/V3R1T4S/pulls. HTTP 200, first page only (26 titles parsed from the embedded JSON).
- The titles cover immrep22, polaris-moleculeace, constant-weight-codes, sorting-network-size-records and snake-coil-in-the-box.
- None mention mlearn, JARVIS, forces or MAE. Later pages were not fetched (one request per instructions), so an unseen PR is not strictly ruled out.

## Literature search
I ran 5 web searches and one fetch.
- Searches covered mlearn Mo force MAE for 2025-2026, ALIGNN 2.0 (arXiv 2609.19487), Zuo et al. 2020 with Mo force MAE, and MACE/NequIP/Allegro/ACE on the mlearn Zuo split.
- The fetch was AtomProNet (arXiv 2501.14039); it returned unreadable binary PDF content, so I could extract nothing from it.
- ALIGNN 2.0 (arXiv 2609.19487): the search result summary gives mlearn-Mo force MAE 0.1121 eV/A, from 0.0179 for Cu to 0.1121 for Mo. CLAIM.md marks it as pending verification in that paper. The claimed 0.0974 is lower than 0.1121.
- Zuo et al. 2020 (J. Phys. Chem. A 124, 731): the abstract says Mo forces are "significantly higher" than for Cu, Ni and Li. I could not extract Mo force numbers, which are only in a figure. Its split is its own, not the leaderboard's official test ids, so it is not a same-split comparison.
- I found no paper reporting a lower Mo force MAE on the leaderboard's mlearn test split than 0.0974. The other hits (MLIP Arena, LAMBench, CHIPS-FF, MLIPAudit, NeurIPS 2023 MLFF benchmark) did not show Mo force MAEs on this split.

## Judgment
- The claim strictly beats the live table best (0.18434), by 47.2%. It also beats the only literature value found on the same train/test sizes (ALIGNN 2.0, 0.1121).
- The caveats are the unquantified Zuo Mo figure on a different split, the unverified ALIGNN 2.0 number, and the unchecked later PR pages. None of these is a known lower value on the same split.

pass: true
