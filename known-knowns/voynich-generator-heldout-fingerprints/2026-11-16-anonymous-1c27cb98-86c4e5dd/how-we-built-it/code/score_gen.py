#!/usr/bin/env python3
"""Score a generated corpus (list of token lines) on the 14 PREREG statistics and
compare against the frozen envelopes (output/env_*.json) and observed values.

A 'generated corpus' = pooled template-wrapped lines of all runs in a mode.
Generated-text folio proxy = 21-line blocks (PREREG §2 S9); quire proxy for H4 =
the same 21-line blocks (CV of per-block hapax).

Usage (library): score_corpus(lines, cell) -> dict of stats
Usage (cli): python score_gen.py <runs_json> <mode>   (runs_json: {mode: {T: {lines: [[tok,...]]}}})
"""
from __future__ import annotations
import json, os, sys, random, math
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vstats import (collapse, make_greedy, conditional_entropy, mi_bits, entropy,
                    _log2)
from precompute import stat_pool  # reuse the exact same pooling code (keys=sel indices)

RUN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(RUN, 'output')
BLOCK = 21  # generated-text folio/quire proxy (PREREG)

def gen_stat_pool(name, lines, shuffles=100):
    """Compute a PREREG statistic on generated token lines (list of lists of raw tokens).
    Collapses internally; uses the same definitions as the Voynich precompute."""
    # normalize: input may be list-of-lines or a flat list of tokens
    if lines and isinstance(lines[0], str):
        lines = [lines]
    col_lines = [[collapse(w) for w in line if w] for line in lines]
    col_lines = [line for line in col_lines if line]
    raw_lines = [line for line in lines if line]
    INV = make_greedy(json.load(open(os.path.join(OUT, 'paper_graph_inv.json'))))
    if name == 'S3':
        # flat-stream h2 (PREREG): within-token + within-line edge glyph pairs
        pair_c = Counter()
        for line in col_lines:
            for w in line:
                for i in range(len(w)-1):
                    pair_c[(w[i], w[i+1])] += 1
            for a,b in zip(line, line[1:]):
                pair_c[(a[-1], b[0])] += 1
        return conditional_entropy(pair_c)
    if name == 'S1':
        pc = Counter()
        Lc = Counter(); Fc = Counter()
        for line in col_lines:
            for w in line:
                Lc[w[-1]] += 1; Fc[w[0]] += 1
            for a,b in zip(line, line[1:]):
                pc[(a[-1], b[0])] += 1
        mi_obs = mi_bits(pc)
        nullc = Counter()
        for a in Lc:
            for b in Fc:
                nullc[(a,b)] = Lc[a]*Fc[b]
        mi_null = mi_bits(nullc)
        s1b = mi_obs - mi_null
        Hn = entropy(Fc)
        return s1b, (s1b/Hn if Hn>0 else 0.0)
    if name == 'S2':
        freq = Counter(w for line in raw_lines for w in line)
        types = len(freq)
        hap = sum(1 for v in freq.values() if v==1)
        return hap/types if types else 0.0
    if name == 'S4':
        lens = [len(w) for line in raw_lines for w in line]
        if not lens: return 0.0, 0.0
        return (sum(lens)/len(lens), sum(1 for L in lens if L==1)/len(lens))
    if name in ('S5','S7','S6','S8'):
        fl = []
        sc, ec, firstc = Counter(), Counter(), Counter()
        for line in col_lines:
            fl_line = []
            for w in line:
                t = INV(w)
                if not t: continue
                fl_line.append((t[0], t[-1]))
                sc[t[0]] += 1; ec[t[-1]] += 1; firstc[t[0]] += 1
            fl.append(fl_line)
        if name == 'S6':
            nse = sum(1 for g in set(sc)|set(ec) if (sc.get(g,0)+1)/(ec.get(g,0)+1)>100)
            nee = sum(1 for g in set(sc)|set(ec) if (ec.get(g,0)+1)/(sc.get(g,0)+1)>100)
            return nse, nee
        if name == 'S8':
            import numpy as np
            freqs = np.array(sorted(firstc.values(), reverse=True), dtype=float)
            ranks = np.arange(1, len(freqs)+1, dtype=float)
            log_r, log_f = np.log(ranks), np.log(freqs+1e-10)
            pred = np.polyval(np.polyfit(log_r, log_f, 1), log_r)
            ss_res = float(np.sum((log_f-pred)**2)); ss_tot = float(np.sum((log_f-np.mean(log_f))**2))
            r2 = 1.0-ss_res/ss_tot if ss_tot>0 else 0.0
            cv = float(np.std(freqs)/np.mean(freqs)) if np.mean(freqs)>0 else 0.0
            return r2, cv
        # S5 / S7
        cls = {}
        for g in set(sc)|set(ec):
            s,e = sc.get(g,0), ec.get(g,0)
            cls[g] = 'start' if s>2*e else 'end' if e>2*s else 'ambig'
        if name == 'S5':
            es = tot = 0
            for fl_line in fl:
                for i in range(len(fl_line)-1):
                    if cls.get(fl_line[i][1])=='end' and cls.get(fl_line[i+1][0])=='start': es += 1
                    tot += 1
            return 100.0*es/tot if tot else 0.0
        tr = Counter()
        for fl_line in fl:
            for i in range(len(fl_line)-1):
                tr[(fl_line[i][1], fl_line[i+1][0])] += 1
        return mi_bits(tr)
    if name == 'S9':
        fr = []
        for i in range(0, len(col_lines), BLOCK):
            block = col_lines[i:i+BLOCK]
            if not block: continue
            ncho = nche = 0
            for w in (x for line in block for x in line):
                hco = ('Co' in w) or ('So' in w); hce = ('Ce' in w) or ('Se' in w)
                if hco and not hce: ncho += 1
                elif hce and not hco: nche += 1
            if ncho+nche >= 5:
                fr.append(ncho/(ncho+nche))
        if not fr: return 0.0, 0.0, 0.0
        amb = sum(1 for r in fr if 0.3<=r<=0.5)/len(fr)
        cho = [r for r in fr if r>0.5]; che = [r for r in fr if r<=0.5]
        return amb, (sum(cho)/len(cho) if cho else 0.0), (sum(che)/len(che) if che else 0.0)
    if name == 'H1':
        # exact within-line shuffle expectation (PREREG.v2): E[adj edit-1 count]
        # = (1/n) * sum_{a,b} n_a (n_b - [a==b]) lev1(a,b)
        def lev1(a,b):
            la,lb=len(a),len(b)
            if abs(la-lb)>1: return False
            if la==lb:
                d=sum(1 for i in range(la) if a[i]!=b[i]); return d<=1
            if la==lb+1:
                i=j=0;sk=False
                while i<la and j<lb:
                    if a[i]==b[j]: i+=1;j+=1
                    else:
                        if sk: return False
                        sk=True;i+=1
                return True
            i=j=0;sk=False
            while i<la and j<lb:
                if a[i]==b[j]: i+=1;j+=1
                else:
                    if sk: return False
                    sk=True;j+=1
            return True
        obs = 0; nul = 0.0
        for line in col_lines:
            n = len(line)
            obs += sum(1 for a,b in zip(line,line[1:]) if lev1(a,b))
            if n < 2: continue
            m = 0
            for i in range(n):
                for j in range(n):
                    if i!=j and lev1(line[i], line[j]): m += 1
            nul += m / n
        return obs/nul if nul>0 else float('inf')
    if name == 'H2':
        li = Counter(); mi = Counter()
        for line in col_lines:
            if line:
                for i,w in enumerate(line):
                    if i==0: li[w[0]] += 1
                    else: mi[w[0]] += 1
        tp, tq = sum(li.values()), sum(mi.values())
        if tp==0 or tq==0: return 0.0
        m = {k:(li.get(k,0)/tp + mi.get(k,0)/tq)/2.0 for k in set(li)|set(mi)}
        pm = {k:v/tp for k,v in li.items()}; qm = {k:v/tq for k,v in mi.items()}
        def _kl(x,y):
            return sum(vx*_log2(vx/y.get(k,0.0)) for k,vx in x.items() if y.get(k,0.0)>0)
        return 0.5*_kl(pm,m) + 0.5*_kl(qm,m)
    if name == 'H3':
        freq = Counter(w for line in raw_lines for w in line)
        tot = sum(freq.values())
        return (sum(c for _,c in freq.most_common(50))/tot) if tot else 0.0
    if name == 'H4':
        vals = []
        for i in range(0, len(raw_lines), BLOCK):
            block = raw_lines[i:i+BLOCK]
            if len(block) < BLOCK*0.5: continue
            freq = Counter(w for line in block for w in line)
            if not freq: continue
            vals.append(sum(1 for v in freq.values() if v==1)/len(freq))
        if len(vals)<2: return 0.0
        import statistics
        m = statistics.mean(vals)
        return (statistics.pstdev(vals)/m) if m else 0.0
    raise ValueError(name)

def score_all(lines):
    out = {}
    a = gen_stat_pool('S1', lines); out['S1_bits'], out['S1_share'] = a
    out['S2'] = gen_stat_pool('S2', lines)
    out['S3'] = gen_stat_pool('S3', lines)
    a = gen_stat_pool('S4', lines); out['S4a'], out['S4b'] = a
    out['S5'] = gen_stat_pool('S5', lines)
    a = gen_stat_pool('S6', lines); out['S6_Se'], out['S6_Ee'] = a
    out['S7'] = gen_stat_pool('S7', lines)
    a = gen_stat_pool('S8', lines); out['S8_R2'], out['S8_CV'] = a
    a = gen_stat_pool('S9', lines); out['S9_amb'], out['S9_cho'], out['S9_che'] = a
    out['H1'] = gen_stat_pool('H1', lines)
    out['H2'] = gen_stat_pool('H2', lines)
    out['H3'] = gen_stat_pool('H3', lines)
    out['H4'] = gen_stat_pool('H4', lines)
    return out

if __name__ == '__main__':
    lines = [l.split() for l in open(sys.argv[1]).read().splitlines() if l.strip()]
    s = score_all(lines)
    print(json.dumps(s, indent=1))
