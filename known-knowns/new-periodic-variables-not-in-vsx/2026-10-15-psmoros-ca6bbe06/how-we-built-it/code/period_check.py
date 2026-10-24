"""Period-side checks for new-periodic-variables-not-in-vsx, criterion items (4) and (5).

agree(p1, p2)            periods agree within 0.1%, or one is exactly 2x the other within 0.1%
day_alias(p, space)      within 1% of n/k day (solar or sidereal day, n = 1..10, k = 1..4); waived if space-based
bootstrap_fap(t, y, dy, p_grid_min, p_grid_max, n_boot, seed)
                         peak Lomb-Scargle power of the real series vs the max peak of n_boot copies with the
                         magnitudes shuffled over the same times; FAP = (1 + #boot >= real) / (1 + n_boot)
amplitude_ok(y, scatter_at_mag)  peak-to-peak (5-95 percentile) amplitude > 5 x median scatter at that magnitude

Run as a script for self-tests: venv/bin/python -I code/period_check.py
"""
import numpy as np

SOLAR, SIDEREAL = 1.0, 0.99726958


def agree(p1, p2, tol=1e-3):
    for a, b in ((p1, p2), (2 * p1, p2), (p1, 2 * p2)):
        if abs(a - b) / b <= tol:
            return True
    return False


def day_alias(p, space=False, tol=0.01):
    if space:
        return False
    for day in (SOLAR, SIDEREAL):
        for n in range(1, 11):
            for k in range(1, 5):
                a = n * day / k
                if abs(p - a) / a <= tol:
                    return True
    return False


def ls_peak(t, y, dy, fmin, fmax, n=None):
    from astropy.timeseries import LombScargle
    ls = LombScargle(t, y, dy)
    if n is None:
        span = t.max() - t.min()
        n = int(min(2_000_000, max(10_000, 5 * span * (fmax - fmin))))
    f = np.linspace(fmin, fmax, n)
    pw = ls.power(f)
    i = int(np.argmax(pw))
    return 1 / f[i], pw[i], f, pw


def bootstrap_fap(t, y, dy, pmin, pmax, n_boot=10000, seed=0, nfreq=None):
    """Exact-resolution bootstrap is expensive; callers may pass a coarser nfreq for the boot copies only
    if they also report it. FAP < 1e-4 needs n_boot >= 10000 (FAP floor = 1/(1+n_boot))."""
    rng = np.random.default_rng(seed)
    p, pw, f, _ = ls_peak(t, y, dy, 1 / pmax, 1 / pmin, nfreq)
    from astropy.timeseries import LombScargle
    hits = 0
    for _ in range(n_boot):
        idx = rng.permutation(len(y))
        bp = LombScargle(t, y[idx], dy[idx]).power(f).max()
        hits += bp >= pw
    return p, pw, (1 + hits) / (1 + n_boot)


def amplitude_ok(y, scatter_at_mag, factor=5.0):
    amp = np.percentile(y, 95) - np.percentile(y, 5)
    return amp > factor * scatter_at_mag, amp


if __name__ == "__main__":
    assert agree(0.5, 0.5004) and not agree(0.5, 0.5006)
    assert agree(0.25, 0.5) and agree(1.0, 0.5) and not agree(0.33, 0.5)
    assert day_alias(0.5) and day_alias(0.9973) and day_alias(1.0 / 3 * 1.005) and not day_alias(0.3127)
    assert not day_alias(0.5, space=True)
    # planted positive: 0.3127 d sinusoid, 300 epochs over 900 d, noise 0.02 mag, amplitude 0.3 mag
    rng = np.random.default_rng(1)
    t = np.sort(rng.uniform(0, 900, 300)); dy = np.full(300, 0.02)
    y = 0.15 * np.sin(2 * np.pi * t / 0.3127) + rng.normal(0, 0.02, 300)
    p, pw, fap = bootstrap_fap(t, y, dy, 0.1, 10, n_boot=200, nfreq=200000)
    assert abs(p - 0.3127) / 0.3127 < 1e-4 and fap <= 1 / 201 + 1e-12, (p, fap)
    # planted negative: pure noise
    y0 = rng.normal(0, 0.02, 300)
    p0, pw0, fap0 = bootstrap_fap(t, y0, dy, 0.1, 10, n_boot=200, nfreq=200000)
    assert fap0 > 0.01, fap0
    print("period_check self-test PASS", round(p, 6), fap, round(p0, 4), fap0)
