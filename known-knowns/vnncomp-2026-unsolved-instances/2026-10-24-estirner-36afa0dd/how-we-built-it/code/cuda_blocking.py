"""Import this before torch or cupy touches the GPU: sets cudaDeviceScheduleBlockingSync (flag 4) on the CUDA
runtime that torch will use, so the host thread sleeps instead of spin-waiting while the GPU works.
Finds libcudart from the pip package nvidia-cuda-runtime (as torch wheels ship it), else from the system,
else from the environment variable CUDART_PATH."""
import ctypes, ctypes.util, glob, importlib.util, os


def _find():
    if os.environ.get('CUDART_PATH'):
        return os.environ['CUDART_PATH']
    try:
        spec = importlib.util.find_spec('nvidia.cuda_runtime')
        for d in (spec.submodule_search_locations or []) if spec else []:
            hits = sorted(glob.glob(os.path.join(d, 'lib', 'libcudart.so*')))
            if hits:
                return hits[0]
    except (ImportError, ValueError):
        pass
    return ctypes.util.find_library('cudart')


_path = _find()
if not _path:
    raise RuntimeError('libcudart not found; set CUDART_PATH')
_rc = ctypes.CDLL(_path).cudaSetDeviceFlags(ctypes.c_uint(4))
if _rc != 0:
    raise RuntimeError('cudaSetDeviceFlags(4) failed with code %d' % _rc)
