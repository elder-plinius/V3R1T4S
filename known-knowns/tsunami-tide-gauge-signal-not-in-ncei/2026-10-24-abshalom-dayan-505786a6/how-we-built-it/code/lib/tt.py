"""Travel-time model of this run (frozen in PREREG.md before any gauge series is scored).

ETOPO1 Ice, grid-registered, 2 arcmin (NCEI THREDDS, stride 2) -> azimuthal-equidistant grid centred on the source
(dx 3.7 km) -> second-order fast marching (scikit-fmm) with speed sqrt(g * max(h, 1 m)) on water cells (z < 0).
Gauges are snapped to the nearest water cell with depth >= dmin within 30 km.
"""
import os, glob, math
import numpy as np
import skfmm

RUN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BATHY = os.path.join(RUN, 'data', 'bathy')
NPY = os.path.join(BATHY, 'etopo1_2min_int16.npy')
RE = 6371.0
G = 9.81
_Z = None


def build_npy():
    """Parse the six OPeNDAP .dods slabs (rows 0..10800 step 2, cols 0..21600 step 2) into one int16 array."""
    parts = []
    for s in (0, 1800, 3600, 5400, 7200, 9000):
        b = open(os.path.join(BATHY, f'etopo1_s2_rows{s}.dods'), 'rb').read()
        i = b.index(b'\nData:\n') + 7
        n = int.from_bytes(b[i:i + 4], 'big')
        a = np.frombuffer(b, dtype='>f4', count=n, offset=i + 8)
        nr = 901 if s == 9000 else 900
        parts.append(a.reshape(nr, 10801))
    z = np.vstack(parts)
    assert z.shape == (5401, 10801), z.shape
    np.save(NPY, np.round(z).astype(np.int16))


def grid():
    """int16 altitude (m), shape (5401, 10801): row i = lat -90 + i/30, col j = lon -180 + j/30."""
    global _Z
    if _Z is None:
        if not os.path.exists(NPY):
            build_npy()
        _Z = np.load(NPY, mmap_mode='r')
    return _Z


def alt_at(lat, lon):
    z = grid()
    i = np.clip(np.rint((np.asarray(lat) + 90.0) * 30).astype(int), 0, 5400)
    j = np.rint(((np.asarray(lon) + 180.0) % 360.0) * 30).astype(int) % 10800
    return z[i, j]


def gc_km(la1, lo1, la2, lo2):
    la1, lo1, la2, lo2 = map(np.radians, (la1, lo1, la2, lo2))
    a = np.sin((la2 - la1) / 2) ** 2 + np.cos(la1) * np.cos(la2) * np.sin((lo2 - lo1) / 2) ** 2
    return RE * 2 * np.arcsin(np.sqrt(np.clip(a, 0, 1)))


def aeqd_fwd(lat0, lon0, lat, lon):
    """Spherical azimuthal-equidistant forward projection (km)."""
    p0, l0 = math.radians(lat0), math.radians(lon0)
    p, l = np.radians(lat), np.radians(lon)
    c = gc_km(lat0, lon0, lat, lon) / RE
    az = np.arctan2(np.sin(l - l0) * np.cos(p), math.cos(p0) * np.sin(p) - math.sin(p0) * np.cos(p) * np.cos(l - l0))
    return RE * c * np.sin(az), RE * c * np.cos(az)


def aeqd_inv(lat0, lon0, x, y):
    p0, l0 = math.radians(lat0), math.radians(lon0)
    rho = np.hypot(x, y)
    c = rho / RE
    with np.errstate(invalid='ignore', divide='ignore'):
        lat = np.arcsin(np.clip(np.cos(c) * math.sin(p0) + np.where(rho > 0, y * np.sin(c) * math.cos(p0) / rho, 0), -1, 1))
        lon = l0 + np.arctan2(x * np.sin(c), rho * math.cos(p0) * np.cos(c) - y * math.sin(p0) * np.sin(c))
    return np.degrees(lat), (np.degrees(lon) + 180.0) % 360.0 - 180.0


class FMM:
    """First-arrival travel times (minutes) from a point source over an AEQD grid of half-width radius_km."""

    def __init__(self, lat0, lon0, radius_km=1700.0, dx=3.7, flat_depth=None, src_snap_km=50.0):
        self.lat0, self.lon0, self.dx = lat0, lon0, dx
        n = int(math.ceil(radius_km / dx))
        ax = np.arange(-n, n + 1) * dx
        self.ax = ax
        X, Y = np.meshgrid(ax, ax)  # rows = y, cols = x
        LA, LO = aeqd_inv(lat0, lon0, X, Y)
        if flat_depth is not None:
            h = np.full(X.shape, float(flat_depth))
        else:
            h = -alt_at(LA, LO).astype(float)
        del LA, LO
        self.h = h
        self.water = h > 0
        c = np.ma.MaskedArray(np.sqrt(G * np.maximum(h, 1.0)) * 60.0 / 1000.0, mask=~self.water)  # km/min
        ic = n  # centre index
        si, sj = ic, ic
        self.src_snap_km = 0.0
        if not self.water[ic, ic]:
            d = np.hypot(X, Y)
            d[~self.water] = np.inf
            k = np.unravel_index(np.argmin(d), d.shape)
            if not d[k] <= src_snap_km:
                raise RuntimeError('source not within %.0f km of water' % src_snap_km)
            si, sj = k
            self.src_snap_km = float(d[k])
        dist0 = np.hypot(X - ax[sj], Y - ax[si])
        T = None
        for r0 in (0.5, 1.5, 2.5):  # an isolated water cell has no zero contour at 0.5 dx; widen the start circle
            try:
                T = skfmm.travel_time(np.ma.MaskedArray(dist0 - r0 * dx, mask=~self.water), c, dx=dx, order=2)
                break
            except ValueError:
                continue
        if T is None:
            raise RuntimeError('no zero contour around the source')
        self.r0 = r0
        self.T = T.filled(np.nan) if np.ma.isMaskedArray(T) else np.asarray(T, dtype=float)
        self.T[~self.water] = np.nan
        # inside the initial circle travel_time returns negative values; clamp to 0
        self.T = np.where(self.T < 0, 0.0, self.T)
        self.n = n

    def eta(self, lat, lon, dmin=20.0, max_km=30.0):
        """(minutes, snap distance km, snapped depth m) at the nearest water cell with depth >= dmin within max_km."""
        x, y = aeqd_fwd(self.lat0, self.lon0, lat, lon)
        j0 = int(round(x / self.dx)) + self.n
        i0 = int(round(y / self.dx)) + self.n
        w = int(math.ceil(max_km / self.dx)) + 1
        a0, a1 = max(0, i0 - w), min(2 * self.n + 1, i0 + w + 1)
        b0, b1 = max(0, j0 - w), min(2 * self.n + 1, j0 + w + 1)
        if a0 >= a1 or b0 >= b1:
            return np.nan, np.nan, np.nan
        yy = self.ax[a0:a1][:, None]; xx = self.ax[b0:b1][None, :]
        d = np.hypot(xx - x, yy - y)
        ok = (self.h[a0:a1, b0:b1] >= dmin) & np.isfinite(self.T[a0:a1, b0:b1])
        d = np.where(ok, d, np.inf)
        if not np.isfinite(d).any():
            return np.nan, np.nan, np.nan
        k = np.unravel_index(np.argmin(d), d.shape)
        if d[k] > max_km:
            return np.nan, np.nan, np.nan
        return float(self.T[a0 + k[0], b0 + k[1]]), float(d[k]), float(self.h[a0 + k[0], b0 + k[1]])
