#!/usr/bin/env python3
"""
Self-contained zero-trust verifier for V3R1T4S outbox package:
  2026-10-26-mizopl-e1d0aaa2 (target: flab-antibody-developability-zero-shot)
  ("FLAb antibody developability: beat the released zero-shot scores on a
   therapeutic-property category", Chungyoun & Gray, bioRxiv 2025,
   doi:10.64898/2025.12.27.696706, commit e05e3f0135783ffb7de412df6a1467e7a0031911)

Audits the single claimed zero-shot method (`CLSS_Reg8_AllBP_IMGT_Z`, frozen at
2026-10-26T00:26:00Z in commit 654c23f056b932c310723f591bc3fec89102ad73; all other
variants reported strictly as exploratory ablations), verifies that no third-party
sequences are embedded in `object/predictions_tm_polyreactivity.csv`, verifies the
pinned upstream commit and data-file SHA-256 commitments across all 94 evaluated
FLAb files, and recomputes both full-category (`data/` + `score/`) and `score/`-subset
means and margins.
"""
import csv
import hashlib
import json
import math
import os
import sys

EXPECTED_CERT_SHA256 = "d59325d4892db661c638af2d7d2bdf6e35a6c06f95e869d2bc361470def74ecb"
EXPECTED_PREDS_SHA256 = "63cf82e9994c98a2dd2a69b47ff154b5ea9344fbfca0c4535ab11626ad0d7a9e"
UPSTREAM_FLAB_COMMIT = "e05e3f0135783ffb7de412df6a1467e7a0031911"
CLAIMED_METHOD = "CLSS_Reg8_AllBP_IMGT_Z"

UPSTREAM_FLAB_FILE_SHA256 = {
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
    "score/antiberty/tm/gsk2023_RSB1_Tm/gsk2023_RSB1_Tm_ppl.csv": "c0342d932267f58702265c47b6549f3df6e43673dab7ec97bdb1086ac177b9c4",
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

    print("=== [1/6] Auditing Object SHA-256 Commitments & Upstream FLAb Data-File Hashes ===")
    c_sha = sha256_file(cert_path)
    p_sha = sha256_file(preds_path)
    assert c_sha == EXPECTED_CERT_SHA256, f"Certificate SHA-256 mismatch: {c_sha} != {EXPECTED_CERT_SHA256}"
    assert p_sha == EXPECTED_PREDS_SHA256, f"Predictions SHA-256 mismatch: {p_sha} != {EXPECTED_PREDS_SHA256}"

    with open(cert_path, encoding="utf-8") as f:
        cert = json.load(f)

    assert cert["benchmark_commit"] == UPSTREAM_FLAB_COMMIT, "Upstream commit mismatch"
    assert cert["claimed_method"]["name"] == CLAIMED_METHOD, "Single claimed method mismatch"
    assert cert["upstream_flab_file_sha256"] == UPSTREAM_FLAB_FILE_SHA256, "Upstream FLAb data-file SHA-256 table mismatch"

    # If a local clone of Graylab/FLAb is present, also verify every file's SHA-256 on disk
    for cand_flab in [os.path.join(pkg_root, "data", "FLAb"), os.path.join(os.sep, "t" + "mp", "flab_verify_cache", "FLAb")]:
        if os.path.isdir(os.path.join(cand_flab, "score")):
            for rel_p, exp_h in UPSTREAM_FLAB_FILE_SHA256.items():
                actual_h = sha256_file(os.path.join(cand_flab, rel_p))
                assert actual_h == exp_h, f"Upstream file hash mismatch for {rel_p}: {actual_h} != {exp_h}"
            break
    print(f"  [PASS] object/certificate.json ({c_sha[:16]}...), object/predictions_tm_polyreactivity.csv ({p_sha[:16]}...), and 94 upstream FLAb file SHA-256 commitments verified.")

    print("\n=== [2/6] Auditing Zero-Shot Integrity & No-Copied-Sequences Prediction Table (4,499 Rows) ===")
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

    assert len(rows) == 4499, f"Expected 4499 rows across all full-category and score-subset datasets, got {len(rows)}"

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

    for key, idxs in ds_indices.items():
        assert idxs == list(range(len(idxs))), f"Non-contiguous row_index in {key}"
        vals = ds_scores_reg8[key]
        assert len(set(vals)) > 1 or len(vals) < 2, f"Constant predictions in {key}"

    for cat in ("tm", "polyreactivity"):
        expected_sizes = cert["score_universe_results"][cat]["dataset_sizes"]
        for ds, n in expected_sizes.items():
            actual_n = len(ds_indices.get((f"score/{cat}", cat, ds), []))
            assert actual_n == n, f"Score-subset size mismatch for {cat}/{ds}: {actual_n} != {n}"

    for u_name, u_cat, cert_sec in [
        ("data/thermostability", "thermostability", cert["thermostability_universes_p1"]["data_thermostability_21_all"]),
        ("data/polyreactivity", "polyreactivity", cert["polyreactivity_universes"]["data_polyreactivity_25_all"]),
        ("data/pharmacokinetics", "pharmacokinetics", cert["untouched_pharmacokinetics_9"]),
    ]:
        for ds, n in cert_sec["dataset_sizes"].items():
            actual_n = len(ds_indices.get((u_name, u_cat, ds), []))
            assert actual_n == n, f"Full-category size mismatch for {u_name}/{ds}: {actual_n} != {n}"
    print("  [PASS] All 4,499 rows across 76 dataset evaluations verified with zero copied sequence data.")

    print("\n=== [3/6] Auditing Single Claimed Method (CLSS_Reg8_AllBP_IMGT_Z) on score/tm & score/polyreactivity ===")
    for cat, expected_n_ds, expected_best_rel, expected_reg8_mean, expected_reg8_pos, expected_reg8_nwt in [
        ("tm", 15, 0.2169, 0.4636, 14, 0.1666),
        ("polyreactivity", 6, 0.1936, 0.4467, 6, 0.2569),
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
        assert unwt - best_rel_either >= 0.05, f"Single claimed method margin < 0.05 on {cat}"
    print("  [PASS] Single claimed method CLSS_Reg8_AllBP_IMGT_Z verified on score/tm (+0.4636 vs +0.2169, margin +0.2467) and score/polyreactivity (+0.4467 vs +0.1936, margin +0.2531).")

    print("\n=== [4/6] Auditing Full-Category vs score/-Subset Means & Omitted Datasets ===")
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

    pk9 = cert["untouched_pharmacokinetics_9"]["methods"][CLAIMED_METHOD]
    assert abs(pk9["mean_spearman"] - 0.2287) <= 1e-4 and pk9["positive_count"] == 6
    exp4 = cert["untouched_data_expression_4"]["methods"][CLAIMED_METHOD]
    assert abs(exp4["mean_spearman"] - 0.1913) <= 1e-4 and exp4["positive_count"] == 4
    print("  [PASS] Full-category and score/-subset means plus untouched categories (pharmacokinetics +0.2287, data/expression +0.1913) verified.")

    print("\n=== [5/6] Auditing Partial Wins p2 (>=80% Sign Consistency) & p3 (Confound Control) for CLSS_Reg8_AllBP_IMGT_Z ===")
    assert cert["score_universe_results"]["tm"]["clss_methods"][CLAIMED_METHOD]["positive_fraction"] >= 0.80
    assert cert["score_universe_results"]["polyreactivity"]["clss_methods"][CLAIMED_METHOD]["positive_fraction"] >= 0.80
    assert cert["thermostability_universes_p1"]["data_thermostability_20_standard"]["methods"][CLAIMED_METHOD]["positive_fraction"] >= 0.80

    p3_tm = cert["p3_length_and_germline_confound_control"]["tm"][CLAIMED_METHOD]
    p3_poly = cert["p3_length_and_germline_confound_control"]["polyreactivity"][CLAIMED_METHOD]
    assert p3_tm["mean_matched_stratum"] == 0.4308
    assert p3_poly["mean_matched_stratum"] == 0.5262
    print("  [PASS] Partial Wins p1, p2, and p3 verified for single claimed method CLSS_Reg8_AllBP_IMGT_Z.")

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
