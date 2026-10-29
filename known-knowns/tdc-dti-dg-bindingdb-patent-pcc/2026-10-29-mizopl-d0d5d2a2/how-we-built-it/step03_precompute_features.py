#!/usr/bin/env python3
"""
Step 3: Precompute intrinsic per-protein and per-ligand biochemical representations
(zero label usage, zero cross-split leakage: each molecule/protein is featurized
purely from its own SMILES / amino-acid sequence string).
Caches packed uint64 fingerprints (ECFP4, ECFP6, FCFP4, MACCS, Scaffold ECFP4),
Murcko scaffold & generic framework IDs, RDKit 2D physicochemical descriptors,
and protein AAC + Dipeptide + CTD + Physicochemical descriptors.
"""
import hashlib
import os
import time
from multiprocessing import Pool, cpu_count
from pathlib import Path
import numpy as np
import pandas as pd
from rdkit import Chem, DataStructs, RDLogger
from rdkit.Chem import AllChem, Crippen, Descriptors, Lipinski, MACCSkeys, MolSurf, QED, rdMolDescriptors
from rdkit.Chem.Scaffolds import MurckoScaffold
from tdc.benchmark_group import dti_dg_group

RDLogger.DisableLog("rdApp.*")

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
CACHE_DIR = BASE_DIR / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------------------------------
# 1. Protein Intrinsic Sequence Featurizer (AAC + DPC + CTD + PhysChem)
# -------------------------------------------------------------------------
AA_LIST = list("ACDEFGHIKLMNPQRSTVWY")
AA_TO_IDX = {aa: i for i, aa in enumerate(AA_LIST)}

# Kyte-Doolittle hydropathy, molecular weight, net charge at pH 7.4, volume
KD_HYDRO = {
    "A": 1.8, "C": 2.5, "D": -3.5, "E": -3.5, "F": 2.8, "G": -0.4, "H": -3.2,
    "I": 4.5, "K": -3.9, "L": 3.8, "M": 1.9, "N": -3.5, "P": -1.6, "Q": -3.5,
    "R": -4.5, "S": -0.8, "T": -0.7, "V": 4.2, "W": -0.9, "Y": -1.3,
}
AA_MW = {
    "A": 89.1, "C": 121.2, "D": 133.1, "E": 147.1, "F": 165.2, "G": 75.1, "H": 155.2,
    "I": 131.2, "K": 146.2, "L": 131.2, "M": 149.2, "N": 132.1, "P": 115.1, "Q": 146.2,
    "R": 174.2, "S": 105.1, "T": 119.1, "V": 117.1, "W": 204.2, "Y": 181.2,
}

# Standard 7 CTD groupings (3 classes each: 0, 1, 2)
CTD_GROUPS = {
    "hydrophobicity": ("RKEDQN", "GASTPHY", "CLVIMFW"),
    "vdw_volume":     ("GASTCPD", "NVEQIL", "MHKFRYW"),
    "polarity":       ("LIFWCMVY", "PATGS", "HQRKNED"),
    "polarizability": ("GASDT", "CPNVEQIL", "KMHFRYW"),
    "charge":         ("KR", "ANCQGHILMFPSTWYV", "DE"),
    "secondary_str":  ("EALMQKRH", "VIYCWFT", "GNPSD"),
    "solvent_acc":    ("ALFCGIVW", "RKQEND", "MPSTHY"),
}


def featurize_protein(seq: str) -> np.ndarray:
    s = "".join(ch for ch in seq.upper() if ch in AA_TO_IDX)
    L = max(len(s), 1)
    invL = 1.0 / L

    # 1. AAC (20)
    aac = np.zeros(20, dtype=np.float32)
    for ch in s:
        aac[AA_TO_IDX[ch]] += invL

    # 2. Dipeptide composition (400)
    dpc = np.zeros((20, 20), dtype=np.float32)
    if L >= 2:
        invL2 = 1.0 / (L - 1)
        idx_arr = [AA_TO_IDX[ch] for ch in s]
        for a, b in zip(idx_arr[:-1], idx_arr[1:]):
            dpc[a, b] += invL2
    dpc = dpc.ravel()

    # 3. CTD (7 * (3 + 3 + 15) = 147)
    ctd_feats = []
    for _, (g0, g1, g2) in CTD_GROUPS.items():
        cmap = {}
        for ch in g0: cmap[ch] = 0
        for ch in g1: cmap[ch] = 1
        for ch in g2: cmap[ch] = 2
        cls = [cmap[ch] for ch in s]
        # Composition (3)
        c0 = cls.count(0) * invL
        c1 = cls.count(1) * invL
        c2 = cls.count(2) * invL
        ctd_feats.extend([c0, c1, c2])
        # Transition (3)
        t01 = t02 = t12 = 0.0
        if L >= 2:
            invL2 = 1.0 / (L - 1)
            for a, b in zip(cls[:-1], cls[1:]):
                if a != b:
                    mn, mx = (a, b) if a < b else (b, a)
                    if mn == 0 and mx == 1: t01 += invL2
                    elif mn == 0 and mx == 2: t02 += invL2
                    else: t12 += invL2
        ctd_feats.extend([t01, t02, t12])
        # Distribution (15)
        for c_id in (0, 1, 2):
            pos = [i + 1 for i, x in enumerate(cls) if x == c_id]
            n_c = len(pos)
            if n_c == 0:
                ctd_feats.extend([0.0, 0.0, 0.0, 0.0, 0.0])
            else:
                for frac in (0.0, 0.25, 0.50, 0.75, 1.0):
                    idx_p = max(0, min(n_c - 1, int(round(frac * (n_c - 1)))))
                    ctd_feats.append(pos[idx_p] * invL)
    ctd_arr = np.array(ctd_feats, dtype=np.float32)

    # 4. Global & Terminal Physicochemical stats (25)
    hyd = np.array([KD_HYDRO[ch] for ch in s], dtype=np.float32) if L > 0 else np.zeros(1, dtype=np.float32)
    mw = np.array([AA_MW[ch] for ch in s], dtype=np.float32) if L > 0 else np.zeros(1, dtype=np.float32)
    n50 = hyd[:min(50, L)]
    c50 = hyd[max(0, L - 50):]
    pos_chg = aac[AA_TO_IDX["K"]] + aac[AA_TO_IDX["R"]] + 0.1 * aac[AA_TO_IDX["H"]]
    neg_chg = aac[AA_TO_IDX["D"]] + aac[AA_TO_IDX["E"]]
    net_chg = pos_chg - neg_chg
    tot_chg = pos_chg + neg_chg
    arom = aac[AA_TO_IDX["F"]] + aac[AA_TO_IDX["W"]] + aac[AA_TO_IDX["Y"]]
    aliph = aac[AA_TO_IDX["A"]] + aac[AA_TO_IDX["I"]] + aac[AA_TO_IDX["L"]] + aac[AA_TO_IDX["V"]]
    turn_pg = aac[AA_TO_IDX["P"]] + aac[AA_TO_IDX["G"]]
    nz = aac[aac > 0]
    entropy = float(-np.sum(nz * np.log2(nz)))

    phys = np.array([
        float(L), float(np.log1p(L)),
        float(hyd.mean()), float(hyd.std()), float(np.percentile(hyd, 10)), float(np.percentile(hyd, 90)),
        float(n50.mean()), float(c50.mean()),
        float(mw.mean()), float(mw.sum() * 1e-4),
        float(pos_chg), float(neg_chg), float(net_chg), float(tot_chg),
        float(arom), float(aliph), float(turn_pg), float(aac[AA_TO_IDX["C"]]),
        entropy,
    ], dtype=np.float32)

    return np.concatenate([aac, dpc, ctd_arr, phys])


# -------------------------------------------------------------------------
# 2. Ligand Intrinsic SMILES Featurizer (Bit-packed FPs + Scaffolds + 2D)
# -------------------------------------------------------------------------
def bv_to_uint64(bv, n_words: int) -> np.ndarray:
    on_bits = list(bv.GetOnBits())
    arr = np.zeros(n_words, dtype=np.uint64)
    for b in on_bits:
        w = b >> 6
        if w < n_words:
            arr[w] |= (np.uint64(1) << np.uint64(b & 63))
    return arr


def _featurize_single_smiles(smi: str):
    mol = Chem.MolFromSmiles(smi)
    if mol is None:
        return (
            smi, "", "",
            np.zeros(32, dtype=np.uint64),
            np.zeros(16, dtype=np.uint64),
            np.zeros(16, dtype=np.uint64),
            np.zeros(3, dtype=np.uint64),
            np.zeros(40, dtype=np.float32),
        )
    try:
        can_smi = Chem.CanonSmiles(smi)
    except Exception:
        can_smi = smi

    # Murcko scaffold & generic framework
    scaf_smi = ""
    gen_scaf_smi = ""
    scaf_mol = None
    try:
        scaf_mol = MurckoScaffold.GetScaffoldForMol(mol)
        if scaf_mol is not None and scaf_mol.GetNumAtoms() > 0:
            scaf_smi = Chem.MolToSmiles(scaf_mol, isomericSmiles=False)
            gen_mol = MurckoScaffold.MakeScaffoldGeneric(scaf_mol)
            if gen_mol is not None:
                gen_scaf_smi = Chem.MolToSmiles(gen_mol, isomericSmiles=False)
    except Exception:
        pass

    # Fingerprints:
    # 1. ECFP4 (radius 2, 2048 bits -> 32 uint64)
    bv_ecfp4 = AllChem.GetMorganFingerprintAsBitVect(mol, 2, nBits=2048)
    fp_ecfp4 = bv_to_uint64(bv_ecfp4, 32)

    # 2. ECFP6 (radius 3, 1024 bits -> 16 uint64)
    bv_ecfp6 = AllChem.GetMorganFingerprintAsBitVect(mol, 3, nBits=1024)
    fp_ecfp6 = bv_to_uint64(bv_ecfp6, 16)

    # 3. FCFP4 (radius 2, useFeatures=True, 1024 bits -> 16 uint64)
    bv_fcfp4 = AllChem.GetMorganFingerprintAsBitVect(mol, 2, nBits=1024, useFeatures=True)
    fp_fcfp4 = bv_to_uint64(bv_fcfp4, 16)

    # 4. MACCS keys (167 bits -> 3 uint64)
    bv_maccs = MACCSkeys.GenMACCSKeys(mol)
    fp_maccs = bv_to_uint64(bv_maccs, 3)

    # 5. Fast 2D physicochemical & topological descriptors (40 floats)
    try:
        mw = Descriptors.MolWt(mol)
        logp, mr = Crippen.MolLogP(mol), Crippen.MolMR(mol)
        tpsa = MolSurf.TPSA(mol)
        hasa = MolSurf.LabuteASA(mol)
        hbd = Lipinski.NumHDonors(mol)
        hba = Lipinski.NumHAcceptors(mol)
        rot = Lipinski.NumRotatableBonds(mol)
        het = Lipinski.NumHeteroatoms(mol)
        fcsp3 = Lipinski.FractionCSP3(mol)
        heavy = mol.GetNumHeavyAtoms()
        bonds = mol.GetNumBonds()
        rings = rdMolDescriptors.CalcNumRings(mol)
        arom_rings = rdMolDescriptors.CalcNumAromaticRings(mol)
        sat_rings = rdMolDescriptors.CalcNumSaturatedRings(mol)
        aliph_rings = rdMolDescriptors.CalcNumAliphaticRings(mol)
        arom_het = rdMolDescriptors.CalcNumAromaticHeterocycles(mol)
        arom_carb = rdMolDescriptors.CalcNumAromaticCarbocycles(mol)
        sat_het = rdMolDescriptors.CalcNumSaturatedHeterocycles(mol)
        spiro = rdMolDescriptors.CalcNumSpiroAtoms(mol)
        bridge = rdMolDescriptors.CalcNumBridgeheadAtoms(mol)
        amide = rdMolDescriptors.CalcNumAmideBonds(mol)
        fchg = Chem.GetFormalCharge(mol)
        try:
            qed_val = QED.qed(mol)
        except Exception:
            qed_val = 0.5
        scaf_atoms = scaf_mol.GetNumHeavyAtoms() if scaf_mol is not None else 0

        # Atom counts
        atom_counts = {6: 0, 7: 0, 8: 0, 9: 0, 15: 0, 16: 0, 17: 0, 35: 0, 53: 0}
        arom_atoms = 0
        for a in mol.GetAtoms():
            z = a.GetAtomicNum()
            if z in atom_counts:
                atom_counts[z] += 1
            if a.GetIsAromatic():
                arom_atoms += 1
        inv_heavy = 1.0 / max(heavy, 1)

        desc = np.array([
            mw, np.log1p(mw), logp, mr, tpsa, np.log1p(tpsa), hasa,
            hbd, hba, rot, het, fcsp3, heavy, bonds,
            rings, arom_rings, sat_rings, aliph_rings, arom_het, arom_carb, sat_het,
            spiro, bridge, amide, fchg, qed_val, scaf_atoms, scaf_atoms * inv_heavy,
            arom_atoms, arom_atoms * inv_heavy,
            atom_counts[6], atom_counts[7], atom_counts[8], atom_counts[9],
            atom_counts[15], atom_counts[16], atom_counts[17], atom_counts[35], atom_counts[53],
            float(bv_ecfp4.GetNumOnBits()),
        ], dtype=np.float32)
        desc = np.nan_to_num(desc, nan=0.0, posinf=0.0, neginf=0.0)
    except Exception:
        desc = np.zeros(40, dtype=np.float32)

    return (can_smi, scaf_smi, gen_scaf_smi, fp_ecfp4, fp_ecfp6, fp_fcfp4, fp_maccs, desc)


def main():
    t0 = time.time()
    group = dti_dg_group(path=str(DATA_DIR))
    bm = group.get("BindingDB_Patent")
    tv = bm["train_val"]
    te = bm["test"]

    # 1. Unique proteins across train_val and test
    all_targets = sorted(set(tv["Target"]).union(set(te["Target"])))
    print(f"Featurizing {len(all_targets)} unique protein targets...")
    prot_feats = np.vstack([featurize_protein(s) for s in all_targets])
    print(f"  prot_feats shape: {prot_feats.shape} ({time.time() - t0:.2f}s)")

    np.savez_compressed(
        CACHE_DIR / "protein_features.npz",
        targets=np.array(all_targets, dtype=object),
        prot_feats=prot_feats,
    )

    # 2. Unique SMILES across train_val and test
    t1 = time.time()
    all_smiles = sorted(set(tv["Drug"]).union(set(te["Drug"])))
    n_smi = len(all_smiles)
    n_workers = min(8, cpu_count())
    print(f"Featurizing {n_smi} unique ligand SMILES on {n_workers} workers...")

    with Pool(processes=n_workers) as pool:
        results = pool.map(_featurize_single_smiles, all_smiles, chunksize=1024)

    can_smiles = [r[0] for r in results]
    scaf_smiles = [r[1] for r in results]
    gen_scaf_smiles = [r[2] for r in results]
    fp_ecfp4 = np.vstack([r[3] for r in results])
    fp_ecfp6 = np.vstack([r[4] for r in results])
    fp_fcfp4 = np.vstack([r[5] for r in results])
    fp_maccs = np.vstack([r[6] for r in results])
    mol_desc = np.vstack([r[7] for r in results])

    # Map canonical SMILES, Murcko scaffold, and Generic scaffold to integer IDs
    uniq_can = {s: i for i, s in enumerate(sorted(set(can_smiles)))}
    uniq_scaf = {s: i for i, s in enumerate(sorted(set(scaf_smiles)))}
    uniq_gscaf = {s: i for i, s in enumerate(sorted(set(gen_scaf_smiles)))}

    can_id = np.array([uniq_can[s] for s in can_smiles], dtype=np.int32)
    scaf_id = np.array([uniq_scaf[s] if s != "" else -1 for s in scaf_smiles], dtype=np.int32)
    gscaf_id = np.array([uniq_gscaf[s] if s != "" else -1 for s in gen_scaf_smiles], dtype=np.int32)

    print(f"  Featurized {n_smi} SMILES in {time.time() - t1:.2f}s:")
    print(f"    Unique canonical SMILES: {len(uniq_can)}")
    print(f"    Unique Murcko scaffolds: {len(uniq_scaf)}")
    print(f"    Unique Generic scaffolds: {len(uniq_gscaf)}")
    print(f"    fp_ecfp4: {fp_ecfp4.shape}, fp_ecfp6: {fp_ecfp6.shape}, fp_fcfp4: {fp_fcfp4.shape}, mol_desc: {mol_desc.shape}")

    np.savez_compressed(
        CACHE_DIR / "ligand_features.npz",
        smiles=np.array(all_smiles, dtype=object),
        can_id=can_id,
        scaf_id=scaf_id,
        gscaf_id=gscaf_id,
        fp_ecfp4=fp_ecfp4,
        fp_ecfp6=fp_ecfp6,
        fp_fcfp4=fp_fcfp4,
        fp_maccs=fp_maccs,
        mol_desc=mol_desc,
    )
    print(f"Saved cache to {CACHE_DIR} in total {time.time() - t0:.2f}s")


if __name__ == "__main__":
    main()
