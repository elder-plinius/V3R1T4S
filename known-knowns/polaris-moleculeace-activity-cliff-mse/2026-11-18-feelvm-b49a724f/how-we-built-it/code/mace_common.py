"""Shared instrument for the MoleculeACE JAK1 (CHEMBL2835_Ki) attack.

Loads the official CSV, featurizes, and provides the frozen split / InChIKey machinery.
"""
import csv
import hashlib
import os

import numpy as np
from rdkit import Chem, RDLogger
from rdkit.Chem import MACCSkeys, rdMolDescriptors
from rdkit.Chem import Descriptors
from rdkit.Chem.AllChem import GetMorganFingerprintAsBitVect

CALC_MOL_DESCRIPTORS = Descriptors.CalcMolDescriptors

RDLogger.DisableLog("rdApp.*")

RUN = r"<RUNDIR>"
CSV_DIR = os.path.join(RUN, "data", "moleculeace_csv")
PRIMARY = "CHEMBL2835_Ki"


def csv_sha256(name):
    with open(os.path.join(CSV_DIR, name + ".csv"), "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def load_dataset(name=PRIMARY):
    """Return dict with rows, masks, labels, features in official CSV order."""
    path = os.path.join(CSV_DIR, name + ".csv")
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    smiles = [r["smiles"] for r in rows]
    y = np.array([float(r["y"]) for r in rows])
    y_p = np.array([float(r["y [pEC50/pKi]"]) for r in rows])
    cliff = np.array([int(r["cliff_mol"]) for r in rows])
    split = np.array([r["split"] for r in rows])
    mols = [Chem.MolFromSmiles(s) for s in smiles]
    return {
        "name": name, "path": path, "sha256": csv_sha256(name), "rows": rows,
        "smiles": smiles, "mols": mols, "y": y, "y_p": y_p,
        "cliff": cliff, "split": split,
        "train": split == "train", "test": split == "test",
    }


def stereo_stripped_inchikey(mol):
    """InChIKey ignoring stereo: recompute from a stereo-stripped molecule."""
    from rdkit.Chem.inchi import MolToInchiKey
    m = Chem.Mol(mol)
    Chem.RemoveStereochemistry(m)
    return MolToInchiKey(m)


def inchikeys(ds):
    return [stereo_stripped_inchikey(m) if m is not None else None for m in ds["mols"]]


def ecfp(mols, radius=2, nbits=1024):
    X = np.zeros((len(mols), nbits), dtype=np.float64)
    for i, m in enumerate(mols):
        if m is None:
            continue
        fp = GetMorganFingerprintAsBitVect(m, radius, nBits=nbits)
        arr = np.zeros((nbits,), dtype=np.int8)
        for b in fp.GetOnBits():
            arr[b] = 1
        X[i] = arr
    return X


def ecfp_count(mols, radius=2, nbits=1024):
    """Count-based ECFP (Gen Morgan counts, folded)."""
    from rdkit.Chem import rdMolDescriptors as rd
    X = np.zeros((len(mols), nbits), dtype=np.float64)
    for i, m in enumerate(mols):
        if m is None:
            continue
        fv = rd.GetHashedMorganFingerprint(m, radius, nBits=nbits)
        for k, v in fv.GetNonzeroElements().items():
            X[i, k] = v
    return X


def fcfp(mols, radius=2, nbits=1024):
    from rdkit.Chem.Scaffolds import MurckoScaffold  # noqa (unused, keep imports local)
    from rdkit.Chem import rdFingerprintGenerator
    inv = rdFingerprintGenerator.GetMorganFeatureAtomInvGen()
    gen = rdFingerprintGenerator.GetMorganGenerator(radius=radius, fpSize=nbits, atomInvariantsGenerator=inv)
    X = np.zeros((len(mols), nbits), dtype=np.float64)
    for i, m in enumerate(mols):
        if m is None:
            continue
        fp = gen.GetFingerprint(m)
        for b in fp.GetOnBits():
            X[i, b] = 1
    return X


def maccs(mols):
    X = np.zeros((len(mols), 167), dtype=np.float64)
    for i, m in enumerate(mols):
        if m is None:
            continue
        fp = MACCSkeys.GenMACCSKeys(m)
        for b in fp.GetOnBits():
            if b - 1 < 167:
                X[i, b - 1] = 1
    return X


_RDKIT_DESCS = None


def rdkit2d(mols):
    """RDKit 2D descriptors (the ~210 descriptor set), invalid rows zeroed."""
    global _RDKIT_DESCS
    if _RDKIT_DESCS is None:
        _RDKIT_DESCS = sorted(CALC_MOL_DESCRIPTORS(Chem.MolFromSmiles("CCO")).keys())
    X = np.zeros((len(mols), len(_RDKIT_DESCS)))
    for i, m in enumerate(mols):
        if m is None:
            continue
        try:
            d = CALC_MOL_DESCRIPTORS(m)
            X[i] = [d[k] for k in _RDKIT_DESCS]
        except Exception:
            continue
    # impute NaN/inf and clip extreme magnitudes (some descriptors blow up on edge cases;
    # float32 trees overflow otherwise)
    X = np.nan_to_num(X, nan=0.0, posinf=0.0, neginf=0.0)
    np.clip(X, -1e12, 1e12, out=X)
    return X


def descriptor_names():
    return ["ECFP4", "ECFP6", "FCFP4", "MACCS", "RDKIT2D"]


def featurize(mols, which):
    if which == "ECFP4":  return ecfp(mols, 2, 1024)
    if which == "ECFP6":  return ecfp(mols, 3, 1024)
    if which == "FCFP4":  return fcfp(mols, 2, 1024)
    if which == "MACCS":  return maccs(mols)
    if which == "RDKIT2D": return rdkit2d(mols)
    raise ValueError(which)
