# How we built it (cell L30, proportion 0.30, mean BLEU)

Stage-2 entries (the same six frozen systems as the 0.30 mean-NED package 2026-10-18-psmoros-634f2c35; every entry's string is a candidate in the per-item choice):
- broker/PRIMARY (BLEU-MBR weight 2 at 0.30)
- analogist/SECONDARY (BLEU-MBR weight 2 at 0.30)
- broker/SECONDARY (BLEU-MBR weight 1 at 0.30)
- phylo/PRIMARY (BLEU-MBR weight 3 at 0.30)
- analogist/PRIMARY (BLEU-MBR weight 1 at 0.30)
- classifier/PRIMARY (BLEU-MBR weight 3 at 0.30)

- entries/LENS/ROLE/code/: each entry's frozen code; entries/LENS/FROZEN.md: the freeze records.
- tools/q15h.py: the harness (training manifest = the 10 surprise training-0.30.tsv files plus the development families; prediction one masked-language partition at a time). tools/stage2_bleu.py: the BLEU-targeted per-item minimum-Bayes-risk combiner of PREREG.v2.md (weights in combiner/combiner_fit.json, "0.30", "weights_all10": [2, 2, 1, 3, 1, 3]); tools/make_object.py writes object/.
- PREREG.md (frozen 2026-10-18T02:09:41Z: data rules 5-7 and the entries' development protocol), PREREG.v2.md (frozen 2026-10-18T07:19:21Z: this cell, its object and its bar), bleu_freeze.md (the object's sha256, 07:22:11Z, before any test BLEU of it was computed), selection.md (the entry list), null_test.md (400 paired-permutation controls against the earlier object), sealed_check_0.30.log and sealed2_check_0.30.log (every entry retrained in a sandbox and every test partition predicted alone, byte-identical).
- Disclosure: before PREREG.v2.md was written, the test BLEU of these entries and of the earlier object were known; six such objects (BLEU and BCFS at 0.10, 0.20, 0.30) were pre-registered and scored once, and only this one beat its bar.
Paths in these files that began with the workspace folder read WORKDIR.
