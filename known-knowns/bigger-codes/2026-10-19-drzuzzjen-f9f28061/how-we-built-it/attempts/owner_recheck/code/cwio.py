"""Readers for binary constant-weight code files (shared by the checkers for PARSING only; validity logic is not
shared). Formats:
  - Brouwer archive files (aeb.win.tue.nl/codes/cwc/...): header "$BASE=16", optionally "$N=<n>" (else n comes from
    the caller), then the words as fixed-width base-16 numbers (width = ceil(n/4)), one per line or concatenated.
  - Plain files: one word per line as a 0/1 string of length n (lines starting with '#' ignored).
Returns (n, list of Python ints). Bit i of the int is coordinate i (any fixed bijection is fine for the checks).
"""


def read_code(path, n_hint=None):
    text = open(path, encoding="utf-8", errors="strict").read()
    lines = [ln.strip() for ln in text.splitlines()]
    header = {}
    body = []
    for ln in lines:
        if not ln or ln.startswith("#"):
            continue
        if ln.startswith("$"):
            key, _, val = ln[1:].partition("=")
            header[key.strip().upper()] = val.strip()
        else:
            body.append(ln)
    if "BASE" in header:
        base = int(header["BASE"])
        if base != 16:
            raise ValueError("unsupported base %d" % base)
        if "N" in header:
            n = int(header["N"])
            if n_hint is not None and n_hint != n:
                raise ValueError("$N=%d differs from n=%d" % (n, n_hint))
        elif n_hint is not None:
            n = n_hint  # archive files without $N: one word per line, width ceil(n/4)
        else:
            raise ValueError("no $N header and no n given")
        width = (n + 3) // 4
        digits = "".join(body).replace(" ", "")
        if len(digits) % width:
            raise ValueError("hex stream length %d not a multiple of word width %d" % (len(digits), width))
        words = [int(digits[i:i + width], 16) for i in range(0, len(digits), width)]
        for x in words:
            if x >> n:
                raise ValueError("word exceeds length n")
        return n, words
    n = None
    words = []
    for ln in body:
        if set(ln) - {"0", "1"}:
            raise ValueError("non-binary line")
        if n is None:
            n = len(ln)
        elif len(ln) != n:
            raise ValueError("lines of different length")
        words.append(int(ln[::-1], 2))  # character j -> bit j
    return n, words
