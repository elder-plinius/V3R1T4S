"""Shared alignment library for the ebl-fragment-identification hunt.

Design (frozen in PREREG.md):
- Input: eBL 'signs' strings (newline-separated lines, whitespace-separated sign tokens)
  from the public bulk endpoints /api/fragments/all-signs and /api/corpus/all-signs.
- Normalisation: consistent on both fragment and chapter sides (both come from the same
  eBL sign-name pipeline). See normalise_token.
- Aligner: independent sign-level local alignment (Smith-Waterman style) that tracks
  line boundaries so we can report 'consecutive lines' and 'consecutive signs'.
- Candidate pre-filter: rare sign n-gram inverted index (order-independent), to keep the
  per-fragment x per-chapter cost bounded. The alignment itself (and the null) is what
  judges candidates; the filter only prunes.
- Null: shuffle the GLOBAL pool of corpus lines (order randomised per seed), re-run the
  same filter+align pipeline, record best score. Real must beat every control.
"""
import json, re, unicodedata
from collections import defaultdict

# ---------------- token normalisation (frozen) ----------------
_SLASH = re.compile(r"/")

def normalise_token(t):
    """Consistent, documented sign-token normalisation.
    - NFC normalise (fixes diš / di+combining, subscript markers, etc.)
    - variant reading 'a/b/c' -> primary reading 'a' (first element). Variants are
      recorded separately; the alignment uses the primary reading.
    - 'X' (damaged / unknown sign) is kept as the special token X (a wildcard that
      may match anything with a penalty).
    - everything else is kept verbatim (ABZ codes are case-stable; values/numerals kept).
    """
    t = unicodedata.normalize("NFC", t).strip()
    if t == "":
        return None
    if "/" in t:
        t = t.split("/", 1)[0].strip()  # primary reading only
        t = unicodedata.normalize("NFC", t)
    return t

def normalise_signs(signs):
    """signs: str or list[str]. Returns list of lines, each a tuple of normalised tokens."""
    if isinstance(signs, (list, tuple)):
        signs = signs[0] if signs else ""
    if not isinstance(signs, str):
        signs = ""
    lines = []
    for raw in signs.split("\n"):
        toks = [normalise_token(x) for x in raw.split()]
        toks = [x for x in toks if x is not None]
        lines.append(tuple(toks))
    return lines

# ---------------- n-gram inverted index (candidate filter) ----------------
def ngrams(tokens, n):
    for i in range(max(0, len(tokens) - n + 1)):
        yield tuple(tokens[i:i+n])

class NgramIndex:
    """Inverted index over rare n-grams of a corpus of line-sequence 'documents'.
    document = a chapter (or a shuffled-chapter pool). We index sign n-grams across the
    whole corpus (line order preserved within a doc for the real corpus; for a shuffled
    pool the n-grams are recomputed on the shuffled order)."""
    def __init__(self, n, rare_df_max):
        self.n = n
        self.rare_df_max = rare_df_max
        self.df = defaultdict(int)          # ngram -> number of docs containing it
        self.docs = []                      # list of docs (each a list of token tuples)

    def add_doc(self, doc_tokens_list, meta):
        self.docs.append((doc_tokens_list, meta))
        seen = set()
        for line in doc_tokens_list:
            for g in ngrams(line, self.n):
                seen.add(g)
        for g in seen:
            self.df[g] += 1

    def rare_grams(self, tokens_list):
        """rare n-grams of a fragment (df <= rare_df_max), as a set."""
        out = set()
        for line in tokens_list:
            for g in ngrams(line, self.n):
                if self.df.get(g, 0) <= self.rare_df_max:
                    out.add(g)
        return out

    def _build_inverted(self):
        if hasattr(self, "_inv"): return
        inv = defaultdict(set)
        for di,(doc_tokens, meta) in enumerate(self.docs):
            seen=set()
            for line in doc_tokens:
                for g in ngrams(line, self.n):
                    if self.df.get(g,0) <= self.rare_df_max:
                        seen.add(g)
            for g in seen:
                inv[g].add(di)
        self._inv = inv

    def candidate_docs(self, frag_grams, topk=20, min_hits=1):
        """Return the doc ids whose rare n-grams overlap frag_grams, ranked by #shared
        rare n-grams (order-independent). This is the pre-filter; alignment is the judge."""
        self._build_inverted()
        counts = defaultdict(int)
        if not frag_grams:
            return []
        for g in frag_grams:
            for di in self._inv.get(g, ()):
                counts[di] += 1
        ranked = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
        return [kv for kv in ranked if kv[1] >= min_hits][:topk]

# ---------------- sign-level local alignment (Smith-Waterman) with line tracking ----
def _flat_with_lines(lines):
    """Return (flat tokens list, token->line index list)."""
    flat = []
    tl = []
    for li, line in enumerate(lines):
        for t in line:
            flat.append(t)
            tl.append(li)
    return flat, tl

def local_align(a_lines, b_lines, match=3, mismatch=-1, gap=-2, xmatch=1,
                 min_score=1, min_block_len=6, band=None):
    """Independent sign-level local alignment (Smith-Waterman) over the flat token
    sequence, with line tracking. numpy-accelerated; optional diagonal band to bound cost.

    - 'X' (damaged) tokens act as a wildcard: they match any non-X token with score
      xmatch (penalised relative to a real match).
    Returns dict or None (if best < min_score or block < min_block_len).
    """
    import numpy as np
    a, a_line = _flat_with_lines(a_lines)
    b, b_line = _flat_with_lines(b_lines)
    n, m = len(a), len(b)
    if n == 0 or m == 0:
        return None
    a = np.asarray(a); b = np.asarray(b)
    # banded: restrict to a diagonal window of half-width `band`. If band is None,
    # use full (band = max(n,m)) i.e. no banding.
    if band is None:
        band = max(n, m)
    band = int(band)
    prev = np.zeros(m + 1, dtype=np.int32)
    cur = np.zeros(m + 1, dtype=np.int32)
    trace = np.zeros((n + 1, m + 1), dtype=np.int8)
    best = 0; bi = 0; bj = 0
    for i in range(1, n + 1):
        ai = a[i-1]
        jlo = max(1, i - band); jhi = min(m, i + band)
        if jlo > jhi:  # fragment row is beyond the banded window of the (shorter) text
            prev, cur = cur, prev
            cur[:] = 0
            continue
        w = jhi - jlo + 1           # number of j columns in this row band
        seg = b[jlo-1:jhi]          # length w : b[j-1] for j in [jlo..jhi]
        # substitution scores for aligning a[i-1] with b[j-1], j in band
        sub = np.full(w, mismatch, dtype=np.int32)
        eq = (seg == ai)
        sub[eq] = match
        wild = (seg == "X") | (ai == "X")
        sub[wild & ~eq] = xmatch
        # recurrence candidates at (i, j), j in [jlo..jhi] (w values):
        #   diag = prev[j-1] + sub     -> prev[jlo-1 .. jhi-1]  (length w)
        #   up   = cur[j-1] + gap      -> cur[jlo-1 .. jhi-1]  (length w)
        #   left = cur[j]  + gap       -> cur[jlo   .. jhi]    (length w)
        diag = prev[jlo-1:jhi] + sub
        up   = cur [jlo-1:jhi] + gap
        left = cur [jlo:jhi+1] + gap
        M = np.stack([diag, up, left], axis=0)      # shape (3, w)
        idx = M.argmax(axis=0)                       # (w,)
        v = M[idx, np.arange(w)]                     # (w,)
        trv = np.where(idx == 0, 2, np.where(idx == 1, 1, 3)).astype(np.int8)
        cur[jlo:jhi+1] = v
        trace[i, jlo:jhi+1] = trv
        k = int(np.argmax(v))
        pos = v[k]
        if pos > best:
            best = int(pos); bi = i; bj = jlo + k
        prev, cur = cur, prev
        cur[:] = 0
    if best < min_score:
        return None
    # backtrack
    i, j = bi, bj
    pairs = []
    while i > 0 and j > 0 and trace[i, j] != 0:
        trv = trace[i, j]
        if trv == 2:
            pairs.append((i-1, j-1)); i -= 1; j -= 1
        elif trv == 1:
            i -= 1
        else:
            j -= 1
    pairs.reverse()
    if len(pairs) < min_block_len:
        return None
    aligned = 0; mismatch_ct = 0; wildcard_ct = 0
    for (x, y) in pairs:
        aligned += 1
        ai = a[x]; bj_t = b[y]
        if ai == bj_t:
            pass
        elif ai == "X" or bj_t == "X":
            wildcard_ct += 1
        else:
            mismatch_ct += 1
    a_min_line = min(a_line[x] for (x, _) in pairs)
    a_max_line = max(a_line[x] for (x, _) in pairs)
    b_min_line = min(b_line[y] for (_, y) in pairs)
    b_max_line = max(b_line[y] for (_, y) in pairs)
    mismatch_frac = (mismatch_ct / aligned) if aligned else 0.0
    return {
        "score": best,
        "aligned": aligned,
        "mismatches": mismatch_ct,
        "wildcards": wildcard_ct,
        "mismatch_frac": mismatch_frac,
        "consec_lines_a": a_max_line - a_min_line + 1,
        "consec_lines_b": b_max_line - b_min_line + 1,
        "a_line_span": (a_min_line, a_max_line),
        "b_line_span": (b_min_line, b_max_line),
        "pairs": pairs,
    }
