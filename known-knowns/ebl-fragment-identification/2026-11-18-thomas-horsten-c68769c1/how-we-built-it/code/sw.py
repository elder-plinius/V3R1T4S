"""ctypes wrapper for the C banded Smith-Waterman aligner (swalign.so).

Token model: a *document* is a list of lines; each line is a tuple of sign tokens.
'X' (damaged/unknown sign) is the wildcard -> X_CODE = -1 in the C code.
Scores (frozen in PREREG): match +3, mismatch -1, gap -2, wildcard (X vs real) +1.
"""
import ctypes, os
import numpy as np
_here = os.path.dirname(os.path.abspath(__file__))
_lib = ctypes.CDLL(os.path.join(_here, "swalign.so"))
_lib.sw_align.argtypes = [
    ctypes.POINTER(ctypes.c_int), ctypes.c_int, ctypes.POINTER(ctypes.c_int),
    ctypes.POINTER(ctypes.c_int), ctypes.c_int, ctypes.POINTER(ctypes.c_int),
    ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int,
    ctypes.POINTER(ctypes.c_long), ctypes.POINTER(ctypes.c_long),
    ctypes.POINTER(ctypes.c_long), ctypes.POINTER(ctypes.c_long),
    ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int),
    ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)]
_lib.sw_align.restype = ctypes.c_int
X_CODE = -1


class Aligner:
    def __init__(self):
        self.code = {}
        self.n = 0

    def intern(self, docs):
        """docs: list of documents (list of line-tuples). Registers every token."""
        for doc in docs:
            for line in doc:
                for t in line:
                    if t not in self.code:
                        self.code[t] = self.n
                        self.n += 1
        return self

    def enc(self, doc):
        """doc: one document (list of line-tuples) -> (int32 token array, int32 line-index array)."""
        A, Al = [], []
        for li, line in enumerate(doc):
            for t in line:
                A.append(X_CODE if t == "X" else self.code[t])
                Al.append(li)
        return np.array(A, np.int32), np.array(Al, np.int32)

    def align(self, A, Al, B, Bl, band=40, min_block=6):
        def p(arr, ctype):
            return arr.ctypes.data_as(ctypes.POINTER(ctype))
        sc = np.zeros(1, np.int64); al = np.zeros(1, np.int64)
        mm = np.zeros(1, np.int64); wd = np.zeros(1, np.int64)
        alo = np.zeros(1, np.int32); ahi = np.zeros(1, np.int32)
        blo = np.zeros(1, np.int32); bhi = np.zeros(1, np.int32)
        r = _lib.sw_align(
            p(A, ctypes.c_int), len(A),
            p(Al, ctypes.c_int),
            p(B, ctypes.c_int), len(B),
            p(Bl, ctypes.c_int),
            band, 3, -1, -2, 1, min_block,
            p(sc, ctypes.c_long), p(al, ctypes.c_long),
            p(mm, ctypes.c_long), p(wd, ctypes.c_long),
            p(alo, ctypes.c_int), p(ahi, ctypes.c_int),
            p(blo, ctypes.c_int), p(bhi, ctypes.c_int))
        if r != 1:
            return None
        return {
            "score": int(sc[0]), "aligned": int(al[0]),
            "mismatches": int(mm[0]), "wildcards": int(wd[0]),
            "consec_lines_a": int(ahi[0] - alo[0] + 1),
            "consec_lines_b": int(bhi[0] - blo[0] + 1),
            "a_line_span": (int(alo[0]), int(ahi[0])),
            "b_line_span": (int(blo[0]), int(bhi[0])),
            "mismatch_frac": (int(mm[0]) / int(al[0])) if al[0] else 0.0,
        }
