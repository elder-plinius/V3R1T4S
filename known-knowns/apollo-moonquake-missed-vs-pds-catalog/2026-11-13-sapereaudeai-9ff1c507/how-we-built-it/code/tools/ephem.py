"""Low-precision lunar angles (Meeus, Astronomical Algorithms, ch. 47 mean elements; ignores Delta-T).

mean_anomaly_deg(t_ns): Moon's mean anomaly M' (anomalistic phase = M' / 360).
mean_elongation_deg(t_ns): Moon's mean elongation D.
solar_elevation_deg(t_ns, lat, lon): Sun's elevation at a lunar surface site, with the subsolar selenographic
    longitude approximated as 180 - D and subsolar latitude 0 (errors of a few degrees, i.e. a few hours).
"""
import numpy as np

J2000_NS = 946728000 * 1_000_000_000  # 2000-01-01T12:00:00 UTC in ns since 1970


def _T(t_ns):
    return (np.asarray(t_ns, dtype=np.float64) - J2000_NS) / 1e9 / 86400.0 / 36525.0


def mean_anomaly_deg(t_ns):
    T = _T(t_ns)
    return np.mod(134.9633964 + 477198.8675055 * T + 0.0087414 * T * T + T ** 3 / 69699.0, 360.0)


def mean_elongation_deg(t_ns):
    T = _T(t_ns)
    return np.mod(297.8501921 + 445267.1114034 * T - 0.0018819 * T * T + T ** 3 / 545868.0, 360.0)


def solar_elevation_deg(t_ns, lat, lon):
    lam_s = 180.0 - mean_elongation_deg(t_ns)
    la = np.radians(lat)
    return np.degrees(np.arcsin(np.cos(la) * np.cos(np.radians(lon - lam_s))))


# station coordinates from the PDS StationXML data/pse/stationxml.xa.0.sxml (fetched 2026-11-12T19:04:26Z)
STATIONS = {'s12': (-3.01084, -23.42456), 's14': (-3.6445, -17.47753), 's15': (26.13407, 3.62981),
            's16': (-8.97577, 15.49649)}
