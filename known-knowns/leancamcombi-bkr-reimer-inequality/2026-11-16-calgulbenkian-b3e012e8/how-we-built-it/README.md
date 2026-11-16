# How We Built It

1. Checked live `YaelDillies/LeanCamCombi` `master` (`0a42535119073f677dd60a28acbbdcda11b87f60`), Issue #34, and open PRs (`PREREG.md`).
2. Prototyped and verified the pure-`ℤ` Butterfly vector basis (`vecUR`, `vecUY`, `vecVB`), involution orthogonality, and mod-2 parity descent in Python (`how-we-built-it/`).
3. Formalized `reimer_butterfly_card_le` and the subcube dicing double-count inside a `private` auxiliary section (`section ReimerAuxiliary`) in `object/VanDenBergKesten.lean`, leaving every public import and public declaration in `CamCombi/PlainCombi/VanDenBergKesten.lean` 100% verbatim and building all 6,699 `CamCombi` jobs cleanly.
