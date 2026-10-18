# selection.md (PREREG rule 10), run 2026-10-18-0839, cells N50 / B50 / L50 (proportion 0.50)

Written by the main session at 2026-10-18T11:25:56Z (date -u), before any surprise-test gold of this session was read or any test output scored.
Every lens had returned (last at 2026-10-18T11:20:47Z); no lens was started after them, so no entry can be frozen before the 12:40:00Z deadline beyond those below.

## Eligible entries (tools/check_freezes.py --carried; out/frozen_entries.md)
21 eligible entries: 10 new (this run's six lenses), 11 carried (run 2026-10-18-0202, code re-verified against the 0202 freeze hashes, test-0.50 runs and audits by the main session in carry/). Every entry: code and result tree hashes recomputed and equal to its freeze record, val/0.50 and test/0.50 for 10 families, test-mode audit at 0.50 AUDIT PASS.

## Stage 2 (PREREG rule 9; tools/stage2.py, out/stage2_comb6.log, out/stage2_comb8.log)
- out/stage2_comb6.log:stage2: K=6 entries ['broker/PRIMARY', 'classifier/SECONDARY', 'broker/SECONDARY', 'r0202-broker/PRIMARY', 'classifier/PRIMARY', 'analogist/PRIMARY']; 4095 weight tuples; out WORKDIR/runs/2026-10-18-0839/out/comb6
- out/stage2_comb6.log:0.50 weights(all 10) [2, 2, 1, 0, 2, 1] in-sample 0.261830 LOFO 0.267432
- out/stage2_comb8.log:stage2: K=8 entries ['broker/PRIMARY', 'classifier/SECONDARY', 'broker/SECONDARY', 'r0202-broker/PRIMARY', 'classifier/PRIMARY', 'analogist/PRIMARY', 'phylo/PRIMARY', 'r0202-analogist/SECONDARY']; 65535 weight tuples; out WORKDIR/runs/2026-10-18-0839/out/comb8
- out/stage2_comb8.log:0.50 weights(all 10) [1, 2, 3, 2, 2, 1, 0, 2] in-sample 0.259198 LOFO 0.262507

## Rule 10 ranking (singles: frozen val-0.50 files; combinations: LOFO val files; official compare_words)

| order | candidate | kind | val NED | val ED | val BCFS | val BLEU | stage2 cross-check |
|---|---|---|---|---|---|---|---|
| 1 | COMB-8 | combination | 0.26250736260023105 | 1.085555251937082 | 0.842856 | 0.624176 | equal |
| 2 | COMB-6 | combination | 0.267432012235394 | 1.1169616443545596 | 0.839753 | 0.617030 | equal |
| 3 | broker/PRIMARY | single | 0.27104726508767685 | 1.117791906917987 | 0.838784 | 0.613038 | - |
| 4 | classifier/SECONDARY | single | 0.2725097701028512 | 1.128038409920328 | 0.827111 | 0.610258 | - |
| 5 | broker/SECONDARY | single | 0.2758653182632716 | 1.1334852460916984 | 0.836111 | 0.606632 | - |
| 6 | r0202-broker/PRIMARY | single | 0.2780802108388158 | 1.1477916922461475 | 0.834398 | 0.604617 | - |
| 7 | classifier/PRIMARY | single | 0.27837673041473154 | 1.161272579828635 | 0.829200 | 0.600519 | - |
| 8 | analogist/PRIMARY | single | 0.28029406101885673 | 1.1650546666433073 | 0.834868 | 0.597583 | - |
| 9 | phylo/PRIMARY | single | 0.28276039319290625 | 1.1611120467101628 | 0.826779 | 0.597321 | - |
| 10 | r0202-analogist/SECONDARY | single | 0.2837348172878465 | 1.175079234323396 | 0.830884 | 0.594652 | - |
| 11 | r0202-broker/SECONDARY | single | 0.28376005998455833 | 1.170875140721858 | 0.830790 | 0.598693 | - |
| 12 | phylo/SECONDARY | single | 0.2839042876857526 | 1.169513641152215 | 0.828204 | 0.594517 | - |
| 13 | r0202-phylo/PRIMARY | single | 0.2845922609747311 | 1.1711511863949315 | 0.825222 | 0.594452 | - |
| 14 | correspondence/PRIMARY | single | 0.2847322616079229 | 1.176680746387501 | 0.836742 | 0.594518 | - |
| 15 | correspondence/SECONDARY | single | 0.2863260093056118 | 1.2057281228928776 | 0.830835 | 0.594151 | - |
| 16 | transducer/PRIMARY | single | 0.2874055706582019 | 1.1618469873541448 | 0.824465 | 0.593378 | - |
| 17 | r0202-analogist/PRIMARY | single | 0.2885706072901764 | 1.1991531400959292 | 0.827976 | 0.587319 | - |
| 18 | r0202-classifier/PRIMARY | single | 0.2896033417663429 | 1.2036210646771197 | 0.824118 | 0.587502 | - |
| 19 | r0202-correspondence/SECONDARY | single | 0.2908258046195304 | 1.2046294002508686 | 0.831236 | 0.591447 | - |
| 20 | r0202-correspondence/PRIMARY | single | 0.2913077560369119 | 1.2028531717085433 | 0.830716 | 0.589349 | - |
| 21 | r0202-classifier/SECONDARY | single | 0.2947015906669862 | 1.2295829504220965 | 0.818691 | 0.582488 | - |
| 22 | r0202-transducer/SECONDARY | single | 0.29843657939584967 | 1.169373958759764 | 0.815307 | 0.583818 | - |
| 23 | r0202-transducer/PRIMARY | single | 0.3033229092509786 | 1.1881544782320603 | 0.812167 | 0.577373 | - |

CANDIDATE (rule 10): COMB-8 (combination), val-0.50 mean NED 0.26250736260023105

CANDIDATE for N50, B50 and L50: COMB-8 (per-item MBR over the 8 entries above with weights [1, 2, 3, 2, 2, 1, 0, 2] in the listed order; test predictions out/comb8/test/0.50/).

## Disclosure for the panel (main session, from the lens reports; no test data involved)
classifier/PRIMARY and classifier/SECONDARY (both in COMB-8, weight 2 each) add rows of two development families as training data for two surprise families whose languages they share: mannburmish rows renamed onto hillburmish languages (Achang, Bela, Lashi, Maru, Zaiwa as AchangLongchuan, Bola, Lashi, Maru, Atsi; tones dropped; used for sparse targets) and listsamplesize rows (english, german, french) onto kesslersignificance's English, German and French with hand-made notation maps. PREREG rule 4 permits the development families (data/view/dev, the harness manifest's dev_dir) and the BRIEF named related development families as permitted training data; the shared task README calls the development data the data 'users should use to test and design their models'. The rows may contain the same concepts as the surprise gold in another dataset's transcription. The claim packages state this so that the CRITERION skeptic can judge it.

## sha256 of freeze records and of every val and test result file of every entry and of COMB-6 / COMB-8

```
ee19d511f28edddb7dee00ac7412baaef3503de3c4bf7901b73f9aa7b0b3294b  WORKDIR/runs/2026-10-18-0839/attempts/broker/FROZEN.md  (freeze record of broker)
fdc52d8bb7b34165b441c70001f1f5e45950382aec8fa2d2aa4de903622bc3c3  WORKDIR/runs/2026-10-18-0839/attempts/classifier/FROZEN.md  (freeze record of classifier)
d41dd287245ade644c9b101d867da3c0bf7c0bd8e63bb7aaddd050e837d36071  WORKDIR/runs/2026-10-18-0202/attempts/broker/FROZEN.md  (freeze record of r0202-broker)
a6bb14c4636ca63ea06f0dd3ee274edf4066f736445f7ee8c63053129dc1a68a  WORKDIR/runs/2026-10-18-0839/attempts/analogist/FROZEN.md  (freeze record of analogist)
e6588445159ebfe255a513a2c1df3b3613b46952733fe7778b799f631e144829  WORKDIR/runs/2026-10-18-0839/attempts/phylo/FROZEN.md  (freeze record of phylo)
c8b4cf2cf8cdfea760c5e8b5225e63597d86b36876f0757a27c110c636e24e63  WORKDIR/runs/2026-10-18-0202/attempts/analogist/FROZEN.md  (freeze record of r0202-analogist)
32b2829e22d9b2eabec2a9e5495995a43ffa58f6156e9a418c65e8ea88e0aaf6  WORKDIR/runs/2026-10-18-0202/attempts/phylo/FROZEN.md  (freeze record of r0202-phylo)
a76f26a1355f048ab59cc857ced36b127b98d0f0b2f93e8e69f03db8bfb736c5  WORKDIR/runs/2026-10-18-0839/attempts/correspondence/FROZEN.md  (freeze record of correspondence)
797d7a3e355455037efe3b2a0f575a0bfd0420ddce50e1bc999dc26363392202  WORKDIR/runs/2026-10-18-0839/attempts/transducer/FROZEN.md  (freeze record of transducer)
df50a06e0f9d9e0b2c01e0f01fda8d4f207b8651439fa80e00fadd558d6935cd  WORKDIR/runs/2026-10-18-0202/attempts/classifier/FROZEN.md  (freeze record of r0202-classifier)
cdb370ddc0d2fbf1d510bfbe6bc068fcfd02d88bc1e8c27508e55fb97178eac6  WORKDIR/runs/2026-10-18-0202/attempts/correspondence/FROZEN.md  (freeze record of r0202-correspondence)
4fb0ee28b20c7ec71524268bccefced87efc3e9964e7c66a4e927d3918bfcd91  WORKDIR/runs/2026-10-18-0202/attempts/transducer/FROZEN.md  (freeze record of r0202-transducer)
1e8bd3f856db7a2944d79d1f78ce9004a4028bbfe374fa6d3fa32deff32df3f5  WORKDIR/runs/2026-10-18-0839/attempts/broker/frozen/PRIMARY/val/0.50/bantubvd/result-0.50.tsv
1d5b7807128f44a7ba05ae1f4fba81ba7eb71f04b13f087c6b8facc318006497  WORKDIR/runs/2026-10-18-0839/attempts/broker/frozen/PRIMARY/val/0.50/beidazihui/result-0.50.tsv
089f2bab6c7871fd2bf2885a5cd2cde413d066aee7763968100fc9f0940aa66d  WORKDIR/runs/2026-10-18-0839/attempts/broker/frozen/PRIMARY/val/0.50/birchallchapacuran/result-0.50.tsv
a64023f8eb1941dae9457dd253c7fdbcfe7a5b732ed54c25818377a0588c2e06  WORKDIR/runs/2026-10-18-0839/attempts/broker/frozen/PRIMARY/val/0.50/bodtkhobwa/result-0.50.tsv
59c912441702dea2d183ccd767b4cce4f07bd38b8d8d671d31f8c44675ddce83  WORKDIR/runs/2026-10-18-0839/attempts/broker/frozen/PRIMARY/val/0.50/bremerberta/result-0.50.tsv
9af7da3043c1389f16bddbc16e1a3cc58da8440962ef67f04aa667f8618dcdc6  WORKDIR/runs/2026-10-18-0839/attempts/broker/frozen/PRIMARY/val/0.50/deepadungpalaung/result-0.50.tsv
7b89494592da18fe940bec5c3b3da7fbc369e1b0d99ce78a1d35a728eb25aaf5  WORKDIR/runs/2026-10-18-0839/attempts/broker/frozen/PRIMARY/val/0.50/hillburmish/result-0.50.tsv
580d7f5813657fd79d74b732ff333865396e403d9d43e10676593a0461825d49  WORKDIR/runs/2026-10-18-0839/attempts/broker/frozen/PRIMARY/val/0.50/kesslersignificance/result-0.50.tsv
961ba14554832453e78690d9aabd0f19aab79d544cfbc996281b065aefd1b266  WORKDIR/runs/2026-10-18-0839/attempts/broker/frozen/PRIMARY/val/0.50/luangthongkumkaren/result-0.50.tsv
6ca1628b76f16de3ca96129629e19f9801cc9673b6cb428d003fd15aac11e819  WORKDIR/runs/2026-10-18-0839/attempts/broker/frozen/PRIMARY/val/0.50/wangbai/result-0.50.tsv
d10f584c85bac66dab71e0c9a72859f5fdfa3615da61d78e0932c568caa9b3e3  WORKDIR/runs/2026-10-18-0839/attempts/broker/frozen/PRIMARY/test/0.50/bantubvd/result-0.50.tsv
67f4bc8e8667deefe2fbd32117a51875c651fb765ecbf3f16dd5d4050f3cf25f  WORKDIR/runs/2026-10-18-0839/attempts/broker/frozen/PRIMARY/test/0.50/beidazihui/result-0.50.tsv
5c24a120ec26a7c9e4808185889766bc3cfb3c1790178ee8e5632a1a61becde5  WORKDIR/runs/2026-10-18-0839/attempts/broker/frozen/PRIMARY/test/0.50/birchallchapacuran/result-0.50.tsv
fc7baa1e3c98d6a88a77a83e5a307156b1189aa3725f7f70e194638f4a999054  WORKDIR/runs/2026-10-18-0839/attempts/broker/frozen/PRIMARY/test/0.50/bodtkhobwa/result-0.50.tsv
95be5ff513f04a4e67f52a7430faeaee9add6a9734cbfbfb3731198a2bd469a7  WORKDIR/runs/2026-10-18-0839/attempts/broker/frozen/PRIMARY/test/0.50/bremerberta/result-0.50.tsv
864ca042b0ea12ccb47d645dc8529c10ea4b636fe39d9f0804ae324f8691f901  WORKDIR/runs/2026-10-18-0839/attempts/broker/frozen/PRIMARY/test/0.50/deepadungpalaung/result-0.50.tsv
72df6d401ee35f3d5110cb202d76e9e7cb4952d7e6d5c4db605b2c9fa057d86b  WORKDIR/runs/2026-10-18-0839/attempts/broker/frozen/PRIMARY/test/0.50/hillburmish/result-0.50.tsv
0ab9040377e3f4fbe506ef626bb6f69704ce1d079f15f5ca85b6a0666843cc50  WORKDIR/runs/2026-10-18-0839/attempts/broker/frozen/PRIMARY/test/0.50/kesslersignificance/result-0.50.tsv
1ac3cff3d483c95d34e55644eb1017f085c0047ea3596c919cabd4229406e9f6  WORKDIR/runs/2026-10-18-0839/attempts/broker/frozen/PRIMARY/test/0.50/luangthongkumkaren/result-0.50.tsv
b49e3fd4356f1f49979a441e6097210e5dae8a18d08939013d63585bb651fd7f  WORKDIR/runs/2026-10-18-0839/attempts/broker/frozen/PRIMARY/test/0.50/wangbai/result-0.50.tsv
2fb9d04eff0eca06c6f254621ecc4a4f9417244ef3473def4a3e691667c25831  WORKDIR/runs/2026-10-18-0839/attempts/classifier/frozen/SECONDARY/val/0.50/bantubvd/result-0.50.tsv
b4f3cf5599a80374091f14252ff225f38589c99670597e2b0861d77cb924c8c1  WORKDIR/runs/2026-10-18-0839/attempts/classifier/frozen/SECONDARY/val/0.50/beidazihui/result-0.50.tsv
00cb9a4f65060c3b23d1b09d4821b1dca7b544eff7c86301100775245ab9e9e5  WORKDIR/runs/2026-10-18-0839/attempts/classifier/frozen/SECONDARY/val/0.50/birchallchapacuran/result-0.50.tsv
da138b5ea464d9fb752446073b86c9646aa827e4b6850f15337b066840f8f1ae  WORKDIR/runs/2026-10-18-0839/attempts/classifier/frozen/SECONDARY/val/0.50/bodtkhobwa/result-0.50.tsv
1b6ea3e3601501ba9dec49588642a1cb7944b81ae373c1b394d679e52a01314a  WORKDIR/runs/2026-10-18-0839/attempts/classifier/frozen/SECONDARY/val/0.50/bremerberta/result-0.50.tsv
b5334769030ded817834f2cdd1857f59e5e6fd42a5b8b1fb5673cc9e72db0791  WORKDIR/runs/2026-10-18-0839/attempts/classifier/frozen/SECONDARY/val/0.50/deepadungpalaung/result-0.50.tsv
2ad34f805e6d660bbc91295f178241f8392afeec30cbfda5726d7bc128a79b14  WORKDIR/runs/2026-10-18-0839/attempts/classifier/frozen/SECONDARY/val/0.50/hillburmish/result-0.50.tsv
f2651efaca9fdcf9fba5b4b8362b770445c70dc20f3f1f3fa1c1cc65beda4f66  WORKDIR/runs/2026-10-18-0839/attempts/classifier/frozen/SECONDARY/val/0.50/kesslersignificance/result-0.50.tsv
1a45f9938ad160e9cba3be84b39d920f53d09d0404e4dad3c2154e8541d29e6d  WORKDIR/runs/2026-10-18-0839/attempts/classifier/frozen/SECONDARY/val/0.50/luangthongkumkaren/result-0.50.tsv
b1a5e9c2a46dde7d61e8ce55b97d1a7dbddbb6338a447ce7bd20fec901b79fe1  WORKDIR/runs/2026-10-18-0839/attempts/classifier/frozen/SECONDARY/val/0.50/wangbai/result-0.50.tsv
272f873480ce9fb7a00a092401c66d5f545d31572aa114e8c2c6f388d77d4453  WORKDIR/runs/2026-10-18-0839/attempts/classifier/frozen/SECONDARY/test/0.50/bantubvd/result-0.50.tsv
b4c414d767cba3e755e0d35c9b11ceab64b11c15330ccf906c328cacacefcc6f  WORKDIR/runs/2026-10-18-0839/attempts/classifier/frozen/SECONDARY/test/0.50/beidazihui/result-0.50.tsv
b37a454a99d913ba14a39d4d2142f167a4e041a5232784c70f8464b8a6e70f6e  WORKDIR/runs/2026-10-18-0839/attempts/classifier/frozen/SECONDARY/test/0.50/birchallchapacuran/result-0.50.tsv
f7e73c79b3dbb5f13acaf0a4488d1fa557208a5e41560a92417cf96096374c61  WORKDIR/runs/2026-10-18-0839/attempts/classifier/frozen/SECONDARY/test/0.50/bodtkhobwa/result-0.50.tsv
fea31b8f94af54ef1e419708c81635e85cc7dc8799489bc2111d047f560d31f5  WORKDIR/runs/2026-10-18-0839/attempts/classifier/frozen/SECONDARY/test/0.50/bremerberta/result-0.50.tsv
c27f946106c7a9ccf3b1a6454162b357bad65e2e340b8b01bddd1ac723e3c788  WORKDIR/runs/2026-10-18-0839/attempts/classifier/frozen/SECONDARY/test/0.50/deepadungpalaung/result-0.50.tsv
80ac8572d92ad41e255de3896a89b72932284d56297824c73e1af81d24151ace  WORKDIR/runs/2026-10-18-0839/attempts/classifier/frozen/SECONDARY/test/0.50/hillburmish/result-0.50.tsv
c457d74a40ad10db2501071e2da31f2bef1c06abbb422872e43167adbdd49392  WORKDIR/runs/2026-10-18-0839/attempts/classifier/frozen/SECONDARY/test/0.50/kesslersignificance/result-0.50.tsv
627c7f665bf2436b93b8ac6debdf193d417349f430bdd5116687b52fc9b0d33e  WORKDIR/runs/2026-10-18-0839/attempts/classifier/frozen/SECONDARY/test/0.50/luangthongkumkaren/result-0.50.tsv
aeda2cd3186fa1e3aedbb38cdea82cc33d6eedc6a9ff00a6d88e23d74f4b8dac  WORKDIR/runs/2026-10-18-0839/attempts/classifier/frozen/SECONDARY/test/0.50/wangbai/result-0.50.tsv
33719d84f7023b41f9effcdbcce284f7636580321b8cc47d6c2663553e93f74a  WORKDIR/runs/2026-10-18-0839/attempts/broker/frozen/SECONDARY/val/0.50/bantubvd/result-0.50.tsv
6f69547c77985bf1ae0db9413228114db6c8e3e8a77ba13302512af1032b48b8  WORKDIR/runs/2026-10-18-0839/attempts/broker/frozen/SECONDARY/val/0.50/beidazihui/result-0.50.tsv
7c0670d0bce90d29b2c58510d781d6e7fe10e4d2bc6cd890a00ead9e7e6b2fa2  WORKDIR/runs/2026-10-18-0839/attempts/broker/frozen/SECONDARY/val/0.50/birchallchapacuran/result-0.50.tsv
ad043e091d49de057d66abf299b79fada41ef66e08d5afe75192bf182c10cb15  WORKDIR/runs/2026-10-18-0839/attempts/broker/frozen/SECONDARY/val/0.50/bodtkhobwa/result-0.50.tsv
e52d5e6f1d0041e4bd8014da7dbb24b134a3c13e4e0fd4bc0d369bb52475b0c1  WORKDIR/runs/2026-10-18-0839/attempts/broker/frozen/SECONDARY/val/0.50/bremerberta/result-0.50.tsv
f4d85a14a4fcf809e6a6002584905bac5fc091218862c7b6d34be9695311d0b6  WORKDIR/runs/2026-10-18-0839/attempts/broker/frozen/SECONDARY/val/0.50/deepadungpalaung/result-0.50.tsv
05c3c23bada0dc4834cbf4d49f61f79497626a914138a681257633016406f7e0  WORKDIR/runs/2026-10-18-0839/attempts/broker/frozen/SECONDARY/val/0.50/hillburmish/result-0.50.tsv
b3b7c0a0a520196ec21a97c8ab9c12afd05d2d4fdb343b8088910ce157e23401  WORKDIR/runs/2026-10-18-0839/attempts/broker/frozen/SECONDARY/val/0.50/kesslersignificance/result-0.50.tsv
834d2938feb69394a0cab694498205f07032a644fd124f72a47985cf16426ecb  WORKDIR/runs/2026-10-18-0839/attempts/broker/frozen/SECONDARY/val/0.50/luangthongkumkaren/result-0.50.tsv
ac428e8dc1645efb43774c69588f967fd8960d9287dff17663f817dd26f4ed47  WORKDIR/runs/2026-10-18-0839/attempts/broker/frozen/SECONDARY/val/0.50/wangbai/result-0.50.tsv
796124a6a2e79f0f06e357c4bc917e4365a677cde9aac6f60ea7cbc4cbdea822  WORKDIR/runs/2026-10-18-0839/attempts/broker/frozen/SECONDARY/test/0.50/bantubvd/result-0.50.tsv
29df27525f4cdbeda217bffa6dd0b30c93e08789b4226029689bdfd236a53aec  WORKDIR/runs/2026-10-18-0839/attempts/broker/frozen/SECONDARY/test/0.50/beidazihui/result-0.50.tsv
4001e56e13387189a0d734fde08565032cb5e8533b2eeaa5f62518a207d83c11  WORKDIR/runs/2026-10-18-0839/attempts/broker/frozen/SECONDARY/test/0.50/birchallchapacuran/result-0.50.tsv
bfec3542bc6600ad74da3c365246d1d916fbeea6eace97bae6d806c83e551a1d  WORKDIR/runs/2026-10-18-0839/attempts/broker/frozen/SECONDARY/test/0.50/bodtkhobwa/result-0.50.tsv
c2a582407389ec7d2389c51adf3952a52068e8578f001d57811f45d0963c6e83  WORKDIR/runs/2026-10-18-0839/attempts/broker/frozen/SECONDARY/test/0.50/bremerberta/result-0.50.tsv
0a3351b4970210188ac7b4d0f820079a643b521ec69e01953a0cc9613ce92865  WORKDIR/runs/2026-10-18-0839/attempts/broker/frozen/SECONDARY/test/0.50/deepadungpalaung/result-0.50.tsv
16759b57cfada1bc7da62f3d3720a482f31703d5f6e7e44b2880d73fc175f507  WORKDIR/runs/2026-10-18-0839/attempts/broker/frozen/SECONDARY/test/0.50/hillburmish/result-0.50.tsv
692552b0008c2c462f22baa0ce69f3a31e2ba7d85bca640427f10e09e0f81f59  WORKDIR/runs/2026-10-18-0839/attempts/broker/frozen/SECONDARY/test/0.50/kesslersignificance/result-0.50.tsv
814e536d14dedeed0265fdb7e4abe8eac69c1934f35855574ccf58ba4c0fbbcf  WORKDIR/runs/2026-10-18-0839/attempts/broker/frozen/SECONDARY/test/0.50/luangthongkumkaren/result-0.50.tsv
a6947f23ef8173f598739c05a96b0537e296287959ad98b766dd9d9e3b2b5aed  WORKDIR/runs/2026-10-18-0839/attempts/broker/frozen/SECONDARY/test/0.50/wangbai/result-0.50.tsv
0def15f60ff5a5ffd44f2dfe21e3a603851c387b100664cfd6f1692952574d81  WORKDIR/runs/2026-10-18-0839/carry/broker-PRIMARY/val/0.50/bantubvd/result-0.50.tsv
97ab36f9cd2d5c2983a583989f1963d3294c7791f4c1eda659651024580fbcac  WORKDIR/runs/2026-10-18-0839/carry/broker-PRIMARY/val/0.50/beidazihui/result-0.50.tsv
00529e31ed59e3da1c466db7614d29909fa80cebec6dd97c75d5b6bee66eb0c2  WORKDIR/runs/2026-10-18-0839/carry/broker-PRIMARY/val/0.50/birchallchapacuran/result-0.50.tsv
83d63daa6c890694a715bbeff626471b6dbdd1d57d186a2cc6698b3958cc99eb  WORKDIR/runs/2026-10-18-0839/carry/broker-PRIMARY/val/0.50/bodtkhobwa/result-0.50.tsv
347e6f961cd1a143789451bdf96f547ee4e94545327bc87a8305a78ab2e14624  WORKDIR/runs/2026-10-18-0839/carry/broker-PRIMARY/val/0.50/bremerberta/result-0.50.tsv
127115e9179abce00ce30bbd69b29e40c10e54363cd9647012e2bef1fedf98a8  WORKDIR/runs/2026-10-18-0839/carry/broker-PRIMARY/val/0.50/deepadungpalaung/result-0.50.tsv
733621b30912e26ebbabf6174c3d86842bce7881f3c4fdd97ffb0a49c3ae30bb  WORKDIR/runs/2026-10-18-0839/carry/broker-PRIMARY/val/0.50/hillburmish/result-0.50.tsv
55d16d3167554e63f3b51a8eb4dfe9182b657911f6c30f7041b8ede47e49dbe7  WORKDIR/runs/2026-10-18-0839/carry/broker-PRIMARY/val/0.50/kesslersignificance/result-0.50.tsv
ebecf4c23c593cfbcf4cd582137691938b982dafe252bdb3df43a6596502c795  WORKDIR/runs/2026-10-18-0839/carry/broker-PRIMARY/val/0.50/luangthongkumkaren/result-0.50.tsv
f4bcbb439843fb792d3dcd8dd5bb5b0b0a4523f9eb0b209c4f4ca963c0839ae5  WORKDIR/runs/2026-10-18-0839/carry/broker-PRIMARY/val/0.50/wangbai/result-0.50.tsv
49199b962360449425fd2839bc12c267bdf55d99443e4040af054a9d41d15f8d  WORKDIR/runs/2026-10-18-0839/carry/broker-PRIMARY/test/0.50/bantubvd/result-0.50.tsv
42e2fc74b7c60ed9bc3269c0a6bfdf0873d10fd67b7f37c7cdeb1a33e5a34181  WORKDIR/runs/2026-10-18-0839/carry/broker-PRIMARY/test/0.50/beidazihui/result-0.50.tsv
e9efa86d9a9e5db9919a67b3a7da6ca12d3ebe68098cb2d1dbdca1602a868f87  WORKDIR/runs/2026-10-18-0839/carry/broker-PRIMARY/test/0.50/birchallchapacuran/result-0.50.tsv
7c15eb63a7a113ba5c2b09b166e21b806622ddac074a60095137157d04e33544  WORKDIR/runs/2026-10-18-0839/carry/broker-PRIMARY/test/0.50/bodtkhobwa/result-0.50.tsv
8ea90ff81861ac57f7eb245420c0471b86e6cb95f5a5821115424e247c838af2  WORKDIR/runs/2026-10-18-0839/carry/broker-PRIMARY/test/0.50/bremerberta/result-0.50.tsv
57698791aa4081c0887930e9b977312b000c6a552d8529cfd812fdcfa31b829f  WORKDIR/runs/2026-10-18-0839/carry/broker-PRIMARY/test/0.50/deepadungpalaung/result-0.50.tsv
8c043ea1cf909e261a35c85289fb8dbddd43b9f2edeeb1fa0ca09a8fe5229341  WORKDIR/runs/2026-10-18-0839/carry/broker-PRIMARY/test/0.50/hillburmish/result-0.50.tsv
eb14c7f33674cfe0e02412106f65064d0a6aad110983ac8357b4d49a139ea70c  WORKDIR/runs/2026-10-18-0839/carry/broker-PRIMARY/test/0.50/kesslersignificance/result-0.50.tsv
578e0ea7c2f1daeedb93185c18b5894445248b7a1711a3f012f04e947242eae1  WORKDIR/runs/2026-10-18-0839/carry/broker-PRIMARY/test/0.50/luangthongkumkaren/result-0.50.tsv
d833de839b1f12904172740f0ecea2e7e836850a0d0f0f754fb4cf12e4e227c8  WORKDIR/runs/2026-10-18-0839/carry/broker-PRIMARY/test/0.50/wangbai/result-0.50.tsv
efba3ac92c28b0833ce7c5ad7d1613485f190491a4385c8d850893a39fd7430c  WORKDIR/runs/2026-10-18-0839/attempts/classifier/frozen/PRIMARY/val/0.50/bantubvd/result-0.50.tsv
67cea2eff575e35855dae507683d7486e155418e5d881f76a09fc0c32d349688  WORKDIR/runs/2026-10-18-0839/attempts/classifier/frozen/PRIMARY/val/0.50/beidazihui/result-0.50.tsv
ec214dfc7e357754c0e9b4c7417bd152c85358b9979917266c05720e1c471803  WORKDIR/runs/2026-10-18-0839/attempts/classifier/frozen/PRIMARY/val/0.50/birchallchapacuran/result-0.50.tsv
dd5ecfc09d35e2e61e593f58be91125cb1c9ab4d95e7f9c71c572d5805c96f47  WORKDIR/runs/2026-10-18-0839/attempts/classifier/frozen/PRIMARY/val/0.50/bodtkhobwa/result-0.50.tsv
8dd62221b211ff8ba7b248c5c9316ac8550404ac18a403611538357615b39885  WORKDIR/runs/2026-10-18-0839/attempts/classifier/frozen/PRIMARY/val/0.50/bremerberta/result-0.50.tsv
a5c84e828b37026766f041976c74c2081815d2d34f9c582a585b1f8266923544  WORKDIR/runs/2026-10-18-0839/attempts/classifier/frozen/PRIMARY/val/0.50/deepadungpalaung/result-0.50.tsv
66734db13fde9c10c5b2bad1b49858cf88b2e8c26fc36f2f08d43b642f9653d9  WORKDIR/runs/2026-10-18-0839/attempts/classifier/frozen/PRIMARY/val/0.50/hillburmish/result-0.50.tsv
c19c20d4cf6326ae37e27d1712b8c431bf67b1a2ee4b706b6bd96cf165b0a76c  WORKDIR/runs/2026-10-18-0839/attempts/classifier/frozen/PRIMARY/val/0.50/kesslersignificance/result-0.50.tsv
d60d6b0bf445ea27301600b9c923890979416c0be37ddd0735442b36fab8da54  WORKDIR/runs/2026-10-18-0839/attempts/classifier/frozen/PRIMARY/val/0.50/luangthongkumkaren/result-0.50.tsv
0aa4cddfe6b412f35cb761928eb67a065df488bd22199b0e53e66d5fea606b2a  WORKDIR/runs/2026-10-18-0839/attempts/classifier/frozen/PRIMARY/val/0.50/wangbai/result-0.50.tsv
22c9cc934bdbc1ef54cb04e248220bd2ce38dd73dc45dc1d55bc0af9b4ba238f  WORKDIR/runs/2026-10-18-0839/attempts/classifier/frozen/PRIMARY/test/0.50/bantubvd/result-0.50.tsv
ecf4c073905910222387ad1c91d7d897ebdd28704a899e594af8adb45d8bcc88  WORKDIR/runs/2026-10-18-0839/attempts/classifier/frozen/PRIMARY/test/0.50/beidazihui/result-0.50.tsv
4b74fc5fc5203893f91aa07199797bc115ab716f10a34e6a9de51d710b020878  WORKDIR/runs/2026-10-18-0839/attempts/classifier/frozen/PRIMARY/test/0.50/birchallchapacuran/result-0.50.tsv
8a5617bf50f7f3b39732d193975a40f49bb1df029e84bfed9f660b2659f69db5  WORKDIR/runs/2026-10-18-0839/attempts/classifier/frozen/PRIMARY/test/0.50/bodtkhobwa/result-0.50.tsv
43ab226c9cc94941009ecaec3e1025eb81f917d923cdbce033b550464504b5bb  WORKDIR/runs/2026-10-18-0839/attempts/classifier/frozen/PRIMARY/test/0.50/bremerberta/result-0.50.tsv
6d6dad031fd229929cfb26b05925d18ae8374bc9dd03314867bca5a9bbf21772  WORKDIR/runs/2026-10-18-0839/attempts/classifier/frozen/PRIMARY/test/0.50/deepadungpalaung/result-0.50.tsv
63e5eb21b934bc2c77673755597e8a5f435f6f882aa30b06ec07f366697d3b7f  WORKDIR/runs/2026-10-18-0839/attempts/classifier/frozen/PRIMARY/test/0.50/hillburmish/result-0.50.tsv
178c52512cfa0621356cc6709f34ca45fcd836bd31f59b7b125043d977792cba  WORKDIR/runs/2026-10-18-0839/attempts/classifier/frozen/PRIMARY/test/0.50/kesslersignificance/result-0.50.tsv
c198a82b831c2113986fbeeb28bddab994f190ac3756da8ac5a5fe46615d7b91  WORKDIR/runs/2026-10-18-0839/attempts/classifier/frozen/PRIMARY/test/0.50/luangthongkumkaren/result-0.50.tsv
1b88b2b835958ed2465d0799a86202b46a0f48f49a728f0d986d77d7564cbdca  WORKDIR/runs/2026-10-18-0839/attempts/classifier/frozen/PRIMARY/test/0.50/wangbai/result-0.50.tsv
7985e44a2d3b74f8ab3a8e20ccc6810b187c616b4e6261bfa5f822b31185540a  WORKDIR/runs/2026-10-18-0839/attempts/analogist/frozen/PRIMARY/val/0.50/bantubvd/result-0.50.tsv
4d2fbd3bbcf9f423e64041befc449a07d50bdc5b4a6ff4d2fca9e61406c13281  WORKDIR/runs/2026-10-18-0839/attempts/analogist/frozen/PRIMARY/val/0.50/beidazihui/result-0.50.tsv
9351895d55fb1ace1941a1557c485e4b18b60e7be7916c45338fa6123b170f7d  WORKDIR/runs/2026-10-18-0839/attempts/analogist/frozen/PRIMARY/val/0.50/birchallchapacuran/result-0.50.tsv
e8d755499d7fd3ad2888b99e8426f58fff77613c7dddbdfc5534e325e29ae39c  WORKDIR/runs/2026-10-18-0839/attempts/analogist/frozen/PRIMARY/val/0.50/bodtkhobwa/result-0.50.tsv
211e64d57db8fcaa0f39ba700cc33bc1ebabc80b5e655f3efb4f600a3ac3e77d  WORKDIR/runs/2026-10-18-0839/attempts/analogist/frozen/PRIMARY/val/0.50/bremerberta/result-0.50.tsv
1413fc0c3896a33d570e28a92facaf58f5588c7772d035279b3d181e88726ddd  WORKDIR/runs/2026-10-18-0839/attempts/analogist/frozen/PRIMARY/val/0.50/deepadungpalaung/result-0.50.tsv
9f68d1352be65c12bacb1918d06de7f37d3754be3ba1960377f4e22f20bbdc2c  WORKDIR/runs/2026-10-18-0839/attempts/analogist/frozen/PRIMARY/val/0.50/hillburmish/result-0.50.tsv
4210e8fa1a080061c165caa348d0c00719c2dcd60499da658e26eef1dcfe812c  WORKDIR/runs/2026-10-18-0839/attempts/analogist/frozen/PRIMARY/val/0.50/kesslersignificance/result-0.50.tsv
adb5550f887e7abbe025b9ecb11d3fe2f6a92538e9854023b885f046cbb7c811  WORKDIR/runs/2026-10-18-0839/attempts/analogist/frozen/PRIMARY/val/0.50/luangthongkumkaren/result-0.50.tsv
8a01a63941d8fb4283d3220780dfe1f7b709c3aaa6603a60bd1c1ea083658105  WORKDIR/runs/2026-10-18-0839/attempts/analogist/frozen/PRIMARY/val/0.50/wangbai/result-0.50.tsv
6ca6ebf941d97185506fa847bbc388653cea7f30f6c189b96be4cb6cb9f8fdc5  WORKDIR/runs/2026-10-18-0839/attempts/analogist/frozen/PRIMARY/test/0.50/bantubvd/result-0.50.tsv
8340881fc87f305bca64b5692e6e9e2061b0e40cc04b5020e2ec9baf767eaa88  WORKDIR/runs/2026-10-18-0839/attempts/analogist/frozen/PRIMARY/test/0.50/beidazihui/result-0.50.tsv
1eb9429cbf6b30238847bcac9bd9400dde1c6f08d3f6d81129502e79214f7cc8  WORKDIR/runs/2026-10-18-0839/attempts/analogist/frozen/PRIMARY/test/0.50/birchallchapacuran/result-0.50.tsv
7e60e93794d70e9961b9aab562a7cf4b72a18f1458a51b9c5bf9169db4368250  WORKDIR/runs/2026-10-18-0839/attempts/analogist/frozen/PRIMARY/test/0.50/bodtkhobwa/result-0.50.tsv
76716e543dd2955171d215be72546f958cebb15560da6b79ad3e653f9f528658  WORKDIR/runs/2026-10-18-0839/attempts/analogist/frozen/PRIMARY/test/0.50/bremerberta/result-0.50.tsv
2e13ea45c0a6e006a6d6fffe6642153c947f1ce429a76dcf0f9bae5cc6acd469  WORKDIR/runs/2026-10-18-0839/attempts/analogist/frozen/PRIMARY/test/0.50/deepadungpalaung/result-0.50.tsv
ed88f4dbae5c2a7f49ee8ff64af287e760df1c7c2e25a060a9a6051fa093a5d3  WORKDIR/runs/2026-10-18-0839/attempts/analogist/frozen/PRIMARY/test/0.50/hillburmish/result-0.50.tsv
d4823be8407570f0572b5c4b37c4ce9b4f357b61d0d7b8120d4514d8009253b9  WORKDIR/runs/2026-10-18-0839/attempts/analogist/frozen/PRIMARY/test/0.50/kesslersignificance/result-0.50.tsv
84d096c945d71fab50f719224a39768d3ec9b1db1a77c8572f4d5fdb5ed25f37  WORKDIR/runs/2026-10-18-0839/attempts/analogist/frozen/PRIMARY/test/0.50/luangthongkumkaren/result-0.50.tsv
84535fdf5b0713af96510eda5873e8eacf12739dd371771bb5ea30acba90025a  WORKDIR/runs/2026-10-18-0839/attempts/analogist/frozen/PRIMARY/test/0.50/wangbai/result-0.50.tsv
1a2f6fef58ab43ca6d235bc53b8ebc8f502f78b58eed57f2d89c37b3bbf41bc0  WORKDIR/runs/2026-10-18-0839/attempts/phylo/frozen/PRIMARY/val/0.50/bantubvd/result-0.50.tsv
a1162536ac2a02e55b01df0ab919621616c9511eda06c0ee5c7f6000b46e94cb  WORKDIR/runs/2026-10-18-0839/attempts/phylo/frozen/PRIMARY/val/0.50/beidazihui/result-0.50.tsv
4419d80b702fdccd37cbaf79f1a94c9efe02a5ecd1885e903746260942b9ee97  WORKDIR/runs/2026-10-18-0839/attempts/phylo/frozen/PRIMARY/val/0.50/birchallchapacuran/result-0.50.tsv
311031ae7aefaceb5e54f06958fb2d68b8bc961b59991d5c51e5726027bf5252  WORKDIR/runs/2026-10-18-0839/attempts/phylo/frozen/PRIMARY/val/0.50/bodtkhobwa/result-0.50.tsv
2f8f45563a90b3ddb896c62c92156250629e49bdc94797737c61018641ea8cd5  WORKDIR/runs/2026-10-18-0839/attempts/phylo/frozen/PRIMARY/val/0.50/bremerberta/result-0.50.tsv
07fcad9b108697dcd9b519df6d323aae6fc021fad3c5fa2314d14645e1a66e56  WORKDIR/runs/2026-10-18-0839/attempts/phylo/frozen/PRIMARY/val/0.50/deepadungpalaung/result-0.50.tsv
7dbd2fc9995175c4a0540f794aeb785d12ef333475d699e6c9f380f3375c5c61  WORKDIR/runs/2026-10-18-0839/attempts/phylo/frozen/PRIMARY/val/0.50/hillburmish/result-0.50.tsv
171f2fd90609bcfb02992f17757f2d4c14ed10289d66f0b45ee4dcb0de30944a  WORKDIR/runs/2026-10-18-0839/attempts/phylo/frozen/PRIMARY/val/0.50/kesslersignificance/result-0.50.tsv
4b7daadc671cd68c10e2e0de9d07cda4fec8f88e935f108eaf9c3b124136b243  WORKDIR/runs/2026-10-18-0839/attempts/phylo/frozen/PRIMARY/val/0.50/luangthongkumkaren/result-0.50.tsv
13d81491bbbd850890f7492ce77092aae85bf885f5a509f8c79bef6337d2e76b  WORKDIR/runs/2026-10-18-0839/attempts/phylo/frozen/PRIMARY/val/0.50/wangbai/result-0.50.tsv
cf78f9641341f8ab7afc321a3d79352560d5535032c849b32290a87668c573b7  WORKDIR/runs/2026-10-18-0839/attempts/phylo/frozen/PRIMARY/test/0.50/bantubvd/result-0.50.tsv
96952ca4efcf0021bd77d69269ac891de4b7f4aa5f3e4f4bdf5cee7864675df5  WORKDIR/runs/2026-10-18-0839/attempts/phylo/frozen/PRIMARY/test/0.50/beidazihui/result-0.50.tsv
12d4850fc91477e1c77c7f27fc8383a4ee66b07105dc7c3fcca4230abb46ffb9  WORKDIR/runs/2026-10-18-0839/attempts/phylo/frozen/PRIMARY/test/0.50/birchallchapacuran/result-0.50.tsv
4a260478f1dd8e66a7bbd993c2ecc7c4116d8815bc55b053033ceb7251966065  WORKDIR/runs/2026-10-18-0839/attempts/phylo/frozen/PRIMARY/test/0.50/bodtkhobwa/result-0.50.tsv
73e8b8e4fd4a0edb695839c9efafab0d4b583f94bd4d42a6621dc8a2c1f23898  WORKDIR/runs/2026-10-18-0839/attempts/phylo/frozen/PRIMARY/test/0.50/bremerberta/result-0.50.tsv
8df2e6300b268e289faf3c69dcb6cd12fa72242e73272c030095f9882bb0fbd6  WORKDIR/runs/2026-10-18-0839/attempts/phylo/frozen/PRIMARY/test/0.50/deepadungpalaung/result-0.50.tsv
92ee9709bb8ed5ae68b194dfbda702c3ed23589355a06fd62c7f8366a81ba358  WORKDIR/runs/2026-10-18-0839/attempts/phylo/frozen/PRIMARY/test/0.50/hillburmish/result-0.50.tsv
9301c9f1ecd9a48b4fbd220e891da1bb5da0722672c5b00421aac12d03a09ac7  WORKDIR/runs/2026-10-18-0839/attempts/phylo/frozen/PRIMARY/test/0.50/kesslersignificance/result-0.50.tsv
04b10d6a8584242065e8b7f840b6653331461c336e2d89906ae277214eaf1a26  WORKDIR/runs/2026-10-18-0839/attempts/phylo/frozen/PRIMARY/test/0.50/luangthongkumkaren/result-0.50.tsv
9d4e388d5870f5a12f7825bb64622328bc2af789a8b6fe9d8cf9b558deebdaed  WORKDIR/runs/2026-10-18-0839/attempts/phylo/frozen/PRIMARY/test/0.50/wangbai/result-0.50.tsv
c820468bcb17309f931345d81c8139f2e7b7ea6ca6b7bb4762da5f755cc7c311  WORKDIR/runs/2026-10-18-0839/carry/analogist-SECONDARY/val/0.50/bantubvd/result-0.50.tsv
363aa329133e239a6812fd5ccf01df21a1b9e16d212f492cbfa1fae360edad63  WORKDIR/runs/2026-10-18-0839/carry/analogist-SECONDARY/val/0.50/beidazihui/result-0.50.tsv
b82c9fbf426abcd8a6a46ba4fa2625e7c16e8031fa5c44d7775a1791f2bb4cdd  WORKDIR/runs/2026-10-18-0839/carry/analogist-SECONDARY/val/0.50/birchallchapacuran/result-0.50.tsv
c3f2ec080af849a4aae87baa5c9c92d68c3c213eefc5d5852c84f5c39f355250  WORKDIR/runs/2026-10-18-0839/carry/analogist-SECONDARY/val/0.50/bodtkhobwa/result-0.50.tsv
d6dab6eb25cf472cd967b676222df1bb731b046247ac7feb8e73f10769132c86  WORKDIR/runs/2026-10-18-0839/carry/analogist-SECONDARY/val/0.50/bremerberta/result-0.50.tsv
dc90d5167d4601afed617e2b384d1691ce8e85b02a1643f3b12b8e18584aa585  WORKDIR/runs/2026-10-18-0839/carry/analogist-SECONDARY/val/0.50/deepadungpalaung/result-0.50.tsv
0054eb3b5ceee65d05e40392b9498270c7fc752965ce2ca3ddb000204a036da7  WORKDIR/runs/2026-10-18-0839/carry/analogist-SECONDARY/val/0.50/hillburmish/result-0.50.tsv
8e06e83a05f2e56cb45d97e9d03490bd31acfc5b9a99c5e3887d207c7f863c90  WORKDIR/runs/2026-10-18-0839/carry/analogist-SECONDARY/val/0.50/kesslersignificance/result-0.50.tsv
073e3262d5d751d86e330482c4e212c3b472ec832fdbc25064896cf1ee0f9c73  WORKDIR/runs/2026-10-18-0839/carry/analogist-SECONDARY/val/0.50/luangthongkumkaren/result-0.50.tsv
92461444c4251a161bed4a0f85636670dfa1eb1a5601e197fa9008a4b619195b  WORKDIR/runs/2026-10-18-0839/carry/analogist-SECONDARY/val/0.50/wangbai/result-0.50.tsv
7e4ce56fddfa7c72ef960dac5a4bf0e62e9784761915feea52eac2f832c48965  WORKDIR/runs/2026-10-18-0839/carry/analogist-SECONDARY/test/0.50/bantubvd/result-0.50.tsv
9316de554aee264ee181f7c7a9dca1086c3d92d64a75ba33a6e4e64fa784e84c  WORKDIR/runs/2026-10-18-0839/carry/analogist-SECONDARY/test/0.50/beidazihui/result-0.50.tsv
118c9e23b10544fb319df9437c03e606f3093dc7ba67a5598bcb1eedda7733c6  WORKDIR/runs/2026-10-18-0839/carry/analogist-SECONDARY/test/0.50/birchallchapacuran/result-0.50.tsv
17b902bf5039a42a003b3f84b54b22da94f2afa37ed92427eb0e282623a9d6fc  WORKDIR/runs/2026-10-18-0839/carry/analogist-SECONDARY/test/0.50/bodtkhobwa/result-0.50.tsv
4df3da71b394883ed98a29907bff7ca6dc7c5f841bf9928c789602bef5913f9b  WORKDIR/runs/2026-10-18-0839/carry/analogist-SECONDARY/test/0.50/bremerberta/result-0.50.tsv
62f9de565f47e33862cd00a8f17cdac822b5101e0b0ed1dc0b801c8f66515905  WORKDIR/runs/2026-10-18-0839/carry/analogist-SECONDARY/test/0.50/deepadungpalaung/result-0.50.tsv
939c7754fb3d80970749595d47ffbef65ad066dfaf8c570f7b2894b7bb2cc50d  WORKDIR/runs/2026-10-18-0839/carry/analogist-SECONDARY/test/0.50/hillburmish/result-0.50.tsv
05229aeafe5fb0eea8b543959565ed651c2643d229199e84134fede1ff6950cf  WORKDIR/runs/2026-10-18-0839/carry/analogist-SECONDARY/test/0.50/kesslersignificance/result-0.50.tsv
b742c52eea0c415fc715c7bd77755fd54007954c4e3d380435aaecee62061aa8  WORKDIR/runs/2026-10-18-0839/carry/analogist-SECONDARY/test/0.50/luangthongkumkaren/result-0.50.tsv
89f643863302be4441bff85776d32a2ed8909bb25611a5ad7b8ea7487174da74  WORKDIR/runs/2026-10-18-0839/carry/analogist-SECONDARY/test/0.50/wangbai/result-0.50.tsv
58c5e7cbd4aeb916df88b1ef92fe664629832df16fa7143054e5df5dc05daf27  WORKDIR/runs/2026-10-18-0839/carry/broker-SECONDARY/val/0.50/bantubvd/result-0.50.tsv
3d8757f19c8ac120707158cf884c635cef39c3c02e7a3d640cce7f5990fe7a7a  WORKDIR/runs/2026-10-18-0839/carry/broker-SECONDARY/val/0.50/beidazihui/result-0.50.tsv
9a7a3faefb17b84ff9dd525dd9a82492eaad9d45dd62f573699b0d35ecbe1dab  WORKDIR/runs/2026-10-18-0839/carry/broker-SECONDARY/val/0.50/birchallchapacuran/result-0.50.tsv
4829ad93f8dc5a24907dd0424a86566edb5f3cb304f6ceabca8162e85a67bf88  WORKDIR/runs/2026-10-18-0839/carry/broker-SECONDARY/val/0.50/bodtkhobwa/result-0.50.tsv
1e04222396ff15d68a1ebbc85a93c1101ea919d88a627397b1ada0f5fa63f2fe  WORKDIR/runs/2026-10-18-0839/carry/broker-SECONDARY/val/0.50/bremerberta/result-0.50.tsv
23d31ffca5f8a310ad14550f8500260a4c6f254440e026b4cced40c7254c2823  WORKDIR/runs/2026-10-18-0839/carry/broker-SECONDARY/val/0.50/deepadungpalaung/result-0.50.tsv
a0f0fa4ba556de9487d3343eeffab760a75a8629a7dc9dbd6a9979a1beedcb33  WORKDIR/runs/2026-10-18-0839/carry/broker-SECONDARY/val/0.50/hillburmish/result-0.50.tsv
6733c38a103081800929edf4de7d75484c16348e3c6d536fd84324902829c936  WORKDIR/runs/2026-10-18-0839/carry/broker-SECONDARY/val/0.50/kesslersignificance/result-0.50.tsv
49f43dd5909bc6aa2d1d8f565f52c1ca2ec5572d7ee1ccaece2587c98e94cb42  WORKDIR/runs/2026-10-18-0839/carry/broker-SECONDARY/val/0.50/luangthongkumkaren/result-0.50.tsv
91ac6f255ec40be406eccab61a810a22db216718dec7d1a8ffec74dd105bfb01  WORKDIR/runs/2026-10-18-0839/carry/broker-SECONDARY/val/0.50/wangbai/result-0.50.tsv
4b0d70ed62aca809adf2865b09d258c29463c6ba3c60feeec58b83556f62a8d2  WORKDIR/runs/2026-10-18-0839/carry/broker-SECONDARY/test/0.50/bantubvd/result-0.50.tsv
ea9443e036900978f4939a569da7e5b0b11b9c2bad811e95b8878fc18597c569  WORKDIR/runs/2026-10-18-0839/carry/broker-SECONDARY/test/0.50/beidazihui/result-0.50.tsv
0c68c76d232c82d30a31db32fc2c0abb7249eb6a57c0b5135b55f9e6e46e54d4  WORKDIR/runs/2026-10-18-0839/carry/broker-SECONDARY/test/0.50/birchallchapacuran/result-0.50.tsv
2c37a9b1f0f17cc73c963ff752b444f51f86dd8881f5e463f12b8405c6fb8426  WORKDIR/runs/2026-10-18-0839/carry/broker-SECONDARY/test/0.50/bodtkhobwa/result-0.50.tsv
96ff0d2c715a73961832466d971fe82dc0ff2257ce8e5d6f89c075db774651c9  WORKDIR/runs/2026-10-18-0839/carry/broker-SECONDARY/test/0.50/bremerberta/result-0.50.tsv
aa7b11900e85bcab7f40e5d8024e3832adca348a074879a371c3ed44b515c64f  WORKDIR/runs/2026-10-18-0839/carry/broker-SECONDARY/test/0.50/deepadungpalaung/result-0.50.tsv
51ccb756e8d706cfb76cb4d3d8fd96a96ef81358388787a4f9d916c165e1d223  WORKDIR/runs/2026-10-18-0839/carry/broker-SECONDARY/test/0.50/hillburmish/result-0.50.tsv
d8f73eeff4721849742ea1d4feb7fd1d10070bb35cee275b0a19ffdb525ec21a  WORKDIR/runs/2026-10-18-0839/carry/broker-SECONDARY/test/0.50/kesslersignificance/result-0.50.tsv
42b8ac59b96cb34e461796035f482d4d1c15d23728eb654c3e6b1d6ecef7c6cd  WORKDIR/runs/2026-10-18-0839/carry/broker-SECONDARY/test/0.50/luangthongkumkaren/result-0.50.tsv
38f39a0ca66642d2347daa0c419964ac3ea7712bfc56705d330ab00e77643f71  WORKDIR/runs/2026-10-18-0839/carry/broker-SECONDARY/test/0.50/wangbai/result-0.50.tsv
9d2b42785efe7916a0a932ec5f531b7ba85fda836b8da401a4c8cce2549870ae  WORKDIR/runs/2026-10-18-0839/attempts/phylo/frozen/SECONDARY/val/0.50/bantubvd/result-0.50.tsv
da4fb3f20de7c4f144fdab2167a2233bc93941857b81dbd6e28b323e52b8a4e6  WORKDIR/runs/2026-10-18-0839/attempts/phylo/frozen/SECONDARY/val/0.50/beidazihui/result-0.50.tsv
a726b9ad0e9653df281ec0d6f0469eef0122ca04a6c9df182067d232566ebbc0  WORKDIR/runs/2026-10-18-0839/attempts/phylo/frozen/SECONDARY/val/0.50/birchallchapacuran/result-0.50.tsv
dd2ff7e2cb3e475a4022c649c8f67a89c3fe1d723b57220195cc1e08d1f36884  WORKDIR/runs/2026-10-18-0839/attempts/phylo/frozen/SECONDARY/val/0.50/bodtkhobwa/result-0.50.tsv
0520f9129fe16028c7739068f683e49c33d775a8bf8899a6c11e69b365a0720f  WORKDIR/runs/2026-10-18-0839/attempts/phylo/frozen/SECONDARY/val/0.50/bremerberta/result-0.50.tsv
d95052715cb200c48f79502ee55fbd351dd9697479c3c554083b532c1435a4e5  WORKDIR/runs/2026-10-18-0839/attempts/phylo/frozen/SECONDARY/val/0.50/deepadungpalaung/result-0.50.tsv
8cfdc7173af62b7a1f8db90cc4d23ac86cfaeffd3e1903d06013a46cb1781804  WORKDIR/runs/2026-10-18-0839/attempts/phylo/frozen/SECONDARY/val/0.50/hillburmish/result-0.50.tsv
83b8605ce620963a8d3c33051bdef2a2aacdeccd62da01bcc2cba64641feb2ca  WORKDIR/runs/2026-10-18-0839/attempts/phylo/frozen/SECONDARY/val/0.50/kesslersignificance/result-0.50.tsv
ed374805089bd3b2e9ff4ee57573eaf5458fac9fbc6138615f368e56d97b7de7  WORKDIR/runs/2026-10-18-0839/attempts/phylo/frozen/SECONDARY/val/0.50/luangthongkumkaren/result-0.50.tsv
04cbb9d998e62b7e57754056fbb7ac2df01d7fef3c47c9492db70b658abeae7c  WORKDIR/runs/2026-10-18-0839/attempts/phylo/frozen/SECONDARY/val/0.50/wangbai/result-0.50.tsv
2b148236bb2941182deaa428576f62ec89fd69d8d6ad9171d259fab32508cb38  WORKDIR/runs/2026-10-18-0839/attempts/phylo/frozen/SECONDARY/test/0.50/bantubvd/result-0.50.tsv
6ea22e2a464227b41850e6165818a90d8a02446baa820eff8aec461e910ade66  WORKDIR/runs/2026-10-18-0839/attempts/phylo/frozen/SECONDARY/test/0.50/beidazihui/result-0.50.tsv
d646b79068268bcc3c5890ffb5b51c420d5c259bf09d5770d6c3186fcece79de  WORKDIR/runs/2026-10-18-0839/attempts/phylo/frozen/SECONDARY/test/0.50/birchallchapacuran/result-0.50.tsv
21c6d952ec4de37e8d5add1582f196a4613725933b019f4495bfb63191659a67  WORKDIR/runs/2026-10-18-0839/attempts/phylo/frozen/SECONDARY/test/0.50/bodtkhobwa/result-0.50.tsv
42e6e5fc784a6a6a4c81f92680f9109b721de6d0fda43bb578f4ebe91d1dd0ef  WORKDIR/runs/2026-10-18-0839/attempts/phylo/frozen/SECONDARY/test/0.50/bremerberta/result-0.50.tsv
fea1ab2d94a5cf6eb73bbca8f0ea26d49d9d8be82d357cd2b025aa84ec379849  WORKDIR/runs/2026-10-18-0839/attempts/phylo/frozen/SECONDARY/test/0.50/deepadungpalaung/result-0.50.tsv
962c7b6d6c7deb58d657ad05be989a42e25e512cc6db734be78b806213d137b4  WORKDIR/runs/2026-10-18-0839/attempts/phylo/frozen/SECONDARY/test/0.50/hillburmish/result-0.50.tsv
b214e2d961b4b0f9d5841bb25148255cc77ee30d3161524ba7c7e47818afade7  WORKDIR/runs/2026-10-18-0839/attempts/phylo/frozen/SECONDARY/test/0.50/kesslersignificance/result-0.50.tsv
f634016f83f9d3328215f84aeba07d30e0173f82c1d74ed8e8a37712e058b1da  WORKDIR/runs/2026-10-18-0839/attempts/phylo/frozen/SECONDARY/test/0.50/luangthongkumkaren/result-0.50.tsv
040e9c698b3b13ac40ef5f00b645f4ae1429a63695ae9e025c15a99328a5be6e  WORKDIR/runs/2026-10-18-0839/attempts/phylo/frozen/SECONDARY/test/0.50/wangbai/result-0.50.tsv
0d374a8a9571ddc13463dab909c3c938db22ba5ff679c6c852aaedd80bf0ba6e  WORKDIR/runs/2026-10-18-0839/carry/phylo-PRIMARY/val/0.50/bantubvd/result-0.50.tsv
c6961a03999f4e6c6f4c80fb231f284feb96ce13a84bd7d3d41843ba01ac1b2e  WORKDIR/runs/2026-10-18-0839/carry/phylo-PRIMARY/val/0.50/beidazihui/result-0.50.tsv
10d28aac82e84525843281d6021beed4b1f8f1154d19e8660cd589c77d4d95cd  WORKDIR/runs/2026-10-18-0839/carry/phylo-PRIMARY/val/0.50/birchallchapacuran/result-0.50.tsv
661d5c1ba763fa44655547f73d3418f6b144b2c2e94eac7be002ad318ba1f7c6  WORKDIR/runs/2026-10-18-0839/carry/phylo-PRIMARY/val/0.50/bodtkhobwa/result-0.50.tsv
b6d9817c499745f412b74ff8301ec5c05fa377f6801213ada3e01f9f6bd8957c  WORKDIR/runs/2026-10-18-0839/carry/phylo-PRIMARY/val/0.50/bremerberta/result-0.50.tsv
83d8b55a08f7f4d02e5d8dd63a03cacb1648d4faa85cd4897f82b371ba8353ec  WORKDIR/runs/2026-10-18-0839/carry/phylo-PRIMARY/val/0.50/deepadungpalaung/result-0.50.tsv
5edc993f4d05d6a59493119cbc44de3c06d5fe0fec65cda2402c3f5f3445ff15  WORKDIR/runs/2026-10-18-0839/carry/phylo-PRIMARY/val/0.50/hillburmish/result-0.50.tsv
e6b1e077744d5a9c20f2bf562a9c8a06da0a5ba7e4f33904bccfbc1a61d3e988  WORKDIR/runs/2026-10-18-0839/carry/phylo-PRIMARY/val/0.50/kesslersignificance/result-0.50.tsv
bbba78dcd1a7c091faae3a9234dad76fb9208f0cced99ce5ac8b3c82dfea2bd2  WORKDIR/runs/2026-10-18-0839/carry/phylo-PRIMARY/val/0.50/luangthongkumkaren/result-0.50.tsv
e7be0e3791f512b82dbda467774065552bd38587d0328478b11ac652f9d2b153  WORKDIR/runs/2026-10-18-0839/carry/phylo-PRIMARY/val/0.50/wangbai/result-0.50.tsv
577549e879ed4f453fb917933e99f0d918b2262a494af287405c7574732ea68c  WORKDIR/runs/2026-10-18-0839/carry/phylo-PRIMARY/test/0.50/bantubvd/result-0.50.tsv
ec65ac673780c8f7b65c3e7b47fbf340cc0627705b141acf25118e0c61d05a33  WORKDIR/runs/2026-10-18-0839/carry/phylo-PRIMARY/test/0.50/beidazihui/result-0.50.tsv
b9875c8bc6df4f29ceb74dfab82a6aa00b6331b03a4c78540e9313520f260275  WORKDIR/runs/2026-10-18-0839/carry/phylo-PRIMARY/test/0.50/birchallchapacuran/result-0.50.tsv
c9ffea361105e53db0e67c998aea0a949752a13938396880a78d7b8e0f0cdb86  WORKDIR/runs/2026-10-18-0839/carry/phylo-PRIMARY/test/0.50/bodtkhobwa/result-0.50.tsv
c88b826f36920a875e5de45dc081a92555e9fc9374682b853f0a2f0d76bf6058  WORKDIR/runs/2026-10-18-0839/carry/phylo-PRIMARY/test/0.50/bremerberta/result-0.50.tsv
4650083d6c246c5d07ac6d0de627bda20c8a38b40225ac4e3b6cba4c5df012d6  WORKDIR/runs/2026-10-18-0839/carry/phylo-PRIMARY/test/0.50/deepadungpalaung/result-0.50.tsv
69500b3e1826cc4e243a9acfc42a90853cb6ad2e0fac4a4f2bf37df5f80aefb0  WORKDIR/runs/2026-10-18-0839/carry/phylo-PRIMARY/test/0.50/hillburmish/result-0.50.tsv
9b0dc06b7b74eca88824523d820e82514632dab609c2ff85ca441553d484e6e9  WORKDIR/runs/2026-10-18-0839/carry/phylo-PRIMARY/test/0.50/kesslersignificance/result-0.50.tsv
3535364844bb976da96d1db3e9f9d79efe1bfab2efc9d7251a7ea1b9003c8085  WORKDIR/runs/2026-10-18-0839/carry/phylo-PRIMARY/test/0.50/luangthongkumkaren/result-0.50.tsv
add4dc598f50bcbdc83ce463fbffac4992612acc068809ca61b40454b3e132fd  WORKDIR/runs/2026-10-18-0839/carry/phylo-PRIMARY/test/0.50/wangbai/result-0.50.tsv
8c33f872615c41bfc1c1b13be6ecc9cdf7f86a3a981116e975ac93a58262de7e  WORKDIR/runs/2026-10-18-0839/attempts/correspondence/frozen/PRIMARY/val/0.50/bantubvd/result-0.50.tsv
352d52a56f1abb0fd4b71e33bdf47f831b820ba36cfc02e7478bf07b6c41af63  WORKDIR/runs/2026-10-18-0839/attempts/correspondence/frozen/PRIMARY/val/0.50/beidazihui/result-0.50.tsv
e8440f91304c39b29d2d457232650d9510a126727fdb6c2f7e41d1241a7674ee  WORKDIR/runs/2026-10-18-0839/attempts/correspondence/frozen/PRIMARY/val/0.50/birchallchapacuran/result-0.50.tsv
d48bd0650b85567b027a556b5b7524790ddf418b7fdd513cc91c65a80fda55e2  WORKDIR/runs/2026-10-18-0839/attempts/correspondence/frozen/PRIMARY/val/0.50/bodtkhobwa/result-0.50.tsv
19546a66cc1fb10fb1eecd841b99419b98b903f16ec63c229919646e46f78071  WORKDIR/runs/2026-10-18-0839/attempts/correspondence/frozen/PRIMARY/val/0.50/bremerberta/result-0.50.tsv
a0253fed757d81401439e08e2f1a4c9acb9864f42f24068cbbfaab61db96a797  WORKDIR/runs/2026-10-18-0839/attempts/correspondence/frozen/PRIMARY/val/0.50/deepadungpalaung/result-0.50.tsv
86d8cccd68d296fe5b333cb139b8d6b8020641dec8cf531a00c1d462be28f289  WORKDIR/runs/2026-10-18-0839/attempts/correspondence/frozen/PRIMARY/val/0.50/hillburmish/result-0.50.tsv
903a3fd0bc8919930dacfbe67b6cda0d500ce9473d07133f2f7c73a8e0812625  WORKDIR/runs/2026-10-18-0839/attempts/correspondence/frozen/PRIMARY/val/0.50/kesslersignificance/result-0.50.tsv
c5cc229afd6211f4bfdbe1c6092e8ef45ad503414c67f7c11722ebf894c58958  WORKDIR/runs/2026-10-18-0839/attempts/correspondence/frozen/PRIMARY/val/0.50/luangthongkumkaren/result-0.50.tsv
35936983c952dbf496d8e5539fb2312720c3e9c7f7531dd1a8de7be55341ce21  WORKDIR/runs/2026-10-18-0839/attempts/correspondence/frozen/PRIMARY/val/0.50/wangbai/result-0.50.tsv
0d8fc17d45df2cb86e5a154fd10ea418c3a41e3317b54fb51a2d3fbe6801581e  WORKDIR/runs/2026-10-18-0839/attempts/correspondence/frozen/PRIMARY/test/0.50/bantubvd/result-0.50.tsv
06a63c5c81b78a72d367ec1c10fbfa8be1aa03198f966718166d3b365513446c  WORKDIR/runs/2026-10-18-0839/attempts/correspondence/frozen/PRIMARY/test/0.50/beidazihui/result-0.50.tsv
86b271f44c5dcf5eee03cade02743cd07b8c3d70e3267f40005563dcd88d25e3  WORKDIR/runs/2026-10-18-0839/attempts/correspondence/frozen/PRIMARY/test/0.50/birchallchapacuran/result-0.50.tsv
ab70d007d2087f169cce83a44476a1c7eb34283c176711c29552e625aa97dc15  WORKDIR/runs/2026-10-18-0839/attempts/correspondence/frozen/PRIMARY/test/0.50/bodtkhobwa/result-0.50.tsv
379bec62933fefede079fa5687e5302de3223c03dd02340190df7ca76e044be2  WORKDIR/runs/2026-10-18-0839/attempts/correspondence/frozen/PRIMARY/test/0.50/bremerberta/result-0.50.tsv
d19044b9203cab58faf50ebd15153189f332aed90132c34222fdfa51d93250a8  WORKDIR/runs/2026-10-18-0839/attempts/correspondence/frozen/PRIMARY/test/0.50/deepadungpalaung/result-0.50.tsv
cff70b4f34bd1ebefba100efe4a4a601442d1de245c4efe81359ec131dc8ff6a  WORKDIR/runs/2026-10-18-0839/attempts/correspondence/frozen/PRIMARY/test/0.50/hillburmish/result-0.50.tsv
684a3a7a1331b7374e7fdf329c1039f75f64326c2d436bd997329e463e29fbef  WORKDIR/runs/2026-10-18-0839/attempts/correspondence/frozen/PRIMARY/test/0.50/kesslersignificance/result-0.50.tsv
7b3bfaadcb3733fdf73006b532b61d666282fad1ef93450dee22876ce547de71  WORKDIR/runs/2026-10-18-0839/attempts/correspondence/frozen/PRIMARY/test/0.50/luangthongkumkaren/result-0.50.tsv
5849262bd744cc1317a3e3dbd7422c6876cf83f6abce0746a3c83518b6f4781f  WORKDIR/runs/2026-10-18-0839/attempts/correspondence/frozen/PRIMARY/test/0.50/wangbai/result-0.50.tsv
cfbca1b8fc43227ba7dad8aeddf6d9afccf4787bffd43e0da2f94a6b59df158b  WORKDIR/runs/2026-10-18-0839/attempts/correspondence/frozen/SECONDARY/val/0.50/bantubvd/result-0.50.tsv
db729da9e86bb57ac0ca12390a9541e83a86e94ea8a63875106632e3c56e1bc6  WORKDIR/runs/2026-10-18-0839/attempts/correspondence/frozen/SECONDARY/val/0.50/beidazihui/result-0.50.tsv
77f225b86e2d57ec91fbfd4f1c69dbdd26b544adbfd750580f349892e61e7886  WORKDIR/runs/2026-10-18-0839/attempts/correspondence/frozen/SECONDARY/val/0.50/birchallchapacuran/result-0.50.tsv
74cb944ece1a048137027b6f884a3013c44ba2f13c8da226dd6dda7adfe6e07f  WORKDIR/runs/2026-10-18-0839/attempts/correspondence/frozen/SECONDARY/val/0.50/bodtkhobwa/result-0.50.tsv
0b6361a63d5740f50bd41c2ae3b3400a3628a7ff1d2311f2d53d29fbbb3c3299  WORKDIR/runs/2026-10-18-0839/attempts/correspondence/frozen/SECONDARY/val/0.50/bremerberta/result-0.50.tsv
2f7a9bf2f9a11ff5aefe49d5774b0efb6d5b5c0797964caa2f0bc629c1ddf739  WORKDIR/runs/2026-10-18-0839/attempts/correspondence/frozen/SECONDARY/val/0.50/deepadungpalaung/result-0.50.tsv
e3814797362b02d571c04e7f7b899689a3a52d4665263d0b1214fbc5293110fb  WORKDIR/runs/2026-10-18-0839/attempts/correspondence/frozen/SECONDARY/val/0.50/hillburmish/result-0.50.tsv
38f7c1888e22dc27bb78796b95e78a84786fcdf3bbf399b59e54699948fe86bb  WORKDIR/runs/2026-10-18-0839/attempts/correspondence/frozen/SECONDARY/val/0.50/kesslersignificance/result-0.50.tsv
246322ba50bb6a49bf449b65874183771386a3cbfc3093f061fa04801b26873c  WORKDIR/runs/2026-10-18-0839/attempts/correspondence/frozen/SECONDARY/val/0.50/luangthongkumkaren/result-0.50.tsv
1c0eb52c5cf0eb38b74dcac006f0baa0eb04e8ba5bc13a2072b8fa9f4794e192  WORKDIR/runs/2026-10-18-0839/attempts/correspondence/frozen/SECONDARY/val/0.50/wangbai/result-0.50.tsv
93281de3e70e2718d51bc49d48999997d867b5d4e2fc68fa6c7a25ed2b06ba92  WORKDIR/runs/2026-10-18-0839/attempts/correspondence/frozen/SECONDARY/test/0.50/bantubvd/result-0.50.tsv
20859275e82194fbd5d114fc150bf4b3f49912833849e2ae12f715379dfc0ba4  WORKDIR/runs/2026-10-18-0839/attempts/correspondence/frozen/SECONDARY/test/0.50/beidazihui/result-0.50.tsv
39c1288f10865f98859df04e4d2f08c6fb7ee85da162ce5911f8c35cfca8673b  WORKDIR/runs/2026-10-18-0839/attempts/correspondence/frozen/SECONDARY/test/0.50/birchallchapacuran/result-0.50.tsv
2b01cf497d98008d8bc295228dd77db98323d486e54b0f7b022e0d8ec464b1c1  WORKDIR/runs/2026-10-18-0839/attempts/correspondence/frozen/SECONDARY/test/0.50/bodtkhobwa/result-0.50.tsv
b5366dbe56c5ef1e708f1c908e7146b2de51e21a535a0f3ffe62c9b6fff9fdc8  WORKDIR/runs/2026-10-18-0839/attempts/correspondence/frozen/SECONDARY/test/0.50/bremerberta/result-0.50.tsv
e156f590f8010febdb2f8f68cab4b0ae9bff6ba684c8463e2719f98d2d4484b3  WORKDIR/runs/2026-10-18-0839/attempts/correspondence/frozen/SECONDARY/test/0.50/deepadungpalaung/result-0.50.tsv
22fc671575fe1cea0d8431e27557b1f019eab23a673c15efffb393348fd3ebeb  WORKDIR/runs/2026-10-18-0839/attempts/correspondence/frozen/SECONDARY/test/0.50/hillburmish/result-0.50.tsv
7d3fdbde6ed3323af0f70254fcb011d1859ecd955a440c49aa67f1e42a4c5655  WORKDIR/runs/2026-10-18-0839/attempts/correspondence/frozen/SECONDARY/test/0.50/kesslersignificance/result-0.50.tsv
75560babce00a0ea64d2eb9eab1888aa40378cc17316a7ce1cd65bab696e8aa9  WORKDIR/runs/2026-10-18-0839/attempts/correspondence/frozen/SECONDARY/test/0.50/luangthongkumkaren/result-0.50.tsv
72298fce85a5eae84f933ec61a6c20718649fba5f08b9ce85f24c5548ac20e6d  WORKDIR/runs/2026-10-18-0839/attempts/correspondence/frozen/SECONDARY/test/0.50/wangbai/result-0.50.tsv
79ceb6a75d8ffd7895774a7f165592e24b88342eb6bdfd720df121c2a635e8d4  WORKDIR/runs/2026-10-18-0839/attempts/transducer/frozen/PRIMARY/val/0.50/bantubvd/result-0.50.tsv
818eb5f31196913ec02c1ca5eb92e67370b18d0bccbcdebd262d33529e88b822  WORKDIR/runs/2026-10-18-0839/attempts/transducer/frozen/PRIMARY/val/0.50/beidazihui/result-0.50.tsv
445ebbb43b815d854ee43b51239a73c2b3390500a4eac79c215e62837d6ba700  WORKDIR/runs/2026-10-18-0839/attempts/transducer/frozen/PRIMARY/val/0.50/birchallchapacuran/result-0.50.tsv
ee14884cf5332f3f5da055eedc7e13ad06c227079489d530b4e26ca5e009c7f0  WORKDIR/runs/2026-10-18-0839/attempts/transducer/frozen/PRIMARY/val/0.50/bodtkhobwa/result-0.50.tsv
65cb74b235f09116da5fb0c0a3bf4c3e2cd4c8ab78aa3565989f9198e68c7c90  WORKDIR/runs/2026-10-18-0839/attempts/transducer/frozen/PRIMARY/val/0.50/bremerberta/result-0.50.tsv
493d14c3f07c3e5dfd34891ca323e1fa84a27083fd83311386ad539cca5af588  WORKDIR/runs/2026-10-18-0839/attempts/transducer/frozen/PRIMARY/val/0.50/deepadungpalaung/result-0.50.tsv
7804325cb6d449cc1113e30496edee10aa130d624c77a70cc9556da6accfb589  WORKDIR/runs/2026-10-18-0839/attempts/transducer/frozen/PRIMARY/val/0.50/hillburmish/result-0.50.tsv
665bc35262d7d2d38f6e4a16441db96e571d4fce1a39ae332e0b677e26c834d0  WORKDIR/runs/2026-10-18-0839/attempts/transducer/frozen/PRIMARY/val/0.50/kesslersignificance/result-0.50.tsv
8a43c095501bc4a882d38c3cb7aa2afe5cc6af021075a00147ef1a46a4ffb07c  WORKDIR/runs/2026-10-18-0839/attempts/transducer/frozen/PRIMARY/val/0.50/luangthongkumkaren/result-0.50.tsv
c0fde0f7ab3ee2139300054c1d82ff926a57383fadf851a9acf5a7fbd4984203  WORKDIR/runs/2026-10-18-0839/attempts/transducer/frozen/PRIMARY/val/0.50/wangbai/result-0.50.tsv
1d3c17ae2b42f35057c06bef73f5c784e3deafc5d3d8b0323bd02149650dcbbf  WORKDIR/runs/2026-10-18-0839/attempts/transducer/frozen/PRIMARY/test/0.50/bantubvd/result-0.50.tsv
1c70414bea98c62d0dffec65cb59ff022a18bba4e871f46d4c8d60e0398e90a2  WORKDIR/runs/2026-10-18-0839/attempts/transducer/frozen/PRIMARY/test/0.50/beidazihui/result-0.50.tsv
30cf2bf176e808181d765968d34f9ae735a15a2ce551e7d81050b177e78158a4  WORKDIR/runs/2026-10-18-0839/attempts/transducer/frozen/PRIMARY/test/0.50/birchallchapacuran/result-0.50.tsv
e6fce2b00fc1de57e852f5a18ade561327a7663869fd5d0f8b64e59475cafa14  WORKDIR/runs/2026-10-18-0839/attempts/transducer/frozen/PRIMARY/test/0.50/bodtkhobwa/result-0.50.tsv
6029df32ed7484ea0766233fa5465dc98552a8ec598a9253ae9497a0d8dca400  WORKDIR/runs/2026-10-18-0839/attempts/transducer/frozen/PRIMARY/test/0.50/bremerberta/result-0.50.tsv
8502a2f2e0041dfaed9168b2eb141c93e782d950637434dc191f29888d825a62  WORKDIR/runs/2026-10-18-0839/attempts/transducer/frozen/PRIMARY/test/0.50/deepadungpalaung/result-0.50.tsv
13e47d52e91ce2e1a1d4cf00791966f24a4a9e92bb0b79ac9bef59adddfd3af3  WORKDIR/runs/2026-10-18-0839/attempts/transducer/frozen/PRIMARY/test/0.50/hillburmish/result-0.50.tsv
8316b0e0543e658472bfd2e756cd756c7c08a5271f0e3762a30ce270874743d3  WORKDIR/runs/2026-10-18-0839/attempts/transducer/frozen/PRIMARY/test/0.50/kesslersignificance/result-0.50.tsv
977a46cd40173fcd389b772bfe48cd099579b9aff1243c35be4bf6a1f55d3625  WORKDIR/runs/2026-10-18-0839/attempts/transducer/frozen/PRIMARY/test/0.50/luangthongkumkaren/result-0.50.tsv
220ea18e7f3c0c0c5b0c6bab54ea2a61c1b0cb8767f3aa1e450fac3d113d9182  WORKDIR/runs/2026-10-18-0839/attempts/transducer/frozen/PRIMARY/test/0.50/wangbai/result-0.50.tsv
4a9330ff83e084ac6d92b1a185ed2724d75d0c4bc1b05ae3596c10f996bcba02  WORKDIR/runs/2026-10-18-0839/carry/analogist-PRIMARY/val/0.50/bantubvd/result-0.50.tsv
f6ff416362be610e178c96cd07dcf97f6d94cc52dc5be595a2bd2fc3387367b3  WORKDIR/runs/2026-10-18-0839/carry/analogist-PRIMARY/val/0.50/beidazihui/result-0.50.tsv
f22455de8da7167aa91443f8c108ab7118a4c8b466c272ae1839835bc41ce119  WORKDIR/runs/2026-10-18-0839/carry/analogist-PRIMARY/val/0.50/birchallchapacuran/result-0.50.tsv
558cea5ff6873ecf79020dfa2cbbf64e949e2297edc73a19b4a07c48dff174fb  WORKDIR/runs/2026-10-18-0839/carry/analogist-PRIMARY/val/0.50/bodtkhobwa/result-0.50.tsv
c41ea5a4a18e1f64598ce21d2dfdb02d31b4cdb24061d643da054bf9197ee508  WORKDIR/runs/2026-10-18-0839/carry/analogist-PRIMARY/val/0.50/bremerberta/result-0.50.tsv
a1563eab6326a859d4e50e5c11c8e299a6259eae6222b91619b123d5359491d4  WORKDIR/runs/2026-10-18-0839/carry/analogist-PRIMARY/val/0.50/deepadungpalaung/result-0.50.tsv
ca25bf352920bd5b16d74224c060f25dcb40394ed6b92721afdd3155ee6a3cc9  WORKDIR/runs/2026-10-18-0839/carry/analogist-PRIMARY/val/0.50/hillburmish/result-0.50.tsv
4831e5f374bae381005ee53f70f92498cbed717dd998970ffdf805757fc026c6  WORKDIR/runs/2026-10-18-0839/carry/analogist-PRIMARY/val/0.50/kesslersignificance/result-0.50.tsv
70f5517e58726b4f6922d87a7512c8e4369ec0966de7f4f2f45922df6069639a  WORKDIR/runs/2026-10-18-0839/carry/analogist-PRIMARY/val/0.50/luangthongkumkaren/result-0.50.tsv
5f01bccc70c66b8979be14d4881e16a6331b961ec171ff8cbd95a9b1b7abef3b  WORKDIR/runs/2026-10-18-0839/carry/analogist-PRIMARY/val/0.50/wangbai/result-0.50.tsv
95605c9a93ca035f023008642872f1c521ca21ac1635fccbbd3b3fa31d4a93bb  WORKDIR/runs/2026-10-18-0839/carry/analogist-PRIMARY/test/0.50/bantubvd/result-0.50.tsv
482daece635b6bd17e535c2b688f69c635dace5775c8b6cbfef0e5686686f5e8  WORKDIR/runs/2026-10-18-0839/carry/analogist-PRIMARY/test/0.50/beidazihui/result-0.50.tsv
eb33e9f9c01134000d968d0ee6a762fd5039461210c481e8e6ed5ae9210947bc  WORKDIR/runs/2026-10-18-0839/carry/analogist-PRIMARY/test/0.50/birchallchapacuran/result-0.50.tsv
f311cf8d355be02c4abcc2b19da1f5af577cef888beafd02e4d358262f966b54  WORKDIR/runs/2026-10-18-0839/carry/analogist-PRIMARY/test/0.50/bodtkhobwa/result-0.50.tsv
3177aac82c67b983cb11b7a1542f4547e79b644249f3133b3ee843acea75bebf  WORKDIR/runs/2026-10-18-0839/carry/analogist-PRIMARY/test/0.50/bremerberta/result-0.50.tsv
fc4114282f9b0ab10e26eb5946dbfa4f32a0cdeba2dbe5800c30bdf15b40f0a3  WORKDIR/runs/2026-10-18-0839/carry/analogist-PRIMARY/test/0.50/deepadungpalaung/result-0.50.tsv
a5308f528620f3e5b5e0a528fcfe1d5f2873798c43b126721a61909c0fa8b9ea  WORKDIR/runs/2026-10-18-0839/carry/analogist-PRIMARY/test/0.50/hillburmish/result-0.50.tsv
8b58dde66d8133b0d584f8af00a27398b71b33652bf14250f15bd343b18179c6  WORKDIR/runs/2026-10-18-0839/carry/analogist-PRIMARY/test/0.50/kesslersignificance/result-0.50.tsv
b322106b54630e068b89740a4084bd172192c080ae3042613109e2a4cbdebd4d  WORKDIR/runs/2026-10-18-0839/carry/analogist-PRIMARY/test/0.50/luangthongkumkaren/result-0.50.tsv
8ad874949213cdd82f5c7fbf4863f24fde94d9c9888cfa2bc1651312e61d3e61  WORKDIR/runs/2026-10-18-0839/carry/analogist-PRIMARY/test/0.50/wangbai/result-0.50.tsv
efba3ac92c28b0833ce7c5ad7d1613485f190491a4385c8d850893a39fd7430c  WORKDIR/runs/2026-10-18-0839/carry/classifier-PRIMARY/val/0.50/bantubvd/result-0.50.tsv
67cea2eff575e35855dae507683d7486e155418e5d881f76a09fc0c32d349688  WORKDIR/runs/2026-10-18-0839/carry/classifier-PRIMARY/val/0.50/beidazihui/result-0.50.tsv
ec214dfc7e357754c0e9b4c7417bd152c85358b9979917266c05720e1c471803  WORKDIR/runs/2026-10-18-0839/carry/classifier-PRIMARY/val/0.50/birchallchapacuran/result-0.50.tsv
dd5ecfc09d35e2e61e593f58be91125cb1c9ab4d95e7f9c71c572d5805c96f47  WORKDIR/runs/2026-10-18-0839/carry/classifier-PRIMARY/val/0.50/bodtkhobwa/result-0.50.tsv
8dd62221b211ff8ba7b248c5c9316ac8550404ac18a403611538357615b39885  WORKDIR/runs/2026-10-18-0839/carry/classifier-PRIMARY/val/0.50/bremerberta/result-0.50.tsv
a5c84e828b37026766f041976c74c2081815d2d34f9c582a585b1f8266923544  WORKDIR/runs/2026-10-18-0839/carry/classifier-PRIMARY/val/0.50/deepadungpalaung/result-0.50.tsv
e1ee89b71c745e9b2a18ddb681dfd96645cf2ddd85114a330ddb1eb67130c5c9  WORKDIR/runs/2026-10-18-0839/carry/classifier-PRIMARY/val/0.50/hillburmish/result-0.50.tsv
e036ecef1afaeec1b4796abafa5490cde9a055227381ba68f5d168be66d668e2  WORKDIR/runs/2026-10-18-0839/carry/classifier-PRIMARY/val/0.50/kesslersignificance/result-0.50.tsv
d60d6b0bf445ea27301600b9c923890979416c0be37ddd0735442b36fab8da54  WORKDIR/runs/2026-10-18-0839/carry/classifier-PRIMARY/val/0.50/luangthongkumkaren/result-0.50.tsv
0aa4cddfe6b412f35cb761928eb67a065df488bd22199b0e53e66d5fea606b2a  WORKDIR/runs/2026-10-18-0839/carry/classifier-PRIMARY/val/0.50/wangbai/result-0.50.tsv
22c9cc934bdbc1ef54cb04e248220bd2ce38dd73dc45dc1d55bc0af9b4ba238f  WORKDIR/runs/2026-10-18-0839/carry/classifier-PRIMARY/test/0.50/bantubvd/result-0.50.tsv
ecf4c073905910222387ad1c91d7d897ebdd28704a899e594af8adb45d8bcc88  WORKDIR/runs/2026-10-18-0839/carry/classifier-PRIMARY/test/0.50/beidazihui/result-0.50.tsv
4b74fc5fc5203893f91aa07199797bc115ab716f10a34e6a9de51d710b020878  WORKDIR/runs/2026-10-18-0839/carry/classifier-PRIMARY/test/0.50/birchallchapacuran/result-0.50.tsv
8a5617bf50f7f3b39732d193975a40f49bb1df029e84bfed9f660b2659f69db5  WORKDIR/runs/2026-10-18-0839/carry/classifier-PRIMARY/test/0.50/bodtkhobwa/result-0.50.tsv
43ab226c9cc94941009ecaec3e1025eb81f917d923cdbce033b550464504b5bb  WORKDIR/runs/2026-10-18-0839/carry/classifier-PRIMARY/test/0.50/bremerberta/result-0.50.tsv
6d6dad031fd229929cfb26b05925d18ae8374bc9dd03314867bca5a9bbf21772  WORKDIR/runs/2026-10-18-0839/carry/classifier-PRIMARY/test/0.50/deepadungpalaung/result-0.50.tsv
c0e4b82e7ca86bbe27189f2fa74ee38d15bd76a2317ced9ec16b15dd936f9b12  WORKDIR/runs/2026-10-18-0839/carry/classifier-PRIMARY/test/0.50/hillburmish/result-0.50.tsv
add4e16220affc079abaf24bcc12cad2cc5e076bb648a068030724bd595cd4e1  WORKDIR/runs/2026-10-18-0839/carry/classifier-PRIMARY/test/0.50/kesslersignificance/result-0.50.tsv
c198a82b831c2113986fbeeb28bddab994f190ac3756da8ac5a5fe46615d7b91  WORKDIR/runs/2026-10-18-0839/carry/classifier-PRIMARY/test/0.50/luangthongkumkaren/result-0.50.tsv
1b88b2b835958ed2465d0799a86202b46a0f48f49a728f0d986d77d7564cbdca  WORKDIR/runs/2026-10-18-0839/carry/classifier-PRIMARY/test/0.50/wangbai/result-0.50.tsv
e72b85ae70b2be05494fff8ef20d63272568c17f5469ee4ea69c52875b201ab7  WORKDIR/runs/2026-10-18-0839/carry/correspondence-SECONDARY/val/0.50/bantubvd/result-0.50.tsv
458705a33d1ae1dd26000e8d977f7822297a2a3753d379e940cf0a10bcd6e283  WORKDIR/runs/2026-10-18-0839/carry/correspondence-SECONDARY/val/0.50/beidazihui/result-0.50.tsv
9ebcf92b589f1a55be4b98f95102b82ad3221c7df2a0ce95ed83c7986fbce3da  WORKDIR/runs/2026-10-18-0839/carry/correspondence-SECONDARY/val/0.50/birchallchapacuran/result-0.50.tsv
4bc0f6601f25688bec6aed856ac780029940e16788ea20d4ce55bf3da8d8e33f  WORKDIR/runs/2026-10-18-0839/carry/correspondence-SECONDARY/val/0.50/bodtkhobwa/result-0.50.tsv
dc04ea5b1ecea23bb22caf8bd0a669a6169f60ffdd52509587917c98fe500851  WORKDIR/runs/2026-10-18-0839/carry/correspondence-SECONDARY/val/0.50/bremerberta/result-0.50.tsv
29ab7711d50679799a9ad31b0084b80da748e5a163a8770ea34f490cc201ac57  WORKDIR/runs/2026-10-18-0839/carry/correspondence-SECONDARY/val/0.50/deepadungpalaung/result-0.50.tsv
88d057c0ef357c6a5ac2d8432b5fa06bae508f4af9362aaac9d1300839659af3  WORKDIR/runs/2026-10-18-0839/carry/correspondence-SECONDARY/val/0.50/hillburmish/result-0.50.tsv
600a432b560e037ff6331dc59e9103a6e6d1fd13d4d98a0b9fe964ce445dd142  WORKDIR/runs/2026-10-18-0839/carry/correspondence-SECONDARY/val/0.50/kesslersignificance/result-0.50.tsv
0e018a13d8e844ce697b115e994718544621e08d8059f7ac4631ed6492b6c83e  WORKDIR/runs/2026-10-18-0839/carry/correspondence-SECONDARY/val/0.50/luangthongkumkaren/result-0.50.tsv
dc954f85f5d75dc6d1d5363e9ac4795975b2a6194dbb20f980a48c34f8dd5e1d  WORKDIR/runs/2026-10-18-0839/carry/correspondence-SECONDARY/val/0.50/wangbai/result-0.50.tsv
f8aabe12d0e62ff99137e63d0af0135354935ea01934e26bc90bf9938a569ccb  WORKDIR/runs/2026-10-18-0839/carry/correspondence-SECONDARY/test/0.50/bantubvd/result-0.50.tsv
45f245b3c46b001d0662a22ee9c97998ab6f5431302be44fddc77bad44e4479a  WORKDIR/runs/2026-10-18-0839/carry/correspondence-SECONDARY/test/0.50/beidazihui/result-0.50.tsv
790075d88cd1fd7643ff772faac9f13e8fb9e1439178cf8ae01e1cd9fe04b309  WORKDIR/runs/2026-10-18-0839/carry/correspondence-SECONDARY/test/0.50/birchallchapacuran/result-0.50.tsv
524ec29b8f0310e6e2034f7279cd97398e7583997bc68ae19c64d364691ca0a5  WORKDIR/runs/2026-10-18-0839/carry/correspondence-SECONDARY/test/0.50/bodtkhobwa/result-0.50.tsv
23fe0e61cb354762764c319910af2416a73694f1da500fb83a9b4539aa5211c5  WORKDIR/runs/2026-10-18-0839/carry/correspondence-SECONDARY/test/0.50/bremerberta/result-0.50.tsv
335d809073fe6ab5e28749fb930836a095a3ed1cf94cd51ac6a400b01de5ed87  WORKDIR/runs/2026-10-18-0839/carry/correspondence-SECONDARY/test/0.50/deepadungpalaung/result-0.50.tsv
33399ea5ccc01813be47b31c49fed8c7e81bf3317ce9b71563062fcd6d13ebc8  WORKDIR/runs/2026-10-18-0839/carry/correspondence-SECONDARY/test/0.50/hillburmish/result-0.50.tsv
fbe86505f86694abcffec94b9a073bfe0f5199b3c82bb250bd3e0af9f0b2e1bc  WORKDIR/runs/2026-10-18-0839/carry/correspondence-SECONDARY/test/0.50/kesslersignificance/result-0.50.tsv
b7c85b87f74dd941e05b6e0997f33dfa9b6023702e6600a632e2c1b16ee02a54  WORKDIR/runs/2026-10-18-0839/carry/correspondence-SECONDARY/test/0.50/luangthongkumkaren/result-0.50.tsv
7f41b95bf05476e840c604e4596fe148afaf685b8f508905d6e675d1c2525262  WORKDIR/runs/2026-10-18-0839/carry/correspondence-SECONDARY/test/0.50/wangbai/result-0.50.tsv
e72b85ae70b2be05494fff8ef20d63272568c17f5469ee4ea69c52875b201ab7  WORKDIR/runs/2026-10-18-0839/carry/correspondence-PRIMARY/val/0.50/bantubvd/result-0.50.tsv
d2d89e5aa44ab7d3b35a7ef3af0bbead3414b003323ca3f3a66cc8206e9984d7  WORKDIR/runs/2026-10-18-0839/carry/correspondence-PRIMARY/val/0.50/beidazihui/result-0.50.tsv
c600f5a0ef5dcb6f4aef6bfff904256d479cd20e9b7285a032b9312b2b95cb54  WORKDIR/runs/2026-10-18-0839/carry/correspondence-PRIMARY/val/0.50/birchallchapacuran/result-0.50.tsv
7691ede702c7167cbff2ccff0cd36ae1d24eb4dbff210361c96ec7e69c5411d3  WORKDIR/runs/2026-10-18-0839/carry/correspondence-PRIMARY/val/0.50/bodtkhobwa/result-0.50.tsv
dc04ea5b1ecea23bb22caf8bd0a669a6169f60ffdd52509587917c98fe500851  WORKDIR/runs/2026-10-18-0839/carry/correspondence-PRIMARY/val/0.50/bremerberta/result-0.50.tsv
962263d411176f3bd94d36c135b89c5c54b342cc1fa60a8729d6b20594e801e3  WORKDIR/runs/2026-10-18-0839/carry/correspondence-PRIMARY/val/0.50/deepadungpalaung/result-0.50.tsv
76995ddd74d68f7a01f121ebe268623775a4ff8ddfee46d5ad724c9af671780c  WORKDIR/runs/2026-10-18-0839/carry/correspondence-PRIMARY/val/0.50/hillburmish/result-0.50.tsv
39e67048f06b58f2992d4fbbdccc1c94a9ae2b12fe76f033b2be2e58ec06a778  WORKDIR/runs/2026-10-18-0839/carry/correspondence-PRIMARY/val/0.50/kesslersignificance/result-0.50.tsv
221b04d0b0aa586b053e2d6647dd7a229e64926fe06dd5ac61729a3c6225c7dd  WORKDIR/runs/2026-10-18-0839/carry/correspondence-PRIMARY/val/0.50/luangthongkumkaren/result-0.50.tsv
9eabdb633376416407f8a68050427b0d10f07b1861e4346ee89e7c0cee822c92  WORKDIR/runs/2026-10-18-0839/carry/correspondence-PRIMARY/val/0.50/wangbai/result-0.50.tsv
6af911655c992a74b171791784a950ed148f007024470bee1a7f727d1de8dd09  WORKDIR/runs/2026-10-18-0839/carry/correspondence-PRIMARY/test/0.50/bantubvd/result-0.50.tsv
f2ac0d1faf3afc08930e13c5d068add0437dca7006aefc9f1cfaf7005f032402  WORKDIR/runs/2026-10-18-0839/carry/correspondence-PRIMARY/test/0.50/beidazihui/result-0.50.tsv
ff849d3f07ad37d10136b26acc57e65b4a7971cb1ca06df27ea37fb0ddd3f939  WORKDIR/runs/2026-10-18-0839/carry/correspondence-PRIMARY/test/0.50/birchallchapacuran/result-0.50.tsv
1628abf738fc110b1fc32893088a6ef798212a2f5779206bada7027c1038f6ec  WORKDIR/runs/2026-10-18-0839/carry/correspondence-PRIMARY/test/0.50/bodtkhobwa/result-0.50.tsv
8b68b8b26fb58f7c70dbb9f3ddb15af1b67d8e2d3a86c77eb5627450d45d79db  WORKDIR/runs/2026-10-18-0839/carry/correspondence-PRIMARY/test/0.50/bremerberta/result-0.50.tsv
b153e531ff21213f361c7a44d63ecb8c7acf932303e08794a19ec27c30ce1732  WORKDIR/runs/2026-10-18-0839/carry/correspondence-PRIMARY/test/0.50/deepadungpalaung/result-0.50.tsv
ffdf963e3ad0c8c130137e9b813af299fa0875bdbdccdef177ba77da6b75ec70  WORKDIR/runs/2026-10-18-0839/carry/correspondence-PRIMARY/test/0.50/hillburmish/result-0.50.tsv
26fca4265140c992b37f17b37ffde54eecd4c6a7f84fbb5e1ba1663791032442  WORKDIR/runs/2026-10-18-0839/carry/correspondence-PRIMARY/test/0.50/kesslersignificance/result-0.50.tsv
90e8030a6c9f8df3878b2c6fe5242fd828999a2f7836ab4eb333bcb2c8b03506  WORKDIR/runs/2026-10-18-0839/carry/correspondence-PRIMARY/test/0.50/luangthongkumkaren/result-0.50.tsv
92317f7984081b1b7308efd8c44500459053a729cf7fd36063c7fb5c5aa33be0  WORKDIR/runs/2026-10-18-0839/carry/correspondence-PRIMARY/test/0.50/wangbai/result-0.50.tsv
279227377db0ebaa2a19114cc4832ca6c7932ab68c98968c0904a751361e49a2  WORKDIR/runs/2026-10-18-0839/carry/classifier-SECONDARY/val/0.50/bantubvd/result-0.50.tsv
0e9afa9f151cfedc6161ccd5d816024c5f9c51d599a4e56fcdff5691b0389136  WORKDIR/runs/2026-10-18-0839/carry/classifier-SECONDARY/val/0.50/beidazihui/result-0.50.tsv
91faaf0f3ab4989cf870e3adbbf465baee6b908b83c8b07629f17b22bd66f3be  WORKDIR/runs/2026-10-18-0839/carry/classifier-SECONDARY/val/0.50/birchallchapacuran/result-0.50.tsv
d279ebbd996b36ac7209e20ac853ba0d52c9ed7c1a4264800a62a211de5dddcc  WORKDIR/runs/2026-10-18-0839/carry/classifier-SECONDARY/val/0.50/bodtkhobwa/result-0.50.tsv
1b2cc0360129d0ee25a69dd48c9889eddd5d9d6131a2e559601916178e67c838  WORKDIR/runs/2026-10-18-0839/carry/classifier-SECONDARY/val/0.50/bremerberta/result-0.50.tsv
bc5235b7beb0bf5e1fd9dd127dbad313d9d61cabb90b77bbb0d27f77510db3aa  WORKDIR/runs/2026-10-18-0839/carry/classifier-SECONDARY/val/0.50/deepadungpalaung/result-0.50.tsv
45881fb236eed054c713ed93b31280e31c147777aa78f3516ed612aa53b46ce6  WORKDIR/runs/2026-10-18-0839/carry/classifier-SECONDARY/val/0.50/hillburmish/result-0.50.tsv
724098cab700d071a7b92b0c1893a3449ee55fb66527178985d423b205b2e05e  WORKDIR/runs/2026-10-18-0839/carry/classifier-SECONDARY/val/0.50/kesslersignificance/result-0.50.tsv
09607d58539164525515b772b0178ae76ca9ff5ef1405c5d3c2b6a8f8a2b5394  WORKDIR/runs/2026-10-18-0839/carry/classifier-SECONDARY/val/0.50/luangthongkumkaren/result-0.50.tsv
4f0dd3a58afaacb53f02bbc23a3d69dcc872519697fc04e6dee62393235e20c4  WORKDIR/runs/2026-10-18-0839/carry/classifier-SECONDARY/val/0.50/wangbai/result-0.50.tsv
741673a4fa60f45a798848c99ac37e62ecd7f18f95f52cbcc47f39ead6d45e6f  WORKDIR/runs/2026-10-18-0839/carry/classifier-SECONDARY/test/0.50/bantubvd/result-0.50.tsv
465324d1808c291938c7d77783f75480dc060f500d2d67240b3d1b22ec59a956  WORKDIR/runs/2026-10-18-0839/carry/classifier-SECONDARY/test/0.50/beidazihui/result-0.50.tsv
4ec21b30c326f0f31fbee078da4dffc00411439e1e0feb613928fad3dd0a45df  WORKDIR/runs/2026-10-18-0839/carry/classifier-SECONDARY/test/0.50/birchallchapacuran/result-0.50.tsv
900b1edee8dd973dd90d4c0815a4585310bcf24e828a36187846e63faf0de458  WORKDIR/runs/2026-10-18-0839/carry/classifier-SECONDARY/test/0.50/bodtkhobwa/result-0.50.tsv
6620b441117b23b3b56548b5db97c3812da1cd453f50140f75e9802169d30eb8  WORKDIR/runs/2026-10-18-0839/carry/classifier-SECONDARY/test/0.50/bremerberta/result-0.50.tsv
f6465267c7d05de0f937f9a14efce2a173b2d481da6364546bdd2ec0ba076201  WORKDIR/runs/2026-10-18-0839/carry/classifier-SECONDARY/test/0.50/deepadungpalaung/result-0.50.tsv
257b6b7920815d97ca3287bf2deb42310c4a412fe40b378490852bc34ffa58ff  WORKDIR/runs/2026-10-18-0839/carry/classifier-SECONDARY/test/0.50/hillburmish/result-0.50.tsv
c17d1247df5f364000c484c02bc85b96058c1f7b944556b2cf28e568968d5145  WORKDIR/runs/2026-10-18-0839/carry/classifier-SECONDARY/test/0.50/kesslersignificance/result-0.50.tsv
70f213c6159a8abb2949820a999f542aa4b8f1cb074104a5b7c79026a1988f32  WORKDIR/runs/2026-10-18-0839/carry/classifier-SECONDARY/test/0.50/luangthongkumkaren/result-0.50.tsv
6b1e4296f460e428b7cdfe4a2a6db5bf9b114497ef72dfb3b238ae8086a81f06  WORKDIR/runs/2026-10-18-0839/carry/classifier-SECONDARY/test/0.50/wangbai/result-0.50.tsv
88caef598d87927ef751bf9bf8e07c8db84c6fd572b7d8783a139f96e9882451  WORKDIR/runs/2026-10-18-0839/carry/transducer-SECONDARY/val/0.50/bantubvd/result-0.50.tsv
aa88c651d8ca4efa9c765b3a4223d1d0dd33651bc5726fe2a46984568e9ef90d  WORKDIR/runs/2026-10-18-0839/carry/transducer-SECONDARY/val/0.50/beidazihui/result-0.50.tsv
23322061ed704696daa953bcdab2e95f02aeaafc8e9902e445e7ff0d15478e9c  WORKDIR/runs/2026-10-18-0839/carry/transducer-SECONDARY/val/0.50/birchallchapacuran/result-0.50.tsv
3f74775009570dc5b56f1433074ad3d25964daebc7023ec08d4b6a1690215798  WORKDIR/runs/2026-10-18-0839/carry/transducer-SECONDARY/val/0.50/bodtkhobwa/result-0.50.tsv
18aca7cf590913609f0b764d54708dee8ad6f35c039f647c8ca06296505f63d0  WORKDIR/runs/2026-10-18-0839/carry/transducer-SECONDARY/val/0.50/bremerberta/result-0.50.tsv
5e6723e1e7d485799542320b23697a82d05a60894f77b147bc340935a4447425  WORKDIR/runs/2026-10-18-0839/carry/transducer-SECONDARY/val/0.50/deepadungpalaung/result-0.50.tsv
b92ea2cb1cda22dabd3ba392bb41301c0b0d1f1e3cf9b315c1194608407f1ed6  WORKDIR/runs/2026-10-18-0839/carry/transducer-SECONDARY/val/0.50/hillburmish/result-0.50.tsv
eed30bdccdf73fd40d6ecd614e7e066662d7838f0f16b39a4d926d1b97aa784e  WORKDIR/runs/2026-10-18-0839/carry/transducer-SECONDARY/val/0.50/kesslersignificance/result-0.50.tsv
f415ee13a4c84f5813f9b1d57302b024fa739816b1ea6c87a51eae359b8b2c71  WORKDIR/runs/2026-10-18-0839/carry/transducer-SECONDARY/val/0.50/luangthongkumkaren/result-0.50.tsv
d7d62027b85ace2843d727e9ecd7d8cb54d164a32fec3bc3e478a6d1a2ed00e6  WORKDIR/runs/2026-10-18-0839/carry/transducer-SECONDARY/val/0.50/wangbai/result-0.50.tsv
d874340aa7a8871e0a5ff3efcdfbc1bae3bcc9688e66b73ba77bf00a3bdc60cf  WORKDIR/runs/2026-10-18-0839/carry/transducer-SECONDARY/test/0.50/bantubvd/result-0.50.tsv
ef7beff4fa9e054c47ab4366302ad0028ff886ecc7138043401e0bea38d64986  WORKDIR/runs/2026-10-18-0839/carry/transducer-SECONDARY/test/0.50/beidazihui/result-0.50.tsv
93391a524c3f4c57ad60b7d72b0187dc7daab7f038d5cf485cbf2e387f924e69  WORKDIR/runs/2026-10-18-0839/carry/transducer-SECONDARY/test/0.50/birchallchapacuran/result-0.50.tsv
a591894a504577d03b5023e82a8db6f3aa94443f675aba423ebcb7e9652ff3e9  WORKDIR/runs/2026-10-18-0839/carry/transducer-SECONDARY/test/0.50/bodtkhobwa/result-0.50.tsv
910d658791ca5faf05f9532a83a581aa1c7b6435051a07a6ff9fd9a72c82dcf3  WORKDIR/runs/2026-10-18-0839/carry/transducer-SECONDARY/test/0.50/bremerberta/result-0.50.tsv
ccf1d61e825f724b6ea9436c122415bd38720889a49461e0201ec3225ef09699  WORKDIR/runs/2026-10-18-0839/carry/transducer-SECONDARY/test/0.50/deepadungpalaung/result-0.50.tsv
8fb34e9e740c4fe85965bfa084183d13892494880021ef47cfdedc7c2e268d16  WORKDIR/runs/2026-10-18-0839/carry/transducer-SECONDARY/test/0.50/hillburmish/result-0.50.tsv
072cd356350b22fe3ff035fbb29a9f3731b13fc27e7e353c3af048d8c389d45c  WORKDIR/runs/2026-10-18-0839/carry/transducer-SECONDARY/test/0.50/kesslersignificance/result-0.50.tsv
a1d3073f64e6e468710a587868fbc77cdb2da6b980ea747aaa7070e889d7966e  WORKDIR/runs/2026-10-18-0839/carry/transducer-SECONDARY/test/0.50/luangthongkumkaren/result-0.50.tsv
3c9b61748e48f1cbb11343ea177341546a333714fb02ca700f4d0fe77b1235f4  WORKDIR/runs/2026-10-18-0839/carry/transducer-SECONDARY/test/0.50/wangbai/result-0.50.tsv
88caef598d87927ef751bf9bf8e07c8db84c6fd572b7d8783a139f96e9882451  WORKDIR/runs/2026-10-18-0839/carry/transducer-PRIMARY/val/0.50/bantubvd/result-0.50.tsv
b0ab7f6cc4f2f468c19ee5b2743f74a3e853fd2d3c198c8bfefb3bd5fe07c5ea  WORKDIR/runs/2026-10-18-0839/carry/transducer-PRIMARY/val/0.50/beidazihui/result-0.50.tsv
1b7685b0d03458e31a8b0d02056f3e5d8341bf550da5055a81bc54ea2b160b6b  WORKDIR/runs/2026-10-18-0839/carry/transducer-PRIMARY/val/0.50/birchallchapacuran/result-0.50.tsv
da7b9def6cba14e095f6dfb6dfbb32a00c7aa088d9837e7b947685d1d18068f8  WORKDIR/runs/2026-10-18-0839/carry/transducer-PRIMARY/val/0.50/bodtkhobwa/result-0.50.tsv
d321ebb9cc3f7ce66fab39ee3dc781392e12dab43edcfcf24c43064c7864d2c3  WORKDIR/runs/2026-10-18-0839/carry/transducer-PRIMARY/val/0.50/bremerberta/result-0.50.tsv
e333c85d96b57d3e4ffc6a27ecf0d8c44dfbbbbac47821694f832430a64e9701  WORKDIR/runs/2026-10-18-0839/carry/transducer-PRIMARY/val/0.50/deepadungpalaung/result-0.50.tsv
c92d783842dcd3d143d62f0f2d45cece2bb3a69208458172e79b005748ae88d7  WORKDIR/runs/2026-10-18-0839/carry/transducer-PRIMARY/val/0.50/hillburmish/result-0.50.tsv
eed30bdccdf73fd40d6ecd614e7e066662d7838f0f16b39a4d926d1b97aa784e  WORKDIR/runs/2026-10-18-0839/carry/transducer-PRIMARY/val/0.50/kesslersignificance/result-0.50.tsv
f5c63c95fb2cb57f803653d20c349a1fd0792bd3f24cc8fbbb202b6c8f76657d  WORKDIR/runs/2026-10-18-0839/carry/transducer-PRIMARY/val/0.50/luangthongkumkaren/result-0.50.tsv
c829f070b2a1334224f2b4bc80f59e45ef5fa8d075081c4d43b800679180f80e  WORKDIR/runs/2026-10-18-0839/carry/transducer-PRIMARY/val/0.50/wangbai/result-0.50.tsv
88e8608ae7717c9ce2e9d5ad2e9d263491772d7a3bd554f750cdf13dd4e33a50  WORKDIR/runs/2026-10-18-0839/carry/transducer-PRIMARY/test/0.50/bantubvd/result-0.50.tsv
948eea925da39f962f6ce90d1176fdf370a134c6591e9d8d493e18b27ea79e19  WORKDIR/runs/2026-10-18-0839/carry/transducer-PRIMARY/test/0.50/beidazihui/result-0.50.tsv
0371e53937cf8d4b86b91cd7db84b93e30e2cddc88689013901fe3af1fef04f9  WORKDIR/runs/2026-10-18-0839/carry/transducer-PRIMARY/test/0.50/birchallchapacuran/result-0.50.tsv
f77b6a107c3965645370fb4893b6bcf9593351707a4e6bc28ea1b6b1c6eac7b7  WORKDIR/runs/2026-10-18-0839/carry/transducer-PRIMARY/test/0.50/bodtkhobwa/result-0.50.tsv
0727c5ed607d1f3597f7d49c680434d3a60a4b0926880ddc66d8a8ddd4e9c6f0  WORKDIR/runs/2026-10-18-0839/carry/transducer-PRIMARY/test/0.50/bremerberta/result-0.50.tsv
612bd79ea822f677a03c963e64130efe53da665104ca388427b2b489013bdf13  WORKDIR/runs/2026-10-18-0839/carry/transducer-PRIMARY/test/0.50/deepadungpalaung/result-0.50.tsv
ce17895b7eb9401abdfc880417cd8e68a72c4d0b7d968a2d38d44f1cccdc9d74  WORKDIR/runs/2026-10-18-0839/carry/transducer-PRIMARY/test/0.50/hillburmish/result-0.50.tsv
072cd356350b22fe3ff035fbb29a9f3731b13fc27e7e353c3af048d8c389d45c  WORKDIR/runs/2026-10-18-0839/carry/transducer-PRIMARY/test/0.50/kesslersignificance/result-0.50.tsv
51facf10d7a32b8706c35738acaf9ff2b4a79d3d5f6177cce5335ae9fb9b7afc  WORKDIR/runs/2026-10-18-0839/carry/transducer-PRIMARY/test/0.50/luangthongkumkaren/result-0.50.tsv
33f0f7c9316cfc2a729442562039d05bbb46af40ae9244ff7695890e13d4feeb  WORKDIR/runs/2026-10-18-0839/carry/transducer-PRIMARY/test/0.50/wangbai/result-0.50.tsv
a9665d86100c4e9120b87270fb89f3a44ed70e92792c768f3cecdf2eb85398c2  WORKDIR/runs/2026-10-18-0839/out/comb6/val/0.50/bantubvd/result-0.50.tsv
d8377ba5127ae0912b20a071b6657ebcb5c361ec174ac737969cc4ffea58764e  WORKDIR/runs/2026-10-18-0839/out/comb6/val/0.50/beidazihui/result-0.50.tsv
d57e62912a994de4d1f60703306c573649fd0821ab2460954c0d7511c5c57d7c  WORKDIR/runs/2026-10-18-0839/out/comb6/val/0.50/birchallchapacuran/result-0.50.tsv
468f6b85d88bb585b92ec910d30b02fffda551a785ebb4d6aabb43ada532faf3  WORKDIR/runs/2026-10-18-0839/out/comb6/val/0.50/bodtkhobwa/result-0.50.tsv
2f6be0dd0f787ae9f35e4f04df4ddfdcd3390b3533c181dcc515d15b42bcd2f8  WORKDIR/runs/2026-10-18-0839/out/comb6/val/0.50/bremerberta/result-0.50.tsv
2ce7f6d9a111c4a94230e2f946f99e012f0d03d807d6c4cd25cb1c8e49d28d41  WORKDIR/runs/2026-10-18-0839/out/comb6/val/0.50/deepadungpalaung/result-0.50.tsv
4ad180c02da7c3b17e73f87a58be4a11d39977850f15d2f019badb7f925fee01  WORKDIR/runs/2026-10-18-0839/out/comb6/val/0.50/hillburmish/result-0.50.tsv
a65d589878c94c2d8037876054d7d86c76dcd8066429aab8c473e767e34e3716  WORKDIR/runs/2026-10-18-0839/out/comb6/val/0.50/kesslersignificance/result-0.50.tsv
59c82dfcee8d196db3a28c8b3448f8b59199fef1f5f76a6a1f910db7244a1db3  WORKDIR/runs/2026-10-18-0839/out/comb6/val/0.50/luangthongkumkaren/result-0.50.tsv
36f8236266db7ab90556b2a5aa2888a8e487fb6d1d7fd23a9d19c2469bf60a37  WORKDIR/runs/2026-10-18-0839/out/comb6/val/0.50/wangbai/result-0.50.tsv
dfb39897aacf7d87d390b552973863f0430573b20df91fd98425e8096bd65358  WORKDIR/runs/2026-10-18-0839/out/comb6/test/0.50/bantubvd/result-0.50.tsv
c7527771d021531dd296acee57331d249a5d2acaa7a4a5e000b0dbac9b4e2341  WORKDIR/runs/2026-10-18-0839/out/comb6/test/0.50/beidazihui/result-0.50.tsv
6bce8ff88c48f2ba38efc0174dfcf92212c4f73560e8a106f96c3f786197e8f2  WORKDIR/runs/2026-10-18-0839/out/comb6/test/0.50/birchallchapacuran/result-0.50.tsv
c22809fb89aaf4ea78e6c1405a3c1bd51c7293abd828b1f4a88ab1018cd9bf33  WORKDIR/runs/2026-10-18-0839/out/comb6/test/0.50/bodtkhobwa/result-0.50.tsv
1bb2e0e2dfdec4b6412db32d7c77795453fa807c8e5e9a2d25f770d83808c928  WORKDIR/runs/2026-10-18-0839/out/comb6/test/0.50/bremerberta/result-0.50.tsv
b143ad97681f7d017f195d78b887501c6c03f1d8e43d1638f3efede6a08d69cd  WORKDIR/runs/2026-10-18-0839/out/comb6/test/0.50/deepadungpalaung/result-0.50.tsv
e9fbf74c4eb9f9d94b643f09d151f1a09f39a916aa2c2055b85119f33aaa9063  WORKDIR/runs/2026-10-18-0839/out/comb6/test/0.50/hillburmish/result-0.50.tsv
b3c00d23019a184173f0437d8e3cc878e2bcb58e70cb8031f23c5604ccce698c  WORKDIR/runs/2026-10-18-0839/out/comb6/test/0.50/kesslersignificance/result-0.50.tsv
7f24a7cf17fae5eb2ae531e98ed594ee4585180433ab2ea96768fa38348e6871  WORKDIR/runs/2026-10-18-0839/out/comb6/test/0.50/luangthongkumkaren/result-0.50.tsv
093b398d75c2ed24ec31f777157790690e3fdccd212ebc7342ccf1d1efd8356a  WORKDIR/runs/2026-10-18-0839/out/comb6/test/0.50/wangbai/result-0.50.tsv
f13d0c4566978421d6e1bdcb0274b9d3e45700f2016df0410aec815c481ea25c  WORKDIR/runs/2026-10-18-0839/out/comb8/val/0.50/bantubvd/result-0.50.tsv
43b74705fdb9b58b3bb203c63a689bc85a510f3a0ef30afddc781db138104dd5  WORKDIR/runs/2026-10-18-0839/out/comb8/val/0.50/beidazihui/result-0.50.tsv
036bd8607c081d4816f18d474a0ca42fba260e1af61242b37f3607d45d23d3ef  WORKDIR/runs/2026-10-18-0839/out/comb8/val/0.50/birchallchapacuran/result-0.50.tsv
566dda9b3a4c792bfb84d9716d40ea90c84c73004b1d3bf606fe8969918fc3b2  WORKDIR/runs/2026-10-18-0839/out/comb8/val/0.50/bodtkhobwa/result-0.50.tsv
77c1b00269a0ae049ef2399c27924b12a000a97c7d4cf41dabe956442abfa5fa  WORKDIR/runs/2026-10-18-0839/out/comb8/val/0.50/bremerberta/result-0.50.tsv
4c2a945edda46ebdf3f1b661fa05b1e023ef320b5c6e26cfa38628c680ec02f4  WORKDIR/runs/2026-10-18-0839/out/comb8/val/0.50/deepadungpalaung/result-0.50.tsv
71699328f642f7bb3278f591850e5cde35508a6f7a1f5d17b16c027f15f36a24  WORKDIR/runs/2026-10-18-0839/out/comb8/val/0.50/hillburmish/result-0.50.tsv
a802e7bbe8e558e2bbce373af23f357fdc10d3f53cf496be3dc98f286c8b5c4f  WORKDIR/runs/2026-10-18-0839/out/comb8/val/0.50/kesslersignificance/result-0.50.tsv
aa48ac1b6f993c1fb87a3e8e9517d59000654ee99fb7ceded39f4286d234dc7b  WORKDIR/runs/2026-10-18-0839/out/comb8/val/0.50/luangthongkumkaren/result-0.50.tsv
8b9a599040136113be9a99b98c8b6ced2eb66a884e836fd73fc6c4c5daaff7b2  WORKDIR/runs/2026-10-18-0839/out/comb8/val/0.50/wangbai/result-0.50.tsv
0463946121fe8515d80370660c7f353ee1d810cd8cab24b00ff931ce5408b2a1  WORKDIR/runs/2026-10-18-0839/out/comb8/test/0.50/bantubvd/result-0.50.tsv
9944fed1c09941a70d3c0392d6755fa3e7b2c4642801da86656a5f95aea25990  WORKDIR/runs/2026-10-18-0839/out/comb8/test/0.50/beidazihui/result-0.50.tsv
74492b033f5ee99c6ab92aae279eee40d0362451c01506ffa7660480052bebf8  WORKDIR/runs/2026-10-18-0839/out/comb8/test/0.50/birchallchapacuran/result-0.50.tsv
2ec935c8049cdc2519a1fd84e97a2726c6f1cce4f8907774cfa9fbc0fd3c574a  WORKDIR/runs/2026-10-18-0839/out/comb8/test/0.50/bodtkhobwa/result-0.50.tsv
ea8706f42a426cf34b8560bc3a7cb117fd4bae05d2db768fe2694314905d0933  WORKDIR/runs/2026-10-18-0839/out/comb8/test/0.50/bremerberta/result-0.50.tsv
a115b687fd3dfa37e5a3169f2f0989a91597f89543f96a26124a86c06dbc5ceb  WORKDIR/runs/2026-10-18-0839/out/comb8/test/0.50/deepadungpalaung/result-0.50.tsv
6ba9bfcb851b550f3e42ea76e07566cfbd1f25eb47481c5e05f20c4f37d9c0f4  WORKDIR/runs/2026-10-18-0839/out/comb8/test/0.50/hillburmish/result-0.50.tsv
03482611ff381dd58789cb468ddc7e179777c91955e496605bb32880cb78fc20  WORKDIR/runs/2026-10-18-0839/out/comb8/test/0.50/kesslersignificance/result-0.50.tsv
094830c2700c6f665c5695eef80ce5ca0e0db8d5bba35d1e2208c82824d0692d  WORKDIR/runs/2026-10-18-0839/out/comb8/test/0.50/luangthongkumkaren/result-0.50.tsv
7da40223d54805b18131096de2228c170fc679ea3c7668f4ed7ba7f7978fc0a2  WORKDIR/runs/2026-10-18-0839/out/comb8/test/0.50/wangbai/result-0.50.tsv
```

