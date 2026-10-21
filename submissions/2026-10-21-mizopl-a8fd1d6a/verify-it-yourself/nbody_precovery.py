import struct
import math
import json
import os
import urllib.request
import urllib.parse
import numpy as np
from scipy.integrate import solve_ivp

AU_KM = 149597870.700
DAY_SEC = 86400.0
C_AU_DAY = 299792.458 * DAY_SEC / AU_KM  # 173.14463267424034 AU/day
K_GAUSS = 0.01720209895
GM_SUN = K_GAUSS ** 2
GM_BODIES = {
    10: GM_SUN,
    1: GM_SUN / 6023600.0,
    2: GM_SUN / 408523.71,
    399: GM_SUN / 332946.050895,
    301: GM_SUN / 27068700.387534,
    4: GM_SUN / 3098708.0,
    5: GM_SUN / 1047.3486,
    6: GM_SUN / 3497.898,
    7: GM_SUN / 22902.98,
    8: GM_SUN / 19412.24,
    9: GM_SUN / 135200000.0,
}

# Ecliptic J2000 (IAU 1976 / JPL obliquity eps = 84381.448 arcsec) to ICRS equatorial
EPS_J2000 = math.radians(84381.448 / 3600.0)
COS_E, SIN_E = math.cos(EPS_J2000), math.sin(EPS_J2000)
R_ECL_TO_EQ = np.array([
    [1.0, 0.0, 0.0],
    [0.0, COS_E, -SIN_E],
    [0.0, SIN_E,  COS_E],
])

# Standard MPC Observatory Coordinates: code -> (lon_deg_east, rho_cos_phi, rho_sin_phi) in Earth radii (R_EARTH = 6378.137 km)
R_EARTH_AU = 6378.137 / AU_KM
MPC_OBS_COORDS = {
    "500": (0.0, 0.0, 0.0),
    "I41": (243.14107, 0.835267, 0.547281),  # ZTF, Palomar Mountain
    "675": (243.1350,  0.83529,  0.54725),   # Palomar Mountain
    "F51": (203.74241, 0.935568, 0.351853),  # Pan-STARRS 1, Haleakala
    "F52": (203.74245, 0.935569, 0.351852),  # Pan-STARRS 2, Haleakala
    "G96": (249.20832, 0.844260, 0.533560),  # Mt. Lemmon Survey
    "703": (249.26736, 0.844572, 0.533060),  # Catalina Sky Survey
    "G83": (249.21114, 0.844269, 0.533548),  # Mt. Graham-LBT
    "691": (248.40042, 0.848715, 0.526699),  # Steward Observatory, Kitt Peak-Spacewatch
    "291": (248.3996,  0.84872,  0.52670),   # LPL/Spacewatch II
    "T05": (203.7420,  0.93557,  0.35185),   # ATLAS-HKO, Haleakala
    "T08": (204.4239,  0.94228,  0.33339),   # ATLAS-MLO, Mauna Loa
    "M22": (149.0644,  0.85513, -0.51598),   # ATLAS South Africa / Siding Spring
    "W68": (289.2353,  0.86416, -0.50085),   # ATLAS Chile, Rio Hurtado
    "W84": (289.1936,  0.86480, -0.49975),   # Cerro Tololo-DECam
    "807": (289.1941,  0.86479, -0.49976),   # Cerro Tololo Observatory, La Serena
    "H01": (252.8112,  0.83961,  0.54079),   # Magdalena Ridge Observatory
    "568": (204.5278,  0.94106,  0.33682),   # Mauna Kea
    "T12": (204.5278,  0.94106,  0.33682),   # University of Hawaii 88-inch, Mauna Kea
    "T14": (204.5313,  0.94106,  0.33682),   # CFHT, Mauna Kea
}


def build_compact_de421_npz(bsp_path, npz_path, jd_start=2454832.5, jd_end=2461500.5):
    """Extract 2009-2027 Chebyshev records from de421.bsp into a ~900 KB .npz file."""
    with open(bsp_path, "rb") as f:
        raw = f.read()
    arr_all = np.frombuffer(raw, dtype="<f8")
    fward = struct.unpack("<i", raw[76:80])[0]
    rec = raw[(fward - 1)*1024 : fward*1024]
    nsum = int(struct.unpack("<d", rec[16:24])[0])
    arr_sum = np.frombuffer(rec[24:], dtype="<f8")

    t_min = (jd_start - 2451545.0) * DAY_SEC
    t_max = (jd_end - 2451545.0) * DAY_SEC

    out = {}
    for i in range(nsum):
        s_int = np.frombuffer(arr_sum[i*5 + 2 : (i+1)*5].tobytes(), dtype="<i4")
        target, center, frame, spk_type, start_addr, end_addr = s_int[:6]
        if (target, center) not in [(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(9,0),(10,0),(301,3),(399,3)]:
            continue
        init_sec, intlen, rsize, nrec = arr_all[end_addr - 4 : end_addr]
        rsize, nrec = int(rsize), int(nrec)
        records = arr_all[start_addr - 1 : start_addr - 1 + nrec * rsize].reshape((nrec, rsize))
        i0 = max(0, int((t_min - init_sec) // intlen) - 1)
        i1 = min(nrec, int((t_max - init_sec) // intlen) + 2)
        sub_recs = records[i0:i1].copy()
        new_init = init_sec + i0 * intlen
        key = f"seg_{target}_{center}"
        out[f"{key}_meta"] = np.array([new_init, intlen, float(rsize), float(len(sub_recs))], dtype=np.float64)
        out[f"{key}_recs"] = sub_recs
    np.savez_compressed(npz_path, **out)
    return os.path.getsize(npz_path)


class DE421Loader:
    def __init__(self, npz_path):
        data = np.load(npz_path)
        self.segs = {}
        for t, c in [(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(9,0),(10,0),(301,3),(399,3)]:
            key = f"seg_{t}_{c}"
            meta = data[f"{key}_meta"]
            recs = data[f"{key}_recs"]
            init_sec, intlen, rsize, nrec = meta[0], meta[1], int(meta[2]), int(meta[3])
            ncoeff = (rsize - 2) // 3
            self.segs[(t, c)] = (init_sec, intlen, ncoeff, recs)

    def eval_pos(self, tc, jd_tdb):
        init_sec, intlen, ncoeff, records = self.segs[tc]
        t_sec = (jd_tdb - 2451545.0) * DAY_SEC
        idx = int((t_sec - init_sec) // intlen)
        idx = max(0, min(len(records) - 1, idx))
        r = records[idx]
        x = (t_sec - r[0]) / r[1]
        T = np.empty(ncoeff)
        T[0] = 1.0
        if ncoeff > 1:
            T[1] = x
        for k in range(2, ncoeff):
            T[k] = 2.0 * x * T[k-1] - T[k-2]
        coeffs = r[2:].reshape((3, ncoeff))
        return (coeffs @ T) / AU_KM

    def eval_pos_vel(self, tc, jd_tdb):
        init_sec, intlen, ncoeff, records = self.segs[tc]
        t_sec = (jd_tdb - 2451545.0) * DAY_SEC
        idx = int((t_sec - init_sec) // intlen)
        idx = max(0, min(len(records) - 1, idx))
        r = records[idx]
        x = (t_sec - r[0]) / r[1]
        T = np.empty(ncoeff)
        dT = np.zeros(ncoeff)
        T[0] = 1.0
        if ncoeff > 1:
            T[1] = x
            dT[1] = 1.0
        for k in range(2, ncoeff):
            T[k] = 2.0 * x * T[k-1] - T[k-2]
            dT[k] = 2.0 * T[k-1] + 2.0 * x * dT[k-1] - dT[k-2]
        coeffs = r[2:].reshape((3, ncoeff))
        pos = (coeffs @ T) / AU_KM
        vel = (coeffs @ dT) * (DAY_SEC / r[1]) / AU_KM
        return pos, vel

    def get_bary_bodies(self, jd_tdb):
        pos = {}
        for t in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
            pos[t] = self.eval_pos((t, 0), jd_tdb)
        pos[301] = pos[3] + self.eval_pos((301, 3), jd_tdb)
        pos[399] = pos[3] + self.eval_pos((399, 3), jd_tdb)
        return pos


def obs_topocentric_offset_au(jd_utc, obs_code):
    """Geocentric vector of observatory in ICRS equatorial coordinates (AU)."""
    lon_deg, r_cos_phi, r_sin_phi = MPC_OBS_COORDS.get(obs_code, (0.0, 0.0, 0.0))
    if r_cos_phi == 0.0 and r_sin_phi == 0.0:
        return np.zeros(3)
    # Earth rotation angle (ERA / GMST)
    du = jd_utc - 2451545.0
    theta = 2.0 * math.pi * (0.7790572732640 + 1.00273781191135448 * du) + math.radians(lon_deg)
    return R_EARTH_AU * np.array([
        r_cos_phi * math.cos(theta),
        r_cos_phi * math.sin(theta),
        r_sin_phi
    ])


def elements_to_bary_state(eph, el_vec, epoch_tdb):
    """Convert [e, q, tp, om_deg, w_deg, i_deg] at epoch_tdb to 6D barycentric ICRS state (AU, AU/d)."""
    e, q, tp, om_deg, w_deg, i_deg = el_vec
    a = q / (1.0 - e)
    n = K_GAUSS / (a ** 1.5)
    M = n * (epoch_tdb - tp)
    E = M
    for _ in range(15):
        f = E - e * math.sin(E) - M
        E -= f / (1.0 - e * math.cos(E))
    cosE, sinE = math.cos(E), math.sin(E)
    sqrt1me2 = math.sqrt(max(0.0, 1.0 - e * e))
    x_orb = a * (cosE - e)
    y_orb = a * sqrt1me2 * sinE
    edot = n / (1.0 - e * cosE)
    vx_orb = -a * sinE * edot
    vy_orb = a * sqrt1me2 * cosE * edot
    om, w, inc = math.radians(om_deg), math.radians(w_deg), math.radians(i_deg)
    co, so = math.cos(om), math.sin(om)
    cw, sw = math.cos(w), math.sin(w)
    ci, si = math.cos(inc), math.sin(inc)
    P = np.array([co*cw - so*sw*ci, so*cw + co*sw*ci, sw*si])
    Q = np.array([-co*sw - so*cw*ci, -so*sw + co*cw*ci, cw*si])
    r_helio_eq = R_ECL_TO_EQ @ (x_orb * P + y_orb * Q)
    v_helio_eq = R_ECL_TO_EQ @ (vx_orb * P + vy_orb * Q)
    sun_pos, sun_vel = eph.eval_pos_vel((10, 0), epoch_tdb)
    return np.concatenate([sun_pos + r_helio_eq, sun_vel + v_helio_eq])


def make_nbody_rhs(eph):
    def rhs(t, y):
        r = y[:3]
        v = y[3:6]
        pos = eph.get_bary_bodies(t)
        acc = np.zeros(3)
        for b, gm in GM_BODIES.items():
            d = pos[b] - r
            dist2 = float(np.dot(d, d))
            dist = math.sqrt(dist2)
            acc += gm * d / (dist2 * dist)
        d_sun = r - pos[10]
        r_s = float(np.linalg.norm(d_sun))
        v2 = float(np.dot(v, v))
        rv = float(np.dot(d_sun, v))
        acc += (GM_SUN / (C_AU_DAY**2 * r_s**3)) * ((4.0 * GM_SUN / r_s - v2) * d_sun + 4.0 * rv * v)
        return np.concatenate([v, acc])
    return rhs


def hg_apparent_mag(H, G, r_sun_au, delta_au, phase_rad):
    """Standard IAU (H, G) Bowell phase function apparent magnitude V."""
    tan_half = math.tan(0.5 * phase_rad)
    phi1 = math.exp(-3.33 * (tan_half ** 0.63))
    phi2 = math.exp(-1.87 * (tan_half ** 1.22))
    return H + 5.0 * math.log10(max(1e-9, r_sun_au * delta_au)) - 2.5 * math.log10(max(1e-9, (1.0 - G) * phi1 + G * phi2))


def integrate_trajectory(eph, el_vec, epoch_tdb, t_min_tdb, t_max_tdb):
    """Integrate forward and backward from epoch_tdb to cover [t_min_tdb, t_max_tdb] with dense_output=True."""
    y0 = elements_to_bary_state(eph, el_vec, epoch_tdb)
    rhs = make_nbody_rhs(eph)
    sol_bwd = None
    sol_fwd = None
    if t_min_tdb < epoch_tdb:
        sol_bwd = solve_ivp(rhs, (epoch_tdb, t_min_tdb - 0.5), y0, method="DOP853", rtol=1e-11, atol=1e-13, dense_output=True)
    if t_max_tdb > epoch_tdb:
        sol_fwd = solve_ivp(rhs, (epoch_tdb, t_max_tdb + 0.5), y0, method="DOP853", rtol=1e-11, atol=1e-13, dense_output=True)

    def eval_state(t_tdb):
        if abs(t_tdb - epoch_tdb) < 1e-12:
            return y0
        elif t_tdb < epoch_tdb:
            return sol_bwd.sol(t_tdb)
        else:
            return sol_fwd.sol(t_tdb)
    return eval_state


def predict_astrometry_from_sol(eph, eval_state, jd_utc, obs_code="I41", H=18.0, G=0.15):
    """Compute light-time corrected astrometric RA, Dec (deg), rate (arcsec/hr), and V mag."""
    jd_tdb = jd_utc + 0.00080074
    bodies = eph.get_bary_bodies(jd_tdb)
    obs_bary = bodies[399] + obs_topocentric_offset_au(jd_utc, obs_code)
    # 2-step light-time iteration
    tau = 0.0
    for _ in range(3):
        st = eval_state(jd_tdb - tau)
        rho_vec = st[:3] - obs_bary
        delta = float(np.linalg.norm(rho_vec))
        tau = delta / C_AU_DAY
    st_emit = eval_state(jd_tdb - tau)
    rho_vec = st_emit[:3] - obs_bary
    delta = float(np.linalg.norm(rho_vec))
    ra_rad = math.atan2(rho_vec[1], rho_vec[0]) % (2.0 * math.pi)
    dec_rad = math.asin(np.clip(rho_vec[2] / delta, -1.0, 1.0))

    # Sun-asteroid distance and phase angle at emission time
    sun_emit = eph.eval_pos((10, 0), jd_tdb - tau)
    r_helio = st_emit[:3] - sun_emit
    r_sun = float(np.linalg.norm(r_helio))
    cos_phase = float(np.dot(r_helio, rho_vec)) / max(1e-12, r_sun * delta)
    phase_rad = math.acos(np.clip(cos_phase, -1.0, 1.0))
    vmag = hg_apparent_mag(H, G, r_sun, delta, phase_rad)
    return math.degrees(ra_rad), math.degrees(dec_rad), delta, r_sun, vmag


def propagate_with_covariance(eph, el_vec, cov_mat, epoch_tdb, target_list, H=18.0, G=0.15):
    """
    target_list: list of (jd_utc, obs_code)
    Returns list of dicts with predicted ra, dec, rate_ra_arcsec_hr, rate_dec_arcsec_hr,
    vmag, cov_radec_arcsec2 (2x2), sigma_ra_arcsec, sigma_dec_arcsec, ell3sigma_major_arcsec, ell3sigma_minor_arcsec, ell_pa_deg, jacobian.
    """
    jds_tdb = [jd + 0.00080074 for jd, _ in target_list]
    t_min = min(jds_tdb) - 0.1
    t_max = max(jds_tdb) + 0.1
    nom_sol = integrate_trajectory(eph, el_vec, epoch_tdb, t_min, t_max)

    # Step sizes for finite-difference Jacobian d(RA*cosDec, Dec)/d(e, q, tp, om, w, i)
    steps = np.array([1e-6, 1e-6, 1e-4, 1e-4, 1e-4, 1e-4])
    pert_sols = []
    for k in range(6):
        el_p = el_vec.copy()
        el_p[k] += steps[k]
        pert_sols.append(integrate_trajectory(eph, el_p, epoch_tdb, t_min, t_max))

    results = []
    dt_rate = 1.0 / 24.0  # 1 hour in days
    for jd_utc, obs_code in target_list:
        ra0, dec0, delta, r_sun, vmag = predict_astrometry_from_sol(eph, nom_sol, jd_utc, obs_code, H, G)
        ra_p1h, dec_p1h, _, _, _ = predict_astrometry_from_sol(eph, nom_sol, jd_utc + 0.5 * dt_rate, obs_code, H, G)
        ra_m1h, dec_m1h, _, _, _ = predict_astrometry_from_sol(eph, nom_sol, jd_utc - 0.5 * dt_rate, obs_code, H, G)
        cos_dec = math.cos(math.radians(dec0))
        dra_hr = ((ra_p1h - ra_m1h + 180.0) % 360.0 - 180.0) * cos_dec * 3600.0
        ddec_hr = (dec_p1h - dec_m1h) * 3600.0

        J = np.zeros((2, 6))
        for k in range(6):
            rak, deck, _, _, _ = predict_astrometry_from_sol(eph, pert_sols[k], jd_utc, obs_code, H, G)
            dra = ((rak - ra0 + 180.0) % 360.0 - 180.0) * cos_dec * 3600.0
            ddec = (deck - dec0) * 3600.0
            J[0, k] = dra / steps[k]
            J[1, k] = ddec / steps[k]

        cov_sky = J @ cov_mat @ J.T
        eigvals, eigvecs = np.linalg.eigh(cov_sky)
        eigvals = np.maximum(eigvals, 0.0)
        # Largest eigenvalue is index 1
        sig_maj = math.sqrt(float(eigvals[1]))
        sig_min = math.sqrt(float(eigvals[0]))
        vx, vy = float(eigvecs[0, 1]), float(eigvecs[1, 1])  # vx = East (RA*cosDec), vy = North (Dec)
        pa_deg = (math.degrees(math.atan2(vx, vy)) + 180.0) % 180.0

        results.append({
            "jd_utc": jd_utc,
            "obs_code": obs_code,
            "ra_deg": ra0,
            "dec_deg": dec0,
            "delta_au": delta,
            "r_sun_au": r_sun,
            "vmag": vmag,
            "rate_ra_cosdec_arcsec_hr": dra_hr,
            "rate_dec_arcsec_hr": ddec_hr,
            "rate_total_arcsec_hr": math.hypot(dra_hr, ddec_hr),
            "rate_pa_deg": (math.degrees(math.atan2(dra_hr, ddec_hr)) + 360.0) % 360.0,
            "cov_sky_arcsec2": cov_sky.tolist(),
            "sigma_ra_cosdec_arcsec": math.sqrt(max(0.0, float(cov_sky[0, 0]))),
            "sigma_dec_arcsec": math.sqrt(max(0.0, float(cov_sky[1, 1]))),
            "sigma_major_arcsec": sig_maj,
            "sigma_minor_arcsec": sig_min,
            "ell3sigma_major_arcsec": 3.0 * sig_maj,
            "ell3sigma_minor_arcsec": 3.0 * sig_min,
            "ell_pa_deg": pa_deg,
            "jacobian": J.tolist(),
        })
    return results


def parse_obs80_line(line):
    """Parse an 80-column MPC optical observation line into (jd_utc, ra_deg, dec_deg, mag, band, obs_code)."""
    if len(line) < 80:
        return None
    note2 = line[14]
    if note2 in ("s", "v", "R", "Q", "x", "X"):
        return None  # satellite/radar/roving second line
    try:
        date_str = line[15:32].strip()
        parts = date_str.split()
        if len(parts) != 3:
            return None
        year, month, day_frac = int(parts[0]), int(parts[1]), float(parts[2])
        # Convert calendar date (year, month, day_frac) to JD
        y, m = year, month
        if m <= 2:
            y -= 1
            m += 12
        A = y // 100
        B = 2 - A + (A // 4)
        jd_utc = int(365.25 * (y + 4716)) + int(30.6001 * (m + 1)) + day_frac + B - 1524.5

        ra_str = line[32:44].strip().split()
        ra_deg = (float(ra_str[0]) + float(ra_str[1]) / 60.0 + float(ra_str[2]) / 3600.0) * 15.0

        dec_raw = line[44:56].strip()
        sign = -1.0 if dec_raw.startswith("-") else 1.0
        dec_parts = dec_raw.lstrip("+-").split()
        dec_deg = sign * (float(dec_parts[0]) + float(dec_parts[1]) / 60.0 + float(dec_parts[2]) / 3600.0)

        mag_str = line[65:70].strip()
        mag = float(mag_str) if mag_str else None
        band = line[70].strip()
        obs_code = line[77:80].strip()
        return {
            "jd_utc": jd_utc,
            "date_str": date_str,
            "ra_deg": ra_deg,
            "dec_deg": dec_deg,
            "mag": mag,
            "band": band,
            "obs_code": obs_code,
            "raw_line": line,
        }
    except Exception:
        return None


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    bsp = os.path.join(here, "de421.bsp")
    npz = os.path.join(here, "de421_2009_2027.npz")
    if not os.path.exists(npz) and os.path.exists(bsp):
        sz = build_compact_de421_npz(bsp, npz)
        print(f"Created {npz} ({sz} bytes)")
    if os.path.exists(npz):
        eph = DE421Loader(npz)
        print("DE421Loader ready.")
