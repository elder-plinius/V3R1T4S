#!/usr/bin/env python3
"""Shared statistic library for voynich-generator-heldout-fingerprints (run 2026-11-16-1141).

Implements the frozen PREREG §2 statistic definitions (S1-S9, H1-H4) on the fetched
ZL3b-n.txt / IT2a-n.txt (IVTFF), the per-quire / per-dialect bootstrap envelopes (PREREG §1),
and a standalone re-implementation of the Naibbe cipher (the author's published procedure)
for generating candidate corpora. Everything is deterministic given a seed.

This is independent of the pinned driver (lrozanova/voynich-units) — the driver's published
values are the reproduction gate (baseline/record.md); this library is what scores the
generator (lens 1) and the falsifier (lens 2).
"""
from __future__ import annotations
import math, random, re, json, hashlib
from collections import Counter, defaultdict

# ---------------------------------------------------------------- IVTFF parsing

PAGE_RE = re.compile(r'^<([^>.]+)>\s+<!\s*(.*?)>\s*$')
LOCUS_RE = re.compile(r'^<([^>.]+)\.(\d+),([@+*=~&])([A-Za-z])[^>]*>\s*(.*)$')
SUBS = [('cth','T'),('ckh','K'),('cph','P'),('cfh','F'),('ch','C'),('sh','S'),('iin','N'),('in','I'),('ee','E')]

def _strip_markup(s):
    s = re.sub(r'<[^>]*>','',s)
    s = re.sub(r'\[([^:\]]*):[^\]]*\]', r'\1', s)
    s = re.sub(r'\{[^}]*\}','',s)
    s = s.replace("'",'')
    return s

def collapse(w):
    w = w.lower().strip()
    for a,b in SUBS:
        w = w.replace(a,b)
    return w

def _line_tokens(content):
    """Return (raw_tokens, collapsed_tokens) for one locus line body."""
    s = _strip_markup(content)
    raw, col = [], []
    for w in re.split(r'[.,\s]+', s):
        w = w.strip().lower()
        if not w or any(c in '?*<>{}[]()|@' for c in w) or not re.fullmatch(r'[a-z]+', w):
            continue
        raw.append(w); col.append(collapse(w))
    return raw, col

class Doc:
    def __init__(self, path):
        self.path = path
        self.pages = []   # dicts: folio, quire, lang, raw_lines, col_lines
        quire=None; lang=None; folio=None
        with open(path, encoding='utf-8', errors='replace') as f:
            for raw in f:
                raw = raw.rstrip('\n')
                m = PAGE_RE.match(raw)
                if m:
                    folio = m.group(1)
                    var = dict(re.findall(r'\$([A-Z])=(\S+)', m.group(2)))
                    quire = var.get('Q'); lang = var.get('L')
                    continue
                m = LOCUS_RE.match(raw)
                if m and m.group(4) == 'P':
                    raw_t, col_t = _line_tokens(m.group(5))
                    if raw_t:
                        self.pages.append(dict(folio=folio, quire=quire, lang=lang,
                                               raw=raw_t, col=col_t))
        if not self.pages:
            raise SystemExit(f"no P-locus lines parsed from {path}")

    def by_dialect(self, d):
        return [p for p in self.pages if p['lang']==d]

    def quires(self, d):
        """map quire -> list of pages (in file order) for dialect d."""
        out = defaultdict(list)
        for p in self.pages:
            if p['lang']==d:
                out[p['quire']].append(p)
        return dict(out)

# ---------------------------------------------------------------- entropy helpers

def _log2(x): return math.log2(x) if x>0 else 0.0

def entropy(counts):
    tot = sum(counts.values())
    if tot==0: return 0.0
    return -sum((v/tot)*_log2(v/tot) for v in counts.values())

def conditional_entropy(pair_counts):
    """H(Y|X) for X->Y pair counts."""
    tot = sum(pair_counts.values())
    if tot==0: return 0.0
    xc = Counter()
    for (x,_),c in pair_counts.items(): xc[x]+=c
    h_xy = -sum((c/tot)*_log2(c/tot) for c in pair_counts.values())
    h_x  = -sum((v/tot)*_log2(v/tot) for v in xc.values())
    return max(h_xy - h_x, 0.0)

def mi_bits(pair_counts):
    """MI(X;Y) in bits."""
    tot = sum(pair_counts.values())
    if tot==0: return 0.0
    xc = Counter(); yc = Counter()
    for (x,y),c in pair_counts.items():
        xc[x]+=c; yc[y]+=c
    h_x = -sum((v/tot)*_log2(v/tot) for v in xc.values())
    h_y = -sum((v/tot)*_log2(v/tot) for v in yc.values())
    h_xy = -sum((c/tot)*_log2(c/tot) for c in pair_counts.values())
    return max(h_x + h_y - h_xy, 0.0)

# ---------------------------------------------------------------- per-corpus stats

def _edge_pairs(col_lines):
    """(left,last-char)(right,first-char) pairs across token boundaries within a line."""
    pairs = []
    for line in col_lines:
        for a,b in zip(line, line[1:]):
            pairs.append((a[-1], b[0]))
    return pairs

def s1_edge(col_lines, n_shuf=100, seed=20261116):
    """S1_bits, S1_share  (PREREG §2)."""
    obs = Counter(_edge_pairs(col_lines))
    mi_obs = mi_bits(obs)
    # marginal of the predicted (next) char
    nxt = Counter(p[1] for p in obs)
    h_next = entropy(nxt)
    rng = random.Random(seed)
    shuf_sum = 0.0; nused = 0
    for _ in range(n_shuf):
        sh_lines = []
        for line in col_lines:
            sl = list(line); rng.shuffle(sl); sh_lines.append(sl)
        shuf_sum += mi_bits(Counter(_edge_pairs(sh_lines))); nused += 1
    s1_bits = mi_obs - (shuf_sum/nused if nused else 0.0)
    s1_share = (s1_bits/h_next) if h_next>0 else 0.0
    return s1_bits, s1_share

def s2_hapax(raw_pages):
    freq = Counter(t for p in raw_pages for t in p['raw'])
    types = len(freq)
    if types==0: return 0.0, 0, 0
    hap = sum(1 for v in freq.values() if v==1)
    return hap/types, types, len(freq)

def s3_h2(col_pages):
    stream = [c for p in col_pages for w in p['col'] for c in w]
    if len(stream)<2: return 0.0
    pairs = Counter((stream[i], stream[i+1]) for i in range(len(stream)-1))
    return conditional_entropy(pairs)

def s4_wordlen(raw_pages):
    lens = [len(t) for p in raw_pages for t in p['raw']]
    if not lens: return 0.0, 0.0
    mean = sum(lens)/len(lens)
    share1 = sum(1 for L in lens if L==1)/len(lens)
    return mean, share1

def s5_es(col_pages, graph_inv=None):
    """S5: E->S % using grapheme start/end classes (PREREG §2, currier-signatures def)."""
    if graph_inv is None:
        graph_inv = [c for c in set(''.join(''.join(p['col']) for p in col_pages)) if len(c)==1]
    tok = make_greedy(graph_inv)
    sc, ec = Counter(), Counter()
    for p in col_pages:
        for w in p['col']:
            t = tok(w)
            if not t: continue
            sc[t[0]] += 1; ec[t[-1]] += 1
    cls = {}
    for g in set(sc)|set(ec):
        s,e = sc.get(g,0), ec.get(g,0)
        cls[g] = 'start' if s>2*e else 'end' if e>2*s else 'ambig'
    es = tot = 0
    for p in col_pages:
        words = [tok(w) for w in p['col']]
        words = [w for w in words if w]
        for i in range(len(words)-1):
            if cls.get(words[i][-1])=='end' and cls.get(words[i+1][0])=='start':
                es += 1
            tot += 1
    return 100.0*es/tot if tot else 0.0

def s6_bilateral(col_pages, graph_inv=None, thr=100.0):
    if graph_inv is None:
        graph_inv = [c for c in set(''.join(''.join(p['col']) for p in col_pages)) if len(c)==1]
    tok = make_greedy(graph_inv)
    sc, ec = Counter(), Counter()
    for p in col_pages:
        for w in p['col']:
            t = tok(w)
            if not t: continue
            sc[t[0]] += 1; ec[t[-1]] += 1
    nse = sum(1 for g in set(sc)|set(ec) if (sc.get(g,0)+1)/(ec.get(g,0)+1) > thr)
    nee = sum(1 for g in set(sc)|set(ec) if (ec.get(g,0)+1)/(sc.get(g,0)+1) > thr)
    return nse, nee

def s7_mi(col_pages, graph_inv=None):
    if graph_inv is None:
        graph_inv = [c for c in set(''.join(''.join(p['col']) for p in col_pages)) if len(c)==1]
    tok = make_greedy(graph_inv)
    tr = Counter()
    for p in col_pages:
        words = [tok(w) for w in p['col']]; words=[w for w in words if w]
        for i in range(len(words)-1):
            tr[(words[i][-1], words[i+1][0])] += 1
    return mi_bits(tr)

def s8_zipf(col_pages, graph_inv=None):
    if graph_inv is None:
        graph_inv = [c for c in set(''.join(''.join(p['col']) for p in col_pages)) if len(c)==1]
    tok = make_greedy(graph_inv)
    sc = Counter()
    for p in col_pages:
        for w in p['col']:
            t = tok(w)
            if t: sc[t[0]] += 1
    if len(sc)<3: return 0.0,0.0,'insufficient'
    import numpy as np
    freqs = np.array(sorted(sc.values(), reverse=True), dtype=float)
    ranks = np.arange(1, len(freqs)+1, dtype=float)
    log_r, log_f = np.log(ranks), np.log(freqs+1e-10)
    pred = np.polyval(np.polyfit(log_r, log_f, 1), log_r)
    ss_res = np.sum((log_f-pred)**2); ss_tot = np.sum((log_f-np.mean(log_f))**2)
    r2 = 1.0-ss_res/ss_tot if ss_tot>0 else 0.0
    cv = float(np.std(freqs)/np.mean(freqs)) if np.mean(freqs)>0 else 0.0
    shape = 'Zipfian' if r2>0.85 and cv>0.8 else 'Plateau' if cv<0.5 else 'Intermediate'
    return r2, cv, shape

def s9_switch(col_pages):
    """Per-folio (per-page here) cho/che switch statistic (PREREG §2 S9)."""
    folio_r = []
    for p in col_pages:
        ncho = nche = 0
        for w in p['col']:
            has_cho = ('Co' in w) or ('So' in w)
            has_che = ('Ce' in w) or ('Se' in w)
            if has_cho and not has_che: ncho += 1
            elif has_che and not has_cho: nche += 1
        if ncho+nche >= 1:
            folio_r.append(ncho/(ncho+nche))
    if not folio_r:
        return dict(n=0, ambiguous=0.0, mean_cho=0.0, mean_che=0.0, r_all=[])
    amb = sum(1 for r in folio_r if 0.3<=r<=0.5)
    cho = [r for r in folio_r if r>0.5]; che=[r for r in folio_r if r<=0.5]
    return dict(n=len(folio_r),
                ambiguous=amb/len(folio_r),
                mean_cho=(sum(cho)/len(cho)) if cho else 0.0,
                mean_che=(sum(che)/len(che)) if che else 0.0,
                r_all=folio_r)

def h1_edit1(col_pages, n_shuf=100, seed=20261117):
    """H1: edit-1 adjacency ratio (observed / mean-shuffled) (PREREG §2 H1)."""
    def edit1count(lines):
        c = 0
        for line in lines:
            for a,b in zip(line, line[1:]):
                if _lev1(a,b): c += 1
        return c
    obs = edit1count(col_pages)
    rng = random.Random(seed); tot=0
    for _ in range(n_shuf):
        sl = []
        for line in col_pages:
            x = list(line); rng.shuffle(x); sl.append(x)
        tot += edit1count(sl)
    shuf = tot/n_shuf
    return (obs/shuf) if shuf>0 else float('inf')

def _lev1(a,b):
    """True if Levenshtein distance <= 1 (strings similar length)."""
    if a==b: return True
    la, lb = len(a), len(b)
    if abs(la-lb)>1: return False
    if la==lb:
        d = sum(1 for i in range(la) if a[i]!=b[i]); return d<=1
    if la==lb+1:
        # deletion: skip one char in a
        i=j=0; skipped=False; d=0
        while i<la and j<lb:
            if a[i]==b[j]: i+=1; j+=1
            else:
                if skipped: return False
                skipped=True; i+=1
        return True
    # lb==la+1: insertion
    i=j=0; skipped=False; d=0
    while i<la and j<lb:
        if a[i]==b[j]: i+=1; j+=1
        else:
            if skipped: return False
            skipped=True; j+=1
    return True

def h2_jsd(col_pages):
    """H2: JSD between line-initial and mid-line token-initial glyph distributions (PREREG §2 H2)."""
    line_init = Counter(); mid_init = Counter()
    for p in col_pages:
        for i, w in enumerate(p['col']):
            if not w: continue
            if i==0: line_init[w[0]] += 1
            else: mid_init[w[0]] += 1
    def _jsd(p,q):
        tp, tq = sum(p.values()), sum(q.values())
        if tp==0 or tq==0: return 0.0
        m = {k:(p.get(k,0)/tp + q.get(k,0)/tq)/2.0 for k in set(p)|set(q)}
        pm = {k:v/tp for k,v in p.items()}
        qm = {k:v/tq for k,v in q.items()}
        def _kl(x,y):
            return sum(vx*_log2(vx/yv) for k,vx in x.items() if (yv:=y.get(k,0.0))>0)
        return 0.5*_kl(pm,m)+0.5*_kl(qm,m)
    return _jsd(line_init, mid_init)

def h3_top50(raw_pages):
    freq = Counter(t for p in raw_pages for t in p['raw'])
    tot = sum(freq.values())
    if tot==0: return 0.0
    top = sum(c for _,c in freq.most_common(50))
    return top/tot

def h4_quire_cv(cv_of_quires):
    """CV of the per-quire hapax rates (list of floats)."""
    if len(cv_of_quires)<2: return 0.0
    import statistics
    m = statistics.mean(cv_of_quires)
    if m==0: return 0.0
    return statistics.pstdev(cv_of_quires)/m

# ---------------------------------------------------------------- grapheme inventory

def make_greedy(grapheme_list):
    srt = sorted(grapheme_list, key=lambda x:(-len(x),x))
    def tok(word):
        toks=[]; i=0
        while i < len(word):
            for g in srt:
                if word[i:i+len(g)]==g:
                    toks.append(g); i+=len(g); break
            else:
                toks.append(word[i]); i+=1
        return toks
    return tok

def build_graph_inv(texts):
    """Data-driven grapheme inventory: distinct substrings (len>=2, freq>=3) + single chars."""
    freq = Counter()
    single = set()
    for t in texts:
        for c in t: single.add(c)
        n=len(t)
        for L in (2,3,4):
            for i in range(n-L+1):
                freq[t[i:i+L]] += 1
    inv = [g for g,c in freq.items() if c>=3]
    inv += sorted(single)
    return sorted(set(inv), key=lambda x:(-len(x),x))

# ---------------------------------------------------------------- Naibbe cipher (standalone)

def load_naibbe_tables(json_path):
    j = json.load(open(json_path))
    return j

def NaibbeGen(tables, deck="deck_52", p_uni=17/36, rule="v1"):
    unigram = tables['unigram']; prefix = tables['prefix']; suffix = tables['suffix']
    deck_spec = tables[deck]
    uni_glyphs = {g for t in unigram.values() for g in t.values()}
    alphabet = set(tables['alphabet'])
    class Gen:
        def __init__(self):
            self.rng = None
        def respace(self, letters):
            chunks=[]; i=0; n=len(letters)
            while i<n:
                if i==n-1 or self.rng.random()<p_uni:
                    chunks.append((i,letters[i])); i+=1
                else:
                    chunks.append((i,letters[i:i+2])); i+=2
            return chunks
        def encrypt(self, letters, seed):
            self.rng = random.Random(seed)
            chunks = self.respace(letters)
            deck=[]; tokens=[]; retries=0
            def draw():
                nonlocal deck
                if not deck:
                    deck=[t for t,n in deck_spec.items() for _ in range(n)]
                    self.rng.shuffle(deck); deck.reverse()
                return deck.pop()
            for _,ch in chunks:
                if len(ch)==1:
                    tokens.append(unigram[draw()][ch]); continue
                while True:
                    t1=draw(); pre=prefix[t1][ch[0]]
                    t2=draw(); suf=suffix[t2][ch[1]]
                    comb=pre+suf
                    if comb in uni_glyphs:
                        retries+=1
                        if rule=='v2':
                            pass
                        continue
                    tokens.append(comb); break
            return tokens, retries
    return Gen()

# ---------------------------------------------------------------- envelopes

def quire_bootstrap(doc, d, statfn, B=4000, seed=20261116, pages_arg=None):
    """Bootstrap a per-quire statistic over dialect d's quires (PREREG §1)."""
    if pages_arg is None:
        quires = doc.quires(d)
    else:
        quires = pages_arg
    qkeys = list(quires.keys())
    rng = random.Random(seed)
    vals = []
    for b in range(B):
        pick = [qkeys[rng.randrange(len(qkeys))] for _ in range(len(qkeys))]
        pool = [p for q in pick for p in quires[q]]
        if pool:
            vals.append(statfn(pool))
    return vals

def pct(vals, p):
    if not vals: return (0.0,0.0)
    vs = sorted(vals)
    k = (len(vs)-1)*p/100.0
    f = math.floor(k); c = math.ceil(k)
    if f==c: return vs[int(k)]
    return vs[f]*(c-k)+vs[c]*(k-f)

def envelope(vals, lo=0.025, hi=97.5):
    return pct(vals, lo*100), pct(vals, hi*100)
