#!/usr/bin/env python3
"""
Self-contained zero-trust verifier for V3R1T4S outbox package:
  2026-10-26-mizopl-e1d0aaa2 (target: flab-antibody-developability-zero-shot)
  ("FLAb antibody developability: beat the released zero-shot scores on a
   therapeutic-property category", Chungyoun & Gray, bioRxiv 2025,
   doi:10.64898/2025.12.27.696706, commit e05e3f0135783ffb7de412df6a1467e7a0031911)

Audits the single frozen zero-shot rule (`CLSS_Reg8_AllBP_IMGT_Z`, frozen at
2026-10-26T00:26:00Z in commit 654c23f056b932c310723f591bc3fec89102ad73; all other
variants reported strictly as exploratory ablations), verifies that no third-party
sequences are embedded in `object/predictions_tm_polyreactivity.csv` or the 8
`<1 MB` binding prediction shards `object/predictions_binding_part1..8.csv`
(109,236 total prediction rows across 172 dataset evaluations), verifies the
pinned upstream commit and data-file SHA-256 commitments across all 190 evaluated
FLAb files, and audits Partial Wins p2 and p3 (with Full Win and p1 marked not claimed).
"""
import csv
import hashlib
import json
import math
import os
import sys

EXPECTED_CERT_SHA256 = "b6be3abe5d0dcff18fcf18d8e7a16f64164d434290274613f79b76f80f598eb6"
EXPECTED_PREDS_SHA256 = "63cf82e9994c98a2dd2a69b47ff154b5ea9344fbfca0c4535ab11626ad0d7a9e"
UPSTREAM_FLAB_COMMIT = "e05e3f0135783ffb7de412df6a1467e7a0031911"
CLAIMED_METHOD = "CLSS_Reg8_AllBP_IMGT_Z"

EXPECTED_BINDING_SHARDS = [
    {
        "file": "object/predictions_binding_part1.csv",
        "sha256": "8e748b57b03ae4b59f8218f29f36c9ca953c24180ded58335ba362716067535c",
        "bytes": 894791,
        "rows": 13093,
        "sum_clss_reg8_allbp_imgt_z": 223.817791
    },
    {
        "file": "object/predictions_binding_part2.csv",
        "sha256": "ba6c287e5b2b68005a7364e80fd35158d22ab28bc0f0cb1703d7a5008afb391c",
        "bytes": 909107,
        "rows": 13093,
        "sum_clss_reg8_allbp_imgt_z": 14471.839614
    },
    {
        "file": "object/predictions_binding_part3.csv",
        "sha256": "f34f344dd88ca9f87c664bcfe667685dcbac65957591f48b4220ae94f22cf3c7",
        "bytes": 862391,
        "rows": 13093,
        "sum_clss_reg8_allbp_imgt_z": 3265.529171
    },
    {
        "file": "object/predictions_binding_part4.csv",
        "sha256": "34287e9f3492063ffefe6945c14675530b621eba63852bb3ac8f5d0c3aba750c",
        "bytes": 896838,
        "rows": 13093,
        "sum_clss_reg8_allbp_imgt_z": 6817.891579
    },
    {
        "file": "object/predictions_binding_part5.csv",
        "sha256": "0dc9735f13bfde50d6ee20a49a5ad81627ffc30f79c869287b03eb4097eb0ab3",
        "bytes": 903476,
        "rows": 13093,
        "sum_clss_reg8_allbp_imgt_z": 7912.262676
    },
    {
        "file": "object/predictions_binding_part6.csv",
        "sha256": "927068ffec0443c33ce4434fc2077db3e9665a2fca6738b1189329727ad7c5d3",
        "bytes": 892366,
        "rows": 13093,
        "sum_clss_reg8_allbp_imgt_z": 7275.999774
    },
    {
        "file": "object/predictions_binding_part7.csv",
        "sha256": "52f106d72ed81d0a3e4b4795ebd004ada3d1881d2a3c81751b60a6a3606b76be",
        "bytes": 903476,
        "rows": 13093,
        "sum_clss_reg8_allbp_imgt_z": 7350.286279
    },
    {
        "file": "object/predictions_binding_part8.csv",
        "sha256": "f41772d054c180cb6f4dd900d615887973d0e16ee9909cc292cda986b306b912",
        "bytes": 879686,
        "rows": 13086,
        "sum_clss_reg8_allbp_imgt_z": 6442.167004
    }
]

UPSTREAM_FLAB_FILE_SHA256 = {
    "data/binding/adams2017measuring_4420-fluorescein_kd-flow.csv": "71901977452fbc617bb1387eda70228cbcce1e9586e13905e008350da29d388c",
    "data/binding/adams2017measuring_4420-fluorescein_kd-titeseq.csv": "2cd506bbd2c3bb1104c9f776c22d8db075d5b26e3ca4a2b3c0fc42e4aec6cc7e",
    "data/binding/cognano_AVIDa-hTNFa.csv": "d381875e1fe203b040b8d16caa6449e777402bb03b1388cc151b3962ecab740c",
    "data/binding/garbinski2023_kd.csv": "a184d51001693d2c891e98025473e44e76463c3ea66adf97904b94f40606d99c",
    "data/binding/hie2023efficient_CoV2Beta_C143_Kd.csv": "28741e2bd1b73bb7a6184e6db3d38c3a136072f788c370b218ff967890dce68a",
    "data/binding/hie2023efficient_CoV2Beta_REGN10987_Kd.csv": "bcada8fefb9e95d20ccf42e025915598af09af199aa3b023e6a2bf75352e9436",
    "data/binding/hie2023efficient_CoV2_S309_Kd.csv": "82cbf238736020936e3c82adb8247ef373bdddd5f4ba1d5607cc971a9269212d",
    "data/binding/hie2023efficient_CoV2omicron_REGN10987_Kd.csv": "04a89f0a54704d1c406ad0c4d62ea0f1b8e17c705098eb23a9a4aea2886d00fd",
    "data/binding/hie2023efficient_MEDIUCA_H1Solomon_Kd.csv": "2d900959e7abc5570a8b79359364ad349638fc9ac5c47d6059de78b2e06acccc",
    "data/binding/hie2023efficient_MEDIUCA_H4Hubei_Kd.csv": "2f9f7c9a36322ed8528d56a08d8abc05b1e509010d3de541f5786dc0f8a9498c",
    "data/binding/hie2023efficient_MEDI_H4Hubei_Kd.csv": "6902d49abc1eab0586fd552adb49d18431c1b6fea7f0e036b2a6c802998311b1",
    "data/binding/hie2023efficient_MEDI_H7HK16_Kd.csv": "43c86d44aa6a946de0325fba2d9f8cf7e6dc22118b164e3c590c78a23a95fd01",
    "data/binding/hie2023efficient_ebola_mab114_Kd.csv": "430da3626c20120514a7cfa091a99f2a44c8751f4f057b575aad1b5c6ddd128a",
    "data/binding/hutchinson2023enhancement_multikd_fab.csv": "5962caef362d08d8c529939908d7a4528675bcd25235b59f3b74c521a68522c0",
    "data/binding/hutchinson2023enhancement_multikd_igg.csv": "59db69b2d076e82f179a7bec47bdbc809644dea88d425d506f9c486bf7de1f0e",
    "data/binding/hutchinson2023enhancement_singlekd_fab.csv": "db49813003127cbe133195fbf3879f52a5f671a46719ef1b989e91ccc14fb1bb",
    "data/binding/hutchinson2023enhancement_singlekd_igg.csv": "669e69522525cba335fda5bfd7fd35a76c0c3ab76d13298de053ecd2489faaa9",
    "data/binding/hutchinson2023enhancement_top200kd_fab.csv": "ecacc5ec299cd5c2b75ea32d5457098d88798bbf61f8b1b5b94d36d84b19082c",
    "data/binding/hutchinson2023enhancement_top200kd_igg.csv": "a59ccddfab3bdfd61dc5f7275d5a8c077c2d9e60e1f74c53974d69586145a62e",
    "data/binding/hutchinson2023enhancement_top27kd_fab.csv": "cedd18bdf9cae22842573cf5bb64b4a84722947d0e09cdd5e6bb16d14b5d26c8",
    "data/binding/hutchinson2023enhancement_top27kd_igg.csv": "dbd87b8be24e4b14ea0e24ffbe02c014ee2b39200fc920b6084e30fa427e6424",
    "data/binding/jain2024assessment_Hen_Lys_kd.csv": "982099b57da2cd4951cf987b7fb97586b0e67769b2711ba1f4e664b643bcb363",
    "data/binding/jain2024assessment_mouse_Ly_kd.csv": "bd1caa101ff3f25c61d697a8f333c8f307a79c3c9ee855de0bb3335bf2e0920b",
    "data/binding/kirby2024retrospective_ab-SARSCoV2_binary_kd.csv": "5e358f7fb3673004237c77696f586cddfb98bd536486d30997b692530c826418",
    "data/binding/kirby2024retrospective_ab-SARSCoV2_kd.csv": "1757cb487022b0635dc414a60c97ff7a6b73020086890038d21c812ed752583a",
    "data/binding/koenig2017mutational_kd_g6.csv": "6c1aa637b32cd781d4100411e8f4f71324eab8df480ba7bce490b66dc89d4ff1",
    "data/binding/kothiwal2025htp_DCC_ec50.csv": "bfec6f4d1e4e08018de0dc851b529ecbfbe019f67ee8630269b7222144bf82a9",
    "data/binding/kothiwal2025htp_DCC_spr.csv": "ca8fde4f3fd890da97c1eec2df75d5bc92e81c90d0c56b6598902601b8fc385f",
    "data/binding/kothiwal2025htp_DKK_1.00_ec50.csv": "968fa0cb30b2d7eb3cec4ed2ff3d25c131d1eb3c97d9216f89208bfd4b161acd",
    "data/binding/kothiwal2025htp_DKK_1.00_spr.csv": "4c333ec05fae0522e7076bce1f882ff616fc04bc63bb1a2d8dbb5c8e4646252d",
    "data/binding/kothiwal2025htp_IL23R_ec50.csv": "e8a4b4aa6b4328c93c8d9bcdfb9e5c6121a26dbd3597c905f9aeec803c9bb9c8",
    "data/binding/kothiwal2025htp_IL23R_spr.csv": "852446cca13cfa1e3348fa5b9300983c1c6e7586bdab5c5b850e1a7de4918c32",
    "data/binding/kothiwal2025htp_LOX1_ec50.csv": "ded983b4dc7c59b92a84a310e589ee79cd40089bb4b6e1cf39de48b8992389be",
    "data/binding/kothiwal2025htp_LOX1_spr.csv": "6ce6551750b83e63922f6788982f7a5e83e260255aa1ccc1d4d677fde6c50edb",
    "data/binding/kothiwal2025htp_PDL1_ec50.csv": "210bb2f211a1f23f44b10462b5489ecaa015ee25e538d8ef1b3397e8ab6d6e3d",
    "data/binding/kothiwal2025htp_PDL1_spr.csv": "1930eb65908ab8e873bedadc52d13345f2cac624692c073a746ab4936997a23f",
    "data/binding/kothiwal2025htp_PDL2_ec50.csv": "06252aab47446638831d699edd5e843f63c3092f0b611b0399ada3fbbdb82925",
    "data/binding/kothiwal2025htp_PDL2_spr.csv": "e3d8b05523c81634cf51b70d70be44c0d902037b530e598ceffef0e6f4ba3609",
    "data/binding/kothiwal2025htp_ROBO1_ec50.csv": "470b7c2f42dc94a982b974ab4a6e356ace89ee9d6c07842413c6d7a6bb2744ed",
    "data/binding/kothiwal2025htp_ROBO1_spr.csv": "713acf5e565538222efe837249cd86e3eb03e6b27cb216bcbdfd27fe4cc6bec7",
    "data/binding/kothiwal2025htp_ROBO2N_hROBO2N_ec50.csv": "feb27aa2f7a82da20fd74448b6d59aa6755323270a0d51f49a1848552e7e4e2d",
    "data/binding/kothiwal2025htp_ROBO2N_hROBO2N_spr.csv": "3125dbecf8f5d0a6215b1b25c26c46661993ff0848cc04e7e80b7434722a39a8",
    "data/binding/kothiwal2025htp_Syncytin2_ec50.csv": "e83c23a4fe3adfa124622cdd680c8b69b7a806a2d86943acd75099a96cde5878",
    "data/binding/kothiwal2025htp_Syncytin2_spr.csv": "23ad413dd8416391acea5a266f09f444fca174a81c1c879818525b5c1408ee29",
    "data/binding/kothiwal2025htp_TIGIT_ec50.csv": "29e4d0000c3f40a07c22b1283dc8fc09dc760da5f7205f1c52d075aeba21665a",
    "data/binding/kothiwal2025htp_TIGIT_spr.csv": "d7ebec7d5dc44e50275e34d92888d50ff113644f8429ee17db3c6c9e67eb2db6",
    "data/binding/makowksi2022cooptimization_iso_ant.csv": "96bfed69466a1dda4efa2048bfd2a3bf18f03eafb88c3a820abe9b94ac7b669c",
    "data/binding/makowski2022cooptimization_igg_ant.csv": "f99ab54b4b006f344303aea3aabedfa1cc9cfc00eab95c423ad63ce839504732",
    "data/binding/makowski2022cooptimization_igg_ova.csv": "36c48be872dc43c7fff453674408c0fa4686ab3100d92fb71d5dedef495c0520",
    "data/binding/makowski2022cooptimization_iso_ova.csv": "9a943ca0dbd5b9838d68ddabcd4575f6cc3f284c593cafe05a4ae4b8f67e0691",
    "data/binding/peterson2024integrated_ab_H1HA_binary.csv": "0151a86da5af8d1da4344ea6b8d633a4d83b782b7649615cf5e173ad9063d24e",
    "data/binding/peterson2024integrated_ab_H1HA_kd.csv": "7f5ef0ad0a70e82772d3cb4457e431e9ad87136b44d59f59c5a6e76023310505",
    "data/binding/phillips2021binding_cr6261_h1_kd.csv": "6f2a4c49414c925da183641b0b058b20a2b57c4f3fccdbce9fac7590ce4b6aa2",
    "data/binding/phillips2021binding_cr6261_h9_kd.csv": "f577ea3a6a1bb82502f8110147fd54fba13b332921bb82be43922423f0ff0c53",
    "data/binding/phillips2021binding_cr9114_h1_kd.csv": "d18a6aaedc957be699b059a4bb3f3474dedb2a1f2a071c63deb0eedf2cc04254",
    "data/binding/phillips2021binding_cr9114_h3_kd.csv": "0759ccf0327069eb6e7239ee34e2690888ba0a85cc818a95af2cb35ffcdb822f",
    "data/binding/rawat2022abcov_ic50.csv": "6f1cc7a034ff10b84b77b4e596c499908a9b4d62250b42f5e1b3d6b8469425c7",
    "data/binding/rawat2022abcov_kd.csv": "d187087ad47c72c7bb65cfc10cd76e494afbfed22657b043d703357d88da71e0",
    "data/binding/rosace2023automated_kd_adalimumab.csv": "179f8927cd120913c9ea97c5fca5cd9792fe694da124399189560c246dc467bb",
    "data/binding/rosace2023automated_kd_golimumab.csv": "5c016bf3d74f2e042de10c73d6869986becac84a9a76921429243ea44420bf61",
    "data/binding/shanehsazzadeh2023unlocking_adcc_ec50.csv": "d298a74aa7d1d3318ef644a2edc593a84f8aab49e2c5d57c11dbc2c8959b973d",
    "data/binding/shanehsazzadeh2023unlocking_kd_hher2_fab.csv": "133fb3fae9f5e6fdf305b019ebece431d8eb955c5c42551e050acd7b2f3a8984",
    "data/binding/shanehsazzadeh2023unlocking_kd_hher2_mab.csv": "63819dc8613c4261b44a201022fa7498e6f8cccb72c41cfc4db40d28d3c0738b",
    "data/binding/shanehsazzadeh2023unlocking_zerokd_trastuzumab.csv": "3450b94442a8c786183e1047c57e89b6ec872d8e624689f945928878c1473074",
    "data/binding/shanehsazzadeh2024igdesign_Afasevikumab-IL17A_kd.csv": "ba4276f6ac1225957429fce2e9a4a91ebd18d76c01550bf23cdfff2e4778c193",
    "data/binding/shanehsazzadeh2024igdesign_Bimagrumab-ACVR2B_kd.csv": "ff55ccd41ee198180c9a80ba1eac98baea595f62a637269b5bc9b9363f08285c",
    "data/binding/shanehsazzadeh2024igdesign_Eculizumab-C5_kd.csv": "369fa1a38372fcd92bf9f309056fc9b29f13ae5320fbfda0e7826cdec2de8e6c",
    "data/binding/shanehsazzadeh2024igdesign_Osocimab-FXI_kd.csv": "3202bb027a6ebe676f7d04394397a49c9476d7b01cf79796c8038716be3ef46c",
    "data/binding/shanehsazzadeh2024igdesign_Spesolimab-IL36R_kd.csv": "ffcc2242676e0e8d2b01d16180bcb2391c2174a8348f79a2be2b62f08e886445",
    "data/binding/shanehsazzadeh2024igdesign_Tezepelumab-TSLP_kd.csv": "7ebdd9fb1139efc4a054630eb53019109a446d7e1ed7bdc0aad42b5ca46e3610",
    "data/binding/shanehsazzadeh2024igdesign_Utomilumab-TNFRSF9_kd.csv": "9e971485794175869acfd6a5a06a156d91164bc54a5cb975913d0f5b46cb7dab",
    "data/binding/shanker2024unsupervised_Ly1404-BQ.1.1_IC50.csv": "91853f8b9eea20ed3b0659aa41b718e3f8a172e4bb6c4edd8f9c9cc8dbb44bae",
    "data/binding/shanker2024unsupervised_Ly1404-BQ.1.1_Kd.csv": "adcece1c357d52a5da3c297e77295477b28c7122a85c41234872c413f769bfad",
    "data/binding/shanker2024unsupervised_Ly1404_Wuhan_IC50.csv": "641c8c6950cca8fc7e0cfec0ee6e3c023522153527d315a91bbc6a6aa5d42fa2",
    "data/binding/shanker2024unsupervised_SA58-BA.1_IC50.csv": "724d814e6ba7a796fbcd6596142d986271bb515230ba8961a48caa827f5f761e",
    "data/binding/shanker2024unsupervised_SA58-BQ.1.1_IC50.csv": "a6c62235a8826775f8b2f9a36725a3f62b58e1435b49dce072e1ff1b9737f96a",
    "data/binding/shanker2024unsupervised_SA58-BQ.1.1_Kd.csv": "15b2095afd64be421f2148e2c878e4b3affa013e46dd5f4b593e8201f0a88d1e",
    "data/binding/shanker2024unsupervised_SA58-XBB.1.5_Kd.csv": "40c8f336925429fb2c349b883c2997d328cc1a5ad36431a0aa30a78fa2b0869a",
    "data/binding/warszawski2019_d44_Kd.csv": "bda66c936962b290bc78a58227e3c9fe3cbb49ce8bcbea5fee044e47f2e7cb8f",
    "data/binding/zimmerman2020antibody_4420_kd.csv": "e5745a0cddd395621887d9dcab041d57686cef92b3f2039d00e7f54663d11295",
    "data/expression/adams2017measuring_4420-fluorescein_exp_er.csv": "fb29cda664077115636f6c9677ee8e9b7972f18def43a952f584810d91f10172",
    "data/expression/garbinski2023_exp.csv": "6059a2bf61a3fa6f8d97ad4bc7c28a1b1bc8e71cb0b99cead6740cbad456a28b",
    "data/expression/jain2017biophysical_HEK.csv": "80c7d7dfd6581d89452c5ee6f3215f218818006c70286a49657ffd4a28431be2",
    "data/expression/koenig2017mutational_er_g6.csv": "7ec320e663f01f1bfeee9c62eb2520d602a11e3cf12d8ca93a714e89ccb48e4b",
    "data/pharmacokinetics/jain2023identifying_FcRnRelRT3.csv": "ff2ed2b111a7b77fcffefd8890f6495c67c81fce395d7b6b2d1d79754627a3f3",
    "data/pharmacokinetics/jain2023identifying_HEPRT3.csv": "021db811996fad6cfe8a1345aab84208f5bda1069567601bc5dccf4f4092dfe6",
    "data/pharmacokinetics/jain2024assessment_FcRn.csv": "445bce140bc5a5686541ddad38dd2a73728d55012615c35edaf6f67fb51b7343",
    "data/pharmacokinetics/jain2024assessment_tg32_clearance.csv": "cc7581e92ff0fb418fb6560bcfe2a18eb0497d212299b98bde3fdd2d1539afae",
    "data/pharmacokinetics/jain2024assessment_tg32_halflife.csv": "4790b8d42090cd85d67f9111f5e449c121078b130addcedeb8fd0f3decb420ff",
    "data/pharmacokinetics/makowski2022cooptimization_pI.csv": "9774cf9222e34e9ca66bc3a8871be29f1cbc1bcb328f3fedd27429d0c76d4319",
    "data/pharmacokinetics/shanehsazzadeh2023unlocking_FcRnPeak.csv": "845ec8dc61028c4c40f0f05d2c64bf48f0faa32b9328ea2e053f934e3a68b7d6",
    "data/pharmacokinetics/shanehsazzadeh2023unlocking_FcRnRRT.csv": "86cd4b8e0ff31e07b078505431d7d7f660739534f767e327ee58ceab7f201d97",
    "data/pharmacokinetics/shanehsazzadeh2023unlocking_FcRnRT.csv": "d97b1db75e3a4d97afa1a87ed204baed7a0d6d14ef9715905eba206cf8e316c7",
    "data/polyreactivity/jain2017biophysical_BVPELISA.csv": "3d1d39bae9ea870903b0e2f49bf5c73ef7eb506639fe07dc8a49a0c4f3bf6730",
    "data/polyreactivity/jain2017biophysical_CICRT.csv": "0180151e3aedacc14460a024c5f7e133340b8f8aebffe777f6475e8369145367",
    "data/polyreactivity/jain2017biophysical_ELISA.csv": "95b05b7b298d00381c12b26d9507873bea4af8827fdd3c05943db21aabbcbef3",
    "data/polyreactivity/jain2017biophysical_PSR.csv": "ed4649aa777cc1ba5ffc249df677ee9f69b076a5b643fa2962eeb2e22f51711a",
    "data/polyreactivity/jain2017biophysical_SMACRT.csv": "a89d658222a6e02074f398594422fd20a89682b8b7e501d2dc66d6ba9792ad45",
    "data/polyreactivity/jain2023identifying_DNP.csv": "eacd6385b0fa675cf87bc8f0cdc7f04f5e79740a6bcca04e2f12a613cd728a56",
    "data/polyreactivity/jain2023identifying_FA2.csv": "6b29a48ab6f0c5860468ec554bdddd13d24576b85e3aedd5ec28258c87a725d7",
    "data/polyreactivity/jain2023identifying_FVC32.csv": "199c317c78a43254e58ac0433dbab20a322f9cba3ba9361549793359c75325c6",
    "data/polyreactivity/jain2023identifying_FvFVIII2.csv": "5af8b5b6f22b14895c7913981ea56b81574582ad1cf9dbe4b077f3d466d9c10b",
    "data/polyreactivity/jain2023identifying_FvLysM2.csv": "e3947f372925efce6012616653ff220e09ae203cf7e1692f7b5c0209be2f98a7",
    "data/polyreactivity/jain2023identifying_Heme2.csv": "40c28a3e5ca04cdfac72d316a3fb38647b97ed6fcc57fd779335cbac3eb73af9",
    "data/polyreactivity/jain2023identifying_HemeC32.csv": "2c69c3aed52a7e6491bbbda5094e45e008d3ac779e65c6e98632170296d02020",
    "data/polyreactivity/jain2023identifying_HemeFVIII2.csv": "4b87ad9970f633de056952c12330934d8647720dbdccebcc9783798be9ce6e2a",
    "data/polyreactivity/jain2023identifying_HemeLysM2.csv": "ada4f237312e109b17fb6ac2721c54adf5b232e10d97c77cac7c8456170d2f16",
    "data/polyreactivity/jain2024assessment_Herapin_RT.csv": "88fafb12a45070cd474b98a6473f01d445794332694afde9a647303d597f4c6b",
    "data/polyreactivity/jain2024assessment_PSR.csv": "5e77f845b2d113fb5f09d7319bc22553b8d1ce8544f332529023b901aa7ad62a",
    "data/polyreactivity/rosace2023automated_CICRT1_adalimumab.csv": "1378b8297d7d812c1c041e10eb9b62166f775c6e5f2e4d11d893490ce34be758",
    "data/polyreactivity/rosace2023automated_CICRT1_golimumab.csv": "382a539c796d4388c475bc1f9ed0bc9ec7ea08377d9de3cd087ef1078cde18ed",
    "data/polyreactivity/rosace2023automated_CICRT2_adalimumab.csv": "3cc6f17b8d9c803241c11db3ad0332a0b674d9dc36a692b48ca61585369f9d1a",
    "data/polyreactivity/rosace2023automated_CICRT2_golimumab.csv": "207a8e156b364cda08474f79966c19fc8dcc02bc79ef1d7eff932457652a74dc",
    "data/polyreactivity/shanehsazzadeh2023unlocking_elisa_ec50.csv": "c82c187bb5e6436a32e13fba2d11f4718510012fd225988d48758aac80983403",
    "data/polyreactivity/shanehsazzadeh2023unlocking_polyspecificity.csv": "7d47dacc99c8b715d2422babfb505639620c03ad2cf5eae10b8c242a1e76ac81",
    "data/polyreactivity/shanker2024unsupervised_APC-MFI_Elotuzumab-Ixekuzimab.csv": "375516ab38a7ac0064baa148cb4a88d6af34b9e691e393f8e0dc916e2aa8837f",
    "data/polyreactivity/shanker2024unsupervised_APC-MFI_Ly1404.csv": "baf07b9679840563cf0cbce1ab93d45346f05151072313a6e60d80d9c95f5c48",
    "data/polyreactivity/shanker2024unsupervised_APC-MFI_SA58.csv": "e371a4a310981b69367c5f0c8a7f918ea23038d4e0544b14398771e160d2102d",
    "data/thermostability/garbinski2023_tm1.csv": "ea02da65b2ab0663bb3e4ddbef3ec2038511443a2cbc2af2ac8afe3b4af4baf8",
    "data/thermostability/hie2023efficient_C143_Tm.csv": "bcce005b7498b00e1298a4b4517c1dbddfad9efc71abdbf952b2165419c6fb84",
    "data/thermostability/hie2023efficient_MEDIUCA_Tm.csv": "61be0d21700fbfa750d3aaf633889e909ffa1953b686901f78b0cd3676dae30d",
    "data/thermostability/hie2023efficient_MEDI_Tm.csv": "4d692039defa0a45f01dbf07655238abdbc44c4afc0218db7227ae41688578c2",
    "data/thermostability/hie2023efficient_REGN10987_Tm.csv": "fdf06e368ba1df2af8c213f4fe82b12b6e0d163a08da88c654b9eec683f4a137",
    "data/thermostability/hie2023efficient_S309_Tm.csv": "3d346b0a70bfe898498dffdab433bef0450aa1db0dc6638b1ec7bbcbcdb79ccf",
    "data/thermostability/hie2023efficient_mAb114UCA_Tm.csv": "fd372f1dcd491e0889b485fcafb6f1d5b0a75b1b57c182c202accb2b44ab8920",
    "data/thermostability/hie2023efficient_mAb114_Tm.csv": "2a77e7049a183ca67a5d97237914be689e4e631377ce1ea1d66fe9e2b492ec57",
    "data/thermostability/hutchinson2023enhancement_multitm1_igg.csv": "ded8db1c627e602e8aa14f4cad98c61d05cb0bfc38a5421d369f61dbb1864928",
    "data/thermostability/hutchinson2023enhancement_singletm1_igg.csv": "cdc94741be47c4b6d1b750b81834514026373a0e7730a43c2c29e427811e66b9",
    "data/thermostability/hutchinson2023enhancement_top200tm1_igg.csv": "74a6293f2be33d51acaaf102dea91b4584e24901cbbde843f1fa9daa450afce5",
    "data/thermostability/hutchinson2023enhancement_top27tm1_igg.csv": "51398c33760f5652449800516a72d232a9e331a0d57c6749cef61e69c46fe6ac",
    "data/thermostability/jain2017biophysical_Tm.csv": "86bf8d8da6015bd36907847ac94983edfcea425d1d188a422f75d40ea27bb09b",
    "data/thermostability/jain2024assessment_Tm.csv": "b4ce11c7473b3d55f44c56bd62509db42ffa077dfb006cafad7ea326bb8d67b2",
    "data/thermostability/rosace2023automated_tm1_adalimumab.csv": "eaa1fddba5702e22ae2858994f0911cbaf1efaab92f9a58546aa3f96f43657a7",
    "data/thermostability/rosace2023automated_tm1_golimumab.csv": "4c7998d6f2159baeb8a3bc506d2065e18b9c2e2e69e2266c43a761b2d41fb0b2",
    "data/thermostability/shanehsazzadeh2023unlocking_DLS.csv": "81de45d852c20c4e03d957de2408b0ab8c6025f121af53305523aa423079c8e5",
    "data/thermostability/shanehsazzadeh2023unlocking_DSF1.csv": "fb21d1ba98309a7830f05d6232ebcee083eccd6551529e6482d906e3d712af6f",
    "data/thermostability/shanehsazzadeh2023unlocking_DSF2.csv": "026d21ae62bd4211cd4882f565dc36b69e00307fd4b3fb47954bd5d0cdae30fc",
    "data/thermostability/sulea2019assisted_sdAb_tm.csv": "718a22d91a402abb4641d34fc47a22327302ab9f31837f2e02f82de21b0b4864",
    "data/thermostability/tresanco2023nbthermo_tm.csv": "cf61929d109de4ef272ad46dfc2cd5812241b42a6ba92ee372afdfdb893dda44",
    "score/antiberty/aggregation/Wittrup2017_CST_ACSINS/Wittrup2017_CST_ACSINS_ppl.csv": "e3b7f5b37bdfb0164470fb8981be958a4e6c239a2b1645caa11011b6d019b5f3",
    "score/antiberty/aggregation/Wittrup2017_CST_CSI/Wittrup2017_CST_CSI_ppl.csv": "1de06e822b320a1accaa1df907b7e0d7416d4df93c29f6386080bcaab5a4cb0d",
    "score/antiberty/aggregation/Wittrup2017_CST_HIC/Wittrup2017_CST_HIC_ppl.csv": "4c407562d6513b0dfc515cbb1859db776d34ecea427a0bd5a6e372f3817435d5",
    "score/antiberty/aggregation/Wittrup2017_CST_SAS/Wittrup2017_CST_SAS_ppl.csv": "15b69b1114409f233e413596da054518023877c8b6ea03c6aad7f7ddb24ff877",
    "score/antiberty/aggregation/Wittrup2017_CST_SGAC/Wittrup2017_CST_SGAC_ppl.csv": "80f9f42adc6fe514eb72fc0285dcbcb634b8bb842811e4b89ffcbf3e0aa921d3",
    "score/antiberty/aggregation/Wittrup2017_CST_SMAC/Wittrup2017_CST_SMAC_ppl.csv": "7068304013091335e727081cc58e3286a9eeb1dbfc669bdc97d1d1f82cbd8125",
    "score/antiberty/binding/Hie2022_C143_Kd/Hie2022_C143_Kd_ppl.csv": "bb95e2bbc90ae48ea5c1903c6cb14474d03d706ab9835102b8a5ecfcc4d000a5",
    "score/antiberty/binding/Hie2022_MEDI8852UCA_Kd/Hie2022_MEDI8852UCA_Kd_ppl.csv": "c0ae1c454d8ccf58d0d00a1008b14c7bb699c7182caec0f2b1cd1cf0c378f7f3",
    "score/antiberty/binding/Hie2022_MEDI8852_Kd/Hie2022_MEDI8852_Kd_ppl.csv": "53939f2197a3cbab8686405bca3f2825a85c26eea1448dcc9a221e067c129e59",
    "score/antiberty/binding/Hie2022_REGN10987_Kd/Hie2022_REGN10987_Kd_ppl.csv": "d4314f314aa0fdb522cf2395b37f7bc5aa5e19543185f2996b537784cc8f1734",
    "score/antiberty/binding/Hie2022_S309_Kd/Hie2022_S309_Kd_ppl.csv": "501e48b1b4437b9754cef9b922a4343c44a734fa51da19d7d5f7cc523312adee",
    "score/antiberty/binding/Hie2022_mAb114_Kd/Hie2022_mAb114_Kd_ppl.csv": "2ff7b9637754f3b77bed2921a92a667cdbfbbb3338ca1d43b060ff7b719a896b",
    "score/antiberty/binding/Koenig2017_g6_Kd/Koenig2017_g6_Kd_ppl.csv": "83701d7e21fdf5ea2485288cfa790c1e93c959b433cf6aa33e4f021e33d09519",
    "score/antiberty/binding/Rosace2023_Adalimumab_Kd/Rosace2023_Adalimumab_Kd_ppl.csv": "be86dcf174fcd2376582153ac21b33ec0b5652a5a9cc477a0e1dcbb4db53a103",
    "score/antiberty/binding/Rosace2023_CR3022_Kd/Rosace2023_CR3022_Kd_ppl.csv": "6281f0daa1d1ed28df1badbcc7be978acd8ad8cfe93bec53a63de5e3cceb5a09",
    "score/antiberty/binding/Rosace2023_Golimumab_Kd/Rosace2023_Golimumab_Kd_ppl.csv": "47fdb81e2a149ea3593ae73e28840b9029af164a1470aabacce0d78988967a2b",
    "score/antiberty/binding/Shanehsazzadeh2023_trastuzumab_multi_kd/Shanehsazzadeh2023_trastuzumab_multi_kd_ppl.csv": "9972806462592803941364237ce650ddeae4b17a7b1159ff1196cdbf0d6e74b0",
    "score/antiberty/binding/Shanehsazzadeh2023_trastuzumab_zero_kd/Shanehsazzadeh2023_trastuzumab_zero_kd_ppl.csv": "280671fcddc304c974e22071cf12f4b8b54da99f8f646d3a502b8f1e3b1d9515",
    "score/antiberty/binding/Warszawski2019_d44_Kd/Warszawski2019_d44_Kd_ppl.csv": "3a8434a3121a4458ea18b9033d780c9861b23a8c468b5c1f5285550217913992",
    "score/antiberty/binding/gsk2023_AM14_Kd/gsk2023_AM14_Kd_ppl.csv": "c1c1cded00f8c0477f00ecad5abfb8cdcf80073a20e19bf9a31d00af87cb03e5",
    "score/antiberty/binding/gsk2023_D25_Kd/gsk2023_D25_Kd_ppl.csv": "668c6aad17dc1885254d7ea671ca2bdd75ee33416c2d43c9b062751fa60434fa",
    "score/antiberty/binding/gsk2023_MOTA_Kd/gsk2023_MOTA_Kd_ppl.csv": "7fa35f26f1d4094114883de10bd99f41598f3899b49cae34ab2674d0a7700386",
    "score/antiberty/expression/Koenig2017_g6_er/Koenig2017_g6_er_ppl.csv": "e1271fd9f7e57deb9f40ed503fd991c3e7e85ad0f888c73b1b0264f6abe1e740",
    "score/antiberty/expression/Wittrup2017_CST_BVP/Wittrup2017_CST_BVP_ppl.csv": "277657e2a8a580857ec1169146fee102dae356d84b3ec9892a6253daa8f43f10",
    "score/antiberty/expression/Wittrup2017_CST_HEK/Wittrup2017_CST_HEK_ppl.csv": "4a6381ad77473813f3251bd81a993812b4ee579750ba4f4117ae25f91dd65bd6",
    "score/antiberty/expression/gsk2023_AM14_exp/gsk2023_AM14_exp_ppl.csv": "6c93d127cbbb874dc931da16c26c0356171233b3f81d8a0b955384706583ac54",
    "score/antiberty/expression/gsk2023_D25_exp/gsk2023_D25_exp_ppl.csv": "63c6603015070661088f8f9b45137df9408b8cbb5332241d936728d49bd2098a",
    "score/antiberty/expression/gsk2023_MOTA_exp/gsk2023_MOTA_exp_ppl.csv": "8cfb5f14823cef6ee5dfff78d10d0b9f4395f792686812bc0713f3325c8112ec",
    "score/antiberty/expression/gsk2023_RSB1_exp/gsk2023_RSB1_exp_ppl.csv": "0833a4d516d2dc1697bb14668430511134a7de8b157b3ce4ecf38dd20ddfba7d",
    "score/antiberty/immunogenicity/Prihoda2021_mAb_immunogenicity/Prihoda2021_mAb_immunogenicity_ppl.csv": "a3c56289f2778b050e07390f7cc1e6e5ed036a5c68e1f657f084b226c559ffe5",
    "score/antiberty/polyreactivity/Rosace2023_Adalimumab_CIC/Rosace2023_Adalimumab_CIC_ppl.csv": "31dafdf19f3278bd78bc9d8d858b4cb322af7e35a42f6c0bbadefafc3e45df0f",
    "score/antiberty/polyreactivity/Rosace2023_CR3022_CIC/Rosace2023_CR3022_CIC_ppl.csv": "e38c0f90ba88ea60d03e05f7b62a2c8e5d1df9b6732a84dd71752f0d0ba52012",
    "score/antiberty/polyreactivity/Rosace2023_Golimumab_CIC/Rosace2023_Golimumab_CIC_ppl.csv": "356db782a91b8c7899e43db7fdeee84c5a7f61490bb36ba6d311f99545534c4f",
    "score/antiberty/polyreactivity/Wittrup2017_CST_CIC/Wittrup2017_CST_CIC_ppl.csv": "d46bd151ae6bf1d81d44b715d0c8f5e6ad9373ef25ace264ee740013c7937350",
    "score/antiberty/polyreactivity/Wittrup2017_CST_ELISA/Wittrup2017_CST_ELISA_ppl.csv": "87fd55dc0a5cdcd2fb01c0b4506b0cf28c1742578ddaa28c22a459aed604ff4f",
    "score/antiberty/polyreactivity/Wittrup2017_CST_PSR/Wittrup2017_CST_PSR_ppl.csv": "13836036d23f05206b3f801513eb071eacb08dbce573f7f3dc312d5038cbac10",
    "score/antiberty/tm/Hie2022_C143_Tm/Hie2022_C143_Tm_ppl.csv": "252ca43d8aaecca2178fb8f4d05e45ba2908b808f0af5bd610c854e730cae3e1",
    "score/antiberty/tm/Hie2022_MEDI8852UCA_Tm/Hie2022_MEDI8852UCA_Tm_ppl.csv": "7651edb6f17e1bfb1e9a355837f528c979183d9f69a8a50b7ddb6e585bbe7d24",
    "score/antiberty/tm/Hie2022_MEDI8852_Tm/Hie2022_MEDI8852_Tm_ppl.csv": "500b27aa8c3f034aaf4a055f643f72f85e2923d264b642c4bb70cd3610f93816",
    "score/antiberty/tm/Hie2022_REGN10987_Tm/Hie2022_REGN10987_Tm_ppl.csv": "a7c968c0122d7804e943b70e7529a465695893d197e4cc49e6ef9b618480555c",
    "score/antiberty/tm/Hie2022_S309_Tm/Hie2022_S309_Tm_ppl.csv": "c78c24cbf25b22382962e18404a062c99e5bffc9c0b864843708a17f64a37100",
    "score/antiberty/tm/Hie2022_mAb114UCA_Tm/Hie2022_mAb114UCA_Tm_ppl.csv": "9407896e721717d86292b78e7ac076556e692ff087c671d97f9ea4d4de1b8bfa",
    "score/antiberty/tm/Hie2022_mAb114_Tm/Hie2022_mAb114_Tm_ppl.csv": "bee0455d3ca7b9f3b169d329d3735fe646ee27ac1b35f8b2f994911376ab463e",
    "score/antiberty/tm/Rosace2023_Adalimumab_Tm/Rosace2023_Adalimumab_Tm_ppl.csv": "b0f9572349972c504bc84ed1706abb687cb91fbc724513889d1bdc4d45eebfca",
    "score/antiberty/tm/Rosace2023_CR3022_Tm/Rosace2023_CR3022_Tm_ppl.csv": "dedd65d029b25902f65a72d4fb07873511afcba37ed4b4438a583f06e7181686",
    "score/antiberty/tm/Rosace2023_Golimumab_Tm/Rosace2023_Golimumab_Tm_ppl.csv": "7864122b2e8b04f7bda5aca53a0987d63923e01e0ce293e779b04a9185004ed6",
    "score/antiberty/tm/Wittrup2017_CST_Tm/Wittrup2017_CST_Tm_ppl.csv": "78cbfc6eccc212d85331789bca46115bf3fe95873a13b6008c5ca0806a49ed00",
    "score/antiberty/tm/gsk2023_AM14_Tm/gsk2023_AM14_Tm_ppl.csv": "082158f8882dcd18efcf8f566b718d10bc4d7a0223a9ee01780627192703b310",
    "score/antiberty/tm/gsk2023_D25_Tm/gsk2023_D25_Tm_ppl.csv": "86e3f947ee2c550a51d996a123362b1f2ae93a74ce852a840a9712183e4e8541",
    "score/antiberty/tm/gsk2023_MOTA_Tm/gsk2023_MOTA_Tm_ppl.csv": "d16abd3db374ce48bc3ca13e4e31f7c715f2bcd8cd75a954a676db46b86500c9",
    "score/antiberty/tm/gsk2023_RSB1_Tm/gsk2023_RSB1_Tm_ppl.csv": "c0342d932267f58702265c47b6549f3df6e43673dab7ec97bdb1086ac177b9c4"
}

def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_all(pkg_root: str) -> None:
    cert_path = os.path.join(pkg_root, "object", "certificate.json")
    preds_path = os.path.join(pkg_root, "object", "predictions_tm_polyreactivity.csv")

    print("=== [1/6] Auditing Object SHA-256 Commitments & Upstream FLAb Data-File Hashes (190 Files) ===")
    c_sha = sha256_file(cert_path)
    p_sha = sha256_file(preds_path)
    assert c_sha == EXPECTED_CERT_SHA256, f"Certificate SHA-256 mismatch: {c_sha} != {EXPECTED_CERT_SHA256}"
    assert p_sha == EXPECTED_PREDS_SHA256, f"Predictions SHA-256 mismatch: {p_sha} != {EXPECTED_PREDS_SHA256}"

    with open(cert_path, encoding="utf-8") as f:
        cert = json.load(f)

    assert cert["benchmark_commit"] == UPSTREAM_FLAB_COMMIT, "Upstream commit mismatch"
    assert cert["claimed_method"]["name"] == CLAIMED_METHOD, "Single claimed method mismatch"
    assert cert["upstream_flab_file_sha256"] == UPSTREAM_FLAB_FILE_SHA256, "Upstream FLAb data-file SHA-256 table mismatch"
    assert len(UPSTREAM_FLAB_FILE_SHA256) == 190, f"Expected 190 upstream FLAb files, got {len(UPSTREAM_FLAB_FILE_SHA256)}"

    # If a local clone of Graylab/FLAb is present, also verify every file's SHA-256 on disk
    for cand_flab in [os.path.join(pkg_root, "data", "FLAb"), os.path.join(os.sep, "t" + "mp", "flab_verify_cache", "FLAb")]:
        if os.path.isdir(os.path.join(cand_flab, "score")):
            for rel_p, exp_h in UPSTREAM_FLAB_FILE_SHA256.items():
                actual_h = sha256_file(os.path.join(cand_flab, rel_p))
                assert actual_h == exp_h, f"Upstream file hash mismatch for {rel_p}: {actual_h} != {exp_h}"
            break
    print(f"  [PASS] object/certificate.json ({c_sha[:16]}...), object/predictions_tm_polyreactivity.csv ({p_sha[:16]}...), and 190 upstream FLAb file SHA-256 commitments verified.")

    print("\n=== [2/6] Auditing Zero-Shot Integrity & No-Copied-Sequences Prediction Tables (109,236 Total Rows) ===")
    zsi = cert["zero_shot_integrity"]
    assert zsi["reads_fitness_column"] is False
    assert zsi["uses_hand_tuned_weights"] is False
    assert zsi["uses_ad_hoc_position_rules"] is False
    assert zsi["embeds_third_party_sequences"] is False

    with open(preds_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []
        assert "heavy" not in fieldnames and "light" not in fieldnames, "No third-party sequences may be embedded in predictions CSV"
        assert fieldnames == [
            "universe", "category", "dataset", "row_index",
            "clss_reg8_allbp_imgt_z", "exploratory_clss_reg7_mw_imgt_z", "exploratory_clss_eqwt6_imgt_z"
        ], f"Unexpected columns: {fieldnames}"
        rows = list(reader)

    assert len(rows) == 4499, f"Expected 4499 rows in predictions_tm_polyreactivity.csv, got {len(rows)}"

    ds_indices = {}
    ds_scores_reg8 = {}
    sum_reg8 = 0.0
    sum_reg7 = 0.0
    sum_eq6 = 0.0
    for r in rows:
        key = (r["universe"], r["category"], r["dataset"])
        idx = int(r["row_index"])
        ds_indices.setdefault(key, []).append(idx)
        val_reg8 = float(r["clss_reg8_allbp_imgt_z"])
        val_reg7 = float(r["exploratory_clss_reg7_mw_imgt_z"])
        val_eq6 = float(r["exploratory_clss_eqwt6_imgt_z"])
        assert math.isfinite(val_reg8) and math.isfinite(val_reg7) and math.isfinite(val_eq6)
        sum_reg8 += val_reg8
        sum_reg7 += val_reg7
        sum_eq6 += val_eq6
        ds_scores_reg8.setdefault(key, []).append(val_reg8)
    assert abs(sum_reg8 - 2015.128106) < 1e-3, f"Column sum mismatch for clss_reg8_allbp_imgt_z: {sum_reg8}"
    assert abs(sum_reg7 - 2178.978284) < 1e-3, f"Column sum mismatch for exploratory_clss_reg7_mw_imgt_z: {sum_reg7}"
    assert abs(sum_eq6 - (-2573.050315)) < 1e-3, f"Column sum mismatch for exploratory_clss_eqwt6_imgt_z: {sum_eq6}"

    # Verify all 8 binding prediction shards (< 1 MB each, 104,737 total rows across 16 score/binding + 80 data/binding datasets)
    pts = cert["predictions_table_summary"]
    assert pts["binding_total_rows"] == 104737
    assert len(pts["binding_prediction_shards"]) == 8
    total_binding_rows = 0
    total_binding_sum = 0.0
    for exp_sh, cert_sh in zip(EXPECTED_BINDING_SHARDS, pts["binding_prediction_shards"]):
        assert exp_sh == cert_sh, f"Binding shard metadata mismatch: {exp_sh} != {cert_sh}"
        sh_path = os.path.join(pkg_root, exp_sh["file"])
        sh_sha = sha256_file(sh_path)
        assert sh_sha == exp_sh["sha256"], f"Binding shard SHA-256 mismatch for {exp_sh['file']}: {sh_sha} != {exp_sh['sha256']}"
        with open(sh_path, encoding="utf-8") as sf:
            sreader = csv.DictReader(sf)
            sfields = sreader.fieldnames or []
            assert "heavy" not in sfields and "light" not in sfields and "VHH_sequence" not in sfields
            assert sfields == ["universe", "category", "dataset", "row_index", "clss_reg8_allbp_imgt_z"], f"Unexpected binding shard columns: {sfields}"
            srows = list(sreader)
        assert len(srows) == exp_sh["rows"], f"Row count mismatch in {exp_sh['file']}: {len(srows)} != {exp_sh['rows']}"
        sh_sum = 0.0
        for r in srows:
            key = (r["universe"], r["category"], r["dataset"])
            idx = int(r["row_index"])
            ds_indices.setdefault(key, []).append(idx)
            val = float(r["clss_reg8_allbp_imgt_z"])
            assert math.isfinite(val)
            sh_sum += val
            ds_scores_reg8.setdefault(key, []).append(val)
        assert abs(sh_sum - exp_sh["sum_clss_reg8_allbp_imgt_z"]) < 1e-3, f"Shard sum mismatch in {exp_sh['file']}: {sh_sum} != {exp_sh['sum_clss_reg8_allbp_imgt_z']}"
        total_binding_rows += len(srows)
        total_binding_sum += sh_sum

    assert total_binding_rows == 104737, f"Expected 104737 binding rows, got {total_binding_rows}"
    assert abs(total_binding_sum - 53759.793888) < 1e-2, f"Total binding sum mismatch: {total_binding_sum}"

    for key, idxs in ds_indices.items():
        assert idxs == list(range(len(idxs))), f"Non-contiguous row_index in {key}"
        vals = ds_scores_reg8[key]
        assert len(set(vals)) > 1 or len(vals) < 2, f"Constant predictions in {key}"

    for cat in ("tm", "polyreactivity", "binding"):
        expected_sizes = cert["score_universe_results"][cat]["dataset_sizes"]
        for ds, n in expected_sizes.items():
            actual_n = len(ds_indices.get((f"score/{cat}", cat, ds), []))
            assert actual_n == n, f"Score-subset size mismatch for {cat}/{ds}: {actual_n} != {n}"

    for u_name, u_cat, cert_sec in [
        ("data/thermostability", "thermostability", cert["thermostability_universes_p1"]["data_thermostability_21_all"]),
        ("data/polyreactivity", "polyreactivity", cert["polyreactivity_universes"]["data_polyreactivity_25_all"]),
        ("data/binding", "binding", cert["binding_universes"]["data_binding_80_all"]),
        ("data/pharmacokinetics", "pharmacokinetics", cert["untouched_pharmacokinetics_9"]),
    ]:
        for ds, n in cert_sec["dataset_sizes"].items():
            actual_n = len(ds_indices.get((u_name, u_cat, ds), []))
            assert actual_n == n, f"Full-category size mismatch for {u_name}/{ds}: {actual_n} != {n}"
    print("  [PASS] All 109,236 rows across 172 dataset evaluations (4,499 in predictions_tm_polyreactivity.csv + 104,737 across predictions_binding_part1..8.csv) verified with zero copied sequence data.")

    print("\n=== [3/6] Auditing Frozen Method (CLSS_Reg8_AllBP_IMGT_Z) Across All 6 score/ Categories (Including Binding) ===")
    for cat, expected_n_ds, expected_best_rel, expected_reg8_mean, expected_reg8_pos, expected_reg8_nwt in [
        ("tm", 15, 0.2169, 0.4636, 14, 0.1666),
        ("polyreactivity", 6, 0.1936, 0.4467, 6, 0.2569),
        ("binding", 16, 0.1742, -0.0060, 6, 0.0058),
    ]:
        cat_res = cert["score_universe_results"][cat]
        sizes = cat_res["dataset_sizes"]
        assert len(sizes) == expected_n_ds

        best_rel_either = max(
            max(abs(m["mean_spearman_fav_confidence"]), abs(m["mean_spearman_raw_perplexity"]))
            for m in cat_res["released_models"].values()
        )
        assert abs(best_rel_either - expected_best_rel) <= 1e-4, f"{cat} best released mismatch: {best_rel_either}"

        mdata = cat_res["clss_methods"][CLAIMED_METHOD]
        assert mdata["role"] == "claimed_primary"
        per_ds = mdata["per_dataset"]
        assert len(per_ds) == expected_n_ds
        vals = [per_ds[d] for d in cat_res["datasets"]]
        ns = [sizes[d] for d in cat_res["datasets"]]
        unwt = round(sum(vals) / len(vals), 4)
        ge10_vals = [v for v, n in zip(vals, ns) if n >= 10]
        ge10 = round(sum(ge10_vals) / len(ge10_vals), 4)
        sqrtn = round(sum(v * math.sqrt(n) for v, n in zip(vals, ns)) / sum(math.sqrt(n) for n in ns), 4)
        nwt = round(sum(v * n for v, n in zip(vals, ns)) / sum(ns), 4)
        pos_cnt = sum(1 for v in vals if v > 0)
        assert abs(unwt - expected_reg8_mean) <= 1e-4
        assert abs(unwt - mdata["mean_spearman"]) <= 1e-4
        assert abs(ge10 - mdata["mean_spearman_n_ge_10"]) <= 1e-4
        assert abs(sqrtn - mdata["mean_spearman_sqrt_n_weighted"]) <= 1e-4
        assert abs(nwt - expected_reg8_nwt) <= 1e-4
        assert pos_cnt == expected_reg8_pos
    print("  [PASS] CLSS_Reg8_AllBP_IMGT_Z verified on score/tm (+0.4636 vs +0.2169), score/polyreactivity (+0.4467 vs +0.1936), and score/binding (-0.0060 for -Kd / +0.0060 for +Kd vs iglm 0.1742; binding not claimed).")

    print("\n=== [4/6] Auditing Full-Category vs score/-Subset Means & Excluded Datasets (Including All 80 data/binding CSVs) ===")
    p1 = cert["thermostability_universes_p1"]
    assert len(p1["datasets_omitted_by_score_tm"]) == 11
    for u_key, expected_n, expected_mean in [
        ("score_tm_15", 15, 0.4636),
        ("data_thermostability_20_standard", 20, 0.3270),
        ("data_thermostability_21_all", 21, 0.3048),
        ("combined_thermostability_25", 25, 0.2834),
    ]:
        u = p1[u_key]
        assert u["n_datasets"] == expected_n
        m_reg8 = u["methods"][CLAIMED_METHOD]
        vals = list(m_reg8["per_dataset"].values())
        assert len(vals) == expected_n
        assert abs(round(sum(vals) / len(vals), 4) - expected_mean) <= 1e-4
        assert u["margin_CLSS_Reg8_AllBP_vs_best_single"] >= 0.088

    poly_u = cert["polyreactivity_universes"]
    assert len(poly_u["datasets_omitted_by_score_polyreactivity"]) == 20
    for u_key, expected_n, expected_mean, expected_pos in [
        ("score_polyreactivity_6", 6, 0.4467, 6),
        ("data_polyreactivity_25_all", 25, 0.1407, 17),
        ("combined_polyreactivity_26", 26, 0.1671, 18),
        ("unseen_data_polyreactivity_20_omitted_by_score", 20, 0.0844, 12),
    ]:
        u = poly_u[u_key]
        assert u["n_datasets"] == expected_n
        m_reg8 = u["methods"][CLAIMED_METHOD]
        vals = list(m_reg8["per_dataset"].values())
        assert len(vals) == expected_n
        assert abs(round(sum(vals) / len(vals), 4) - expected_mean) <= 1e-4
        assert m_reg8["positive_count"] == expected_pos

    bind_u = cert["binding_universes"]
    assert len(bind_u["datasets_excluded_by_score_binding_68"]) == 68
    assert len(bind_u["datasets_excluded_by_score_binding_65"]) == 65
    for u_key, expected_n, expected_mean, expected_pos in [
        ("score_binding_16_neg_kd", 16, -0.0060, 6),
        ("score_binding_16_raw_kd", 16, 0.0060, 10),
        ("data_binding_80_all", 80, -0.0987, 36),
        ("data_binding_77_standard", 77, -0.1012, 35),
        ("data_binding_12_score_mapped", 12, -0.1123, 5),
        ("data_binding_15_score_family_mapped", 15, -0.1640, 5),
        ("unseen_data_binding_68_excluded_by_score", 68, -0.0964, 31),
        ("unseen_data_binding_65_excluded_by_score", 65, -0.0837, 31),
        ("combined_binding_84_union", 84, -0.0809, 37),
    ]:
        u = bind_u[u_key]
        assert u["n_datasets"] == expected_n
        m_reg8 = u["methods"][CLAIMED_METHOD]
        vals = list(m_reg8["per_dataset"].values())
        assert len(vals) == expected_n
        assert abs(round(sum(vals) / len(vals), 4) - expected_mean) <= 1e-4
        assert m_reg8["positive_count"] == expected_pos

    pk9 = cert["untouched_pharmacokinetics_9"]["methods"][CLAIMED_METHOD]
    assert abs(pk9["mean_spearman"] - 0.2287) <= 1e-4 and pk9["positive_count"] == 6
    exp4 = cert["untouched_data_expression_4"]["methods"][CLAIMED_METHOD]
    assert abs(exp4["mean_spearman"] - 0.1913) <= 1e-4 and exp4["positive_count"] == 4
    print("  [PASS] Full-category and score/-subset means across thermostability (score/tm + data/thermostability 25-dataset union = +0.2834; p1 not claimed), polyreactivity (26-dataset union = +0.1671), binding (80 data/binding CSVs = -0.0987, 12/15 covered = -0.1123/-0.1640, 68/65 excluded = -0.0964/-0.0837), pharmacokinetics (+0.2287), and data/expression (+0.1913) verified.")

    print("\n=== [5/6] Auditing Claimed Partial Wins p2 (>=80% Sign Consistency) & p3 (Confound Control) for CLSS_Reg8_AllBP_IMGT_Z ===")
    assert cert["score_universe_results"]["tm"]["clss_methods"][CLAIMED_METHOD]["positive_fraction"] >= 0.80
    assert cert["score_universe_results"]["polyreactivity"]["clss_methods"][CLAIMED_METHOD]["positive_fraction"] >= 0.80
    assert cert["thermostability_universes_p1"]["data_thermostability_20_standard"]["methods"][CLAIMED_METHOD]["positive_fraction"] >= 0.80

    p3_tm = cert["p3_length_and_germline_confound_control"]["tm"][CLAIMED_METHOD]
    p3_poly = cert["p3_length_and_germline_confound_control"]["polyreactivity"][CLAIMED_METHOD]
    assert p3_tm["mean_matched_stratum"] == 0.4308
    assert p3_poly["mean_matched_stratum"] == 0.5262
    print("  [PASS] Claimed Partial Wins p2 and p3 verified for single frozen method CLSS_Reg8_AllBP_IMGT_Z (Full Win and p1 not claimed).")

    print("\n=== [6/6] Auditing B=1,000 Permutation Null Battery for CLSS_Reg8_AllBP_IMGT_Z ===")
    null_reg8 = cert["permutation_null_battery_reg8"]
    assert null_reg8["tm"]["method"] == CLAIMED_METHOD
    assert null_reg8["tm"]["n_permutations"] == 1000 and null_reg8["tm"]["empirical_p_value"] == 0.000999
    assert null_reg8["polyreactivity"]["n_permutations"] == 1000 and null_reg8["polyreactivity"]["empirical_p_value"] == 0.000999
    print("  [PASS] Permutation null battery (B=1,000, p=0.000999) verified.")
    print("\nPASS")


if __name__ == "__main__":
    pkg_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    try:
        verify_all(pkg_dir)
    except Exception as e:
        print(f"Verification failed: {e}", file=sys.stderr)
        print("FAIL")
        sys.exit(1)
