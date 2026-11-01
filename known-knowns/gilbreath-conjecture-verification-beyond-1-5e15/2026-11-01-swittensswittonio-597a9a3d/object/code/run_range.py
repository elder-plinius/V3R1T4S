#!/usr/bin/env python
"""Driver: contiguous range of primes >= A (default 1.5e15) up to a prime > B (default 1.6e15); resumable."""
import os, sys, time, json, argparse
import numpy as np, cupy as cp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gil_gpu as g

ap = argparse.ArgumentParser()
ap.add_argument('--A', type=int, default=1_500_000_000_000_000)
ap.add_argument('--B', type=int, default=1_600_000_000_000_000)
ap.add_argument('--NB', type=int, default=1<<30)
ap.add_argument('--out', required=True)
ap.add_argument('--maxwin', type=int, default=10**9)
ap.add_argument('--verify_every', type=int, default=250)
a = ap.parse_args()
os.makedirs(a.out, exist_ok=True)
sp = os.path.join(a.out, 'state.json'); dp = os.path.join(a.out, 'depth.u16'); cpth = os.path.join(a.out, 'carry.npy')
wl = os.path.join(a.out, 'windows.csv'); fp = os.path.join(a.out, 'chunk_first_primes.csv'); vl = os.path.join(a.out, 'selfverify.log')
lo0 = a.A + 1  # first odd number >= A (A even)
assert a.A % 2 == 0
pipe = g.Pipe(NB=a.NB)
M, O = g.M, g.L - g.M
st = dict(w=0, carry=0, chunks=0, cum=0, max_depth=0, max_chunk=-1, flagged=0)
if os.path.exists(sp):
    st = json.load(open(sp))
    c = np.load(cpth); pipe.P[:len(c)] = cp.asarray(c)
    with open(dp, 'r+b') as f: f.truncate(st['chunks']*2)
    with open(os.path.join(a.out, 'clean1280.u8'), 'r+b') as f: f.truncate(st['chunks'])
    print('resumed', st, flush=True)
else:
    open(dp, 'wb').close()
    open(wl, 'w').write('w,lo,nprimes,cum_primes,chunks_done,win_max_depth,win_max_chunk,elapsed_s\n')
    open(fp, 'w').write('chunk,first_prime\n')
rng = np.random.default_rng(12345 + st['w'])
t0 = time.time(); done = False
while not done and st['w'] < a.maxwin:
    w = st['w']; lo = lo0 + 2*a.NB*w
    tw = time.time()
    n = pipe.sieve(lo, st['carry'])
    total = st['carry'] + n
    nch = (total - O - 1)//M
    d = cp.zeros(max(nch,1), dtype=cp.uint16); cl_ = cp.zeros(max(nch,1), dtype=cp.uint8)
    chunk0 = st['chunks']          # global chunk id of local chunk 0
    pipe.rows(nch, 0, d, cl_)
    dh = d[:nch].get(); ch = cl_[:nch].get()
    nunclean = int((ch == 0).sum()); st['unclean'] = st.get('unclean', 0) + nunclean
    with open(os.path.join(a.out, 'clean1280.u8'), 'ab') as f: f.write(ch.tobytes())
    cp.cuda.Stream.null.synchronize()
    nfl = int((dh == 0xFFFF).sum())
    wmax = int(dh[dh != 0xFFFF].max()) if nch and (dh != 0xFFFF).any() else 0
    wchunk = chunk0 + int(np.argmax(np.where(dh == 0xFFFF, 0, dh))) if nch else -1
    with open(dp, 'ab') as f: f.write(dh.tobytes())
    if wmax > st['max_depth']: st['max_depth'] = wmax; st['max_chunk'] = wchunk
    st['flagged'] += nfl
    # first primes of every 4096th global chunk
    idx = [c for c in range(chunk0, chunk0+nch) if c % 4096 == 0]
    if idx:
        fv = pipe.P[cp.asarray([(c-chunk0)*M for c in idx])].get()
        with open(fp, 'a') as f:
            for c, v in zip(idx, fv): f.write(f'{c},{int(v)}\n')
    # in-run independent numpy verification on a few chunks
    if nch > 0 and (w % a.verify_every == 0):
        picks = sorted(set(int(x) for x in rng.integers(0, nch, 3)) | {0})
        for c in picks:
            seg = pipe.P[c*M:c*M+g.L+1].get()
            r = g.ref_depth(seg.astype(np.uint64), 0)
            rc = g.ref_clean(seg.astype(np.uint64), 0); ok = (r == int(dh[c])) and (rc == bool(ch[c]))
            with open(vl, 'a') as f: f.write(f'w={w} chunk={chunk0+c} first_prime={int(seg[0])} gpu={int(dh[c])} numpy={r} clean1280_gpu={int(ch[c])} clean1280_numpy={int(rc)} ok={ok}\n')
            if not ok: print('MISMATCH', w, c, flush=True); sys.exit(2)
    # carry
    cl = total - nch*M
    tmp = pipe.P[nch*M:total].copy(); pipe.P[:cl] = tmp
    st['carry'] = cl; st['chunks'] += nch; st['cum'] += n; st['w'] = w + 1
    lastowned = None
    # termination: first prime of next chunk (start of stream carry) beyond B
    firstcarry = int(pipe.P[0].get())
    el = time.time() - t0
    with open(wl, 'a') as f: f.write(f'{w},{lo},{n},{st["cum"]},{st["chunks"]},{wmax},{wchunk},{el:.1f}\n')
    np.save(cpth + '.tmp.npy', pipe.P[:cl].get()); os.replace(cpth + '.tmp.npy', cpth)
    json.dump(st, open(sp + '.tmp', 'w')); os.replace(sp + '.tmp', sp)
    if w % 50 == 0: print(f'w={w} n={n} chunks={st["chunks"]} maxd={st["max_depth"]} flagged={st["flagged"]} unclean={st.get("unclean",0)} t={el:.0f}s win={time.time()-tw:.3f}s firstcarry={firstcarry}', flush=True)
    if firstcarry > a.B: done = True
print('DONE' if done else 'STOPPED', st, flush=True)
