"""Cap scipy.fft worker threads for scripts run next to other jobs (results are unchanged; only threads).
Import before the other tools. Cap from the environment variable V3_WORKERS (default 2)."""
import os
import scipy.fft as _f

CAP = int(os.environ.get('V3_WORKERS', '2'))
for _name in ('rfft', 'irfft', 'fft', 'ifft'):
    _orig = getattr(_f, _name)

    def _wrap(*a, _o=_orig, **k):
        if 'workers' in k and k['workers'] is not None:
            k['workers'] = min(int(k['workers']), CAP)
        else:
            k['workers'] = CAP
        return _o(*a, **k)
    setattr(_f, _name, _wrap)
