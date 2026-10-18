# Selection (PREREG rules 8-10), session 2026-10-18-1758 (cells N40, B40, L40 and NA, BA, LA)

Written by the main session (Opus 5.5) at 2026-10-18T21:16:09Z (date -u), before any surprise-test gold has been read in this session (no score_test, null test or other gold-reading tool has run in this session).

## Inputs
- Lenses: all seven lens subagents of this session had returned by 2026-10-18T21:10:30Z (the smuggler, second wave, last); no lens process was alive; every freeze record below was written before the 21:50:00Z deadline (latest: smuggler/PRIMARY 21:05:45Z). Transducer froze nothing.
- Eligibility (rule 8): tools/check_freezes_040.py, output out/frozen_entries.json and out/frozen_entries.md (out/check_freezes_040.out): 29 eligible entries, 8 new (classifier/PRIMARY, broker/PRIMARY, classifier/SECONDARY, analogist/PRIMARY, phylo/PRIMARY, correspondence/PRIMARY, correspondence/SECONDARY, smuggler/PRIMARY) and 21 carried, every one with code and result hashes matching its record and AUDIT PASS at 0.40.
- Ranking (rule 9): tools/rank_040.py on val-0.50 (official scorer; out/ranking_040.md; no NED ties).
- Stage 2 (rule 9): tools/stage2x.py (weights fit on val-0.50; LOFO val; test at 0.40 with the all-10 weights): out/comb6, out/comb8, out/comb10 (logs out/stage2_comb6.log, -8, -10). Weights fit on all 10 val families: COMB-6 [2, 2, 2, 1, 3, 2]; COMB-8 [2, 2, 2, 2, 1, 2, 1, 3]; COMB-10 [2, 2, 2, 2, 1, 2, 1, 3, 0, 0].

## Rule 10 table (singles: their frozen val-0.50 files; combinations: LOFO val files) and the candidate

| order | candidate | kind | val NED | val ED | val BCFS | val BLEU | stage2 cross-check |
|---|---|---|---|---|---|---|---|
| 1 | classifier/PRIMARY | single | 0.26631878067630127 | 1.1139670176922158 | 0.835625 | 0.619474 | - |
| 2 | broker/PRIMARY | single | 0.2692807965192631 | 1.1082314695879794 | 0.839804 | 0.613962 | - |
| 3 | classifier/SECONDARY | single | 0.2702343133887876 | 1.1354684307976552 | 0.834599 | 0.614706 | - |
| 4 | COMB-6 | combination | 0.2707859930173011 | 1.1237131309576867 | 0.837534 | 0.613401 | equal |
| 5 | r0839-broker/PRIMARY | single | 0.27104726508767685 | 1.117791906917987 | 0.838784 | 0.613038 | - |
| 6 | r0839-classifier/SECONDARY | single | 0.2725097701028512 | 1.128038409920328 | 0.827111 | 0.610258 | - |
| 7 | COMB-8 | combination | 0.2726853997296398 | 1.1331039348427467 | 0.835279 | 0.610026 | equal |
| 8 | COMB-10 | combination | 0.2735025293592694 | 1.1394928237316357 | 0.834657 | 0.608832 | equal |
| 9 | r0839-broker/SECONDARY | single | 0.2758653182632716 | 1.1334852460916984 | 0.836111 | 0.606632 | - |
| 10 | r0202-broker/PRIMARY | single | 0.2780802108388158 | 1.1477916922461475 | 0.834398 | 0.604617 | - |
| 11 | r0839-classifier/PRIMARY | single | 0.27837673041473154 | 1.161272579828635 | 0.829200 | 0.600519 | - |
| 12 | analogist/PRIMARY | single | 0.27900621947674104 | 1.1567333624053817 | 0.832735 | 0.601517 | - |
| 13 | r0839-analogist/PRIMARY | single | 0.28029406101885673 | 1.1650546666433073 | 0.834868 | 0.597583 | - |
| 14 | phylo/PRIMARY | single | 0.28050636001379203 | 1.1558240739651149 | 0.826457 | 0.601693 | - |
| 15 | r0839-phylo/PRIMARY | single | 0.28276039319290625 | 1.1611120467101628 | 0.826779 | 0.597321 | - |
| 16 | correspondence/PRIMARY | single | 0.28343379170112615 | 1.1686215353680711 | 0.835903 | 0.597794 | - |
| 17 | r0202-analogist/SECONDARY | single | 0.2837348172878465 | 1.175079234323396 | 0.830884 | 0.594652 | - |
| 18 | r0202-broker/SECONDARY | single | 0.28376005998455833 | 1.170875140721858 | 0.830790 | 0.598693 | - |
| 19 | r0839-phylo/SECONDARY | single | 0.2839042876857526 | 1.169513641152215 | 0.828204 | 0.594517 | - |
| 20 | correspondence/SECONDARY | single | 0.28412388965963753 | 1.1806287189934512 | 0.837420 | 0.598061 | - |
| 21 | r0202-phylo/PRIMARY | single | 0.2845922609747311 | 1.1711511863949315 | 0.825222 | 0.594452 | - |
| 22 | r0839-correspondence/PRIMARY | single | 0.2847322616079229 | 1.176680746387501 | 0.836742 | 0.594518 | - |
| 23 | r0839-correspondence/SECONDARY | single | 0.2863260093056118 | 1.2057281228928776 | 0.830835 | 0.594151 | - |
| 24 | r0839-transducer/PRIMARY | single | 0.2874055706582019 | 1.1618469873541448 | 0.824465 | 0.593378 | - |
| 25 | r0202-analogist/PRIMARY | single | 0.2885706072901764 | 1.1991531400959292 | 0.827976 | 0.587319 | - |
| 26 | r0202-classifier/PRIMARY | single | 0.2896033417663429 | 1.2036210646771197 | 0.824118 | 0.587502 | - |
| 27 | r0202-correspondence/SECONDARY | single | 0.2908258046195304 | 1.2046294002508686 | 0.831236 | 0.591447 | - |
| 28 | r0202-correspondence/PRIMARY | single | 0.2913077560369119 | 1.2028531717085433 | 0.830716 | 0.589349 | - |
| 29 | r0202-classifier/SECONDARY | single | 0.2947015906669862 | 1.2295829504220965 | 0.818691 | 0.582488 | - |
| 30 | smuggler/PRIMARY | single | 0.29549880646903076 | 1.213312611547503 | 0.820405 | 0.585637 | - |
| 31 | r0202-transducer/SECONDARY | single | 0.29843657939584967 | 1.169373958759764 | 0.815307 | 0.583818 | - |
| 32 | r0202-transducer/PRIMARY | single | 0.3033229092509786 | 1.1881544782320603 | 0.812167 | 0.577373 | - |

CANDIDATE (rule 10): classifier/PRIMARY (single), val-0.50 mean NED 0.26631878067630127

The rule picks the single entry classifier/PRIMARY (frozen 2026-10-18T19:14:05Z): its frozen val-0.50 mean NED 0.26631878067630127 is the lowest of every eligible single entry and of COMB-6 (0.2707859930173011), COMB-8 (0.2726853997296398) and COMB-10 (0.2735025293592694). The main session applied the rule as written, without discretion.
Notes for the panel (disclosed, not a reason to deviate from the rule): (1) classifier/PRIMARY reads development-family rows for two surprise families (mannburmish rows for hillburmish, listsamplesize English/German/French rows for kesslersignificance; inherited from run 2026-10-18-0839's classifier, permitted by PREREG rules 4 and 6). (2) Its lens report says the per-family gate of its reranker was written after per-family val numbers of the ungated reranker were visible (ungated val 0.2722; the gate follows the lens's own fold deltas); its val number may therefore be optimistic; combinations are scored LOFO. The PREREG compares singles and combinations on val as stated.

## The candidate's object for each cell
- N40, B40, L40: classifier/PRIMARY's frozen test-0.40 predictions (attempts/classifier/frozen/PRIMARY/test/0.40/FAM/result-0.40.tsv; byte copies in newent/classifier-PRIMARY/test/0.40/, verified against the freeze record by code/setup_new.py).
- NA, BA, LA: classifier/PRIMARY at every P: test-0.40 as above, and the main session's test runs of the same frozen code (newent/classifier-PRIMARY/code, code tree hash 4880a9cd6f2bd892ecdc2008277bb78f7fe5435c1cd2415183b12f2ebb993051) at 0.10, 0.20, 0.30, 0.50 (newent/classifier-PRIMARY/test/P/), each with its test-mode audit at P.
- Rule 12 (iii) therefore concerns one entry: classifier/PRIMARY (audit at 0.40 and, for the aggregate, at every P; sealed check at 0.40 and, for the aggregate, at every P).

## sha256 of freeze records, of every eligible entry's val-0.50 and test-0.40 result files, and of the COMB outputs

```
1310b14a27896e86804e4cd600ebe9dbab4eb91c2aa260c11c777ce4d5376ae0  WORKDIR/runs/2026-10-18-1758/attempts/classifier/FROZEN.md  (freeze record of classifier)
5b2dfc409a24fe92411762dcb87a0fafd5bdee351f4b683a960249bbea830880  WORKDIR/runs/2026-10-18-1758/attempts/broker/FROZEN.md  (freeze record of broker)
ee19d511f28edddb7dee00ac7412baaef3503de3c4bf7901b73f9aa7b0b3294b  WORKDIR/runs/2026-10-18-0839/attempts/broker/FROZEN.md  (freeze record of r0839-broker)
fdc52d8bb7b34165b441c70001f1f5e45950382aec8fa2d2aa4de903622bc3c3  WORKDIR/runs/2026-10-18-0839/attempts/classifier/FROZEN.md  (freeze record of r0839-classifier)
d41dd287245ade644c9b101d867da3c0bf7c0bd8e63bb7aaddd050e837d36071  WORKDIR/runs/2026-10-18-0202/attempts/broker/FROZEN.md  (freeze record of r0202-broker)
786d043fe727f5d2d62caab59d8c0c78b9d8b7e236f28e620eee1c7f70fbed2b  WORKDIR/runs/2026-10-18-1758/attempts/analogist/FROZEN.md  (freeze record of analogist)
a6bb14c4636ca63ea06f0dd3ee274edf4066f736445f7ee8c63053129dc1a68a  WORKDIR/runs/2026-10-18-0839/attempts/analogist/FROZEN.md  (freeze record of r0839-analogist)
566ab6105ce992bf107d274dd1185a9976a183e332d04b1954715f71fcae7099  WORKDIR/runs/2026-10-18-1758/attempts/phylo/FROZEN.md  (freeze record of phylo)
e6588445159ebfe255a513a2c1df3b3613b46952733fe7778b799f631e144829  WORKDIR/runs/2026-10-18-0839/attempts/phylo/FROZEN.md  (freeze record of r0839-phylo)
eda73c8671a1c2732068a7d615593ce47e77817bdb826240cc2cdb26a52abcbc  WORKDIR/runs/2026-10-18-1758/attempts/correspondence/FROZEN.md  (freeze record of correspondence)
c8b4cf2cf8cdfea760c5e8b5225e63597d86b36876f0757a27c110c636e24e63  WORKDIR/runs/2026-10-18-0202/attempts/analogist/FROZEN.md  (freeze record of r0202-analogist)
32b2829e22d9b2eabec2a9e5495995a43ffa58f6156e9a418c65e8ea88e0aaf6  WORKDIR/runs/2026-10-18-0202/attempts/phylo/FROZEN.md  (freeze record of r0202-phylo)
a76f26a1355f048ab59cc857ced36b127b98d0f0b2f93e8e69f03db8bfb736c5  WORKDIR/runs/2026-10-18-0839/attempts/correspondence/FROZEN.md  (freeze record of r0839-correspondence)
797d7a3e355455037efe3b2a0f575a0bfd0420ddce50e1bc999dc26363392202  WORKDIR/runs/2026-10-18-0839/attempts/transducer/FROZEN.md  (freeze record of r0839-transducer)
df50a06e0f9d9e0b2c01e0f01fda8d4f207b8651439fa80e00fadd558d6935cd  WORKDIR/runs/2026-10-18-0202/attempts/classifier/FROZEN.md  (freeze record of r0202-classifier)
cdb370ddc0d2fbf1d510bfbe6bc068fcfd02d88bc1e8c27508e55fb97178eac6  WORKDIR/runs/2026-10-18-0202/attempts/correspondence/FROZEN.md  (freeze record of r0202-correspondence)
c042aadaab84f508f389dba96b78235156716e0e2902dff3423b878b0d517fdc  WORKDIR/runs/2026-10-18-1758/attempts/smuggler/FROZEN.md  (freeze record of smuggler)
4fb0ee28b20c7ec71524268bccefced87efc3e9964e7c66a4e927d3918bfcd91  WORKDIR/runs/2026-10-18-0202/attempts/transducer/FROZEN.md  (freeze record of r0202-transducer)
efba3ac92c28b0833ce7c5ad7d1613485f190491a4385c8d850893a39fd7430c  WORKDIR/runs/2026-10-18-1758/newent/classifier-PRIMARY/val/0.50/bantubvd/result-0.50.tsv
67cea2eff575e35855dae507683d7486e155418e5d881f76a09fc0c32d349688  WORKDIR/runs/2026-10-18-1758/newent/classifier-PRIMARY/val/0.50/beidazihui/result-0.50.tsv
6ee155ff756714372d476e135ca1d90e7651a29b35550c0d27c21afa55a42594  WORKDIR/runs/2026-10-18-1758/newent/classifier-PRIMARY/val/0.50/birchallchapacuran/result-0.50.tsv
d2757e45808ec5c0da986a4fa4d95e12163bea6b90b56373e686b72a8a3f6b66  WORKDIR/runs/2026-10-18-1758/newent/classifier-PRIMARY/val/0.50/bodtkhobwa/result-0.50.tsv
a6fcb0b37f218a0ff4119dd894912acb488f1f03d22ffae2c89edbfd160488f8  WORKDIR/runs/2026-10-18-1758/newent/classifier-PRIMARY/val/0.50/bremerberta/result-0.50.tsv
f6c7d362ff346a698db6ccf92d00ae87b89455e2c9a19f8eb427722f73e465db  WORKDIR/runs/2026-10-18-1758/newent/classifier-PRIMARY/val/0.50/deepadungpalaung/result-0.50.tsv
3644a6c9eb8512cb847006e60968aa48ce7998a0bee10c5f082da97334079f1f  WORKDIR/runs/2026-10-18-1758/newent/classifier-PRIMARY/val/0.50/hillburmish/result-0.50.tsv
c19c20d4cf6326ae37e27d1712b8c431bf67b1a2ee4b706b6bd96cf165b0a76c  WORKDIR/runs/2026-10-18-1758/newent/classifier-PRIMARY/val/0.50/kesslersignificance/result-0.50.tsv
af3ce78103f858c8c3bba952e54260a0ae5a313e4acb651f3062a1f16eed9296  WORKDIR/runs/2026-10-18-1758/newent/classifier-PRIMARY/val/0.50/luangthongkumkaren/result-0.50.tsv
1dff982d7976392a472eaac85e03e7269c6d3371ff18536cf8c2694afc70c00b  WORKDIR/runs/2026-10-18-1758/newent/classifier-PRIMARY/val/0.50/wangbai/result-0.50.tsv
cbf74c9d5562246ed0b6334bffff11e3110432b136bc4b791ef2f75b6c0eedd0  WORKDIR/runs/2026-10-18-1758/newent/classifier-PRIMARY/test/0.40/bantubvd/result-0.40.tsv
096c896ef22e806cab60db5346925328f219d95cb40ec2ddfe67b0ffc701efbf  WORKDIR/runs/2026-10-18-1758/newent/classifier-PRIMARY/test/0.40/beidazihui/result-0.40.tsv
d82e290ed3a0a8339296bfcc058c8b83a97d06a5e85c841843aeded890281ced  WORKDIR/runs/2026-10-18-1758/newent/classifier-PRIMARY/test/0.40/birchallchapacuran/result-0.40.tsv
804f2df8637d20c4ed10f42ccf99a862b28b5c4930d9ae203ab869b446cec51f  WORKDIR/runs/2026-10-18-1758/newent/classifier-PRIMARY/test/0.40/bodtkhobwa/result-0.40.tsv
7122207b75a26d21c1188a84c3c6b39e919cd2ec0da58b0fed6dc3e3470fffb3  WORKDIR/runs/2026-10-18-1758/newent/classifier-PRIMARY/test/0.40/bremerberta/result-0.40.tsv
df842a55cd8ce8805f6be53d4b30c4dc80e2ded16882f5f29b66842834c84da3  WORKDIR/runs/2026-10-18-1758/newent/classifier-PRIMARY/test/0.40/deepadungpalaung/result-0.40.tsv
ea8df80b485f7ec04571209f092bb363bcff9cdab7f2ebb59c1047f515016123  WORKDIR/runs/2026-10-18-1758/newent/classifier-PRIMARY/test/0.40/hillburmish/result-0.40.tsv
b98771950df9a71c476ef07bae0f59bff4bdefa01f13a0d37432f84a3d44209e  WORKDIR/runs/2026-10-18-1758/newent/classifier-PRIMARY/test/0.40/kesslersignificance/result-0.40.tsv
71c83295ca2e79d44c79647090c7791739afeb2932848b62479769a7537ba644  WORKDIR/runs/2026-10-18-1758/newent/classifier-PRIMARY/test/0.40/luangthongkumkaren/result-0.40.tsv
b3c23443788bb3e86affd45f137ecb00799dec3c4968d432b4d2f311fd07f943  WORKDIR/runs/2026-10-18-1758/newent/classifier-PRIMARY/test/0.40/wangbai/result-0.40.tsv
1e8bd3f856db7a2944d79d1f78ce9004a4028bbfe374fa6d3fa32deff32df3f5  WORKDIR/runs/2026-10-18-1758/newent/broker-PRIMARY/val/0.50/bantubvd/result-0.50.tsv
116643a94f97052a3dc284ee3962403012bd24495dd67cf2fd1bff5b34234a36  WORKDIR/runs/2026-10-18-1758/newent/broker-PRIMARY/val/0.50/beidazihui/result-0.50.tsv
089f2bab6c7871fd2bf2885a5cd2cde413d066aee7763968100fc9f0940aa66d  WORKDIR/runs/2026-10-18-1758/newent/broker-PRIMARY/val/0.50/birchallchapacuran/result-0.50.tsv
02d8531bd02ff46d3d4fd89bc21f776986cbecd7ee44f41eeb871c78fc1807db  WORKDIR/runs/2026-10-18-1758/newent/broker-PRIMARY/val/0.50/bodtkhobwa/result-0.50.tsv
49c0729eed74ef7227e74ca911830992a7f9cd62df554fd800bc968e8d0d3691  WORKDIR/runs/2026-10-18-1758/newent/broker-PRIMARY/val/0.50/bremerberta/result-0.50.tsv
47d36e1a4cca27797766e2d580fa79d0f3a138dc5f3c3ddb68fd4995352a203d  WORKDIR/runs/2026-10-18-1758/newent/broker-PRIMARY/val/0.50/deepadungpalaung/result-0.50.tsv
9b8fc104130313a0f0bc8d76e291fafd12b5ee31bbcfbdd0fa1aa245e1141eef  WORKDIR/runs/2026-10-18-1758/newent/broker-PRIMARY/val/0.50/hillburmish/result-0.50.tsv
a614b0f771e6622f96f3ecc1c63b9ebd7c2bc852b136c028f6a9e702017c8b89  WORKDIR/runs/2026-10-18-1758/newent/broker-PRIMARY/val/0.50/kesslersignificance/result-0.50.tsv
e1dd82337fbfff51f15e5e24f8303a8804cc93cf30beefa398e95cfcdd9ca22c  WORKDIR/runs/2026-10-18-1758/newent/broker-PRIMARY/val/0.50/luangthongkumkaren/result-0.50.tsv
18f9b96262a16c2a56ab293ca72c6a2b28593790250396a45fb9ae8eda8ffdbc  WORKDIR/runs/2026-10-18-1758/newent/broker-PRIMARY/val/0.50/wangbai/result-0.50.tsv
a66c0670b83c3d8e3e6f24118911858ed345e6ce4d5476468585a388fecb12a5  WORKDIR/runs/2026-10-18-1758/newent/broker-PRIMARY/test/0.40/bantubvd/result-0.40.tsv
a758286234e74176dc2f2e959c526f467e3a70a722f6d1cd9c65fb7fc8bf85ce  WORKDIR/runs/2026-10-18-1758/newent/broker-PRIMARY/test/0.40/beidazihui/result-0.40.tsv
933979ad6c106e7edc2099bc6ec6b6fb03a02f55307139c23fac06831c0c7354  WORKDIR/runs/2026-10-18-1758/newent/broker-PRIMARY/test/0.40/birchallchapacuran/result-0.40.tsv
b408a10959fec3487bfbc2db50ab69e69126baefa59ed51fcad993e7c1d16662  WORKDIR/runs/2026-10-18-1758/newent/broker-PRIMARY/test/0.40/bodtkhobwa/result-0.40.tsv
2fa8c26c875a070225ef43273a76ce284a9aec68d2049afebc6217a47360ca61  WORKDIR/runs/2026-10-18-1758/newent/broker-PRIMARY/test/0.40/bremerberta/result-0.40.tsv
0cac6e65055115b4f7914a490d30bf16e51dfa06762249f73ed1f378aeee6b07  WORKDIR/runs/2026-10-18-1758/newent/broker-PRIMARY/test/0.40/deepadungpalaung/result-0.40.tsv
ff2009d92824f22a5e1f0f8d4c032466f05a9476e3fa1a2625f1da2fdfda0c5f  WORKDIR/runs/2026-10-18-1758/newent/broker-PRIMARY/test/0.40/hillburmish/result-0.40.tsv
69456dfc1b14aebd3ad1d5b76930e1625689d20c7915f96f8fc74e6e25fae566  WORKDIR/runs/2026-10-18-1758/newent/broker-PRIMARY/test/0.40/kesslersignificance/result-0.40.tsv
701fe5b14a70b8b6a0a49a2cf17236d52e5fbd4011c50caccf4c01d54d328e50  WORKDIR/runs/2026-10-18-1758/newent/broker-PRIMARY/test/0.40/luangthongkumkaren/result-0.40.tsv
eeddf2b441ef0362ff1d8a017d62fa31188c8b7300d2526b9ba633efb008c713  WORKDIR/runs/2026-10-18-1758/newent/broker-PRIMARY/test/0.40/wangbai/result-0.40.tsv
efba3ac92c28b0833ce7c5ad7d1613485f190491a4385c8d850893a39fd7430c  WORKDIR/runs/2026-10-18-1758/newent/classifier-SECONDARY/val/0.50/bantubvd/result-0.50.tsv
67cea2eff575e35855dae507683d7486e155418e5d881f76a09fc0c32d349688  WORKDIR/runs/2026-10-18-1758/newent/classifier-SECONDARY/val/0.50/beidazihui/result-0.50.tsv
42ef016dcd09fa3079eaab958d80b7fbb039d44ae971687d2b767f76629ed622  WORKDIR/runs/2026-10-18-1758/newent/classifier-SECONDARY/val/0.50/birchallchapacuran/result-0.50.tsv
510b2f94bd93b5d26fa37c566f39f0b6953af2543adcfb84f45acd4d8ae6f563  WORKDIR/runs/2026-10-18-1758/newent/classifier-SECONDARY/val/0.50/bodtkhobwa/result-0.50.tsv
e12ac3cb6e2208a03c6dc318e477a113fc5d423687c7a7c6a1b8367e5da8cc20  WORKDIR/runs/2026-10-18-1758/newent/classifier-SECONDARY/val/0.50/bremerberta/result-0.50.tsv
f4aa16dbe562ef5fc01216e7b2fc407069f188dab678bc7c5a9cd478fe4fabb2  WORKDIR/runs/2026-10-18-1758/newent/classifier-SECONDARY/val/0.50/deepadungpalaung/result-0.50.tsv
66734db13fde9c10c5b2bad1b49858cf88b2e8c26fc36f2f08d43b642f9653d9  WORKDIR/runs/2026-10-18-1758/newent/classifier-SECONDARY/val/0.50/hillburmish/result-0.50.tsv
c19c20d4cf6326ae37e27d1712b8c431bf67b1a2ee4b706b6bd96cf165b0a76c  WORKDIR/runs/2026-10-18-1758/newent/classifier-SECONDARY/val/0.50/kesslersignificance/result-0.50.tsv
78b48ea5872548dcf0fe7e308ba5d93d46ea72cbf961c10084078e6de313f36f  WORKDIR/runs/2026-10-18-1758/newent/classifier-SECONDARY/val/0.50/luangthongkumkaren/result-0.50.tsv
76a1742343f120ed4152cdbd6c0e628ab4a45c1292f37cafd88ba0176b9d326a  WORKDIR/runs/2026-10-18-1758/newent/classifier-SECONDARY/val/0.50/wangbai/result-0.50.tsv
cbf74c9d5562246ed0b6334bffff11e3110432b136bc4b791ef2f75b6c0eedd0  WORKDIR/runs/2026-10-18-1758/newent/classifier-SECONDARY/test/0.40/bantubvd/result-0.40.tsv
096c896ef22e806cab60db5346925328f219d95cb40ec2ddfe67b0ffc701efbf  WORKDIR/runs/2026-10-18-1758/newent/classifier-SECONDARY/test/0.40/beidazihui/result-0.40.tsv
16d803ea25306c3f8e2f81f54918a3c0285fb35ab7539c1c8f409295fea46681  WORKDIR/runs/2026-10-18-1758/newent/classifier-SECONDARY/test/0.40/birchallchapacuran/result-0.40.tsv
b7f2c1b4c6cfb8e8ac32a79fbb5e4b6bac92f600acc37e20e21633945598a349  WORKDIR/runs/2026-10-18-1758/newent/classifier-SECONDARY/test/0.40/bodtkhobwa/result-0.40.tsv
46956b8947e2c6d506d13b21a0a2342ec20d67a8c0f978593e97e5ed390c4102  WORKDIR/runs/2026-10-18-1758/newent/classifier-SECONDARY/test/0.40/bremerberta/result-0.40.tsv
8a70e9b09dc1c95347924fbbba54261929350242a4179daea5ef05a76538c73b  WORKDIR/runs/2026-10-18-1758/newent/classifier-SECONDARY/test/0.40/deepadungpalaung/result-0.40.tsv
69d4bc0fdfd7db641e3c04a38b200e90c0c90ce9bbd02eaee2697ac01ceb0c67  WORKDIR/runs/2026-10-18-1758/newent/classifier-SECONDARY/test/0.40/hillburmish/result-0.40.tsv
b98771950df9a71c476ef07bae0f59bff4bdefa01f13a0d37432f84a3d44209e  WORKDIR/runs/2026-10-18-1758/newent/classifier-SECONDARY/test/0.40/kesslersignificance/result-0.40.tsv
0dcfc9f07ddc3f5dff96c2dc9b65d3f168061100e3ddff54a0b4e56afc06ffc1  WORKDIR/runs/2026-10-18-1758/newent/classifier-SECONDARY/test/0.40/luangthongkumkaren/result-0.40.tsv
1e69f5a05afd4ad368dab454c2a93f15a124edf98b9b67c7f688e7fbbf0c79c5  WORKDIR/runs/2026-10-18-1758/newent/classifier-SECONDARY/test/0.40/wangbai/result-0.40.tsv
1e8bd3f856db7a2944d79d1f78ce9004a4028bbfe374fa6d3fa32deff32df3f5  WORKDIR/runs/2026-10-18-1758/carry/r0839-broker-PRIMARY/val/0.50/bantubvd/result-0.50.tsv
1d5b7807128f44a7ba05ae1f4fba81ba7eb71f04b13f087c6b8facc318006497  WORKDIR/runs/2026-10-18-1758/carry/r0839-broker-PRIMARY/val/0.50/beidazihui/result-0.50.tsv
089f2bab6c7871fd2bf2885a5cd2cde413d066aee7763968100fc9f0940aa66d  WORKDIR/runs/2026-10-18-1758/carry/r0839-broker-PRIMARY/val/0.50/birchallchapacuran/result-0.50.tsv
a64023f8eb1941dae9457dd253c7fdbcfe7a5b732ed54c25818377a0588c2e06  WORKDIR/runs/2026-10-18-1758/carry/r0839-broker-PRIMARY/val/0.50/bodtkhobwa/result-0.50.tsv
59c912441702dea2d183ccd767b4cce4f07bd38b8d8d671d31f8c44675ddce83  WORKDIR/runs/2026-10-18-1758/carry/r0839-broker-PRIMARY/val/0.50/bremerberta/result-0.50.tsv
9af7da3043c1389f16bddbc16e1a3cc58da8440962ef67f04aa667f8618dcdc6  WORKDIR/runs/2026-10-18-1758/carry/r0839-broker-PRIMARY/val/0.50/deepadungpalaung/result-0.50.tsv
7b89494592da18fe940bec5c3b3da7fbc369e1b0d99ce78a1d35a728eb25aaf5  WORKDIR/runs/2026-10-18-1758/carry/r0839-broker-PRIMARY/val/0.50/hillburmish/result-0.50.tsv
580d7f5813657fd79d74b732ff333865396e403d9d43e10676593a0461825d49  WORKDIR/runs/2026-10-18-1758/carry/r0839-broker-PRIMARY/val/0.50/kesslersignificance/result-0.50.tsv
961ba14554832453e78690d9aabd0f19aab79d544cfbc996281b065aefd1b266  WORKDIR/runs/2026-10-18-1758/carry/r0839-broker-PRIMARY/val/0.50/luangthongkumkaren/result-0.50.tsv
6ca1628b76f16de3ca96129629e19f9801cc9673b6cb428d003fd15aac11e819  WORKDIR/runs/2026-10-18-1758/carry/r0839-broker-PRIMARY/val/0.50/wangbai/result-0.50.tsv
bc7d1ee6e92cf2f3337b6a8bd2b39acbb966dd9567786444e575432f3d08e3e7  WORKDIR/runs/2026-10-18-1758/carry/r0839-broker-PRIMARY/test/0.40/bantubvd/result-0.40.tsv
a758286234e74176dc2f2e959c526f467e3a70a722f6d1cd9c65fb7fc8bf85ce  WORKDIR/runs/2026-10-18-1758/carry/r0839-broker-PRIMARY/test/0.40/beidazihui/result-0.40.tsv
6441d7b0cafe2fde7b20a64952fc8e5e9f95b2a8815fbcfe34cb00206b4f9354  WORKDIR/runs/2026-10-18-1758/carry/r0839-broker-PRIMARY/test/0.40/birchallchapacuran/result-0.40.tsv
f5368baee0e1b7f19b1cdc9fc222b57c345bbefd9773c9cca0821a4ce9da4364  WORKDIR/runs/2026-10-18-1758/carry/r0839-broker-PRIMARY/test/0.40/bodtkhobwa/result-0.40.tsv
368e498c427c93f0e17ebd5b00a3d5943dcc64df73b9e5bf41d4f4ea527ba527  WORKDIR/runs/2026-10-18-1758/carry/r0839-broker-PRIMARY/test/0.40/bremerberta/result-0.40.tsv
caeda3d9787d58e6bb7207120267684180177788aa0b8a447b06a3d43df8d6c3  WORKDIR/runs/2026-10-18-1758/carry/r0839-broker-PRIMARY/test/0.40/deepadungpalaung/result-0.40.tsv
a3927a5c69c389dc33ccc357f014d4103265fe194be3f2162a29c978bd95860a  WORKDIR/runs/2026-10-18-1758/carry/r0839-broker-PRIMARY/test/0.40/hillburmish/result-0.40.tsv
d9b44831e14f1d4cf0075d36c17d41b897c50412e6435e9492fe5ab67e3a6b78  WORKDIR/runs/2026-10-18-1758/carry/r0839-broker-PRIMARY/test/0.40/kesslersignificance/result-0.40.tsv
97a57ac84325ad039c618a2d0b30082fb321ae1ad5b378e5a2817d4f81826ec7  WORKDIR/runs/2026-10-18-1758/carry/r0839-broker-PRIMARY/test/0.40/luangthongkumkaren/result-0.40.tsv
7237bbf6c2cc9d404cd8cb8ae61618d604b8ed061799fe943a3fd3bcdf4c1b51  WORKDIR/runs/2026-10-18-1758/carry/r0839-broker-PRIMARY/test/0.40/wangbai/result-0.40.tsv
2fb9d04eff0eca06c6f254621ecc4a4f9417244ef3473def4a3e691667c25831  WORKDIR/runs/2026-10-18-1758/carry/r0839-classifier-SECONDARY/val/0.50/bantubvd/result-0.50.tsv
b4f3cf5599a80374091f14252ff225f38589c99670597e2b0861d77cb924c8c1  WORKDIR/runs/2026-10-18-1758/carry/r0839-classifier-SECONDARY/val/0.50/beidazihui/result-0.50.tsv
00cb9a4f65060c3b23d1b09d4821b1dca7b544eff7c86301100775245ab9e9e5  WORKDIR/runs/2026-10-18-1758/carry/r0839-classifier-SECONDARY/val/0.50/birchallchapacuran/result-0.50.tsv
da138b5ea464d9fb752446073b86c9646aa827e4b6850f15337b066840f8f1ae  WORKDIR/runs/2026-10-18-1758/carry/r0839-classifier-SECONDARY/val/0.50/bodtkhobwa/result-0.50.tsv
1b6ea3e3601501ba9dec49588642a1cb7944b81ae373c1b394d679e52a01314a  WORKDIR/runs/2026-10-18-1758/carry/r0839-classifier-SECONDARY/val/0.50/bremerberta/result-0.50.tsv
b5334769030ded817834f2cdd1857f59e5e6fd42a5b8b1fb5673cc9e72db0791  WORKDIR/runs/2026-10-18-1758/carry/r0839-classifier-SECONDARY/val/0.50/deepadungpalaung/result-0.50.tsv
2ad34f805e6d660bbc91295f178241f8392afeec30cbfda5726d7bc128a79b14  WORKDIR/runs/2026-10-18-1758/carry/r0839-classifier-SECONDARY/val/0.50/hillburmish/result-0.50.tsv
f2651efaca9fdcf9fba5b4b8362b770445c70dc20f3f1f3fa1c1cc65beda4f66  WORKDIR/runs/2026-10-18-1758/carry/r0839-classifier-SECONDARY/val/0.50/kesslersignificance/result-0.50.tsv
1a45f9938ad160e9cba3be84b39d920f53d09d0404e4dad3c2154e8541d29e6d  WORKDIR/runs/2026-10-18-1758/carry/r0839-classifier-SECONDARY/val/0.50/luangthongkumkaren/result-0.50.tsv
b1a5e9c2a46dde7d61e8ce55b97d1a7dbddbb6338a447ce7bd20fec901b79fe1  WORKDIR/runs/2026-10-18-1758/carry/r0839-classifier-SECONDARY/val/0.50/wangbai/result-0.50.tsv
15dfb614f04d5d557fb8d9cd7613f00ae39b15453d2d4cc3347324644b4c373a  WORKDIR/runs/2026-10-18-1758/carry/r0839-classifier-SECONDARY/test/0.40/bantubvd/result-0.40.tsv
074a7c2d152b07bd58955c51dbaa70bc3d0bb318e61060019e2530f01c0091a3  WORKDIR/runs/2026-10-18-1758/carry/r0839-classifier-SECONDARY/test/0.40/beidazihui/result-0.40.tsv
70a5709f2373b091515255e2fd9f1c24a76876a778cb73a23c45b53c9ac5af15  WORKDIR/runs/2026-10-18-1758/carry/r0839-classifier-SECONDARY/test/0.40/birchallchapacuran/result-0.40.tsv
42a92f4776ff8045d01555e4d6cc18eb0f01f186ecbad40684db409a470a3ded  WORKDIR/runs/2026-10-18-1758/carry/r0839-classifier-SECONDARY/test/0.40/bodtkhobwa/result-0.40.tsv
50f8b659563435e32097ec16dd48b66682466826df5bef32bd70c99b5857851e  WORKDIR/runs/2026-10-18-1758/carry/r0839-classifier-SECONDARY/test/0.40/bremerberta/result-0.40.tsv
ecab9d32c742729e3a4531e969cda82a0fe6b90d477f41e00dfbf258858419c9  WORKDIR/runs/2026-10-18-1758/carry/r0839-classifier-SECONDARY/test/0.40/deepadungpalaung/result-0.40.tsv
e2c71065b821e8cccb25f4085780616e1e8d508a5bcddf64fa1521fbd3c14aa1  WORKDIR/runs/2026-10-18-1758/carry/r0839-classifier-SECONDARY/test/0.40/hillburmish/result-0.40.tsv
5d3391c43c04a75286576ca2f404b4f6deebb1e004f508e2d590d6a1f5ea6ec3  WORKDIR/runs/2026-10-18-1758/carry/r0839-classifier-SECONDARY/test/0.40/kesslersignificance/result-0.40.tsv
dd43ecbf4af8373899ee56f6b1a4e0e028eeb29982bcb6d5407e861ba45eda36  WORKDIR/runs/2026-10-18-1758/carry/r0839-classifier-SECONDARY/test/0.40/luangthongkumkaren/result-0.40.tsv
6425a0c335ac61985f1433b92b797037a962dea8208dd41552eeeef1db7bb44b  WORKDIR/runs/2026-10-18-1758/carry/r0839-classifier-SECONDARY/test/0.40/wangbai/result-0.40.tsv
33719d84f7023b41f9effcdbcce284f7636580321b8cc47d6c2663553e93f74a  WORKDIR/runs/2026-10-18-1758/carry/r0839-broker-SECONDARY/val/0.50/bantubvd/result-0.50.tsv
6f69547c77985bf1ae0db9413228114db6c8e3e8a77ba13302512af1032b48b8  WORKDIR/runs/2026-10-18-1758/carry/r0839-broker-SECONDARY/val/0.50/beidazihui/result-0.50.tsv
7c0670d0bce90d29b2c58510d781d6e7fe10e4d2bc6cd890a00ead9e7e6b2fa2  WORKDIR/runs/2026-10-18-1758/carry/r0839-broker-SECONDARY/val/0.50/birchallchapacuran/result-0.50.tsv
ad043e091d49de057d66abf299b79fada41ef66e08d5afe75192bf182c10cb15  WORKDIR/runs/2026-10-18-1758/carry/r0839-broker-SECONDARY/val/0.50/bodtkhobwa/result-0.50.tsv
e52d5e6f1d0041e4bd8014da7dbb24b134a3c13e4e0fd4bc0d369bb52475b0c1  WORKDIR/runs/2026-10-18-1758/carry/r0839-broker-SECONDARY/val/0.50/bremerberta/result-0.50.tsv
f4d85a14a4fcf809e6a6002584905bac5fc091218862c7b6d34be9695311d0b6  WORKDIR/runs/2026-10-18-1758/carry/r0839-broker-SECONDARY/val/0.50/deepadungpalaung/result-0.50.tsv
05c3c23bada0dc4834cbf4d49f61f79497626a914138a681257633016406f7e0  WORKDIR/runs/2026-10-18-1758/carry/r0839-broker-SECONDARY/val/0.50/hillburmish/result-0.50.tsv
b3b7c0a0a520196ec21a97c8ab9c12afd05d2d4fdb343b8088910ce157e23401  WORKDIR/runs/2026-10-18-1758/carry/r0839-broker-SECONDARY/val/0.50/kesslersignificance/result-0.50.tsv
834d2938feb69394a0cab694498205f07032a644fd124f72a47985cf16426ecb  WORKDIR/runs/2026-10-18-1758/carry/r0839-broker-SECONDARY/val/0.50/luangthongkumkaren/result-0.50.tsv
ac428e8dc1645efb43774c69588f967fd8960d9287dff17663f817dd26f4ed47  WORKDIR/runs/2026-10-18-1758/carry/r0839-broker-SECONDARY/val/0.50/wangbai/result-0.50.tsv
e3c7b3f169c091fc8e63cec673a69d1fe206a5a3598d6022855acb631c51859c  WORKDIR/runs/2026-10-18-1758/carry/r0839-broker-SECONDARY/test/0.40/bantubvd/result-0.40.tsv
c7d9a2ab1386f7e35ad20726d4b8c3eefc30ee5be7cd2565f6f43d331e372d8a  WORKDIR/runs/2026-10-18-1758/carry/r0839-broker-SECONDARY/test/0.40/beidazihui/result-0.40.tsv
e368ad1bb30735aa07f030341f548df673df7a6c25623b05b7f6231760cdcfed  WORKDIR/runs/2026-10-18-1758/carry/r0839-broker-SECONDARY/test/0.40/birchallchapacuran/result-0.40.tsv
7d590e9edc770786a9350e6da1bc3d4f2dd7f1531649a89d216934497061c5e0  WORKDIR/runs/2026-10-18-1758/carry/r0839-broker-SECONDARY/test/0.40/bodtkhobwa/result-0.40.tsv
d192c3a4e25f9bf55d9e8ef354261de11650aa0a2f1c4dd3bc6c5ac23f5e562f  WORKDIR/runs/2026-10-18-1758/carry/r0839-broker-SECONDARY/test/0.40/bremerberta/result-0.40.tsv
e80375ecd723f2b302f5e743a333961f8c0f57fe72725c5effb0ef90ec82c4bf  WORKDIR/runs/2026-10-18-1758/carry/r0839-broker-SECONDARY/test/0.40/deepadungpalaung/result-0.40.tsv
d0f79008db62c81cea60b614640407f71db6930b33b48c60bf1ff214be1b5ff4  WORKDIR/runs/2026-10-18-1758/carry/r0839-broker-SECONDARY/test/0.40/hillburmish/result-0.40.tsv
94baf8fbf304fb28cdfa6ea315d857fed2d6134de509e33c66c8ef39f90c529d  WORKDIR/runs/2026-10-18-1758/carry/r0839-broker-SECONDARY/test/0.40/kesslersignificance/result-0.40.tsv
635ac2985681dbe496b10c19f6d35e70c3e3db990a5fe3cd0fff0bd54612626a  WORKDIR/runs/2026-10-18-1758/carry/r0839-broker-SECONDARY/test/0.40/luangthongkumkaren/result-0.40.tsv
6cf9cfe9af31f17939e99b21c2275ee09ebd3b5f570d07c5b619b1bc7b46d50d  WORKDIR/runs/2026-10-18-1758/carry/r0839-broker-SECONDARY/test/0.40/wangbai/result-0.40.tsv
0def15f60ff5a5ffd44f2dfe21e3a603851c387b100664cfd6f1692952574d81  WORKDIR/runs/2026-10-18-1758/carry/r0202-broker-PRIMARY/val/0.50/bantubvd/result-0.50.tsv
97ab36f9cd2d5c2983a583989f1963d3294c7791f4c1eda659651024580fbcac  WORKDIR/runs/2026-10-18-1758/carry/r0202-broker-PRIMARY/val/0.50/beidazihui/result-0.50.tsv
00529e31ed59e3da1c466db7614d29909fa80cebec6dd97c75d5b6bee66eb0c2  WORKDIR/runs/2026-10-18-1758/carry/r0202-broker-PRIMARY/val/0.50/birchallchapacuran/result-0.50.tsv
83d63daa6c890694a715bbeff626471b6dbdd1d57d186a2cc6698b3958cc99eb  WORKDIR/runs/2026-10-18-1758/carry/r0202-broker-PRIMARY/val/0.50/bodtkhobwa/result-0.50.tsv
347e6f961cd1a143789451bdf96f547ee4e94545327bc87a8305a78ab2e14624  WORKDIR/runs/2026-10-18-1758/carry/r0202-broker-PRIMARY/val/0.50/bremerberta/result-0.50.tsv
127115e9179abce00ce30bbd69b29e40c10e54363cd9647012e2bef1fedf98a8  WORKDIR/runs/2026-10-18-1758/carry/r0202-broker-PRIMARY/val/0.50/deepadungpalaung/result-0.50.tsv
733621b30912e26ebbabf6174c3d86842bce7881f3c4fdd97ffb0a49c3ae30bb  WORKDIR/runs/2026-10-18-1758/carry/r0202-broker-PRIMARY/val/0.50/hillburmish/result-0.50.tsv
55d16d3167554e63f3b51a8eb4dfe9182b657911f6c30f7041b8ede47e49dbe7  WORKDIR/runs/2026-10-18-1758/carry/r0202-broker-PRIMARY/val/0.50/kesslersignificance/result-0.50.tsv
ebecf4c23c593cfbcf4cd582137691938b982dafe252bdb3df43a6596502c795  WORKDIR/runs/2026-10-18-1758/carry/r0202-broker-PRIMARY/val/0.50/luangthongkumkaren/result-0.50.tsv
f4bcbb439843fb792d3dcd8dd5bb5b0b0a4523f9eb0b209c4f4ca963c0839ae5  WORKDIR/runs/2026-10-18-1758/carry/r0202-broker-PRIMARY/val/0.50/wangbai/result-0.50.tsv
9b5428ead2ef0baf78aae6e97cbc4f6a8902eee7deeca37f47c4475a93cebc07  WORKDIR/runs/2026-10-18-1758/carry/r0202-broker-PRIMARY/test/0.40/bantubvd/result-0.40.tsv
861c135368cd2a53d5f12d9a4a65b265379b69f1980278fcb60d9a3dbd62dbf1  WORKDIR/runs/2026-10-18-1758/carry/r0202-broker-PRIMARY/test/0.40/beidazihui/result-0.40.tsv
73e6b91b3e9fac634ade2ed92c6122e54eaaa83bf9a4821d5e3a08cf646eb0fc  WORKDIR/runs/2026-10-18-1758/carry/r0202-broker-PRIMARY/test/0.40/birchallchapacuran/result-0.40.tsv
4496833ce7032621ee17e68677de2badf81e3b7f9376b7dc3128ecc091af4d74  WORKDIR/runs/2026-10-18-1758/carry/r0202-broker-PRIMARY/test/0.40/bodtkhobwa/result-0.40.tsv
645975d409b9de05a46f554d13411ca23bb3f4db29fd3e389388d3aa70bc2481  WORKDIR/runs/2026-10-18-1758/carry/r0202-broker-PRIMARY/test/0.40/bremerberta/result-0.40.tsv
fe2acdf0346670292a2672483538b14043c41c8919f04788ba6a32f91e846995  WORKDIR/runs/2026-10-18-1758/carry/r0202-broker-PRIMARY/test/0.40/deepadungpalaung/result-0.40.tsv
4e33ca709a420906d34420de11f3798f84cd8330188404f6138577ddb3ebbeee  WORKDIR/runs/2026-10-18-1758/carry/r0202-broker-PRIMARY/test/0.40/hillburmish/result-0.40.tsv
3b54168f65f5235997923b0d81e776b3ab4d91387fef4ba0d48d551b2e98a440  WORKDIR/runs/2026-10-18-1758/carry/r0202-broker-PRIMARY/test/0.40/kesslersignificance/result-0.40.tsv
b18d0c475916c6f5821c55297b0ba72a309bd9d6dd008f2e22c1c38102297ee8  WORKDIR/runs/2026-10-18-1758/carry/r0202-broker-PRIMARY/test/0.40/luangthongkumkaren/result-0.40.tsv
10455913b833f0be73fc4f04f0632f92b20530089db12d1ba0bcb012f986f644  WORKDIR/runs/2026-10-18-1758/carry/r0202-broker-PRIMARY/test/0.40/wangbai/result-0.40.tsv
efba3ac92c28b0833ce7c5ad7d1613485f190491a4385c8d850893a39fd7430c  WORKDIR/runs/2026-10-18-1758/carry/r0839-classifier-PRIMARY/val/0.50/bantubvd/result-0.50.tsv
67cea2eff575e35855dae507683d7486e155418e5d881f76a09fc0c32d349688  WORKDIR/runs/2026-10-18-1758/carry/r0839-classifier-PRIMARY/val/0.50/beidazihui/result-0.50.tsv
ec214dfc7e357754c0e9b4c7417bd152c85358b9979917266c05720e1c471803  WORKDIR/runs/2026-10-18-1758/carry/r0839-classifier-PRIMARY/val/0.50/birchallchapacuran/result-0.50.tsv
dd5ecfc09d35e2e61e593f58be91125cb1c9ab4d95e7f9c71c572d5805c96f47  WORKDIR/runs/2026-10-18-1758/carry/r0839-classifier-PRIMARY/val/0.50/bodtkhobwa/result-0.50.tsv
8dd62221b211ff8ba7b248c5c9316ac8550404ac18a403611538357615b39885  WORKDIR/runs/2026-10-18-1758/carry/r0839-classifier-PRIMARY/val/0.50/bremerberta/result-0.50.tsv
a5c84e828b37026766f041976c74c2081815d2d34f9c582a585b1f8266923544  WORKDIR/runs/2026-10-18-1758/carry/r0839-classifier-PRIMARY/val/0.50/deepadungpalaung/result-0.50.tsv
66734db13fde9c10c5b2bad1b49858cf88b2e8c26fc36f2f08d43b642f9653d9  WORKDIR/runs/2026-10-18-1758/carry/r0839-classifier-PRIMARY/val/0.50/hillburmish/result-0.50.tsv
c19c20d4cf6326ae37e27d1712b8c431bf67b1a2ee4b706b6bd96cf165b0a76c  WORKDIR/runs/2026-10-18-1758/carry/r0839-classifier-PRIMARY/val/0.50/kesslersignificance/result-0.50.tsv
d60d6b0bf445ea27301600b9c923890979416c0be37ddd0735442b36fab8da54  WORKDIR/runs/2026-10-18-1758/carry/r0839-classifier-PRIMARY/val/0.50/luangthongkumkaren/result-0.50.tsv
0aa4cddfe6b412f35cb761928eb67a065df488bd22199b0e53e66d5fea606b2a  WORKDIR/runs/2026-10-18-1758/carry/r0839-classifier-PRIMARY/val/0.50/wangbai/result-0.50.tsv
cbf74c9d5562246ed0b6334bffff11e3110432b136bc4b791ef2f75b6c0eedd0  WORKDIR/runs/2026-10-18-1758/carry/r0839-classifier-PRIMARY/test/0.40/bantubvd/result-0.40.tsv
096c896ef22e806cab60db5346925328f219d95cb40ec2ddfe67b0ffc701efbf  WORKDIR/runs/2026-10-18-1758/carry/r0839-classifier-PRIMARY/test/0.40/beidazihui/result-0.40.tsv
d0552eedfaa713424f1d5672a72fc5c35874bcd26767c3b659ece6166751ca12  WORKDIR/runs/2026-10-18-1758/carry/r0839-classifier-PRIMARY/test/0.40/birchallchapacuran/result-0.40.tsv
f35f7dd43be6dd5b3f92b5292c978519bcef39c236bbfaa6103f31f1dc16a86e  WORKDIR/runs/2026-10-18-1758/carry/r0839-classifier-PRIMARY/test/0.40/bodtkhobwa/result-0.40.tsv
f821a602e8e916548a8f76111d37a494a67f83541782d14492a9b9c90e69e7c7  WORKDIR/runs/2026-10-18-1758/carry/r0839-classifier-PRIMARY/test/0.40/bremerberta/result-0.40.tsv
ed6ebcc23ab15f87e6fcf436866193f28e8a549e95ce0e993073668f627f0d96  WORKDIR/runs/2026-10-18-1758/carry/r0839-classifier-PRIMARY/test/0.40/deepadungpalaung/result-0.40.tsv
69d4bc0fdfd7db641e3c04a38b200e90c0c90ce9bbd02eaee2697ac01ceb0c67  WORKDIR/runs/2026-10-18-1758/carry/r0839-classifier-PRIMARY/test/0.40/hillburmish/result-0.40.tsv
b98771950df9a71c476ef07bae0f59bff4bdefa01f13a0d37432f84a3d44209e  WORKDIR/runs/2026-10-18-1758/carry/r0839-classifier-PRIMARY/test/0.40/kesslersignificance/result-0.40.tsv
c3465c26673311d40d5ee97b0507c17f31d8a1f5d5d7740fef27301b1ab147b9  WORKDIR/runs/2026-10-18-1758/carry/r0839-classifier-PRIMARY/test/0.40/luangthongkumkaren/result-0.40.tsv
3b81cc6b00dac4de21ec927909cc88be0b23ce961fc61137eed31fecb045ebeb  WORKDIR/runs/2026-10-18-1758/carry/r0839-classifier-PRIMARY/test/0.40/wangbai/result-0.40.tsv
a2a0702eaa0c89aa841e67d1503623077626bde35b9b608643290f37b5266583  WORKDIR/runs/2026-10-18-1758/newent/analogist-PRIMARY/val/0.50/bantubvd/result-0.50.tsv
06770e0ce5863e59252d972556580b24094449e4d42fdb20dc93b3d54a518e39  WORKDIR/runs/2026-10-18-1758/newent/analogist-PRIMARY/val/0.50/beidazihui/result-0.50.tsv
dc9f1d12004c16f361894b8aedc70aa300b96177262f144274d0cf3288659413  WORKDIR/runs/2026-10-18-1758/newent/analogist-PRIMARY/val/0.50/birchallchapacuran/result-0.50.tsv
3b50c77dc793ffb4107d750230b2cfc5c5f795e03313d234ddfe4639dc5fc86d  WORKDIR/runs/2026-10-18-1758/newent/analogist-PRIMARY/val/0.50/bodtkhobwa/result-0.50.tsv
a5e4ed76e06f3030851cc532e402eb41edd2c6699ad99bd72cdc695e18a51c2b  WORKDIR/runs/2026-10-18-1758/newent/analogist-PRIMARY/val/0.50/bremerberta/result-0.50.tsv
dbf8d74f039ac2683823817ca53d640e715e93ae0105dd5bf4018800d0d38319  WORKDIR/runs/2026-10-18-1758/newent/analogist-PRIMARY/val/0.50/deepadungpalaung/result-0.50.tsv
411b6760fbf45123f5a3ca1386bdb1d898872e9bd12e37405b9af0dbc43e718e  WORKDIR/runs/2026-10-18-1758/newent/analogist-PRIMARY/val/0.50/hillburmish/result-0.50.tsv
899ea10493bc1ec4891cba5a92f7e178833131c600bbdc91748e537d79e24fa0  WORKDIR/runs/2026-10-18-1758/newent/analogist-PRIMARY/val/0.50/kesslersignificance/result-0.50.tsv
fa3c5319e58aae334a1f476457901e7f6b9c7ce2d2d1e625c165ef7d7ec1125a  WORKDIR/runs/2026-10-18-1758/newent/analogist-PRIMARY/val/0.50/luangthongkumkaren/result-0.50.tsv
0b1aeec79937c5400fa30c80a44dc964350ac69a86df351a14154b47411ce52d  WORKDIR/runs/2026-10-18-1758/newent/analogist-PRIMARY/val/0.50/wangbai/result-0.50.tsv
3a0465f1cd065b0d4ce1659faf7e3201282210885b0876e344ed32cb29a90f3e  WORKDIR/runs/2026-10-18-1758/newent/analogist-PRIMARY/test/0.40/bantubvd/result-0.40.tsv
453aa6e0a5909ab0e574ced0d6081af0e59ff8636593739d9b537cf5678d66eb  WORKDIR/runs/2026-10-18-1758/newent/analogist-PRIMARY/test/0.40/beidazihui/result-0.40.tsv
ea86a56535b8f49f090851cca98812a3c219ca3a12c30bb9df473102d0f900a1  WORKDIR/runs/2026-10-18-1758/newent/analogist-PRIMARY/test/0.40/birchallchapacuran/result-0.40.tsv
f15564560cc36c2b52ed99d0f5248131306167225a80ae1399b0eaf181d331b3  WORKDIR/runs/2026-10-18-1758/newent/analogist-PRIMARY/test/0.40/bodtkhobwa/result-0.40.tsv
899cc9342ae03a66a66773e196eeb7e3cee6d3116c052953630e8f6c8fe89f57  WORKDIR/runs/2026-10-18-1758/newent/analogist-PRIMARY/test/0.40/bremerberta/result-0.40.tsv
4ecd841f8c62ad40d9e9c0cfc4bfd7fa823411877c373dd04605f4d3651089ca  WORKDIR/runs/2026-10-18-1758/newent/analogist-PRIMARY/test/0.40/deepadungpalaung/result-0.40.tsv
57ad192b577d1fc3eea9fa4c58d14251f87824aa36b445cb2b2668f3296d78e9  WORKDIR/runs/2026-10-18-1758/newent/analogist-PRIMARY/test/0.40/hillburmish/result-0.40.tsv
3e25145e6cf5032baf04682683d595713d6ae0ad42812994da5c575a7b177a75  WORKDIR/runs/2026-10-18-1758/newent/analogist-PRIMARY/test/0.40/kesslersignificance/result-0.40.tsv
25bc31c5e07ce04220f04b4ed76aa29d7802e233b477bd6a1c06abd58ca26d3c  WORKDIR/runs/2026-10-18-1758/newent/analogist-PRIMARY/test/0.40/luangthongkumkaren/result-0.40.tsv
7c64ff5e8367c115a6b80b044adb65b77629575fbe15e3f639e62e0533989210  WORKDIR/runs/2026-10-18-1758/newent/analogist-PRIMARY/test/0.40/wangbai/result-0.40.tsv
7985e44a2d3b74f8ab3a8e20ccc6810b187c616b4e6261bfa5f822b31185540a  WORKDIR/runs/2026-10-18-1758/carry/r0839-analogist-PRIMARY/val/0.50/bantubvd/result-0.50.tsv
4d2fbd3bbcf9f423e64041befc449a07d50bdc5b4a6ff4d2fca9e61406c13281  WORKDIR/runs/2026-10-18-1758/carry/r0839-analogist-PRIMARY/val/0.50/beidazihui/result-0.50.tsv
9351895d55fb1ace1941a1557c485e4b18b60e7be7916c45338fa6123b170f7d  WORKDIR/runs/2026-10-18-1758/carry/r0839-analogist-PRIMARY/val/0.50/birchallchapacuran/result-0.50.tsv
e8d755499d7fd3ad2888b99e8426f58fff77613c7dddbdfc5534e325e29ae39c  WORKDIR/runs/2026-10-18-1758/carry/r0839-analogist-PRIMARY/val/0.50/bodtkhobwa/result-0.50.tsv
211e64d57db8fcaa0f39ba700cc33bc1ebabc80b5e655f3efb4f600a3ac3e77d  WORKDIR/runs/2026-10-18-1758/carry/r0839-analogist-PRIMARY/val/0.50/bremerberta/result-0.50.tsv
1413fc0c3896a33d570e28a92facaf58f5588c7772d035279b3d181e88726ddd  WORKDIR/runs/2026-10-18-1758/carry/r0839-analogist-PRIMARY/val/0.50/deepadungpalaung/result-0.50.tsv
9f68d1352be65c12bacb1918d06de7f37d3754be3ba1960377f4e22f20bbdc2c  WORKDIR/runs/2026-10-18-1758/carry/r0839-analogist-PRIMARY/val/0.50/hillburmish/result-0.50.tsv
4210e8fa1a080061c165caa348d0c00719c2dcd60499da658e26eef1dcfe812c  WORKDIR/runs/2026-10-18-1758/carry/r0839-analogist-PRIMARY/val/0.50/kesslersignificance/result-0.50.tsv
adb5550f887e7abbe025b9ecb11d3fe2f6a92538e9854023b885f046cbb7c811  WORKDIR/runs/2026-10-18-1758/carry/r0839-analogist-PRIMARY/val/0.50/luangthongkumkaren/result-0.50.tsv
8a01a63941d8fb4283d3220780dfe1f7b709c3aaa6603a60bd1c1ea083658105  WORKDIR/runs/2026-10-18-1758/carry/r0839-analogist-PRIMARY/val/0.50/wangbai/result-0.50.tsv
7a2820e5f95790756d2879c0b692a591f5a5237c4639f53c02ddeb6183afc7ba  WORKDIR/runs/2026-10-18-1758/carry/r0839-analogist-PRIMARY/test/0.40/bantubvd/result-0.40.tsv
f0099c06f4861f316d158a661d060ee6fa7d0b27a3ea56873395d43f037a9a3e  WORKDIR/runs/2026-10-18-1758/carry/r0839-analogist-PRIMARY/test/0.40/beidazihui/result-0.40.tsv
d6ec4f1ae6a5374cec63a7f75433fe8913251bcaffaa38d716fea9e658026dbc  WORKDIR/runs/2026-10-18-1758/carry/r0839-analogist-PRIMARY/test/0.40/birchallchapacuran/result-0.40.tsv
27dd814bc889b7d05334eb5e94e849d6c8520cfc9b7e5274b91c2072f3e1c49f  WORKDIR/runs/2026-10-18-1758/carry/r0839-analogist-PRIMARY/test/0.40/bodtkhobwa/result-0.40.tsv
71693475e037a1256348d3169b3c0a6f4b381eb2c74e084e207e1ea694b89b98  WORKDIR/runs/2026-10-18-1758/carry/r0839-analogist-PRIMARY/test/0.40/bremerberta/result-0.40.tsv
40527e3c9654d0660beefe065e74ce557cbd0bb0e1666accc03edd26dfa678ab  WORKDIR/runs/2026-10-18-1758/carry/r0839-analogist-PRIMARY/test/0.40/deepadungpalaung/result-0.40.tsv
6e38765fa3a56dd4a6da10d2a42d281c20c4b7bf5c4e9e792e77da6097e3c9f5  WORKDIR/runs/2026-10-18-1758/carry/r0839-analogist-PRIMARY/test/0.40/hillburmish/result-0.40.tsv
0b8ff133b0977185033c3007a0a6a24d69c3a0a8247d17ff6ab562cb11c4094f  WORKDIR/runs/2026-10-18-1758/carry/r0839-analogist-PRIMARY/test/0.40/kesslersignificance/result-0.40.tsv
f474975723b698cddb6e61cc421bb9898a2b2a873ffc7c3fa6da406540a69ff6  WORKDIR/runs/2026-10-18-1758/carry/r0839-analogist-PRIMARY/test/0.40/luangthongkumkaren/result-0.40.tsv
83efde98640c0abe86fab2f66ad7063a82e84afcc7ce0d267cd4dec34637cfc0  WORKDIR/runs/2026-10-18-1758/carry/r0839-analogist-PRIMARY/test/0.40/wangbai/result-0.40.tsv
8e800b7cc606ca24ed18ab9291080893678ab0b85b5a5bad8be30645fe51eb79  WORKDIR/runs/2026-10-18-1758/newent/phylo-PRIMARY/val/0.50/bantubvd/result-0.50.tsv
112691c1fe08224c30b69f5ac03fdf3586ecbf819677bc767f83f19cde9bf00f  WORKDIR/runs/2026-10-18-1758/newent/phylo-PRIMARY/val/0.50/beidazihui/result-0.50.tsv
980a592d9bdcacd794e2459385f91da3a3eb7dd18227d01c2f52b32f0314eea8  WORKDIR/runs/2026-10-18-1758/newent/phylo-PRIMARY/val/0.50/birchallchapacuran/result-0.50.tsv
c83be9e81e3c9d31daa48b96c54ee773eb010f669c4f07a4aa3654ba8bb90391  WORKDIR/runs/2026-10-18-1758/newent/phylo-PRIMARY/val/0.50/bodtkhobwa/result-0.50.tsv
f98aee172c89c031770a9f2e890ee64519eb26a8d7e38e0f05172a417a29ff68  WORKDIR/runs/2026-10-18-1758/newent/phylo-PRIMARY/val/0.50/bremerberta/result-0.50.tsv
4683ed9f273ca14acbf404cb9ecce8b34798ffbc3d542d228737740877b89291  WORKDIR/runs/2026-10-18-1758/newent/phylo-PRIMARY/val/0.50/deepadungpalaung/result-0.50.tsv
b052486f747962b806d3ebf0c805f42a9a9efc03deb648d6b5cff18d60b5c23b  WORKDIR/runs/2026-10-18-1758/newent/phylo-PRIMARY/val/0.50/hillburmish/result-0.50.tsv
73f309460eaed46eccf8235330404bf04c3e878d3405392bc4744172fb07c58c  WORKDIR/runs/2026-10-18-1758/newent/phylo-PRIMARY/val/0.50/kesslersignificance/result-0.50.tsv
e87ae47856dcf4b396a80ff8192d332e9e2b552f370e6c4c324e2578ed3d58ad  WORKDIR/runs/2026-10-18-1758/newent/phylo-PRIMARY/val/0.50/luangthongkumkaren/result-0.50.tsv
e0179e80719b88dc902f689003a41e035927d92d814ca9e4016ec277095d76bb  WORKDIR/runs/2026-10-18-1758/newent/phylo-PRIMARY/val/0.50/wangbai/result-0.50.tsv
98adbada09fb62578f5c0ea060af74706d59ed7f791dd4b41f3ab78b4e3200b1  WORKDIR/runs/2026-10-18-1758/newent/phylo-PRIMARY/test/0.40/bantubvd/result-0.40.tsv
d1928cf555e43d79d78a1fa061626c19ddbceb5da63537fe48f4d3087c44c179  WORKDIR/runs/2026-10-18-1758/newent/phylo-PRIMARY/test/0.40/beidazihui/result-0.40.tsv
5f9984a6672b1dcf65ebcb98f5aaea4be04e1392998b16437891d6afb0ef2cfa  WORKDIR/runs/2026-10-18-1758/newent/phylo-PRIMARY/test/0.40/birchallchapacuran/result-0.40.tsv
40a5a82d1803b7536359e0fd33d9a4c05c37685b74568a549ff6b1c2e2cc79e3  WORKDIR/runs/2026-10-18-1758/newent/phylo-PRIMARY/test/0.40/bodtkhobwa/result-0.40.tsv
8ec9e18f05ecacd4275a834783af03283f3cd1cdfb81e8202aca0d7b21cda193  WORKDIR/runs/2026-10-18-1758/newent/phylo-PRIMARY/test/0.40/bremerberta/result-0.40.tsv
0a4fdcb3cabc7dea05681e912990ec8e4d1eb65819bf27edaaa06dd18315e52c  WORKDIR/runs/2026-10-18-1758/newent/phylo-PRIMARY/test/0.40/deepadungpalaung/result-0.40.tsv
bb3eab19cda4ca8e794353d78e0d9c51fd7fa468d5caf92e1a7b3e6006d1be08  WORKDIR/runs/2026-10-18-1758/newent/phylo-PRIMARY/test/0.40/hillburmish/result-0.40.tsv
7bcb98204f4a99224d58e8ae0e0213a5597e002d8f3a7e2b6610168fde5eaabf  WORKDIR/runs/2026-10-18-1758/newent/phylo-PRIMARY/test/0.40/kesslersignificance/result-0.40.tsv
203ef2c3fde4edf2adaed61bfeb3a9b122376102ca1110fcb48fd0c8ea215f8d  WORKDIR/runs/2026-10-18-1758/newent/phylo-PRIMARY/test/0.40/luangthongkumkaren/result-0.40.tsv
a7d5da4419cc358acc5506b19cbecf3de2117eea89e05531fb1d92afb495e672  WORKDIR/runs/2026-10-18-1758/newent/phylo-PRIMARY/test/0.40/wangbai/result-0.40.tsv
1a2f6fef58ab43ca6d235bc53b8ebc8f502f78b58eed57f2d89c37b3bbf41bc0  WORKDIR/runs/2026-10-18-1758/carry/r0839-phylo-PRIMARY/val/0.50/bantubvd/result-0.50.tsv
a1162536ac2a02e55b01df0ab919621616c9511eda06c0ee5c7f6000b46e94cb  WORKDIR/runs/2026-10-18-1758/carry/r0839-phylo-PRIMARY/val/0.50/beidazihui/result-0.50.tsv
4419d80b702fdccd37cbaf79f1a94c9efe02a5ecd1885e903746260942b9ee97  WORKDIR/runs/2026-10-18-1758/carry/r0839-phylo-PRIMARY/val/0.50/birchallchapacuran/result-0.50.tsv
311031ae7aefaceb5e54f06958fb2d68b8bc961b59991d5c51e5726027bf5252  WORKDIR/runs/2026-10-18-1758/carry/r0839-phylo-PRIMARY/val/0.50/bodtkhobwa/result-0.50.tsv
2f8f45563a90b3ddb896c62c92156250629e49bdc94797737c61018641ea8cd5  WORKDIR/runs/2026-10-18-1758/carry/r0839-phylo-PRIMARY/val/0.50/bremerberta/result-0.50.tsv
07fcad9b108697dcd9b519df6d323aae6fc021fad3c5fa2314d14645e1a66e56  WORKDIR/runs/2026-10-18-1758/carry/r0839-phylo-PRIMARY/val/0.50/deepadungpalaung/result-0.50.tsv
7dbd2fc9995175c4a0540f794aeb785d12ef333475d699e6c9f380f3375c5c61  WORKDIR/runs/2026-10-18-1758/carry/r0839-phylo-PRIMARY/val/0.50/hillburmish/result-0.50.tsv
171f2fd90609bcfb02992f17757f2d4c14ed10289d66f0b45ee4dcb0de30944a  WORKDIR/runs/2026-10-18-1758/carry/r0839-phylo-PRIMARY/val/0.50/kesslersignificance/result-0.50.tsv
4b7daadc671cd68c10e2e0de9d07cda4fec8f88e935f108eaf9c3b124136b243  WORKDIR/runs/2026-10-18-1758/carry/r0839-phylo-PRIMARY/val/0.50/luangthongkumkaren/result-0.50.tsv
13d81491bbbd850890f7492ce77092aae85bf885f5a509f8c79bef6337d2e76b  WORKDIR/runs/2026-10-18-1758/carry/r0839-phylo-PRIMARY/val/0.50/wangbai/result-0.50.tsv
c3a8f6a0f10a45d87c84c38cc7003870e2f5d8c41539ff23351ed3a74955f46d  WORKDIR/runs/2026-10-18-1758/carry/r0839-phylo-PRIMARY/test/0.40/bantubvd/result-0.40.tsv
ac8758f37feefc20113b2d89d0544f043778ed625a346feb35020cc816a379fc  WORKDIR/runs/2026-10-18-1758/carry/r0839-phylo-PRIMARY/test/0.40/beidazihui/result-0.40.tsv
88d1d6b4d63d38ff05833c8d36929ad5a2aa0a13982935a4c8a997a05a1b2763  WORKDIR/runs/2026-10-18-1758/carry/r0839-phylo-PRIMARY/test/0.40/birchallchapacuran/result-0.40.tsv
325e9ba8c7d45281d65db647c5a70e1a8175b8c46806f8edd81c600f4f5d1047  WORKDIR/runs/2026-10-18-1758/carry/r0839-phylo-PRIMARY/test/0.40/bodtkhobwa/result-0.40.tsv
6428e472bd19f2b0912d9f0e946936e00d243eac010bb49a210ff963ccb2ce08  WORKDIR/runs/2026-10-18-1758/carry/r0839-phylo-PRIMARY/test/0.40/bremerberta/result-0.40.tsv
fc2eb524cce8376f0315c4d6f3c14b8744c5c41b9fcd5b00d73de37e85e36ed1  WORKDIR/runs/2026-10-18-1758/carry/r0839-phylo-PRIMARY/test/0.40/deepadungpalaung/result-0.40.tsv
8a9708ae1d6d0cf4813bd3d40ab427aad1848688e6cbe3d849a869f7c734f485  WORKDIR/runs/2026-10-18-1758/carry/r0839-phylo-PRIMARY/test/0.40/hillburmish/result-0.40.tsv
02bf1cedd7f8b580624a4b0d15195c18e6c885bf224b36e7447daa89c097cf27  WORKDIR/runs/2026-10-18-1758/carry/r0839-phylo-PRIMARY/test/0.40/kesslersignificance/result-0.40.tsv
70c90b9ac3306f717dc910c71e5f7ad3746c83067c25aa2165250863d75490fc  WORKDIR/runs/2026-10-18-1758/carry/r0839-phylo-PRIMARY/test/0.40/luangthongkumkaren/result-0.40.tsv
ef294c3e1ee9575c88543825e8750ba168adcb7b44cf8731ebeba6557bd5c1f4  WORKDIR/runs/2026-10-18-1758/carry/r0839-phylo-PRIMARY/test/0.40/wangbai/result-0.40.tsv
6da834e7c18ac95a773642ea6af5cc1aae8f0d68834f7492f60552e368cab3d9  WORKDIR/runs/2026-10-18-1758/newent/correspondence-PRIMARY/val/0.50/bantubvd/result-0.50.tsv
247fd078f4e75ed2c438dcfa476d1f8646b94ad6dee60bad6480715924528219  WORKDIR/runs/2026-10-18-1758/newent/correspondence-PRIMARY/val/0.50/beidazihui/result-0.50.tsv
b4cbc2fb5bed2a035bcb2b38a94a55fcd365a4402fc377beb6501897aaa9c60b  WORKDIR/runs/2026-10-18-1758/newent/correspondence-PRIMARY/val/0.50/birchallchapacuran/result-0.50.tsv
2e556f33f964f93c1d8538e36fe959bf04f9bdbb2ab4ceeff6c87458992ae4c9  WORKDIR/runs/2026-10-18-1758/newent/correspondence-PRIMARY/val/0.50/bodtkhobwa/result-0.50.tsv
cbed8f4d22b7e45337b0c6e90ed6727df05a026c6697c623cf9b82edab9f292a  WORKDIR/runs/2026-10-18-1758/newent/correspondence-PRIMARY/val/0.50/bremerberta/result-0.50.tsv
7f776ebb6557ff379a7b75650a4170117b59d70f069d2c59e0319608151874b7  WORKDIR/runs/2026-10-18-1758/newent/correspondence-PRIMARY/val/0.50/deepadungpalaung/result-0.50.tsv
86d8cccd68d296fe5b333cb139b8d6b8020641dec8cf531a00c1d462be28f289  WORKDIR/runs/2026-10-18-1758/newent/correspondence-PRIMARY/val/0.50/hillburmish/result-0.50.tsv
66d0d41265663411658101d6646dddd5ebd35b1fa2df3613c5ec58259c04d76e  WORKDIR/runs/2026-10-18-1758/newent/correspondence-PRIMARY/val/0.50/kesslersignificance/result-0.50.tsv
abf64ad099c707d7a770d5aae81544862d9a97770f43a76b03329611c0c7290c  WORKDIR/runs/2026-10-18-1758/newent/correspondence-PRIMARY/val/0.50/luangthongkumkaren/result-0.50.tsv
5dc09bcf9031682a251662885afda07a61e25c34bd217db14cc9afbf08a831a5  WORKDIR/runs/2026-10-18-1758/newent/correspondence-PRIMARY/val/0.50/wangbai/result-0.50.tsv
d06dfa1f0ca7cbf91a17805e9c1296661b6ee82291e07e9c7217d88afa62ec43  WORKDIR/runs/2026-10-18-1758/newent/correspondence-PRIMARY/test/0.40/bantubvd/result-0.40.tsv
436e037c3b55ec36015d0cf4def383d5dd9d89956b18911d69794e7bbf3e1c17  WORKDIR/runs/2026-10-18-1758/newent/correspondence-PRIMARY/test/0.40/beidazihui/result-0.40.tsv
a977dd96649182e119a2db41a6561fdee836afb1fe53fa5c2bfe5c6850f4015f  WORKDIR/runs/2026-10-18-1758/newent/correspondence-PRIMARY/test/0.40/birchallchapacuran/result-0.40.tsv
3d9ba9e47e3f8fe7fb09a4cc44bd64f011683cff3b230a276391c7938426e94d  WORKDIR/runs/2026-10-18-1758/newent/correspondence-PRIMARY/test/0.40/bodtkhobwa/result-0.40.tsv
c7da87d2893e969a60d65eb645f68ffe5bc0bb842068da31a439af3df0b8ba84  WORKDIR/runs/2026-10-18-1758/newent/correspondence-PRIMARY/test/0.40/bremerberta/result-0.40.tsv
faa28a76e698fcb14ae98eb851fc02b13ee304bd1f4480ad1722065743b8fee5  WORKDIR/runs/2026-10-18-1758/newent/correspondence-PRIMARY/test/0.40/deepadungpalaung/result-0.40.tsv
58413b61a56afbcd2f818e4180636d24eccab7528e0c29d87d52dce388087133  WORKDIR/runs/2026-10-18-1758/newent/correspondence-PRIMARY/test/0.40/hillburmish/result-0.40.tsv
b0c49a84143aee214585ac0cf3a4736176f4299b2540e626b30a16e9ea518e4c  WORKDIR/runs/2026-10-18-1758/newent/correspondence-PRIMARY/test/0.40/kesslersignificance/result-0.40.tsv
4028c92370919c928d5008609e163b9795046d8bd6ee1ad9ec08d8dfb9432215  WORKDIR/runs/2026-10-18-1758/newent/correspondence-PRIMARY/test/0.40/luangthongkumkaren/result-0.40.tsv
9be98c8f8852b61308a964ffb6dd9f5d855e5849a7105f5dabe82adaade512a2  WORKDIR/runs/2026-10-18-1758/newent/correspondence-PRIMARY/test/0.40/wangbai/result-0.40.tsv
c820468bcb17309f931345d81c8139f2e7b7ea6ca6b7bb4762da5f755cc7c311  WORKDIR/runs/2026-10-18-1758/carry/r0202-analogist-SECONDARY/val/0.50/bantubvd/result-0.50.tsv
363aa329133e239a6812fd5ccf01df21a1b9e16d212f492cbfa1fae360edad63  WORKDIR/runs/2026-10-18-1758/carry/r0202-analogist-SECONDARY/val/0.50/beidazihui/result-0.50.tsv
b82c9fbf426abcd8a6a46ba4fa2625e7c16e8031fa5c44d7775a1791f2bb4cdd  WORKDIR/runs/2026-10-18-1758/carry/r0202-analogist-SECONDARY/val/0.50/birchallchapacuran/result-0.50.tsv
c3f2ec080af849a4aae87baa5c9c92d68c3c213eefc5d5852c84f5c39f355250  WORKDIR/runs/2026-10-18-1758/carry/r0202-analogist-SECONDARY/val/0.50/bodtkhobwa/result-0.50.tsv
d6dab6eb25cf472cd967b676222df1bb731b046247ac7feb8e73f10769132c86  WORKDIR/runs/2026-10-18-1758/carry/r0202-analogist-SECONDARY/val/0.50/bremerberta/result-0.50.tsv
dc90d5167d4601afed617e2b384d1691ce8e85b02a1643f3b12b8e18584aa585  WORKDIR/runs/2026-10-18-1758/carry/r0202-analogist-SECONDARY/val/0.50/deepadungpalaung/result-0.50.tsv
0054eb3b5ceee65d05e40392b9498270c7fc752965ce2ca3ddb000204a036da7  WORKDIR/runs/2026-10-18-1758/carry/r0202-analogist-SECONDARY/val/0.50/hillburmish/result-0.50.tsv
8e06e83a05f2e56cb45d97e9d03490bd31acfc5b9a99c5e3887d207c7f863c90  WORKDIR/runs/2026-10-18-1758/carry/r0202-analogist-SECONDARY/val/0.50/kesslersignificance/result-0.50.tsv
073e3262d5d751d86e330482c4e212c3b472ec832fdbc25064896cf1ee0f9c73  WORKDIR/runs/2026-10-18-1758/carry/r0202-analogist-SECONDARY/val/0.50/luangthongkumkaren/result-0.50.tsv
92461444c4251a161bed4a0f85636670dfa1eb1a5601e197fa9008a4b619195b  WORKDIR/runs/2026-10-18-1758/carry/r0202-analogist-SECONDARY/val/0.50/wangbai/result-0.50.tsv
354f29b2c294f267bf6f6559dfd1e767413426fa5f62c42500a1eed2602a390c  WORKDIR/runs/2026-10-18-1758/carry/r0202-analogist-SECONDARY/test/0.40/bantubvd/result-0.40.tsv
37656fea075e569ddccb00b7a237888f41f9a2a6c573112f89fd06c7af0c2e1e  WORKDIR/runs/2026-10-18-1758/carry/r0202-analogist-SECONDARY/test/0.40/beidazihui/result-0.40.tsv
4ce6b022a1046a9fca94fe25f5046f50ae9bc2c2236cc62d84a8337061566435  WORKDIR/runs/2026-10-18-1758/carry/r0202-analogist-SECONDARY/test/0.40/birchallchapacuran/result-0.40.tsv
c3e4dd4e656208b9382d05ebd7c1983e158e1855424f28da2b6b9c68fda7206e  WORKDIR/runs/2026-10-18-1758/carry/r0202-analogist-SECONDARY/test/0.40/bodtkhobwa/result-0.40.tsv
e7c9f9734d1a230f31833be7fec25d4fce3f18fd5dec12eacc8702a406a11cf7  WORKDIR/runs/2026-10-18-1758/carry/r0202-analogist-SECONDARY/test/0.40/bremerberta/result-0.40.tsv
c5e98bc70719183dd69e408cbec4ca8b6c41c15ff020aabf46479af0e31a2a06  WORKDIR/runs/2026-10-18-1758/carry/r0202-analogist-SECONDARY/test/0.40/deepadungpalaung/result-0.40.tsv
56f9c31aad6bfa3b3199523512ea6969c8df09bd18b4283cb0b2be0c6abed32e  WORKDIR/runs/2026-10-18-1758/carry/r0202-analogist-SECONDARY/test/0.40/hillburmish/result-0.40.tsv
5a5ac1f8bba2b889485663b092fd8cd83e6becb15af00f033e26abd4b620dbed  WORKDIR/runs/2026-10-18-1758/carry/r0202-analogist-SECONDARY/test/0.40/kesslersignificance/result-0.40.tsv
38b1e7aa4ba3d43806905f214402e6deafbaa3af8a278aa465dfa24bfe8ee701  WORKDIR/runs/2026-10-18-1758/carry/r0202-analogist-SECONDARY/test/0.40/luangthongkumkaren/result-0.40.tsv
fc9c3c61ebe80a6c1a2dc8181af120f5712a14adcd089913777af317b6f13a2a  WORKDIR/runs/2026-10-18-1758/carry/r0202-analogist-SECONDARY/test/0.40/wangbai/result-0.40.tsv
58c5e7cbd4aeb916df88b1ef92fe664629832df16fa7143054e5df5dc05daf27  WORKDIR/runs/2026-10-18-1758/carry/r0202-broker-SECONDARY/val/0.50/bantubvd/result-0.50.tsv
3d8757f19c8ac120707158cf884c635cef39c3c02e7a3d640cce7f5990fe7a7a  WORKDIR/runs/2026-10-18-1758/carry/r0202-broker-SECONDARY/val/0.50/beidazihui/result-0.50.tsv
9a7a3faefb17b84ff9dd525dd9a82492eaad9d45dd62f573699b0d35ecbe1dab  WORKDIR/runs/2026-10-18-1758/carry/r0202-broker-SECONDARY/val/0.50/birchallchapacuran/result-0.50.tsv
4829ad93f8dc5a24907dd0424a86566edb5f3cb304f6ceabca8162e85a67bf88  WORKDIR/runs/2026-10-18-1758/carry/r0202-broker-SECONDARY/val/0.50/bodtkhobwa/result-0.50.tsv
1e04222396ff15d68a1ebbc85a93c1101ea919d88a627397b1ada0f5fa63f2fe  WORKDIR/runs/2026-10-18-1758/carry/r0202-broker-SECONDARY/val/0.50/bremerberta/result-0.50.tsv
23d31ffca5f8a310ad14550f8500260a4c6f254440e026b4cced40c7254c2823  WORKDIR/runs/2026-10-18-1758/carry/r0202-broker-SECONDARY/val/0.50/deepadungpalaung/result-0.50.tsv
a0f0fa4ba556de9487d3343eeffab760a75a8629a7dc9dbd6a9979a1beedcb33  WORKDIR/runs/2026-10-18-1758/carry/r0202-broker-SECONDARY/val/0.50/hillburmish/result-0.50.tsv
6733c38a103081800929edf4de7d75484c16348e3c6d536fd84324902829c936  WORKDIR/runs/2026-10-18-1758/carry/r0202-broker-SECONDARY/val/0.50/kesslersignificance/result-0.50.tsv
49f43dd5909bc6aa2d1d8f565f52c1ca2ec5572d7ee1ccaece2587c98e94cb42  WORKDIR/runs/2026-10-18-1758/carry/r0202-broker-SECONDARY/val/0.50/luangthongkumkaren/result-0.50.tsv
91ac6f255ec40be406eccab61a810a22db216718dec7d1a8ffec74dd105bfb01  WORKDIR/runs/2026-10-18-1758/carry/r0202-broker-SECONDARY/val/0.50/wangbai/result-0.50.tsv
18af1476e11bf1e8af548a5c6149f1f392b5f863ff9dcb3643f997b033e85b4b  WORKDIR/runs/2026-10-18-1758/carry/r0202-broker-SECONDARY/test/0.40/bantubvd/result-0.40.tsv
eea5698cc5e5c5ee86fa996857094441557a3e902f6ee9d033a7071bc025ec2c  WORKDIR/runs/2026-10-18-1758/carry/r0202-broker-SECONDARY/test/0.40/beidazihui/result-0.40.tsv
d8049aa26bb19ec74b3b3082fbff4de78d24fd1cf6623647f166c25d7b608255  WORKDIR/runs/2026-10-18-1758/carry/r0202-broker-SECONDARY/test/0.40/birchallchapacuran/result-0.40.tsv
2d046604374b2ebc19ee3300a7eec9dddb4a9476c5144cbec08c347d50729377  WORKDIR/runs/2026-10-18-1758/carry/r0202-broker-SECONDARY/test/0.40/bodtkhobwa/result-0.40.tsv
2cf8e6df2871194cc26b874e4c1056b6a05a11ccce34e9f6af9afba1e3699b2b  WORKDIR/runs/2026-10-18-1758/carry/r0202-broker-SECONDARY/test/0.40/bremerberta/result-0.40.tsv
4b63abaecc45f818aa97e9fa9d22ad985a9fabf2375f0133b639273cefd97f16  WORKDIR/runs/2026-10-18-1758/carry/r0202-broker-SECONDARY/test/0.40/deepadungpalaung/result-0.40.tsv
03fd681418e20fa84b8b0f35f3a466e8b8a1122a0936093e9c65cc8008a35742  WORKDIR/runs/2026-10-18-1758/carry/r0202-broker-SECONDARY/test/0.40/hillburmish/result-0.40.tsv
3f33e184d2df149d00ee2f5f0f3480c19bb6b67c6272278824d69d6dddd2d98d  WORKDIR/runs/2026-10-18-1758/carry/r0202-broker-SECONDARY/test/0.40/kesslersignificance/result-0.40.tsv
7e77b3c3246e02d9a13b21d5b959ebc70d59b1ef5c92b12db180125a003dd7fc  WORKDIR/runs/2026-10-18-1758/carry/r0202-broker-SECONDARY/test/0.40/luangthongkumkaren/result-0.40.tsv
86bccd130b0e3ca5615d758c90be845d5857d568c5ac45b22cde1b0b2a9c795e  WORKDIR/runs/2026-10-18-1758/carry/r0202-broker-SECONDARY/test/0.40/wangbai/result-0.40.tsv
9d2b42785efe7916a0a932ec5f531b7ba85fda836b8da401a4c8cce2549870ae  WORKDIR/runs/2026-10-18-1758/carry/r0839-phylo-SECONDARY/val/0.50/bantubvd/result-0.50.tsv
da4fb3f20de7c4f144fdab2167a2233bc93941857b81dbd6e28b323e52b8a4e6  WORKDIR/runs/2026-10-18-1758/carry/r0839-phylo-SECONDARY/val/0.50/beidazihui/result-0.50.tsv
a726b9ad0e9653df281ec0d6f0469eef0122ca04a6c9df182067d232566ebbc0  WORKDIR/runs/2026-10-18-1758/carry/r0839-phylo-SECONDARY/val/0.50/birchallchapacuran/result-0.50.tsv
dd2ff7e2cb3e475a4022c649c8f67a89c3fe1d723b57220195cc1e08d1f36884  WORKDIR/runs/2026-10-18-1758/carry/r0839-phylo-SECONDARY/val/0.50/bodtkhobwa/result-0.50.tsv
0520f9129fe16028c7739068f683e49c33d775a8bf8899a6c11e69b365a0720f  WORKDIR/runs/2026-10-18-1758/carry/r0839-phylo-SECONDARY/val/0.50/bremerberta/result-0.50.tsv
d95052715cb200c48f79502ee55fbd351dd9697479c3c554083b532c1435a4e5  WORKDIR/runs/2026-10-18-1758/carry/r0839-phylo-SECONDARY/val/0.50/deepadungpalaung/result-0.50.tsv
8cfdc7173af62b7a1f8db90cc4d23ac86cfaeffd3e1903d06013a46cb1781804  WORKDIR/runs/2026-10-18-1758/carry/r0839-phylo-SECONDARY/val/0.50/hillburmish/result-0.50.tsv
83b8605ce620963a8d3c33051bdef2a2aacdeccd62da01bcc2cba64641feb2ca  WORKDIR/runs/2026-10-18-1758/carry/r0839-phylo-SECONDARY/val/0.50/kesslersignificance/result-0.50.tsv
ed374805089bd3b2e9ff4ee57573eaf5458fac9fbc6138615f368e56d97b7de7  WORKDIR/runs/2026-10-18-1758/carry/r0839-phylo-SECONDARY/val/0.50/luangthongkumkaren/result-0.50.tsv
04cbb9d998e62b7e57754056fbb7ac2df01d7fef3c47c9492db70b658abeae7c  WORKDIR/runs/2026-10-18-1758/carry/r0839-phylo-SECONDARY/val/0.50/wangbai/result-0.50.tsv
711fb73f0234f352c19af8886097de200ea933ad94a688ea51cbd469ab86b75b  WORKDIR/runs/2026-10-18-1758/carry/r0839-phylo-SECONDARY/test/0.40/bantubvd/result-0.40.tsv
0ddf822ed414eacb1030ffc025880666077727fecdae821ab1c05b3d9bc0c46e  WORKDIR/runs/2026-10-18-1758/carry/r0839-phylo-SECONDARY/test/0.40/beidazihui/result-0.40.tsv
2ea4ee36e94fd11341ec8ea1936bcb5672be07f89005c4d9195bd706f2ef8680  WORKDIR/runs/2026-10-18-1758/carry/r0839-phylo-SECONDARY/test/0.40/birchallchapacuran/result-0.40.tsv
dfe1ba8af7e3e5b1f4fecc2c9a960ed0efb768d64a9321b3112029502620fd75  WORKDIR/runs/2026-10-18-1758/carry/r0839-phylo-SECONDARY/test/0.40/bodtkhobwa/result-0.40.tsv
d6e55293d0c1abc19ce768317cbf52b0f71dafec2d52cbc78c97e8762bd4fb6b  WORKDIR/runs/2026-10-18-1758/carry/r0839-phylo-SECONDARY/test/0.40/bremerberta/result-0.40.tsv
7114c68a96cd83b5e0d86101e44e21ec4c84ee5318623a7916f021d165853632  WORKDIR/runs/2026-10-18-1758/carry/r0839-phylo-SECONDARY/test/0.40/deepadungpalaung/result-0.40.tsv
e520399d2f89d5e9699685f69aecaa2a6c25287a718d5129d45c3c7cd9deb3b8  WORKDIR/runs/2026-10-18-1758/carry/r0839-phylo-SECONDARY/test/0.40/hillburmish/result-0.40.tsv
6bdc0b45d7ad3ec5b2cbda31baedba2c9c646f1456d978e49ab23ef9e8ab8a5f  WORKDIR/runs/2026-10-18-1758/carry/r0839-phylo-SECONDARY/test/0.40/kesslersignificance/result-0.40.tsv
5b745cd30ad9d258d0b61ad404c9914ffdeaee13fdce80713fe5da26597f0096  WORKDIR/runs/2026-10-18-1758/carry/r0839-phylo-SECONDARY/test/0.40/luangthongkumkaren/result-0.40.tsv
4ff9a3c9c42d97445725afdec08088d4093d06367d8cf27271bbb913c6a2d3f5  WORKDIR/runs/2026-10-18-1758/carry/r0839-phylo-SECONDARY/test/0.40/wangbai/result-0.40.tsv
aeef6e9412df1856c275a622692bf3fca3c72e26497f88f3215ba4f76ccab634  WORKDIR/runs/2026-10-18-1758/newent/correspondence-SECONDARY/val/0.50/bantubvd/result-0.50.tsv
31e47015dc69bbd1cbbec4a55ae3500df5dac703df212923e838a58b652d6e3e  WORKDIR/runs/2026-10-18-1758/newent/correspondence-SECONDARY/val/0.50/beidazihui/result-0.50.tsv
8f0d5290c4b47dd1626fb3011f50be2346b1801ffd6e2daaabed1278e9535446  WORKDIR/runs/2026-10-18-1758/newent/correspondence-SECONDARY/val/0.50/birchallchapacuran/result-0.50.tsv
41121d4b6da1570d7ed4976cce958a9536cca43fc337e3ec3516aa1441063334  WORKDIR/runs/2026-10-18-1758/newent/correspondence-SECONDARY/val/0.50/bodtkhobwa/result-0.50.tsv
19546a66cc1fb10fb1eecd841b99419b98b903f16ec63c229919646e46f78071  WORKDIR/runs/2026-10-18-1758/newent/correspondence-SECONDARY/val/0.50/bremerberta/result-0.50.tsv
73b7de7131c3317b3d5c54938dfae88ba198a1a80e3f02deacd68e005f05db7e  WORKDIR/runs/2026-10-18-1758/newent/correspondence-SECONDARY/val/0.50/deepadungpalaung/result-0.50.tsv
66bb5440fdf52a1c16670107ab6fbd27730874498af4cc3e2b217f461f2d744f  WORKDIR/runs/2026-10-18-1758/newent/correspondence-SECONDARY/val/0.50/hillburmish/result-0.50.tsv
f697f68f1487a862742eb34b51fa80c43fc5381ee91e5d8a826ce7c2a46deaa7  WORKDIR/runs/2026-10-18-1758/newent/correspondence-SECONDARY/val/0.50/kesslersignificance/result-0.50.tsv
489f28b9bdec1e48868fedafdb28438039b29bf0570bef2827146ffd57d8e6fe  WORKDIR/runs/2026-10-18-1758/newent/correspondence-SECONDARY/val/0.50/luangthongkumkaren/result-0.50.tsv
371b28a88d04e67024f859a84f6279ad1364be86d1bfd712ce78cee11f4ff0b5  WORKDIR/runs/2026-10-18-1758/newent/correspondence-SECONDARY/val/0.50/wangbai/result-0.50.tsv
2ed0364f4ad5381e584e861f53e20a19a1199964b0576f224ce6b6b0a22ddfc8  WORKDIR/runs/2026-10-18-1758/newent/correspondence-SECONDARY/test/0.40/bantubvd/result-0.40.tsv
862b11d919d73c604d194cce37a4be5c4f1bfae7fd75d8501041094fb67088c0  WORKDIR/runs/2026-10-18-1758/newent/correspondence-SECONDARY/test/0.40/beidazihui/result-0.40.tsv
4b9be3d66e5f6654bf3757e185c87504da1c6fdbe1839f0840f28d401e72bb5e  WORKDIR/runs/2026-10-18-1758/newent/correspondence-SECONDARY/test/0.40/birchallchapacuran/result-0.40.tsv
0bb527b86ef0fd34a3ae189a1dbeeca447a8953c9355b768724149baf6598559  WORKDIR/runs/2026-10-18-1758/newent/correspondence-SECONDARY/test/0.40/bodtkhobwa/result-0.40.tsv
d5894a9caa796daa69b7b712a20e84aac00f418e63c807440e36f2f334e84e90  WORKDIR/runs/2026-10-18-1758/newent/correspondence-SECONDARY/test/0.40/bremerberta/result-0.40.tsv
722570495d50a7c6f50d7b9b7a2c7c12009d7f4b261adda500223003fb1fa1b8  WORKDIR/runs/2026-10-18-1758/newent/correspondence-SECONDARY/test/0.40/deepadungpalaung/result-0.40.tsv
431aec5713f2c91e33ccd0e02aacd4447cfd3282213ad8189ea1239cae36739a  WORKDIR/runs/2026-10-18-1758/newent/correspondence-SECONDARY/test/0.40/hillburmish/result-0.40.tsv
1e71720bc4e10690c602366fa16886a65db43ee6e06ea735feb4255abe3a172e  WORKDIR/runs/2026-10-18-1758/newent/correspondence-SECONDARY/test/0.40/kesslersignificance/result-0.40.tsv
3531d02d25c7fa05012ab237749beffbfe9e6313bfa7d15b9f0b51dd5352e2b7  WORKDIR/runs/2026-10-18-1758/newent/correspondence-SECONDARY/test/0.40/luangthongkumkaren/result-0.40.tsv
6e3e426df888339c66dec43c8021f4a51ed6bfe6c450fa733c5d730a39a79c8b  WORKDIR/runs/2026-10-18-1758/newent/correspondence-SECONDARY/test/0.40/wangbai/result-0.40.tsv
0d374a8a9571ddc13463dab909c3c938db22ba5ff679c6c852aaedd80bf0ba6e  WORKDIR/runs/2026-10-18-1758/carry/r0202-phylo-PRIMARY/val/0.50/bantubvd/result-0.50.tsv
c6961a03999f4e6c6f4c80fb231f284feb96ce13a84bd7d3d41843ba01ac1b2e  WORKDIR/runs/2026-10-18-1758/carry/r0202-phylo-PRIMARY/val/0.50/beidazihui/result-0.50.tsv
10d28aac82e84525843281d6021beed4b1f8f1154d19e8660cd589c77d4d95cd  WORKDIR/runs/2026-10-18-1758/carry/r0202-phylo-PRIMARY/val/0.50/birchallchapacuran/result-0.50.tsv
661d5c1ba763fa44655547f73d3418f6b144b2c2e94eac7be002ad318ba1f7c6  WORKDIR/runs/2026-10-18-1758/carry/r0202-phylo-PRIMARY/val/0.50/bodtkhobwa/result-0.50.tsv
b6d9817c499745f412b74ff8301ec5c05fa377f6801213ada3e01f9f6bd8957c  WORKDIR/runs/2026-10-18-1758/carry/r0202-phylo-PRIMARY/val/0.50/bremerberta/result-0.50.tsv
83d8b55a08f7f4d02e5d8dd63a03cacb1648d4faa85cd4897f82b371ba8353ec  WORKDIR/runs/2026-10-18-1758/carry/r0202-phylo-PRIMARY/val/0.50/deepadungpalaung/result-0.50.tsv
5edc993f4d05d6a59493119cbc44de3c06d5fe0fec65cda2402c3f5f3445ff15  WORKDIR/runs/2026-10-18-1758/carry/r0202-phylo-PRIMARY/val/0.50/hillburmish/result-0.50.tsv
e6b1e077744d5a9c20f2bf562a9c8a06da0a5ba7e4f33904bccfbc1a61d3e988  WORKDIR/runs/2026-10-18-1758/carry/r0202-phylo-PRIMARY/val/0.50/kesslersignificance/result-0.50.tsv
bbba78dcd1a7c091faae3a9234dad76fb9208f0cced99ce5ac8b3c82dfea2bd2  WORKDIR/runs/2026-10-18-1758/carry/r0202-phylo-PRIMARY/val/0.50/luangthongkumkaren/result-0.50.tsv
e7be0e3791f512b82dbda467774065552bd38587d0328478b11ac652f9d2b153  WORKDIR/runs/2026-10-18-1758/carry/r0202-phylo-PRIMARY/val/0.50/wangbai/result-0.50.tsv
eebfdb9e2f05943e8c2b8952c600c9722730b2463899b5096c2f89365e8481a0  WORKDIR/runs/2026-10-18-1758/carry/r0202-phylo-PRIMARY/test/0.40/bantubvd/result-0.40.tsv
5931b0b0351fb4769007221eb6cf44d2cc624283ba184e8fcc33abaa9e126f0d  WORKDIR/runs/2026-10-18-1758/carry/r0202-phylo-PRIMARY/test/0.40/beidazihui/result-0.40.tsv
750b0bcca215d792b9f3f1a1444401124e53d75ef2e37ca7e91b96d200b0f6f6  WORKDIR/runs/2026-10-18-1758/carry/r0202-phylo-PRIMARY/test/0.40/birchallchapacuran/result-0.40.tsv
3a7a4583f68f05ea98682dcecbee32a4f8a45b7e59bf42055a2679512d8d26cd  WORKDIR/runs/2026-10-18-1758/carry/r0202-phylo-PRIMARY/test/0.40/bodtkhobwa/result-0.40.tsv
63aca1bd3e870df2fc4ff6d9da3a46a0f96497f80a803853955016deea7b5d77  WORKDIR/runs/2026-10-18-1758/carry/r0202-phylo-PRIMARY/test/0.40/bremerberta/result-0.40.tsv
51ba9b08bc17076d545297b370b5e217e78643ea76e222d1db2b001ca5f87fe3  WORKDIR/runs/2026-10-18-1758/carry/r0202-phylo-PRIMARY/test/0.40/deepadungpalaung/result-0.40.tsv
ac3cc891692c7419a0cdc9a1a0da68976067cde8a64f5729a11b23eacefe8403  WORKDIR/runs/2026-10-18-1758/carry/r0202-phylo-PRIMARY/test/0.40/hillburmish/result-0.40.tsv
4a8776525ea346c377b79a8be2a4c1b19703143c012530c5902f3cd1d4a0a54e  WORKDIR/runs/2026-10-18-1758/carry/r0202-phylo-PRIMARY/test/0.40/kesslersignificance/result-0.40.tsv
6e0a4c5fe3c5253859c7c999f2841db96f702a12f0c9e4f1f13bce08ecdc8962  WORKDIR/runs/2026-10-18-1758/carry/r0202-phylo-PRIMARY/test/0.40/luangthongkumkaren/result-0.40.tsv
536011514a93fb50a8c34c59310ee060e630801725097202905e2c681576f55d  WORKDIR/runs/2026-10-18-1758/carry/r0202-phylo-PRIMARY/test/0.40/wangbai/result-0.40.tsv
8c33f872615c41bfc1c1b13be6ecc9cdf7f86a3a981116e975ac93a58262de7e  WORKDIR/runs/2026-10-18-1758/carry/r0839-correspondence-PRIMARY/val/0.50/bantubvd/result-0.50.tsv
352d52a56f1abb0fd4b71e33bdf47f831b820ba36cfc02e7478bf07b6c41af63  WORKDIR/runs/2026-10-18-1758/carry/r0839-correspondence-PRIMARY/val/0.50/beidazihui/result-0.50.tsv
e8440f91304c39b29d2d457232650d9510a126727fdb6c2f7e41d1241a7674ee  WORKDIR/runs/2026-10-18-1758/carry/r0839-correspondence-PRIMARY/val/0.50/birchallchapacuran/result-0.50.tsv
d48bd0650b85567b027a556b5b7524790ddf418b7fdd513cc91c65a80fda55e2  WORKDIR/runs/2026-10-18-1758/carry/r0839-correspondence-PRIMARY/val/0.50/bodtkhobwa/result-0.50.tsv
19546a66cc1fb10fb1eecd841b99419b98b903f16ec63c229919646e46f78071  WORKDIR/runs/2026-10-18-1758/carry/r0839-correspondence-PRIMARY/val/0.50/bremerberta/result-0.50.tsv
a0253fed757d81401439e08e2f1a4c9acb9864f42f24068cbbfaab61db96a797  WORKDIR/runs/2026-10-18-1758/carry/r0839-correspondence-PRIMARY/val/0.50/deepadungpalaung/result-0.50.tsv
86d8cccd68d296fe5b333cb139b8d6b8020641dec8cf531a00c1d462be28f289  WORKDIR/runs/2026-10-18-1758/carry/r0839-correspondence-PRIMARY/val/0.50/hillburmish/result-0.50.tsv
903a3fd0bc8919930dacfbe67b6cda0d500ce9473d07133f2f7c73a8e0812625  WORKDIR/runs/2026-10-18-1758/carry/r0839-correspondence-PRIMARY/val/0.50/kesslersignificance/result-0.50.tsv
c5cc229afd6211f4bfdbe1c6092e8ef45ad503414c67f7c11722ebf894c58958  WORKDIR/runs/2026-10-18-1758/carry/r0839-correspondence-PRIMARY/val/0.50/luangthongkumkaren/result-0.50.tsv
35936983c952dbf496d8e5539fb2312720c3e9c7f7531dd1a8de7be55341ce21  WORKDIR/runs/2026-10-18-1758/carry/r0839-correspondence-PRIMARY/val/0.50/wangbai/result-0.50.tsv
e4cd1d6f132392e827a38419c83e56fb04e1375bf1300b92c8fb492e0163c162  WORKDIR/runs/2026-10-18-1758/carry/r0839-correspondence-PRIMARY/test/0.40/bantubvd/result-0.40.tsv
7118b5a042465f91e8c9bd045d36c8326fa2fc253abe4ba07a48ee1d595b95f4  WORKDIR/runs/2026-10-18-1758/carry/r0839-correspondence-PRIMARY/test/0.40/beidazihui/result-0.40.tsv
dd4d87b79d7cbf02f8c2fdac44e839c879a22e261d58eb54639742dcd38e8b8c  WORKDIR/runs/2026-10-18-1758/carry/r0839-correspondence-PRIMARY/test/0.40/birchallchapacuran/result-0.40.tsv
623aa68b078e67906b02ac5ac7f74154102e67a4154a086a0b0205170a508039  WORKDIR/runs/2026-10-18-1758/carry/r0839-correspondence-PRIMARY/test/0.40/bodtkhobwa/result-0.40.tsv
134ac4929fef2c1c6bbde7fe275e919a3aace2ab968f07f313e0a5ede79c88ac  WORKDIR/runs/2026-10-18-1758/carry/r0839-correspondence-PRIMARY/test/0.40/bremerberta/result-0.40.tsv
9aeaa4488e08e5501bf5378fcd5e162ca44a7f988b336c44856b76eac0fd98a3  WORKDIR/runs/2026-10-18-1758/carry/r0839-correspondence-PRIMARY/test/0.40/deepadungpalaung/result-0.40.tsv
4cb094edf3ad9bfd582d1ed592813bd6592986ea566073a80a8a12ac3c08c3b8  WORKDIR/runs/2026-10-18-1758/carry/r0839-correspondence-PRIMARY/test/0.40/hillburmish/result-0.40.tsv
fa66deb2b3172ce8f0f708a13b862adf0d9ebeaf42751b756f5532bc011ab9d9  WORKDIR/runs/2026-10-18-1758/carry/r0839-correspondence-PRIMARY/test/0.40/kesslersignificance/result-0.40.tsv
b7beadb3624bd91aa481fbee7839c319e5adb3c077a64a72c76923ebbf4f1145  WORKDIR/runs/2026-10-18-1758/carry/r0839-correspondence-PRIMARY/test/0.40/luangthongkumkaren/result-0.40.tsv
1c7c0988b3e8163959df4d7610bce6337bd0178250422bf4fc928717949537ee  WORKDIR/runs/2026-10-18-1758/carry/r0839-correspondence-PRIMARY/test/0.40/wangbai/result-0.40.tsv
cfbca1b8fc43227ba7dad8aeddf6d9afccf4787bffd43e0da2f94a6b59df158b  WORKDIR/runs/2026-10-18-1758/carry/r0839-correspondence-SECONDARY/val/0.50/bantubvd/result-0.50.tsv
db729da9e86bb57ac0ca12390a9541e83a86e94ea8a63875106632e3c56e1bc6  WORKDIR/runs/2026-10-18-1758/carry/r0839-correspondence-SECONDARY/val/0.50/beidazihui/result-0.50.tsv
77f225b86e2d57ec91fbfd4f1c69dbdd26b544adbfd750580f349892e61e7886  WORKDIR/runs/2026-10-18-1758/carry/r0839-correspondence-SECONDARY/val/0.50/birchallchapacuran/result-0.50.tsv
74cb944ece1a048137027b6f884a3013c44ba2f13c8da226dd6dda7adfe6e07f  WORKDIR/runs/2026-10-18-1758/carry/r0839-correspondence-SECONDARY/val/0.50/bodtkhobwa/result-0.50.tsv
0b6361a63d5740f50bd41c2ae3b3400a3628a7ff1d2311f2d53d29fbbb3c3299  WORKDIR/runs/2026-10-18-1758/carry/r0839-correspondence-SECONDARY/val/0.50/bremerberta/result-0.50.tsv
2f7a9bf2f9a11ff5aefe49d5774b0efb6d5b5c0797964caa2f0bc629c1ddf739  WORKDIR/runs/2026-10-18-1758/carry/r0839-correspondence-SECONDARY/val/0.50/deepadungpalaung/result-0.50.tsv
e3814797362b02d571c04e7f7b899689a3a52d4665263d0b1214fbc5293110fb  WORKDIR/runs/2026-10-18-1758/carry/r0839-correspondence-SECONDARY/val/0.50/hillburmish/result-0.50.tsv
38f7c1888e22dc27bb78796b95e78a84786fcdf3bbf399b59e54699948fe86bb  WORKDIR/runs/2026-10-18-1758/carry/r0839-correspondence-SECONDARY/val/0.50/kesslersignificance/result-0.50.tsv
246322ba50bb6a49bf449b65874183771386a3cbfc3093f061fa04801b26873c  WORKDIR/runs/2026-10-18-1758/carry/r0839-correspondence-SECONDARY/val/0.50/luangthongkumkaren/result-0.50.tsv
1c0eb52c5cf0eb38b74dcac006f0baa0eb04e8ba5bc13a2072b8fa9f4794e192  WORKDIR/runs/2026-10-18-1758/carry/r0839-correspondence-SECONDARY/val/0.50/wangbai/result-0.50.tsv
b20f5936b552ba673baab3deeda2271cd3ea3cd0c437ca1e35e5d01e08aa0af5  WORKDIR/runs/2026-10-18-1758/carry/r0839-correspondence-SECONDARY/test/0.40/bantubvd/result-0.40.tsv
78d6d84eee74e59bf5044244efeb6257fc235586c6505004bb86e2f3e7db52fb  WORKDIR/runs/2026-10-18-1758/carry/r0839-correspondence-SECONDARY/test/0.40/beidazihui/result-0.40.tsv
48cbb22ad5f65b45e36d27738cd4a6980a678f9cb8f3531ddf417d7ccbba9912  WORKDIR/runs/2026-10-18-1758/carry/r0839-correspondence-SECONDARY/test/0.40/birchallchapacuran/result-0.40.tsv
d99e1210fbf412ab73d9942b6d86a53c41155c5ba73450790ff4dce1f344a94b  WORKDIR/runs/2026-10-18-1758/carry/r0839-correspondence-SECONDARY/test/0.40/bodtkhobwa/result-0.40.tsv
1761d33c82998fee9150bbedfe66c274d4938fd69dea938d1415e17fd50feef6  WORKDIR/runs/2026-10-18-1758/carry/r0839-correspondence-SECONDARY/test/0.40/bremerberta/result-0.40.tsv
8907a444b38344e36ba92796cac3ac6775ee22c9a01199dbc0d81b75c7568e9b  WORKDIR/runs/2026-10-18-1758/carry/r0839-correspondence-SECONDARY/test/0.40/deepadungpalaung/result-0.40.tsv
eb2667faf4887820ba5948a7db41fa89dc97baebfcd590eddfe65a7601ba333e  WORKDIR/runs/2026-10-18-1758/carry/r0839-correspondence-SECONDARY/test/0.40/hillburmish/result-0.40.tsv
7df265347be62e9dd49a5a16a94250397df056e70917cffcbf529012066b2424  WORKDIR/runs/2026-10-18-1758/carry/r0839-correspondence-SECONDARY/test/0.40/kesslersignificance/result-0.40.tsv
e963b30152990d1c6143cb29c8fb6b46cd35677a25acf450a6a1b1551c31f9ac  WORKDIR/runs/2026-10-18-1758/carry/r0839-correspondence-SECONDARY/test/0.40/luangthongkumkaren/result-0.40.tsv
7718016de4160362eabd36a91a16b26836b6f1922818b6e1cd65947313fd0267  WORKDIR/runs/2026-10-18-1758/carry/r0839-correspondence-SECONDARY/test/0.40/wangbai/result-0.40.tsv
79ceb6a75d8ffd7895774a7f165592e24b88342eb6bdfd720df121c2a635e8d4  WORKDIR/runs/2026-10-18-1758/carry/r0839-transducer-PRIMARY/val/0.50/bantubvd/result-0.50.tsv
818eb5f31196913ec02c1ca5eb92e67370b18d0bccbcdebd262d33529e88b822  WORKDIR/runs/2026-10-18-1758/carry/r0839-transducer-PRIMARY/val/0.50/beidazihui/result-0.50.tsv
445ebbb43b815d854ee43b51239a73c2b3390500a4eac79c215e62837d6ba700  WORKDIR/runs/2026-10-18-1758/carry/r0839-transducer-PRIMARY/val/0.50/birchallchapacuran/result-0.50.tsv
ee14884cf5332f3f5da055eedc7e13ad06c227079489d530b4e26ca5e009c7f0  WORKDIR/runs/2026-10-18-1758/carry/r0839-transducer-PRIMARY/val/0.50/bodtkhobwa/result-0.50.tsv
65cb74b235f09116da5fb0c0a3bf4c3e2cd4c8ab78aa3565989f9198e68c7c90  WORKDIR/runs/2026-10-18-1758/carry/r0839-transducer-PRIMARY/val/0.50/bremerberta/result-0.50.tsv
493d14c3f07c3e5dfd34891ca323e1fa84a27083fd83311386ad539cca5af588  WORKDIR/runs/2026-10-18-1758/carry/r0839-transducer-PRIMARY/val/0.50/deepadungpalaung/result-0.50.tsv
7804325cb6d449cc1113e30496edee10aa130d624c77a70cc9556da6accfb589  WORKDIR/runs/2026-10-18-1758/carry/r0839-transducer-PRIMARY/val/0.50/hillburmish/result-0.50.tsv
665bc35262d7d2d38f6e4a16441db96e571d4fce1a39ae332e0b677e26c834d0  WORKDIR/runs/2026-10-18-1758/carry/r0839-transducer-PRIMARY/val/0.50/kesslersignificance/result-0.50.tsv
8a43c095501bc4a882d38c3cb7aa2afe5cc6af021075a00147ef1a46a4ffb07c  WORKDIR/runs/2026-10-18-1758/carry/r0839-transducer-PRIMARY/val/0.50/luangthongkumkaren/result-0.50.tsv
c0fde0f7ab3ee2139300054c1d82ff926a57383fadf851a9acf5a7fbd4984203  WORKDIR/runs/2026-10-18-1758/carry/r0839-transducer-PRIMARY/val/0.50/wangbai/result-0.50.tsv
949f3257f98820b4fa8ec3d8d0361071727a5cd23742f6c3e3ab23482579e993  WORKDIR/runs/2026-10-18-1758/carry/r0839-transducer-PRIMARY/test/0.40/bantubvd/result-0.40.tsv
5252662e11d8a7d642b91ae0f801b51ffb4aef8412e4af62a8786fde7a558f97  WORKDIR/runs/2026-10-18-1758/carry/r0839-transducer-PRIMARY/test/0.40/beidazihui/result-0.40.tsv
f638c5930fe392f4302179d9f18f13458d683cb959407420fe00990bcec47826  WORKDIR/runs/2026-10-18-1758/carry/r0839-transducer-PRIMARY/test/0.40/birchallchapacuran/result-0.40.tsv
ac3a8d863ca65583a8a34b9cc78c81bd56c663b8bbd51e19e6863fe7852624fc  WORKDIR/runs/2026-10-18-1758/carry/r0839-transducer-PRIMARY/test/0.40/bodtkhobwa/result-0.40.tsv
d4200b7508b5bd80b4b8150b47480ef08d0c981c74715a06eedf1da989463612  WORKDIR/runs/2026-10-18-1758/carry/r0839-transducer-PRIMARY/test/0.40/bremerberta/result-0.40.tsv
25658d23368e8e24b82e43d997d038b238eed4a4837ffbc7a0f5a3dfcd77a79f  WORKDIR/runs/2026-10-18-1758/carry/r0839-transducer-PRIMARY/test/0.40/deepadungpalaung/result-0.40.tsv
c479f255abeb8a2bfdef1ccbaadf8a1f82e217b2325314b98f391d83bfb4ce3d  WORKDIR/runs/2026-10-18-1758/carry/r0839-transducer-PRIMARY/test/0.40/hillburmish/result-0.40.tsv
002152ca11e692d8c06291e3e8e4530b2a1fc7dc246428e61c1c73c33013cdd0  WORKDIR/runs/2026-10-18-1758/carry/r0839-transducer-PRIMARY/test/0.40/kesslersignificance/result-0.40.tsv
5c852b54545bd52d707da5dea9d60474f418c9d69aba748715dab7716ee432f9  WORKDIR/runs/2026-10-18-1758/carry/r0839-transducer-PRIMARY/test/0.40/luangthongkumkaren/result-0.40.tsv
82656ffe2d31b6f049ad61d50e1027e3fe1ecce8cdf7270c67c95aef688a0f61  WORKDIR/runs/2026-10-18-1758/carry/r0839-transducer-PRIMARY/test/0.40/wangbai/result-0.40.tsv
4a9330ff83e084ac6d92b1a185ed2724d75d0c4bc1b05ae3596c10f996bcba02  WORKDIR/runs/2026-10-18-1758/carry/r0202-analogist-PRIMARY/val/0.50/bantubvd/result-0.50.tsv
f6ff416362be610e178c96cd07dcf97f6d94cc52dc5be595a2bd2fc3387367b3  WORKDIR/runs/2026-10-18-1758/carry/r0202-analogist-PRIMARY/val/0.50/beidazihui/result-0.50.tsv
f22455de8da7167aa91443f8c108ab7118a4c8b466c272ae1839835bc41ce119  WORKDIR/runs/2026-10-18-1758/carry/r0202-analogist-PRIMARY/val/0.50/birchallchapacuran/result-0.50.tsv
558cea5ff6873ecf79020dfa2cbbf64e949e2297edc73a19b4a07c48dff174fb  WORKDIR/runs/2026-10-18-1758/carry/r0202-analogist-PRIMARY/val/0.50/bodtkhobwa/result-0.50.tsv
c41ea5a4a18e1f64598ce21d2dfdb02d31b4cdb24061d643da054bf9197ee508  WORKDIR/runs/2026-10-18-1758/carry/r0202-analogist-PRIMARY/val/0.50/bremerberta/result-0.50.tsv
a1563eab6326a859d4e50e5c11c8e299a6259eae6222b91619b123d5359491d4  WORKDIR/runs/2026-10-18-1758/carry/r0202-analogist-PRIMARY/val/0.50/deepadungpalaung/result-0.50.tsv
ca25bf352920bd5b16d74224c060f25dcb40394ed6b92721afdd3155ee6a3cc9  WORKDIR/runs/2026-10-18-1758/carry/r0202-analogist-PRIMARY/val/0.50/hillburmish/result-0.50.tsv
4831e5f374bae381005ee53f70f92498cbed717dd998970ffdf805757fc026c6  WORKDIR/runs/2026-10-18-1758/carry/r0202-analogist-PRIMARY/val/0.50/kesslersignificance/result-0.50.tsv
70f5517e58726b4f6922d87a7512c8e4369ec0966de7f4f2f45922df6069639a  WORKDIR/runs/2026-10-18-1758/carry/r0202-analogist-PRIMARY/val/0.50/luangthongkumkaren/result-0.50.tsv
5f01bccc70c66b8979be14d4881e16a6331b961ec171ff8cbd95a9b1b7abef3b  WORKDIR/runs/2026-10-18-1758/carry/r0202-analogist-PRIMARY/val/0.50/wangbai/result-0.50.tsv
7c6aa58218834403271cd7e884b60e079bb17280d90de84d17d70e9e885be702  WORKDIR/runs/2026-10-18-1758/carry/r0202-analogist-PRIMARY/test/0.40/bantubvd/result-0.40.tsv
9ab637f22acd66a0034c9c5bf53dcdb01b94f5831ed30c2d8443761cd8526caa  WORKDIR/runs/2026-10-18-1758/carry/r0202-analogist-PRIMARY/test/0.40/beidazihui/result-0.40.tsv
3b62a58969590ac94668cbe5fd27df8fa72980d14e44bef5b6401a7b3d39b432  WORKDIR/runs/2026-10-18-1758/carry/r0202-analogist-PRIMARY/test/0.40/birchallchapacuran/result-0.40.tsv
9f0826afae57197a417b512aaa0f8d0d13ffa38ff72baaceca214525e5fdbc8e  WORKDIR/runs/2026-10-18-1758/carry/r0202-analogist-PRIMARY/test/0.40/bodtkhobwa/result-0.40.tsv
12d22bf6fab778d99047883cd62f084ccee8bb7088eef75860f294eddf0bd9cc  WORKDIR/runs/2026-10-18-1758/carry/r0202-analogist-PRIMARY/test/0.40/bremerberta/result-0.40.tsv
7adc6e3dd9f5bd516ddf4626008345efcc2fd14dc363c8e1af3a52310cf96698  WORKDIR/runs/2026-10-18-1758/carry/r0202-analogist-PRIMARY/test/0.40/deepadungpalaung/result-0.40.tsv
90e14829920e7b76ea4114a44985ec2bc57f117135be704552efe58fa5935ac2  WORKDIR/runs/2026-10-18-1758/carry/r0202-analogist-PRIMARY/test/0.40/hillburmish/result-0.40.tsv
146fc64301f6c897c0d112fe82c3c3a21ddd561b51abfc1afc39ce1f13ae1d62  WORKDIR/runs/2026-10-18-1758/carry/r0202-analogist-PRIMARY/test/0.40/kesslersignificance/result-0.40.tsv
9e8b8af512468307c21204c7b86398c9798595072f0885478b2afb53ee79e44a  WORKDIR/runs/2026-10-18-1758/carry/r0202-analogist-PRIMARY/test/0.40/luangthongkumkaren/result-0.40.tsv
969221f2a0d16ae04b06f84db360ed1fb77ec54a3a0afdbd0f2c835d650f545d  WORKDIR/runs/2026-10-18-1758/carry/r0202-analogist-PRIMARY/test/0.40/wangbai/result-0.40.tsv
efba3ac92c28b0833ce7c5ad7d1613485f190491a4385c8d850893a39fd7430c  WORKDIR/runs/2026-10-18-1758/carry/r0202-classifier-PRIMARY/val/0.50/bantubvd/result-0.50.tsv
67cea2eff575e35855dae507683d7486e155418e5d881f76a09fc0c32d349688  WORKDIR/runs/2026-10-18-1758/carry/r0202-classifier-PRIMARY/val/0.50/beidazihui/result-0.50.tsv
ec214dfc7e357754c0e9b4c7417bd152c85358b9979917266c05720e1c471803  WORKDIR/runs/2026-10-18-1758/carry/r0202-classifier-PRIMARY/val/0.50/birchallchapacuran/result-0.50.tsv
dd5ecfc09d35e2e61e593f58be91125cb1c9ab4d95e7f9c71c572d5805c96f47  WORKDIR/runs/2026-10-18-1758/carry/r0202-classifier-PRIMARY/val/0.50/bodtkhobwa/result-0.50.tsv
8dd62221b211ff8ba7b248c5c9316ac8550404ac18a403611538357615b39885  WORKDIR/runs/2026-10-18-1758/carry/r0202-classifier-PRIMARY/val/0.50/bremerberta/result-0.50.tsv
a5c84e828b37026766f041976c74c2081815d2d34f9c582a585b1f8266923544  WORKDIR/runs/2026-10-18-1758/carry/r0202-classifier-PRIMARY/val/0.50/deepadungpalaung/result-0.50.tsv
e1ee89b71c745e9b2a18ddb681dfd96645cf2ddd85114a330ddb1eb67130c5c9  WORKDIR/runs/2026-10-18-1758/carry/r0202-classifier-PRIMARY/val/0.50/hillburmish/result-0.50.tsv
e036ecef1afaeec1b4796abafa5490cde9a055227381ba68f5d168be66d668e2  WORKDIR/runs/2026-10-18-1758/carry/r0202-classifier-PRIMARY/val/0.50/kesslersignificance/result-0.50.tsv
d60d6b0bf445ea27301600b9c923890979416c0be37ddd0735442b36fab8da54  WORKDIR/runs/2026-10-18-1758/carry/r0202-classifier-PRIMARY/val/0.50/luangthongkumkaren/result-0.50.tsv
0aa4cddfe6b412f35cb761928eb67a065df488bd22199b0e53e66d5fea606b2a  WORKDIR/runs/2026-10-18-1758/carry/r0202-classifier-PRIMARY/val/0.50/wangbai/result-0.50.tsv
cbf74c9d5562246ed0b6334bffff11e3110432b136bc4b791ef2f75b6c0eedd0  WORKDIR/runs/2026-10-18-1758/carry/r0202-classifier-PRIMARY/test/0.40/bantubvd/result-0.40.tsv
096c896ef22e806cab60db5346925328f219d95cb40ec2ddfe67b0ffc701efbf  WORKDIR/runs/2026-10-18-1758/carry/r0202-classifier-PRIMARY/test/0.40/beidazihui/result-0.40.tsv
d0552eedfaa713424f1d5672a72fc5c35874bcd26767c3b659ece6166751ca12  WORKDIR/runs/2026-10-18-1758/carry/r0202-classifier-PRIMARY/test/0.40/birchallchapacuran/result-0.40.tsv
f35f7dd43be6dd5b3f92b5292c978519bcef39c236bbfaa6103f31f1dc16a86e  WORKDIR/runs/2026-10-18-1758/carry/r0202-classifier-PRIMARY/test/0.40/bodtkhobwa/result-0.40.tsv
f821a602e8e916548a8f76111d37a494a67f83541782d14492a9b9c90e69e7c7  WORKDIR/runs/2026-10-18-1758/carry/r0202-classifier-PRIMARY/test/0.40/bremerberta/result-0.40.tsv
ed6ebcc23ab15f87e6fcf436866193f28e8a549e95ce0e993073668f627f0d96  WORKDIR/runs/2026-10-18-1758/carry/r0202-classifier-PRIMARY/test/0.40/deepadungpalaung/result-0.40.tsv
69d4bc0fdfd7db641e3c04a38b200e90c0c90ce9bbd02eaee2697ac01ceb0c67  WORKDIR/runs/2026-10-18-1758/carry/r0202-classifier-PRIMARY/test/0.40/hillburmish/result-0.40.tsv
1d1c435e611176c39803d57d34c6f3d2d97cbf72eed57bfad8572c67f97881df  WORKDIR/runs/2026-10-18-1758/carry/r0202-classifier-PRIMARY/test/0.40/kesslersignificance/result-0.40.tsv
c3465c26673311d40d5ee97b0507c17f31d8a1f5d5d7740fef27301b1ab147b9  WORKDIR/runs/2026-10-18-1758/carry/r0202-classifier-PRIMARY/test/0.40/luangthongkumkaren/result-0.40.tsv
3b81cc6b00dac4de21ec927909cc88be0b23ce961fc61137eed31fecb045ebeb  WORKDIR/runs/2026-10-18-1758/carry/r0202-classifier-PRIMARY/test/0.40/wangbai/result-0.40.tsv
e72b85ae70b2be05494fff8ef20d63272568c17f5469ee4ea69c52875b201ab7  WORKDIR/runs/2026-10-18-1758/carry/r0202-correspondence-SECONDARY/val/0.50/bantubvd/result-0.50.tsv
458705a33d1ae1dd26000e8d977f7822297a2a3753d379e940cf0a10bcd6e283  WORKDIR/runs/2026-10-18-1758/carry/r0202-correspondence-SECONDARY/val/0.50/beidazihui/result-0.50.tsv
9ebcf92b589f1a55be4b98f95102b82ad3221c7df2a0ce95ed83c7986fbce3da  WORKDIR/runs/2026-10-18-1758/carry/r0202-correspondence-SECONDARY/val/0.50/birchallchapacuran/result-0.50.tsv
4bc0f6601f25688bec6aed856ac780029940e16788ea20d4ce55bf3da8d8e33f  WORKDIR/runs/2026-10-18-1758/carry/r0202-correspondence-SECONDARY/val/0.50/bodtkhobwa/result-0.50.tsv
dc04ea5b1ecea23bb22caf8bd0a669a6169f60ffdd52509587917c98fe500851  WORKDIR/runs/2026-10-18-1758/carry/r0202-correspondence-SECONDARY/val/0.50/bremerberta/result-0.50.tsv
29ab7711d50679799a9ad31b0084b80da748e5a163a8770ea34f490cc201ac57  WORKDIR/runs/2026-10-18-1758/carry/r0202-correspondence-SECONDARY/val/0.50/deepadungpalaung/result-0.50.tsv
88d057c0ef357c6a5ac2d8432b5fa06bae508f4af9362aaac9d1300839659af3  WORKDIR/runs/2026-10-18-1758/carry/r0202-correspondence-SECONDARY/val/0.50/hillburmish/result-0.50.tsv
600a432b560e037ff6331dc59e9103a6e6d1fd13d4d98a0b9fe964ce445dd142  WORKDIR/runs/2026-10-18-1758/carry/r0202-correspondence-SECONDARY/val/0.50/kesslersignificance/result-0.50.tsv
0e018a13d8e844ce697b115e994718544621e08d8059f7ac4631ed6492b6c83e  WORKDIR/runs/2026-10-18-1758/carry/r0202-correspondence-SECONDARY/val/0.50/luangthongkumkaren/result-0.50.tsv
dc954f85f5d75dc6d1d5363e9ac4795975b2a6194dbb20f980a48c34f8dd5e1d  WORKDIR/runs/2026-10-18-1758/carry/r0202-correspondence-SECONDARY/val/0.50/wangbai/result-0.50.tsv
4271ea4ff384ef7357692608885a0e977d3f3b5885f851076ae09775a43c85db  WORKDIR/runs/2026-10-18-1758/carry/r0202-correspondence-SECONDARY/test/0.40/bantubvd/result-0.40.tsv
a93bb1a0c2d027c9f434ec7a3fd85775469e358b677e8a57958b20693120eef3  WORKDIR/runs/2026-10-18-1758/carry/r0202-correspondence-SECONDARY/test/0.40/beidazihui/result-0.40.tsv
80a6fe963cf8abc27c418ef4023d9fe035499dee13c3efa278c464fd22088d6f  WORKDIR/runs/2026-10-18-1758/carry/r0202-correspondence-SECONDARY/test/0.40/birchallchapacuran/result-0.40.tsv
e112e284f910972ea37939397c313239a77bb87f0b8871ccab6a2f0064e2fbf1  WORKDIR/runs/2026-10-18-1758/carry/r0202-correspondence-SECONDARY/test/0.40/bodtkhobwa/result-0.40.tsv
911972d8e7f2b6ea68a1aee5b3a3ff6b5b2c0f94136d095aea43a2f738c93d58  WORKDIR/runs/2026-10-18-1758/carry/r0202-correspondence-SECONDARY/test/0.40/bremerberta/result-0.40.tsv
9b61809dfef3dc47f5280b9fcd040748d157ade8cc6b40603cbb9e45f69bc434  WORKDIR/runs/2026-10-18-1758/carry/r0202-correspondence-SECONDARY/test/0.40/deepadungpalaung/result-0.40.tsv
9d3d8db195bdeecfff48458db3eee6c90cae3543530cbb73b1c00f2005ff8027  WORKDIR/runs/2026-10-18-1758/carry/r0202-correspondence-SECONDARY/test/0.40/hillburmish/result-0.40.tsv
630bc1e36a711722eded7e4bfef39c5a825fe82b3f7dd16f74a0e21d5fe4cb70  WORKDIR/runs/2026-10-18-1758/carry/r0202-correspondence-SECONDARY/test/0.40/kesslersignificance/result-0.40.tsv
0d2af42a53ce6d8dd67d877ef043043e55b02b50115858eaf5d450a5a06e55e2  WORKDIR/runs/2026-10-18-1758/carry/r0202-correspondence-SECONDARY/test/0.40/luangthongkumkaren/result-0.40.tsv
adfc14e576192a99a69d7faf8d6f580c399e5cb4a4a0716e33d21bd8906fd82a  WORKDIR/runs/2026-10-18-1758/carry/r0202-correspondence-SECONDARY/test/0.40/wangbai/result-0.40.tsv
e72b85ae70b2be05494fff8ef20d63272568c17f5469ee4ea69c52875b201ab7  WORKDIR/runs/2026-10-18-1758/carry/r0202-correspondence-PRIMARY/val/0.50/bantubvd/result-0.50.tsv
d2d89e5aa44ab7d3b35a7ef3af0bbead3414b003323ca3f3a66cc8206e9984d7  WORKDIR/runs/2026-10-18-1758/carry/r0202-correspondence-PRIMARY/val/0.50/beidazihui/result-0.50.tsv
c600f5a0ef5dcb6f4aef6bfff904256d479cd20e9b7285a032b9312b2b95cb54  WORKDIR/runs/2026-10-18-1758/carry/r0202-correspondence-PRIMARY/val/0.50/birchallchapacuran/result-0.50.tsv
7691ede702c7167cbff2ccff0cd36ae1d24eb4dbff210361c96ec7e69c5411d3  WORKDIR/runs/2026-10-18-1758/carry/r0202-correspondence-PRIMARY/val/0.50/bodtkhobwa/result-0.50.tsv
dc04ea5b1ecea23bb22caf8bd0a669a6169f60ffdd52509587917c98fe500851  WORKDIR/runs/2026-10-18-1758/carry/r0202-correspondence-PRIMARY/val/0.50/bremerberta/result-0.50.tsv
962263d411176f3bd94d36c135b89c5c54b342cc1fa60a8729d6b20594e801e3  WORKDIR/runs/2026-10-18-1758/carry/r0202-correspondence-PRIMARY/val/0.50/deepadungpalaung/result-0.50.tsv
76995ddd74d68f7a01f121ebe268623775a4ff8ddfee46d5ad724c9af671780c  WORKDIR/runs/2026-10-18-1758/carry/r0202-correspondence-PRIMARY/val/0.50/hillburmish/result-0.50.tsv
39e67048f06b58f2992d4fbbdccc1c94a9ae2b12fe76f033b2be2e58ec06a778  WORKDIR/runs/2026-10-18-1758/carry/r0202-correspondence-PRIMARY/val/0.50/kesslersignificance/result-0.50.tsv
221b04d0b0aa586b053e2d6647dd7a229e64926fe06dd5ac61729a3c6225c7dd  WORKDIR/runs/2026-10-18-1758/carry/r0202-correspondence-PRIMARY/val/0.50/luangthongkumkaren/result-0.50.tsv
9eabdb633376416407f8a68050427b0d10f07b1861e4346ee89e7c0cee822c92  WORKDIR/runs/2026-10-18-1758/carry/r0202-correspondence-PRIMARY/val/0.50/wangbai/result-0.50.tsv
6346eaa2f337a313e937da746594e4589569c6899af7a8403246680c6de5e731  WORKDIR/runs/2026-10-18-1758/carry/r0202-correspondence-PRIMARY/test/0.40/bantubvd/result-0.40.tsv
e448ea10f868a9fef978999499307dfe837a4ba49ad7faa2169712d0f5c3bfde  WORKDIR/runs/2026-10-18-1758/carry/r0202-correspondence-PRIMARY/test/0.40/beidazihui/result-0.40.tsv
d02acc798dadbdd5c72bb6fb26d6b5696d53ef7e9c1498cbdc3d5ecb00b5ed10  WORKDIR/runs/2026-10-18-1758/carry/r0202-correspondence-PRIMARY/test/0.40/birchallchapacuran/result-0.40.tsv
d02d8cdf5846f5473cf319df666fe0d492e4c051e1abc73910bcb7de31361134  WORKDIR/runs/2026-10-18-1758/carry/r0202-correspondence-PRIMARY/test/0.40/bodtkhobwa/result-0.40.tsv
bdde69defac799ac6c9e436a312f627a1aa72f06baf9bf886e2c87975a9c29b0  WORKDIR/runs/2026-10-18-1758/carry/r0202-correspondence-PRIMARY/test/0.40/bremerberta/result-0.40.tsv
0d6c88951c731afeb2ab246fa8b232ac7f40d823cbf5f33aa6766a8c5338a0f3  WORKDIR/runs/2026-10-18-1758/carry/r0202-correspondence-PRIMARY/test/0.40/deepadungpalaung/result-0.40.tsv
b02c7c32ab456bac74fe9be6cc78cba8dee025586638b0906801c7133b89e2bf  WORKDIR/runs/2026-10-18-1758/carry/r0202-correspondence-PRIMARY/test/0.40/hillburmish/result-0.40.tsv
441aa688d93e0c11dd26cd64587965d9e9c63778db661820b1daf6e42283ea37  WORKDIR/runs/2026-10-18-1758/carry/r0202-correspondence-PRIMARY/test/0.40/kesslersignificance/result-0.40.tsv
86c23c88cc286f85dea95d4c06c578d685e15bcb02f0cd4ab6a8d0a32fbf50e2  WORKDIR/runs/2026-10-18-1758/carry/r0202-correspondence-PRIMARY/test/0.40/luangthongkumkaren/result-0.40.tsv
ebde98145f35d15737d2a2b69eac499c4c51ec8bbe3d89752d50afd16e5039e9  WORKDIR/runs/2026-10-18-1758/carry/r0202-correspondence-PRIMARY/test/0.40/wangbai/result-0.40.tsv
279227377db0ebaa2a19114cc4832ca6c7932ab68c98968c0904a751361e49a2  WORKDIR/runs/2026-10-18-1758/carry/r0202-classifier-SECONDARY/val/0.50/bantubvd/result-0.50.tsv
0e9afa9f151cfedc6161ccd5d816024c5f9c51d599a4e56fcdff5691b0389136  WORKDIR/runs/2026-10-18-1758/carry/r0202-classifier-SECONDARY/val/0.50/beidazihui/result-0.50.tsv
91faaf0f3ab4989cf870e3adbbf465baee6b908b83c8b07629f17b22bd66f3be  WORKDIR/runs/2026-10-18-1758/carry/r0202-classifier-SECONDARY/val/0.50/birchallchapacuran/result-0.50.tsv
d279ebbd996b36ac7209e20ac853ba0d52c9ed7c1a4264800a62a211de5dddcc  WORKDIR/runs/2026-10-18-1758/carry/r0202-classifier-SECONDARY/val/0.50/bodtkhobwa/result-0.50.tsv
1b2cc0360129d0ee25a69dd48c9889eddd5d9d6131a2e559601916178e67c838  WORKDIR/runs/2026-10-18-1758/carry/r0202-classifier-SECONDARY/val/0.50/bremerberta/result-0.50.tsv
bc5235b7beb0bf5e1fd9dd127dbad313d9d61cabb90b77bbb0d27f77510db3aa  WORKDIR/runs/2026-10-18-1758/carry/r0202-classifier-SECONDARY/val/0.50/deepadungpalaung/result-0.50.tsv
45881fb236eed054c713ed93b31280e31c147777aa78f3516ed612aa53b46ce6  WORKDIR/runs/2026-10-18-1758/carry/r0202-classifier-SECONDARY/val/0.50/hillburmish/result-0.50.tsv
724098cab700d071a7b92b0c1893a3449ee55fb66527178985d423b205b2e05e  WORKDIR/runs/2026-10-18-1758/carry/r0202-classifier-SECONDARY/val/0.50/kesslersignificance/result-0.50.tsv
09607d58539164525515b772b0178ae76ca9ff5ef1405c5d3c2b6a8f8a2b5394  WORKDIR/runs/2026-10-18-1758/carry/r0202-classifier-SECONDARY/val/0.50/luangthongkumkaren/result-0.50.tsv
4f0dd3a58afaacb53f02bbc23a3d69dcc872519697fc04e6dee62393235e20c4  WORKDIR/runs/2026-10-18-1758/carry/r0202-classifier-SECONDARY/val/0.50/wangbai/result-0.50.tsv
c29240af673c7170f64f5f3ae22a1acfd5396c2b1339d4459fc48d4d459b7e71  WORKDIR/runs/2026-10-18-1758/carry/r0202-classifier-SECONDARY/test/0.40/bantubvd/result-0.40.tsv
3216c8e736544476dc6b9c42908ae4fcca1553e4660a4817991cbde93de998da  WORKDIR/runs/2026-10-18-1758/carry/r0202-classifier-SECONDARY/test/0.40/beidazihui/result-0.40.tsv
eba9ee23e7aea729038502d11a3561a145b16c4500aeaf03573f4ebf863fa689  WORKDIR/runs/2026-10-18-1758/carry/r0202-classifier-SECONDARY/test/0.40/birchallchapacuran/result-0.40.tsv
88406fef24afaf67fbd7fb357dbdedd19283390ab902f269644f759302924268  WORKDIR/runs/2026-10-18-1758/carry/r0202-classifier-SECONDARY/test/0.40/bodtkhobwa/result-0.40.tsv
7590bb77a7f838c7170d74f9aeb56e0e9c55e2990503d83fbe846d47c555a2d3  WORKDIR/runs/2026-10-18-1758/carry/r0202-classifier-SECONDARY/test/0.40/bremerberta/result-0.40.tsv
37b5bf7fa9903a0372639f6a66c3424cd43f02b7077c71ad7f9ef5a82623e70b  WORKDIR/runs/2026-10-18-1758/carry/r0202-classifier-SECONDARY/test/0.40/deepadungpalaung/result-0.40.tsv
b8c0f4466efefc0503f814a18d8277ff2fa20bb5e1b548f6e015b9f60894fa35  WORKDIR/runs/2026-10-18-1758/carry/r0202-classifier-SECONDARY/test/0.40/hillburmish/result-0.40.tsv
d4fdd3a21e2afe22ca02f90948b4e589aef52c667667e8dd339b37dbbd796dd4  WORKDIR/runs/2026-10-18-1758/carry/r0202-classifier-SECONDARY/test/0.40/kesslersignificance/result-0.40.tsv
b1deddbba41f719a912fd7cfa0dff4ff8c14fe562972969334d12ee6f1d52f94  WORKDIR/runs/2026-10-18-1758/carry/r0202-classifier-SECONDARY/test/0.40/luangthongkumkaren/result-0.40.tsv
51b6b02b05f676dd319b5d0b967bf48823f4ac203f9504a8ff92835fcff4bbd7  WORKDIR/runs/2026-10-18-1758/carry/r0202-classifier-SECONDARY/test/0.40/wangbai/result-0.40.tsv
1ea877c1d5c3e6f9addeae647be96bcc4c4b2292c3fd36a1c38f362b6adc9ab3  WORKDIR/runs/2026-10-18-1758/newent/smuggler-PRIMARY/val/0.50/bantubvd/result-0.50.tsv
0423e14fbadc237e10ec47a487ef796fff6a4e6e21129a8ff7ab0b4aaa59be1c  WORKDIR/runs/2026-10-18-1758/newent/smuggler-PRIMARY/val/0.50/beidazihui/result-0.50.tsv
9fb4465c2545a00666005f5e071aae1e93c6c86501eba8f625c489d932c7a570  WORKDIR/runs/2026-10-18-1758/newent/smuggler-PRIMARY/val/0.50/birchallchapacuran/result-0.50.tsv
86fc6213ad4d2533155e96b5439bd0729b07465794adb78996e58de26648f029  WORKDIR/runs/2026-10-18-1758/newent/smuggler-PRIMARY/val/0.50/bodtkhobwa/result-0.50.tsv
a8f4b23e544ecd5c9d3456a806376520ab800c9525c0ef532101b127a945416f  WORKDIR/runs/2026-10-18-1758/newent/smuggler-PRIMARY/val/0.50/bremerberta/result-0.50.tsv
ee8dcc75554998e29d3d787983da71d3768b9280a367ac0ed75d058e91edcc3a  WORKDIR/runs/2026-10-18-1758/newent/smuggler-PRIMARY/val/0.50/deepadungpalaung/result-0.50.tsv
79c13e706ac5abeb9fcc8ed8bc6f098329cb41142561ca5d2a2c2b945d42107f  WORKDIR/runs/2026-10-18-1758/newent/smuggler-PRIMARY/val/0.50/hillburmish/result-0.50.tsv
0e69d3181debab46ab4ef50fde027279485335d2caffa60e5edb79688b90e22e  WORKDIR/runs/2026-10-18-1758/newent/smuggler-PRIMARY/val/0.50/kesslersignificance/result-0.50.tsv
65e37428323161b4ee5f8bc81c6bf1a5a31acb6b2c7cb26d50d6a117c0fed1ba  WORKDIR/runs/2026-10-18-1758/newent/smuggler-PRIMARY/val/0.50/luangthongkumkaren/result-0.50.tsv
5518532b30710c1367f877273d1d7ce1fada0a27462a1c057ff4051111ce764e  WORKDIR/runs/2026-10-18-1758/newent/smuggler-PRIMARY/val/0.50/wangbai/result-0.50.tsv
60c423bb6506c8377c0161dd606cf94724e6844d6ac0a9e68a97e79ae90838ce  WORKDIR/runs/2026-10-18-1758/newent/smuggler-PRIMARY/test/0.40/bantubvd/result-0.40.tsv
048daabbc1dfc9fb883a2a5f81d2839852920e73756ff8c8356751ec6fc0b750  WORKDIR/runs/2026-10-18-1758/newent/smuggler-PRIMARY/test/0.40/beidazihui/result-0.40.tsv
f61497a48e1a2e851704ce2ce31bbc876a8548f1c74829f891eccd0153786b69  WORKDIR/runs/2026-10-18-1758/newent/smuggler-PRIMARY/test/0.40/birchallchapacuran/result-0.40.tsv
7a6c34f749896328975ff1f330403b851ad6a582fd6b55967634966cad60fdd4  WORKDIR/runs/2026-10-18-1758/newent/smuggler-PRIMARY/test/0.40/bodtkhobwa/result-0.40.tsv
3249848ae4fc9e057d0e63d59609773bfbfd61c9d131770001f726aa54ff542a  WORKDIR/runs/2026-10-18-1758/newent/smuggler-PRIMARY/test/0.40/bremerberta/result-0.40.tsv
8b06a8dda5a13c733a00ce4fb333f357cbc11c889c5c05dfacd8cc83bd73e604  WORKDIR/runs/2026-10-18-1758/newent/smuggler-PRIMARY/test/0.40/deepadungpalaung/result-0.40.tsv
da3f26a0a3ba568dffd1f2ad229e937301f675fffc2f7776ed7c0244c4ab09c2  WORKDIR/runs/2026-10-18-1758/newent/smuggler-PRIMARY/test/0.40/hillburmish/result-0.40.tsv
7f48784405565d4160fc506947284e5de15512924665d2be82af41e25cc26469  WORKDIR/runs/2026-10-18-1758/newent/smuggler-PRIMARY/test/0.40/kesslersignificance/result-0.40.tsv
cbb2e5268b05a3d7aa519a3abd61ce2081e28fc488376c97c069575a181d39c6  WORKDIR/runs/2026-10-18-1758/newent/smuggler-PRIMARY/test/0.40/luangthongkumkaren/result-0.40.tsv
3efb030e3ef55ce7133ac2bf1c07a5fbb459093d1a90a86708614e6e4ab7113a  WORKDIR/runs/2026-10-18-1758/newent/smuggler-PRIMARY/test/0.40/wangbai/result-0.40.tsv
88caef598d87927ef751bf9bf8e07c8db84c6fd572b7d8783a139f96e9882451  WORKDIR/runs/2026-10-18-1758/carry/r0202-transducer-SECONDARY/val/0.50/bantubvd/result-0.50.tsv
aa88c651d8ca4efa9c765b3a4223d1d0dd33651bc5726fe2a46984568e9ef90d  WORKDIR/runs/2026-10-18-1758/carry/r0202-transducer-SECONDARY/val/0.50/beidazihui/result-0.50.tsv
23322061ed704696daa953bcdab2e95f02aeaafc8e9902e445e7ff0d15478e9c  WORKDIR/runs/2026-10-18-1758/carry/r0202-transducer-SECONDARY/val/0.50/birchallchapacuran/result-0.50.tsv
3f74775009570dc5b56f1433074ad3d25964daebc7023ec08d4b6a1690215798  WORKDIR/runs/2026-10-18-1758/carry/r0202-transducer-SECONDARY/val/0.50/bodtkhobwa/result-0.50.tsv
18aca7cf590913609f0b764d54708dee8ad6f35c039f647c8ca06296505f63d0  WORKDIR/runs/2026-10-18-1758/carry/r0202-transducer-SECONDARY/val/0.50/bremerberta/result-0.50.tsv
5e6723e1e7d485799542320b23697a82d05a60894f77b147bc340935a4447425  WORKDIR/runs/2026-10-18-1758/carry/r0202-transducer-SECONDARY/val/0.50/deepadungpalaung/result-0.50.tsv
b92ea2cb1cda22dabd3ba392bb41301c0b0d1f1e3cf9b315c1194608407f1ed6  WORKDIR/runs/2026-10-18-1758/carry/r0202-transducer-SECONDARY/val/0.50/hillburmish/result-0.50.tsv
eed30bdccdf73fd40d6ecd614e7e066662d7838f0f16b39a4d926d1b97aa784e  WORKDIR/runs/2026-10-18-1758/carry/r0202-transducer-SECONDARY/val/0.50/kesslersignificance/result-0.50.tsv
f415ee13a4c84f5813f9b1d57302b024fa739816b1ea6c87a51eae359b8b2c71  WORKDIR/runs/2026-10-18-1758/carry/r0202-transducer-SECONDARY/val/0.50/luangthongkumkaren/result-0.50.tsv
d7d62027b85ace2843d727e9ecd7d8cb54d164a32fec3bc3e478a6d1a2ed00e6  WORKDIR/runs/2026-10-18-1758/carry/r0202-transducer-SECONDARY/val/0.50/wangbai/result-0.50.tsv
35bb3da7fed2db62694ed983291ac927a27c3566db40530bfbfc5e0d8b494b01  WORKDIR/runs/2026-10-18-1758/carry/r0202-transducer-SECONDARY/test/0.40/bantubvd/result-0.40.tsv
23b1020142b9468c3cb639c374b66dc85406c6fbcdcfde29702831ce1875243c  WORKDIR/runs/2026-10-18-1758/carry/r0202-transducer-SECONDARY/test/0.40/beidazihui/result-0.40.tsv
8d8471d617b009072acbecc24d4e053c07c3e5f8ca253c1e6b64a07817460522  WORKDIR/runs/2026-10-18-1758/carry/r0202-transducer-SECONDARY/test/0.40/birchallchapacuran/result-0.40.tsv
8337405e80b2fe3991e97f705d66bae53f0a2480d890a86c8778f32c966672aa  WORKDIR/runs/2026-10-18-1758/carry/r0202-transducer-SECONDARY/test/0.40/bodtkhobwa/result-0.40.tsv
6d19b657a6aeefa0de84a37c3b261c25513d71c0d0c6582af5bf9e5e0f769f2a  WORKDIR/runs/2026-10-18-1758/carry/r0202-transducer-SECONDARY/test/0.40/bremerberta/result-0.40.tsv
0f2e607300e5ae4779585d0fbd5660cfdff242e6184f472450411b70a7baca61  WORKDIR/runs/2026-10-18-1758/carry/r0202-transducer-SECONDARY/test/0.40/deepadungpalaung/result-0.40.tsv
7083bf60e90d9e99f164bc7943ee0f7b11a47d9d720fbde4f6df7dd7035d9c13  WORKDIR/runs/2026-10-18-1758/carry/r0202-transducer-SECONDARY/test/0.40/hillburmish/result-0.40.tsv
6fc78053f928fc50190dc970ebd235926fe3930c82ec4c2522cf7f763e0d7dde  WORKDIR/runs/2026-10-18-1758/carry/r0202-transducer-SECONDARY/test/0.40/kesslersignificance/result-0.40.tsv
9adcd6f32601e01e2093c4f453c1bcd9d7b4700d0bccd7d8106905b15d32d1f9  WORKDIR/runs/2026-10-18-1758/carry/r0202-transducer-SECONDARY/test/0.40/luangthongkumkaren/result-0.40.tsv
c5cb7ecebc923d1761d0a472af658a4904e626b51debf790ebb4a5ff0c361f88  WORKDIR/runs/2026-10-18-1758/carry/r0202-transducer-SECONDARY/test/0.40/wangbai/result-0.40.tsv
88caef598d87927ef751bf9bf8e07c8db84c6fd572b7d8783a139f96e9882451  WORKDIR/runs/2026-10-18-1758/carry/r0202-transducer-PRIMARY/val/0.50/bantubvd/result-0.50.tsv
b0ab7f6cc4f2f468c19ee5b2743f74a3e853fd2d3c198c8bfefb3bd5fe07c5ea  WORKDIR/runs/2026-10-18-1758/carry/r0202-transducer-PRIMARY/val/0.50/beidazihui/result-0.50.tsv
1b7685b0d03458e31a8b0d02056f3e5d8341bf550da5055a81bc54ea2b160b6b  WORKDIR/runs/2026-10-18-1758/carry/r0202-transducer-PRIMARY/val/0.50/birchallchapacuran/result-0.50.tsv
da7b9def6cba14e095f6dfb6dfbb32a00c7aa088d9837e7b947685d1d18068f8  WORKDIR/runs/2026-10-18-1758/carry/r0202-transducer-PRIMARY/val/0.50/bodtkhobwa/result-0.50.tsv
d321ebb9cc3f7ce66fab39ee3dc781392e12dab43edcfcf24c43064c7864d2c3  WORKDIR/runs/2026-10-18-1758/carry/r0202-transducer-PRIMARY/val/0.50/bremerberta/result-0.50.tsv
e333c85d96b57d3e4ffc6a27ecf0d8c44dfbbbbac47821694f832430a64e9701  WORKDIR/runs/2026-10-18-1758/carry/r0202-transducer-PRIMARY/val/0.50/deepadungpalaung/result-0.50.tsv
c92d783842dcd3d143d62f0f2d45cece2bb3a69208458172e79b005748ae88d7  WORKDIR/runs/2026-10-18-1758/carry/r0202-transducer-PRIMARY/val/0.50/hillburmish/result-0.50.tsv
eed30bdccdf73fd40d6ecd614e7e066662d7838f0f16b39a4d926d1b97aa784e  WORKDIR/runs/2026-10-18-1758/carry/r0202-transducer-PRIMARY/val/0.50/kesslersignificance/result-0.50.tsv
f5c63c95fb2cb57f803653d20c349a1fd0792bd3f24cc8fbbb202b6c8f76657d  WORKDIR/runs/2026-10-18-1758/carry/r0202-transducer-PRIMARY/val/0.50/luangthongkumkaren/result-0.50.tsv
c829f070b2a1334224f2b4bc80f59e45ef5fa8d075081c4d43b800679180f80e  WORKDIR/runs/2026-10-18-1758/carry/r0202-transducer-PRIMARY/val/0.50/wangbai/result-0.50.tsv
f9f3779078f5c0f620a69adfb3355116a22168e0bef0fb3937ff33ab725d2097  WORKDIR/runs/2026-10-18-1758/carry/r0202-transducer-PRIMARY/test/0.40/bantubvd/result-0.40.tsv
92fe594a5110ebace1d4aaa6702357903c2ccfeadb85662ae7c01039ad23e62a  WORKDIR/runs/2026-10-18-1758/carry/r0202-transducer-PRIMARY/test/0.40/beidazihui/result-0.40.tsv
11baf6edaf2c7c7f7f93b24ab8808bee46b72dbb4e9f85960a606dc1eea12003  WORKDIR/runs/2026-10-18-1758/carry/r0202-transducer-PRIMARY/test/0.40/birchallchapacuran/result-0.40.tsv
dbea727c040bf22827ce2690eaf675f962663d442de961521cc98ec0eca3dabd  WORKDIR/runs/2026-10-18-1758/carry/r0202-transducer-PRIMARY/test/0.40/bodtkhobwa/result-0.40.tsv
38ec23fe39685f7998b378f3b29e89e42a1f6e53d2d614f442011d45e4176c32  WORKDIR/runs/2026-10-18-1758/carry/r0202-transducer-PRIMARY/test/0.40/bremerberta/result-0.40.tsv
fd37ecbdf535a53e6094147df09abdb248bcc2416631f2627e9084f2d7b9165a  WORKDIR/runs/2026-10-18-1758/carry/r0202-transducer-PRIMARY/test/0.40/deepadungpalaung/result-0.40.tsv
32bb3c4a06993337021cea384ea24f53ca347a5c03599ced779ac49e715f20f6  WORKDIR/runs/2026-10-18-1758/carry/r0202-transducer-PRIMARY/test/0.40/hillburmish/result-0.40.tsv
6fc78053f928fc50190dc970ebd235926fe3930c82ec4c2522cf7f763e0d7dde  WORKDIR/runs/2026-10-18-1758/carry/r0202-transducer-PRIMARY/test/0.40/kesslersignificance/result-0.40.tsv
acfb740bc935c3a006ef13a9822c879cd1214cb9d09b4576203cd56d8be25bdf  WORKDIR/runs/2026-10-18-1758/carry/r0202-transducer-PRIMARY/test/0.40/luangthongkumkaren/result-0.40.tsv
f193bd13a605460ed15375fab0e2ba8fa29debefb2074735f3de22ef831eb6a9  WORKDIR/runs/2026-10-18-1758/carry/r0202-transducer-PRIMARY/test/0.40/wangbai/result-0.40.tsv
2fb3789f644e3a20abf905db49a792eda5f23cd9cc061f6915bf1cab04ba7a43  WORKDIR/runs/2026-10-18-1758/out/comb6/val/0.50/bantubvd/result-0.50.tsv
b1cfdf6a3c6bcefd3def27d791bb16c14201cc3e2d27b833f0f19a4c53d90efa  WORKDIR/runs/2026-10-18-1758/out/comb6/val/0.50/beidazihui/result-0.50.tsv
7978b0bbaa3610d22a7e3afcb51f4ab9b828c7f1b31d829ae4082a995a71054c  WORKDIR/runs/2026-10-18-1758/out/comb6/val/0.50/birchallchapacuran/result-0.50.tsv
48e302ff6295d0af505573415e8165444c7ce8fa87be81a4ff5b12425b44dc7a  WORKDIR/runs/2026-10-18-1758/out/comb6/val/0.50/bodtkhobwa/result-0.50.tsv
c33f9bad02bed22584a157a23bdf0a3dfe969b14b86f38f0617345bd71e6a020  WORKDIR/runs/2026-10-18-1758/out/comb6/val/0.50/bremerberta/result-0.50.tsv
3b5126cbe0498d2c32c31ad20ab4e7ad9c66a23c67e13cb4771bd8b4f6ae8e75  WORKDIR/runs/2026-10-18-1758/out/comb6/val/0.50/deepadungpalaung/result-0.50.tsv
cae79a45ccb5187684b5ab3f93cacbd0450eb0af88a924722d7096a5e269e28d  WORKDIR/runs/2026-10-18-1758/out/comb6/val/0.50/hillburmish/result-0.50.tsv
737611e1e23d721610a605e41650daa96588f2aefd7338d3ece784ab932a071d  WORKDIR/runs/2026-10-18-1758/out/comb6/val/0.50/kesslersignificance/result-0.50.tsv
0129f663900cd117b4e0157278c81d027884f76fbc67042fb304fcfa774a544f  WORKDIR/runs/2026-10-18-1758/out/comb6/val/0.50/luangthongkumkaren/result-0.50.tsv
4123c0d88ef1055f6beb35a4ad9669812ede01076537a6d39880faf81559e922  WORKDIR/runs/2026-10-18-1758/out/comb6/val/0.50/wangbai/result-0.50.tsv
ea8b2dca8d882232a91a8bb0dbfa1dc450abd1bb643b2aac83e90bb5ed79ecfd  WORKDIR/runs/2026-10-18-1758/out/comb6/test/0.40/bantubvd/result-0.40.tsv
42a1230d3faedb62af6bf0c9bec38673137e09d52a3feae26f88853ed8316254  WORKDIR/runs/2026-10-18-1758/out/comb6/test/0.40/beidazihui/result-0.40.tsv
a02e456c8a3923405045aad3e9110023212f7a18998515fb565951ab86f75ea5  WORKDIR/runs/2026-10-18-1758/out/comb6/test/0.40/birchallchapacuran/result-0.40.tsv
599e9a1b6526cc9e2702880dd157924c51e01166f5c800fa3353f2aa5e918c8f  WORKDIR/runs/2026-10-18-1758/out/comb6/test/0.40/bodtkhobwa/result-0.40.tsv
b26cf04b941bde4c85fd4ebd30fa4fb8679990fcd0ae0eeee5372db0ea7e6557  WORKDIR/runs/2026-10-18-1758/out/comb6/test/0.40/bremerberta/result-0.40.tsv
6cfd5c584961c745f0e66ebe48957916266951ff4afebd252c7dd48b52315704  WORKDIR/runs/2026-10-18-1758/out/comb6/test/0.40/deepadungpalaung/result-0.40.tsv
d7093505f903a8ab9d55ef23fb68870e3cf87e8b8ce9f9e2e3d5fa622412d0a6  WORKDIR/runs/2026-10-18-1758/out/comb6/test/0.40/hillburmish/result-0.40.tsv
b9f52c37c663083b1257285209d521009132c2b9fb65818c278fb4c2edb088ac  WORKDIR/runs/2026-10-18-1758/out/comb6/test/0.40/kesslersignificance/result-0.40.tsv
a552fce3de1f3c429fe7216624aa5d6e7a997b657f0ee4f24b6adedd7469b03c  WORKDIR/runs/2026-10-18-1758/out/comb6/test/0.40/luangthongkumkaren/result-0.40.tsv
629b658748bc760e225a7bf9afd928d8bcdde92c14d4db444096a5bdb1491d66  WORKDIR/runs/2026-10-18-1758/out/comb6/test/0.40/wangbai/result-0.40.tsv
a260dbfccdcd2a16e75bc74d81aae0437234fe509308c0ec24345d9e5bb6cf12  WORKDIR/runs/2026-10-18-1758/out/comb8/val/0.50/bantubvd/result-0.50.tsv
630eea3709d4c513e46d2e715a30abc5a870164c497f98140aec44f87b364be2  WORKDIR/runs/2026-10-18-1758/out/comb8/val/0.50/beidazihui/result-0.50.tsv
ed1c7b0dd16e8a2ef331b777bfcc4258c187b547f76b95dbe9467c89e8743191  WORKDIR/runs/2026-10-18-1758/out/comb8/val/0.50/birchallchapacuran/result-0.50.tsv
ac6977804210e4d55bfbed9c1f153562c48e2329a246255422b4c3ce5a2c686c  WORKDIR/runs/2026-10-18-1758/out/comb8/val/0.50/bodtkhobwa/result-0.50.tsv
019814a9efc25b951eaa77a3187f232548d8c02bdcb6f266a2c627b599484180  WORKDIR/runs/2026-10-18-1758/out/comb8/val/0.50/bremerberta/result-0.50.tsv
604d650f730f214e8493c437df452d5f8d920510ea0964dbc2678eb6445aa0ad  WORKDIR/runs/2026-10-18-1758/out/comb8/val/0.50/deepadungpalaung/result-0.50.tsv
9b1568e63f4114499f4af8356159106d5817f84d6aeaad85c42f65bb4237bda3  WORKDIR/runs/2026-10-18-1758/out/comb8/val/0.50/hillburmish/result-0.50.tsv
737611e1e23d721610a605e41650daa96588f2aefd7338d3ece784ab932a071d  WORKDIR/runs/2026-10-18-1758/out/comb8/val/0.50/kesslersignificance/result-0.50.tsv
5797662e6a9433aa4d06f99646f21738fe4adc8427a5af4a07986e6e7cb69c79  WORKDIR/runs/2026-10-18-1758/out/comb8/val/0.50/luangthongkumkaren/result-0.50.tsv
1096d027707e123eec4074c98780395f6d9a1fc159a1667c6704d8c43aa5f10d  WORKDIR/runs/2026-10-18-1758/out/comb8/val/0.50/wangbai/result-0.50.tsv
5219048ae09e87dea431f9f6b1da359f2b76a8082ccf5886a94e77f303001481  WORKDIR/runs/2026-10-18-1758/out/comb8/test/0.40/bantubvd/result-0.40.tsv
3bb53e5951eeb23db96afb8e6a164f791c27277f28b0939478a78e018c7261c8  WORKDIR/runs/2026-10-18-1758/out/comb8/test/0.40/beidazihui/result-0.40.tsv
4c48c10797b7f2bc061e3ebc58376c59086465f5111437cee6821636c45252ed  WORKDIR/runs/2026-10-18-1758/out/comb8/test/0.40/birchallchapacuran/result-0.40.tsv
d360180bcc01993145ecefccddb28dbe73ba90b0a87e913cb9f8bbaff97150e0  WORKDIR/runs/2026-10-18-1758/out/comb8/test/0.40/bodtkhobwa/result-0.40.tsv
6ac201cb5dfc6fe75bc88f35f3eb04d31250a52bf300774cef7b895190e363df  WORKDIR/runs/2026-10-18-1758/out/comb8/test/0.40/bremerberta/result-0.40.tsv
121e2bc1ffac03f43c0f446bc2123a21a20106399929b36a130c72df75637072  WORKDIR/runs/2026-10-18-1758/out/comb8/test/0.40/deepadungpalaung/result-0.40.tsv
1dbf9a21b8c7b56c42ad23572fcb1653d8133dbacf1a49a1fceac9ec0559a875  WORKDIR/runs/2026-10-18-1758/out/comb8/test/0.40/hillburmish/result-0.40.tsv
b79bae2d054bbb530b707ec0bb14424c2046c610e1d99f817aae9408bf87d656  WORKDIR/runs/2026-10-18-1758/out/comb8/test/0.40/kesslersignificance/result-0.40.tsv
caa8908b7e180355ebde5cb2deead4275508ef8bd264f4a15692e73178f42be6  WORKDIR/runs/2026-10-18-1758/out/comb8/test/0.40/luangthongkumkaren/result-0.40.tsv
ec63c10229b9d3370d3ca367e9012131ace88d4a8b2fb2d4c8db82ebee384c53  WORKDIR/runs/2026-10-18-1758/out/comb8/test/0.40/wangbai/result-0.40.tsv
a260dbfccdcd2a16e75bc74d81aae0437234fe509308c0ec24345d9e5bb6cf12  WORKDIR/runs/2026-10-18-1758/out/comb10/val/0.50/bantubvd/result-0.50.tsv
630eea3709d4c513e46d2e715a30abc5a870164c497f98140aec44f87b364be2  WORKDIR/runs/2026-10-18-1758/out/comb10/val/0.50/beidazihui/result-0.50.tsv
041d0971080463b0c25bec23f58f71b0495578bf3d7e92ae30501cb29746b139  WORKDIR/runs/2026-10-18-1758/out/comb10/val/0.50/birchallchapacuran/result-0.50.tsv
ac6977804210e4d55bfbed9c1f153562c48e2329a246255422b4c3ce5a2c686c  WORKDIR/runs/2026-10-18-1758/out/comb10/val/0.50/bodtkhobwa/result-0.50.tsv
019814a9efc25b951eaa77a3187f232548d8c02bdcb6f266a2c627b599484180  WORKDIR/runs/2026-10-18-1758/out/comb10/val/0.50/bremerberta/result-0.50.tsv
604d650f730f214e8493c437df452d5f8d920510ea0964dbc2678eb6445aa0ad  WORKDIR/runs/2026-10-18-1758/out/comb10/val/0.50/deepadungpalaung/result-0.50.tsv
9b1568e63f4114499f4af8356159106d5817f84d6aeaad85c42f65bb4237bda3  WORKDIR/runs/2026-10-18-1758/out/comb10/val/0.50/hillburmish/result-0.50.tsv
fc58f477cd0d8f5c9a12e4809262b9c1483b0cfa7d3ac79b72061adcfbf7c36b  WORKDIR/runs/2026-10-18-1758/out/comb10/val/0.50/kesslersignificance/result-0.50.tsv
5797662e6a9433aa4d06f99646f21738fe4adc8427a5af4a07986e6e7cb69c79  WORKDIR/runs/2026-10-18-1758/out/comb10/val/0.50/luangthongkumkaren/result-0.50.tsv
1096d027707e123eec4074c98780395f6d9a1fc159a1667c6704d8c43aa5f10d  WORKDIR/runs/2026-10-18-1758/out/comb10/val/0.50/wangbai/result-0.50.tsv
5219048ae09e87dea431f9f6b1da359f2b76a8082ccf5886a94e77f303001481  WORKDIR/runs/2026-10-18-1758/out/comb10/test/0.40/bantubvd/result-0.40.tsv
3bb53e5951eeb23db96afb8e6a164f791c27277f28b0939478a78e018c7261c8  WORKDIR/runs/2026-10-18-1758/out/comb10/test/0.40/beidazihui/result-0.40.tsv
a671ed01e964fa7d17bab67d12e60d00295e5fb24bbc7732064876b1a2a1fa1d  WORKDIR/runs/2026-10-18-1758/out/comb10/test/0.40/birchallchapacuran/result-0.40.tsv
94b3de709f60f1533389b2af024dee4597b7c047812d80ec6bbeac2970064505  WORKDIR/runs/2026-10-18-1758/out/comb10/test/0.40/bodtkhobwa/result-0.40.tsv
6ac201cb5dfc6fe75bc88f35f3eb04d31250a52bf300774cef7b895190e363df  WORKDIR/runs/2026-10-18-1758/out/comb10/test/0.40/bremerberta/result-0.40.tsv
121e2bc1ffac03f43c0f446bc2123a21a20106399929b36a130c72df75637072  WORKDIR/runs/2026-10-18-1758/out/comb10/test/0.40/deepadungpalaung/result-0.40.tsv
a08fcebc8e18fa31384ecad8ed5e65f15287f0eea692df620eb0d73767c0d2fa  WORKDIR/runs/2026-10-18-1758/out/comb10/test/0.40/hillburmish/result-0.40.tsv
b79bae2d054bbb530b707ec0bb14424c2046c610e1d99f817aae9408bf87d656  WORKDIR/runs/2026-10-18-1758/out/comb10/test/0.40/kesslersignificance/result-0.40.tsv
caa8908b7e180355ebde5cb2deead4275508ef8bd264f4a15692e73178f42be6  WORKDIR/runs/2026-10-18-1758/out/comb10/test/0.40/luangthongkumkaren/result-0.40.tsv
ec63c10229b9d3370d3ca367e9012131ace88d4a8b2fb2d4c8db82ebee384c53  WORKDIR/runs/2026-10-18-1758/out/comb10/test/0.40/wangbai/result-0.40.tsv
```


Other inputs:
63ec589f0e088218ce1b9f6257cb336e32562ead324ee3aafb431f33a64c9a10  out/frozen_entries.json
fe6567746b72f307feda666ef834d3cfd676c12f8a895ec47eab2957be2abcef  carry/carry_entries.json
58234964fb82efe0cea6b0a6e0d30c19e18511c6b57c2bf47cb7e67cbf12c620  newent/new_entries.json
72640abb6676b462ad4b4e444fd175190dd66fa2a05787bee33946ae94a8daac  out/comb6_entries.json
6879878dcdd219cbe432a7ff03d83e037e4c16cbaf4be5e8d3a32925e048d4e8  out/comb8_entries.json
d0ae8926306459581893f916766ad908234fe365e7ce7b0a02c2810b26add7d9  out/comb10_entries.json
bae2513548ba6607116f99662a12fda7292a19e880bac5e0c6873b323723e5e1  out/comb6/combiner_fit.json
6f9d48f827d8f86ca5671a0e19728de127d125f5186332d5276f7315c39bc1dd  out/comb8/combiner_fit.json
be9159a020bf7c0aa691a12c0592bdcc66e098445c6e880e30a2086e912836e4  out/comb10/combiner_fit.json
254f8e51a592ea6cf2e59215d7219b1ab47df443308a7bc172f7a1173db2761b  PREREG.md
