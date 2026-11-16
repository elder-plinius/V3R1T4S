#!/usr/bin/env python3
"""Precompute per-quire structures, observed Voynich stats, and save preloads.

For each (d, T) cell: parse Doc, group P-pages by quire, and precompute per quire:
  col_lines, raw_lines, pair_c (glyph-stream pairs), gc (glyph unigrams), n_glyphs,
  edge_pairs (last-char -> first-char across token boundaries within a line),
  edge_sh_mean (mean MI over 100 within-line shuffles, fixed seed), n_edges,
  H_next (pooled next-char marginal entropy placeholder; recomputed pooled),
  sc/ec/firstc (start/end/first grapheme... via precomputed first/last grapheme
  streams: fstream = per-token first grapheme, lstream = per-token last grapheme),
  raw_freq, n_tokens, mean_len, share1, hapax, n_types,
  line_init_c / mid_init_c (first-glyph counters for line-initial vs mid-line tokens),
  folio_r (per-page r_cho),
  h1_obs (observed adjacent edit-1 count), h1_sh_tot (sum over 100 shuffles).
Also: inter-quire boundary glyph pairs (for S3 pool exactness) in canonical quire order.

Observed values (full corpus, canonical order) -> output/observed_<d>_<T>.json
Preloads (picklable) -> output/preload_<d>_<T>.json  (consumed by env_worker.py)

Grapheme inventory: frozen from ZL3b (all collapsed lines), output/graph_inv.json.
"""
from __future__ import annotations
import json, os, sys, hashlib, random, math
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vstats import (Doc, make_greedy, build_graph_inv, conditional_entropy,
                    mi_bits, entropy, _log2)

RUN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(RUN, 'data')
OUT = os.path.join(RUN, 'output')
os.makedirs(OUT, exist_ok=True)
SHUF_SEED = 20261116

def load_docs():
    return {'ZL3b': Doc(os.path.join(DATA,'ZL3b-n.txt')),
            'IT2a': Doc(os.path.join(DATA,'IT2a-n.txt'))}

def _lev1(a,b):
    """Levenshtein distance <= 1."""
    la, lb = len(a), len(b)
    if abs(la-lb) > 1: return False
    if la == lb:
        d = 0
        for i in range(la):
            d += a[i] != b[i]
            if d > 1: return False
        return True
    if lb == la + 1:  # one char inserted into a -> b
        i = j = 0; skipped = False
        while i < la and j < lb:
            if a[i] == b[j]: i += 1; j += 1
            else:
                if skipped: return False
                skipped = True; j += 1
        return True
    i = j = 0; skipped = False  # one char deleted from a -> b
    while i < la and j < lb:
        if a[i] == b[j]: i += 1; j += 1
        else:
            if skipped: return False
            skipped = True; i += 1
    return True

def precompute_quires(T, d, INV):
    doc = load_docs()[T]
    quires = doc.quires(d)
    P = {}
    for qk, pages in sorted(quires.items()):
        col_lines = [p['col'] for p in pages]
        raw_lines = [p['raw'] for p in pages]
        n_glyphs = sum(len(w) for line in col_lines for w in line)
        gc = Counter(c for line in col_lines for w in line for c in w)
        pair_c = Counter()
        for w in (x for line in col_lines for x in line):
            for i in range(len(w)-1):
                pair_c[(w[i],w[i+1])] += 1
        edge_pairs = Counter()
        n_edges = 0
        for line in col_lines:
            for a,b in zip(line, line[1:]):
                edge_pairs[(a[-1], b[0])] += 1
                n_edges += 1
        # flat-stream glyph pairs (for S3 h2): within-token + within-line edge + inter-quire boundary
        flat_pairs = Counter()
        for line in col_lines:
            for w in line:
                for i in range(len(w)-1):
                    flat_pairs[(w[i], w[i+1])] += 1
            for a,b in zip(line, line[1:]):
                flat_pairs[(a[-1], b[0])] += 1
        # 100 within-line shuffles of the edge MI (fixed seed, quire-local)
        rng = random.Random(SHUF_SEED + 7*ord(d) + 13*ord(T[0]))
        sh_tot = 0.0
        for _ in range(100):
            sl = []
            for line in col_lines:
                x = list(line); rng.shuffle(x); sl.append(x)
            sh_tot += mi_bits(Counter((a[-1],b[0]) for line in sl for a,b in zip(line,line[1:])))
        edge_sh_mean = sh_tot/100.0
        # per-line first/last grapheme pairs (for S5/S7; boundaries within lines only)
        fl_lines = []
        sc = Counter(); ec = Counter(); firstc = Counter()
        for line in col_lines:
            fl = []
            for w in line:
                t = INV(w)
                if not t: continue
                fl.append((t[0], t[-1]))
                sc[t[0]] += 1; ec[t[-1]] += 1; firstc[t[0]] += 1
            fl_lines.append(fl)
        # H2 structures
        line_init_c = Counter(); mid_init_c = Counter()
        for line in col_lines:
            for i, w in enumerate(line):
                if i==0: line_init_c[w[0]] += 1
                else: mid_init_c[w[0]] += 1
        # H1 (PREREG: observed/shuffled ratio of adjacent tokens within one edit;
        # the paper's Table-4 uses 100 within-line shuffles)
        h1_obs = sum(1 for line in col_lines for a,b in zip(line,line[1:]) if _lev1(a,b))
        rng2 = random.Random(20261117 + 101*ord(d) + 103*ord(T[0]))
        h1_sh_tot = 0
        for _ in range(100):
            c = 0
            for line in col_lines:
                x = list(line); rng2.shuffle(x)
                c += sum(1 for a,b in zip(x,x[1:]) if _lev1(a,b))
            h1_sh_tot += c
        # token-level first/last char counters (for S1 null, v2: within-line expectation)
        first_c_t = Counter(); last_c_t = Counter()
        for line in col_lines:
            for w in line:
                first_c_t[w[0]] += 1; last_c_t[w[-1]] += 1
        # H1 null (v2): exact expectation of adjacent edit-1 count under within-line
        # shuffling = (n-1)/n * (number of ordered distinct-token pairs within edit 1)
        # H1 exact within-line shuffle null (unbiased estimator of the paper's
        # 100-shuffle ratio): E[# adjacent edit-1 pairs after shuffling a line]
        # = (1/n) * sum_{a,b} n_a (n_b - [a==b]) * lev1(a,b)  [random permutation]
        h1_m = 0.0
        for line in col_lines:
            n = len(line)
            if n < 2: continue
            m = 0
            for i in range(n):
                for j in range(n):
                    if i!=j and _lev1(line[i], line[j]): m += 1
            h1_m += m / n
        # vocabulary
        raw_freq = Counter(t for p in raw_lines for t in p)
        n_tokens = len(raw_freq) and sum(raw_freq.values())
        hap = sum(1 for v in raw_freq.values() if v==1)/max(1,len(raw_freq))
        lens = [len(t) for p in raw_lines for t in p]
        # per-folio r_cho
        folio_r = []
        for p in pages:
            ncho = nche = 0
            for w in p['col']:
                hco = ('Co' in w) or ('So' in w); hce = ('Ce' in w) or ('Se' in w)
                if hco and not hce: ncho += 1
                elif hce and not hco: nche += 1
            if ncho+nche >= 5:
                folio_r.append(ncho/(ncho+nche))
        P[qk] = dict(col_lines=col_lines, raw_freq=raw_freq, n_tokens=n_tokens,
                     flat_pairs=flat_pairs,
                     mean_len=(sum(lens)/len(lens)) if lens else 0.0,
                     share1=(sum(1 for L in lens if L==1)/len(lens)) if lens else 0.0,
                     hapax=hap, n_types=len(raw_freq),
                     pair_c=pair_c, gc=gc, n_glyphs=n_glyphs,
                     edge_pairs=edge_pairs, n_edges=n_edges, edge_sh_mean=edge_sh_mean,
                     first_c_t=first_c_t, last_c_t=last_c_t, h1_m=h1_m,
                     sc=sc, ec=ec, firstc=firstc, fl_lines=fl_lines,
                     line_init_c=line_init_c, mid_init_c=mid_init_c,
                     folio_r=folio_r, h1_obs=h1_obs, h1_sh_tot=h1_sh_tot)
    qorder = sorted(P.keys(), key=lambda x:(len(x),x))
    boundaries = Counter()
    for a,b in zip(qorder, qorder[1:]):
        la = [x for p in P[a]['col_lines'] for x in p]
        lb = [x for p in P[b]['col_lines'] for x in p]
        if la and lb:
            boundaries[(la[-1][-1], lb[0][0])] += 1
    return P, qorder, boundaries

def stat_pool(name, P, qorder, boundaries, sel):
    keys = [qorder[i] for i in sel]
    if name == 'S3':
        pc = Counter()
        for k in keys: pc.update(P[k]['flat_pairs'])
        pc.update(boundaries)
        return conditional_entropy(pc)
    if name == 'S1':
        pc = Counter()
        Lc = Counter(); Fc = Counter()
        for k in keys:
            pc.update(P[k]['edge_pairs'])
            Lc.update(P[k]['last_c_t']); Fc.update(P[k]['first_c_t'])
        mi_obs = mi_bits(pc)
        # within-line expectation null: pooled token-level joint distribution
        nullc = Counter()
        for a in Lc:
            for b in Fc:
                nullc[(a,b)] = Lc[a]*Fc[b]
        mi_null = mi_bits(nullc)
        s1b = mi_obs - mi_null
        Hnext = entropy(Fc)
        return s1b, (s1b/Hnext if Hnext>0 else 0.0)
    if name == 'S2':
        tt = sum(P[k]['n_types'] for k in keys)
        th = sum(P[k]['hapax']*P[k]['n_types'] for k in keys)
        return (th/tt) if tt else 0.0
    if name == 'S4':
        nl = sum(P[k]['n_tokens'] for k in keys)
        if not nl: return 0.0, 0.0
        return (sum(P[k]['mean_len']*P[k]['n_tokens'] for k in keys)/nl,
                sum(P[k]['share1']*P[k]['n_tokens'] for k in keys)/nl)
    if name == 'S5':
        sc, ec = Counter(), Counter()
        for k in keys:
            sc.update(P[k]['sc']); ec.update(P[k]['ec'])
        cls = {}
        for g in set(sc)|set(ec):
            s,e = sc.get(g,0), ec.get(g,0)
            cls[g] = 'start' if s>2*e else 'end' if e>2*s else 'ambig'
        es = tot = 0
        for k in keys:
            for fl in P[k]['fl_lines']:
                for i in range(len(fl)-1):
                    if cls.get(fl[i][1])=='end' and cls.get(fl[i+1][0])=='start': es += 1
                    tot += 1
        return 100.0*es/tot if tot else 0.0
    if name == 'S6':
        sc, ec = Counter(), Counter()
        for k in keys:
            sc.update(P[k]['sc']); ec.update(P[k]['ec'])
        nse = sum(1 for g in set(sc)|set(ec) if (sc.get(g,0)+1)/(ec.get(g,0)+1)>100)
        nee = sum(1 for g in set(sc)|set(ec) if (ec.get(g,0)+1)/(sc.get(g,0)+1)>100)
        return nse, nee
    if name == 'S7':
        tr = Counter()
        for k in keys:
            for fl in P[k]['fl_lines']:
                for i in range(len(fl)-1):
                    tr[(fl[i][1], fl[i+1][0])] += 1
        return mi_bits(tr)
    if name == 'S8':
        fc = Counter()
        for k in keys: fc.update(P[k]['firstc'])
        import numpy as np
        freqs = np.array(sorted(fc.values(), reverse=True), dtype=float)
        ranks = np.arange(1, len(freqs)+1, dtype=float)
        log_r, log_f = np.log(ranks), np.log(freqs+1e-10)
        pred = np.polyval(np.polyfit(log_r, log_f, 1), log_r)
        ss_res = float(np.sum((log_f-pred)**2)); ss_tot = float(np.sum((log_f-np.mean(log_f))**2))
        r2 = 1.0-ss_res/ss_tot if ss_tot>0 else 0.0
        cv = float(np.std(freqs)/np.mean(freqs)) if np.mean(freqs)>0 else 0.0
        return r2, cv
    if name == 'S9':
        fr = [r for k in keys for r in P[k]['folio_r']]
        if not fr: return 0.0, 0.0, 0.0
        amb = sum(1 for r in fr if 0.3<=r<=0.5)/len(fr)
        cho = [r for r in fr if r>0.5]; che=[r for r in fr if r<=0.5]
        return amb, (sum(cho)/len(cho) if cho else 0.0), (sum(che)/len(che) if che else 0.0)
    if name == 'H1':
        obs = sum(P[k]['h1_obs'] for k in keys)
        nul = sum(P[k]['h1_sh_tot'] for k in keys)/100.0
        return obs/nul if nul>0 else float('inf')
    if name == 'H2':
        li = Counter(); mi = Counter()
        for k in keys:
            li.update(P[k]['line_init_c']); mi.update(P[k]['mid_init_c'])
        tp, tq = sum(li.values()), sum(mi.values())
        if tp==0 or tq==0: return 0.0
        m = {k:(li.get(k,0)/tp + mi.get(k,0)/tq)/2.0 for k in set(li)|set(mi)}
        pm = {k:v/tp for k,v in li.items()}; qm = {k:v/tq for k,v in mi.items()}
        def _kl(x,y):
            return sum(vx*_log2(vx/y.get(k,0.0)) for k,vx in x.items() if y.get(k,0.0)>0)
        return 0.5*_kl(pm,m) + 0.5*_kl(qm,m)
    if name == 'H3':
        fc = Counter()
        for k in keys: fc.update(P[k]['raw_freq'])
        tot = sum(fc.values())
        return (sum(c for _,c in fc.most_common(50))/tot) if tot else 0.0
    if name == 'H4':
        vals = [P[k]['hapax'] for k in keys]
        if len(vals)<2: return 0.0
        import statistics
        m = statistics.mean(vals)
        return (statistics.pstdev(vals)/m) if m else 0.0
    raise ValueError(name)

STATS = ['S1','S2','S3','S4','S5','S6','S7','S8','S9','H1','H2','H3','H4']

def main():
    inv_path = os.path.join(OUT, 'paper_graph_inv.json')
    INV_list = json.load(open(inv_path))
    if not INV_list:
        raise SystemExit('paper_graph_inv.json missing (reconstruct from 2604.19762 pools)')
    INV = make_greedy(INV_list)
    print(f"grapheme inventory frozen: {len(INV_list)} graphemes, sha256 "
          f"{hashlib.sha256(json.dumps(INV_list).encode()).hexdigest()[:16]}", flush=True)

    for T in ('ZL3b','IT2a'):
        for d in ('A','B'):
            P, qorder, boundaries = precompute_quires(T, d, INV)
            keys_all = list(range(len(qorder)))
            obs = {}
            obs['S1_bits'], obs['S1_share'] = stat_pool('S1', P, qorder, boundaries, keys_all)
            obs['S2'] = stat_pool('S2', P, qorder, boundaries, keys_all)
            obs['S3'] = stat_pool('S3', P, qorder, boundaries, keys_all)
            obs['S4a'], obs['S4b'] = stat_pool('S4', P, qorder, boundaries, keys_all)
            obs['S5'] = stat_pool('S5', P, qorder, boundaries, keys_all)
            nse, nee = stat_pool('S6', P, qorder, boundaries, keys_all)
            obs['S6_Se'], obs['S6_Ee'] = nse, nee
            obs['S7'] = stat_pool('S7', P, qorder, boundaries, keys_all)
            r2, cv = stat_pool('S8', P, qorder, boundaries, keys_all)
            obs['S8_R2'], obs['S8_CV'] = r2, cv
            a, m1, m0 = stat_pool('S9', P, qorder, boundaries, keys_all)
            obs['S9_amb'], obs['S9_mean_cho'], obs['S9_mean_che'] = a, m1, m0
            obs['H1'] = stat_pool('H1', P, qorder, boundaries, keys_all)
            obs['H2'] = stat_pool('H2', P, qorder, boundaries, keys_all)
            obs['H3'] = stat_pool('H3', P, qorder, boundaries, keys_all)
            obs['H4'] = stat_pool('H4', P, qorder, boundaries, keys_all)
            json.dump(obs, open(os.path.join(OUT, f'observed_{d}_{T}.json'),'w'), indent=1)
            print(f"OBS {d}/{T}: S1={obs['S1_bits']:.4f}/{obs['S1_share']:.3f} "
                  f"S2={obs['S2']:.4f} S3={obs['S3']:.4f} S4={obs['S4a']:.2f}/{obs['S4b']:.3f} "
                  f"S5={obs['S5']:.1f}% S6={nse}/{nee} S7={obs['S7']:.4f} "
                  f"S8={r2:.3f}/{cv:.2f} S9={a:.3f}/{m1:.3f}/{m0:.3f} "
                  f"H1={obs['H1']:.3f} H2={obs['H2']:.3f} H3={obs['H3']:.3f} H4={obs['H4']:.3f}",
                  flush=True)
            import pickle
            pickle.dump({'P':P,'qorder':qorder,'boundaries':boundaries},
                        open(os.path.join(OUT, f'preload_{d}_{T}.pkl'),'wb'))
            print(f"preload {d}/{T} written ({os.path.getsize(os.path.join(OUT, f'preload_{d}_{T}.pkl'))//1024//1024} MB)", flush=True)

if __name__ == '__main__':
    main()
