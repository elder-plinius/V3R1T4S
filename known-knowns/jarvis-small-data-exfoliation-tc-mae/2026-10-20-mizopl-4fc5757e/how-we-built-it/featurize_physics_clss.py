#!/usr/bin/env python3
"""
Strict Leak-Free Physics-Informed CLSS Crystal & Composition Feature Engine (v2).
Uses ONLY raw crystal geometry (lattice_mat, coords, elements) or chemical formula
and elemental constants (jarvis Specie cfid + magpie). Zero DFT target/property leakage.

Physical Feature Blocks:
  1. Compositional & Stoichiometric Moments (Magpie 21 + Fundamental CFID 42 + Full CFID 438)
  2. BCS Superconductivity McMillan / Allen-Dynes Priors (M^{-1/2}, Debye velocity, Matthias e/a, Hopfield d/p filling)
  3. Ward-2017 SiteStatsFingerprint Superset (21-property LocalPropertyDifference, LocalPropertyMean, Coordination, PackingEfficiency, StructuralHeterogeneity)
  4. Topological Periodic Bond-Graph Layer Decomposition (0D/1D/2D/3D component ranks across 8 covalent scales + cleavage gap)
  5. Grimme D3 / London C6 & C8 Interlayer vs Intralayer Dispersion Contact Energies
  6. Point-Group Multipole Tensor Invariants:
     - 1st-rank Polar / Site Dipole Asymmetry vectors
     - 2nd-rank Traceless Quadrupole / Electric Field Gradient (EFG) Tensor eigenvalues
     - 3rd-rank Odd-Parity Piezoelectric Structure Tensor & Exact Centrosymmetry Test
  7. Smooth Multi-Weight Radial Distribution Functions (RDF), Bond-Angle Distributions (ADF), and Quotient Graph Laplacian Spectrum
"""
import math
import numpy as np
from scipy.spatial import cKDTree
from jarvis.core.specie import Specie
from jarvis.core.composition import Composition

_CFID_CACHE = {}
_MAGPIE_CACHE = {}
_COV_RAD = {}
_MASS = {}
_ION_EN = {}
_POLARIZ = {}
_ELEC_NEG = {}
_Z_NUM = {}
_VAL_D = {}
_VAL_P = {}
_VAL_S = {}
_UNFILL_D = {}
_KV_EL = {}
_GV_EL = {}

_SAMPLE_CFID_KEYS = list(Specie("H", source="cfid")._data["H"].keys())
_SAMPLE_MAG_KEYS = list(Specie("H", source="magpie")._data["H"].keys())

_FUND_CFID_KEYS = [
    "Z", "atom_mass", "atom_rad", "avg_ion_rad", "X", "first_ion_en", "elec_aff",
    "polzbl", "mol_vol", "vol_pa", "voro_coord", "KV", "GV", "therm_cond",
    "hfus", "mp", "bp", "row", "column", "max_oxid_s", "min_oxid_s",
    "ndvalence", "npvalence", "nsvalence", "nfvalence",
    "ndunfill", "npunfill", "nsunfill", "nfunfill",
    "op_eg", "mop_eg", "jv_enp", "oq_bg", "oq_enp",
    "is_alkali", "is_alkaline", "is_metalloid", "is_transition_metal",
    "is_halogen", "is_lanthanoid", "is_actinoid", "is_noble_gas"
]
_FUND_CFID_IDX = [_SAMPLE_CFID_KEYS.index(k) for k in _FUND_CFID_KEYS if k in _SAMPLE_CFID_KEYS]


def _get_el_info(el: str):
    if el not in _CFID_CACHE:
        try:
            sc = Specie(el, source="cfid")
            arr_c = np.nan_to_num(np.array(sc.get_descrp_arr, dtype=np.float64), nan=0.0, posinf=0.0, neginf=0.0)
            d_c = sc._data.get(el, {})
        except Exception:
            arr_c = np.zeros(len(_SAMPLE_CFID_KEYS), dtype=np.float64)
            d_c = {}
        try:
            sm = Specie(el, source="magpie")
            arr_m = np.nan_to_num(np.array(sm.get_descrp_arr, dtype=np.float64), nan=0.0, posinf=0.0, neginf=0.0)
            d_m = sm._data.get(el, {})
        except Exception:
            arr_m = np.zeros(len(_SAMPLE_MAG_KEYS), dtype=np.float64)
            d_m = {}
        _CFID_CACHE[el] = arr_c
        _MAGPIE_CACHE[el] = arr_m
        r_cov = float(d_m.get("CovalentRadius", 100.0) or 100.0) / 100.0
        if r_cov <= 0.1:
            r_cov = float(d_c.get("atom_rad", 1.2) or 1.2)
        _COV_RAD[el] = max(r_cov, 0.30)
        _MASS[el] = max(float(d_c.get("atom_mass", d_m.get("AtomicWeight", 20.0)) or 20.0), 1.0079)
        _ION_EN[el] = max(float(d_c.get("first_ion_en", 7.0) or 7.0), 1.0)
        _POLARIZ[el] = max(float(d_c.get("polzbl", 5.0) or 5.0), 0.1)
        _ELEC_NEG[el] = float(d_c.get("X", d_m.get("Electronegativity", 1.8)) or 1.8)
        _Z_NUM[el] = float(d_c.get("Z", d_m.get("Number", 10.0)) or 10.0)
        _VAL_D[el] = float(d_m.get("NdValence", d_c.get("ndvalence", 0.0)) or 0.0)
        _VAL_P[el] = float(d_m.get("NpValence", d_c.get("npvalence", 0.0)) or 0.0)
        _VAL_S[el] = float(d_m.get("NsValence", d_c.get("nsvalence", 0.0)) or 0.0)
        _UNFILL_D[el] = float(d_m.get("NdUnfilled", d_c.get("ndunfill", 0.0)) or 0.0)
        _KV_EL[el] = max(float(d_c.get("KV", 50.0) or 50.0), 0.0)
        _GV_EL[el] = max(float(d_c.get("GV", 25.0) or 25.0), 0.0)
    return _CFID_CACHE[el], _MAGPIE_CACHE[el]


def featurize_composition_dict(el_counts: dict) -> np.ndarray:
    """Compute compositional + BCS McMillan/Allen-Dynes elemental priors from {el: count}."""
    tot = float(sum(el_counts.values()))
    if tot <= 0:
        tot = 1.0
    els = list(el_counts.keys())
    fracs = np.array([el_counts[e] / tot for e in els], dtype=np.float64)

    cfid_mat = []
    mag_mat = []
    for e in els:
        c_arr, m_arr = _get_el_info(e)
        cfid_mat.append(c_arr[_FUND_CFID_IDX])
        mag_mat.append(m_arr)
    cfid_mat = np.vstack(cfid_mat)  # (n_el, 42)
    mag_mat = np.vstack(mag_mat)    # (n_el, 21)
    comb = np.hstack([mag_mat, cfid_mat])  # (n_el, 63)

    w_mean = np.sum(comb * fracs[:, None], axis=0)
    w_var = np.sum(((comb - w_mean[None, :]) ** 2) * fracs[:, None], axis=0)
    w_std = np.sqrt(np.maximum(w_var, 0.0))
    w_mad = np.sum(np.abs(comb - w_mean[None, :]) * fracs[:, None], axis=0)
    c_min = np.min(comb, axis=0)
    c_max = np.max(comb, axis=0)
    c_range = c_max - c_min
    mode_idx = int(np.argmax(fracs))
    c_mode = comb[mode_idx]

    full_cfid = np.vstack([_CFID_CACHE[e] for e in els])
    cfid_mean = np.sum(full_cfid * fracs[:, None], axis=0)
    cfid_std = np.sqrt(np.maximum(np.sum(((full_cfid - cfid_mean[None, :]) ** 2) * fracs[:, None], axis=0), 0.0))

    n_species = float(len(els))
    l2 = float(np.sum(fracs ** 2) ** (1.0 / 2.0))
    l3 = float(np.sum(fracs ** 3) ** (1.0 / 3.0))
    l5 = float(np.sum(fracs ** 5) ** (1.0 / 5.0))
    l7 = float(np.sum(fracs ** 7) ** (1.0 / 7.0))
    l10 = float(np.sum(fracs ** 10) ** (1.0 / 10.0))
    entropy = float(-np.sum(fracs * np.log(np.maximum(fracs, 1e-12))))
    max_frac = float(np.max(fracs))
    min_frac = float(np.min(fracs))

    masses = np.array([_MASS[e] for e in els], dtype=np.float64)
    inv_sqrt_m = 1.0 / np.sqrt(masses)
    inv_m = 1.0 / masses
    mean_inv_sqrt_m = float(np.sum(fracs * inv_sqrt_m))
    std_inv_sqrt_m = float(np.sqrt(np.sum(fracs * (inv_sqrt_m - mean_inv_sqrt_m) ** 2)))
    max_inv_sqrt_m = float(np.max(inv_sqrt_m))
    min_mass = float(np.min(masses))
    max_mass = float(np.max(masses))
    harm_mass = float(1.0 / np.sum(fracs * inv_m))
    geom_mass = float(np.exp(np.sum(fracs * np.log(masses))))
    mass_ratio = max_mass / max(min_mass, 1.0)

    zs = np.array([_Z_NUM[e] for e in els], dtype=np.float64)
    frac_H = float(np.sum(fracs[zs == 1]))
    frac_B_C_N = float(np.sum(fracs[(zs >= 5) & (zs <= 7)]))
    frac_light_Z8 = float(np.sum(fracs[zs <= 8]))
    frac_light_Z16 = float(np.sum(fracs[zs <= 16]))

    val_s = np.array([_VAL_S[e] for e in els], dtype=np.float64)
    val_p = np.array([_VAL_P[e] for e in els], dtype=np.float64)
    val_d = np.array([_VAL_D[e] for e in els], dtype=np.float64)
    unf_d = np.array([_UNFILL_D[e] for e in els], dtype=np.float64)
    ve_tot = val_s + val_p + val_d
    ea = float(np.sum(fracs * ve_tot))
    matthias_peak1 = math.exp(-((ea - 4.7) ** 2) / 0.8)
    matthias_peak2 = math.exp(-((ea - 6.5) ** 2) / 0.8)
    d_frac = float(np.sum(fracs * val_d) / max(ea, 1.0))
    p_frac = float(np.sum(fracs * val_p) / max(ea, 1.0))
    s_frac = float(np.sum(fracs * val_s) / max(ea, 1.0))
    d_fill = float(np.sum(fracs * (val_d / 10.0) * (unf_d / 10.0)))

    kv_mean = float(np.sum(fracs * np.array([_KV_EL[e] for e in els])))
    gv_mean = float(np.sum(fracs * np.array([_GV_EL[e] for e in els])))
    debye_el_proxy = math.sqrt(max(gv_mean, 0.1)) * mean_inv_sqrt_m
    debye_bulk_proxy = math.sqrt(max(kv_mean + 1.333 * gv_mean, 0.1)) * mean_inv_sqrt_m

    bcs_priors = np.array([
        n_species, l2, l3, l5, l7, l10, entropy, max_frac, min_frac,
        mean_inv_sqrt_m, std_inv_sqrt_m, max_inv_sqrt_m, min_mass, max_mass,
        harm_mass, geom_mass, mass_ratio, math.log(mass_ratio + 1.0),
        frac_H, frac_B_C_N, frac_light_Z8, frac_light_Z16,
        ea, matthias_peak1, matthias_peak2, d_frac, p_frac, s_frac, d_fill,
        debye_el_proxy, debye_bulk_proxy,
        debye_el_proxy * d_fill, debye_el_proxy * p_frac,
    ], dtype=np.float64)

    return np.concatenate([w_mean, w_std, w_mad, c_min, c_max, c_range, c_mode, bcs_priors, cfid_mean, cfid_std])


def featurize_formula(formula: str) -> np.ndarray:
    comp = Composition.from_string(formula).to_dict()
    return featurize_composition_dict(comp)


def _periodic_component_ranks(n_atoms: int, edges_i: np.ndarray, edges_j: np.ndarray, shifts: np.ndarray):
    visited = np.full(n_atoms, -1, dtype=np.int32)
    pos_shift = np.zeros((n_atoms, 3), dtype=np.float64)
    adj = [[] for _ in range(n_atoms)]
    for u, v, s in zip(edges_i, edges_j, shifts):
        adj[u].append((v, s))

    comp_dims = np.zeros(n_atoms, dtype=np.int32)
    n_comps = 0
    for start in range(n_atoms):
        if visited[start] != -1:
            continue
        cid = n_comps
        n_comps += 1
        visited[start] = cid
        stack = [start]
        members = [start]
        cycle_vecs = []
        while stack:
            u = stack.pop()
            for v, s in adj[u]:
                if visited[v] == -1:
                    visited[v] = cid
                    pos_shift[v] = pos_shift[u] + s
                    stack.append(v)
                    members.append(v)
                elif visited[v] == cid:
                    cyc = pos_shift[u] + s - pos_shift[v]
                    if np.any(np.abs(cyc) > 1e-5):
                        cycle_vecs.append(cyc)
        if not cycle_vecs:
            dim = 0
        else:
            mat = np.array(cycle_vecs, dtype=np.float64)
            svals = np.linalg.svd(mat, compute_uv=False)
            dim = int(np.sum(svals > 1e-4))
        for m in members:
            comp_dims[m] = dim
    return visited, comp_dims, n_comps


def _check_inversion_symmetry(frac_coords: np.ndarray, elements: list, lat: np.ndarray) -> tuple[float, float]:
    """
    Fast exact check for crystallographic inversion symmetry (r -> -r + t0 mod 1).
    Returns (is_centrosymmetric_flag, min_inversion_rmsd_angstrom).
    """
    n = len(elements)
    if n == 1:
        return 1.0, 0.0
    # Group fractional coords by element, pick rarest element to generate candidate inversion origins t0 = f_0 + f_k
    el_groups = {}
    for i, e in enumerate(elements):
        el_groups.setdefault(e, []).append(i)
    rarest_el = min(el_groups.keys(), key=lambda k: len(el_groups[k]))
    rarest_idx = el_groups[rarest_el]
    f0 = frac_coords[rarest_idx[0]]

    best_rmsd = 10.0
    for k in rarest_idx:
        t0 = f0 + frac_coords[k]
        # Inverted fractional positions: (-frac + t0) mod 1
        inv_f = np.mod(-frac_coords + t0[None, :], 1.0)
        # Check max nearest-neighbor discrepancy within each element group
        max_d_sq = 0.0
        possible = True
        for e, idxs in el_groups.items():
            orig_e = frac_coords[idxs]
            inv_e = inv_f[idxs]
            # Minimum image fractional difference
            diff = orig_e[:, None, :] - inv_e[None, :, :]
            diff = diff - np.round(diff)
            cart_diff = diff @ lat
            dist_mat = np.sum(cart_diff ** 2, axis=-1)
            min_per_site = np.min(dist_mat, axis=1)
            m_sq = float(np.max(min_per_site))
            if m_sq > max_d_sq:
                max_d_sq = m_sq
            if max_d_sq > 0.25:  # > 0.5 A
                possible = False
                break
        rmsd = math.sqrt(max_d_sq)
        if rmsd < best_rmsd:
            best_rmsd = rmsd
        if best_rmsd < 0.05:
            return 1.0, best_rmsd
    return (1.0 if best_rmsd < 0.12 else 0.0), best_rmsd


def featurize_structure(atoms_dict: dict) -> np.ndarray:
    lat = np.array(atoms_dict["lattice_mat"], dtype=np.float64)
    coords = np.array(atoms_dict["coords"], dtype=np.float64)
    elements = list(atoms_dict["elements"])
    cartesian = bool(atoms_dict.get("cartesian", False))
    n_atoms = len(elements)

    if cartesian:
        inv_lat = np.linalg.inv(lat)
        frac_coords = np.mod(coords @ inv_lat, 1.0)
        cart_coords = frac_coords @ lat
    else:
        frac_coords = np.mod(coords, 1.0)
        cart_coords = frac_coords @ lat

    el_counts = {}
    for e in elements:
        el_counts[e] = el_counts.get(e, 0) + 1
    comp_feat = featurize_composition_dict(el_counts)

    vol = max(abs(float(np.linalg.det(lat))), 1.0)
    v_pa = vol / n_atoms
    log_v_pa = math.log(v_pa)
    norms = np.linalg.norm(lat, axis=1)
    a_len, b_len, c_len = sorted(norms)
    c_over_a = c_len / max(a_len, 0.1)
    b_over_a = b_len / max(a_len, 0.1)
    c_over_b = c_len / max(b_len, 0.1)

    cross_ab = np.linalg.norm(np.cross(lat[0], lat[1]))
    cross_bc = np.linalg.norm(np.cross(lat[1], lat[2]))
    cross_ca = np.linalg.norm(np.cross(lat[2], lat[0]))
    h_perp = np.array([vol / max(cross_bc, 1e-4), vol / max(cross_ca, 1e-4), vol / max(cross_ab, 1e-4)])
    areas = np.array([cross_bc, cross_ca, cross_ab])

    radii = np.array([_COV_RAD[e] for e in elements], dtype=np.float64)
    masses = np.array([_MASS[e] for e in elements], dtype=np.float64)
    enegs = np.array([_ELEC_NEG[e] for e in elements], dtype=np.float64)
    zs = np.array([_Z_NUM[e] for e in elements], dtype=np.float64)
    val_d = np.array([_VAL_D[e] for e in elements], dtype=np.float64)
    val_p = np.array([_VAL_P[e] for e in elements], dtype=np.float64)
    ion_e = np.array([_ION_EN[e] for e in elements], dtype=np.float64)
    polz = np.array([_POLARIZ[e] for e in elements], dtype=np.float64)
    site_mag = np.vstack([_MAGPIE_CACHE[e] for e in elements])  # (n_atoms, 21)

    atom_vol_sum = float(np.sum((4.0 * math.pi / 3.0) * (radii ** 3)))
    packing_frac = atom_vol_sum / vol
    tot_mass = float(np.sum(masses))
    density = (tot_mass * 1.660539) / vol

    is_centro, inv_rmsd = _check_inversion_symmetry(frac_coords, elements, lat)

    miller_dirs = [
        (1, 0, 0), (0, 1, 0), (0, 0, 1),
        (1, 1, 0), (1, -1, 0), (1, 0, 1), (1, 0, -1), (0, 1, 1), (0, 1, -1),
        (1, 1, 1), (1, 1, -1), (1, -1, 1), (-1, 1, 1)
    ]
    recip = np.linalg.inv(lat).T
    max_cart_gap = 0.0
    max_rel_gap = 0.0
    max_gap_area_norm = 0.0
    axis_gaps_cart = []
    for idx_m, m_vec in enumerate(miller_dirs):
        m_arr = np.array(m_vec, dtype=np.float64)
        g_cart = m_arr @ recip
        g_norm = float(np.linalg.norm(g_cart))
        if g_norm < 1e-6:
            continue
        d_spacing = 1.0 / g_norm
        proj = np.mod(frac_coords @ m_arr, 1.0)
        p_sorted = np.sort(proj)
        diffs = np.diff(np.append(p_sorted, p_sorted[0] + 1.0))
        g_frac = float(np.max(diffs))
        g_c = g_frac * d_spacing
        if idx_m < 3:
            axis_gaps_cart.append(g_c)
        if g_c > max_cart_gap:
            max_cart_gap = g_c
            max_rel_gap = g_frac
            max_gap_area_norm = g_c / max(d_spacing, 0.5)

    r_max = 9.0
    n_rep = np.clip(np.ceil(r_max / np.maximum(h_perp, 1.0)).astype(int), 1, 5)
    gx = np.arange(-n_rep[0], n_rep[0] + 1)
    gy = np.arange(-n_rep[1], n_rep[1] + 1)
    gz = np.arange(-n_rep[2], n_rep[2] + 1)
    shifts_grid = np.stack(np.meshgrid(gx, gy, gz, indexing="ij"), axis=-1).reshape(-1, 3)
    cart_shifts = shifts_grid @ lat

    sc_coords = (cart_coords[None, :, :] + cart_shifts[:, None, :]).reshape(-1, 3)
    sc_atom_idx = np.tile(np.arange(n_atoms), len(shifts_grid))
    sc_shift_idx = np.repeat(np.arange(len(shifts_grid)), n_atoms)

    tree = cKDTree(sc_coords)
    d_list, idx_list = tree.query(cart_coords, k=min(65, len(sc_coords)), distance_upper_bound=r_max)

    u_list, v_list, dist_list, shift_vec_list, vec_list = [], [], [], [], []
    nn1_dists = np.zeros(n_atoms, dtype=np.float64)
    nn2_dists = np.zeros(n_atoms, dtype=np.float64)
    nn4_dists = np.zeros(n_atoms, dtype=np.float64)
    nn6_dists = np.zeros(n_atoms, dtype=np.float64)
    nn12_dists = np.zeros(n_atoms, dtype=np.float64)
    eff_cn = np.zeros(n_atoms, dtype=np.float64)
    site_bond_std = np.zeros(n_atoms, dtype=np.float64)
    site_loc_diff = np.zeros((n_atoms, 21), dtype=np.float64)

    for i in range(n_atoms):
        ds = d_list[i]
        ixs = idx_list[i]
        valid = (ds > 1e-4) & (ds < r_max) & (ixs < len(sc_coords))
        ds_v = ds[valid]
        ixs_v = ixs[valid]
        if len(ds_v) == 0:
            continue
        order = np.argsort(ds_v)
        ds_v = ds_v[order]
        ixs_v = ixs_v[order]

        nn1_dists[i] = ds_v[0]
        nn2_dists[i] = ds_v[min(1, len(ds_v) - 1)]
        nn4_dists[i] = ds_v[min(3, len(ds_v) - 1)]
        nn6_dists[i] = np.mean(ds_v[:min(6, len(ds_v))])
        nn12_dists[i] = np.mean(ds_v[:min(12, len(ds_v))])

        d0 = max(ds_v[0], 0.4)
        w_cn = np.exp(1.0 - (ds_v / d0) ** 6)
        w_sum = float(np.sum(w_cn))
        eff_cn[i] = w_sum
        w_norm = w_cn / max(w_sum, 1e-8)

        js = sc_atom_idx[ixs_v]
        d_mean_i = float(np.sum(w_norm * ds_v))
        site_bond_std[i] = math.sqrt(max(float(np.sum(w_norm * ((ds_v - d_mean_i) ** 2))), 0.0)) / max(d_mean_i, 0.5)
        # Ward LocalPropertyDifference across all 21 Magpie properties
        site_loc_diff[i] = np.sum(w_norm[:, None] * np.abs(site_mag[i][None, :] - site_mag[js]), axis=0)

        s_ids = sc_shift_idx[ixs_v]
        u_list.append(np.full(len(ds_v), i, dtype=np.int32))
        v_list.append(js)
        dist_list.append(ds_v)
        shift_vec_list.append(shifts_grid[s_ids])
        vec_list.append(sc_coords[ixs_v] - cart_coords[i])

    if u_list:
        u_arr = np.concatenate(u_list)
        v_arr = np.concatenate(v_list)
        d_arr = np.concatenate(dist_list)
        s_arr = np.vstack(shift_vec_list)
        r_vec = np.vstack(vec_list)
    else:
        u_arr = np.zeros(1, dtype=np.int32)
        v_arr = np.zeros(1, dtype=np.int32)
        d_arr = np.ones(1, dtype=np.float64) * 3.0
        s_arr = np.zeros((1, 3), dtype=np.float64)
        r_vec = np.ones((1, 3), dtype=np.float64)

    # Ward SiteStatsFingerprint summary: mean, std, min, max of site_loc_diff (84 features) + max packing efficiency
    ward_lpd_feats = np.concatenate([
        np.mean(site_loc_diff, axis=0),
        np.std(site_loc_diff, axis=0),
        np.min(site_loc_diff, axis=0),
        np.max(site_loc_diff, axis=0),
    ])
    max_pack_eff = float(np.sum((4.0 * math.pi / 3.0) * ((0.5 * nn1_dists) ** 3)) / vol)
    struct_het_feats = np.array([
        max_pack_eff,
        float(np.mean(site_bond_std)), float(np.std(site_bond_std)), float(np.max(site_bond_std)),
        float(np.std(nn1_dists) / max(float(np.mean(nn1_dists)), 0.5)),
    ], dtype=np.float64)

    r_sum = radii[u_arr] + radii[v_arr]
    rel_d = d_arr / np.maximum(r_sum, 0.5)

    ii = ion_e[u_arr]
    ij = ion_e[v_arr]
    c6_pair = 1.5 * (ii * ij / np.maximum(ii + ij, 1.0)) * polz[u_arr] * polz[v_arr]
    f_damp6 = 1.0 / (1.0 + 6.0 * (np.maximum(d_arr, 0.8) / (1.15 * r_sum)) ** (-12))
    e_disp_pair = (c6_pair / (np.maximum(d_arr, 0.8) ** 6)) * f_damp6
    e_disp8_pair = (c6_pair * r_sum * r_sum / (np.maximum(d_arr, 0.8) ** 8)) * f_damp6
    tot_disp6_pa = float(0.5 * np.sum(e_disp_pair) / n_atoms)
    tot_disp8_pa = float(0.5 * np.sum(e_disp8_pair) / n_atoms)

    alphas = [1.05, 1.12, 1.18, 1.25, 1.32, 1.40, 1.50, 1.65]
    topo_feats = []
    alpha_perc_3d = 2.0
    for alpha in alphas:
        mask_cov = rel_d <= alpha
        if np.any(mask_cov):
            comp_id, comp_dims, n_comps = _periodic_component_ranks(
                n_atoms, u_arr[mask_cov], v_arr[mask_cov], s_arr[mask_cov]
            )
        else:
            comp_id = np.arange(n_atoms, dtype=np.int32)
            comp_dims = np.zeros(n_atoms, dtype=np.int32)
            n_comps = n_atoms

        f_0d = float(np.mean(comp_dims == 0))
        f_1d = float(np.mean(comp_dims == 1))
        f_2d = float(np.mean(comp_dims == 2))
        f_3d = float(np.mean(comp_dims == 3))
        if f_3d > 0.5 and alpha < alpha_perc_3d:
            alpha_perc_3d = alpha

        inter_mask = (~mask_cov) & (comp_id[u_arr] != comp_id[v_arr])
        if not np.any(inter_mask):
            inter_mask = ~mask_cov

        d_inter_min = float(np.min(d_arr[inter_mask])) if np.any(inter_mask) else 6.0
        rel_inter_min = float(np.min(rel_d[inter_mask])) if np.any(inter_mask) else 2.5
        d_intra_mean = float(np.mean(d_arr[mask_cov])) if np.any(mask_cov) else 2.5
        disp6_inter_pa = float(0.5 * np.sum(e_disp_pair[inter_mask]) / n_atoms) if np.any(inter_mask) else 0.0
        disp8_inter_pa = float(0.5 * np.sum(e_disp8_pair[inter_mask]) / n_atoms) if np.any(inter_mask) else 0.0
        sr_inter = inter_mask & (d_arr <= 4.5)
        n_sr_inter_pa = float(np.sum(sr_inter) / n_atoms)
        disp6_sr_inter = float(0.5 * np.sum(e_disp_pair[sr_inter]) / n_atoms) if np.any(sr_inter) else 0.0

        topo_feats.extend([
            f_0d, f_1d, f_2d, f_3d, float(n_comps) / n_atoms,
            d_inter_min, rel_inter_min, d_inter_min / max(d_intra_mean, 0.5),
            disp6_inter_pa, disp8_inter_pa, n_sr_inter_pa, disp6_sr_inter
        ])

    best_m_idx = int(np.argmax(axis_gaps_cart)) if axis_gaps_cart else 2
    cleave_area = float(areas[best_m_idx])
    cleave_h = float(h_perp[best_m_idx])
    normal_vec = np.cross(lat[(best_m_idx + 1) % 3], lat[(best_m_idx + 2) % 3])
    normal_vec = normal_vec / max(float(np.linalg.norm(normal_vec)), 1e-6)
    dz_pair = np.abs(r_vec @ normal_vec)
    across_gap_mask = (dz_pair >= max(0.65 * max_cart_gap, 1.8)) & (rel_d > 1.18)
    disp6_across_gap_pa = float(0.5 * np.sum(e_disp_pair[across_gap_mask]) / n_atoms) if np.any(across_gap_mask) else 0.0
    disp6_across_gap_area = float(0.5 * np.sum(e_disp_pair[across_gap_mask]) / max(cleave_area, 1.0)) if np.any(across_gap_mask) else 0.0
    min_d_across_gap = float(np.min(d_arr[across_gap_mask])) if np.any(across_gap_mask) else 6.0

    # Multipole Tensor Invariants (Dipole, Quadrupole EFG, and 3rd-rank Piezoelectric Tensor)
    r_hat = r_vec / np.maximum(d_arr[:, None], 1e-6)
    d3_inv = 1.0 / (np.maximum(d_arr, 0.6) ** 3)
    d2_inv = 1.0 / (np.maximum(d_arr, 0.6) ** 2)
    dq_pair = enegs[v_arr] - enegs[u_arr]

    # Site dipole vectors & EFG quadrupole tensors
    site_dip_geom = np.zeros((n_atoms, 3), dtype=np.float64)
    site_dip_chg = np.zeros((n_atoms, 3), dtype=np.float64)
    np.add.at(site_dip_geom, u_arr, r_hat * d2_inv[:, None])
    np.add.at(site_dip_chg, u_arr, r_hat * (dq_pair * d2_inv)[:, None])
    dip_geom_norm = np.linalg.norm(site_dip_geom, axis=1)
    dip_chg_norm = np.linalg.norm(site_dip_chg, axis=1)
    net_dip_geom = float(np.linalg.norm(np.mean(site_dip_geom, axis=0)))
    net_dip_chg = float(np.linalg.norm(np.mean(site_dip_chg, axis=0)))

    # 2nd-rank EFG quadrupole tensor per site: sum_j Z_j * (3 r_a r_b - delta_ab) / d^3
    efg_max_evals = np.zeros(n_atoms, dtype=np.float64)
    efg_eta = np.zeros(n_atoms, dtype=np.float64)
    for i in range(n_atoms):
        m_i = (u_arr == i) & (d_arr < 6.5)
        if np.any(m_i):
            rh = r_hat[m_i]
            w_q = zs[v_arr[m_i]] * d3_inv[m_i]
            q_ten = np.einsum("k,ka,kb->ab", w_q, rh, 3.0 * rh) - np.sum(w_q) * np.eye(3)
            ev = np.sort(np.abs(np.linalg.eigvalsh(q_ten)))
            efg_max_evals[i] = ev[2]
            efg_eta[i] = (ev[1] - ev[0]) / max(ev[2], 1e-6)

    # 3rd-rank Piezoelectric Odd-Parity Structure Tensor: P_abc = (1/N) sum_{i,j} (chi_j - chi_i) r_a r_b r_c / d^2
    m_piezo = rel_d <= 1.45
    if np.any(m_piezo):
        rh_p = r_hat[m_piezo]
        w_p = (dq_pair[m_piezo] * d2_inv[m_piezo]) / n_atoms
        p_tensor = np.einsum("k,ka,kb,kc->abc", w_p, rh_p, rh_p, rh_p)
        piezo_frob = float(np.linalg.norm(p_tensor))
        piezo_max = float(np.max(np.abs(p_tensor)))
        # Also unweighted geometric octupole tensor (for elemental non-centrosymmetric crystals)
        w_g = d3_inv[m_piezo] / n_atoms
        g_tensor = np.einsum("k,ka,kb,kc->abc", w_g, rh_p, rh_p, rh_p)
        oct_frob = float(np.linalg.norm(g_tensor))
    else:
        piezo_frob, piezo_max, oct_frob = 0.0, 0.0, 0.0

    multipole_feats = np.array([
        is_centro, inv_rmsd,
        float(np.mean(dip_geom_norm)), float(np.max(dip_geom_norm)), net_dip_geom,
        float(np.mean(dip_chg_norm)), float(np.max(dip_chg_norm)), net_dip_chg,
        float(np.mean(efg_max_evals)), float(np.max(efg_max_evals)), float(np.std(efg_max_evals)),
        float(np.mean(efg_eta)), float(np.max(efg_eta)),
        piezo_frob, piezo_max, oct_frob,
        (1.0 - is_centro) * piezo_frob, (1.0 - is_centro) * net_dip_chg,
    ], dtype=np.float64)

    shell1 = rel_d <= 1.28
    if not np.any(shell1):
        shell1 = d_arr <= (np.min(d_arr) * 1.25 + 0.1)

    u1 = u_arr[shell1]
    v1 = v_arr[shell1]
    d1 = d_arr[shell1]
    rel1 = rel_d[shell1]
    vec1 = r_vec[shell1]

    mu1 = (masses[u1] * masses[v1]) / (masses[u1] + masses[v1])
    inv_sqrt_mu1 = 1.0 / np.sqrt(mu1)
    spring2 = inv_sqrt_mu1 / (d1 ** 2)
    spring3 = inv_sqrt_mu1 / (d1 ** 3)
    mean_spring2 = float(np.sum(spring2) / n_atoms)
    max_spring2 = float(np.max(spring2))
    mean_spring3 = float(np.sum(spring3) / n_atoms)

    d_eneg = np.abs(enegs[u1] - enegs[v1])
    d_rad = np.abs(radii[u1] - radii[v1])
    d_mass_b = np.abs(masses[u1] - masses[v1]) / (masses[u1] + masses[v1])
    d_val_d = np.abs(val_d[u1] - val_d[v1])
    d_val_p = np.abs(val_p[u1] - val_p[v1])
    d_z_b = np.abs(zs[u1] - zs[v1])
    hetero_frac = float(np.mean(zs[u1] != zs[v1]))

    unit_vec1 = vec1 / np.maximum(d1[:, None], 1e-6)
    cos_angles = []
    for i in range(n_atoms):
        m_i = (u1 == i)
        vecs_i = unit_vec1[m_i]
        if 2 <= len(vecs_i) <= 24:
            gram = vecs_i @ vecs_i.T
            iu = np.triu_indices(len(vecs_i), k=1)
            cos_angles.append(gram[iu])
    if cos_angles:
        all_cos = np.clip(np.concatenate(cos_angles), -1.0, 1.0)
        adf_hist, _ = np.histogram(all_cos, bins=24, range=(-1.0, 1.0), density=True)
        cos_mean = float(np.mean(all_cos))
        cos_std = float(np.std(all_cos))
        f_tet = float(np.mean(np.abs(all_cos + 0.3333) < 0.12))
        f_oct = float(np.mean((np.abs(all_cos) < 0.12) | (all_cos < -0.92)))
        f_hex = float(np.mean((np.abs(all_cos + 0.5) < 0.12) | (np.abs(all_cos - 0.5) < 0.12)))
    else:
        adf_hist = np.zeros(24, dtype=np.float64)
        cos_mean, cos_std, f_tet, f_oct, f_hex = 0.0, 0.0, 0.0, 0.0, 0.0

    r_grid = np.linspace(1.0, 7.0, 40)
    dr = r_grid[1] - r_grid[0]
    mask_rdf = d_arr <= 7.2
    d_rdf = d_arr[mask_rdf]
    u_rdf = u_arr[mask_rdf]
    v_rdf = v_arr[mask_rdf]
    if len(d_rdf) > 0:
        gauss = np.exp(-0.5 * ((d_rdf[:, None] - r_grid[None, :]) / 0.15) ** 2)
        shell_norm = 1.0 / (4.0 * math.pi * (r_grid ** 2) * dr * n_atoms * (n_atoms / vol))
        rdf_plain = np.sum(gauss, axis=0) * shell_norm
        w_m_pair = 1.0 / np.sqrt(masses[u_rdf] * masses[v_rdf])
        rdf_mass = np.sum(gauss * w_m_pair[:, None], axis=0) * shell_norm
        w_en_pair = (enegs[u_rdf] - enegs[v_rdf]) ** 2
        rdf_eneg = np.sum(gauss * w_en_pair[:, None], axis=0) * shell_norm
        w_c6_pair = e_disp_pair[mask_rdf]
        rdf_disp = np.sum(gauss * w_c6_pair[:, None], axis=0) / n_atoms
    else:
        rdf_plain = np.zeros(40, dtype=np.float64)
        rdf_mass = np.zeros(40, dtype=np.float64)
        rdf_eneg = np.zeros(40, dtype=np.float64)
        rdf_disp = np.zeros(40, dtype=np.float64)

    if n_atoms <= 64 and len(u1) > 0:
        adj_mat = np.zeros((n_atoms, n_atoms), dtype=np.float64)
        np.add.at(adj_mat, (u1, v1), spring2)
        deg = np.sum(adj_mat, axis=1)
        inv_sqrt_deg = np.where(deg > 1e-8, 1.0 / np.sqrt(np.maximum(deg, 1e-12)), 0.0)
        norm_lap = np.eye(n_atoms) - (inv_sqrt_deg[:, None] * adj_mat * inv_sqrt_deg[None, :])
        evals = np.sort(np.linalg.eigvalsh(norm_lap))
        lap_feats = np.array([
            float(np.mean(evals)), float(np.std(evals)),
            float(evals[1]) if len(evals) > 1 else 0.0,
            float(evals[-1]) if len(evals) > 0 else 0.0,
            float(np.percentile(evals, 25)), float(np.percentile(evals, 50)), float(np.percentile(evals, 75))
        ], dtype=np.float64)
    else:
        lap_feats = np.zeros(7, dtype=np.float64)

    kv_el_arr = np.array([_KV_EL[e] for e in elements], dtype=np.float64)
    gv_el_arr = np.array([_GV_EL[e] for e in elements], dtype=np.float64)
    kv_s = float(np.mean(kv_el_arr)) * (packing_frac / 0.5)
    gv_s = float(np.mean(gv_el_arr)) * (packing_frac / 0.5)
    v_long = math.sqrt(max((kv_s + 1.3333 * gv_s) / max(density, 0.1), 0.01))
    v_trans = math.sqrt(max(gv_s / max(density, 0.1), 0.01))
    q_debye = (6.0 * (math.pi ** 2) / v_pa) ** (1.0 / 3.0)
    theta_debye_proxy = v_trans * q_debye

    struct_summary = np.array([
        float(n_atoms), math.log(n_atoms + 1.0),
        v_pa, log_v_pa, packing_frac, 1.0 - packing_frac, density,
        a_len, b_len, c_len, c_over_a, b_over_a, c_over_b,
        float(np.min(h_perp)), float(np.max(h_perp)), float(np.max(h_perp) / max(np.min(h_perp), 0.1)),
        max_cart_gap, max_rel_gap, max_gap_area_norm,
        alpha_perc_3d, tot_disp6_pa, tot_disp8_pa,
        disp6_across_gap_pa, disp6_across_gap_area, min_d_across_gap,
        cleave_area / n_atoms, cleave_h,
        float(np.mean(nn1_dists)), float(np.std(nn1_dists)), float(np.min(nn1_dists)), float(np.max(nn1_dists)),
        float(np.mean(nn2_dists)), float(np.mean(nn4_dists)), float(np.mean(nn6_dists)), float(np.mean(nn12_dists)),
        float(np.mean(nn2_dists / np.maximum(nn1_dists, 0.3))),
        float(np.mean(nn6_dists / np.maximum(nn1_dists, 0.3))),
        float(np.mean(nn12_dists / np.maximum(nn1_dists, 0.3))),
        float(np.mean(eff_cn)), float(np.std(eff_cn)), float(np.min(eff_cn)), float(np.max(eff_cn)),
        float(np.mean(rel1)), float(np.std(rel1)), float(np.min(rel1)), float(np.max(rel1)),
        mean_spring2, max_spring2, mean_spring3, math.sqrt(max(mean_spring2, 0.0)),
        v_long, v_trans, q_debye, theta_debye_proxy,
        float(np.mean(d_eneg)), float(np.max(d_eneg)),
        float(np.mean(d_rad)), float(np.max(d_rad)),
        float(np.mean(d_mass_b)), float(np.max(d_mass_b)),
        float(np.mean(d_val_d)), float(np.mean(d_val_p)),
        float(np.mean(d_z_b)), hetero_frac,
        cos_mean, cos_std, f_tet, f_oct, f_hex,
    ], dtype=np.float64)

    all_feat = np.concatenate([
        comp_feat,
        ward_lpd_feats,
        struct_het_feats,
        multipole_feats,
        struct_summary,
        np.array(topo_feats, dtype=np.float64),
        adf_hist,
        rdf_plain,
        rdf_mass,
        rdf_eneg,
        rdf_disp,
        lap_feats,
    ])
    return np.nan_to_num(all_feat, nan=0.0, posinf=0.0, neginf=0.0)


_COL_IDX = _SAMPLE_MAG_KEYS.index("Column")
_ROW_IDX = _SAMPLE_MAG_KEYS.index("Row")
_SOFT_IONIC_ELS = {"Li", "Na", "K", "Rb", "Cs", "Ca", "Sr", "Ba", "F", "Cl", "Br", "I", "H"}
_CNO_ELS = {"B", "C", "N", "O"}


def extract_iso_homolog_signature(atoms_dict: dict):
    """
    Scale-free unit-volume-per-atom crystallographic prototype + Periodic Table Group (Column)
    signature for Single-Site Isoelectronic Substitutional Homolog matching.
    """
    from scipy.spatial.distance import cdist
    lat = np.array(atoms_dict["lattice_mat"], dtype=np.float64)
    coords = np.array(atoms_dict["coords"], dtype=np.float64)
    els = list(atoms_dict["elements"])
    cart = bool(atoms_dict.get("cartesian", False))
    n = len(els)
    frac = np.mod(coords @ np.linalg.inv(lat), 1.0) if cart else np.mod(coords, 1.0)
    vol = max(abs(float(np.linalg.det(lat))), 1.0)
    scale = (vol / n) ** (1.0 / 3.0)
    lat_n = lat / scale
    norms = np.sort(np.linalg.norm(lat_n, axis=1))
    cart_n = frac @ lat_n
    shifts = np.array(
        [[i, j, k] for i in (-1, 0, 1) for j in (-1, 0, 1) for k in (-1, 0, 1)],
        dtype=np.float64,
    ) @ lat_n
    all_pts = (cart_n[:, None, :] + shifts[None, :, :]).reshape(-1, 3)
    dmat = np.sort(cdist(cart_n, all_pts), axis=1)[:, 1:9]
    geom_vec = np.concatenate([norms, np.mean(dmat, axis=0), np.std(dmat, axis=0)])
    col_hist = np.zeros(19, dtype=np.float64)
    el_rows = {}
    for e in els:
        m = _get_el_info(e)[1]
        c = int(round(m[_COL_IDX]))
        if 1 <= c <= 18:
            col_hist[c] += 1.0 / n
        el_rows[e] = float(m[_ROW_IDX])
    return n, col_hist, geom_vec, set(els), el_rows


def compute_single_sub_homolog_distance(sigs_a, sigs_b, D_phys: np.ndarray) -> np.ndarray:
    """
    Pairwise distance in the Exact Isoelectronic Crystallographic Homolog manifold:
    finite (< 1.0) iff two crystals have the same unit-cell atom count, identical Periodic Group
    stoichiometry, scale-free crystal geometry within 0.008, and at most a single-element
    substitution across adjacent periodic rows (|dRow| <= 1).
    """
    na = len(sigs_a)
    nb = len(sigs_b)
    D_hom = np.ones((na, nb), dtype=np.float64) * 10.0
    for i, (ni, chi, gi, el_i, er_i) in enumerate(sigs_a):
        for j, (nj, chj, gj, el_j, er_j) in enumerate(sigs_b):
            if ni == nj and np.sum(np.abs(chi - chj)) < 0.01:
                g_dist = float(np.mean(np.abs(gi - gj)))
                if g_dist > 0.008:
                    continue
                diff_i = el_i - el_j
                diff_j = el_j - el_i
                if len(diff_i) <= 1 and len(diff_j) <= 1 and len(el_i & el_j) >= 1:
                    row_jump = 0.0
                    if len(diff_i) == 1 and len(diff_j) == 1:
                        e1 = next(iter(diff_i))
                        e2 = next(iter(diff_j))
                        row_jump = abs(er_i[e1] - er_j[e2])
                    if row_jump <= 1.0:
                        D_hom[i, j] = g_dist + 0.05 * row_jump + 0.25 * float(D_phys[i, j])
    return D_hom


def extract_fracture_regime_vector(atoms_dict: dict, feat_vec: np.ndarray) -> np.ndarray:
    """
    Griffith 3D-Covalent Fracture vs 2D van der Waals Cleavage regime descriptor:
    identifies crystals that are 3D-percolated at alpha <= 1.05 covalent radii with zero
    soft ionic spacer atoms (Alkali / Alkaline-Earth / Halogen).
    """
    els = list(atoms_dict["elements"])
    n = len(els)
    f_soft = sum(1 for e in els if e in _SOFT_IONIC_ELS) / n
    f_cno = sum(1 for e in els if e in _CNO_ELS) / n
    a3d = float(feat_vec[1462])
    is_3d_105 = 1.0 if a3d <= 1.05 else 0.0
    is_3d_112 = 1.0 if a3d <= 1.12 else 0.0
    is_cov_3d = is_3d_105 * (1.0 if f_soft == 0.0 else 0.0)
    is_refractory_3d = is_cov_3d * (1.0 if f_cno > 0.0 and n <= 9 else 0.0)
    return np.array(
        [a3d, f_soft, f_cno, is_3d_105, is_3d_112, is_cov_3d, is_refractory_3d, 1.0 / n],
        dtype=np.float64,
    )


def extract_canonical_adsorbate_slab(atoms_dict: dict) -> np.ndarray:
    """
    Hammer-Norskov Adsorbate-Centered Canonical Slab descriptor for transition-metal nitride
    surface adsorption slabs (tinnet_N_ead): canonically orders metal sites by their layer depth
    and periodic distance to the active *N and *OH adsorbates.
    """
    els = list(atoms_dict["elements"])
    coords = np.array(atoms_dict["coords"], dtype=np.float64)
    lat = np.array(atoms_dict["lattice_mat"], dtype=np.float64)
    a_lat = float(np.linalg.norm(lat[0]))
    n_pos = coords[els.index("N")]
    o_pos = coords[els.index("O")]
    shifts = np.array(
        [[i, j, 0] for i in (-1, 0, 1) for j in (-1, 0, 1)], dtype=np.float64
    ) @ lat
    m_idx = [i for i, e in enumerate(els) if e not in ("N", "O", "H")]
    m_z = sorted(set(np.round(coords[m_idx, 2], 1)), reverse=True)
    m_atoms = []
    for i in m_idx:
        l_rank = int(np.argmin([abs(coords[i, 2] - z0) for z0 in m_z]))
        dn = min(float(np.linalg.norm(coords[i] + sh - n_pos)) for sh in shifts)
        do = min(float(np.linalg.norm(coords[i] + sh - o_pos)) for sh in shifts)
        m_atoms.append((l_rank, round(dn, 2), round(do, 2), els[i], dn, do))
    m_atoms.sort()
    m_dop = m_atoms[0][3]
    m_host = m_atoms[1][3]
    m_sub_n = m_atoms[4][3]
    l2_els = [m_atoms[k][3] for k in range(4, 8)]
    n_pt_l2 = sum(1 for e in l2_els if e == "Pt")
    cfg = 2 if n_pt_l2 == 4 else (0 if m_sub_n == "Pt" else 1)

    def _el_vec(e: str) -> np.ndarray:
        c, m = _get_el_info(e)
        return np.concatenate([c[_FUND_CFID_IDX], m])

    v_dop = _el_vec(m_dop)
    v_host = _el_vec(m_host)
    v_sub = _el_vec(m_sub_n)
    v_l2_mean = np.mean([_el_vec(e) for e in l2_els], axis=0)
    d_vec = np.array(
        [a_lat, float(cfg == 0), float(cfg == 1), float(cfg == 2), float(n_pt_l2)]
        + [x[4] for x in m_atoms[:8]]
        + [x[5] for x in m_atoms[:8]],
        dtype=np.float64,
    )
    return np.concatenate(
        [d_vec, v_dop, v_host, v_sub, v_l2_mean, v_host - v_dop, v_host - v_sub]
    )

