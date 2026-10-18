# Selection, run 2026-10-18-0202 (PREREG rule 10; cells C20, C30, C10)

Written 2026-10-18T04:46:29Z (date -u) by the main session (Opus 5.5, claude-opus-5-5[1m]) BEFORE any surprise-test gold was read in this
session (no solutions file opened, no test score computed). Val scores: tools/val_table.py (official compare_words via
tools/q15h.py score-val; P < 0.50 with --gold-root main_only/val_gold). Stage 2: tools/stage2.py (out/stage2_*.log).

## Freeze records (sha256 of each lens's FROZEN.md; tools/check_freezes.py: every hash, rule-8 file and audit ok)
- attempts/analogist/FROZEN.md: c8b4cf2cf8cdfea760c5e8b5225e63597d86b36876f0757a27c110c636e24e63
- attempts/broker/FROZEN.md: d41dd287245ade644c9b101d867da3c0bf7c0bd8e63bb7aaddd050e837d36071
- attempts/classifier/FROZEN.md: df50a06e0f9d9e0b2c01e0f01fda8d4f207b8651439fa80e00fadd558d6935cd
- attempts/correspondence/FROZEN.md: cdb370ddc0d2fbf1d510bfbe6bc068fcfd02d88bc1e8c27508e55fb97178eac6
- attempts/phylo/FROZEN.md: 32b2829e22d9b2eabec2a9e5495995a43ffa58f6156e9a418c65e8ea88e0aaf6
- attempts/transducer/FROZEN.md: 4fb0ee28b20c7ec71524268bccefced87efc3e9964e7c66a4e927d3918bfcd91
- transducer: its FROZEN.md holds a withdrawn SECONDARY record (02:52:42Z, see attempts/transducer/frozen/WITHDRAWN.md); the LAST record per lens and ROLE counts (04:24:24Z), as tools/check_freezes.py applies it, all before 05:45:00Z.

## Eligible new entries (11) and val mean NED
| entry | freeze | val-0.10 | val-0.20 | val-0.30 | val-0.50 |
|---|---|---|---|---|---|
| analogist/PRIMARY | 2026-10-18T02:43:13Z | 0.23167660379365396 | 0.2525175339013857 | 0.25854207036628124 | 0.2885706072901764 |
| broker/PRIMARY | 2026-10-18T03:14:07Z | 0.22875623787952468 | 0.24198975917528148 | 0.2396718067901131 | 0.2780802108388158 |
| phylo/PRIMARY | 2026-10-18T03:19:07Z | 0.23015112156991335 | 0.24974815834059724 | 0.24967751264760174 | 0.2845922609747311 |
| analogist/SECONDARY | 2026-10-18T03:23:18Z | 0.22035923017679387 | 0.24502147837249033 | 0.2505703630644814 | 0.2837348172878465 |
| correspondence/PRIMARY | 2026-10-18T03:40:38Z | 0.2298230059399591 | 0.25571400327616256 | 0.2451909155749041 | 0.2913077560369119 |
| transducer/PRIMARY | 2026-10-18T03:50:45Z | 0.24142850331501214 | 0.2630746061288382 | 0.27020026993603674 | 0.3033229092509786 |
| broker/SECONDARY | 2026-10-18T04:00:49Z | 0.23207995365680192 | 0.24895311839150372 | 0.2522261711928647 | 0.28376005998455833 |
| classifier/PRIMARY | 2026-10-18T04:03:30Z | 0.22761637745145086 | 0.2487108602351726 | 0.2510380609772471 | 0.2896033417663429 |
| correspondence/SECONDARY | 2026-10-18T04:20:28Z | 0.2307884591256007 | 0.2558015925284433 | 0.2457277160978133 | 0.2908258046195304 |
| transducer/SECONDARY | 2026-10-18T04:24:24Z | 0.23401988825758585 | 0.25256959665421724 | 0.2658274113295442 | 0.29843657939584967 |
| classifier/SECONDARY | 2026-10-18T04:36:18Z | 0.23456854928229795 | 0.25727272170389004 | 0.2566178629967308 | 0.2947015906669862 |

Run 2026-10-17-1806's six frozen components (eligible in COMB-ALL10 and at C10 only), val-0.10 mean NED (scored here; val split identical to 1806's, MANIFEST.sha256 byte-identical):
- r1806:brute-scale/SECONDARY: 0.26876937736858214
- r1806:correspondence/PRIMARY: 0.220252540575942
- r1806:feature-transformer/PRIMARY: 0.2691260028611679
- r1806:feature-transformer/SECONDARY: 0.2661710628757787
- r1806:smuggler/PRIMARY: 0.22023538945342006
- r1806:wildcard/PRIMARY: 0.24665570187702437
- r1806:combiner/PRIMARY: 0.21358978758026678 (its leave-one-family-out val value, PREREG rule 10)

## Stage 2 (PREREG rule 9)
COMB-NEW entries (K = 6 lowest val-0.50 mean NED, in that order): broker/PRIMARY, analogist/SECONDARY, broker/SECONDARY, phylo/PRIMARY, analogist/PRIMARY, classifier/PRIMARY
- P 0.10: weights fit on all 10 val families [0, 2, 0, 3, 1, 3]; LOFO val mean NED 0.21766634729481002
- P 0.20: weights fit on all 10 val families [2, 3, 2, 1, 0, 3]; LOFO val mean NED 0.23429616596915276
- P 0.30: weights fit on all 10 val families [2, 2, 0, 3, 0, 3]; LOFO val mean NED 0.23436296736916745
COMB-ALL10 entries (7 lowest val-0.10 mean NED among the 11 new and 1806's six, in that order): r1806:smuggler/PRIMARY, r1806:correspondence/PRIMARY, analogist/SECONDARY, classifier/PRIMARY, broker/PRIMARY, correspondence/PRIMARY, phylo/PRIMARY
- P 0.10: weights fit on all 10 val families [3, 3, 1, 2, 1, 0, 1]; LOFO val mean NED 0.21131035771832854

## Candidates
- C20 (P 0.20): COMB-NEW, val-0.20 0.23429616596915276, below the best single new entry broker/PRIMARY 0.24198975917528148. Components with non-zero weight: broker/PRIMARY (w 2), analogist/SECONDARY (w 3), broker/SECONDARY (w 2), phylo/PRIMARY (w 1), classifier/PRIMARY (w 3)
- C30 (P 0.30): COMB-NEW, val-0.30 0.23436296736916745, below the best single new entry broker/PRIMARY 0.2396718067901131. Components with non-zero weight: broker/PRIMARY (w 2), analogist/SECONDARY (w 2), phylo/PRIMARY (w 3), classifier/PRIMARY (w 3)
- C10 (P 0.10): COMB-ALL10, val-0.10 0.21131035771832854, below COMB-NEW 0.21766634729481002, run 1806's combiner 0.21358978758026678, every new entry (best analogist/SECONDARY 0.22035923017679387) and every 1806 component (best r1806:smuggler/PRIMARY 0.22023538945342006). Not run 1806's combiner or one of its components, so C10 may claim (rule 10). Components with non-zero weight: r1806:smuggler/PRIMARY (w 3), r1806:correspondence/PRIMARY (w 3), analogist/SECONDARY (w 1), classifier/PRIMARY (w 2), broker/PRIMARY (w 1), phylo/PRIMARY (w 1)
No ties at any cell.

## Frozen candidate objects (sha256 of the stage-2 test predictions; nothing changes after this file)
- out/comb_new/test/0.10/bantubvd/result-0.10.tsv: 642b7b63833017b7f99330c6b0fdd44a01824ef8a992e0298876b22b9e4d1166
- out/comb_new/test/0.10/beidazihui/result-0.10.tsv: 72092bb0e78ab22df70d9471902e4bdbe32b6705fd83b4f7d9311ee128f1d6f3
- out/comb_new/test/0.10/birchallchapacuran/result-0.10.tsv: d7f872d1813fdf274652dd7e2e8e2342cc0bc210b0992bd6cdb2d6a3da0e86ef
- out/comb_new/test/0.10/bodtkhobwa/result-0.10.tsv: 53a99de9807dec6d870d56e885e1553a82a248d9790fdd483debb48c8eec86a6
- out/comb_new/test/0.10/bremerberta/result-0.10.tsv: 8b5dec52695a325c60f235bdc8bdc1f2d437b0a410f3fe0dcfca97aeb1a3bfe0
- out/comb_new/test/0.10/deepadungpalaung/result-0.10.tsv: d89caec20a411c6ecd9cebed4aa3973318a4af151911b7f7a3fbcd3a0e19d29c
- out/comb_new/test/0.10/hillburmish/result-0.10.tsv: eb8fd22ceca63c2c3cf9157a57372bed1c2892651c96d743dbc2a77ef84ba5b9
- out/comb_new/test/0.10/kesslersignificance/result-0.10.tsv: 3ae5f5a956258a9e2a831cf3a1d8beb43c1273ee32e396801e36370bbd368921
- out/comb_new/test/0.10/luangthongkumkaren/result-0.10.tsv: 148ce66d9754f453d4bc0fcd0bb0978b44a8ff034fff13784a946622c496aebf
- out/comb_new/test/0.10/wangbai/result-0.10.tsv: b8c37d4e0eb8488e0329b911b52448a8ff46858f08da662423fdfce09179f5ae
- out/comb_new/test/0.20/bantubvd/result-0.20.tsv: 92cdd998f63900a64a1fac55187dfd00a0be551733e0a01002a365a019250a1b
- out/comb_new/test/0.20/beidazihui/result-0.20.tsv: bf9a1eb5106a78088a62fb8e6690aca42f5cc3fadf8d9cb9e78449bcee5aadd9
- out/comb_new/test/0.20/birchallchapacuran/result-0.20.tsv: c1f5c4706bc4cab85bb7ef6d4d5a9b71bc4c1de891e167bf268dcddf435aef05
- out/comb_new/test/0.20/bodtkhobwa/result-0.20.tsv: 3de057c88c63c734436e422ccc470776a02d14286340e61475c83dd2cc6baf13
- out/comb_new/test/0.20/bremerberta/result-0.20.tsv: bab5ff08213fa43f24b2eeb099377a7ea15ae2ff0ba0652a7ccd1edef7b907b8
- out/comb_new/test/0.20/deepadungpalaung/result-0.20.tsv: 17ba785b88ccba0e97df60f513b89841f90f9febc544dcd5cc72d6d497c05d8a
- out/comb_new/test/0.20/hillburmish/result-0.20.tsv: b9384471b5ea2908e2b97b5381ead46f38822fe46946a3f0cabb03e4eb38e4a4
- out/comb_new/test/0.20/kesslersignificance/result-0.20.tsv: eb6b589441c609428fb4b95408832a8c14bd6d6182e751523e14b69943b65ae5
- out/comb_new/test/0.20/luangthongkumkaren/result-0.20.tsv: 65bbe9d6959527a94d002f147eba91662eb8dee79c0ba85bbd989ebc060705f2
- out/comb_new/test/0.20/wangbai/result-0.20.tsv: b6af7a153d557634cc75ac8b8c259574df69d93eb667d47f4acff86b0a3ca51e
- out/comb_new/test/0.30/bantubvd/result-0.30.tsv: b00b20ce373b13548b6c871eaff4f8154537fc057529ef98b1e4e653860f569a
- out/comb_new/test/0.30/beidazihui/result-0.30.tsv: 8443c3f8c27b1c8c42161ba5c58528d2cf408e9f009a0ff847b4006a3a9cab6c
- out/comb_new/test/0.30/birchallchapacuran/result-0.30.tsv: c456dcaea723b2c5d24a0cf3913a151ad1b71e3d6449884a9d5b6a0b38e1c49b
- out/comb_new/test/0.30/bodtkhobwa/result-0.30.tsv: 6342b5b9353d5a841b412eedfa8ce5c03f08de831e487bc26f93958461627ea3
- out/comb_new/test/0.30/bremerberta/result-0.30.tsv: b18214d07c447abc8dba2f14b62f8fb34357d383065a5fc62bc411c797689d4e
- out/comb_new/test/0.30/deepadungpalaung/result-0.30.tsv: ec493adda285411ef26c704b0b7c1ec4732670462eecf341fef96ee023926537
- out/comb_new/test/0.30/hillburmish/result-0.30.tsv: 0c3ffda5170a592620f9484b6a22a4f43a27193b5022db24f4aac9838c891cd4
- out/comb_new/test/0.30/kesslersignificance/result-0.30.tsv: 9936cfb59420c58375f02ca1a4f7e2788aa31ee0ef366a8847003ea6722f9edf
- out/comb_new/test/0.30/luangthongkumkaren/result-0.30.tsv: 6400f69ddaa68ec411de9ca05d9948ca3332435cf3f263bf907b49cda516cba9
- out/comb_new/test/0.30/wangbai/result-0.30.tsv: e13a8b1f2a11664ef5a847e4f1a3acbe6f75d26b846ff556ba0a45b7bd34f330
- out/comb_all10/test/0.10/bantubvd/result-0.10.tsv: cc286787149e9718e2376af74038f20c20ee2bff86cd68ab70844a8dfa1863bb
- out/comb_all10/test/0.10/beidazihui/result-0.10.tsv: 19cf6f6deffd201025ce910040067890be7beaa27c16296269ea0ca7e00a80d3
- out/comb_all10/test/0.10/birchallchapacuran/result-0.10.tsv: ce633686a0454194451afeaf3cdaa5e130153f13548ddceb5628d1b4ae2d849a
- out/comb_all10/test/0.10/bodtkhobwa/result-0.10.tsv: bd93e4512180ca3f88dd39461af49b9bf4cf01750cbbd4c54317f38d3a505a9a
- out/comb_all10/test/0.10/bremerberta/result-0.10.tsv: b14aa14dd0cfbf63c95cb7c4a379324aedfd77f93141844c71c4b7ea2db8bcf0
- out/comb_all10/test/0.10/deepadungpalaung/result-0.10.tsv: 6d72d7590864c6ab27fbc7fe7758b4fb6537069212a40d8c9d7175338c99a393
- out/comb_all10/test/0.10/hillburmish/result-0.10.tsv: 30681015a95f83ddbefc0645314bca5c866a3d5b91f6632425b453c90a816034
- out/comb_all10/test/0.10/kesslersignificance/result-0.10.tsv: 64c1becce9146fb8390f9ba6b67face9e1c790963d1cfce5c82f10688917d32f
- out/comb_all10/test/0.10/luangthongkumkaren/result-0.10.tsv: 974fd1bacfa0c1b53fa726015c32fea5bbccdbb2dfc9f178e93b59e20d90581e
- out/comb_all10/test/0.10/wangbai/result-0.10.tsv: a48f71397b61b10cb72281edda6aa5f0bf6277a3c7091d3148cfefbee820618c
- out/comb_new/combiner_fit.json: 9cc0d8a7adfc1e27d5994a26d1676d54a678f6ddf009f49d68d48a1b108f53ec
- out/comb_all10/combiner_fit.json: c6c55f4b9701ef79b18784c9dd5a94ccdbb01dd8c770f09a89af7108647bea92

Next (PREREG rules 11-13): tools/score_test.py on all eligible entries, COMB-NEW and COMB-ALL10; null tests; sealed checks of the non-zero components at each claimed P (run 1806's smuggler/PRIMARY and correspondence/PRIMARY at 0.10: run 1806's sealed check, resume/out/sealed_check.log, SEALED_COMPARE PASS).
