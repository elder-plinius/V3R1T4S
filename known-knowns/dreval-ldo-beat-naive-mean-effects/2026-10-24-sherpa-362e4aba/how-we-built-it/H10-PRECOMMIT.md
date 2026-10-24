# H10 pre-commitment — written 2026-10-23T22:32:51Z, before any NCI-60-derived feature is scored

Fixed now so that none of these can be tuned to the outcome:

1. **Source.** NCI DTP public NCI-60 release: `GI50.zip` (sha256 65212008012e0fc4648709f5f081c18e577986a40a8ba45ea271f8c3bb81f728),
   `nsc_smiles.csv` (1e5cb587...), `nsc_sid_cid.csv` (ad07b301...), fetched 2026-10-23T22:31Z.
2. **Teacher target.** Per NSC: mean over cell lines of log10 GI50 (molar), using only rows with
   `CONCENTRATION_UNIT == "M"` and `LOG_HI_CONCENTRATION` equal to the single most common value in the
   file (one standard top dose, so the teacher cannot learn the tested range).
3. **Exclusions, both applied:**
   (a) every NSC whose PubChem CID equals the `pubchem_id` of any of the 545 CTRPv2 drugs;
   (b) every NSC whose Morgan fingerprint has Tanimoto **>= 0.85** to any CTRPv2 compound.
   This removes all CTRPv2 compounds (including every component of every combination) and their
   near-twins, so no held-out drug's own response, in any screen, can reach the model.
4. **Use.** The teacher's prediction for each CTRPv2 drug is computed from that drug's structure only
   and enters the CTRPv2 model as one additional standardized scalar feature, its scale fitted on the
   split's training drugs. Its weight is chosen by the same inner drug-grouped CV as every other
   hyperparameter.
5. **Reporting.** Results reported all drugs / single agents / novel scaffolds, and with and without the
   teacher, whatever the outcome. If the teacher does not help, H10 is recorded as dead.

## Amendment, 2026-10-23T22:34:05Z — before any NCI-60-derived feature was scored

While writing `code/h10_build_teacher.py` a data-quality filter was added that is not in item 2 above:
a compound enters the teacher only if it has **at least 30 cell-line measurements** at the standard top
dose, because a panel mean needs a panel. It removed compounds before any teacher was trained or any
CTRPv2 result scored. Recorded here rather than folded silently into item 2.

## Amendment 2, 2026-10-23T23:02:29Z — after a leak audit, BEFORE any result under the new rule

`code/h10_leak_audit.py` found that the original exclusion rule (PubChem CID match, Tanimoto >= 0.85 on
the raw SMILES) **let 3 CTRPv2 compounds into the teacher** under different identifiers: NSC 373989,
721951 and 757444 share an InChIKey connectivity block, after salt stripping, with CTRPv2 drugs
136227924, 11683005 and 11497983. Counter-ions add fingerprint bits and pushed salt forms below 0.85.
The development result for variant D (all drugs +0.2235) was obtained with these 3 present.

**New primary exclusion rule, fixed now:** remove every NCI-60 compound whose **salt-stripped** largest
fragment either (i) shares the InChIKey first block with any CTRPv2 drug, or (ii) has Morgan Tanimoto
**>= 0.60** to any CTRPv2 compound (474 + any skeleton matches). This is deliberately stricter than the
original 0.85: it removes close analogues as well as identities, so that any gain cannot be analogue
lookup through the back door.

**Sensitivity analyses, all reported whatever they show:** thresholds 0.85, 0.70, 0.50.

If the novel-scaffold gain disappears under the stricter rule, H10 is recorded as an analogue effect,
not chemistry transfer.

## Attribution, added 2026-10-24 after a novelty review found it was only in the contributor narrative

The idea this file operationalises is **not original to this work**. Lavelle, Zhu, Marlor, Brettin and
Stevens, *Large-scale AI-Ready Data for Anti-Cancer Drug Response Modeling*, arXiv:2608.11444 (2026), show
drug-blind response R^2 rising from 0.03 to 0.22 when the training set is expanded by compounds dominated by
NCI-60. Predicting NCI-60 panel-mean potency from structure is a long-established QSAR task
(Cortes-Ciriano et al., 10.1093/bioinformatics/btv529; Martorana et al., 10.3390/ijms232214374).

What is original here is narrow and should be described as such: the **exclusion rule** in items 3 and
amendment 2 (salt-stripped InChIKey skeleton matching plus a Tanimoto cutoff), and reporting the result as a
**monotone curve over that cutoff** rather than at a single threshold. Lavelle et al. excluded held-out
compound identities; they did not exclude close analogues, and did not report sensitivity to doing so.
