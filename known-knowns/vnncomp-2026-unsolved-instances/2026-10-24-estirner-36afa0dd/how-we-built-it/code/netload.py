"""Load an ONNX(.gz) model for attacks: onnxruntime CPU session (1 thread) plus an onnx2torch module.
If onnx2torch fails on a BatchNormalization with unknown input rank, shapes are inferred with onnx.shape_inference
first (no weights are changed)."""
import gzip
import numpy as np
import onnx, onnxruntime as ort


def read_bytes(p):
    raw = open(p, 'rb').read()
    return gzip.decompress(raw) if p.endswith('.gz') else raw


def ort_session(raw):
    so = ort.SessionOptions(); so.intra_op_num_threads = 1; so.inter_op_num_threads = 1
    return ort.InferenceSession(raw, so, providers=['CPUExecutionProvider'])


def torch_model(raw, device):
    import torch
    from onnx2torch import convert
    m = onnx.load_from_string(raw)
    try:
        net = convert(m)
    except Exception as e:  # noqa
        m = onnx.shape_inference.infer_shapes(m)
        net = convert(m)
    return net.to(device).eval()


def ort_forward(sess, x, ishape):
    inp = sess.get_inputs()[0]
    shp = [d if isinstance(d, int) else 1 for d in inp.shape]
    if int(np.prod(shp)) != x.size:
        shp = ishape
    return sess.run(None, {inp.name: x.astype(np.float32).reshape(shp)})[0].astype(np.float32).ravel()
